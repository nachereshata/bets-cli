import re
import tkinter as tk
import tkinter.filedialog as file_dialog
import tkinter.messagebox as message_box
import tkinter.ttk as ttk

from more_itertools import circular_shifts

from bets.model.scenarios import Scenario, Scenarios
from bets.ui.scenarios_tab.filter_frames import FromToFilterFrame
from bets.ui.table_frame import TableFrame
from bets.utils import log


def _get_from_to_values(text: str, max_value: int):
    try:
        values = tuple(int(value) for value in text.strip().split(" "))
        if len(values) == 1:
            values = (values[0], values[0])
    except ValueError:
        values = 0, max_value

    log.debug("gor from-to values:", str(values))
    return values


class ScenariosDataRow(ttk.LabelFrame):

    def __init__(self, parent, title, scenarios: Scenarios):
        self.title = f"{title} Scenarios ({len(scenarios)}) "
        super().__init__(parent, text=self.title)
        self.parent = parent
        self.scenarios = scenarios
        self.create_widgets()

    def _create_actions_frame(self):
        view_frame = ttk.LabelFrame(self, text=" Actions: ")
        view_frame.pack(side=tk.RIGHT, anchor="se", fill=tk.X, padx=10, pady=5)

        ttk.Button(view_frame, text="View", command=self.view_as_grid).grid(column=0, row=0, padx=10, pady=5)
        ttk.Button(view_frame, text="Delete", command=self.destroy).grid(column=0, row=1, padx=10, pady=5)

    def _create_outcome_counts_filter(self, filter_frame):
        outcomes_filter_frame = FromToFilterFrame(filter_frame,
                                                  text=" Outcomes counts ",
                                                  combo_values=("1", "X", "2"),
                                                  max_value=len(self.scenarios.matches))
        outcomes_filter_frame.grid(column=0, row=0)

        def _apply_filter():
            outcome = outcomes_filter_frame.combo_box.get()
            count_from = int(outcomes_filter_frame.spin_from.get())
            count_to = int(outcomes_filter_frame.spin_to.get())
            filter_func = outcomes_counts_filter(outcome, count_from, count_to)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Count({outcome})[{count_from} - {count_to}]"
            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        outcomes_filter_frame.apply_button["command"] = _apply_filter

    def _create_ranks_counts_filter(self, filter_frame):
        # outcomes filter
        tk.Label(filter_frame, text="Ranks:").grid(column=0, row=1)
        ranks_combo = ttk.Combobox(filter_frame, width=5, values=("min", "med", "max"), state="readonly")
        ranks_combo.current(0)
        ranks_combo.grid(column=1, row=1)
        tk.Label(filter_frame, text="From: ").grid(column=2, row=1)
        spin_ranks_from = tk.Spinbox(filter_frame, width=5, from_=0, to=len(self.scenarios.matches), state="readonly")
        spin_ranks_from.grid(column=3, row=1)

        tk.Label(filter_frame, text="To: ").grid(column=4, row=1)

        spin_ranks_to = tk.Spinbox(filter_frame, from_=0, width=5, to=len(self.scenarios.matches), state="readonly")
        spin_ranks_to.grid(column=5, row=1)

        def _apply_ranks_counts_filter():
            rank = ranks_combo.get()
            count_from = int(spin_ranks_from.get())
            count_to = int(spin_ranks_to.get())
            filter_func = ranks_counts_filter(rank, count_from, count_to)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Count({rank})[{count_from} - {count_to}]"
            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        tk.Button(filter_frame, text="Add", command=_apply_ranks_counts_filter).grid(column=6, row=1)

    def _create_sequential_outcomes_filter(self, filter_frame):
        tk.Label(filter_frame, text="Outcomes: ").grid(column=0, row=2)
        seq_combo = ttk.Combobox(filter_frame, width=5, values=("1", "X", "2"), state="readonly")
        seq_combo.current(0)
        seq_combo.grid(column=1, row=2)
        tk.Label(filter_frame, text="No more than: ").grid(column=2, row=2)
        spin_seq_outcomes = tk.Spinbox(filter_frame, width=5, from_=0, to=len(self.scenarios.matches), state="readonly")
        spin_seq_outcomes.grid(column=3, row=2)
        tk.Label(filter_frame, text="same outcomes in a row").grid(column=4, row=2, columnspan=2)

        def _apply_seq_outcomes_filter():
            outcome = seq_combo.get()
            count = int(spin_seq_outcomes.get())
            filter_func = outcomes_sequential_filter(outcome, count)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Seq({outcome})[up to {count}]"

            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        tk.Button(filter_frame, text="Add", command=_apply_seq_outcomes_filter).grid(column=6, row=2)

    def _create_sequential_ranks_filter(self, filter_frame):
        tk.Label(filter_frame, text="Ranks: ").grid(column=0, row=3)
        seq_combo = ttk.Combobox(filter_frame, width=5, values=("min", "med", "max"), state="readonly")
        seq_combo.current(0)
        seq_combo.grid(column=1, row=3)
        tk.Label(filter_frame, text="No more than: ").grid(column=2, row=3)
        spin_seq_ranks = tk.Spinbox(filter_frame, width=5, from_=0, to=len(self.scenarios.matches), state="readonly")
        spin_seq_ranks.grid(column=3, row=3)
        tk.Label(filter_frame, text="same ranks in a row").grid(column=4, row=3, columnspan=2)

        def _apply_seq_ranks_filter():
            rank = seq_combo.get()
            count = int(spin_seq_ranks.get())
            filter_func = ranks_sequential_filter(rank, count)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Seq({rank})[up to {count}]"

            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        tk.Button(filter_frame, text="Add", command=_apply_seq_ranks_filter).grid(column=6, row=3)

    def _create_filters(self):
        filter_frame = ttk.LabelFrame(self, text=" Filters: ")
        filter_frame.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=5)
        self._create_outcome_counts_filter(filter_frame)
        self._create_ranks_counts_filter(filter_frame)
        self._create_sequential_outcomes_filter(filter_frame)
        self._create_sequential_ranks_filter(filter_frame)
        for child in filter_frame.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=tk.W)

    def create_widgets(self):
        self._create_filters()
        self._create_actions_frame()

    def _export_scenarios(self, file_ext):
        ext = f".{file_ext}"
        target_file = file_dialog.asksaveasfilename(filetypes=(f"Text {ext}",))
        if not target_file.lower().endswith(ext):
            target_file = target_file + ext

        if message_box.askyesno("Confirm export", f"Target file:\n{target_file}"):
            self.scenarios.write_to_file(target_file)
            message_box.showinfo("Export success!", f"File location:\n{target_file}")
        else:
            message_box.showinfo("", "Export canceled")

    def view_as_grid(self):
        TableFrame(self.title, columns=self.scenarios.columns, rows=[s.values for s in self.scenarios])

    def export_as_grid(self):
        self._export_scenarios("txt")

    def export_as_csv(self):
        self._export_scenarios("csv")


def outcomes_counts_filter(outcome, min_count, max_count):
    def count_outcomes(scenario: Scenario):
        count = 0
        for o in scenario.outcomes:
            if outcome in o:
                count = count + 1
        return min_count <= count <= max_count

    return count_outcomes


def ranks_counts_filter(rank, min_count, max_count):
    def count_ranks(scenario: Scenario):
        count = 0
        for r in scenario.ranks:
            if rank in r:
                count = count + 1
        return min_count <= count <= max_count

    return count_ranks


def outcomes_sequential_filter(outcome, max_count):
    def check_scenario(scenario: Scenario):
        for shift in circular_shifts(scenario.outcomes):
            matching_parts = re.findall(f"[{outcome}]+", "".join(shift))
            if matching_parts:
                for part in matching_parts:
                    if len(part) > max_count:
                        return False
        return True

    return check_scenario


def ranks_sequential_filter(rank, max_count):
    def check_scenario(scenario: Scenario):
        for shift in circular_shifts(scenario.ranks):
            matching_parts = re.findall(f"/?((?:{rank})+)", "".join(shift))
            if matching_parts:
                for part in matching_parts:
                    if len(part) // 3 > max_count:
                        return False
        return True

    return check_scenario
