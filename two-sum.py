array = [1, 2, 3, 5, 8, 2]
target = 4

# Brute Force O(n2)

# for i in range(len(array)):
#     for j in range(i):
#         if (array[i] + array[j] == target):
#             print(j, i)

# Optimize Approach O(n) + Space Constant using Hash Map

seen = {}

for index, value in enumerate(array):
    compare = target - value
    if compare in seen:
        print(seen[compare], index)
        # break
    seen[value] = index