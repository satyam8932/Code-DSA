# Optimized Approach (using sorted array)

array = [2, 2, 2, 4, 4, 4, 6, 6, 6]
target = 12
pairs = []

for i in range(len(array)):
    if i > 0 and array[i] == array[i - 1]:
        continue

    left, right = i+1, len(array) - 1

    while left < right:
        sm = array[i] + array[left] + array[right]
        if sm == target:
            pairs.append([array[i], array[left], array[right]])
            left += 1
            right -= 1

            while left < right and array[left] == array[left - 1]:
                left += 1
            while left < right and array[right] == array[right + 1]:
                right -= 1

        elif sm > target:
            right -= 1
        else:
            left += 1

print(pairs)

