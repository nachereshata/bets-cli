from tkinter import Button, Frame, Label, Entry
from tkinter import IntVar, StringVar
from tkinter.ttk import LabelFrame
from tkinter import EW, W, E
from tkinter.filedialog import askopenfilename

from typing import List
from pathlib import Path
from typing import Tuple
from bets.model.stats.stats_collection import StatsCollection
from bets.ui.constants import PAD_X, PAD_Y
from bets.utils import log


def _get_summary_counts(stats: StatsCollection) -> Tuple[int, int, int]:
    log.debug(f"getting summary counts (records, countries, tournaments)...")
    if not stats:
        log.debug(f"stats - returning zeroes ")
        return 0, 0, 0

    records_count = len(stats)
    countries_count = len(stats.unique_countries)
    tournaments_count = sum(
        [sum([len(t) for t in tournaments])
         for country, tournaments
         in stats.tournaments_by_countries().items()]
    )

    log.debug(
        f"got summary counts: records={records_count}, countries={countries_count}, tournaments={tournaments_count}")
    return records_count, countries_count, tournaments_count


def _update_padding(frame):
    for child in frame.winfo_children():
        child.grid_configure(padx=PAD_X, pady=PAD_Y)


class StatsTabFrame(Frame):
    all_stats: StatsCollection = None
    selection_stats: StatsCollection = None

    def __init__(self, win, tabs):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.tabs.add(self, text="Stats")

        self.var_total_records_count = IntVar(0)
        self.var_total_countries_count = IntVar(0)
        self.var_total_tournaments_count = IntVar(0)
        self.var_selection_records_count = IntVar(0)
        self.var_selection_countries_count = IntVar(0)
        self.var_selection_tournaments_count = IntVar(0)
        self.var_stats_file = StringVar()

        self.body_frame = Frame(self)
        self.load_stats_frame = LabelFrame(self.body_frame, text="  Load stats  ")
        self.summary_frame = LabelFrame(self.body_frame, text="  Summary  ")
        self.filter_frame = LabelFrame(self.body_frame, text="  Filter Selection")

        self.body_frame.grid(row=0, column=0, sticky=EW, padx=PAD_X, pady=PAD_Y)
        self.load_stats_frame.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky=EW)
        self.summary_frame.grid(row=1, column=0, sticky=EW)
        self.filter_frame.grid(row=2, column=0, sticky=EW)

        self.create_widgets()

        for child in self.load_stats_frame.winfo_children():
            child.grid_configure(padx=10, pady=5, sticky=EW)

        for child in self.summary_frame.winfo_children():
            child.grid_configure(padx=50, pady=10, sticky=EW)

        for child in self.filter_frame.winfo_children():
            child.grid_configure(padx=10, pady=5, sticky=EW)

    def _load_stats_from_file(self):
        self.all_stats = StatsCollection.read_json(self.var_stats_file.get())
        self.selection_stats = self.all_stats
        self._update_totals_summary()
        self._update_selection_summary()

    def _update_totals_summary(self):
        records, countries, tournaments = _get_summary_counts(self.all_stats)
        self.var_total_records_count.set(records)
        self.var_total_countries_count.set(countries)
        self.var_total_tournaments_count.set(tournaments)

    def _update_selection_summary(self):
        records, countries, tournaments = _get_summary_counts(self.selection_stats)
        self.var_selection_records_count.set(records)
        self.var_selection_countries_count.set(countries)
        self.var_selection_tournaments_count.set(tournaments)

    def create_widgets(self):

        # Create Load Stats Frame

        Label(self.load_stats_frame, text="Pick stats file: ").grid(row=0, column=0)
        file_input = Entry(self.load_stats_frame, width=60, textvariable=self.var_stats_file, state="disabled")
        file_input.grid(row=0, column=1, sticky=EW)

        def _pick_stats_file():
            self.var_stats_file.set(askopenfilename())

        def _use_bundled_file():
            self.var_stats_file.set(str(Path(__file__).parent.joinpath("matches.json")))
            self._load_stats_from_file()

        Button(self.load_stats_frame, text="Browse", command=_pick_stats_file).grid(row=0, column=2, sticky=E)
        Button(self.load_stats_frame, text="Load", command=self._load_stats_from_file).grid(row=0, column=3, sticky=E)
        Button(self.load_stats_frame, text="Use Bundled", command=_use_bundled_file).grid(row=0, column=4, sticky=E)

        # Create Summary Frame

        # Create Totals
        totals_summary_frame = LabelFrame(self.summary_frame, text="  Totals  ")
        Label(totals_summary_frame, text="Records: ").grid(column=0, row=0)
        Label(totals_summary_frame, textvariable=self.var_total_records_count).grid(column=1, row=0)
        Label(totals_summary_frame, text="Countries: ").grid(column=2, row=0)
        Label(totals_summary_frame, textvariable=self.var_total_countries_count).grid(column=3, row=0)
        Label(totals_summary_frame, text="Tournaments: ").grid(column=4, row=0)
        Label(totals_summary_frame, textvariable=self.var_total_tournaments_count).grid(column=5, row=0)
        totals_summary_frame.grid(row=0, column=0, sticky=EW)

        # Create Selection
        selection_summary_frame = LabelFrame(self.summary_frame, text="  Selection  ")
        Label(selection_summary_frame, text="Records: ").grid(column=0, row=0)
        Label(selection_summary_frame, textvariable=self.var_selection_records_count).grid(column=1, row=0)
        Label(selection_summary_frame, text="Countries: ").grid(column=2, row=0)
        Label(selection_summary_frame, textvariable=self.var_selection_countries_count).grid(column=3, row=0)
        Label(selection_summary_frame, text="Tournaments: ").grid(column=4, row=0)
        Label(selection_summary_frame, textvariable=self.var_selection_tournaments_count).grid(column=5, row=0)
        selection_summary_frame.grid(column=1, row=0, sticky=EW)
