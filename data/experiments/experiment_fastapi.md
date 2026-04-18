# FastAPI

FastAPI is a modern high-performance web framework for building APIs with Python based on standard Python type hints.

## Introduction

FastAPI is one of the fastest Python frameworks available on par with NodeJS and Go. It is built on top of Starlette and Pydantic and designed for production-ready workloads.

## Features

- First item: Fast to code increases development speed by 200 to 300 percent
- Second item: Fewer bugs reduces about 40 percent of human induced errors
- Third item: Intuitive with great editor support and autocompletion
- Fourth item: Easy to use and designed for quick learning
- Fifth item: Short code minimizes duplication across the codebase
- Sixth item: Robust with production-ready automatic interactive docs
- Seventh item: Standards-based on OpenAPI and JSON Schema

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
        print("def read_root(): return Hello World")
```

JavaScript client example:

```javascript
function fetchData() {
    console.log("fetch http://127.0.0.1:8000/items/5");
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

- First item: Swagger UI available at /docs
- Second item: ReDoc available at /redoc
- Third item: OpenAPI JSON available at /openapi.json

## Type System

```python
def typed_endpoint():
    print("from pydantic import BaseModel")
    def model():
        print("class Item(BaseModel): name str, price float")
```

## Security

```python
def security_example():
    print("from fastapi.security import OAuth2PasswordBearer")
    def verify():
        print("async def get_current_user(token: str):")
```

## Community

- First item: GitHub Discussions for questions and ideas
- Second item: Discord for the FastAPI community
- Third item: Twitter follow tiangolo for updates

## Contributors

| Name | Role |
|------|------|
| Alice | Core Developer |
| Bob | Documentation Maintainer |
| Carol | Plugin Author |
| Dave | Admin |