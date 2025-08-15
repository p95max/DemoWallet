# DemoWallet

DemoWallet is a modern MVP for a digital wallet and payment system, built with Django 5, Django REST Framework, and PostgreSQL. It supports user registration, KYC, P2P transfers, merchant payments, transaction ledger, and dispute management.

---

## Features

- User registration & KYC
- Account management
- P2P transfers
- Merchant payments (Stripe/PayPal ready)
- Ledger for all transactions
- Dispute management
- Django admin panel
- OpenAPI documentation (Swagger / ReDoc)
- Auth by Google

---

## Tech Stack

- Python 3.12+
- Django 5.x
- Django REST Framework
- PostgreSQL
- drf-spectacular (OpenAPI)
- Docker & Docker Compose (recommended for local development)

---

## Quickstart

1. Clone the repository:

```bash
    git clone https://github.com/yourusername/demowallet.git
    cd demowallet
```

2. Configure environment:

Copy `.env.example` to `.env` (or use `docker/.env`) and set your secrets and DB credentials.

Example minimal `.env`:

```
    SECRET_KEY=change-me
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    DATABASE_URL=postgres://user:password@db:5432/demowallet
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=admin
    STRIPE_SECRET_KEY=
    PAYPAL_CLIENT_ID=
    PAYPAL_SECRET=
```

3. Install dependencies:

With Poetry (recommended):

```bash
    poetry install
    poetry shell
```


4. Run migrations:

```bash
    python manage.py migrate
```

5. Create superuser:

```bash
    python manage.py createsuperuser
```

6. Start the server:

```bash
      python manage.py runserver
```

App available at: `http://localhost:8000`

---

## Docker (recommended)

Example `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: demouser
      POSTGRES_PASSWORD: demopass
      POSTGRES_DB: demowallet
    volumes:
      - db_data:/var/lib/postgresql/data

  web:
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://demouser:demopass@db:5432/demowallet
    depends_on:
      - db

volumes:
  db_data:
```

Run:

```bash
      docker compose up --build
```

---

## API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`
- Redoc: `http://localhost:8000/api/redoc/`

---

## Project Structure

Apps are located in `apps/`:

- `users` — registration, profile, KYC
- `accounts` — wallets, balances
- `payments` — merchant payments, gateways
- `transactions` — operations & transfers
- `ledger` — transaction ledger
- `disputes` — dispute and refund handling

---

## Admin Panel

Django Admin: `http://localhost:8000/admin/`

---

## Testing

Uses `pytest` and `pytest-django`.

Run tests:

```bash
    pytest
```

---

## Production Recommendations

- Set `DEBUG=False`
- Store secrets in a secure location (vault, secrets manager, CI/CD variables)
- Use HTTPS/TLS
- Configure PostgreSQL backups
- Restrict `ALLOWED_HOSTS` and configure CORS
- Add monitoring/logging (Sentry, Prometheus, ELK, etc.)

---

## Contributing

1. Open an issue before large changes
2. Create branches using `feature/<desc>` or `bugfix/<desc>`
3. Write tests for new features
4. Follow code style and linters

---

## License

MIT License

---

## Author

p95max
