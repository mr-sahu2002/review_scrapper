from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pydantic import ValidationError
from analyze import get_sentiment
from scrapper import get_reviews
import asyncio

app = Flask(__name__)
CORS(app)

# Using a simple class to mock Pydantic's BaseModel for validation
class ProductRequest:
    def __init__(self, product_name: str):
        self.product_name = product_name

@app.route('/scrape-review', methods=['POST'])
def scrape_review():
    try:
        data = request.json
        product_request = ProductRequest(**data)
    except (TypeError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400

    product = product_request.product_name
    # Run the async function in a synchronous context
    asyncio.run(get_reviews(product))
    df = pd.read_csv(f'product_reviews/{product}.csv')
    arr_reviews = df.values
    sentiment=get_sentiment(arr_reviews)
    return sentiment

if __name__ == '__main__':
    app.run(debug=True)
