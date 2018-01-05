def search_nearest(value, L):
    if value <= L[0]: return L[0]
    if value >= L[-1]: return L[-1]

    list_length = len(L)

    if list_length % 2 == 0:
        half_right = list_length // 2
        half_left = half_right - 1
    else:
        half_right = (list_length + 1) // 2
        half_left = half_right - 1

    assert 0 <= half_left <= half_right < list_length

    if value > L[half_right]:
        return search_nearest(value, L[half_right:])
    elif value < L[half_left]:
        return search_nearest(value, L[: half_left + 1])
    else:
        left_delta = abs(value - L[half_left])
        right_delta = abs(value - L[half_right])

        return L[half_left] if left_delta <= right_delta else L[half_right]


def chunks(L, bins):
    bin_size = max(len(L) // bins, 1)
    return (L[i: i+bin_size] for i in range(0, len(L), bin_size))


test_L = [1, 2, 3, 4, 5, 6]
assert search_nearest(1, test_L) == 1
assert search_nearest(0, test_L) == 1
assert search_nearest(1.1, test_L) == 1
assert search_nearest(2.8, test_L) == 3
assert search_nearest(2.5, test_L) == 2
assert search_nearest(6, test_L) == 6
assert search_nearest(7, test_L) == 6
