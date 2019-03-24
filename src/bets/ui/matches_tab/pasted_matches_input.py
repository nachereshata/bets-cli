import tkinter as tk
import tkinter.messagebox as mBox
import tkinter.scrolledtext as scrolledtext
import tkinter.ttk as ttk

from bets.model.matches import Matches
from bets.ui.matches_tab import constants
from bets.utils import log


class PastedMatchesInput(ttk.LabelFrame):
    def __init__(self, parent, matches: Matches, column=0, row=1):
        super().__init__(parent, text=" Pasted input ")
        self.parent = parent
        self.matches = matches
        self.grid(column=column, row=row, rowspan=4, sticky="WNE", padx=10, pady=5)
        self.create_widgets()

    def create_widgets(self):

        pasted_scroll = scrolledtext.ScrolledText(self, width=2 * constants.W_MATCH_TITLE, height=6)
        pasted_scroll.grid(column=0, row=0, rowspan=4, sticky="WNE", padx=10, pady=5)

        ttk.Label(self, text="Paste format:").grid(column=1, row=0, sticky="WE")
        paste_fmt_combo = ttk.Combobox(self, values=("efbet", "lines"), state="readonly")
        paste_fmt_combo.grid(column=1, row=1, sticky="WE", padx=4, pady=2)
        paste_fmt_combo.current(0)

        def _clear_paste_input():
            log.debug("clearing paste input...")
            pasted_scroll.delete("1.0", tk.END)

        def _add_pasted_matches():
            paste_fmt = paste_fmt_combo.get()
            log.debug(f"got paste fmt: {paste_fmt}")
            pasted_text = pasted_scroll.get("1.0", tk.END).strip()
            log.debug(f"got pasted text: [{pasted_text}]")
            log.debug("parsing matches...")
            try:
                parser = Matches.get_parser(paste_fmt)
                matches_to_add = parser(pasted_text)
                log.debug(f" got [{len(matches_to_add)}] new matches!")
                self.matches.extend(matches_to_add)
                _clear_paste_input()
            except Exception:
                mBox.showerror("Invalid input", "Check the selected paste format and try again!")

        ttk.Button(self, text="Add", command=_add_pasted_matches).grid(column=1, row=2, sticky="WE", padx=4, pady=2)
        ttk.Button(self, text="Clear", command=_clear_paste_input).grid(column=1, row=3, sticky="WE", padx=4, pady=2)
