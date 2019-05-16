import json
from pathlib import Path
from typing import List, Union, Iterable, Dict

from bets.model.stats.abstract_stats import AbstractStats
from bets.model.stats.outcome_stats import OutcomeStats
from bets.model.stats.ratio_stats import RatioStats
from bets.model.stats.score_stats import ScoreStats


class StatsCollection(AbstractStats):
    KEYS = ["size",
            "n_1", "n_X", "n_2",
            "perc_1", "perc_X", "perc_2",
            "n_min", "n_med", "n_max",
            "perc_min", "perc_med", "perc_max",
            "ratio_total", "ratio_mean", "ratio_geometric_mean",
            "ratio_perc_total_mean", "ratio_perc_total_mean_geometric",
            "outcomes", "ranks", "ratios"]

    def __init__(self, matches: Iterable[Union[OutcomeStats, ScoreStats]] = None):
        self._matches: List[Union[OutcomeStats, ScoreStats]] = list(matches) if matches else []

    def __iter__(self):
        return self._matches.__iter__()

    def __len__(self):
        return len(self._matches)

    @classmethod
    def read_json(cls, file=None) -> "MatchesList":
        if file is None:
            file = r"D:\PROJECT_HOME\f_stats\src\f_stats\storage\matches.json"
        path = Path(file)
        matches = []
        with path.open("rb") as fp:
            matches_dicts = json.loads(fp.read().decode("utf-8"))
            for m in matches_dicts:
                matches.append(ScoreStats(m["ratio_1"],
                                          m["ratio_x"],
                                          m["ratio_2"],
                                          m["host_score"],
                                          m["guest_score"],
                                          m["host_team"],
                                          m["guest_team"],
                                          m["date"],
                                          m["country"],
                                          m["tournament"]))
        return StatsCollection(matches)

    @property
    def matches_dicts(self) -> List[Dict[str, Union[int, float, str]]]:
        return [m.as_dict() for m in self]

    @property
    def size(self) -> int:
        return len(self._matches)

    @property
    def n_1(self) -> int:
        return len([m for m in self if m.outcome == "1"])

    @property
    def n_X(self) -> int:
        return len([m for m in self if m.outcome == "X"])

    @property
    def n_2(self) -> int:
        return len([m for m in self if m.outcome == "2"])

    @property
    def perc_1(self) -> float:
        return round(((self.n_1 / len(self)) * 100), 2)

    @property
    def perc_X(self) -> float:
        return round(((self.n_X / len(self)) * 100), 2)

    @property
    def perc_2(self) -> float:
        return round(((self.n_2 / len(self)) * 100), 2)

    @property
    def n_min(self) -> int:
        return len([m for m in self._matches if "min" in m.rank])

    @property
    def n_med(self) -> int:
        return len([m for m in self._matches if "med" in m.rank])

    @property
    def n_max(self) -> int:
        return len([m for m in self._matches if "max" in m.rank])

    @property
    def perc_min(self) -> float:
        return round(((self.n_min / len(self)) * 100), 2)

    @property
    def perc_med(self) -> float:
        return round(((self.n_med / len(self)) * 100), 2)

    @property
    def perc_max(self) -> float:
        return round(((self.n_max / len(self)) * 100), 2)

    @property
    def ratio_total(self) -> float:
        total = 1
        for m in self:
            total *= m.ratio

        return round(total, 2)

    @property
    def ratio_mean(self) -> float:
        mean = 1
        for m in self:
            mean *= m.ratio_mean
        return round(mean, 2)

    @property
    def ratio_geometric_mean(self) -> float:
        mean_geometric = 1
        for m in self:
            mean_geometric *= m.ratio_geometric_mean
        return round(mean_geometric, 2)

    @property
    def ratio_perc_total_mean(self) -> float:
        return round(((self.ratio_total / self.ratio_mean) * 100), 2)

    @property
    def ratio_perc_total_mean_geometric(self) -> float:
        return round(((self.ratio_total / self.ratio_geometric_mean) * 100), 2)

    @property
    def dates(self) -> List[str]:
        return [m.date for m in self if m.date]

    @property
    def outcomes(self) -> str:
        return " ".join([m.outcome for m in self])

    @property
    def ranks(self) -> str:
        return " ".join([m.rank for m in self])

    @property
    def ratios(self) -> str:
        return " ".join([f"{m.ratio:.02f}" for m in self])

    def append(self, stats: Union[OutcomeStats, ScoreStats]):
        if not isinstance(stats, (OutcomeStats, ScoreStats)):
            raise TypeError(type(stats))

        self._matches.append(stats)

    def with_country(self, country: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.country == country)

    def with_date(self, date: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.date == date)

    def with_tournament(self, tournament: str) -> "StatsCollection":
        return StatsCollection(m for m in self if m.tournament == tournament)

    def with_similar_ratios_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_ratios_to(sample))

    def with_similar_outcome_ratio_percentages_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_outcome_ratio_percentages_to(sample))

    def with_similar_rank_ratio_percentages_to(self, sample: RatioStats) -> "StatsCollection":
        return StatsCollection(m for m in self if m.is_having_similar_rank_ratio_percentages_to(sample))

    def stats_by_date(self) -> Dict[str, "StatsCollection"]:
        return {date: self.with_date(date) for date in self.dates}

    def summary_by_date(self) -> List[Dict[str, Union[int, float, str]]]:
        stats_by_date = [dict(date=date, **stats.as_dict()) for date, stats in self.stats_by_date().items()]
        stats_by_date.sort(key=(lambda s: s["size"]))
        return stats_by_date
