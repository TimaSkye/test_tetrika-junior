def merge_intervals(intervals):
    """
    Объединяет пересекающиеся интервалы.
    """
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged

def cut_intervals_to_lesson(intervals, lesson_start, lesson_end):
    """
    Обрезает интервалы по границам урока.
    """
    result = []
    for start, end in intervals:
        start = max(start, lesson_start)
        end = min(end, lesson_end)
        if start < end:
            result.append([start, end])
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Возвращает общее время одновременного присутствия ученика и учителя на уроке.
    """
    lesson_start, lesson_end = intervals['lesson']
    # Формируем интервалы для ученика и учителя
    pupil_intervals = [[intervals['pupil'][i], intervals['pupil'][i+1]] for i in range(0, len(intervals['pupil']), 2)]
    tutor_intervals = [[intervals['tutor'][i], intervals['tutor'][i+1]] for i in range(0, len(intervals['tutor']), 2)]
    # Обрезаем по времени урока
    pupil_intervals = cut_intervals_to_lesson(pupil_intervals, lesson_start, lesson_end)
    tutor_intervals = cut_intervals_to_lesson(tutor_intervals, lesson_start, lesson_end)
    # Объединяем пересекающиеся интервалы
    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)
    # Считаем общее время пересечений
    i, j = 0, 0
    total = 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        start = max(pupil_intervals[i][0], tutor_intervals[j][0])
        end = min(pupil_intervals[i][1], tutor_intervals[j][1])
        if start < end:
            total += end - start
        if pupil_intervals[i][1] < tutor_intervals[j][1]:
            i += 1
        else:
            j += 1
    return total
