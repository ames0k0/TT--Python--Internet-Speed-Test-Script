

# Dependencies
#   - Python 3.12.3


# Testing the internet speed by downloading a source / media
#
#
# script -> [ networkIn  ] -> source \
# script <- [ networkOut ] <- source


import time
import math
import urllib.request
from collections import Counter


# REQUEST_SOURCE: str = "https://www.python.org"    # could be an args
REQUEST_SOURCE: str = "https://file-examples.com/wp-content/storage/2017/10/file_example_PNG_3MB.png"
REQUESTS_COUNT: int = 10

DOWNLOADED_CONTENTS_SIZE_B: int = 0
DOWNLOADED_CONTENTS_DURATION: list[float] = []


# DEBUG ZONE
ERRORS: list[str] = []


# continious requests (not parallel)
for _ in range(REQUESTS_COUNT):

    req_start = time.perf_counter()
    try:
        # Request Block
        with urllib.request.urlopen(REQUEST_SOURCE) as response:
            DOWNLOADED_CONTENTS_SIZE_B += response.length
    except Exception as e:
        ERRORS.append(e.reason)
        continue

    req_stop = time.perf_counter()
    DOWNLOADED_CONTENTS_DURATION.append(req_stop - req_start)


# Non downloaded images
if not DOWNLOADED_CONTENTS_DURATION:
    if ERRORS:
        print(f"Ошибки:")
        for err_a, err_t in Counter(ERRORS).items():
            print(f"{err_a} - {err_t} /раз")
    exit()


# Medium req time
mrt = sum(DOWNLOADED_CONTENTS_DURATION) / len(DOWNLOADED_CONTENTS_DURATION)
print(f"Среднее время запроса: {mrt:.2f} /с")

# GoogleAI: "Для сетевых данных (сетевого трафика) стандартно используется десятичная система."
DOWNLOADED_CONTENTS_SIZE_MB = DOWNLOADED_CONTENTS_SIZE_B / 1_000_000
print(f"Объем скачанных данных: {DOWNLOADED_CONTENTS_SIZE_MB:.2f} /мб")

traffic_by_sec = DOWNLOADED_CONTENTS_SIZE_MB / mrt
print(f"Скорость: {traffic_by_sec:.2f} мб/с")




