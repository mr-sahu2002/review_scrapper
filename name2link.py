from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

API_Key=os.getenv('TAVILY_API')
tavily_client = TavilyClient(api_key=API_Key)

def get_link(product_name):
    response = tavily_client.search(product_name + "reviews", max_results=2, include_domains=['https://www.amazon.in/'])
    links=[result['url'] for result in response['results']]
    return links