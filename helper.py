def binary_search_recursive(array, element, start, end):
    if start > end or start == len(array):
        return False

    mid = (start + end) // 2
    if element == array[mid]:
        return True

    if element < array[mid]:
        return binary_search_recursive(array, element, start, mid-1)
    else:
        return binary_search_recursive(array, element, mid+1, end)
