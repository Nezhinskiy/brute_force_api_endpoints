import time
from itertools import product
from sys import getsizeof

import requests

endpoint = 'https://www.binance.com/bapi/fiat/v1/public/ocbs/get-quote'
length = 4
search_word = 'x' * length
body = {
    "baseCurrency":"EUR",
    "cryptoCurrency":"BTC",
    "payType": "Bid",
    "paymentChannel":search_word,
    "rail":"card",
    "requestedAmount":1000,
    "requestedCurrency":"EUR"
}
headers = {
            "Content-Type": "application/json",
            "Content-Length": str(getsizeof(body)),
        }


class brute_force_post_request:
    def __init__(self, length, endpoint, headers):
        self.length = length
        self.iterable = 'etaoinshrdlcumwfgypbvkjxqz'
        self.endpoint = endpoint
        self.headers = headers
        self.run = True
        self.count_api = 0

    def check_answer(self, answer, search_word):
        self.count_api += 1
        print(self.count_api)
        if answer['message'] == '000002:参数异常:000002':
            return
        elif answer['code'] == '000000':
            self.run = False
            with open('result.txt', 'w') as f:
                print(f'Result = {search_word}', file=f)
                print(f'Result = {search_word}')
        else:
            print(f'! = {search_word}')

    def make_body(self, search_word):
        return {
            "baseCurrency": "EUR",
            "cryptoCurrency": "BTC",
            "payType": "Bid",
            "paymentChannel": search_word,
            "rail": "card",
            "requestedAmount": 1000,
            "requestedCurrency": "EUR"
        }

    def get_api_answer(self, search_word):
        with requests.session() as session:
            try:
                response = session.post(self.endpoint, headers=self.headers,
                                        json=self.make_body(search_word))
            except:
                time.sleep(80)
                response = session.post(self.endpoint, headers=self.headers,
                                        json=self.make_body(search_word))
            self.check_answer(response.json(), search_word)

    def permutations(self):
        pool = tuple(self.iterable)
        n = len(pool)
        r = self.length
        for indices in product(range(n), repeat=r):
            if not self.run:
                break
            if len(set(indices)) == r:
                self.get_api_answer(''.join((pool[i]) for i in indices))


if __name__ == '__main__':
    N = 358800
    a = brute_force_post_request(length, endpoint, headers)

    start_timestamp = time.time()
    a.permutations()

    task_time = round(time.time() - start_timestamp, 2)
    rps = round(N / task_time, 1)
    print(
        f"| Requests: {N}; Total time: {task_time} s; RPS: {rps}. |\n"
    )
