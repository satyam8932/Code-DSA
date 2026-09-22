array = [1, 2, 3 ,5, 6, 1, 7, 8]

left , right = 0, len(array) - 1

while left < right:
    if array[left] % 2 != 0 and array[right] % 2 == 0:
        array[left], array[right] = array[right], array[left]
        left += 1
        right -= 1

    elif array[left] % 2 == 0:
        left += 1

    else:
        right -= 1

print(array)
