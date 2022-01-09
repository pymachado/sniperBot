import json
import time
from web3 import Web3

addressWBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c' 
addressRouter = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
addressFactory = '0xca143ce32fe78f1f7019d7d551a6402fc5350c73' 
addressToken = '0x2de5A0F18b9808a4c80a9ddD2789266F0B744Fee'
addressPair = '0x13165203a2Be5D0D6d331DBc795658D5FBbdc712'
recipient = '0xE256d74A4A5D2EE8b4C96cD41d4506A3DFF6D8D8'
adminPrivateKey = ''

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
with open("./abiPancakeRouterV2.json") as fileRouter:
    routerABI = json.load(fileRouter)

with open("./abiPancakePair.json") as filePair:
    pairABI = json.load(filePair)

with open("./abiIERC20.json") as fileIERC20:
     ierc20_json = json.load(fileIERC20)
     tokenABI = ierc20_json['abi']

routerSC = w3.eth.contract(address= addressRouter, abi=routerABI)
pairSC = w3.eth.contract(address=addressPair, abi=pairABI)
tokenSC = w3.eth.contract(address=addressToken, abi=tokenABI)

#print(routerSC.functions.WETH().call())

##Function Buy

def getKlast():
    return pairSC.functions.kLast().call()
       
def swapBNBbyTOKEN(valueInBNB, deadline):
    logs = []
    gasLimit = routerSC.functions.swapExactETHForTokens(0, 
    [addressWBNB, addressToken],
    recipient, deadline).estimateGas({'from': recipient, 'value': w3.toWei(valueInBNB, 'ether')})
    nonce = w3.eth.get_transaction_count(recipient)
    raw_tx = routerSC.functions.swapExactETHForTokens(0, 
    [addressWBNB, addressToken],
    recipient, deadline).buildTransaction({
    'chainId': w3.eth.chain_id,
    'gas': gasLimit,
    'nonce': nonce,
    'value': w3.toWei(valueInBNB, 'ether')
    })
    signed_tx = w3.eth.account.sign_transaction(raw_tx, private_key=adminPrivateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)  
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = tx_receipt['logs']
    print('SUCCESS!!! ;)')
    balance=tokenSC.functions.balanceOf(recipient).call()
    print(w3.fromWei(balance, 'gwei'))
    print(w3.eth.get_balance(recipient))
    print(logs)
    print(pairSC.functions.price1CumulativeLast().call())
    

def swapTOKENbyBNB(amountInToken, deadline): 
    gasLimit = routerSC.functions.swapTokensForExactETH(0, amountInToken,
    [addressToken, addressWBNB], recipient, deadline).estimateGas({'from': recipient})
    nonce = w3.eth.get_transaction_count(recipient)
    raw_tx = routerSC.functions.swapTokensForExactETH(0, amountInToken, 
    [addressWBNB, addressToken], recipient, deadline).buildTransaction({
        'chainId': w3.eth.chain_id,
        'gas': gasLimit,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(raw_tx, private_key=adminPrivateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    balance=tokenSC.functions.balanceOf(recipient).call()
    print(w3.fromWei(balance, 'gwei'))
    print(w3.fromWei(w3.eth.get_balance(recipient)), 'ether')
    print(tx_receipt['logs'])
    
def gasLimit(valueInBNB):
    return routerSC.functions.swapExactETHForTokens(0, 
        [addressWBNB, addressToken],
        recipient, deadline).estimateGas({'from': recipient, 'value': w3.toWei(valueInBNB, 'ether')})
    
deadline = (int(time.time()) + 60*10)

def buyFirst():
    count = 0
    k = getKlast()
    while(k == 0):
        print('k is 0 already')
        count +=1    
    swapBNBbyTOKEN(0.1, deadline)

print(w3.fromWei(w3.eth.get_balance(recipient), 'ether'))
balance = tokenSC.functions.balanceOf(recipient).call()
print(w3.fromWei(balance, 'gwei'))

#print(pairSC.functions.price1CumulativeLast().call())#
#print(pairSC.functions.price0CumulativeLast().call())

