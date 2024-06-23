import requests


class MoexClient:
    BASE_URL = 'https://iss.moex.com'
    _DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }

    def _construct_security_trade_url(self, security_name: str, to_json: bool = True) -> str:
        return f'{self.BASE_URL}/iss/engines/stock/markets/bonds/boards/TQOB/securities/{security_name}/trades{".json" if to_json else ""}'

    def get(self, url: str, headers: dict | None = None, **params) -> requests.Response:
        return requests.get(
            url,
            headers=headers if headers else self._DEFAULT_HEADERS,
            **params
        )

    def get_security_trades(self, security_name: str) -> dict:
        return self.get(self._construct_security_trade_url(security_name)).json()


moex_client = MoexClient()
response = moex_client.get_security_trades('SU29024RMFS5')
print(response)
