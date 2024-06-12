import aiohttp
import asyncio


class Crypto:
    """
    First, you need to create your application and get an API token.
    Open [@CryptoBot](http://t.me/CryptoBot?start=pay) or [@CryptoTestnetBot](http://t.me/CryptoTestnetBot?start=pay) (for testnet),
    send a command `/pay` to create a new app and get API Token.

    Args:
        token {string} - Your API token
    """

    def __init__(
            self,
            token,
            testnet: bool = False
    ):
        self.token = str(token)
        if testnet:
            self.url = 'https://testnet-pay.crypt.bot/api'
        else:
            self.url = 'https://pay.crypt.bot/api'
        self.headers = {
            'Content-Type': 'application/json',
            'Crypto-Pay-API-Token': self.token
        }

    async def _request(
            self,
            method,
            endpoint,
            data: dict = None
    ):
        if data:
            data = {
                k: v for k, v in data.items() if v is not None
            }
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    f'{self.url}/{endpoint}',
                    headers=self.headers,
                    json=data
            ) as response:
                return await response.json()

    async def getMe(self):
        """A simple method for testing your app's authentication token.

        Args:
            Requires no parameters.

        Returns:
            Basic information about the app.
        """
        return await self._request('GET', 'getMe')

    async def createInvoice(
            self,
            asset: str,
            amount: str,
            **kwargs
    ):
        """Use this method to create a new invoice.

        Args:
            asset {string} - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`

            amount {string} - Amount of the invoice in float. For example: `125.50`

            description {string} - Optional. Description of invoice. Up to `1024 symbols`

            hidden_message {string} - Optional. The message will show when the user pays your invoice

            paid_btn_name {string} - Optional. Paid button name. This button will be shown when your invoice was paid
            Supported names: `viewItem` - View Item, `openChannel` - Open Channel, `openBot` - Open Bot, `callback` - Return

            paid_btn_url {string} - Optional. Paid button URL. You can set any payment success link (for example link on your bot)

            payload {string} - Optional. Some data. User ID, payment id, or any data you want to attach to the invoice; up to `4kb`

            allow_comments {boolean} - Optional. Allow adding comments when paying an invoice. `Default is true`

            allow_anonymous  {boolean} - Optional. Allow pay invoice as anonymous. `Default is true`

            expires_in {boolean} - Optional. You can set the expiration date of the invoice in seconds. Use this period: `1-2678400 seconds`

        Returns:
            Object of created invoice.
        """
        return await self._request(
            'POST',
            'createInvoice',
            data={
                'asset': asset,
                'amount': amount,
                **kwargs
            }
        )

    async def transfer(
            self,
            user_id: int,
            asset: str,
            amount: str,
            spend_id: str,
            **kwargs
    ):
        """Use this method to send coins from your app to the user.

        Args:
            user_id {number} - Telegram User ID.

            asset {string} - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`

            amount {string} - Amount of the transfer in float. For example: `125.50`

            spend_id {string} - Uniq ID to make your request idempotent. Up to `64 symbols`

            comment {string} - Optional. The comment of the invoice. Up to `1024 symbols`

            disable_send_notification {boolean} - Optional. Pass true if the user should not receive a notification about the transfer. `Default is false`

        Returns:
            Object of completed transfer.
        """
        return await self._request(
            'POST',
            'transfer',
            data={
                'user_id': user_id,
                'asset': asset,
                'amount': amount,
                'spend_id': spend_id,
                **kwargs
            }
        )

    async def getInvoices(self, **kwargs):
        """Use this method to get invoices created by your app.

        Args:
            asset -- Optional. Currency code.
            Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`. Default: all assets

            invoice_ids {string} - Optional. Invoice `IDs` separated by comma

            status {string} - Optional. Status of invoices. Available statusses: active or paid. `Default: all statusses`

            offset {number} - Optional. Offset needed to return a specific subset of invoices. `Default 0`

            count {number} - Optional. Number of invoices to return. `Default 100, max 1000`

        Returns:
            Array of invoices
        """
        return await self._request('GET', 'getInvoices', kwargs)

    async def getBalance(self):
        """Use this method to get balance of your app

        Args:
            Requires no parameters.

        Returns:
            Array of assets
        """
        return await self._request('GET', 'getBalance')

    async def getExchangeRates(self):
        """Use this method to get exchange rates of supported currencies

        Args:
            Requires no parameters.

        Returns:
            Array of currencies
        """
        return await self._request('GET', 'getExchangeRates')

    async def createCheck(
            self,
            asset: str,
            amount: str,
            pin_to_user_id: int = None,
            pin_to_username: str = None,
    ):
        """Use this method to create a new invoice.

        Args:
            asset {string} - Currency code. Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`

            amount {string} - Amount of the invoice in float. For example: `125.50`

            pin_to_user_id {int} - Optional. ID of the user who will be able to activate the check.

            pin_to_username {string} - Optional. A user with the specified username will be able to activate the check.

        Returns:
            Object of created check.
        """
        return await self._request(
            'POST',
            'createCheck',
            {
                'asset': asset,
                'amount': amount,
                'pin_to_user_id': pin_to_user_id,
                'pin_to_username': pin_to_username
            }
        )

    async def deleteCheck(
            self,
            check_id: str
    ):
        """Use this method to delete checks created by your app.

        Args:
            check_id {int} - Check ID to be deleted.

        Returns:
            True on success.
        """
        return await self._request(
            'POST',
            'deleteCheck',
            {
                'check_id': check_id
            }
        )

    async def getChecks(
            self,
            asset: str = None,
            check_ids: list = None,
            status: str = None,
            offset: int = None,
            count: int = None
    ):
        """Use this method to get checks created by your app.

        Args:
            asset -- Optional. Currency code.
            Supported assets: `BTC`, `TON`, `ETH` (only testnet), `USDT`, `USDC`, `BUSD`. Default: all assets

            check_ids {string} - Optional. Invoice `IDs` separated by comma

            status {string} - Optional. Status of invoices. Available statusses: active or paid. `Default: all statusses`

            offset {number} - Optional. Offset needed to return a specific subset of invoices. `Default 0`

            count {number} - Optional. Number of invoices to return. `Default 100, max 1000`

        Returns:
            Array of Check
        """
        return await self._request(
            'GET',
            'getChecks',
            {
                'asset': asset,
                'check_ids': check_ids,
                'status': status,
                'offset': offset,
                'count': count
            }
        )

    async def getCurrencies(self):
        """Use this method to supported currencies

        Args:
            Requires no parameters.

        Returns:
            Array of currencies
        """
        return await self._request('GET', 'getCurrencies')

    async def getStats(
            self,
            start_at: str = None,
            end_at: str = None
    ):
        """Use this method to get app statistics.

        Args: offset {string} - Optional. Date from which start calculating statistics in ISO 8601 format. Defaults
        is current date minus 24 hours.

            count {number} - Optional. The date on which to finish calculating statistics in ISO 8601 format.
            Defaults is current date.

        Returns:
            AppStats on success.
        """
        return await self._request(
            'GET',
            'getStats',
            {
                'start_at': start_at,
                'end_at': end_at
            }
        )
