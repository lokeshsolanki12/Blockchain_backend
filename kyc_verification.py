import sys
import hashlib
from blockchain import w3, contract
from config import PRIVATE_KEY

def hash_user_id(user_data):
    return hashlib.sha256(user_data.encode()).hexdigest()

def request_kyc(user_address, user_id):
    try:
        hashed_id = hash_user_id(user_id) 
        txn = contract.functions.requestKYC(hashed_id).build_transaction({
            "from": user_address,
            "gas": 3000000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": w3.eth.get_transaction_count(user_address),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"KYC Request Sent! Txn Hash: {txn_hash.hex()}")
        return txn_hash.hex()
    except Exception as e:
        print(f"KYC Request Failed: {e}")
        return None

def check_kyc_status(user_address):
    try:
        status = contract.functions.getUserStatus(user_address).call()
        status_map = {0: "Unverified", 1: "Pending", 2: "Verified", 3: "Rejected"}
        print(f"🔹 User KYC Status: {status_map[status]}")
        return status_map[status]
    except Exception as e:
        print(f"Error Fetching KYC Status: {e}")
        return None

def is_user_verified(user_address):
    try:
        verified = contract.functions.isUserVerified(user_address).call()
        print(f"🔍 User Verified: {verified}")
        return verified
    except Exception as e:
        print(f"Error Checking Verification: {e}")
        return None

def main():
    while True:
        print("\ KYC Verification System")
        print("1️⃣ Request KYC")
        print("2️⃣ Check KYC Status")
        print("3️⃣ Exit")
        choice = input("👉 Enter your choice (1/2/3): ")

        if choice == "1":
            user_wallet = input("🔹 Enter Wallet Address: ").strip()
            user_id = input("🔹 Enter User ID (e.g., Passport No, Aadhaar, etc.): ").strip()
            request_kyc(user_wallet, user_id)

        elif choice == "2":
            user_wallet = input("🔹 Enter Wallet Address: ").strip()
            check_kyc_status(user_wallet)
            is_user_verified(user_wallet)

        elif choice == "3":
            print("Exiting... Bye!")
            sys.exit()

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()