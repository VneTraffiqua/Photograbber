import asyncio
import time


async def archive(cmd="zip -r - media"):
    global data
    proc = await asyncio.create_subprocess_exec(
        'zip', '-r', '-', 'media',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        data += await proc.stdout.read(100000)
    return data


async def main():
    task1 = asyncio.create_task(
        archive())

    print(f"started at {time.strftime('%X')}")
    s = await task1
    print(type(s))
    with open('media_test.zip', "wb") as file:
        file.write(bytes(s))
    print(f"finished at {time.strftime('%X')}")

if __name__ == '__main__':
    data = b''
    asyncio.run(main())
