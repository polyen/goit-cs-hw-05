import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile


class NoSourceFolderFoundException(Exception):
    pass


class CannotCreateFolderException(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description='Sort files by extension')
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-o', '--output', required=True)

    return vars(parser.parse_args())


async def init_folders(paths):
    source_path = AsyncPath(paths['source'])
    output_path = AsyncPath(paths['output'])

    if not await source_path.exists():
        raise NoSourceFolderFoundException

    if not await output_path.exists() or not await output_path.is_dir():
        try:
            await output_path.mkdir(parents=True, exist_ok=True)
        except Exception:
            raise CannotCreateFolderException

    return source_path, output_path


async def copy_file(p: AsyncPath, out: AsyncPath):
    ext = p.suffix.replace('.', '')

    if not ext:
        ext = 'NoExtension'

    ext_path = out.joinpath(f'{ext}')

    try:
        if not await ext_path.exists():
            await ext_path.mkdir(exist_ok=True)
        await copyfile(p, ext_path.joinpath(p.name))
    except Exception:
        print('Error occurs while copying file ', p.name)


async def read_folder(source_path: AsyncPath, output_path):
    async for p in source_path.iterdir():
        try:
            if await p.is_dir():
                await read_folder(p, output_path)
            else:
                print('Copy file: ', p.name)
                await copy_file(p, output_path)
        except Exception:
            print('Something went wrong with ', p.name)


async def main():
    paths = parse_args()
    try:
        source_path, output_path = await init_folders(paths)
        await read_folder(source_path, output_path)
    except NoSourceFolderFoundException:
        print(f'Folder {paths["source"]} not found')
    except CannotCreateFolderException:
        print(f'Cannot create folder {paths["output"]}')


if __name__ == "__main__":
    asyncio.run(main())
