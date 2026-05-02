# Understanding JavaScript Closures

## Introduction to Closures
Closures are a fundamental concept in JavaScript that allow functions to access variables from an enclosing scope even after that scope has finished execution.

### Why Use Closures?
Closures enable powerful patterns like data encapsulation, function factories, and maintaining state in asynchronous programming.

## Team Members and Roles

| Name  | Role          |
|-------|---------------|
| Alice | Frontend Dev  |
| Bob   | Backend Dev   |
| Carol | UX Designer   |
| Dave  | QA Engineer   |

### Key Concepts to Remember
- First item: Closures capture lexical scope
- Second item: Functions can remember the environment
- Third item: Useful for private variables
- Fourth item: Helps in callback functions
- Fifth item: Enables module pattern
- Sixth item: Common in event handlers

## Example Code Snippets

```python
def greet(name):
    print(f"Hello, {name}!")

greet("World")
```