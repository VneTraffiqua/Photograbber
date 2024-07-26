import asyncio
import time


# async def archive(cmd="zip -r - media"):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)
#     await asyncio.sleep(0)


a = b'\x04'
b = b'\x00'
print(a+b, type(a), type(b))

