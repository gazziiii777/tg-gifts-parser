import aiohttp
import asyncio


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Получаем статус ответа (например, 200)
            print("Статус:", response.status)

            # Получаем текстовую часть ответа (HTML, JSON и т.п.)
            content = await response.text()
            print("Контент:", content[:500])  # Показываем первые 500 символов

            return content

# Пример вызова
url = "https://t.me/nft/SpyAgaric-50977"

asyncio.run(fetch_url(url))
