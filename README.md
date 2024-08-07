![](https://raw.githubusercontent.com/sllavon/crypto-pay-api-sdk/3e83818c975a47f4ca61209b478f2508224058db/media/header.svg)
# @aicorelz/async-crypto-pay-api-sdk
## [SDK for working with Crypto Bot](https://t.me/CryptoBot)

# Installation
```sh
pip install git+https://github.com/aicorelz/async-crypto-pay-api-sdk
```

# Explanation

First, you need to create your application and get an API token.
Open [@CryptoBot](http://t.me/CryptoBot?start=pay) or [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay) (for testnet), end a command `/pay` to create a new app and get API Token.
| Net  | Bot | Hostname |
| ------------- | ------------- | ------------- |
| mainnet  | [@CryptoBot](http://t.me/CryptoBot?start=pay)  | pay.crypt.bot |
| testnet  | [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay)  | testnet-pay.crypt.bot |
>All queries to the Crypto Pay API must be sent over HTTPS



# Examples
**Support for all methods [official API](https://help.crypt.bot/crypto-pay-api)**

```python
from async_crypto_pay import cryptopay
import asyncio

crypto = cryptopay.Crypto('TOKEN', testnet=True)  # default testnet = False


async def main():
  print(
    await crypto.get_me()
  )

  print(
    await crypto.create_invoice(
      'TON',
      0.4,
      description='Test Invoice',
      expires_in=300
    )
  )


asyncio.run(main())
```

## Methods

**API**

* [getMe](#getMe)
* [createInvoice](#createInvoice)
* [transfer](#transfer)
* [getInvoices](#getInvoices)
* [getBalance](#getBalance)
* [getExchangeRates](#getExchangeRates)
* [getCurrencies](#getCurrencies)
* мне лень

### getMe

A simple method for testing your app's authentication token. Requires no parameters. Returns basic information about the app.

```python
await crypto.get_me()
```

### createInvoice

Use this method to create a new invoice. Returns object of created invoice.

* **asset** (string)
Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`.
* **amount** (string)
Amount of the invoice in float. For example: `125.50`
* **description** (string)
*Optional*. Description of the invoice. Up to 1024 symbols.
* **hidden_message** (string)
*Optional*. The message will show when the user pays your invoice.
* **paid_btn_name** (string) default - `callback`
*Optional*. Paid button name. This button will be shown when your invoice was paid. Supported names:

  * `viewItem` - View Item
  * `openChannel` - Open Channel
  * `openBot` - Open Bot
  * `callback` - Return

* **paid_btn_url** (string)
*Optional but requried when you use paid_btn_name*. Paid button URL. You can set any payment success link (for example link on your bot). Start with https or http.
* **payload** (string, up to 4kb)
*Optional*. Some data. User ID, payment id, or any data you want to attach to the invoice.
* **allow_comments** (boolean)
*Optional*. Allow adding comments when paying an invoice. Default is true.
* **allow_anonymous** (boolean)
*Optional*. Allow pay invoice as anonymous. Default is true.
* **expires_in** (number)
*Optional*. You can set the expiration date of the invoice in seconds. Use this period: 1-2678400 seconds.

```python
await crypto.create_invoice(
  'BTC', 
  1, 
  description='kitten', 
  paid_btn_name='viewItem',
  paid_btn_url='http://placekitten.com/150'
)
```

### transfer

Use this method to send coins from your app to the user. Returns object of completed transfer.

* **user_id** (number)
Telegram User ID. The user needs to have an account in our bot (send /start if no).
* **asset** (string)
Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`.
* **amount** (string)
Amount of the transfer in float. For example: `125.50`
* **spend_id** (string)
It is used to make your request idempotent. It's guaranteed that only one of the transfers with the same spend_id will be accepted by Crypto Pay API. This parameter is useful when the transfer should be retried (i.e. request timeout/connection reset/500 HTTP status/etc). You can use a withdrawal id or something. Up to 64 symbols.
* **comment** (string)
*Optional*. The comment of the invoice. The comment will show in the notification about the transfer. Up to 1024 symbols.

```python
await crypto.transfer(
  121011054, 
  'ETH',
  0.1, 
  'ZG9uYXRl',
  comment='donate'
)
```

### getInvoices

Use this method to get invoices of your app. On success, the returns array of invoices.

* **asset** (string)
*Optional*. Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`. Default: all assets.
* **invoice_ids** (string)
*Optional*. Invoice IDs separated by comma.
* **status** (string)
*Optional*. Status of invoices. Available statusses: active or paid. Default: all statusses.
* **offset** (number)
*Optional*. Offset needed to return a specific subset of  invoices. Default 0.
* **count** (number)
*Optional*. Number of invoices to return. Default 100, max 1000.

```python
await crypto.get_invoices('TON', 1)
```

### getBalance

Use this method to get balance of your app. Returns array of assets.

```python
await crypto.get_balance()
```

### getExchangeRates

Use this method to get exchange rates of supported currencies. Returns array of currencies.

```python
await crypto.get_exchange_rates()
```

### getCurrencies

Use this method to supported currencies. Returns array of currencies.

```python
await crypto.get_currencies()
```

## License
MIT
