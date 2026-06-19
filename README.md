#  Employee Management System

🚀 **Live Deployment**: [https://web-production-a8a12.up.railway.app/](https://web-production-a8a12.up.railway.app/)

A web-based Employee Management System built using **Django**.  
This application allows users to **add, view, edit, and delete employees and departments** with a clean, simple interface.


---

##  Features

- Add, edit, delete, and view employees  
- Manage departments (CRUD operations)  
- View employee details by department  
- User-friendly interface using HTML, CSS  
- SQLite3 as the default database  
- Modular Django apps (Employee, Departments)

---

##  Tech Stack

- **Backend:** Django 5.2.7 (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite3 (default)
- **Version Control:** Git & GitHub

---

##  Installation

Follow these steps to run the project locally 👇

### 1️ Clone the repository
```bash
git clone https://github.com/<your-username>/employee-management-system.git
cd employee-management-system


### 2 Create a virtual environment
python -m venv companyenv

### 3 Activate the environment
Windows:
companyenv\Scripts\activate

macOS/Linux:
source companyenv/bin/activate

### 4 Install dependencies
pip install -r requirements.txt

### 5 Run migrations
python manage.py migrate

### 6 Start the server
python manage.py runserver
