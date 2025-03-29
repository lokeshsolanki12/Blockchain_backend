from blockchain import w3, contract
from config import PRIVATE_KEY

# Function to check if an address is a KYC verifier
def is_verifier(address):
    try:
        return contract.functions.kycVerifiers(address).call()
    except Exception as e:
        print(f"Error checking verifier status: {e}")
        return False

# Function to check the KYC status of a user
def check_kyc_status(user_address):
    try:
        status = contract.functions.getUserStatus(user_address).call()
        status_map = {0: "Unverified", 1: "Pending", 2: "Verified", 3: "Rejected"}
        print(f"KYC Status for {user_address}: {status_map.get(status, 'Unknown')}")
        return status
    except Exception as e:
        print(f"Error fetching KYC status: {e}")
        return None

# Function to add a KYC verifier (ONLY OWNER CAN CALL THIS)
def add_verifier(verifier_address):
    try:
        txn = contract.functions.addVerifier(verifier_address).build_transaction({
            "from": w3.eth.account.from_key(PRIVATE_KEY).address,
            "gas": 3000000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": w3.eth.get_transaction_count(w3.eth.account.from_key(PRIVATE_KEY).address),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Verifier {verifier_address} Added! Transaction Hash: {txn_hash.hex()}")
        return txn_hash.hex()
    except Exception as e:
        print(f"Failed to add verifier: {e}")
        return None

# Function to approve KYC (ONLY VERIFIER CAN CALL THIS)
def approve_kyc(user_address):
    try:
        if not is_verifier(w3.eth.account.from_key(PRIVATE_KEY).address):
            print(" You are NOT a registered KYC verifier!")
            return None

        txn = contract.functions.approveKYC(user_address).build_transaction({
            "from": w3.eth.account.from_key(PRIVATE_KEY).address,
            "gas": 3000000,
            "gasPrice": w3.to_wei("5", "gwei"),
            "nonce": w3.eth.get_transaction_count(w3.eth.account.from_key(PRIVATE_KEY).address),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"KYC Approved for {user_address}! Transaction Hash: {txn_hash.hex()}")
        return txn_hash.hex()
    except Exception as e:
        print(f"Failed to approve KYC: {e}")
        return None

# CLI interaction
if __name__ == "__main__":
    print("🔹 Blockchain KYC Management 🔹")
    print("1️⃣ Check KYC Status")
    print("2️⃣ Approve KYC (Only for Verifiers)")
    print("3️⃣ Add KYC Verifier (Only for Owner)")
    
    choice = input("Enter choice: ")

    if choice == "1":
        user_wallet = input("Enter user wallet address: ")
        check_kyc_status(user_wallet)

    elif choice == "2":
        user_wallet = input("Enter user wallet address to approve KYC: ")
        approve_kyc(user_wallet)

    elif choice == "3":
        verifier_wallet = input("Enter wallet address to add as verifier: ")
        add_verifier(verifier_wallet)

    else:
        print(" Invalid choice!")
