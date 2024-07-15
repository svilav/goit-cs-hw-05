import argparse
import asyncio
import logging
from pathlib import Path

from aiofiles import open as aio_open

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(src, dst_folder):
    try:
        dst_folder.mkdir(parents=True, exist_ok=True)
        async with aio_open(src, 'rb') as f_src:
            data = await f_src.read()
        dst_file = dst_folder / src.name
        async with aio_open(dst_file, 'wb') as f_dst:
            await f_dst.write(data)
        logging.info(f"Copied: {src} to {dst_file}")
    except Exception as e:
        logging.error(f"Failed to copy {src} to {dst_folder}: {e}")


async def read_folder(src_folder, dst_folder):
    tasks = []
    for item in src_folder.iterdir():
        if item.is_dir():
            tasks.append(asyncio.create_task(read_folder(item, dst_folder)))
        else:
            ext = item.suffix[1:]  # Remove leading dot from extension
            ext_folder = dst_folder / ext
            tasks.append(asyncio.create_task(copy_file(item, ext_folder)))
    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description='Sort files by extension into designated folders.')
    parser.add_argument('source', type=str, help='Source folder')
    parser.add_argument('destination', type=str, help='Destination folder')
    args = parser.parse_args()

    src_path = Path(args.source)
    dst_path = Path(args.destination)

    if not src_path.is_dir():
        logging.error(f"Source folder {src_path} does not exist.")
        return

    # Run the asynchronous read_folder function
    asyncio.run(read_folder(src_path, dst_path))


if __name__ == '__main__':
    main()
