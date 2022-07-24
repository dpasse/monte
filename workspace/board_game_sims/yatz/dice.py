from typing import List, Optional, TypeVar, Dict
import random


class Die():
    def __init__(self, state: int = 0, sides: int = 6, random_state: Optional[int] = None) -> None:
        if random_state:
            random.seed(random_state)

        self._sides = sides
        self._state = state

    @property
    def state(self) -> int:
        return self._state

    def roll(self) -> None:
        self._state = random.randint(1, self._sides)

class DieFactory():
    def __init__(self, sides: int = 6) -> None:
        self._sides = sides

    def create(self) -> Die:
        return Die(state=0, sides=self._sides)

TDice = TypeVar('TDice', bound='Dice')

class Dice():
    def __init__(self, dice: List[Die]) -> None:
        self._dice = { i: die for i, die in enumerate(dice) }

    def retoss(self, flip: List[int]) -> TDice:
        for die in (die for i, die in self._dice.items() if i in flip):
            die.roll()

        return self

    def roll(self, flip: List[int]) -> TDice:
        if len(flip) > 0:
            return self.retoss(flip)

        for die in (die for die in self._dice.values()):
            die.roll()

        return self

    @property
    def state(self) -> Dict[int, int]:
        return {
            i: die.state
            for i, die
            in self._dice.items()
        }

    @property
    def tolist(self) -> List[int]:
        return [
            die.state
            for die
            in self._dice.values()
        ]

    def __len__(self) -> int:
        return len(self._dice.keys())

class DiceFactory():
    def __init__(self, die_factory = DieFactory()) -> None:
        self._die_factory = die_factory

    def create(self, n_die: int) -> Dice:
        return Dice([
            self._die_factory.create()
            for _
            in range(n_die)
        ])
