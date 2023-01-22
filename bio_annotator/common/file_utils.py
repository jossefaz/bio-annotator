import aiofiles


async def byte_file_iterator(filename):
    async with aiofiles.open(filename, mode='rb') as f:
        while True:
            chunk = await f.read(1024)
            if not chunk:
                break
            yield chunk


