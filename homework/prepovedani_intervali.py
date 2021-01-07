prepovedani = [
    (12, 18),
    (2, 5),
    (3, 8),
    (0, 4),
    (15, 19),
    (6, 9),
    (13, 17),
    (4, 8)
]


def max_boundary(intervals):
    max_value = 0
    for inter in intervals:
        if inter[1] > max_value:
            max_value = inter[1]
    return max_value


if __name__ == "__main__":
    print("\n\n_________FIRST_TASK_________")
    print("v seznamu: ", prepovedani)

    max_b = max_boundary(prepovedani)
    print("je najvecja zgornja meja: ", max_b)
    print("\n\n_________SECOND_TASK_________")

    for i in range(0, max_b + 1):
        for j, n in enumerate(prepovedani):
            if n[0] <= i <= n[1]:
                print(i, " je vsebovan v ", n)
                break
            if j == len(prepovedani) - 1:
                print(i, " je dovoljeno")
