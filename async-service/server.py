from aiohttp import web
import asyncio
import aiofiles
import datetime
import os
import logging


THROTTLING_TICS = 0


logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename=u'photo_archive_log.log'
)


INTERVAL_SECS = 1


async def archive(request):
    archive_hash = request.match_info.get('archive_hash')
    if not os.path.exists(os.path.join('test_photos', archive_hash)):
        raise web.HTTPNotFound(text=f'404: Архив {archive_hash} не существует или был удален')
    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_hash}.zip"'
    response.headers['Content-Type'] = 'application/zip'

    await response.prepare(request)

    proc = await asyncio.create_subprocess_exec(
        'zip', '-r', '-', f'{archive_hash}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd='test_photos'
    )
    try:
        while not proc.stdout.at_eof():
            archive_data = await proc.stdout.read(100000)
            logging.info(msg=f'Sending archive chunk {archive_hash}')
            await asyncio.sleep(THROTTLING_TICS)
            await response.write(archive_data)
    finally:
        logging.error(msg='Download was interrupted')
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


async def uptime_handler(request):
    response = web.StreamResponse()

    # Большинство браузеров не отрисовывают частично загруженный контент, только если это не HTML.
    # Поэтому отправляем клиенту именно HTML, указываем это в Content-Type.
    response.headers['Content-Type'] = 'text/html'

    # Отправляет клиенту HTTP заголовки
    await response.prepare(request)

    while True:
        formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f'{formatted_date}<br>'  # <br> — HTML тег переноса строки

        # Отправляет клиенту очередную порцию ответа
        await response.write(message.encode('utf-8'))

        await asyncio.sleep(INTERVAL_SECS)


if __name__ == '__main__':
    data = b''
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
        web.get('/archive/7kna', uptime_handler)
    ])
    web.run_app(app)
