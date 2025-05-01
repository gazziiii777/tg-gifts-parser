import aiohttp
import asyncio
from bs4 import BeautifulSoup
from logging_config import setup_logger

logger = setup_logger('parcer')


class Parcer:
    def __init__(self):
        self.session = None
        self.trigger_phrase = "Gift"  # Замените на нужную фразу

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def fetch(self, num: str, url: str) -> bool:
        async with self.session.get(url + num) as response:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string if soup.title else ''
            if self.trigger_phrase.lower() in title.lower():
                print(title.lower())
                return url + num
            else:
                logger.info(f"❌ Словосочетание не найдено в title. url: {url+num}")
                return False

    async def parcer_start():
        pass
# Пример использования


# async def main():
#     url_suffix = "50977"
#     async with Parcer() as fetcher:
#         result = await fetcher.fetch(url_suffix)
#         print("Результат проверки:", result)

# asyncio.run(main())
