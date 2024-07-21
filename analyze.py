import os
from groq import Groq
import pandas as pd
import re
from dotenv import load_dotenv
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
load_dotenv()

# convert the .csv to array of reviews
df = pd.read_csv(r'product_reviews/iphone 15.csv')
arr_reviews = df.values

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_sentiment(arr_reviews,flag):
    if flag == 0:
        context=f"{arr_reviews} \n give me the sentimental analysis of the input array, the output should be a array of the reviews sentiment (postive=1,negative=-1,neutral=0)"+"array of the sentiments return in -1,0,1 format, for ex:[1,0,-1,0,1,0]"+"only give the output array no explaination"
    elif flag == 1:
        context=f"{arr_reviews} \n give me summary on the above array of reviews as one paragraph (within 100 words)"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": context,
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
        return response


##############  wordcloud code ###############
def generate_word_cloud(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Define a pattern to remove special characters
    def remove_pattern(input_txt, pattern):
        r = re.findall(pattern, input_txt)
        for word in r:
            input_txt = re.sub(word, "", input_txt)
        return input_txt

    # Clean the 'Review' column
    data['Review_clean'] = data['Review'].str.replace("[^a-zA-Z#]", " ", regex=True)

    # Remove words with less than 4 characters
    data['Review_clean'] = data['Review_clean'].apply(lambda x: ' '.join([w for w in str(x).split() if len(w) > 3]))

    # Tokenize the reviews
    tokenized_review = data['Review_clean'].apply(lambda x: x.split())

    # Apply stemming
    stemmer = PorterStemmer()
    tokenized_review = tokenized_review.apply(lambda sentence: [stemmer.stem(word) for word in sentence])

    # Join the stemmed words back into sentences
    for i in range(len(tokenized_review)):
        tokenized_review[i] = " ".join(tokenized_review[i])
    
    # Update the DataFrame with the processed reviews
    data['Review_clean'] = tokenized_review

    # Create the word cloud
    all_words = " ".join([sentence for sentence in data['Review_clean']])
    wordcloud = WordCloud().generate(all_words)
    
    # Generate image file name from the CSV file name
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    image_file_name = f"static/{name}.png"
    
    # Plot the word cloud
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the plot as an image file
    plt.savefig(image_file_name, format='png')  # Save as PNG file
    plt.close()  # Close the plot to free up memory

    print(f"Word cloud saved as {image_file_name}")

# generate_word_cloud("product_reviews/amazon_reviews.csv")
# print(get_sentiment(arr_reviews,0))