"""
Drawback of observer design pattern - Its prone to memory leaks as many observers can be registered
with references, but they may become stale and redundant. Hence, never garbage collected.
Solution - By keeping WeakRefHashMap or weak references to observers, memory leak can be avoided.

Application: Used mainly in distributed event handling systems, eg - search query.
"""


class Observable(object):
    """
    The example implementation shown below is "tightly coupled" with both observer and observable
    needing to know about each other. It can be decoupled by using a msg queue like kafka, or any
    publish-subscribe msg q.
    """
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)


class Observer(object):
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)


subject = Observable()
observer = Observer(subject)
subject.notify_observers('test')