import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud
from nltk.stem.porter import PorterStemmer

data = pd.read_csv(r"product_reviews/amazon_reviews.csv")

### remove all the special characters
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for word in r:
        input_txt = re.sub(word, "", input_txt)
    return input_txt
data['Review_clean'] = data['Review'].str.replace("[^a-zA-Z#]", " ")


### get a array of words from sentence
data['Review_clean'] = data['Review_clean'].apply(lambda x:' '.join([w for w in str(x).split() if len(w)>3]))
tokenized_review = data['Review_clean'].apply(lambda x: x.split())

### form the sentence from the above word
stemmer = PorterStemmer()
tokenized_review = tokenized_review.apply(lambda sentence: [stemmer.stem(word) for word in sentence])

for i in range(len(tokenized_review)):
    tokenized_review[i] = " ".join(tokenized_review[i])
data['Review_clean'] = tokenized_review


### creating the word cloud
all_words = " ".join([sentence for sentence in data['Review_clean']])
wordcloud = WordCloud().generate(all_words)
# plot the graph
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()