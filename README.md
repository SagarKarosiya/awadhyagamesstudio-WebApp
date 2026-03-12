# 🎮 Awadhya Games Studio – Official Website

A dynamic **Game Studio Website** built using **Flask (Python)** that allows visitors to explore games, watch trailers, and view screenshots while providing an **admin dashboard** to manage game content.

This project was created as part of building a **professional portfolio and publishing platform for Awadhya Games Studio**.

---

# 🌐 Live Website

👉 https://awadhyagamesstudio.onrender.com

---

# 🚀 Features

### 🎮 Game Showcase

* View list of all games
* Dedicated **Game Detail Page**
* Game cover images
* Game description
* Embedded **YouTube trailers**
* Screenshot gallery

### 🖼 Dynamic Content

* Game data stored in database
* Screenshots uploaded dynamically
* Game pages generated automatically

### 🔐 Admin Panel

* Secure admin login
* Upload new games
* Upload game cover images
* Upload multiple screenshots
* Add YouTube trailer links
* Manage game information

### 🎬 Cinematic UI

* Dark game-style UI
* Screenshot gallery
* Trailer player
* Responsive layout

---

# 🛠 Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite 
* PostgreSQL (For Deployment)

### Deployment

* Render

---

# 📂 Project Structure

```
Ags_Webapp/
│
├── app.py
├── requirements.txt
├── database.db
│
├── templates/
│   ├── index.html
│   ├── games.html
│   ├── game_detail.html
│   ├── admin.html
│   └── login.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │
│   ├── uploads/
│   │   ├── covers/
│   │   └── screenshots/
│   │
│   └── videos/
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Ags_Webapp.git
cd Ags_Webapp
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 🔑 Admin Access

Admin login allows you to upload and manage games.

Example credentials:

```
Username: 
Password: 
```

You can change these credentials in the database.

---

# 🎮 Example Game Page

Game pages include:

* Game cover
* Description
* Trailer video
* Screenshot gallery

Visitors can explore each game individually.

---

# 🌍 Deployment

This project is deployed using **Render**.

Steps used:

1. Push project to GitHub
2. Connect GitHub repository to Render
3. Configure Flask start command

```
python app.py
```

4. Deploy the service

---

# 📌 Future Improvements

* User authentication system
* Blog / Devlog section
* Download links for games
* Steam-style UI improvements
* Background cinematic slideshow
* PostgreSQL database
* Analytics dashboard

---

# 👨‍💻 Author

**Sagar Karosiya**

AI & ML Graduate
Game Developer | Awadhya Games Studio
## Portfolio : https://sagarkarosiya-portfolio.onrender.com
GitHub
https://github.com/SagarKarosiya

---

# 📜 License

This project is open-source and available under the **MIT License**.

---

⭐ If you like this project, consider **starring the repository**!



## Link : https://awadhyagamesstudio.onrender.com/
