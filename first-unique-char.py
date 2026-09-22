s = "leetcode"
maps = {}

for i in range(len(s)):
    if s[i] not in maps:
        maps[s[i]] = 1
    else:
        maps[s[i]] += 1
# print(maps)
for k in range(len(s)):
    print(k)

    if maps[s[k]] == 1:
        print(k)
