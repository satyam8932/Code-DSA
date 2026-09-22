# Reverse a string

# string = "satyam"

# newLstStr = list(string)

# i,j = 0, len(newLstStr) - 1

# while i < j:
#     newLstStr[i], newLstStr[j] = newLstStr[j], newLstStr[i]
#     i += 1  # ✅ Move inward from left
#     j -= 1  # ✅ Move inward from right

# string = "".join(newLstStr)

# print(string)

# find max


array = [11,2,3,22,52, 1,1, 52,56,21,55,26]

# maxN = -1
# import sys
# minN = sys.maxsize

# for i in array:
#     if i > maxN:
#         maxN = i
#     if i < minN:
#         minN = i

# print(maxN, minN)

# array.sort()
# print(array[len(array)-1])
# sum = 0
# for i in array:
#     sum += i

# print(sum)

# count frequency
# maps = {}

# for i in range(len(array)):
#     if (array[i] in maps):
#         maps[array[i]] += 1
#     else:
#         maps[array[i]] = 1

# print(maps)

# remove duplicates

# array.sort()
# unique = 0

# for cur in range(1, len(array)):
#     if array[unique] != array[cur]:
#         unique += 1
#         array[unique] = array[cur]

# print(array[:unique + 1])


# palindrome check
# num = 1001
# string = str(num)

# let's use two pointer approach

# st, end = 0, len(string) - 1

# while st < end:
#     if string[st] != string[end]:
#         print("Not palindrome")
#         break
#     st += 1
#     end -= 1
# print('palindrome')

