import tkinter as tk
from tkinter import messagebox

def preprocess_bad_character_rule(pattern):
    # Создаёт таблицу плохих символов: для каждого символа — индекс его последнего вхождения в шаблоне
    bad_char = {}
    length = len(pattern)
    for i in range(length):
        bad_char[pattern[i]] = i
    return bad_char

def boyer_moore_search(text, pattern, text_widget):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    bad_char = preprocess_bad_character_rule(pattern)
    s = 0  # смещение шаблона относительно текста

    text_widget.insert(tk.END, f"Текст: {text}\n")
    text_widget.insert(tk.END, f"Шаблон: {pattern}\n")
    text_widget.insert(tk.END, "-" * 40 + "\n")

    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        text_widget.insert(tk.END, f"Сдвиг: {s}\n")
        text_widget.insert(tk.END, f"Сравниваемая часть текста: {text[s:s+m]}\n")

        if j < 0:
            text_widget.insert(tk.END, "Полное совпадение найдено!\n")
            return s
        else:
            text_widget.insert(tk.END, f"Несовпадение в позиции {s + j}: символ '{text[s + j]}' != '{pattern[j]}'\n")

            bad_char_shift = j - bad_char.get(text[s + j], -1)
            text_widget.insert(tk.END, f"Сдвиг по правилу плохого символа: {bad_char_shift}\n")

            сдвиг = max(1, bad_char_shift)
            text_widget.insert(tk.END, f"Применяем сдвиг: {сдвиг}\n\n")

            s += сдвиг

    return n

def visualize_search():
    text = text_entry.get()
    pattern = pattern_entry.get()
    text_widget.delete(1.0, tk.END)  # Очистить предыдущие результаты

    result = boyer_moore_search(text, pattern, text_widget)

    if result == len(text):
        messagebox.showinfo("Результат", f"Шаблон '{pattern}' не найден в тексте.")
    else:
        messagebox.showinfo("Результат", f"Шаблон '{pattern}' найден на позиции {result}.")

# Создаём главное окно
root = tk.Tk()
root.title("Визуализация поиска Бойера-Мура")

# Ввод текста
tk.Label(root, text="Текст:").grid(row=0, column=0, sticky="w")
text_entry = tk.Entry(root, width=50)
text_entry.grid(row=0, column=1)

# Ввод шаблона
tk.Label(root, text="Шаблон:").grid(row=1, column=0, sticky="w")
pattern_entry = tk.Entry(root, width=50)
pattern_entry.grid(row=1, column=1)

# Кнопка запуска поиска
search_button = tk.Button(root, text="Поиск", command=visualize_search)
search_button.grid(row=2, column=0, columnspan=2, pady=5)

# Текстовое окно для отображения шагов сравнения
text_widget = tk.Text(root, height=15, width=80)
text_widget.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
