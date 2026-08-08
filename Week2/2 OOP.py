"""
2 OOP.py

Classes, taught clean -- no Agent in sight. Class 1 only ever showed
you a class wearing an "Agent" costume; this file is the bare pattern,
on its own, so it actually generalizes instead of feeling like
something you can only use for AI.

Run with: uv run "2 OOP.py"
"""

# --- A class is a blueprint. An instance is one specific thing built from it. ---

class BankAccount:
    """A blueprint for a bank account -- nothing to do with AI."""

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner       # every instance gets its OWN owner
        self.balance = balance   # and its OWN balance -- this is the account's STATE
        self.history = []        # a list, just like File 1's data structures

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.history.append(f"Deposited {amount}")

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            print(f"Insufficient funds: tried to withdraw {amount}, balance is {self.balance}")
            return
        self.balance -= amount
        self.history.append(f"Withdrew {amount}")

    def show_history(self) -> None:
        for entry in self.history:
            print(f"  - {entry}")

# Java-style equivalent comments:
# class BankAccount {
#     String owner;
#     double balance;
#     List<String> history;
#
#     BankAccount(String owner, double balance) {
#         this.owner = owner;
#         this.balance = balance;
#         this.history = new ArrayList<>();
#     }
#
#     void deposit(double amount) {
#         this.balance += amount;
#         this.history.add("Deposited " + amount);
#     }
#
#     void withdraw(double amount) {
#         if (amount > this.balance) {
#             System.out.println("Insufficient funds: tried to withdraw " + amount + ", balance is " + this.balance);
#             return;
#         }
#         this.balance -= amount;
#         this.history.add("Withdrew " + amount);
#     }
#
#     void showHistory() {
#         for (String entry : this.history) {
#             System.out.println("  - " + entry);
#         }
#     }
# }


# Build TWO separate accounts from the same blueprint -- each has its own state.
account_1 = BankAccount(owner="pranay", balance=1000)
account_2 = BankAccount(owner="pranay", balance=500)

account_1.deposit(200)
account_1.withdraw(50)
account_2.withdraw(1000)   # deliberately too much -- shows the guard clause working

print(f"{account_1.owner}'s balance: {account_1.balance}")
account_1.show_history()

print(f"\n{account_2.owner}'s balance: {account_2.balance}")
account_2.show_history()


# --- @dataclass: the same idea, with less typing ---
# Normally you write __init__ by hand, like BankAccount above. `@dataclass`
# writes that boilerplate FOR you, just from type-hinted attributes.

from dataclasses import dataclass, field


@dataclass
class Book:
    """The same blueprint concept, written the shorter way."""
    title: str
    author: str
    pages_read: int = 0
    # tags = []
    tags: list = field(default_factory=list)   # mutable defaults need field(default_factory=...)

    def read(self, pages: int) -> None:
        self.pages_read += pages

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

# Java-style equivalent comments:
# class Book {
#     String title;
#     String author;
#     int pagesRead;
#     List<String> tags;
#
#     Book(String title, String author) {
#         this.title = title;
#         this.author = author;
#         this.pagesRead = 0;
#         this.tags = new ArrayList<>();
#     }
#
#     void read(int pages) {
#         this.pagesRead += pages;
#     }
#
#     void addTag(String tag) {
#         this.tags.add(tag);
#     }
# }


my_book = Book(title="Atomic Habits", author="James Clear")
my_book.read(40)
my_book.add_tag("self-help")
print(f"\n{my_book}")


if __name__ == "__main__":
    print("\nOOP done. Two completely ordinary classes -- a bank account and a book.")
    print("Hold onto this exact pattern: file 11 today reuses it, unchanged, to define an Agent.")



# What does @dataclass do? Example
# A dataclass automatically creates common methods like __init__ for you.
# It is useful when you want a simple class to store data.

from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int
    city: str = "Unknown"


p1 = Person("Alice", 25)
print(p1)
print(p1.name)
print(p1.age)


# class Person:
#     def __init__(self, name, age, city="Unknown"):
#         self.name = name
#         self.age = age
#         self.city = city


# p1 = Person("Alice", 25)
# print(p1)
# print(p1.name)
# print(p1.age)


# java 

# public class Person {
#     private String name;
#     private int age;
#     private String city;

#     public Person(String name, int age) {
#         this(name, age, "Unknown");
#     }

#     public Person(String name, int age, String city) {
#         this.name = name;
#         this.age = age;
#         this.city = city;
#     }

#     public static void main(String[] args) {
#         Person p1 = new Person("Alice", 25);
#         System.out.println(p1);
#         System.out.println(p1.name);
#         System.out.println(p1.age);
#     }
# }


