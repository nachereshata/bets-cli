import tkinter as tk
import tkinter.messagebox as mBox
import tkinter.ttk as ttk

from bets.model.matches import Matches
from bets.ui.matches_tab import constants
from bets.utils import log


class SingleMatchInput(ttk.LabelFrame):
    def __init__(self, parent, matches: Matches, column=1, row=1):
        super().__init__(parent, text=" Manual input ")
        self.parent = parent
        self.matches = matches
        self.VAR_MATCH_TITLE = tk.StringVar()
        self.VAR_MATCH_1 = tk.DoubleVar()
        self.VAR_MATCH_x = tk.DoubleVar()
        self.VAR_MATCH_2 = tk.DoubleVar()
        self.grid(column=column, row=row, sticky="WNE", rowspan=4, padx=10, pady=5)
        self.create_widgets()

    def create_widgets(self):

        ttk.Label(self, text="Title:").grid(column=0, row=0)
        title_input = ttk.Entry(self, width=constants.W_MATCH_TITLE - 5, textvariable=self.VAR_MATCH_TITLE)
        title_input.grid(column=1, row=0, columnspan=2)
        title_input.focus()

        ttk.Label(self, text="1:").grid(column=0, row=1)
        ttk.Entry(self, width=constants.W_MATCH_RATIO, textvariable=self.VAR_MATCH_1).grid(column=1, row=1)

        ttk.Label(self, text="X:").grid(column=0, row=2)
        ttk.Entry(self, width=constants.W_MATCH_RATIO, textvariable=self.VAR_MATCH_x).grid(column=1, row=2)

        ttk.Label(self, text="2:", ).grid(column=0, row=3)
        ttk.Entry(self, width=constants.W_MATCH_RATIO, textvariable=self.VAR_MATCH_2).grid(column=1, row=3)

        def _clear_inputs():
            self.VAR_MATCH_TITLE.set("")
            self.VAR_MATCH_1.set(0.0)
            self.VAR_MATCH_x.set(0.0)
            self.VAR_MATCH_2.set(0.0)
            title_input.focus()

        def _add_single_match():
            try:
                self.matches.add_match(self.VAR_MATCH_TITLE.get(),
                                       self.VAR_MATCH_1.get(),
                                       self.VAR_MATCH_x.get(),
                                       self.VAR_MATCH_2.get())
            except Exception as ex:
                log.debug(f"Caught exception: {ex}")
                mBox.showerror("Invalid input", "Try again with different values!")

            _clear_inputs()

        def _clear_all():
            self.matches.clear()

        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(column=2, row=1, rowspan=3, sticky="NE")
        ttk.Button(buttons_frame, text="Add", command=_add_single_match).grid(column=0, row=0, sticky="NE")
        ttk.Button(buttons_frame, text="Clear", command=_clear_inputs).grid(column=0, row=1, sticky="NE")
        ttk.Button(buttons_frame, text="Clear all", command=_clear_all).grid(column=0, row=2, sticky="NE")

        for child in self.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=tk.W)
