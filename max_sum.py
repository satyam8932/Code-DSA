# maximum subarray

arr = [1, -2, -4, 5, 6, 2 ,3, -5]
max_sum = float("-inf")
curr_chain = 0

for i in range(len(arr)):
    curr_chain += arr[i]

    max_sum = max(max_sum, curr_chain)

    if curr_chain < 0:
        curr_chain = 0

print(max_sum)