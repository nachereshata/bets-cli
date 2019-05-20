from tkinter import Frame, Label
from tkinter import EW, W, E, RAISED as SUNKEN
from tkinter.filedialog import askopenfilename

from tkinter.ttk import Button, Combobox, Entry, LabelFrame

from pathlib import Path

from bets.model.stats.stats_collection import StatsCollection
from bets.ui.constants import PAD_X, PAD_Y
from bets.utils import log

ALL = "All"


class LoadStatsFrame(LabelFrame):

    def __init__(self, parent, set_stats):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text="  Load Stats  ")

        self.parent = parent
        self.set_stats = set_stats

        Label(self, text="Pick stats file: ").grid(row=0, column=0, sticky=W)

        self.file_input = Entry(self, width=60, text="Not set!", state="readonly")
        self.file_input.grid(row=0, column=1, sticky=EW)

        Button(self, text="Browse", command=self._browse_for_stats).grid(row=0, column=2, sticky=E)
        Button(self, text="Use Bundled", command=self._use_bundled_stats).grid(row=0, column=3, sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=PAD_Y, sticky=EW)

    def load_stats(self, file: str):
        self.file_input.configure(text=file)
        stats = StatsCollection.read_json(file)
        self.set_stats(stats)

    def _browse_for_stats(self):
        self.load_stats(askopenfilename())

    def _use_bundled_stats(self):
        self.load_stats(str(Path(__file__).parent.joinpath("matches.json")))


class CountsSummaryFrame(LabelFrame):
    def __init__(self, parent, text):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text=text)

    def set_stats(self, stats: StatsCollection):
        for child in self.winfo_children():
            child.destroy()

        col_idx = 0
        for name, count in stats.get_counters().items():
            Label(self, text=f"{name}: ").grid(row=0, column=col_idx)
            col_idx += 1
            Label(self, text=str(count), relief=SUNKEN).grid(row=0, column=col_idx)
            col_idx += 1

        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=2 * PAD_Y)


class FilterSelectionFrame(LabelFrame):
    def __init__(self, parent, get_all, get_selection, set_selection):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text="  Filters  ")

        self.parent = parent
        self.get_all = get_all
        self.get_selection = get_selection
        self.set_selection = set_selection

        Label(self, text="Country: ").grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky=EW)

        self.cb_country = Combobox(self, state="readonly", values=("All",), width=30)
        self.cb_country.bind("<<ComboboxSelected>>", self.apply_country_filter)
        self.cb_country.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y, sticky=EW)
        self.cb_country.current(0)

        Label(self, text="Tournament: ").grid(row=0, column=2, padx=PAD_X, pady=PAD_Y, sticky=EW)

        self.cb_tournament = Combobox(self, state="readonly", values=("All",), width=50)
        self.cb_tournament.bind("<<ComboboxSelected>>", self.apply_tournament_filter)
        self.cb_tournament.current(0)
        self.cb_tournament.grid(row=0, column=3, padx=PAD_X, pady=PAD_Y, sticky=EW)

        Button(self, text="Reset", command=self.reset_filters).grid(row=0, column=4)

    def set_countries(self, *countries):
        values = (ALL,) + tuple(countries)
        self.cb_country.configure(values=values)

    def set_tournaments(self, *tournaments):
        values = (ALL,) + tuple(tournaments)
        self.cb_tournament.configure(values=values)

    def apply_country_filter(self, _):
        country = self.cb_country.get()
        selection = self.get_all() if country == ALL else self.get_selection().with_country(country)
        self.set_selection(selection)

    def apply_tournament_filter(self, _):
        tournament = self.cb_tournament.get()
        selection = self.get_all() if tournament == ALL else self.get_selection().with_tournament(tournament)
        self.set_selection(selection)

    def reset_filters(self):
        self.set_selection(self.get_all())
        self.cb_country.current(0)
        self.cb_tournament.current(0)


class StatsTabFrame(Frame):

    def __init__(self, win, tabs):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.tabs.add(self, text="Stats")

        self.stats: StatsCollection = None
        self.selection: StatsCollection = None

        self.body_frame = Frame(self)
        self.body_frame.grid(row=0, column=0, sticky=EW, padx=PAD_X, pady=PAD_Y)

        # Load
        self.load_stats_frame = LoadStatsFrame(self.body_frame, self.set_stats)
        self.load_stats_frame.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky=EW)

        # Summary
        self.summary_frame = LabelFrame(self.body_frame, text="  Records  ")
        self.summary_frame.grid(row=1, column=0, sticky=EW)

        self.summary_frame_all = CountsSummaryFrame(self.summary_frame, text="  All  ")
        self.summary_frame_all.grid(row=0, column=0, padx=2 * PAD_X, pady=2 * PAD_Y, sticky=EW)

        self.summary_frame_selection = CountsSummaryFrame(self.summary_frame, text="  Selection  ")
        self.summary_frame_selection.grid(column=1, row=0, padx=2 * PAD_X, pady=2 * PAD_Y, sticky=EW)

        # Filter
        self.filter_frame = FilterSelectionFrame(self.body_frame, self.get_all, self.get_selection, self.set_selection)
        self.filter_frame.grid(row=2, column=0, sticky=EW)

        for child in self.summary_frame.winfo_children():
            child.grid_configure(sticky=EW)

    def get_all(self) -> StatsCollection:
        return self.stats

    def get_selection(self) -> StatsCollection:
        return self.selection

    def set_stats(self, stats: StatsCollection):
        self.stats = stats
        self.summary_frame_all.set_stats(stats)
        self.filter_frame.set_countries(*stats.unique_countries)
        self.set_selection(stats)

    def set_selection(self, stats: StatsCollection):
        self.selection = stats
        self.summary_frame_selection.set_stats(stats)
        self.filter_frame.set_tournaments(*stats.unique_tournaments)
