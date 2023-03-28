import asyncio
import json
from web3 import Web3
from websockets import connect

alchemy_ws = 'wss://eth-mainnet.g.alchemy.com/v2/zLyuXCAE2wg68Jy3Z6INCwCdXMCjY5qb'
alchemy_api = 'https://eth-mainnet.g.alchemy.com/v2/zLyuXCAE2wg68Jy3Z6INCwCdXMCjY5qb'

web3 = Web3(Web3.HTTPProvider(alchemy_api))

print(f'Connected via HTTP: {web3.is_connected()}')
#--------------------------------------------------

def EventHandler(pending_tx): 
    """Takes in a subscription transacton response as pending_tx
       Then currently prints out data or can be modified for whatever"""
    transaction = json.loads(pending_tx)
    print(transaction)

async def subscribePendingTX():
    async with connect(alchemy_ws) as ws:
        await ws.send('{"jsonrpc": "2.0", "method": "eth_subscribe","params": ["alchemy_minedTransactions", {"addresses": [{"to": "0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B"}],"includeRemoved": false,  "hashesOnly": true}],"id": 1}')
        while True:
            try:
                pending_tx = await asyncio.wait_for(ws.recv(), timeout=12)
                EventHandler(pending_tx)
            except KeyboardInterrupt:
                exit()
            except:
                pass

if __name__ == "__main__":
    asyncio.run(subscribePendingTX())

