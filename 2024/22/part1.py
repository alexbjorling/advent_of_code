import numpy as np

with open("input.txt", "r") as fp:
    data = list(map(int, fp.read().splitlines()))

def prune(num):
    # keep the last 24 bits
    return num % 16777216

def mix(num, new):
    # xor
    return num ^ new

def generate(num):
    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    num = prune(mix(num, num * 2048))
    return num

def generaten(num, n):
    for i in range(n):
        num = generate(num)
    return num

tot = 0
for d in data:
    tot += generaten(d, 2000)
assert tot == 17965282217