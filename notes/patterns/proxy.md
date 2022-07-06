
### Proxy

- access control. middleman. gets between you and the real subject and controls access to it.
- all about wrapping one object. slightly different from the decorator pattern.

``` python

from abc import ABC, abstractmethod


class Subject(ABC):

    @abstractmethod
    def request(self) -> None:
        pass


class RealSubject(Subject):

    def request(self) -> None:
        print("RealSubject: Handling request.")


class PermissionProxy(Subject):

    def __init__(self, real_subject: RealSubject) -> None:
        self._real_subject = real_subject

    def request(self) -> None:
        if self.check_access():
            self._real_subject.request()

    def check_access(self) -> bool:
        pass

```

