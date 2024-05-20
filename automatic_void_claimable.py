import time
from web3 import Web3

# Connect to Blast node
w3 = Web3(Web3.HTTPProvider('https://rpc.blast.io'))

# Contract addresses and the common ABI
USDB_ADDRESS = '0x4300000000000000000000000000000000000003'
WETH_ADDRESS = '0x4300000000000000000000000000000000000004'
COMMON_ABI = [{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getConfiguration","outputs":[{"internalType":"enum YieldMode","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]

# Create contract objects
usdb_contract = w3.eth.contract(address=USDB_ADDRESS, abi=COMMON_ABI)
weth_contract = w3.eth.contract(address=WETH_ADDRESS, abi=COMMON_ABI)

# Extract "from" addresses from each new block
def handle_block(block_number, rps=25):
    block = w3.eth.get_block(block_number, full_transactions=True)
    active_accounts = set(tx['from'] for tx in block.transactions if 'from' in tx)
    delay = 1 / rps

# Check yield mode for each active account
    for account in active_accounts:
        check_yield_mode(account, usdb_contract, "USDB")
        check_yield_mode(account, weth_contract, "WETH")
        time.sleep(delay)

# Call the getConfiguration function to check the yield mode. 0 = AUTOMATIC, 1 = VOID, 2 = CLAIMABLE
def check_yield_mode(account, contract, contract_name):
    yield_mode = contract.functions.getConfiguration(account).call()
    if yield_mode == 0:
        print(f"{account} yieldMode on {contract_name} is AUTOMATIC")
    elif yield_mode == 1:
        print(f"{account} yieldMode on {contract_name} is VOID")
    elif yield_mode == 2:
        print(f"{account} yieldMode on {contract_name} is CLAIMABLE")

def main(rps=20):
    block_filter = w3.eth.filter('latest')
    while True:
        for block_number in block_filter.get_new_entries():
            handle_block(block_number, rps)

if __name__ == "__main__":
    main()