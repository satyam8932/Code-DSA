# Best time to buy and sell stock

arr = [7, 1, 2, 8, 9, 5, 4, 3, 8]
import sys
cheap = sys.maxsize
mx_profit = 0
for i in range(len(arr)):
    if cheap > arr[i]:
        cheap = arr[i]

    cur_profit = arr[i] - cheap

    if cur_profit > mx_profit:
        mx_profit = cur_profit


print(cheap, mx_profit)