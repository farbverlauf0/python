import asyncio
import aiohttp
import time


def save_img(content, path):
	with open(path, 'wb') as f:
		f.write(content)

async def download_img(url, path, client):
	async with client.get(url) as response:
		save_img(await response.content.read(), path)

async def download_all_imgs(sites, path):
  async with aiohttp.ClientSession() as client:
		tasks = []
		for i, url in enumerate(sites):
			task = asyncio.create_task(download_img(url, path + 'img{}.jpg'.format(i), client))
			tasks.append(task)
		try:
			await asyncio.gather(*tasks, return_exceptions=True)
		except Exception as e:
			print(repr(e))

async def main():
	sites = ['https://picsum.photos/200'] * int(input())
	path = 'C:/Users/dmvik/Desktop/imgs/'
	start = time.time()
	await download_all_imgs(sites, path)
	print(f'Time: {time.time() - start}s')


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
