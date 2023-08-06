# Rutyva - Runtime Type Validation for Python

Rutyva is a python library that enforces static typing at runtime using the type annotations of dataclasses.

It also allows dict parsing into classes, even with nested class objects (compositions).

## How to

At the moment, the classes need to be inherited from the BaseModel class, and need to be dataclasses, to have its type annotations enforced.
