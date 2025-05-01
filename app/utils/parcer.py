import aiohttp
import asyncio


class AsyncFetcher:
    def __init__(self):
        self.session = None
        self.SpyAgaric_url = "https://t.me/nft/SpyAgaric-"
        self.trigger_phrase = "Gift"  # Замените на нужную фразу

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def fetch(self, num: str) -> bool:
        async with self.session.get(self.SpyAgaric_url + num) as response:
            content = await response.text()
            if self.trigger_phrase.lower() in content.lower():
                return self.SpyAgaric_url + num
            else:
                print("❌ Словосочетание не найдено.")
                return False

# Пример использования


async def main():
    url_suffix = "50977"
    async with AsyncFetcher() as fetcher:
        result = await fetcher.fetch(url_suffix)
        print("Результат проверки:", result)

asyncio.run(main())
