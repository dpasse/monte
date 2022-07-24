from abc import ABC
from typing import Dict, Tuple
from .scorer import SumByNumber, Kind, TwoPair, Chance, Yatzy, Straight, FullHouse, Scorer
from .player import Score
from .dice import Dice


class DiceScoreCard(ABC):
    def __init__(self, rules: Tuple[str, Scorer]) -> None:
        self._rules = {
            name: { 'rule': rule }
            for name, rule
            in rules
        }

    def mark(self, rule_key: str, user: str, dice: Dice) -> int:
        if not rule_key in self._rules:
            raise Exception('key not found.')

        score = self._rules[rule_key]['rule'].score(dice)
        if not Scorer.is_response_valid(score):
            raise Exception('dice / scorer combo is invalid')

        self._rules[rule_key]['u'] = user
        self._rules[rule_key]['score'] = score['score']
        return self._rules[rule_key]['score']

    def calculate_score(self):
        card = {}
        for _, item in self._rules.items():
            if not 'u' in item:
                continue

            player_name = item['u']
            if not player_name in card:
                card[player_name] = 0

            card[player_name] += item['score']

        for name, score in self.get_bonus().items():
            if not name in card:
                card[name] = 0

            card[name] += score

        return card

    def get_bonus(self) -> Dict[str, int]:
        return {}

    def get_all_scores_by_dice(self, dice: Dice, skip=[]) -> Dict[str, Score]:
        scores = {}
        for key, item in self._rules.items():
            if 'u' in item:
                continue

            if key in skip:
                continue

            response = item['rule'].score(dice)
            if Scorer.is_response_valid(response):
                scores[key] = response

        return scores

    def is_complete(self) -> bool:
        return len([
            k
            for k, item
            in self._rules.items()
            if not 'u' in item
        ]) == 0

    def reset(self) -> None:
        for item in self._rules.values():
            if 'u' in item:
                del item['u']

            if 'score' in item:
                del item['score']

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        message = 'Score Card:' + '\n'
        for name, item in self._rules.items():
            user = item['u']
            score = item['score']

            message += f' * {name} - {user} w/ {score}'
            message += '\n'

        return message

class YatzyScoreCard(DiceScoreCard):
    def __init__(self) -> None:
        self._upper_bonus_keys = [
            'Ones',
            'Twos',
            'Threes',
            'Fours',
            'Fives',
            'Sixes'
        ]

        super().__init__([
            ## upper section
            ('Ones', SumByNumber(n=1)),
            ('Twos', SumByNumber(n=2)),
            ('Threes', SumByNumber(n=3)),
            ('Fours', SumByNumber(n=4)),
            ('Fives', SumByNumber(n=5)),
            ('Sixes', SumByNumber(n=6)),

            ## lower section
            ('One Pair', Kind(k=2)),
            ('Two Pair', TwoPair()),
            ('Three of a Kind', Kind(k=3)),
            ('Four of a Kind', Kind(k=4)),
            ('Chance', Chance()),
            ('Yatzy', Yatzy()),
            ('Small Straight', Straight([1, 2, 3, 4, 5])),
            ('Large Straight', Straight([2, 3, 4, 5, 6])),
            ('Full House', FullHouse()),
        ])

    def get_bonus(self) -> Dict[str, int]:
        players = {}
        for rule_name, item in self._rules.items():
            if rule_name in self._upper_bonus_keys and 'u' in item:
                player_name = item['u']
                if not player_name in players:
                    players[player_name] = 0

                players[player_name] += item['score']

        return {
            player_name: 50
            for player_name, score
            in players.items()
            if score >= 63
        }
