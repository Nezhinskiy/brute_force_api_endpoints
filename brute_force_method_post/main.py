import time
from itertools import permutations, product
from sys import getsizeof
from typing import List

import requests

endpoint = 'https://www.binance.com/bapi/fiat/v1/public/ocbs/get-quote'
iterable = 'etaoinshrdlcumwfgypbvkjxqz'
length = 3
start_from = 0
good_answer = '000000'
bad_answer = '000002:参数异常:000002'


def create_body(search_word: str) -> dict:
    return {
        "baseCurrency": "EUR",
        "cryptoCurrency": "BTC",
        "payType": "Bid",
        "paymentChannel": search_word,
        "rail": "card",
        "requestedAmount": 1000,
        "requestedCurrency": "EUR"
    }


def create_headers() -> dict:
    search_word = 'x' * length
    body = create_body(search_word)
    return {
        "Content-Type": "application/json",
        "Content-Length": str(getsizeof(body))
    }


def create_permutations_list(iterable: str, length: int) -> List[str]:
    permutations_list = []
    pool = tuple(iterable)
    n = len(pool)
    r = length
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            permutations_list.append(''.join((pool[i]) for i in indices))
    return permutations_list


class BruteForcePostRequest:
    def __init__(self):
        self.length = length
        self.iterable = iterable
        self.endpoint = endpoint
        self.headers = create_headers()
        self.__run = True
        self.__count_api = start_from or 0
        self.good_answer = good_answer
        self.bad_answer = bad_answer

    def __check_answer(self, answer: dict, search_word: str) -> None:
        with open('runtime.txt', 'w') as runtime:
            print(self.__count_api, search_word, file=runtime)
        if answer['message'] == self.bad_answer:
            return
        elif answer['code'] == self.good_answer:
            self.__run = False
            with open('result.txt', 'a') as result:
                print(f'Result = {search_word}', file=result)
                print(f'Result = {search_word}')
        else:
            print(f'! = {search_word}')

    def get_api_answer(self) -> None:
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
                    with open('errors.txt', 'a') as errors:
                        print(f'Errors: {err}, search_word = {search_word}',
                              file=errors)
                    time.sleep(80)
                    response = session.post(self.endpoint, headers=self.headers,
                                            json=body)
                self.__check_answer(response.json(), search_word)
                self.__count_api += 1


def main() -> None:
    brute_force = BruteForcePostRequest()
    n = len(tuple(permutations(brute_force.iterable, length))) - start_from
    start_timestamp = time.time()
    brute_force.get_api_answer()
    task_time = round(time.time() - start_timestamp, 2)
    rps = round(n / task_time, 1)
    with open('rps_info.txt', 'a') as rps_info:
        print(
            f"| Requests: {n}; Total time: {task_time} s; RPS: {rps}. |\n",
            file=rps_info
        )


if __name__ == '__main__':
    main()
