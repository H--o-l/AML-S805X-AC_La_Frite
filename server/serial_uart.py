#!/usr/bin/env python3
import serial_asyncio
import asyncio
import logging


logger = logging.getLogger(__name__)


input_buffer = ''
transport = None


class Protocol_factory(asyncio.Protocol):
    # def connection_made(self, transport):
    #     logger.info('connection_made')
    # def connection_lost(self, exc):
    #     logger.info('connection_lost')

    def data_received(self, data):
        # global input_buffer
        # try:
        #     input_buffer += data.decode('utf-8')
        # except UnicodeDecodeError:
        #     logger.warning(f'reception error type 1, {data}')
        #     input_buffer = ''
        # if len(input_buffer) > 1 and input_buffer[-1] == '\n':
        #     input_buffer_copy = input_buffer[:]
        #     input_buffer = ''
        #     arduino_data_received(input_buffer_copy)
        try:
            arduino_data_received(data.decode('utf-8'))
        except UnicodeDecodeError:
            logger.warning(f'Reception error type 1, {data}')


def arduino_data_received(str):
    if str == 'F':
        logger.info("Fio is OK")
    elif str == 'S':
        logger.info("Shield is OK")
    else:
        try:
            value = int(str)
            event_from_shield(value)
        except:
            logger.warning(f'Reception error type 2: {str}')


def event_from_shield(value):
    global transport
    transport.write(b'A')
    logger.info(f'From shield: {value}')


async def init(app):
    global transport
    global alive
    try:
        loop = asyncio.get_event_loop()
        # 115200 doesn't work
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop, Protocol_factory, '/dev/ttyAMA0', baudrate=9600)

        # transport.write(b'F')
        # await asyncio.sleep(.2)
        # transport.write(b'S')
        # await asyncio.sleep(60 * 15)
    except asyncio.CancelledError:
        pass
    finally:
        pass
