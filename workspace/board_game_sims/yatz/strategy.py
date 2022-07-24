from abc import ABC, abstractmethod
from typing import Dict
import random
from .dice import Dice


class RollStrategy(ABC):
    @abstractmethod
    def move(self, dice: Dice, available_moves: dict) -> dict:
        pass

class RollStrategies():
    def __init__(self, strategies: Dict[str, RollStrategy]) -> None:
        self._strategies = strategies

    def get(self, key) -> RollStrategy:
        if not key in self._strategies:
            raise Exception('key not found.')

        return self._strategies[key]

class PickStrategy(ABC):
    @abstractmethod
    def pick(self, available_moves: dict) -> str:
        pass

class RandomStrategy(RollStrategy, PickStrategy):
    def move(self, dice: Dice, available_moves: dict) -> dict:
        n = len(dice)
        state = dice.state
        keys = list(state.keys())

        if not len(available_moves.keys()) > 0:
            ## dont stay if no moves
            n -= 1

        keep = random.randint(0, n)
        if keep == 0:
            return {
                'toss': keys,
            }

        if keep == n:
            return {
                'toss': [],
            }

        return {
            'toss': random.sample(keys, k=n - keep),
        }

    def pick(self, available_moves: dict) -> str:
        keys = list(available_moves.keys())
        if len(keys) == 0:
            return ''

        return random.sample(keys, k=1)[0]

class AggressiveRandomStrategy(RandomStrategy):
    def move(self, dice: Dice, available_moves: dict) -> dict:
        if not len(available_moves.keys()) > 0:
            return {
                'toss': list(dice.state.keys()),
            }

        return super().move(dice, available_moves)

class PickHighestStrategy(PickStrategy):
    def pick(self, available_moves: dict) -> str:
        items = available_moves.items()
        sort = sorted(items, key=lambda a: a[1]['score'], reverse=True)

        if len(sort) > 0:
            return sort[0][0]

        return ''
