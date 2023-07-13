import os
from pytimeparse.timeparse import timeparse
import sys
import time
import subprocess


CMD = " ".join(sys.argv[1:])
RETRY_TIME = os.environ.get("RETRY_TIME", "1m")
DT = timeparse(RETRY_TIME)
MAX = int(os.environ.get("MAX_RETRIES", "3"))

if not CMD:
    raise ValueError("Invalid command: " + CMD)


def sleep(seconds):
    for x in range(0, seconds):
        time.sleep(1)
        print(f"Slept for {x} seconds")


def log(*args):
    args = ("===",) + args + ("===",)
    print(*args)


def attempt():
    print(CMD)
    status = subprocess.call(["bash", "-c", CMD])
    if status == 0:
        log(f"Done")
        sys.exit(0)
    return status


if __name__ == "__main__":
    status = 0
    for i in range(1, MAX):
        env = dict(os.environ, ATTEMPT=i)
        log(f"Attempt {i}/{MAX}")
        status = attempt()
        log(f"Failed attempt {i}/{MAX}, sleeping for {RETRY_TIME}")
        sleep(DT) 
    status = attempt()
    log(f"Failed last attempt {MAX}/{MAX}, returning {status}")
    sys.exit(status)
