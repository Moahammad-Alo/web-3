# Auction Web Application - ECS639U Group Coursework

A Single Page Application (SPA) auction platform built with Django 5.2 (backend API) and Vue 3 with TypeScript (frontend).

## Group Members

| Name | Assigned Tasks | Actual Contribution |
|------|----------------|---------------------|
| Layan Mohammed A. Alassaf | Backend models, authentication, cron jobs | Implemented Django models, auth system, email notifications |
| Mohammad Marzouq Q Almotairi | Frontend Vue components, Pinia stores | Developed Vue pages, components, state management |
| Bandar Fawaz M Alnhiani | API endpoints, testing, deployment | Created REST API, test data, OpenShift deployment |

## Deployed Application

**URL**: https://django-psql-persistent-web-3.apps.a.comp-teach.qmul.ac.uk

## Admin Credentials

| Username | Password |
|----------|----------|
| admin | admin123 |

Access the admin panel at: `/admin/`

## Test User Credentials

| Username | Password | Email |
|----------|----------|-------|
| alice | alice123 | alice@example.com |
| bob | bob123 | bob@example.com |
| charlie | charlie123 | charlie@example.com |
| diana | diana123 | diana@example.com |
| eve | eve123 | eve@example.com |

## Features

- ✅ User signup/login with custom Django User model (AbstractUser)
- ✅ Editable user profile with profile image (Ajax save)
- ✅ Create auction items with title, description, price, image, end date
- ✅ Search items by keyword (Ajax, no page refresh)
- ✅ Place bids on items before auction ends
- ✅ Questions and answers about items
- ✅ Vue Router for frontend navigation
- ✅ Pinia global store for state management
- ✅ TypeScript interfaces for all data models
- ✅ Python type annotations throughout backend
- ✅ Cron job for sending winner notification emails

## Technology Stack

**Backend:**
- Django 5.2
- Python 3.12
- SQLite (development) / PostgreSQL (production)
- django-crontab for scheduled tasks

**Frontend:**
- Vue 3 with TypeScript
- Pinia for state management
- Vue Router for SPA navigation
- Bootstrap 5 for styling
- Vite for bundling

## Local Development

### Prerequisites

- Python 3.12
- Node.js 18+
- Conda (recommended)

### Setup

1. Create and activate a conda environment:
   ```bash
   conda create -n auction python=3.12
   conda activate auction
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the database:
   ```bash
   python manage.py migrate
   ```

4. Create test data:
   ```bash
   python manage.py create_test_data
   ```

5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

6. Start the Django server:
   ```bash
   python manage.py runserver
   ```

7. Start the Vue dev server (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

8. Open http://localhost:5173 in your browser

### Setting up Email (for winner notifications)

1. Create a Gmail account for your app
2. Enable 2FA and create an App Password
3. Set environment variables:
   ```bash
   export EMAIL_HOST_USER="your-email@gmail.com"
   export EMAIL_HOST_PASSWORD="your-app-password"
   ```

### Setting up Cron Jobs

```bash
# Add cron jobs to crontab
python manage.py crontab add

# Check scheduled jobs
python manage.py crontab show

# Remove cron jobs
python manage.py crontab remove
```

## OpenShift Deployment

1. Build the Vue frontend:
   ```bash
   cd frontend
   npm run build  # or npm run build-windows on Windows
   ```

2. Follow EECS OpenShift deployment instructions on QM+

## Project Structure

```
├── api/                    # Django app
│   ├── management/         # Management commands
│   ├── migrations/         # Database migrations
│   ├── templates/          # Django templates (auth, SPA)
│   ├── admin.py           # Admin configuration
│   ├── cron.py            # Cron job functions
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── serializers.py     # JSON serialization
│   ├── urls.py            # URL routing
│   └── views.py           # View functions
├── frontend/               # Vue frontend
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── pages/         # Vue pages
│   │   ├── router/        # Vue Router config
│   │   ├── services/      # API service
│   │   ├── stores/        # Pinia stores
│   │   └── types/         # TypeScript interfaces
│   └── ...
├── project/               # Django project settings
├── media/                 # User uploads
└── requirements.txt       # Python dependencies
```

## License

This code is dedicated to the public domain under [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
