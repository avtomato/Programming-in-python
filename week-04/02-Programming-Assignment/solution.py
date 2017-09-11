class Value:

    def __init__(self, amount=None):
        self.amount = amount

    def __get__(self, instance, owner):
        return self.amount

    def __set__(self, instance, value):
        self.amount = value - value * instance.comission


class Account:
    amount = Value()

    def __init__(self, comission):
        self.comission = comission
