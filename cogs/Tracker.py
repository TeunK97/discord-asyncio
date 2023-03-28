from nextcord.ext import commands
from websockets import connect
import asyncio

import logging
import json

alchemy_ws = 'wss://eth-mainnet.g.alchemy.com/v2/zLyuXCAE2wg68Jy3Z6INCwCdXMCjY5qb'

logger = logging.getLogger('Audit-COG')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = loop.create_task(self.subscribePendingTX())

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Tracker COG loaded.')
        logging.info('subscribePendingTX task started.')

    def EventHandler(pending_tx): 
        """Takes in a subscription transacton response as pending_tx
        Then currently prints out data or can be modified for whatever"""
        transaction = json.loads(pending_tx)
        print(transaction)

    async def subscribePendingTX(self):
        async with connect(alchemy_ws) as ws:
            await ws.send('{"jsonrpc": "2.0", "method": "eth_subscribe","params": ["alchemy_minedTransactions", {"addresses": [{"to": "0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B"}],"includeRemoved": false,  "hashesOnly": true}],"id": 1}')
            while True:
                try:
                    pending_tx = await asyncio.wait_for(ws.recv(), timeout=12)
                    self.EventHandler(pending_tx)
                except KeyboardInterrupt:
                    exit()
                except:
                    pass

def setup(bot):
    bot.add_cog(Tracker(bot))
        

    
