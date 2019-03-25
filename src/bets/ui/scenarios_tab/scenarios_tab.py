import tkinter as tk

from bets.model.matches import Matches
from bets.model.scenarios import Scenarios
from bets.ui.scenarios_tab.scenarios_data_row import ScenariosDataRow


class ScenariosTab(tk.Frame):
    scenarios: Scenarios

    def __init__(self, win, tabs, matches: Matches):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.matches = matches
        self.scenarios = None
        self.tabs.add(self, text="Scenarios")
        self.var_scenarios_count = tk.IntVar()
        self.var_scenarios_count.set(0)
        self.gen_frame = tk.LabelFrame(self, text=" Initial data ")
        self.gen_frame.pack(side=tk.TOP, fill=tk.X, expand=True, anchor=tk.N, padx=4, pady=2)
        self.create_widgets()

    def _clear_views(self):
        for child in self.winfo_children():
            if child != self.gen_frame:
                child.destroy()

    def _generate_scenarios(self):
        self._clear_views()
        self.scenarios = Scenarios.from_matches(self.matches)
        self.var_scenarios_count.set(len(self.scenarios))
        ScenariosDataRow(self, "Initial", self.scenarios).pack(side=tk.TOP,
                                                               fill=tk.X,
                                                               expand=True,
                                                               anchor=tk.N,
                                                               padx=4, pady=2)

    def create_widgets(self):
        gen_btn = tk.Button(self.gen_frame, text="(Re)Generate Scenarios", command=self._generate_scenarios)
        gen_btn.grid(column=0, row=0, sticky="WE", padx=4, pady=2)
        tk.Label(self.gen_frame, text="total scenarios count:").grid(column=1, row=0, padx=10, pady=5)
        tk.Label(self.gen_frame, textvariable=self.var_scenarios_count).grid(column=2, row=0, padx=10, pady=5)
