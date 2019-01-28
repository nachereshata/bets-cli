import logging
from pathlib import Path
from typing import List

from tabulate import tabulate
from pandas import DataFrame

from bets.model.match import Match

_log = logging.getLogger(__name__)


class MatchesOutput:
    VALID_FORMATS = {"csv", "plain", "fancy_grid"}

    def __init__(self, matches: List[Match], out_dest="console", fmt="plain"):
        if fmt not in self.VALID_FORMATS:
            raise ValueError("Unsupported format [{}]".format(fmt), self.VALID_FORMATS)

        self.matches = matches
        self.out_dest = out_dest
        self.fmt = fmt

    def _fmt_to_csv(self) -> str:
        _log.info("formatting list of matches to CSV...")
        return DataFrame(
            data=(m.tuple for m in self.matches), columns=Match.COLUMNS
        ).to_csv(
            float_format="%.2f", columns=Match.COLUMNS
        )

    def _fmt_to_table(self) -> str:
        return tabulate((m.tuple for m in self.matches),
                        headers=Match.COLUMNS,
                        floatfmt=".2f",
                        stralign="center",
                        disable_numparse=[4, 5, 6, -3, -2, -1],
                        tablefmt=self.fmt)

    def get_formatted_text(self):
        return self._fmt_to_csv() if (self.fmt == "csv") else self._fmt_to_table()

    def write(self):
        text = self.get_formatted_text()

        if self.out_dest == "console":
            print(text)
            return

        with Path(self.out_dest).open("wb") as fp:
            fp.write(text.encode("utf-8"))

    @classmethod
    def write_matches(cls, matches: List[Match], out_dest="console", fmt="plain"):
        cls(matches, out_dest, fmt).write()
