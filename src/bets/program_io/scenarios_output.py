import logging
from pathlib import Path
from typing import List

from pandas import DataFrame
from tabulate import tabulate

_log = logging.getLogger(__name__)


class ScenariosOutput:
    VALID_FORMATS = {"csv", "plain", "fancy_grid"}

    def __init__(self, scenarios: List[dict], out_dest, out_fmt):
        if out_fmt not in self.VALID_FORMATS:
            raise ValueError("Unsupported format [{}]".format(out_fmt), self.VALID_FORMATS)
        self.scenarios = scenarios
        self.columns = list(self.scenarios[0].keys())
        self.out_dest = out_dest
        self.out_fmt = out_fmt

    def _fmt_to_table(self) -> str:
        return tabulate(self.scenarios,
                        headers="keys",
                        floatfmt=".2f",
                        stralign="center",
                        tablefmt=self.out_fmt)

    def _fmt_to_csv(self) -> str:
        return DataFrame(self.scenarios,
                         columns=self.columns).to_csv(columns=self.columns, float_format="%.2f")

    def write(self):
        text = self._fmt_to_csv() if (self.out_fmt == "csv") else self._fmt_to_table()

        if self.out_dest == "console":
            print(text)
            return

        with Path(self.out_dest).open("wb") as fp:
            fp.write(text.encode("utf-8"))

    @classmethod
    def write_scenarios(cls, scenarios, out_dest, out_fmt):
        ScenariosOutput(scenarios, out_dest, out_fmt).write()
