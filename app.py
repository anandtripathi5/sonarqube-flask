import asyncio
import time
from random import randint
import httpx
from flask import Flask


app = Flask(__name__)


# function converted to coroutine
async def get_xkcd_image(session):
    random = randint(0, 300)
    result = await session.get(f'http://xkcd.com/{random}/info.0.json') # dont wait for the response of API
    return result.json()['img']


# function converted to coroutine
async def get_multiple_images(number):
    async with httpx.AsyncClient() as session: # async client used for async functions
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True) # gather used to collect all coroutines and run them using loop and get the ordered response
    return result


@app.get('/comic')
async def hello():
    start = time.perf_counter()
    urls = await get_multiple_images(5)
    end = time.perf_counter()
    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


if __name__ == '__main__':
    app.run(debug=True)
