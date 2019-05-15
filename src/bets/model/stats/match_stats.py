from bets.model.stats.score_stats import ScoreStats


class MatchStats(ScoreStats):
    KEYS = ScoreStats.KEYS + ["host_team", "guest_team", "country", "tournament", "date"]
    host_team: str
    guest_team: str
    country: str
    tournament: str
    date: str

    def __init__(self, ratio_1, ratio_X, ratio_2, host_score, guest_score,
                 host_team, guest_team, country, tournament, date):
        super().__init__(ratio_1, ratio_X, ratio_2, host_score, guest_score)

        self.host_team = host_team
        self.guest_team = guest_team
        self.country = country
        self.tournament = tournament
        self.date = date

