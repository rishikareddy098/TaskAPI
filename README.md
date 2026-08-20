# Task API

A simple CRUD (Create, Read, Update, Delete) REST API built using **FastAPI and PostgreSQL**. The application is containerized using **Docker and Docker Compose**.

The API allows users to create, view, update, and delete tasks. PostgreSQL is used as the database, while Docker Compose manages both the FastAPI application and PostgreSQL database containers.

## Features

- View all tasks
- View a task by its ID
- Create a new task
- Update an existing task
- Delete a task
- Health check endpoint
- PostgreSQL database
- Dockerized FastAPI application
- Docker Compose for multi-container setup
- Automatic database table initialization
- Interactive Swagger API documentation

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- PostgreSQL 16
- Psycopg
- Docker
- Docker Compose
- Uvicorn

## Project Structure

```text
TaskAPI/
│
├── main.py
├── database.py
├── postgres_repository.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── init.sql
├── .env.example
├── .gitignore
├── README.md
└── database_ss.png