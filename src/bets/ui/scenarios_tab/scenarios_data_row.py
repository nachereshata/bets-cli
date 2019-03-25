import re
import tkinter as tk
import tkinter.filedialog as file_dialog
import tkinter.messagebox as message_box
import tkinter.ttk as ttk

from more_itertools import circular_shifts

from bets.model.matches import RANKS, OUTCOMES
from bets.model.scenarios import Scenario, Scenarios
from bets.ui.scenarios_tab.filter_frames import FromToFilterFrame, OccurrenceFilterFrame
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

    def _create_range_filter(self, filter_frame):
        range_filter_frame = FromToFilterFrame(filter_frame,
                                               text=" Range filter ",
                                               combo_values=RANKS + OUTCOMES,
                                               max_value=len(self.scenarios.matches))
        range_filter_frame.grid(column=0, row=0)

        def _apply_filter():
            target = range_filter_frame.combo_box.get()
            count_from = int(range_filter_frame.spin_from.get())
            count_to = int(range_filter_frame.spin_to.get())
            create_filter_func = outcomes_counts_filter if (target in OUTCOMES) else ranks_counts_filter
            filter_func = create_filter_func(target, count_from, count_to)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Range({target})[{count_from} - {count_to}]"
            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        range_filter_frame.apply_button["command"] = _apply_filter

    def _create_occurrence_filter(self, filter_frame):
        occurrence_filter_frame = OccurrenceFilterFrame(filter_frame,
                                                        text=" Sequential occurrences ",
                                                        combo_values=RANKS + OUTCOMES,
                                                        max_value=len(self.scenarios.matches))
        occurrence_filter_frame.grid(column=1, row=0)

        def _apply_filter():
            target = occurrence_filter_frame.combo_box.get()
            count = int(occurrence_filter_frame.spin_to.get())
            create_filter_func = outcomes_sequential_filter if (target in OUTCOMES) else ranks_sequential_filter
            filter_func = create_filter_func(target, count)
            matching_scenarios = Scenarios(self.scenarios.matches, list(filter(filter_func, self.scenarios.scenarios)))
            title = f"Seq({target})[up to {count} in a row]"

            ScenariosDataRow(self.parent, title, matching_scenarios).pack(side=tk.TOP, anchor=tk.W, fill=tk.X)

        occurrence_filter_frame.apply_button["command"] = _apply_filter

    def _create_filters(self):
        filter_frame = tk.LabelFrame(self, text=" Filters: ")
        filter_frame.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=5)
        self._create_range_filter(filter_frame)
        self._create_occurrence_filter(filter_frame)

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
