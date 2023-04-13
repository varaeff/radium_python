import unittest
import os
import asyncio
import tempfile

from main import download_file, download_head
from unittest.mock import patch


class TestDownloadHead(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(os.getcwd(), 'temp')

    def test_download_head(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        test_hashes = loop.run_until_complete(download_head())
        files = os.listdir(self.temp_dir)
        self.assertIn('main.tar.gz', files)
        self.assertIn('master.tar.gz', files)
        self.assertIn('develop.tar.gz', files)
        self.assertEqual(test_hashes[0], '7b465d085374044b52c029c4abfb6c9864960b438f058dd1cfe4d9b2b29a6665')
        self.assertEqual(test_hashes[1], '866632988a6a1c842f89dc2b1ada66d510f89d86a7054b2d4a0bb8f35be75158')
        self.assertEqual(test_hashes[2], '03f89a62b4ace990d4b55489f806d17b9c01c03e90c1aec7e94e070b15fc9b17')


class TestDownloadFile(unittest.IsolatedAsyncioTestCase):
    async def test_download_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            file_path = f.name
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = mock_get.return_value.__aenter__.return_value
            mock_response.content.read.side_effect = [
                b'some', b' ', b'content', b'']
            mock_response.status = 200
            await download_file('http://example.com/somefile.txt', file_path)
        with open(file_path, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'some content')
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
