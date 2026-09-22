# Brute Force

array = [1,8,6,2,5,4,8,3,7]
max_water = 0

# for i in range(len(array)):
#     for j in range(len(array)):
#         width = j - i
#         height = min(array[i], array[j])

#         area = width * height

#         max_water = max(max_water, area)

# print(max_water)

# Optimized Approach

left, right = 0, len(array) - 1

while left < right:
    width = right - left
    height = min(array[left], array[right])
    area = width * height

    max_water = max(max_water, area)

    if array[left] < array[right]:
        left += 1

    else:
        right -= 1

print(max_water)