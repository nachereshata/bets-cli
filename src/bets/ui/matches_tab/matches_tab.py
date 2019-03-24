import tkinter as tk

from bets.ui.matches_tab.matches_table import MatchesTable
from bets.ui.matches_tab.pasted_matches_input import PastedMatchesInput
from bets.ui.matches_tab.single_match_input import SingleMatchInput


class MatchesTab(tk.Frame):
    matches_table: MatchesTable
    single_match_input: SingleMatchInput
    pasted_matches_input: PastedMatchesInput

    def __init__(self, win, tabs, matches):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.matches = matches
        self.tabs.add(self, text="Matches")
        self.create_widgets()

    def create_widgets(self):
        # create matches table
        self.matches_table = MatchesTable(self)
        self.matches.add_observer(self.matches_table)
        self.matches_table.matches_changed(self.matches)
        # single match input
        self.single_match_input = SingleMatchInput(self, self.matches)

        # pasted match input
        self.pasted_matches_input = PastedMatchesInput(self, self.matches)
