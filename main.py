"""Handwritten, tested by human...
"""

import argparse
import urllib.request
import urllib.error
from enum import StrEnum, auto
from functools import reduce
from functools import wraps
from itertools import repeat
from time import perf_counter
from typing import TypeAlias, Any


class AppStateEnum(StrEnum):
    flag_debug = auto()
    request_url = auto()

    # XXX: Keeping the all succeeded network responses lenght
    # may and will be used to check how many and so on...
    network_responses_length = auto()
    network_transaction_elapsed_time_s = auto()


AppStateType: TypeAlias = dict[AppStateEnum, Any]


def deco_error_handler(func):
    @wraps(func)
    def network_request(*args, **kwargs) -> int | None:
        error_message: str = ""
        try:
            return func(*args, **kwargs)
        except urllib.error.URLError as ue:
            error_message = str(ue.reason)
        except Exception as e:
            error_message = e.args[0]
        if kwargs["app_state"][AppStateEnum.flag_debug]:
            print(f"Ошибка: {error_message}")
            # XXX: No need to try N time for the same URL
            # exit()
        return None
    return network_request


def deco_time_network_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[int | None, float]:
        network_request_start = perf_counter()
        return func(*args, **kwargs), perf_counter() - network_request_start
    return wrapper


def calc_network_response_length_and_time(
    app_state: AppStateType,
    request_url: str,
):
    network_response_length, network_transaction_elapsed_time_s = \
        make_network_request(
            app_state=app_state,
        )

    if network_response_length is None:
        return app_state

    app_state[AppStateEnum.network_responses_length].append(
        network_response_length
    )
    app_state[
        AppStateEnum.network_transaction_elapsed_time_s
    ] += network_transaction_elapsed_time_s
    return app_state


@deco_time_network_request
@deco_error_handler
def make_network_request(*, app_state: AppStateType) -> int:
    with urllib.request.urlopen(app_state[AppStateEnum.request_url]) as response:
        return response.length


def main(
        *,
        flag_debug: bool,
        request_url: str,
        total_downloads: int = 10,
) -> None:
    app_state: AppStateType = reduce(
        calc_network_response_length_and_time,
        repeat(request_url, times=total_downloads),
        {
            AppStateEnum.flag_debug: flag_debug,
            AppStateEnum.request_url: request_url,
            AppStateEnum.network_responses_length: [],
            AppStateEnum.network_transaction_elapsed_time_s: 0,
        },
    )

    if not app_state[AppStateEnum.network_responses_length]:
        return

    total_nrl_b = sum(app_state[AppStateEnum.network_responses_length])

    medium_ntet_s = app_state[AppStateEnum.network_transaction_elapsed_time_s] / len(
        app_state[AppStateEnum.network_responses_length]
    )
    print(f"Среднее время запроса: {medium_ntet_s:.2f} /с")

    # GoogleAI: "Для сетевых данных (сетевого трафика) стандартно используется десятичная система."
    total_ntet_mb = total_nrl_b / 1_000_000
    print(f"Объем скачанных данных: {total_ntet_mb:.2f} /мб")

    traffic_by_sec = total_ntet_mb / medium_ntet_s
    print(f"Скорость: {traffic_by_sec:.2f} мб/с")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="python3 main.py -[u]rl -[c]ount",
        epilog="""
        epilog:
        python3 main.py -u https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/refs/heads/master/Python/Tohru-Dragon_Maid_Beginning_Python.jpg -c 50
        """
    )
    parser.add_argument(
        "-u", "--url",
        required=True, type=str,
        help="Адрес, куда стучаться",
    )
    parser.add_argument(
        "-c", "--count",
        required=False, type=int, default=10, choices=list(range(10, 51, 5)),
        help="Количество последовательных запросов к этому адресу",
    )

    args = parser.parse_args()

    main(
        flag_debug=True,
        request_url=args.url,
        total_downloads=args.count,
    )

