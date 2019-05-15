from bets.model.stats.ratio_stats import RatioStats, OUTCOMES


class OutcomeStats(RatioStats):
    KEYS = RatioStats.KEYS + ["outcome", "ratio", "rank"]

    outcome: str
    ratio: float
    rank: str

    def __init__(self, ratio_1, ratio_X, ratio_2, outcome):
        super().__init__(ratio_1, ratio_X, ratio_2)

        if outcome not in OUTCOMES:
            raise ValueError(outcome)

        self.outcome = outcome
        self.ratio = self[f"ratio_{outcome}"]
        self.rank = self[f"rank_{outcome}"]
