# Import dependencies
from constants import BTC, BTCTEST, ETH, numderive
import subprocess
import json
import os
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")
# print(mnemonic) -- test that mnemonic pulls correctly

# Import constants.py and necessary functions from bit and web3
from bipwallet import wallet
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

# Connect to web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
 
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    return keys

# derive_wallets(mnemonic, 'btc', 3) # Test the function

# Create a dictionary object called coins to store the output from `derive_wallets`. I 
coins = {}

# Create dictionary of coins from constants
constants = {BTC, ETH, BTCTEST}

for coin in constants:
    coins[coin] = derive_wallets(mnemonic, coin, numderive)

# print(json.dumps(coins, indent=4, sort_keys=True)) -- print the dictionary to check successful run of function

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.

eth_PK = coins["eth"][0]['privkey'] # Set ETH private key
btctest_PK = coins['btc-test'][0]['privkey'] # Set BTCTEST private key

def priv_key_to_account(coin, key):
    if coin == 'eth':
        return Account.privateKeyToAccount(key)
    else:
        return PrivateKeyTestnet(key)

eth_acc = priv_key_to_account(ETH, eth_PK) # Set ETH account
btctest_acc = priv_key_to_account(BTCTEST, btctest_PK) # Set BTCTEST account

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == 'eth':
        gasEstimate = w3.eth.estimateGas(
         {"from":eth_acc.address, "to":recipient, "value": amount}   
        )
        return {
            "from": eth_acc.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    else:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    txn = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        tx_btctest = create_tx(coin, account, recipient, amount)
        signed_txn = account.sign_transaction(txn)
        print(signed_txn)
        return NetworkAPI.broadcast_tx_testnet(signed_txn)