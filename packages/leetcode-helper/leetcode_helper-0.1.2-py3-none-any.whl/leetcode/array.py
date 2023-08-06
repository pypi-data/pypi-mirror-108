def printWithIndex(nums, idxs=[]):
    def numLen(num):
        cnt = 1 if num >= 0 else 2
        num = abs(num)
        while num//10:
            num //= 10
            cnt += 1
        return cnt
    
    num_str = []
    idx_str = []
    
    for i, n in enumerate(nums):
        num_str.append(str(n))
        if len(idxs) == 0 or (len(idxs) > 0 and i in idxs):
            idx_str.append(" "*(numLen(n)-numLen(i)) + str(i))
        else:
            idx_str.append(" "*numLen(n))
    
    print("  " + " ".join(num_str))
    print("^ " + " ".join(idx_str))