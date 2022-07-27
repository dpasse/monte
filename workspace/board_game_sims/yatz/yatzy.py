from typing import List, Tuple

from .score_card import YatzyScoreCard
from .player import Player
from .dice import DiceFactory


class Yatzy():
    def __init__(self, players: List[Player], debug=True) -> None:
        self._dice = DiceFactory().create(5)
        self._score_card = YatzyScoreCard()

        self._round = 0
        self._players = {
            i: player for i, player in enumerate(players)
        }

        self._debug = debug

    def print(self, message: str = '') -> None:
        if self._debug:
            print(message)

    def play(self) -> List[Tuple[str, int]]:
        self.reset()

        self.print(self._score_card.is_complete())

        while not self._score_card.is_complete():
            self.play_round()

        self.print(self._score_card)

        return sorted(
            [
                (player_name, score)
                for player_name, score
                in self._score_card.calculate_score().items()
            ],
            key=lambda a: a[1],
            reverse=True
        )

    def play_round(self):
        self._round += 1

        self.print(f'Round {self._round}:')
        for player in self._players.values():
            self.play_turn(player)

        return self

    def play_turn(self, player):
        self.print(f'    * {player}')

        die_to_retoss = []
        for round in ['1st', '2nd']:
            self._dice.roll(die_to_retoss)
            self.print(f'    * {round} - {self._dice.tolist}')

            die_to_retoss = player.roll_strategies.get(round).move(
                self._dice,
                self._score_card.get_all_scores_by_dice(self._dice),
            )['toss']

            if len(die_to_retoss) == 0:
                break

        if len(die_to_retoss) != 0:
            round = '3rd'
            self._dice.roll(die_to_retoss)
            self.print(f'    * {round} - {self._dice.tolist}')

        score = 0
        picked = player.pick_strategy.pick(
            self._score_card.get_all_scores_by_dice(self._dice)
        )

        if picked != '':
            score = self._score_card.mark(picked, player.name, self._dice)

        self.print(f'    * Picked - {picked} for {score} point(s)')
        self.print()

    def reset(self):
        self._score_card.reset()
