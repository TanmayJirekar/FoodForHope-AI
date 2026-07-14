# 🍱 FoodForHope-AI

> An AI-powered food donation and distribution platform that connects food donors with NGOs and people in need, helping reduce food waste while fighting hunger.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![AI](https://img.shields.io/badge/AI-Powered-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

FoodForHope-AI is an intelligent food donation management platform designed to bridge the gap between food donors, NGOs, and beneficiaries. The platform leverages Artificial Intelligence to streamline donation verification, optimize food distribution, and minimize food wastage.

Whether it's restaurants, hotels, events, or individuals with surplus food, FoodForHope-AI enables them to donate safely while ensuring food reaches the people who need it the most.

---

## ✨ Features

### 🤖 AI-Powered Food Verification
- Analyze food images using AI
- Estimate food freshness
- Detect food categories
- Verify donation quality

### 🍽️ Food Donation Management
- Easy food donation submission
- Upload food images
- Specify quantity and pickup time
- Real-time donation status tracking

### 🏢 NGO Dashboard
- View nearby food donations
- Accept or reject donation requests
- Track pickups
- Manage completed distributions

### 👤 User Authentication
- Secure Login & Registration
- JWT Authentication
- Role-based Access
- Donor and NGO accounts

### 📍 Smart Distribution
- Location-based donation matching
- Efficient food allocation
- Reduced transportation time
- Better resource utilization

### 📊 Dashboard & Analytics
- Total donations
- Food saved from waste
- Meals served
- Active NGOs
- Donation history

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- MySQL

### AI
- Groq API
- LLM-based Food Analysis
- Image Understanding

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Database
- MySQL

---

## 📂 Project Structure

```
FoodForHope-AI/
│
├── app.py
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── uploads/
├── config.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/TanmayJirekar/FoodForHope-AI.git

cd FoodForHope-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file

```env
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/foodforhope

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=1440

GROQ_API_KEY=your_groq_api_key
```

### 5. Run Database

Create a MySQL database

```sql
CREATE DATABASE foodforhope;
```

### 6. Start Server

```bash
python app.py
```

---

## 📸 Screenshots

> Add screenshots of:

- Home Page
- Login
- Donation Form
- NGO Dashboard
- AI Food Analysis
- Analytics Dashboard

---

## 🔮 Future Enhancements

- 📱 Mobile Application
- 🛰 Live Pickup Tracking
- 🔔 Push Notifications
- 🌍 Multi-language Support
- 🤖 Advanced AI Food Quality Detection
- 📍 Google Maps Integration
- 💳 Donation Support
- 📈 AI Demand Prediction

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork the repository
2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Tanmay Jirekar**

GitHub: https://github.com/TanmayJirekar

---

## 🌟 Support

If you found this project helpful, consider giving it a ⭐ on GitHub!

Together, we can reduce food waste and fight hunger with AI.
