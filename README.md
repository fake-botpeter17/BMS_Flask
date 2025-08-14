# 🧵 Fashion Paradise – Textile Management System (Flask SSR)

A modern, **server-side rendered** Flask application for **Fashion Paradise**, built with **vanilla HTML, CSS, and JavaScript**.  
The system reuses previously developed Python utility modules for **API integration**, **authentication**, and **data handling** to deliver a fast, theme-consistent, and responsive UI — without relying on heavy frontend frameworks.

---

## 🌟 Features

- **Server-Side Rendering (SSR)** for improved performance and SEO.
- **Theme-matched UI** using Fashion Paradise’s dark teal & peach palette.
- **Vanilla HTML, CSS, JS** for minimal dependency overhead.
- **Reused Python utilities** for:
  - Authentication flow & session handling
  - API calls & data caching
  - Inventory & sales data processing
- **Responsive Design** for desktop & mobile.
- Smooth **animations** and interactive form elements.

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Styling:** Tailwind CSS + Custom theme
- **Utilities:** Custom Python modules for API, authentication, and business logic
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
fashion-paradise-ssr/
│
├── main.py             # Server Entry point
├── app.py               # Flask app entry point
├── utils/               # Reused utility modules
├── templates/           # HTML templates (SSR views)
├── static/              # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── img/             # Images & icons
├── requirements.txt     # Python dependencies
└── README.md
````
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/fake.botpeter17/BMS_Flask.git
cd BMS_Flask
````

### 2️⃣ Activate the virtual environment and Install Dependencies

```bash
uv sync
```


### 3️⃣ Run the development server

```bash
uv run main.py
```

The app will be available at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎨 UI Highlights

* **Login Form** with themed styling, focus effects, and password visibility toggle.
* **Responsive Layout** for mobile and desktop.
* **Floating Accents & Patterned Background** to reflect the brand’s textile theme.
* **Consistent Typography** — decorative for headings, readable for body text.

---

## 🔒 Security

* Basic form validation (client & server side)
* Planned features: CSRF protection, secure session storage, and password hashing

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For inquiries or collaboration, contact **[nebinson1@gmail.com](mailto:your-nebinson1@gmail.com)**
