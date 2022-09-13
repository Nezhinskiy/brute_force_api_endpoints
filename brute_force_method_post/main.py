import requests
import time
from itertools import product, permutations
from sys import getsizeof


endpoint = 'https://www.binance.com/bapi/fiat/v1/public/ocbs/get-quote'
length = 3


def create_body(search_word):
    return {
        "baseCurrency": "EUR",
        "cryptoCurrency": "BTC",
        "payType": "Bid",
        "paymentChannel": search_word,
        "rail": "card",
        "requestedAmount": 1000,
        "requestedCurrency": "EUR"
    }


def create_headers():
    search_word = 'x' * length
    body = create_body(search_word)
    return {
        "Content-Type": "application/json",
        "Content-Length": str(getsizeof(body))
    }


class BruteForcePostRequest:
    def __init__(self, length, endpoint):
        self.length = length
        self.iterable = 'etaoinshrdlcumwfgypbvkjxqz'
        self.endpoint = endpoint
        self.headers = create_headers()
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

    def get_api_answer(self, search_word):
        with requests.session() as session:
            body = create_body(search_word)
            try:
                response = session.post(self.endpoint, headers=self.headers,
                                        json=body)
            except BaseException as err:
                with open('errors.txt', 'w') as f:
                    print(f'Errors: {err}, search_word = {search_word}', file=f)
                time.sleep(80)
                response = session.post(self.endpoint, headers=self.headers,
                                        json=body)
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
    brute_force = BruteForcePostRequest(length, endpoint)
    N = len(tuple(permutations(brute_force.iterable, length)))
    start_timestamp = time.time()
    brute_force.permutations()
    task_time = round(time.time() - start_timestamp, 2)
    rps = round(N / task_time, 1)
    print(
        f"| Requests: {N}; Total time: {task_time} s; RPS: {rps}. |\n"
    )
