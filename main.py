import pyautogui
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import threading
import time
import keyboard


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x500")  # Set the window size to 300x500 pixels
        self.root.configure(bg="#21252b")
        self.root.attributes("-toolwindow", 1)
        self.root.minsize(300, 500)

        self.coordinates = []
        self.clicking = False
        self.interval = 1000  # default interval in milliseconds

        # Добавление области с текстом для обозначения функции кнопок
        button_labels_frame = tk.Frame(root, bg="#282c34")
        button_labels_frame.pack(pady=10, padx=10, anchor="w")

        # Обозначение функций кнопок
        set_coords_label = tk.Label(button_labels_frame, text="Set Coordinates [S]", bg="#282c34", fg="white")
        set_coords_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")

        start_clicking_label = tk.Label(button_labels_frame, text="Start Clicking [Space]", bg="#282c34", fg="white")
        start_clicking_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        stop_clicking_label = tk.Label(button_labels_frame, text="Stop Clicking [ESC]", bg="#282c34", fg="white")
        stop_clicking_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        clear_coords_label = tk.Label(button_labels_frame, text="Clear Coordinates [Del]", bg="#282c34", fg="white")
        clear_coords_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="w")

        # Область для интервала и его описания
        interval_frame = tk.Frame(root, bg="#282c34")
        interval_frame.pack(pady=10, padx=10, anchor="w")  # прижатие к левому краю

        # Описание интервала
        interval_label = tk.Label(interval_frame, text="Click Interval (ms):", fg="white", bg="#282c34")
        interval_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Поле ввода интервала
        self.interval_entry = tk.Entry(interval_frame)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.interval_entry.insert(0, "1000")  # Устанавливаем значение по умолчанию

        # Привязываем метод для проверки ввода
        self.interval_entry.bind('<Key>', self.validate_interval_input)
        self.interval_entry.bind('<BackSpace>', self.validate_interval_input)

        frame = tk.Frame(root)
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        columns = ("X", "Y")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")

        # Настройка скроллирования
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        total_width = root.winfo_width()  # Получаем ширину окна
        self.tree.column("X", width=total_width // 2)
        self.tree.column("Y", width=total_width // 2)


        # Bind keys for setting coordinates and starting clicking
        root.bind('<KeyPress-s>', self.set_coordinates_key)
        root.bind('<KeyPress-space>', self.start_clicking_key)

        # Set up a global hotkey for stopping the clicker
        keyboard.add_hotkey('esc', self.stop_clicking_globally)

        # Добавление глобальной горячей клавиши для очистки координат
        keyboard.add_hotkey('delete', self.clear_coordinates)

    def set_coordinates(self):
        x, y = pyautogui.position()
        self.coordinates.append((x, y))
        self.update_coordinates_label()

    def set_coordinates_key(self, event):
        self.set_coordinates()

    def update_coordinates_label(self):
        self.tree.delete(*self.tree.get_children())
        for x, y in self.coordinates:
            self.tree.insert("", "end", values=(x, y))

    def clear_coordinates(self):
        self.coordinates = []
        self.update_coordinates_label()

    # Метод для проверки ввода интервала
    def validate_interval_input(self, event):
        input_text = self.interval_entry.get()
        if event.keysym == 'BackSpace' and not input_text:
            return  # Пропускаем обработку удаления, если поле пустое
        elif event.char.isdigit() or event.keysym == 'BackSpace':
            return  # Пропускаем обработку, если введенный символ - цифра или это Backspace
        else:
            return "break"  # Отменяем ввод неправильного символа

    # Метод для чтения значения интервала с обработкой ошибок
    def get_interval_value(self):
        input_text = self.interval_entry.get()
        if not input_text:
            # Если строка пустая, устанавливаем значение по умолчанию
            self.interval = 1000
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, "1000")
        else:
            try:
                interval = int(input_text)
            except ValueError:
                # Если введено не целое число, устанавливаем значение по умолчанию
                self.interval = 1000
                self.interval_entry.delete(0, tk.END)
                self.interval_entry.insert(0, "1000")


    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            threading.Thread(target=self.clicker).start()

    def start_clicking_key(self, event):
        self.start_clicking()

    def stop_clicking(self):
        self.clicking = False

    def stop_clicking_globally(self):
        self.clicking = False
        print("Clicking stopped by pressing ESC")

    def clicker(self):
        while self.clicking:
            for x, y in self.coordinates:
                if not self.clicking:
                    break
                pyautogui.click(x, y)
                time.sleep(self.interval / 1000.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
