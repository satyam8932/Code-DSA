# Two Sum Sorted Array

# array = [1, 2, 3, 4, 5, 6, 8, 8, 9]
# target = 13

# left = 0
# right = len(array) - 1
# pairs = []

# while left < right:
#     sm = array[left] + array[right]

#     if sm == target:
#         pairs.append((left, right))
#         left += 1
#         right -= 1

#     elif sm > target:
#         right -= 1
#     else:
#         left += 1

# print(pairs)

# Container with Most water

array = [1, 2, 7, 4, 9, 2, 8, 12]
max_water = 0
left, right = 0, len(array) - 1

while left < right:
    widht = right - left + 1
    height = min(array[left], array[right])
    area = widht * height

    max_water = max(max_water, area)

    if array[left] < array[right]:
        left += 1
    else: right -= 1

print(max_water)