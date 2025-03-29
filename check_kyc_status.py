from blockchain import w3, contract

def get_kyc_status(user_address):
    try:
        status = contract.functions.getUserStatus(user_address).call()
        status_map = {0: "Unverified", 1: "Pending", 2: "Verified", 3: "Rejected"}
        print(f"KYC Status for {user_address}: {status_map.get(status, 'Unknown')}")
        return status
    except Exception as e:
        print(f"Error fetching KYC status: {e}")
        return None

# 🔹 Example Usage
if __name__ == "__main__":
    user_wallet = "0x7520CD2E28BD9890Eb1e559c607372718e713d7E"  # Replace with actual address
    get_kyc_status(user_wallet)
