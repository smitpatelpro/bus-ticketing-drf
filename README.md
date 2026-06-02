# Bus Ticketing System

A Django REST Framework based API application for online bus seat booking.

## Tech Stack

- **Backend**: Django 4.0, Django REST Framework 3.13
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Storage**: AWS S3 (via django-storages + boto3)
- **Testing**: pytest-django, Faker, pytest-factoryboy
- **Load Testing**: Locust
- **Deployment**: Gunicorn

## Features

### Authentication
- JWT-based authentication with access/refresh tokens
- Token refresh endpoint

### Bus Operator Portal
- Profile management (view, update, media)
- Bus CRUD operations
- Bus photo management
- Bus amenities management
- Bus stoppage management
- Bus search functionality

### Bus Admin Portal
- Test API endpoint

### Customer Portal
- Customer profile management
- Ticket booking and management

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/login` | Obtain access & refresh tokens |
| POST | `/api/v1/token/refresh` | Refresh access token |

### Bus Operator

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PATCH | `/api/v1/bus_operators/profile` | View/Update own profile |
| GET/PATCH | `/api/v1/bus_operators/profile/media` | View/Update profile media |
| GET/PATCH | `/api/v1/bus_operators/<uuid>` | View/Update specific operator |
| GET/POST | `/api/v1/bus_operators` | List/Create operators |
| GET/POST | `/api/v1/buses` | List/Create buses |
| GET/PATCH/DELETE | `/api/v1/buses/<uuid>` | Bus details |
| GET/POST | `/api/v1/buses/<uuid>/photos` | Bus photos |
| GET/POST | `/api/v1/buses/<uuid>/amenities` | Bus amenities |
| GET/POST | `/api/v1/buses/<uuid>/stops` | Bus stops |
| GET | `/api/v1/buses/search` | Search buses |
| GET | `/api/v1/bookings/tickets` | Book tickets |

### Customer

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PATCH | `/api/v1/customers/profile` | View/Update own profile |
| GET/PATCH | `/api/v1/customers/profile/media` | View/Update profile media |
| GET/POST | `/api/v1/customers` | List/Create customers |
| GET/PATCH/DELETE | `/api/v1/customers/<uuid>` | Customer details |
| GET/POST | `/api/v1/tickets` | List/Create tickets |
| GET/PATCH/DELETE | `/api/v1/tickets/<uuid>` | Ticket details |

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- AWS S3 bucket (for media storage)

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd bus-ticketing-drf
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env-example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration

Copy `.env-example` to `.env` and fill in the required values:

```env
DEBUG=True
SECRET_KEY=""

DB_NAME=""
DB_USER=""
DB_PASS=""
DB_HOST=""
DB_PORT=""

AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""
```

## Testing

### Unit Tests

```bash
pytest
```

### Load Testing

```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Project Structure

```
bus-ticketing-drf/
├── authentication/     # JWT auth, token views
├── bus_admin/          # Bus admin portal endpoints
├── bus_operator/       # Bus operator portal (buses, profiles)
├── bus_ticketing/      # Project settings, urls, wsgi
├── common/             # Shared models, serializers, utilities
├── customer/           # Customer portal (tickets, profiles)
├── tests/              # Test suite
├── manage.py
├── requirements.txt
├── pytest.ini
├── locustfile.py
├── .env-example
└── README.md
```

## Code Quality

This project uses the following tools for code quality:

- **Black** — Code formatting
- **Pre-commit** — Git hook management

Run pre-commit hooks manually:

```bash
pre-commit run --all-files
```
