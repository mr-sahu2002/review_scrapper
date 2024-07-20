import asyncio
import csv
from playwright.async_api import async_playwright
from name2link import get_link

async def scrape_amazon_reviews(product_url, output_file):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(product_url)
        print(f"Navigated to {product_url}")
        
        all_reviews = []
        

        try:
            # Wait for the reviews section to load
            await page.wait_for_selector('.review-text-content', timeout=20000)
            print("Review section loaded")
            
            # Extract review texts, excluding those containing images or videos
            reviews = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.review-text-content')).filter(element => {
                    return element.querySelector('img') === null && element.querySelector('video') === null;
                }).map(element => element.innerText);
            }''')
            
            all_reviews.extend(reviews)
            
        except Exception as e:
            print(f"Error: {e}")
    
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

async def get_reviews(product_name):
    # product_name='lenovo ideapad 3'
    product_url = get_link(product_name)[0] 
    file_path='product_reviews/'
    output_file = f'{file_path}{product_name}.csv'
    await scrape_amazon_reviews(product_url, output_file)