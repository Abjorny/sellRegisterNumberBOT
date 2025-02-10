import aiohttp
import asyncio
from config import API_KEY
BASE_URL = " https://pay.crypt.bot/api/"

async def create_payment(crypto: str, amount_rub: float):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}getExchangeRates",
                headers={"Crypto-Pay-API-Token": API_KEY},
            ) as response:
                rate_data = await response.json()
                for rate in rate_data.get("result", []):
                            if rate.get("is_crypto") and rate.get("is_valid") and rate.get("source") == crypto and rate.get("target") == "USD":
                                rate_price = rate.get('rate')
                                crypto_amount = round(amount_rub / float(rate_price), 8)
                                async with session.post(
                                    f"{BASE_URL}createInvoice",
                                    headers={"Crypto-Pay-API-Token": API_KEY},
                                    json={ "asset": crypto, "amount": crypto_amount}
                                ) as response:
                                    payment_data = await response.json()
                                    if payment_data["ok"]:
                                        return {
                                            "payment_url": payment_data["result"]["pay_url"],
                                            "payment_id": payment_data["result"]["invoice_id"]
                                        }
                                    else:
                                        raise ValueError(f"Ошибка при создании платежа: {payment_data['description']}")
    except Exception :
        return None

async def get_payment_status(payment_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}getInvoices",
                params={ "paid": payment_id},
                headers={"Crypto-Pay-API-Token": API_KEY},
            ) as response:
                invoices = await response.json()
                invoices = invoices["result"]['items']
                for invoise in invoices:
                        if str(invoise['invoice_id']) in str(payment_id):
                            return invoise['status'],invoise['pay_url']
    except Exception:
         return None


async def get_available_currencies():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}getCurrencies",
                headers={"Crypto-Pay-API-Token": API_KEY},
                timeout=10 
            ) as response:
                if response.status == 200:
                    currencies_data = await response.json()
                    if currencies_data.get("ok"):
                        return [
                            currency["code"]
                            for currency in currencies_data.get("result", [])
                            if currency.get("is_blockchain") or currency.get("is_stablecoin")
                        ]
                else:
                    return []
    except:
         return None
