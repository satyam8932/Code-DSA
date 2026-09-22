array = [2,3,1,2,4,3]
left = 0
target = 7
msb = float('inf')
sumC = 0

for right in range(len(array)):
    sumC += array[right]

    while sumC >= target:
        current_window_size = right - left + 1
        msb = min(msb, current_window_size)

        sumC -= array[left]
        left += 1

print(msb if msb != float('inf') else 0)

