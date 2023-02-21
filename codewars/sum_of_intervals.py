def sum_of_intervals(intervals):
    sorted_intervals = sorted([list(n) for n in intervals])
    delete_lst = []
    result = []
    count = 0

    while count != len(intervals):
        for n in range(len(sorted_intervals) - 1):
            if sorted_intervals[n + 1][0] <= sorted_intervals[0][1] <= sorted_intervals[n + 1][1]:
                sorted_intervals[0][1] = sorted_intervals[n + 1][1]

                if sorted_intervals[n + 1] not in delete_lst:
                    delete_lst.append(sorted_intervals[n + 1])

            elif sorted_intervals[n + 1][1] <= sorted_intervals[0][1]:

                if sorted_intervals[n + 1] not in delete_lst:
                    delete_lst.append(sorted_intervals[n + 1])

        if sorted_intervals[0] not in delete_lst or len(result) == 0:
            result.append(sorted_intervals[0])

        sorted_intervals = sorted_intervals[1:]

        count += 1

    return sum(i[1] - i[0] for i in result)


print(sum_of_intervals([(1, 5)]))
print(sum_of_intervals([(1, 4), (7, 10), (3, 5)]))
