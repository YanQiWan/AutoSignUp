import time
from signup import auto_sign, print_log
from enum import Enum
import random

"""
1. 6:00~12:00

2. 20:00~24:00

"""


class Flag(Enum):
    bks = 1
    yjs = 2


def everyday_auto_signup():
    current_hour = time.localtime(time.time()).tm_hour
    if 6 <= current_hour <= 12:
        yjs_daka_success = False
    else:
        yjs_daka_success = True

    if 6 <= current_hour <= 12:
        bks_daka_success = False
    else:
        bks_daka_success = True

    while True:

        current_hour = time.localtime(time.time()).tm_hour
        current_min = time.localtime(time.time()).tm_min

        if 6 <= current_hour < 12 and 1 <= current_min <= 59:
            while not yjs_daka_success:
                print_log("研究生早打卡")
                yjs_daka_success = auto_sign(Flag.yjs.value)

        if 19 <= current_hour < 24 and 1 <= current_min < 59:
            while yjs_daka_success:
                print_log("研究生晚打卡")
                yjs_daka_success = not auto_sign(Flag.yjs.value)

        if 6 <= current_hour < 12 and 1 <= current_min <= 59:
            while not bks_daka_success:
                print_log("本科生早打卡")
                bks_daka_success = auto_sign(Flag.bks.value)

        if 21 <= current_hour < 24 and 1 <= current_min < 59:
            while bks_daka_success:
                print_log("本科生晚打卡")
                bks_daka_success = not auto_sign(Flag.bks.value)
        print_log("本次打卡轮询结束" + str(bks_daka_success) + " " + str(yjs_daka_success))
        ran = random.randrange(600, 1200)
        print_log("间隔时间" + str(ran) + "s")
        time.sleep(ran)


if __name__ == "__main__":
    everyday_auto_signup()
