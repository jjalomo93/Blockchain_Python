# Import dependencies
from Homework.Blockchain_Python.wallet.wallet import create_tx, send_tx
from constants import BTC, BTCTEST, ETH, numderive
import subprocess
import json
import os
from dotenv import load_dotenv
from wallet import *

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

# Create transaction - BTCTEST
create_tx(BTCTEST,btctest_acc,"moo8GpmfFJGtZF7VS3kFZy6UjPNgrfWxgC", 0.001)

# Send transaction - BTCTEST
send_tx(BTCTEST,btc_acc,"moo8GpmfFJGtZF7VS3kFZy6UjPNgrfWxgC", 0.001)

# Create transaction - ETH
create_tx(ETH,eth_acc,"0x1eb01c5AB82731bcbd0bf5d2d459F55C34212FFa", 100)

# Send transaction - ETH
send_tx(ETH, eth_acc,"0x1eb01c5AB82731bcbd0bf5d2d459F55C34212FFa", 1000)