
from typing import List


def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    
    # Ensure nums1 is the smaller array for binary search efficiency
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    total = m + n
    half = total // 2
    
    # Binary search on the smaller array
    left, right = 0, m
    
    while left <= right:
        # Partition index for nums1
        i = (left + right) // 2
        # Partition index for nums2 (to ensure left half has 'half' elements)
        j = half - i
        
        
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')
        
        # Check if we found the correct partition
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Found the correct partition
            if total % 2 == 1:
                # Odd total: median is the min of right elements
                return min(nums1_right, nums2_right)
            else:
                # Even total: median is average of max(left) and min(right)
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
        elif nums1_left > nums2_right:
            # nums1's partition is too far right, move left
            right = i - 1
        else:
            # nums1's partition is too far left, move right
            left = i + 1
    
    raise ValueError("Input arrays are not sorted or invalid")


def find_median_simple(nums1: List[int], nums2: List[int]) -> float:
    # Merge the two sorted arrays
    merged = []
    i, j = 0, 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    
    # Add remaining elements
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])
    
    # Find median
    n = len(merged)
    if n % 2 == 1:
        return merged[n // 2]
    else:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2


def find_median_kth_element(nums1: List[int], nums2: List[int]) -> float:
   
    def find_kth(arr1: List[int], arr2: List[int], k: int) -> int:
        
        if not arr1:
            return arr2[k]
        if not arr2:
            return arr1[k]
        
        mid1, mid2 = len(arr1) // 2, len(arr2) // 2
        
        if mid1 + mid2 < k:
            # k is in the larger half
            if arr1[mid1] > arr2[mid2]:
                return find_kth(arr1, arr2[mid2 + 1:], k - mid2 - 1)
            else:
                return find_kth(arr1[mid1 + 1:], arr2, k - mid1 - 1)
        else:
            # k is in the smaller half
            if arr1[mid1] > arr2[mid2]:
                return find_kth(arr1[:mid1], arr2, k)
            else:
                return find_kth(arr1, arr2[:mid2], k)
    
    total = len(nums1) + len(nums2)
    
    if total % 2 == 1:
        return find_kth(nums1, nums2, total // 2)
    else:
        return (find_kth(nums1, nums2, total // 2 - 1) + 
                find_kth(nums1, nums2, total // 2)) / 2


# Test the solutions
if __name__ == "__main__":
    print("Median of Two Sorted Arrays")
    print("=" * 50)
    
    # Example from the problem
    nums1 = [1, 3]
    nums2 = [2]
    
    print(f"nums1 = {nums1}")
    print(f"nums2 = {nums2}")
    
    median_bs = find_median_sorted_arrays(nums1, nums2)
    median_simple = find_median_simple(nums1, nums2)
    
    print(f"Median (Binary Search): {median_bs}")
    print(f"Median (Simple merge): {median_simple}")
    print(f"Results match: {median_bs == median_simple}")
    
    