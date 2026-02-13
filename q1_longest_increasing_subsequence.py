from typing import List
import bisect


def lis_dp(arr: List[int]) -> int:
    if not arr:
        return 0
    
    n = len(arr)
    # dp[i] represents the length of LIS ending at index i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            # If arr[j] < arr[i], we can extend the subsequence ending at j
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def lis_binary_search(arr: List[int]) -> int:
    if not arr:
        return 0
    
    # tails[i] is the smallest tail of all increasing subsequences of length i+1
    tails = []
    
    for num in arr:
        # Find the position where num should be inserted
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            # num is greater than all elements in tails, extend the sequence
            tails.append(num)
        else:
            # Replace tails[pos] with num (smaller tail is better)
            tails[pos] = num
    
    return len(tails)


def lis_with_sequence(arr: List[int]) -> tuple:
    
    if not arr:
        return 0, []
    
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n  # To reconstruct the sequence
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Find the index with maximum LIS length
    max_length = max(dp)
    max_index = dp.index(max_length)
    
    # Reconstruct the sequence
    sequence = []
    idx = max_index
    while idx != -1:
        sequence.append(arr[idx])
        idx = parent[idx]
    
    sequence.reverse()
    return max_length, sequence


# Test the solutions
if __name__ == "__main__":
    # Example from the problem
    arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
    length, sequence = lis_with_sequence(arr)
    print(f"LIS Length: {length}")
    print(f"One possible LIS: {sequence}")
    
    
   
