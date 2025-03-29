import os
from dotenv import load_dotenv

# 🔹 Load .env file
load_dotenv()

# 🔹 Environment Variables
BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
