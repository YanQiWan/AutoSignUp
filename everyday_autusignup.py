import time
from signup import auto_sign, print_log

"""
1. 6:00~12:00

2. 20:00~24:00

"""


def everyday_auto_signup():
    current_hour = time.localtime(time.time()).tm_hour
    if 6 <= current_hour <= 12:
        daka_succes = False
    else:
        daka_succes = True

    while True:

        current_hour = time.localtime(time.time()).tm_hour
        current_min = time.localtime(time.time()).tm_min

        if 6 <= current_hour <= 12 and 1 <= current_min <= 59:
            while not daka_succes:
                daka_succes = auto_sign()
                time.sleep(1200)

        if 20 <= current_hour <= 24 and 1 <= current_min < 59:
            while daka_succes:
                daka_succes = not auto_sign()
                time.sleep(1200)
        print_log("")
        time.sleep(300)


if __name__ == "__main__":
    everyday_auto_signup()
