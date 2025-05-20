from abc import ABC, abstractmethod  # Abstract Base Class

# Abstract class
class Account(ABC):

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_balance(self):
        pass


# Base bank account class
class BankAccount(Account):
    def __init__(self, name, balance=0):
        self._name = name
        self._balance = balance  # Changed to protected for subclass access

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return f"{amount} deposited"
        return "Deposit amount must be positive"

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return f"{amount} withdrawn"
        return "Withdrawal amount must be positive and less than or equal to the balance"

    def get_balance(self):
        return f"Current balance: {self._balance}"

    def get_name(self):
        return self._name


# Personal account class with overdraft support
class PersonalAccount(BankAccount):
    def __init__(self, name, balance=0, overdraft_limit=500):
        super().__init__(name, balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self._balance - amount) >= -self._overdraft_limit:
            self._balance -= amount
            return f"Premium withdrawn: {amount} (Overdraft allowed)"
        return "Overdraft limit exceeded or amount is invalid"
