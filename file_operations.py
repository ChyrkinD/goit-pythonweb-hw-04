import asyncio

from aiopath import AsyncPath
from aioshutil import copyfile

from logger import logger


async def copy_file(file: AsyncPath, output: AsyncPath):
    try:
        extension = file.suffix.lower().strip(".") or "no_extension"
        target_dir = output / extension
        await target_dir.mkdir(exist_ok=True, parents=True)
        target_file = target_dir / file.name
        await copyfile(file, target_file)
        logger.info(f"File {file.name} copy to {target_file}.")
    except Exception as error:
        logger.error(f"Failed to copy file **{file.name}** (Source: {file}): {error}")


async def read_file(source_path: AsyncPath, output_path: AsyncPath):
    tasks = [
        copy_file(path, output_path)
        async for path in source_path.rglob("*")
        if await path.is_file()
    ]

    if not tasks:
        logger.info("No files found to copy.")
        return

    await asyncio.gather(*tasks, return_exceptions=True)
