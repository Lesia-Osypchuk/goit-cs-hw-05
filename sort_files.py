import asyncio
import os
import shutil
import argparse
from pathlib import Path

async def read_folder(source_folder, output_folder):
    tasks = []
    async for file_path in async_walk(source_folder):
        tasks.append(copy_file(file_path, output_folder))
    await asyncio.gather(*tasks)

async def async_walk(path):
    loop = asyncio.get_event_loop()
    for root, dirs, files in await loop.run_in_executor(None, os.walk, path):
        for file in files:
            yield Path(root) / file

async def copy_file(file_path, output_folder):
    try:
        ext = file_path.suffix[1:]  # Remove the leading dot
        target_folder = Path(output_folder) / ext
        target_folder.mkdir(parents=True, exist_ok=True)
        await asyncio.get_event_loop().run_in_executor(
            None, shutil.copy, file_path, target_folder / file_path.name)
        print(f"Copied {file_path} to {target_folder / file_path.name}")
    except Exception as e:
        print(f"Error copying {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Sort files by extension.')
    parser.add_argument('source_folder', type=str, help='The source folder to read files from')
    parser.add_argument('output_folder', type=str, help='The output folder to copy files to')
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.is_dir():
        print(f"Source folder {source_folder} does not exist or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
