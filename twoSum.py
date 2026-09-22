array = [1, 2, 3, 4, 5, 7, 8, 9 , 12, 16]
target = 6

# Brute Force Time O(n^2) and Space O(1)
# pairs = []

# for i in range(len(array)):
#     for j in range(i+1, len(array)):
#         if array[i] + array[j] == target:
#             pairs.append((i, j))

# print(pairs)

# Optimized with Hashmap - Time O(n) and Space O(n)
# seen = {}
# pairs = []

# for i in range(len(array)):
#     comp = target - array[i]

#     if comp in seen:
#         pairs.append((seen[comp], i))

#     seen[array[i]] = i

# print(pairs)

# Optimized with Two Pointers (Only for sorted array) -  Time O(n) and Space O(1)

pairs = []
i, j = 0, len(array)-1

while i < j:
    value = array[i] + array[j]

    if value == target:
        pairs.append((i, j))
        i += 1
        j -= 1

    elif value > target:
        j -= 1

    else:
        i += 1

print(pairs)