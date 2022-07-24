from typing import List, Dict
from .strategy import PickStrategy, RollStrategies


class Player():
    def __init__(self, name: str, roll_strategies: RollStrategies, pick_strategy: PickStrategy) -> None:
        self._name = name
        self._roll_strategies = roll_strategies
        self._pick_strategy = pick_strategy

    @property
    def name(self) -> str:
        return self._name

    @property
    def roll_strategies(self) -> RollStrategies:
        return self._roll_strategies

    @property
    def pick_strategy(self) -> PickStrategy:
        return self._pick_strategy

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self._name}'

class PlayerTracker():
    def __init__(self, players: List[Player]) -> None:
        self._round = 0
        self._players = {
            i: player for i, player in enumerate(players)
        }

    @property
    def round(self) -> int:
        return self._round

    @property
    def players(self) -> Dict[int, Player]:
        return self._players

    def go_to_next_round(self) -> int:
        self._round += 1

        return self._round

    def reset(self) -> None:
        self._round = 0

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        message = 'Summary:'
        message += '\n'
        message += f' * Round #{self._round}'
        message += '\n'
        message += '\n'.join([ f'   * {player}' for player in self._players.values()])

        return message
