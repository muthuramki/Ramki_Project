a = {
    "2": {"a": [1, 2, 3, 4, 2]},
    "3": {"b": {"w": "2"}},
    "r": 2,
    "t": (2, "2", 3),
    "y": {2, 3, 4, 5}
}

def count_number_2(data):
    count = 0
    if isinstance(data, (int, float)) and data == 2:
        return 1
    elif isinstance(data, (list, tuple, set)):
        return sum(count_number_2(item) for item in data)
    elif isinstance(data, dict):
        return sum(count_number_2(key) + count_number_2(value) for key, value in data.items())
    return 0


result = count_number_2(a)
print(f"Count of number 2: {result}")
