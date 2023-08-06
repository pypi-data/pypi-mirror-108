import aiohttp
import asyncio
import async_timeout
import msgpack
from datetime import datetime
import uuid as uuid_pkg
import traceback
from functools import partial
from io import BytesIO

from .events import DuctConnectionEvent, DuctMessageEvent
from .event_listeners import ConnectionEventListener

import logging
logger = logging.getLogger(__name__)

class DuctException(Exception):
    pass

class CallTimeout(DuctException):
    def __init__(self, future):
        super().__init__()
        self.future = future

class Dummy:
    
    def __getitem__(self, key):
        raise ValueError('Duct not opened.')
   
class Duct:
    def __init__(self):
        self.WSD = None
        self.EVENT = Dummy()
        self._ws = None
        self._last_rid = 0
        self._loop_future = None
        self._open_wait_lock = asyncio.Condition()
        self._futures = {}
        self._loop_queues = {}
        self._divided_buffers = {}

        self.connection_listener = ConnectionEventListener()
        self._event_handler = {}

    def next_rid(self):
        next_id = int(datetime.now().timestamp())
        if next_id <= self._last_rid:
            next_id = self._last_rid + 1
        self._last_rid = next_id
        return next_id

    async def _start_event_loop(self, reconnect = False):
        if self._loop_future is not None and not self._loop_future.done():
            raise asyncio.InvalidStateError('EventLoop is still running')

        self._ws = None
        self._loop_future = asyncio.ensure_future(self._run(reconnect))
        def done_callback(task):
            err = self._loop_future.exception()
            self._loop_future = None
            self._ws = None
            if err is not None:
                asyncio.ensure_future(self.connection_listener.onerror(DuctConnectionEvent("onerror", err)))
            asyncio.ensure_future(self._onclose())
        self._loop_future.add_done_callback(done_callback)

        while self._ws is None and (self._loop_future is not None and not self._loop_future.done()):
            try:
                async with async_timeout.timeout(5) as cm:
                    async with self._open_wait_lock:
                        await self._open_wait_lock.wait()
            except asyncio.TimeoutError as e:
                pass
        #print(self._ws)
        
    async def _run(self, reconnect = False):
        try :
            async with aiohttp.ClientSession() as session:
                #print(session)
                if reconnect:
                    connect_url = self.WSD["websocket_url_reconnect"]
                else:
                    async with session.get(self.wsd_url + self.query) as resp:
                        self.WSD = await resp.json()
                        self.EVENT = self.WSD["EVENT"]
                    connect_url = self.WSD["websocket_url"]
                async with session.ws_connect(connect_url) as ws:
                    #print(ws)
                    event = "someevent"  # FIXME
                    
                    self._ws = ws
                    
                    if reconnect:  await self._onreconnect(event)
                    else:          await self._onopen(event)

                    await self.connection_listener.onopen(DuctConnectionEvent("onopen", event))
                    async with self._open_wait_lock:
                        self._open_wait_lock.notify_all()
                    await self._onmessage_loop(ws)
        finally:
            async with self._open_wait_lock:
                self._open_wait_lock.notify_all()

    async def open(self, wsd_url, uuid=None, params=None):
        if self._ws:
            return

        self.wsd_url = wsd_url  # check
        self.query = f"?uuid={uuid}" if uuid else f"?uuid={uuid_pkg.uuid4()}"
        
        if params:
            for key,val in params: self.query += f"&{key}={val}"

        await self._start_event_loop()

    async def reconnect(self):
        if self._ws:
            return
        await self._start_event_loop(reconnect=True)

    async def send(self, rid, eid, data):
        data_msgpack = msgpack.packb([rid, eid, data])
        await self._ws.send_bytes(data_msgpack)
        return rid
        
    async def call(self, eid, data = [], timeout = 10):
        rid = self.next_rid()
        data_msgpack = msgpack.packb([rid, eid, data])
        future = asyncio.get_event_loop().create_future()
        self._futures[rid] = future
        await self._ws.send_bytes(data_msgpack)
        try:
            async with async_timeout.timeout(timeout) as cm:
                return await future
        except asyncio.TimeoutError as e:
            raise CallTimeout(future)

    async def close(self):
        try:
            if self._ws:
                await self._ws.close()
                await self._onclose()
        finally:
            self._ws = None
        
    def set_event_handler(self, event_id, handler):
        self._event_handler[event_id] = handler

    async def catchall_event_handler(self, rid, eid, data):
        pass

    async def uncaught_event_handler(self, rid, eid, data):
        pass

    async def event_error_handler(self, rid, eid, data, error):
        pass

    @property
    def state(self):
        if self._ws:  return self._ws.ready_state  #FIXME ready_state is probably not available in aiohttp
        else:         return State.CLOSE

    async def _onopen(self, event):
        self._send_timestamp = datetime.now().timestamp()
        self.time_offset = 0
        self.time_latency = 0
        self._time_count = 0
        self.set_event_handler(self.EVENT["ALIVE_MONITORING"], self._alive_monitoring_handler)
        self.set_event_handler(self.EVENT["LOOP_RESPONSE_START"], self._loop_response_handler)
        self.set_event_handler(self.EVENT["LOOP_RESPONSE_NEXT"], self._loop_response_handler)
        self.set_event_handler(self.EVENT["LOOP_RESPONSE_END"], self._loop_response_end_handler)
        self.set_event_handler(self.EVENT["DIVIDED_RESPONSE_APPEND"], self._divided_response_append_handler)
        self.set_event_handler(self.EVENT["DIVIDED_RESPONSE_END"], self._divided_response_end_handler)
        rid = self.next_rid()
        eid = self.EVENT["ALIVE_MONITORING"]
        value = self._send_timestamp
        await self.send(rid, eid, value)
        await self.onopen(event)

    async def _onclose(self):
        await self.onclose()

    async def onopen(self, event):
        pass

    async def onclose(self):
        pass

    async def _onreconnect(self, event):
        print("reconnected")

    async def _onmessage_loop(self, ws):
        async for msg in ws:
            try:
                if msg.type==aiohttp.WSMsgType.CLOSE:
                    await self.connection_listener.onclose(DuctConnectionEvent("onclose", msg))
                    break

                elif msg.type==aiohttp.WSMsgType.BINARY:
                    rid, eid, data = msgpack.unpackb(msg.data)
                    #print(f'####################{rid}-{eid}')
                    #print(f'####################{rid}-{eid}-{data}')
                    await self.connection_listener.onmessage(DuctMessageEvent(rid,eid,data))
                    try:
                        await self.catchall_event_handler(rid, eid, data)
                        handle = self._event_handler[abs(eid)] if eid in self._event_handler else self.uncaught_event_handler
                        ret = await handle(rid, eid, data)
                        if ret:
                            await self._handle_request_future(*ret)
                        else:
                            await self._handle_request_future(rid, eid, data)
                    except Exception as e:
                        await self.event_error_handler(rid, eid, data, e)
            except Exception as e:
                await self.event_error_handler(-1, -1, None, e)

    async def _handle_request_future(self, rid, eid, data):
        future = self._futures.pop(rid, None)
        if future:
            if eid > 0:
                future.set_result(data)
            else:
                try:
                    future.set_exception(eval(data))
                except Exception as e:
                    traceback.print_stack()
                    future.set_exception(Exception(data))
        

    async def _alive_monitoring_handler(self, rid, eid, data):
        client_received = datetime.now().timestamp()
        server_sent = data[0]
        server_received = data[1]
        client_sent = self._send_timestamp
        new_offset = ((server_received - client_sent) - (client_received - server_sent))/2
        new_latency = ((client_received - client_sent) - (server_sent - server_received))/2
        self.time_offset = (self.time_offset * self._time_count + new_offset) / (self._time_count + 1)
        self.time_latency = (self.time_latency * self._time_count + new_latency) / (self._time_count + 1)
        self._time_count += 1

    async def _loop_response_handler(self, rid, eid, data):
        #print(f'1!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]-[{data}]')
        source_eid = data[1]
        source_data = data[2]
        await self.catchall_event_handler(rid, source_eid, source_data)
        handle = self._event_handler[abs(source_eid)] if source_eid in self._event_handler else self.uncaught_event_handler
        await handle(rid, source_eid, source_data)

        queue = self._loop_queues.get(rid, None)
        if queue is None:
            queue = asyncio.Queue()
            self._loop_queues[rid] = queue

        #print(f'2!!!!!!!!!!!!!!!!!!!!!!!![{source_eid}]-[{source_data}]')
        if source_data is not None:
            await queue.put(source_data)
        return rid, source_eid, queue
    
    async def _loop_response_end_handler(self, rid, eid, data):
        #print(f'3!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]-[{data}]')
        source_eid = data[1]
        source_data = data[2]
        await self.catchall_event_handler(rid, source_eid, source_data)
        handle = self._event_handler[abs(source_eid)] if source_eid in self._event_handler else self.uncaught_event_handler
        await handle(rid, source_eid, source_data)
            
        queue = self._loop_queues.pop(rid, None)
        #print(f'4!!!!!!!!!!!!!!!!!!!!!!!![{source_eid}]-[{source_data}]-[{queue}]')
        if queue is not None:
            await queue.put(None)
        if source_data:
            logger.warn('LOOP|RESPONSE_END_HANDLER|DATA_IGNORED|DATA=%s', source_data)

        return rid, source_eid, source_eid
    
    async def _divided_response_append_handler(self, rid, eid, data):
        #print(f'1!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]-[{len(data)}]')
        bio = self._divided_buffers.get(rid, None)
        if bio is None:
            bio = BytesIO()
            self._divided_buffers[rid] = bio
        #print(f'1.5!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]-[{len(bio.getvalue())}]')
        if data:
            bio.write(data)
        #print(f'2!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]-[{len(bio.getvalue())}]')
        return -1, eid, None

    
    async def _divided_response_end_handler(self, rid, eid, data):
        #print(f'3!!!!!!!!!!!!!!!!!!!!![{rid}]-[{eid}]')
        bio = self._divided_buffers.pop(rid, None)
        if bio is not None:
            if data is not None:
                bio.write(data)
            data = bio.getvalue()

        if data is None:
            logger.warn('DIVIDED|RESPONSE_END_HANDLER|DATA_IGNORED|DATA=%s', data)
            
        rid, source_eid, source_data = msgpack.unpackb(data)
        #print(f'4!#################################![{rid}]-[{source_eid}]-[{len(source_data)}]')
        await self.catchall_event_handler(rid, source_eid, source_data)
        handle = self._event_handler[abs(source_eid)] if source_eid in self._event_handler else self.uncaught_event_handler
        await handle(rid, source_eid, source_data)
        return rid, source_eid, source_data
        
