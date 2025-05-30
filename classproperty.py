class classproperty:
    """
    A decorator that converts an instance method in a class into a class
    property.
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, _instance, owner):
        return self.func(owner)
