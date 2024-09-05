from aiohttp import web
import asyncio
import aiofiles
import os
import logging
import argparse


BYTES=100000


logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    filename=u'photo_archive_log.log'
)


async def archive(request):
    global args

    archive_hash = request.match_info.get('archive_hash')
    if not os.path.exists(os.path.join(args.path, archive_hash)):
        raise web.HTTPNotFound(text=f'404: Архив {archive_hash} не существует или был удален')
    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_hash}.zip"'
    response.headers['Content-Type'] = 'application/zip'

    await response.prepare(request)

    proc = await asyncio.create_subprocess_exec(
        'zip', '-r', '-', f'{archive_hash}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=args.path
    )
    try:
        while not proc.stdout.at_eof():
            archive_data = await proc.stdout.read(BYTES)
            logging.info(msg=f'Sending archive chunk {archive_hash}')
            await asyncio.sleep(args.sleep)
            await response.write(archive_data)
    except ConnectionResetError:
        logging.error(msg='ConnectionResetError. Download was interrupted')
    except BaseException:
        logging.error(msg='SystemExit. Download was interrupted')
    finally:
        proc.kill()
        await proc.communicate()
    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Photograbber',
        description='Microservice for downloading files',
        add_help=True
    )

    parser.add_argument('-l', '--logging', action='store_true', default=False, help='logs usage')
    parser.add_argument('-s', '--sleep', type=int, default=0, help='response delay')
    parser.add_argument('-p', '--path', type=str, default='test_photos', help='path to the photo folder')
    args = parser.parse_args()


    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app)
