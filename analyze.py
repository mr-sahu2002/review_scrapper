import os
from groq import Groq
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()

# convert the .csv to array of reviews
df = pd.read_csv(r'product_reviews/lenovo ideapad 3.csv')
arr_reviews = df.values

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_sentiment(arr_reviews):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{arr_reviews} \n give me the sentimental analysis of the input array, the output should        be a array of the reviews sentiment (postive=1,negative=-1,netural=0)"+"array of the sentiments return in -1,0,1 format, for ex:[1,0,-1,0,1,0]"+"only give the output array no explaination",
            }
        ],
        model="llama3-8b-8192",
        temperature=0.1,
    )

    response = chat_completion.choices[0].message.content

    ## get the sentimental array form the response
    match = re.search(r'\[([-0-9, ]+)\]', response)

    if match:
        array_string = match.group(1)
        sentiment_array = list(map(int, array_string.split(',')))
        return sentiment_array
    else:
        return "not found!!!"