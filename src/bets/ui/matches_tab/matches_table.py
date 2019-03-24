import tkinter.ttk as ttk

from bets.model.matches import COLUMNS
from bets.ui.matches_observable import MatchesObserver, MatchesObservable
from bets.ui.matches_tab import constants
from bets.utils import log


class MatchesTable(ttk.LabelFrame, MatchesObserver):

    def __init__(self, parent, column=0, row=0):
        super().__init__(parent, text=" Matches ")
        self.parent = parent
        self.grid(column=column, row=row, columnspan=2, sticky="WE", padx=10, pady=5)

    def _create_row(self, row_idx: int, title, *values):
        log.debug(f"creating new match row - title={title}, values={values}")
        font = ("Consolas", 8, "normal")
        # create title
        ttk.Label(self, font=font, text=title, width=constants.W_MATCH_TITLE + 5).grid(column=0, row=row_idx)
        for col_idx, value in enumerate(values):
            if isinstance(value, float):
                value = value.__format__(".02f")

            value.center(11)
            ttk.Label(self,
                      text=value,
                      width=constants.W_MATCH_RATIO,
                      font=font
                      ).grid(column=(col_idx + 1),
                             row=row_idx)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=1, sticky="WN")

    def _create_header(self):
        self._create_row(0, COLUMNS[-1], *COLUMNS[:-1])
        for child in self.winfo_children():
            child["font"] = ("Consolas", 8, "bold")

    def _clear_table(self):
        for child in self.winfo_children():
            child.destroy()

    def matches_changed(self, matches_observable: MatchesObservable):
        self._clear_table()
        self._create_header()

        for row_idx, match in enumerate(matches_observable):
            self._create_row(row_idx + 1, match.title, *match.tuple[:-1])
            self.config(text=f" Matches ({len(matches_observable)}) ")
