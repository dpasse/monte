from abc import ABC, abstractmethod
from typing import List, Dict

from .dice import Dice

## rules: https://en.wikipedia.org/wiki/Yatzy


class Scorer(ABC):
    @abstractmethod
    def score(self, dice: Dice) -> dict:
        pass

    @staticmethod
    def collapse(dice, taken=[]) -> Dict[int, int]:
        container = {}
        for i, v in dice.state.items():
            if i in taken:
                continue

            if not v in container:
                container[v] = 0

            container[v] += 1

        return container

    @staticmethod
    def is_response_valid(response) -> bool:
        return 'score' in response

class Kind(Scorer):
    def __init__(self, k: int = 2) -> None:
        self._k = k

    def score(self, dice: Dice, taken: List[int] = []) -> dict:
        items = sorted([i for i, c in Scorer.collapse(dice, taken).items() if c >= self._k], reverse=True)
        if len(items) == 0:
            return {}

        highest_value = items[0]
        state = { s: v for s, v in dice.state.items() if v == highest_value }

        count = 0
        response = { 'score': 0, 'contrib': [] }
        for i, value in state.items():
            response['score'] += value
            response['contrib'] += [i]
            count += 1

            if count == self._k:
                break

        return response

class Yatzy(Kind):
    def __init__(self) -> None:
        super().__init__(k=5)

    def score(self, dice: Dice) -> dict:
        response = super().score(dice)
        if not Scorer.is_response_valid(response):
            return {}

        return { 'score': 50, 'contrib': response['contrib'] }

class TwoPair(Scorer):
    def score(self, dice: Dice) -> dict:
        one = Kind(k=2).score(dice)
        if not Scorer.is_response_valid(one):
            return {}

        two = Kind(k=2).score(dice, taken=one['contrib'])
        if not Scorer.is_response_valid(two):
            return {}

        return {
            'score': one['score'] + two['score'],
            'contrib': one['contrib'] + two['contrib'],
        }

class SumByNumber(Scorer):
    def __init__(self, n: int) -> None:
        self._n = n

    def score(self, dice: Dice) -> dict:
        if not self._n in dice.tolist:
            return {}

        state = { i: state for i, state in dice.state.items() if state == self._n }
        return { 'score': sum(state.values()), 'contrib': list(state.keys()) }

class Chance(Scorer):
    def score(self, dice: Dice) -> dict:
        state = dice.state
        return { 'score': sum(state.values()), 'contrib': list(state.keys()) }

class Straight(Scorer):
    def __init__(self, template: List[int]) -> None:
        self._template = template

    def score(self, dice: Dice) -> dict:
        if self._template != sorted(dice.tolist):
            return {}

        state = dice.state
        return { 'score': sum(state.values()), 'contrib': list(state.keys()) }

class FullHouse(Scorer):
    def score(self, dice: Dice) -> dict:
        one = Kind(k=2).score(dice)
        if not Scorer.is_response_valid(one):
            return {}

        two = Kind(k=3).score(dice, taken=one['contrib'])
        if not Scorer.is_response_valid(two):
            return {}

        return {
            'score': one['score'] + two['score'],
            'contrib': one['contrib'] + two['contrib'],
        }
