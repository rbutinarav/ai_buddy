from openai.embeddings_utils import get_embedding, cosine_similarity
import streamlit as st
import pandas as pd
import numpy as np
import openai

#inizialized session state variables
if "df" not in st.session_state:
    st.session_state.df = None

if st.session_state.df is None:
    #load reviews with embeddings from file into a dataframe
    datafile_path = "output/embedded_1k_reviews.csv"
    df = pd.read_csv(datafile_path)
    df["embedding"] = df.ada_embedding.apply(eval).apply(np.array)
    st.session_state.df = df

df = st.session_state.df

# search through the reviews for a specific product
def search_reviews(df, product_description, n=3):
    openai.api_key = st.secrets["OPENAI_KEY"]
    product_embedding = get_embedding(
        product_description,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
        #.combined.str.replace("Title: ", "")
        #.str.replace("; Content:", ": ")
    )
    
    return results


#ask use to input a product description
product_description = st.text_input("Enter a product description or question regarding a product review")

if product_description:
    #search for the product description
    results = search_reviews(st.session_state.df, product_description, n=3)

    #show the results with streamlit
    st.write("Results")
    #show the results only column "Summary","Text
    st.write(results[["Summary","Text"]])
