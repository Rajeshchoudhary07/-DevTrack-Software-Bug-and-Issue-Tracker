
# 🚀 DevTrack — Software Bug and Issue Tracker

A full-stack software issue tracking application built with **Python, Flask, SQLAlchemy, SQLite, REST APIs, HTML, CSS, JavaScript, and Pytest**. DevTrack helps development teams create, assign, prioritize, track, and resolve software bugs through a structured issue management workflow.

## 📌 Project Overview

DevTrack is designed to simplify software defect management by providing a centralized dashboard for tracking issues throughout their lifecycle. Users can create bug reports, assign issues to team members, set priorities, update statuses, search records, and monitor overall issue progress.

The application uses Flask for backend development, SQLite for persistent data storage, and a responsive web interface for issue management.

## ✨ Key Features

- **Issue Management:** Create, view, update, and delete software issues.
- **Status Tracking:** Manage issues through Open, In Progress, and Resolved workflows.
- **Priority Management:** Classify issues as Low, Medium, High, or Critical.
- **Assignment Management:** Assign issues to developers or team members.
- **Search Functionality:** Search issues by title, description, or assignee.
- **Filtering:** Filter issues by status and priority.
- **Dashboard Statistics:** View total issues and status-wise counts.
- **RESTful API:** Expose endpoints for issue creation, retrieval, updates, and deletion.
- **Input Validation:** Validate issue titles, priorities, and status values.
- **Error Handling:** Return structured JSON error responses for invalid requests and missing records.
- **Database Persistence:** Store issue records in an SQLite database.
- **Automated Testing:** Use Pytest to test API endpoints, CRUD operations, filtering, and validation.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Frontend | HTML5, CSS3, JavaScript |
| API Architecture | RESTful APIs |
| Testing Framework | Pytest |
| Version Control | Git, GitHub |
| Development Tools | Visual Studio Code, Postman |

## 🏗️ System Architecture

The application follows a simple layered architecture:

1. **Frontend Layer:** Provides the user interface for creating, editing, searching, filtering, and deleting issues.
2. **Application Layer:** Flask handles HTTP requests, business logic, input validation, and error responses.
3. **Data Access Layer:** SQLAlchemy manages database operations and maps Python objects to database records.
4. **Database Layer:** SQLite stores issue information persistently.
5. **Testing Layer:** Pytest verifies important application and API behaviors.

## 📂 Project Structure

```text
DevTrack/
│
├── app.py                  # Flask application and REST API endpoints
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Files excluded from Git
│
├── templates/
│   └── index.html           # Main application interface
│
├── static/
│   ├── style.css            # UI styling and responsive layout
│   └── app.js               # Frontend interactions and API calls
│
└── tests/
    └── test_api.py          # Automated API tests
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- pip package manager
- Visual Studio Code (recommended)
- Git (optional, for version control)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/DevTrack.git
cd DevTrack
```

Replace `YOUR-USERNAME` with your GitHub username. If you downloaded the ZIP file instead, extract it and open the `DevTrack` folder in your terminal.

### Step 2: Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Start the Application

```bash
python app.py
```

The Flask development server will start at:

**http://127.0.0.1:5000**

Open the URL in your browser to access DevTrack.

The SQLite database is initialized automatically when the application starts.

## 🔌 REST API Documentation

All API endpoints use JSON for request and response bodies, except the web interface route.

### 1. Health Check

**Endpoint:** `GET /api/health`

Checks whether the application is running.

Example response:

```json
{
  "status": "ok",
  "application": "DevTrack"
}
```

### 2. Get All Issues

**Endpoint:** `GET /api/issues`

Returns the list of issues stored in the database.

Optional query parameters:

| Parameter | Description | Example |
|---|---|---|
| `status` | Filter by issue status | `?status=Open` |
| `priority` | Filter by priority | `?priority=High` |
| `q` | Search title, description, or assignee | `?q=login` |

Example:

```http
GET /api/issues?status=Open&priority=High
```

### 3. Create an Issue

**Endpoint:** `POST /api/issues`

Creates a new issue.

Example JSON request:

```json
{
  "title": "Login fails after password reset",
  "description": "The user cannot log in after resetting the password.",
  "priority": "High",
  "status": "Open",
  "assignee": "Asha"
}
```

A successful request returns HTTP `201 Created` with the newly created issue.

### 4. Get an Issue by ID

**Endpoint:** `GET /api/issues/<id>`

Retrieves a specific issue using its unique ID.

Example:

```http
GET /api/issues/1
```

Returns HTTP `404 Not Found` if the issue does not exist.

### 5. Update an Issue

**Endpoint:** `PATCH /api/issues/<id>`

Updates one or more fields of an existing issue.

Example request:

```json
{
  "status": "In Progress",
  "priority": "Critical",
  "assignee": "Rahul"
}
```

Only the supplied fields are updated.

### 6. Delete an Issue

**Endpoint:** `DELETE /api/issues/<id>`

Deletes an issue using its ID.

Example:

```http
DELETE /api/issues/1
```

A successful request returns a confirmation message.

## 🔄 Issue Lifecycle

DevTrack supports the following issue statuses:

- **Open:** The issue has been reported and is awaiting work.
- **In Progress:** A developer is actively investigating or fixing the issue.
- **Resolved:** The issue has been marked as resolved.

Supported priorities:

- **Low:** Minor issue with limited impact.
- **Medium:** Issue requiring normal attention.
- **High:** Significant issue requiring timely resolution.
- **Critical:** Issue requiring urgent attention.

## 🧪 Testing

DevTrack includes Pytest tests for key application behaviors.

Run the test suite using:

```bash
python -m pytest -v
```

The tests cover:

- Application health endpoint
- Issue creation and retrieval
- Required title validation
- Issue status updates
- Invalid status rejection
- Filtering issues by status
- Issue deletion and not-found behavior

These tests help verify the correctness of core REST API functionality.

## 🔍 Example Workflow

1. Launch the application.
2. Create a new issue with a title and description.
3. Select a priority and assign a developer.
4. Track the issue using its status.
5. Search or filter issues to find specific records.
6. Update the issue when work progresses.
7. Mark the issue as Resolved when the fix is complete.

## 🔐 Validation and Error Handling

The application implements basic safeguards, including:

- Required issue title validation
- Maximum title length validation
- Allowed status and priority validation
- JSON request body validation
- Handling of requests for nonexistent issue IDs
- Database rollback on handled create/update failures

**Production considerations:** Authentication, authorization, CSRF protection where applicable, audit logs, pagination, database migrations, and production-grade server configuration should be added before deployment.

## 🚀 Future Enhancements

Potential improvements include:

- User authentication and role-based access control
- Comments and discussion threads on issues
- File attachments and screenshots
- Issue due dates and labels
- Email notifications
- Activity history and audit trails
- Pagination for large issue collections
- PostgreSQL support for production deployments
- CI/CD integration with GitHub Actions
- Docker-based deployment

## 👨‍💻 Development and Version Control

Initialize Git and commit the project:

```bash
git init
git add .
git commit -m "Build DevTrack issue tracker"
```

To push to GitHub, create an empty repository and configure its remote:

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/DevTrack.git
git push -u origin main
```

Replace the URL with your actual GitHub repository URL.

## 📄 License

This project is intended for educational and portfolio use. Add a `LICENSE` file if you want to distribute it under a specific open-source license.

## 👋 Author

**Your Name**

GitHub: https://github.com/YOUR-USERNAME

---

⭐ If you find this project useful, consider starring the repository!
