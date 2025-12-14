# 🏥 **Pharmacy Finder Platform(https://pharmacy-app-niai.onrender.com)**

## 📌 Project Overview

The **Pharmacy Finder Platform** is a backend system built with **Django** and **Django REST Framework (DRF)** that enables:

✔️ Users to search for medicines
✔️ Pharmacies to register & verify their business
✔️ Pharmacy owners to upload medicines and manage stock
✔️ Customers to find the nearest pharmacy that has the medicine
✔️ Secure authentication (JWT or session-based)

---

# ✨ Features

## 👤 User Features (Customers)

* Search medicines by name
* View medicine details
* Check which pharmacies have a specific medicine in stock
* View pharmacy information (location, phone, opening hours)
* View/search history
* Add reviews for pharmacies (optional)

## 🏪 Pharmacy Owner Features

* Register pharmacy
* Submit verification documents
* Add medicines with:

  * Name
  * Category
  * Price
  * Stock
  * Expiration date
  * Image
* Update or delete medicines
* Manage pharmacy profile
* Track stock availability

## 🔍 Advanced Search & Filters

* Search by medicine name
* Filter by category
* Filter by price range
* Filter by availability
* Sort results (A → Z, price low → high)
* Find nearest pharmacy (optional GPS)

## ⭐ Optional Enhancements

* Pharmacy reviews & ratings
* Favorites (users save favorite pharmacies)
* Email verification
* Recommended medicines
* Search history tracking

---

# 🗂️ Entity Relationship Diagram (ERD)

> Insert your exported ERD image here:

```
![ERD Diagram](path-to-your-image.png)
```

### 📘 ERD Entities:

**User** – base user (customer or pharmacy owner)
**Pharmacy** – belongs to a user
**Verification** – pharmacy document approval
**Medicine** – global list of medicine names
**PharmacyStock** – which pharmacy has which medicine
**SearchHistory** – track user search
**Reviews** – optional ratings

---

# 📡 API Endpoints

## 🔐 Authentication Endpoints

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/auth/register/` | Register new user |
| POST   | `/api/auth/login/`    | Login & get token |
| POST   | `/api/auth/logout/`   | Logout user       |
| GET    | `/api/auth/profile/`  | Get profile       |
| PUT    | `/api/auth/profile/`  | Update profile    |

---

## 🏪 Pharmacy Endpoints

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| POST   | `/api/pharmacies/`             | Create a pharmacy        |
| POST   | `/api/pharmacies/{id}/verify/` | Upload verification docs |
| GET    | `/api/pharmacies/`             | List pharmacies          |
| GET    | `/api/pharmacies/{id}/`        | Pharmacy details         |
| PUT    | `/api/pharmacies/{id}/`        | Update pharmacy          |
| DELETE | `/api/pharmacies/{id}/`        | Delete pharmacy          |

---

## 🧾 Verification Endpoints

| Method | Endpoint                           | Description                  |
| ------ | ---------------------------------- | ---------------------------- |
| GET    | `/api/verifications/`              | Admin: list pending requests |
| PUT    | `/api/verifications/{id}/approve/` | Approve pharmacy             |
| PUT    | `/api/verifications/{id}/reject/`  | Reject pharmacy              |

---

## 💊 Medicine Endpoints

| Method | Endpoint               | Description      |
| ------ | ---------------------- | ---------------- |
| POST   | `/api/medicines/`      | Add new medicine |
| GET    | `/api/medicines/`      | List medicines   |
| GET    | `/api/medicines/{id}/` | Get medicine     |

---

## 🏪 Pharmacy Stock Endpoints

| Method | Endpoint                                 | Description                   |
| ------ | ---------------------------------------- | ----------------------------- |
| POST   | `/api/pharmacies/{id}/stock/`            | Add medicine to pharmacy      |
| PUT    | `/api/pharmacies/{id}/stock/{stock_id}/` | Update medicine stock         |
| DELETE | `/api/pharmacies/{id}/stock/{stock_id}/` | Remove medicine from pharmacy |

---

## 🔍 Search Endpoints

| Method | Endpoint                     | Description         |
| ------ | ---------------------------- | ------------------- |
| GET    | `/api/search/?medicine=name` | Search by name      |
| GET    | `/api/search/history/`       | View search history |
| DELETE | `/api/search/history/clear/` | Clear history       |

---

## ⭐ Reviews & Ratings (Optional)

| Method | Endpoint                        | Description  |
| ------ | ------------------------------- | ------------ |
| POST   | `/api/pharmacies/{id}/reviews/` | Add review   |
| GET    | `/api/pharmacies/{id}/reviews/` | List reviews |

---

# 🛠️ Technologies Used

* **Backend:** Django, DRF
* **Database:** PostgreSQL / SQLite
* **Authentication:** JWT or DRF auth
* **Testing:** Postman / Thunder Client
* **Deployment:** Render / PythonAnywhere / DigitalOcean

---

# 📁 Project Structure

```
pharmacy_finder/
│
├── pharmacy_finder/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── pharmacies/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── medicines/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── search/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
└── manage.py
```

---

# 🧪 Testing

Use **Postman** to test:

✔️ Authentication
✔️ Pharmacy creation
✔️ Verification
✔️ Stock management
✔️ Search functionality

---

# 🗓️ Weekly Project Timeline

| Week       | Tasks                            |
| ---------- | -------------------------------- |
| **Week 1** | ERD, Setup project, accounts app |
| **Week 2** | Pharmacy + verification          |
| **Week 3** | Medicine + stock system          |
| **Week 4** | Search, filters, reviews         |
| **Week 5** | Testing + optimization           |
| **Week 6** | Deployment + documentation       |

---

# 🚀 Deployment

Deploy on:

* Render
* PythonAnywhere
* DigitalOcean

You’ll configure:

1. Environment variables
2. PostgreSQL
3. Static files
4. Migrations
