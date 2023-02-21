def sum_of_intervals(intervals):
    lst = sorted([list(n) for n in intervals])
    delete_lst = []
    result = []
    count = 0

    while count != len(intervals):
        for n in range(len(lst) - 1):
            if lst[n + 1][0] <= lst[0][1] <= lst[n + 1][1]:
                lst[0][1] = lst[n + 1][1]

                if lst[n + 1] not in delete_lst:
                    delete_lst.append(lst[n + 1])

            elif lst[n + 1][1] <= lst[0][1]:

                if lst[n + 1] not in delete_lst:
                    delete_lst.append(lst[n + 1])

        if lst[0] not in delete_lst or len(result) == 0:
            result.append(lst[0])

        lst = lst[1:]

        count += 1

    return sum(i[1] - i[0] for i in result)


print(sum_of_intervals([(1, 5)]))
print(sum_of_intervals([(1, 4), (7, 10), (3, 5)]))
