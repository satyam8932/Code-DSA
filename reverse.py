array = [1, 2, 3, 4, 5, 6, 7, 8]

i, j = 0, len(array) - 1

while i < j:
    array[i], array[j] = array[j], array[i]
    i += 1
    j -= 1

print(array)