# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs
with Python based on standard Python type hints.

## Introduction

FastAPI is one of the fastest Python frameworks available, on par with NodeJS and Go.
It was designed to be easy to use, while also being production-ready and capable of
handling high-performance workloads.

## Features

- First item: Fast to code — increase development speed by 200% to 300%
- Second item: Fewer bugs — reduce about 40% of human induced errors
- Third item: Intuitive — great editor support with autocompletion everywhere
- Fourth item: Easy — designed to be easy to use and learn
- Fifth item: Short — minimizes code duplication
- Sixth item: Robust — get production-ready code with automatic interactive docs
- Seventh item: Standards-based — based on OpenAPI and JSON Schema

## Usage

Install FastAPI:

```python
def install():
    print("pip install fastapi")
    print("pip install uvicorn[standard]")
```

Create your first API:

```python
def create_api():
    print("from fastapi import FastAPI")
    print("app = FastAPI()")
    def add_route():
        print("@app.get('/')")
        print("def read_root(): return {'Hello': 'World'}")
```

JavaScript client example:

```javascript
function fetchData() {
    console.log("fetch('http://127.0.0.1:8000/items/5')");
    console.log(".then(response => response.json())");
}
```

## Performance Benchmarks

| Name | Role |
|------|------|
| Alice | Performance Engineer |
| Bob | Benchmark Analyst |
| Carol | Admin |

## Sponsors Table

| Name | Role |
|------|------|
| Alice | Gold Sponsor |
| Bob | Silver Sponsor |
| Carol | Individual Contributor |
| Dave | Admin |

## Interactive Documentation

- First item: Swagger UI — available at /docs for interactive exploration
- Second item: ReDoc — available at /redoc for alternative documentation
- Third item: OpenAPI JSON — available at /openapi.json for schema

## Type System

```python
def typed_endpoint():
    print("from pydantic import BaseModel")
    def model():
        print("class Item(BaseModel):")
        print("    name: str")
        print("    price: float")
```

## Security

```python
def security_example():
    print("from fastapi.security import OAuth2PasswordBearer")
    def verify():
        print("async def get_current_user(token: str):")
        print("    print('Verifying token...')")
```

## Community

- First item: GitHub Discussions — ask questions and share ideas
- Second item: Discord — join the FastAPI community
- Third item: Twitter — follow @tiangolo for updates

## Contributors

| Name | Role |
|------|------|
| Alice | Core Developer |
| Bob | Documentation Maintainer |
| Carol | Plugin Author |
| Dave | Admin |