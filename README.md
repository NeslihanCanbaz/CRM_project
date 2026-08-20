# CRM Project (Customer Relationship Management)

## 📋 Overview

Many organizations rely on Google Drive and its components to manage and store data, since it offers free or low-cost tools for this purpose. Various organizations run mentor interviews, project evaluations, and interview processes for candidates from refugee backgrounds interested in working in IT — and manage all of this through Google Drive.

Challenges like needing a constantly open session, messy Excel files, and slow access to the right data made these workflows harder than they needed to be. This project was built to solve that: a user-friendly desktop application that streamlines the whole process.

## 🛠️ Tech Stack

- **Python 3**
- **PyQt6** — desktop UI
- **Google Drive / Calendar API** — data sync and event tracking
- **openpyxl / pandas** — for reading Excel files (see `requirements.txt`)

## 📂 Project Structure

```
CRM_project/
├── main.py                  # Application entry point
├── backend/                 # Business logic (login, mentor, interview, admin operations)
│   ├── login_logic.py
│   ├── auth.py
│   ├── applications_logic.py
│   ├── mentor_interview_logic.py
│   ├── interview_logic.py
│   ├── admin_menu_logic.py
│   ├── preference_menu_logic.py
│   ├── preference_admin_logic.py
│   ├── read_xlsx.py
│   ├── set_table_data.py
│   ├── get_events.py
│   └── download_file.py
├── py/                      # Screen/window classes
│   ├── login.py
│   ├── admin_menu.py
│   ├── applications.py
│   ├── mentor_interview.py
│   ├── interview.py
│   ├── preference_menu.py
│   └── preference_admin.py
├── ui/                      # Qt Designer interface files (.ui)
│   ├── login.ui
│   ├── admin_menu.ui
│   ├── applications.ui
│   ├── mentor_interview.ui
│   ├── interview.ui
│   ├── preference_menu.ui
│   ├── preference_admin.ui
│   └── requirements.txt
├── documents/                # Project documentation
├── Basvurular.xlsx           # Applications
├── Kullanicilar.xlsx         # Users
├── Mentor.xlsx                # Mentor interviews
└── Mulakatlar.xlsx           # Interviews
```

## 🚀 Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/NeslihanCanbaz/CRM_project.git
   cd CRM_project
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r ui/requirements.txt
   ```

3. Create a `.env` file (it's excluded via `.gitignore` and not included in the repo) and add your own Google API credentials / environment variables.

4. Run the application:

   ```bash
   python main.py
   ```

## 🖥️ User Interface

### Login Screen

Access is granted to users whose username and password were registered by the owner of the main Google Drive/Gmail account. This information is stored in `Kullanicilar.xlsx`.

- If the user's role is **Admin** → redirected to the *Admin Preferences* menu.
- If the user's role is **User** → redirected to the *Preferences* menu.

The login screen includes:
- Separate input fields for username and password
- A login button with a success/error message
- An optional exit button

### Preferences (Admin)

- **Applications** — opens the applications list screen
- **Mentor Interview** — opens the mentor interview screen
- **Interviews** — opens the interviews screen
- **Admin Menu** — opens admin operations

### Preferences (User)

- **Applications**, **Mentor Interview**, **Interviews** screens (no access to the admin menu)

### Applications Screen

- **Search** — search by first/last name (e.g. typing "As" returns all names starting with "As")
- **All Applications** — lists all records from `Basvurular.xlsx`
- **Mentor Assigned / Not Assigned** — filters candidates by whether a mentor has been assigned
- **Duplicate Records** — lists candidates registered more than once with the same name and email
- **Previous Program Check** — cross-references VIT1/VIT2/Applications files to check whether a candidate applied to more than one program cycle
- **Unique to One Program** — lists candidates that only appear in VIT1 or VIT2, not both
- **Deduplicated View** — lists applications with duplicates removed (each name shown once)

### Mentor Screen

- **Search** — search by first/last name
- **All Interviews** — lists all records from `Mentor.xlsx`
- **Multi-tab filtering** — shows records filtered by the selected tab/preference

### Interviews Screen

- **Search** — search by first/last name
- **Project Submitted** — filters candidates who submitted their project, based on `Mulakatlar.xlsx`
- **Project Received** — filters candidates whose project has been received

### Admin Menu

- **Event Log** — lists events from Google Drive/Calendar
- **Mail** — automatically sends emails to addresses registered for calendar events
- **Table** — displays records pulled from Google Calendar

## ⚠️ Security Note

This project uses Google Drive/Calendar API credentials. **Never** commit your `.env` file — it's already listed in `.gitignore`. Keep your credentials local, and rotate them periodically.

## 🙌 Contributing

Feel free to open an issue or submit a pull request with bug fixes or feature suggestions.
