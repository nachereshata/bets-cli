from tkinter import StringVar
from tkinter.ttk import Label, LabelFrame

from bets.ui.matches_observable import MatchesObserver, MatchesObservable


class MatchesTableFrame(LabelFrame, MatchesObserver):

    def __init__(self, parent, matches: MatchesObservable, column=0, row=2):
        super().__init__(parent, text=" Matches ")
        self.grid(column=column, row=row, columnspan=2, padx=4, pady=2, sticky="WNES")
        self.var_table = StringVar()
        self.table_label = Label(self, textvariable=self.var_table, font="Consolas")
        self.table_label.grid(column=0, row=0, padx=4, pady=2, sticky="WNES")
        matches.add_observer(self)

    def matches_changed(self, matches_observable: MatchesObservable):
        if matches_observable:
            self.var_table.set(matches_observable.table)
        else:
            self.var_table.set("")
