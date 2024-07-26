import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def archive():
    proc = await asyncio.create_subprocess_exec(
        "zip", "-r - media",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.stdout.read()


async def main():
    # task1 = asyncio.create_task(
    #     say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))
    asyncio.create_task(archive())

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    # for i in range(3):
    #     await archive()
    # await task2

    print(f"finished at {time.strftime('%X')}")


# async def main():
#     await asyncio.gather(
#         run("zip -r - media"),
#         run('sleep 1'))

asyncio.run(main())
