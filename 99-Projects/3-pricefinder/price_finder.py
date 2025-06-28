"""
Price Finder: LLM Output Validation with Pydantic

This code demonstrates using Pydantic to validate and structure LLM outputs. 
By defining a Product model with strict type definitions, we ensure:
- Type safety (enforcing string for names, integer for prices)
- Data validation (required fields, correct formats)
- Consistent JSON structure in LLM responses

Key Benefits:
- Guarantees data consistency from LLM responses
- Provides clear error messages when validation fails
- Enables type hints and IDE support
- Simplifies data handling with automatic type conversion

The implementation uses LangChain's JsonOutputParser with our Pydantic model to transform 
unstructured LLM responses into validated, typed Python objects.
"""


import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
load_dotenv(override=True)

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

class Product(BaseModel):
    product_name: str = Field(description="Name of the product")
    price: int = Field(description="Price in USD in integer")
    product_features: str = Field(description="Important Features of product")

def get_data(product_name):
    prompt_template = """
    You are a helpful assistant that provides product information in a structured JSON format.
    For any product query, you must return a JSON object with exactly these fields:
    - product_name: The exact name of the product
    - price: The price in USD as an integer (no decimal points)
    - product_features: A string describing the key features of the product
    Ensure the response strictly follows this format and all fields are present.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template),
        ("user", product_name)
    ])
    
    model_name = "deepseek-r1-distill-llama-70b"
    model=ChatGroq(model=model_name)
    parser = JsonOutputParser(pydantic_object=Product)
    chain = prompt | model | parser
    response = chain.invoke({"input": product_name})
    return response

if __name__ == "__main__":
    result = get_data("Apple mac pro m1 2021")
    print(result)