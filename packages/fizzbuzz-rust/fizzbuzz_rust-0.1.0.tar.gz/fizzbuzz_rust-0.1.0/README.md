# Fizzbuzz

A rusty implementation for Python
It uses PyO3 and `maturin` for building.

To install it, you should clone the repository, create a virtualenv and use
```
maturin develop
```
This will install fizzbuzz library.

The library has one function `fizz_buzz`.
```
fizzbuzz.fizz_buzz(n)
```
It takes an argument and returns a list of strings.
