# 🛍️ Product Assistant

A Streamlit-based AI assistant that answers product-related queries using OpenAI's GPT-4o model, structured and validated with LangChain and Pydantic.

## Environment Variables

Create a .env file in the root directory with your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

## 🚀 Features

- 💬 Ask natural language questions about products
- 🧠 Uses OpenAI's GPT-4o for intelligent, context-aware responses
- ✅ Validates output using Pydantic models
- 🌐 Interactive web interface built with Streamlit
- 💵 Outputs structured product details including name, description, and price

## 🧱 Tech Stack

- [Streamlit](https://streamlit.io/) – frontend UI
- [LangChain](https://www.langchain.com/) – prompt chaining and output parsing
- [OpenAI GPT-4o](https://platform.openai.com/) – language model
- [Pydantic](https://docs.pydantic.dev/) – data validation
- [Python 3.9+](https://www.python.org/) – core language


## 📦 Setup Instructions

### 1. Clone the Repo
git clone https://github.com/yourusername/product-assistant.git
cd product-assistant

### 2. Set up the environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 3. Add your API key
Create a .env file in the root directory with your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here

### 4. Run the app
streamlit run Assignment-ProductAssistant.py
## Notes
Make sure your OpenAI key has access to GPT-4o.
You can customize the Pydantic model to include more product fields (e.g., availability, SKU, ratings).
## Project Structure
product-assistant/
├── Assignment-ProductAssistant.py  # Main app logic
├── requirements.txt                # Python dependencies
├── .env                            # Environment file (not committed)
└── README.md                       # This file
![1443DC8B-6C28-4CB8-85C3-3E2EE6A6D6C7](https://github.com/user-attachments/assets/da4ad298-caff-41df-ab91-01c1dae053c3)
