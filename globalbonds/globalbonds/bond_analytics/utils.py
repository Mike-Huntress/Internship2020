

def binary_search(low, high, target, func, precision=0.000001):
    pivot = (low + high) / 2
    guess = func(pivot)
    if abs(target - guess) < precision:
        return pivot
    elif guess > target:
        return binary_search(pivot, high, target, func, precision=precision)
    else:
        return binary_search(low, pivot, target, func, precision=precision)
