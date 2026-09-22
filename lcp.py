def longestCommonPrefix(strs):
    if not strs:
        return ""
    
    for i in range(len(strs[0])):
        char = strs[0][i]
        for s in strs[1:]:
            if i >= len(s) or s[i] != char:
                return strs[0][:i]     # <-- return #1 (inside the loop)
    
    return strs[0]                     # <-- return #2 (outside the loop, at the very end)