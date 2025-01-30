# 📌 Installation & Setup

## 1️⃣ Clone the Repository

git clone https://github.com/your-username/django-product-api.git
cd django-product-api

## 2️⃣ Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

## 3️⃣ Install Dependencies

pip install -r requirements.txt

## 4️⃣ Apply Migrations

python manage.py migrate

## 5️⃣ Create a Superuser (For Admin Panel)

python manage.py createsuperuser

Follow the prompts to set up your admin credentials.
## 6️⃣ Run the Development Server

python manage.py runserver

-   Docker Desktop
-   PHP 8.3+
-   Git

The API will be available at http://127.0.0.1:8000/api/
🛠️ API Endpoints
🔑 Authentication
-   Method	Endpoint	Description
    POST	/api/token/	Obtain JWT token
    POST	/api/token/refresh/	Refresh JWT token
🛍️ Product Management
-   Method	Endpoint	Description
    GET	/api/products/	Get all products (supports filtering & pagination)
    POST	/api/products/	Create a new product (Authenticated users only)
    GET	/api/products/<id>/	Get product by ID
    PUT	/api/products/<id>/	Update product details
    DELETE	/api/products/<id>/	Soft delete a product

🔍 Filtering & Pagination
-   Filter by Name (case-insensitive match)
    GET /api/products/?name=apple

-   Filter by Price Range
    GET /api/products/?price_min=10000&price_max=50000

-   Pagination (Custom Page Size Support)
    GET /api/products/?page=2&page_size=5

# 🔐 Authentication
## 1️⃣ Obtain a JWT Token

    curl -X POST http://127.0.0.1:8000/api/token/ -d "username=admin&password=yourpassword"

    Response:
    {
        "access_token": "your-jwt-token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }

## 2️⃣ Use JWT Token in API Requests

Include the token in the Authorization header:
Authorization: Bearer your-jwt-token

## 🖥️ Admin Panel

🔹 URL: http://127.0.0.1:8000/admin/
🔹 Features: Sorting, searching, and filtering by name, price, created_at, and updated_at.

## Developed by Robi Leksono (kiloo34)
🔹 GitHub: github.com/kiloo34
🔹 LinkedIn: linkedin.com/in/your-profile

