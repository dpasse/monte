
### Decorator Pattern

- allows behavior to be added to an individual object, dynamically, without affecting the behavior of other objects from the same class.
- nest objects within each other... russian dolls.

```python
class Item():
    pass

class ItemDecorator(Item):
    def __init__(self, item: Item) -> None:
        pass

    pass
```