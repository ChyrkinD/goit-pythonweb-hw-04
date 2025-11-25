import asyncio
from argparse import ArgumentParser

from aiopath import AsyncPath

from file_operations import read_file
from logger import logger


async def main():
    parser = ArgumentParser(description="A scrypt to sorted your files")
    parser.add_argument(
        "--source", type=str, default="source", help="Folder that needs to be sorted"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Folder where sorted files will be copied",
    )

    args = parser.parse_args()
    source_path = AsyncPath(args.source)
    output_path = AsyncPath(args.output)

    if not await source_path.exists():
        logger.exception("Source path doesn't exist!")
        return

    if not await output_path.exists():
        logger.exception("Output path doesn't exist!")
        logger.info("Create output path.")
        await output_path.mkdir(exist_ok=True, parents=True)

    await read_file(source_path, output_path)


if __name__ == "__main__":
    asyncio.run(main())
