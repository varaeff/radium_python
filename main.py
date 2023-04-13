import asyncio
import hashlib
import os

import aiohttp


async def download_file(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)


async def download_head():
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    urls = [
        'https://gitea.radium.group/radium/project-configuration/archive/refs/heads/main.tar.gz',
        'https://gitea.radium.group/radium/project-configuration/archive/refs/heads/master.tar.gz',
        'https://gitea.radium.group/radium/project-configuration/archive/refs/heads/develop.tar.gz',
    ]

    tasks = []
    for url in urls:
        file_path = os.path.join(temp_dir, url.split('/')[-1])
        tasks.append(download_file(url, file_path))

    await asyncio.gather(*tasks)

    file_hashes = []
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            file_hashes.append(file_hash)

    return file_hashes


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hashes = loop.run_until_complete(download_head())
    print('hashes:')
    for curr_hash in hashes:
        print(curr_hash)
