# Understanding JavaScript Closures

## Introduction to Closures

Closures are a fundamental concept in JavaScript that allow functions to retain access to their lexical scope even when executed outside that scope.

### Why Use Closures?

Closures enable powerful patterns such as data privacy, function factories, and maintaining state in asynchronous code.

## Team Members and Their Roles

| Name  | Role           |
|-------|----------------|
| Alice | Developer      |
| Bob   | Designer       |
| Carol | Product Owner  |
| Dave  | Tester         |
| Admin | Project Admin  |

## Key Concepts in Closures

- First item: Functions remember the environment where they were created.
- Second item: Inner functions have access to outer function variables.
- Third item: Closures can be used to emulate private variables.
- Fourth item: They help in creating function factories.
- Fifth item: Useful in asynchronous programming for maintaining state.
- Sixth item: Can sometimes lead to memory leaks if not handled properly.

```python
def greet(name):
    print(f"Hello, {name}!")

greet("World")
```

```javascript
console.log("This is a closure example.");
```