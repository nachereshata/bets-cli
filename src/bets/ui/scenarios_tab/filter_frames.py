import tkinter as tk
from tkinter import ttk


class FromToFilterFrame(tk.LabelFrame):

    def __init__(self, parent, text: str, combo_values: tuple, max_value: int):
        super().__init__(parent, text=text)
        self.combo_box = ttk.Combobox(self, values=combo_values, state="readonly", width=5)
        self.combo_box.grid(column=0, row=0)
        self.combo_box.current(0)
        ttk.Label(self, text="From:").grid(column=1, row=0)
        self.spin_from = ttk.Spinbox(self, from_=0, to=max_value, state="readonly", width=5)
        self.spin_from.grid(column=2, row=0)
        self.spin_from.set(0)
        ttk.Label(self, text="To:").grid(column=3, row=0)
        self.spin_to = ttk.Spinbox(self, from_=0, to=max_value, state="readonly", width=5)
        self.spin_to.grid(column=4, row=0)
        self.spin_to.set(max_value)
        self.apply_button = ttk.Button(self, text="Apply")
        self.apply_button.grid(column=5, row=0)
        for child in self.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=tk.W)


class OccurrenceFilterFrame(tk.LabelFrame):

    def __init__(self, parent, text: str, combo_values: tuple, max_value: int):
        super().__init__(parent, text=text)
        tk.Label(self, text="Allow max").grid(column=0, row=0)
        self.spin_to = ttk.Spinbox(self, from_=0, to=max_value, state="readonly", width=5)
        self.spin_to.grid(column=1, row=0)
        self.spin_to.set(max_value)
        tk.Label(self, text="occurrences of").grid(column=2, row=0)
        self.combo_box = ttk.Combobox(self, values=combo_values, state="readonly", width=5)
        self.combo_box.grid(column=3, row=0)
        self.combo_box.current(0)
        tk.Label(self, text="in a row").grid(column=4, row=0)
        self.apply_button = ttk.Button(self, text="Apply")
        self.apply_button.grid(column=5, row=0)
        for child in self.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=tk.W)


def _test_from_to_frame():
    win = tk.Tk()
    text = "Outcomes counts filter"
    combo_values = ("1", "X", "2")
    max_value = 5
    frame = FromToFilterFrame(win, text, combo_values, max_value)
    frame.grid()
    win.mainloop()


def _test_occurrence_frame():
    text = " Sequential occurrences filter"
    combo_values = tuple("min med max".split() + "1 X 2".split())
    max_value = 5
    win = tk.Tk()
    frame = OccurrenceFilterFrame(win, text, combo_values, max_value)
    frame.grid()
    frame2 = FromToFilterFrame(win, text, combo_values, 5)
    frame2.grid()
    win.mainloop()


def main():
    _test_occurrence_frame()


if __name__ == '__main__':
    main()
