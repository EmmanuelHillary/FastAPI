
def add_func(num1:int, num2:int):
    return num1 + num2

def subtract_func(num1:int, num2:int):
    return num1 - num2

class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, default_balance=0):
        self.default_balance = default_balance
    
    def deposit(self, amount):
        self.default_balance += amount

    def withdraw(self, amount):
        if amount > self.default_balance:
            raise InsufficientFunds("Insufficient Funds")
        self.default_balance -= amount
    
    def interest(self):
        return self.default_balance * 1.1