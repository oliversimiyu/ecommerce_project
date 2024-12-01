# Spree E-Commerce Shop

A modern, feature-rich Django e-commerce platform with advanced user management and product features.

## Project Overview

This Django-based e-commerce application provides a comprehensive online shopping experience with robust features for users and administrators.

### Key Features

- User Profile Management
- Advanced Product Filtering
- Product Reviews System
- Order Tracking
- Responsive Design
- Secure Authentication
- Stripe Payment Integration

## Technical Stack

- **Language**: Python 3.12.6
- **Framework**: Django 5.0.1
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5
- **Payment Gateway**: Stripe

## Prerequisites

- Python 3.12.6
- pip
- virtualenv (recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/spree_shop.git
cd spree_shop
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Admin Access

Access the Django admin interface at `/admin` using the superuser credentials you created.

## Testing

```bash
python manage.py test
```

## Deployment Considerations

- Set `DEBUG=False` in production
- Use a production-grade database (PostgreSQL recommended)
- Configure static and media file hosting
- Set up HTTPS
- Use environment-specific settings

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - oliverwafula2020@gmail.com

Project Link: [https://github.com/yourusername/spree_shop](https://github.com/oliversimiyu/spree_shop)
