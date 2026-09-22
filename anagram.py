s = "anagram"
t = "nagaram"

# Bruteforce
# s_list = list(s)
# t_list = list(t)

# if len(s_list) != len(t_list):
#     print('not')

# s_list.sort()
# t_list.sort()

# i = 0
# while i < len(s_list):
#     if s_list[i] != t_list[i]:
#         print('not a')
#         break
#     i += 1

# print("yes")

# Optimal using maps

if len(s) != len(t): print("no")

map_s = {}
map_t = {}

for i in s:
    if i not in map_s:
        map_s[i] = 1
    else:
        map_s[i] += 1

for j in t:
    if j not in map_t:
        map_t[j] = 1
    else:
        map_t[j] += 1

for char in map_s:
    if char not in map_t:
        print("no")

    if map_s[char] != map_t[char]:
        print("no")

print('yes')

