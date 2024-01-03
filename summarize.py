from pyppeteer import launch
import google.generativeai as palm
import asyncio
import config
import os
import openai

import pandas as pd

import time
openai.api_key = 'YOUR_API_KEY'

url = "TYPE_URL_HERE" #Go to reviews page on google maps and add the link here

async def scrape_reviews(url):
    reviews = []
    browser = await launch({"headless": False, "args":["--window-size=800,3200"]})

    page = await browser.newPage()

    try:
        await page.setViewport({"width": 800, "height":3200})
        await page.goto(url)
        await page.waitForSelector('.jJc9Ad ')
    except:
        pass
    
    elements = await page.querySelectorAll('.jJc9Ad ')
    for element in elements:
        try:
            await page.waitForSelector(".w8nwRe")
            more_btn = await element.querySelector(".w8nwRe")
            
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(5000)
        except:
            pass
        
        try:
            await page.waitForSelector('.wiI7pd', timeout=60000)  # Increase the timeout period
            snippet = await element.querySelector('.wiI7pd')
            text = await page.evaluate('selected => selected.textContent', snippet)
            reviews.append(text)
        except:
            print("can t scrape")
        
    await browser.close()
    
    return reviews
    
    
reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))


def summarize_reviews(reviews):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{reviews}"},
            {"role": "assistant", "content": "I am here to help you summarize the reviews."},
        ]
    )
    return response['choices'][0]['message']['content']

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
summary = summarize_reviews(reviews)
print(summary)



    
    




