import tkinter as tk
import tkinter.ttk as ttk

from bets.model.scenarios import Scenarios
from bets.ui.scenarios_tab.scenarios_data_row import ScenariosDataRow
from bets.utils import log


class GenerateScenariosFrame(ttk.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent, text=" All scenarios ")
        self.parent = parent
        self.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, padx=10, pady=5)
        self.VAR_SCENARIOS_COUNT = tk.IntVar()
        self.create_widgets()

    def _generate_scenarios(self):
        for child in self.parent.winfo_children():
            if child != self:
                child.destroy()
        log.debug("generating scenarios...")
        self.parent.scenarios = Scenarios.from_matches(self.parent.matches)
        self.VAR_SCENARIOS_COUNT.set(len(self.parent.scenarios))
        log.debug(f"got [{len(self.parent.scenarios)}] scenarios!")

        ScenariosDataRow(self.parent, "Initial", self.parent.scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

    def create_widgets(self):
        ttk.Label(self, text="Total count: ").grid(column=0, row=0, columnspan=3, padx=10, pady=5, sticky=tk.E)
        ttk.Label(self, textvariable=self.VAR_SCENARIOS_COUNT).grid(column=3, row=0, columnspan=3, padx=10, pady=5,
                                                                    sticky=tk.E)
        ttk.Button(self, text="Generate", command=self._generate_scenarios).grid(column=6, row=0, padx=10, pady=5,
                                                                                 sticky=tk.E)
