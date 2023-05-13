#load csv file in a dataframe
import pandas as pd
import streamlit as st
import openai

df = pd.read_csv("documents\Reviews.csv")

#inspect the dataframe
df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]
df = df.dropna()
df["combined"] = (
    "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
)

#keep the first 1000 rows
df = df.head(1000)

#show shape of the dataframe and first 10 rows
st.write(df.shape)
st.write(df.head(10))


#combine the title and the review text

openai.api_key = st.secrets["OPENAI_KEY"]

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
 
df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))

#check if output folder exists if not create it
import os
if not os.path.exists('output'):
    os.makedirs('output')

df.to_csv('output/embedded_1k_reviews.csv', index=False)