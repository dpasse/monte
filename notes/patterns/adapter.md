
### Adapter "Wrapper" Pattern


- allows an interface of an existing class to be used as another interface.
- make existing classes work with others without modifying their source code.

```
  [client] -> [item]
           -> [adapter] -> [incompatible type]
```

```python

from abc import ABCMeta, abstractmethod

class Item(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

class HatToItemAdapter(Item):

    def __init__(self, hat: Hat) -> None:
        self._hat = hat

    @property
    def name(self) -> str:
        return self._hat.fullname

```