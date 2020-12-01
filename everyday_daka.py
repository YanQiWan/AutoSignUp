import time
from signup import auto_sign
"""
1. 6:00~12:00

2. 20:00~24:00

"""
if __name__ == "__main__":

    current_hour = time.localtime(time.time()).tm_hour
    if 6 <= current_hour <= 12:
        daka_succes = False
    else:
        daka_succes = True

    while True:

        current_hour = time.localtime(time.time()).tm_hour
        current_min = time.localtime(time.time()).tm_min

        if 6 <= current_hour <= 12 and 30 <= current_min <= 59:
            while not daka_succes:
                daka_succes = auto_sign()
                time.sleep(1400)

        if 20 <= current_hour <= 24 and 0 <= current_min < 59:
            while daka_succes:
                daka_succes = not auto_sign()
                time.sleep(1400)

        time.sleep(300)