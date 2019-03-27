import tkinter as tk
import tkinter.filedialog as file_dialog
import tkinter.messagebox as message_box
import tkinter.ttk as ttk

from bets.model.scenarios import Scenarios
from bets.ui.scenarios_tab.filter_frames import TotalOccurrencesFilterFrame, SequentialOccurrencesFilterFrame
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

    def create_widgets(self):
        self._create_filters()
        self._create_actions()

    def _create_filters(self):
        filter_frame = tk.LabelFrame(self)
        filter_frame.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X)
        self._create_range_filter(filter_frame)
        self._create_occurrence_filter(filter_frame)

        for child in filter_frame.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=tk.W)

    def _create_actions(self):
        actions_frame = tk.LabelFrame(self)
        actions_frame.pack(side=tk.RIGHT, anchor=tk.W, fill=tk.BOTH)
        save_frame = tk.LabelFrame(actions_frame, text=" Save as ")
        save_frame.grid(column=0, row=0, padx=4, pady=2)
        ttk.Button(save_frame, text="CSV", command=self.export_as_csv).grid(column=0, row=0, padx=2, pady=2)
        ttk.Button(save_frame, text="TXT", command=self.export_as_grid).grid(column=1, row=0, padx=2, pady=2)
        ttk.Button(actions_frame, text="Delete", command=self.destroy).grid(column=2, row=0, sticky="SE", padx=4,
                                                                            pady=2)

    def _create_range_filter(self, filter_frame):
        range_filter_frame = TotalOccurrencesFilterFrame(filter_frame, max_value=len(self.scenarios.matches))
        range_filter_frame.grid(column=0, row=0)

        def _apply_filter():
            target, count_from, count_to = range_filter_frame.get_values()
            self.parent.add_scenarios_row(title=f"Range({target})[{count_from} - {count_to}]",
                                          scenarios=self.scenarios.filter_by_total_occurrences(target,
                                                                                               count_from,
                                                                                               count_to))

        range_filter_frame.apply_button["command"] = _apply_filter

    def _create_occurrence_filter(self, filter_frame):
        occurrence_filter_frame = SequentialOccurrencesFilterFrame(filter_frame, max_value=len(self.scenarios.matches))
        occurrence_filter_frame.grid(column=1, row=0)

        def _apply_filter():
            target, count = occurrence_filter_frame.get_values()
            self.parent.add_scenarios_row(title=f"Seq({target})[up to {count} in a row]",
                                          scenarios=self.scenarios.filter_by_sequential_occurrences(target, count))

        occurrence_filter_frame.apply_button["command"] = _apply_filter

    def _export_scenarios(self, file_ext):
        target_file = file_dialog.asksaveasfilename(filetypes=(f"Text .{file_ext}",))

        if not target_file:
            message_box.showinfo("", "Export canceled")
            return

        if not target_file.lower().endswith(file_ext):
            target_file = f"{target_file}.{file_ext}"

        if message_box.askyesno("Confirm export", f"Target file:\n{target_file}"):
            self.scenarios.write_to_file(target_file)
            message_box.showinfo("Export success!", f"File location:\n{target_file}")
        else:
            message_box.showinfo("", "Export canceled")

    def export_as_grid(self):
        self._export_scenarios("txt")

    def export_as_csv(self):
        self._export_scenarios("csv")
