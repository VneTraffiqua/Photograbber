import time
import asyncio


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def archive():
    proc = await asyncio.create_subprocess_exec(
        'zip', '-r - media',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    await proc.stdout.read()
    # return proc
    # stdout, stderr = await proc.read(n=-1)
    #
    # if stdout:
    #     print(f'[stdout]\n{stdout.decode()}')
    # if stderr:
    #     print(f'[stderr]\n{stderr.decode()}')


async def main(process):
    while not process.stdout.at_eof():
        task1 = asyncio.create_task(process.read(100000))

    # task2 = asyncio.create_task(
    #     archive())

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    # await task1
    # await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main(archive()))
