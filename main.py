import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_amazon_reviews(product_url, output_file):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(product_url)
        print(f"Navigated to {product_url}")
        
        all_reviews = []
        
        while True:
            try:
                # Wait for the reviews section to load
                await page.wait_for_selector('.review-text-content', timeout=20000)
                print("Review section loaded")
                
                # Extract review texts
                reviews = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('.review-text-content span')).map(element => element.innerText);
                }''')
                
                all_reviews.extend(reviews)
            #     print(f"Page {i+1}: Extracted {len(reviews)} reviews")
            except Exception as e:
                print(f"Error on page")
                break

            # Check if there is a "Next" button
            prev = await page.query_selector('a[data-hook="see-all-reviews-link-foot"]')
          
            if prev:
                await prev.click()
                print("Clicked on 'see all reviews' link")
                await page.wait_for_timeout(7000)  # wait for the next page to load

           
            disable_button=await page.query_selector('li.a-disabled')
            # await page.evaluate('el => el.scrollIntoView()', disable_button)
            # if disable_button:
            #     break
            next_button = await page.query_selector('li.a-last a')
            await page.evaluate('el => el.scrollIntoView()', next_button)
            if next_button:
                if disable_button:
                    await next_button.click()
                    print("Clicked on 'Next' button")
                    await page.wait_for_timeout(7000)  # wait for the next page to load
                else:
                    print("Next button is disabled")
                    break
            else:
                print("No more pages")
                break
        
        # Close the browser
        await browser.close()
        print("Browser closed")
        
        # Save reviews to a CSV file
        save_to_csv(all_reviews, output_file)
        print(f"Saved {len(all_reviews)} reviews to {output_file}")

def save_to_csv(reviews, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Review'])
        for review in reviews:
            writer.writerow([review])

# Run the script with the desired product URL and output file name
product_url = 'https://www.amazon.in/Lenovo-IdeaPad-39-62cm-Warranty-82RK006DIN/dp/B0B4JPC8GT/ref=sr_1_3?crid=3QIFA2FF5FUYI&dib=eyJ2IjoiMSJ9.vnDW-T-yAMIwGr9xXt1G_JveWcg0TyH4zSvHz5x2MpL-NnE_GZ-c_ueIcfSGtArnNabyXfAXImI-P9TIhRZe6RKS4bo2tuC2A3mYAOlXKoNOQtB4Pm4KqscdiHWNISBpok8iP1Lvfdb32zGERgM6drlV_-09k0FTT4a6S8STXjlZbYdyrNuzpyvDs63p5Kcv3Zuu5fzBBKd06MudeT1CNw85XnUN1S4EcjNXb807rzc.uO4vGo1oLac_HOQv4rjDRgLcQTCsDuP3ou_S5UdkaDg&dib_tag=se&keywords=lenovo%2Blaptops&qid=1720365881&sprefix=len%2Caps%2C314&sr=8-3&th=1'  # Replace with the desired product URL
output_file = 'amazon_reviews.csv'
asyncio.run(scrape_amazon_reviews(product_url, output_file))
