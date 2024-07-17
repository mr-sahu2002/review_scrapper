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
        
        for i in range(5):
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
                print(f"Page {i+1}: Extracted {len(reviews)} reviews")
            except Exception as e:
                print(f"Error on page {i+1}: {e}")
                break

            # Check if the "Next" button is disabled
            disabled_next_button = await page.query_selector('li.a-disabled.a-last')
            
            if disabled_next_button:
                print("Next button is disabled, no more pages.")
                break

            # Check if there is a "Next" button
            next_button = await page.query_selector('li.a-last a')
            if next_button:
                try:
                    await next_button.scroll_into_view_if_needed()
                    await next_button.click()
                    print("Clicked on 'Next' button")
                    await page.wait_for_timeout(7000)  # wait for the next page to load
                except Exception as e:
                    print(f"Failed to click 'Next' button on page {i+1}: {e}")
                    break
            else:
                print("No more pages or 'Next' button not found")
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
product_url = 'https://www.amazon.in/Lenovo-IdeaPad-39-62cm-Warranty-82RK006DIN/product-reviews/B0B4JPC8GT/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'  # Replace with the desired product URL
output_file = 'amazon_reviews.csv'
asyncio.run(scrape_amazon_reviews(product_url, output_file))
