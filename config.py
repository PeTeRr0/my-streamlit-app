# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads the .env file

FRED_API_KEY = os.getenv("FRED_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
