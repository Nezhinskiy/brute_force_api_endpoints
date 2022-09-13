import requests
import time
from itertools import product, permutations
from sys import getsizeof


endpoint = 'https://www.binance.com/bapi/fiat/v1/public/ocbs/get-quote'
length = 3
start_from = 0


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


def create_permutations_list(iterable, length):
    permutations_list = []
    pool = tuple(iterable)
    n = len(pool)
    r = length
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            permutations_list.append(''.join((pool[i]) for i in indices))
    return permutations_list


class BruteForcePostRequest:
    def __init__(self, length, endpoint, start_from=0):
        self.length = length
        self.iterable = 'etaoinshrdlcumwfgypbvkjxqz'
        self.endpoint = endpoint
        self.headers = create_headers()
        self.__run = True
        self.__count_api = start_from

    def __check_answer(self, answer, search_word):
        with open('runtime.txt', 'w') as f:
            print(self.__count_api, file=f)
        if answer['message'] == '000002:参数异常:000002':
            return
        elif answer['code'] == '000000':
            self.__run = False
            with open('result.txt', 'w') as f:
                print(f'Result = {search_word}', file=f)
                print(f'Result = {search_word}')
        else:
            print(f'! = {search_word}')

    def get_api_answer(self):
        permutations_list = create_permutations_list(self.iterable, self.length)
        list_size = len(permutations_list)
        while self.__run and self.__count_api < list_size:
            search_word = permutations_list[self.__count_api]
            with requests.session() as session:
                body = create_body(search_word)
                try:
                    response = session.post(self.endpoint, headers=self.headers,
                                            json=body)
                except BaseException as err:
                    with open('errors.txt', 'w') as f:
                        print(f'Errors: {err}, search_word = {search_word}',
                              file=f)
                    time.sleep(80)
                    response = session.post(self.endpoint, headers=self.headers,
                                            json=body)
                self.__check_answer(response.json(), search_word)
                self.__count_api += 1


if __name__ == '__main__':
    brute_force = BruteForcePostRequest(length, endpoint, start_from)
    N = len(tuple(permutations(brute_force.iterable, length))) - start_from
    start_timestamp = time.time()
    brute_force.get_api_answer()
    task_time = round(time.time() - start_timestamp, 2)
    rps = round(N / task_time, 1)
    with open('rps.txt', 'w') as f:
        print(
            f"| Requests: {N}; Total time: {task_time} s; RPS: {rps}. |\n",
            file=f
        )
