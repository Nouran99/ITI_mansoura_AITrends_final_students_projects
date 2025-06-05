
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key[:5]}...") # يطبع فقط الجزء الأول من المفتاح للتحقق

from langchain_groq import ChatGroq
import os
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-70b-8192")
response = llm.invoke("Say hello")
print(response.content)