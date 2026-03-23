# rapidpass

Rapidpass is a small Django + Django REST Framework microservice for event ticketing and bookings. It provides models for events and ticket types, a safe booking service that reserves quantities transactionally, and a small API to create bookings.

Key ideas

- Fast proof-of-concept for event ticket sales and reservations.
- Concurrent-safe booking using database row locking to prevent overselling.
- Minimal REST API endpoints for creating bookings.

Tech stack

- Python 3.12+
- Django 6.x
- Django REST Framework
- djangorestframework-simplejwt (JWT auth available in project dependencies)
- SQLite (development DB included)

Repository layout (important files)

- `config/` — Django project and app wiring
- `config/apps/tickets/` — ticketing models, booking service, and booking API
- `config/apps/users/` — user-related views (simple RegisterAPIView exists)
- `pyproject.toml` — project dependencies

Quick setup (Windows PowerShell)

Open PowerShell and run these commands from the repository root (D:\My-Space\rapidpass):

```powershell
# 1) Create a virtual environment
python -m venv .venv

# 2) Activate the virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# 3) Upgrade pip and install dependencies
python -m pip install --upgrade pip
# Option A: install via pyproject (editable install)
pip install -e .
# Option B: if you prefer a requirements file, create one from pyproject or install directly:
# pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary

# 4) Apply database migrations
python config/manage.py migrate

# 5) (Optional) Create a superuser to access the admin
python config/manage.py createsuperuser

# 6) Run the development server
python config/manage.py runserver
```

Notes

- The project includes a small SQLite database at `config/db.sqlite3` for local development. For production configure `DATABASES` in `config/config/settings.py`.
- The project dependencies are declared in `pyproject.toml` — use `pip install -e .` to install them for development.

Available API

- Create a booking (tickets): POST /api/v1/bookings/
  - Body format (JSON):
    {
      "items": [
        {"ticket_type_id": 1, "quantity": 2},
        {"ticket_type_id": 2, "quantity": 1}
      ]
    }
  - Response on success: 201 Created with booking id and status.

Example request (PowerShell)

```powershell
$body = @{ items = @(@{ ticket_type_id = 1; quantity = 2 }) } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/bookings/ -Method Post -ContentType 'application/json' -Body $body
```

Developer notes

- Booking logic lives in `config/apps/tickets/services/booking_service.py`. It uses `select_for_update()` on `TicketType` rows to lock availability while creating a booking.
- Models are in `config/apps/tickets/models.py` (Event, TicketType, Booking, BookingItem).
- A simple `RegisterAPIView` implementation exists in `config/apps/users/views.py` but may not be wired into project URLs by default — add URL patterns if you need a registration endpoint.
- Run test suite with:

```powershell
python config/manage.py test
```

Contributing

- Open an issue or submit a PR with a clear description and tests where appropriate.

License

- Add a LICENSE file or choose a license for this project.

If you want, I can:

- Add a sample `requirements.txt` and a small script to seed example events and ticket types,
- Wire the `RegisterAPIView` into the API URLs and add authentication examples,
- Or create a Postman collection / README section with more examples.
