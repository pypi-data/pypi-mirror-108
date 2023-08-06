import asyncio

import httpx

import nepse
from nepse import Client


async def main():
    async with httpx.AsyncClient() as async_client:
        client = Client(httpx_client=async_client)
        data = await client.security_client.get_company(symbol="UPPER")
        print(data.high_price)
        market_caps = await client.market_client.get_market_caps()
        # print(market_caps)
        live_trade = await client.security_client.get_company_live_price(symbol="UPPER")
        print(live_trade.high_price)
        
        trades = await client.security_client.get_companies_live_prices()
        upper = nepse.utils.get(trades, symbol="UPPER")
        print(upper.high_price)


asyncio.run(main())
