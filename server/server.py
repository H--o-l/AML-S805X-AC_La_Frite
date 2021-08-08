#!/usr/bin/env python3

from aiohttp import web
import logging
from aioinflux import InfluxDBClient
import asyncio

import serial_uart


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()


@routes.get('/')
async def home(req):
    text = "Hello world\n"
    return web.Response(text=text)

@routes.post('/knocki')
async def knocki(req):
    data = await req.json()
    logger.info(f'knocki {data}')
    return web.json_response({'ok': True})


@routes.post('/wio_link_sensors')
async def wio_link_sensors(req):
    data = await req.json()
    points = []
    for key, value in data.items():
        points.append({
            'measurement': key,
            'tags': {'origin': 'wio_link'},
            'fields': {'value': value}
        })
    if points:
        async with InfluxDBClient(db='sensors') as client:
            await client.create_database(db='sensors')
            await client.write(points)
    return web.json_response({'ok': True})


@routes.get('/fio')
async def fio(req):
    logger.info('Fio')
    serial_uart.transport.write(b'F')
    return web.json_response({'ok': True})


@routes.get('/shield')
async def shield(req):
    logger.info('Shield')
    serial_uart.transport.write(b'S')
    return web.json_response({'ok': True})


app = web.Application()
app.router.add_routes(routes)


def _handle_background_tasks_result(task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception:
        logging.exception('Exception raised by task = %r', task)
        app.loop.stop()


async def start_background_tasks(app):
    loop = asyncio.get_event_loop()
    app['serial_background'] = loop.create_task(serial_uart.init(app))
    app['serial_background'].add_done_callback(_handle_background_tasks_result)


async def cleanup_background_tasks(app):
    app['serial_background'].cancel()
    await app['serial_background']


app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == '__main__':
    logger.info('Server ready')
    web.run_app(app, port=6000)
