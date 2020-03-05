import random

from redis import Redis


def get_mas():
    mas="".join(random.sample("123456789",5))
    return mas
if __name__ == '__main__':
    print(get_mas())
