def binary_search(arr, target):
    iterations = 0
    low = 0
    high = len(arr) - 1
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] == target:
            return (iterations, arr[mid])

        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

        if arr[mid] >= target:
            upper_bound = arr[mid]

    return (iterations, upper_bound)

sorted_array = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
target_value = 2.2

result = binary_search(sorted_array, target_value)
print(f"Number of iterations: {result[0]}")
print(f"Upper limit: {result[1]}")
