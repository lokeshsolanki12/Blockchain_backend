from web3 import Web3
import json
from config import BLOCKCHAIN_URL, PRIVATE_KEY, CONTRACT_ADDRESS

# 🔹 Web3 Connection
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

if w3.is_connected():
    print(" Connected to Blockchain")
else:
    print(" Blockchain Connection Failed")

# 🔹 Load Smart Contract ABI
with open("contract_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

# 🔹 Initialize Contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
