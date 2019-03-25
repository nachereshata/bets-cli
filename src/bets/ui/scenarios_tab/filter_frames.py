import tkinter as tk
from tkinter import ttk


class FromToFilterFrame(tk.LabelFrame):

    def __init__(self, parent, text: str, combo_values: tuple, max_value: int, min_value=0):
        super().__init__(parent, text=text)
        self.combo_box = ttk.Combobox(self, values=combo_values, state="readonly")
        self.combo_box.grid(column=0, row=0)
        self.combo_box.current(0)
        ttk.Label(self, text="From:").grid(column=1, row=0)
        self.spin_from = ttk.Spinbox(self, from_=min_value, to=max_value, state="readonly", width=5)
        self.spin_from.grid(column=2, row=0)
        self.spin_from.set(min_value)
        ttk.Label(self, text="To:").grid(column=3, row=0)
        self.spin_to = ttk.Spinbox(self, from_=min_value, to=max_value, state="readonly", width=5)
        self.spin_to.grid(column=4, row=0)
        self.spin_to.set(max_value)
        self.apply_button = ttk.Button(self, text="Apply")
        self.apply_button.grid(column=5, row=0)
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=1, sticky=tk.W)


def main():
    win = tk.Tk()
    text = "Outcomes counts filter"
    combo_values = ("1", "X", "2")
    max_value = 5
    frame = FromToFilterFrame(win, text, combo_values, max_value)
    frame.grid()
    win.mainloop()


if __name__ == '__main__':
    main()
