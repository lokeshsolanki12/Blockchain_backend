let web3;
let contract;
const contractAddress = "0x731f562e6486ee269Bcb444A711b5FA66ea9A095";

async function loadContract() {
    const response = await fetch("contract_abi.json");  // Load ABI from JSON file
    const contractABI = await response.json();
    contract = new web3.eth.Contract(contractABI, contractAddress);
}

// Connect to MetaMask
document.getElementById("connectWallet").addEventListener("click", async () => {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: "eth_requestAccounts" });
        const accounts = await web3.eth.getAccounts();
        document.getElementById("walletAddress").innerText = `Connected: ${accounts[0]}`;
        await loadContract();
    } else {
        alert("Please install MetaMask!");
    }
});

// Submit KYC Request
document.getElementById("submitKyc").addEventListener("click", async () => {
    if (!contract) return alert("Connect to MetaMask first!");

    const accounts = await web3.eth.getAccounts();
    const userId = document.getElementById("userId").value;
    const hashedUserId = web3.utils.sha3(userId);

    try {
        const tx = await contract.methods.requestKYC(hashedUserId).send({
            from: accounts[0],
            gas: 3000000,
        });
        alert(`KYC Request Submitted! Tx: ${tx.transactionHash}`);
    } catch (error) {
        console.error(error);
        alert("Error submitting KYC.");
    }
});

// Check KYC Status
document.getElementById("checkStatus").addEventListener("click", async () => {
    if (!contract) return alert("Connect to MetaMask first!");

    const accounts = await web3.eth.getAccounts();
    try {
        const status = await contract.methods.getUserStatus(accounts[0]).call();
        const statusMap = ["Unverified", "Pending", "Verified", "Rejected"];
        document.getElementById("kycStatus").innerText = `Status: ${statusMap[status]}`;
    } catch (error) {
        console.error(error);
        alert("Error fetching KYC status.");
    }
});
