
# Backend

Backend is a Python backend project template designed to demonstrate a robust and scalable architecture using:

*   **Hexagonal Architecture (Ports and Adapters)**: Decoupling the core domain logic from external concerns like frameworks, databases, and UI.
*   **CQRS (Command Query Responsibility Segregation)**: Separating read (Query) and write (Command) operations for potential optimization and clarity.
*   **Bundle-Contexts**: Organizing the application into distinct business capabilities (e.g., `users`, `auth`) for modularity and maintainability.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
*   **SQLAlchemy**: A powerful SQL toolkit and Object Relational Mapper (ORM).
*   **RabbitMQ**: For asynchronous command processing.
*   **Dependency Injection**: Leveraging FastAPI's built-in DI and potentially a simple container for decoupling.

## Project Goals

*   Establish a solid foundation for backend projects.
*   Ensure domain independence from external tools.
*   Facilitate scalability and modularity through Bundle-Contexts.
*   Demonstrate clear separation of concerns.

## Architectural Overview

*   **Domain Layer**: Contains the core business logic, entities, value objects, domain events, and repository interfaces. It has no dependencies on other layers.
*   **Application Layer**: Orchestrates use cases (Commands and Queries). It depends on the Domain Layer (interfaces) but not on specific infrastructure implementations.
*   **Infrastructure Layer**: Provides concrete implementations for interfaces defined in the domain or application layers (e.g., SQLAlchemy repositories, RabbitMQ publishers/consumers, database session management).
*   **Interfaces Layer (within contexts)**: Contains adapters that interact with the outside world, such as FastAPI endpoints (REST API) and RabbitMQ consumers. These adapters use the Application Layer.
*   **Core**: Shared components, base classes, and utilities used across different contexts.

```
      +---------------------+      +-----------------------+      +------------------------+
      | External Systems    |----->| Interfaces (Adapters) |----->| Application Layer      |
      | (UI, API Clients, |      | (FastAPI, Consumers)  |      | (Use Cases, DTOs)      |
      |  Message Queues)   |<-----| (Ports)               |<-----| (Ports)                |
      +---------------------+      +-----------------------+      +------------------------+
                                          |                                |
                                          v                                v
      +-------------------------+      +-----------------------+      +------------------------+
      | Infrastructure (Adapters)|<-----| Domain Layer          |      | Core / Shared Kernel |
      | (SQLAlchemy, RabbitMQ)  |      | (Entities, VOs, Repos)|      | (Base Classes, Utils)|
      | (Driven Ports)          |----->| (Ports)               |      +------------------------+
      +-------------------------+      +-----------------------+
```

## Project Structure

```
contextflow/
├── app/                      # FastAPI application setup (main.py, config, DI)
├── contexts/                 # Bundle-Contexts Root (users, auth)
│   ├── auth/                 # Auth Context
│   │   ├── application/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── interfaces/
│   └── users/                # Users Context
│       ├── application/      # Use cases (Commands, Queries, Handlers), DTOs
│       ├── domain/           # Entities, Value Objects, Repository Interfaces
│       ├── infrastructure/   # SQLAlchemy Repos, Models, RabbitMQ Adapters
│       └── interfaces/       # FastAPI Routes, RabbitMQ Consumers
├── core/                     # Shared Kernel / Core Components
├── tests/                    # Unit and Integration Tests
├── .env.example              # Environment variables template
├── .gitignore
├── Dockerfile                # Application Docker image build definition
├── docker-compose.yml        # Docker services orchestration (app, db, rabbitmq)
├── pyproject.toml            # Project metadata and dependencies (using Poetry)
└── README.md                 # This file
```

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   Python 3.10+ (if running locally without Docker)
*   Poetry (if running locally without Docker)

### Setup and Running with Docker (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd contextflow
    ```

2.  **Create environment file:**
    Copy `.env.example` to `.env` and customize the variables if needed (defaults should work for local development).
    ```bash
    cp .env.example .env
    ```

3.  **Build and run the services:**
    ```bash
    docker-compose up --build -d
    ```
    This will start the FastAPI application, a PostgreSQL database, and a RabbitMQ instance.

4.  **Access the API:**
    The API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

### Running Locally (Without Docker)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd contextflow
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

3.  **Set up external services:**
    You'll need running instances of PostgreSQL and RabbitMQ accessible to the application. Configure the connection details in your `.env` file (copy from `.env.example`).

4.  **Run database migrations (if applicable - setup required):**
    *   A migration tool like Alembic would typically be added here.

5.  **Run the FastAPI application:**
    ```bash
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

6.  **Run RabbitMQ Consumers (separate process):**
    ```bash
    poetry run python -m contexts.users.interfaces.consumers.user_consumer # Example
    ```
    *(Note: A dedicated script or entry point for running all consumers is recommended for real applications)*

### Running Tests

**With Docker:**

```bash
docker-compose exec app poetry run pytest tests/
```

**Locally:**

```bash
poetry run pytest tests/
```

To get coverage report:

```bash
poetry run pytest --cov=contexts --cov=core --cov-report=term-missing tests/
```

## Architectural Decisions

*   **Hexagonal Architecture**: Chosen for its ability to isolate the core domain logic, making the application more testable, maintainable, and adaptable to changing external technologies.
*   **CQRS**: Implemented to separate write-side complexity (potentially involving business rules, validation, transactions) from read-side optimizations. Using RabbitMQ for commands allows for asynchronous processing, improving responsiveness and resilience.
*   **Bundle-Contexts**: Grouping features by business capability (contexts) enhances modularity. Each context is a mini-application with its own layers, reducing coupling between different parts of the system.
*   **SQLAlchemy**: Provides flexibility, allowing use as a powerful ORM or a lower-level SQL toolkit when needed.
*   **FastAPI**: Offers excellent performance, automatic documentation generation, and built-in support for data validation (Pydantic) and dependency injection, which aligns well with the architectural goals.
*   **Dependency Injection**: FastAPI's DI is used for wiring dependencies in the interface layer. A simple container or manual wiring might be used within application/infrastructure layers if needed, though FastAPI's DI can often be leveraged throughout.
*   **RabbitMQ for Commands**: Ensures commands are processed reliably and asynchronously. This decouples the command issuer (e.g., API endpoint) from the handler and allows for retries, scaling consumers, etc. Queries bypass RabbitMQ for direct, faster access to read models.

## Further Development

*   Implement Authentication/Authorization (Auth Context).
*   Add database migrations (e.g., using Alembic).
*   Implement more sophisticated error handling.
*   Refine dependency injection setup.
*   Add integration tests.
*   Set up CI/CD pipeline.
*   Implement dedicated read models for optimized queries.
*   Develop a CLI script for managing consumers.

