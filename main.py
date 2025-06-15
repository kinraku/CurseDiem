def bad_character_table(pattern):
    table = {}
    for i in range(len(pattern)):
        table[pattern[i]] = i
    return table

def good_suffix_table(pattern):
    m = len(pattern)
    shift = [0] * (m + 1)
    border = [0] * (m + 1)

    i = m
    j = m + 1
    border[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j

    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]

    return shift

def boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []

    bad_char = bad_character_table(pattern)
    good_suffix = good_suffix_table(pattern)

    result = []
    s = 0  # смещение шаблона
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            result.append(s)
            s += good_suffix[0]
        else:
            bc_shift = j - bad_char.get(text[s + j], -1)
            gs_shift = good_suffix[j + 1]
            s += max(bc_shift, gs_shift)
    return result

# Тесты
if __name__ == "__main__":
    print("Тест 1:", boyer_moore("ABAAABCD", "ABC"))     # → [5]
    print("Тест 2:", boyer_moore("HERE IS A SIMPLE EXAMPLE", "EXAMPLE"))  # → [17]
    print("Тест 3:", boyer_moore("AABAACAADAABAABA", "AABA"))  # → [0, 9, 12]
    print("Тест 4:", boyer_moore("AABAACAADA", "BBB"))  # → [Пусто(не содержится)]
