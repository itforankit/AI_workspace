## Product Assistant using Langchain and streamlit

### create a simple assistant that uses any LLM and should be pydantic. when we ask about any product it should give you two information Product Name, Prodcut details and Tentative price in USD(integer). use ChatPromptTemplate.

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

import streamlit as st
st.title("Product Assistant")
input_txt = st.text_input("Please enter your product query here...")

class Product(BaseModel):
    Product_name: str
    Product_details: str
    Tentative_price: int = Field(description="Price should be in USD only")
    Positive_Review:str=Field(max_length=50)
    Negative_Review:str=Field(max_length=50)
parser =JsonOutputParser(pydantic_object=Product)

prompt = ChatPromptTemplate.from_messages(
    [
        ('system','you are a helpful assistant. Pleasr answer the user question professionally about the product\n'),
        ('user','{product_query} \n {format_instructions}')
    ]

)

llm =ChatOpenAI(model='gpt-4o')

chain = prompt|llm|parser

if input_txt:
    if input_txt.isnumeric():
        st.error("Please enter a valid product query, not just numbers.")
    else:
        result = chain.invoke({"product_query":input_txt,"format_instructions":parser.get_format_instructions()})
        result['Tentative_price'] = f"${result['Tentative_price']:,.2f}"

        st.write("### Product Details")
        st.write(f"**Name:** {result['Product_name']}")
        st.write(f"**Details:** {result['Product_details']}")
        st.write(f"**Tentative Price:** {result['Tentative_price']}")
        st.write(f"**Positive Review:** {result['Positive_Review']}")
        st.write(f"**Negative Review:** {result['Negative_Review']}")
else:
    st.warning("Input cannot be empty")

