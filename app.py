from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os

db = SQLAlchemy()

VALID_STATUSES = {"Open", "In Progress", "Resolved"}
VALID_PRIORITIES = {"Low", "Medium", "High", "Critical"}

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///devtrack.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    class Issue(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(160), nullable=False)
        description = db.Column(db.Text, nullable=False, default="")
        priority = db.Column(db.String(20), nullable=False, default="Medium")
        status = db.Column(db.String(20), nullable=False, default="Open")
        assignee = db.Column(db.String(100), nullable=False, default="Unassigned")
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

        def to_dict(self):
            return {
                "id": self.id, "title": self.title, "description": self.description,
                "priority": self.priority, "status": self.status, "assignee": self.assignee,
                "created_at": self.created_at.isoformat() + "Z",
                "updated_at": self.updated_at.isoformat() + "Z"
            }

    with app.app_context():
        db.create_all()

    def error(message, status=400):
        return jsonify({"error": message}), status

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "application": "DevTrack"})

    @app.get("/api/issues")
    def list_issues():
        query = Issue.query
        status = request.args.get("status")
        priority = request.args.get("priority")
        search = request.args.get("q", "").strip()
        if status:
            if status not in VALID_STATUSES:
                return error("Invalid status. Use Open, In Progress, or Resolved.")
            query = query.filter_by(status=status)
        if priority:
            if priority not in VALID_PRIORITIES:
                return error("Invalid priority. Use Low, Medium, High, or Critical.")
            query = query.filter_by(priority=priority)
        if search:
            query = query.filter(
                db.or_(Issue.title.ilike(f"%{search}%"),
                       Issue.description.ilike(f"%{search}%"),
                       Issue.assignee.ilike(f"%{search}%"))
            )
        issues = query.order_by(Issue.updated_at.desc()).all()
        return jsonify({"items": [item.to_dict() for item in issues], "count": len(issues)})

    @app.post("/api/issues")
    def create_issue():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return error("Request body must be valid JSON.")
        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        priority = data.get("priority", "Medium")
        status = data.get("status", "Open")
        assignee = str(data.get("assignee", "Unassigned")).strip() or "Unassigned"
        if not title:
            return error("Title is required.")
        if len(title) > 160:
            return error("Title must be 160 characters or fewer.")
        if priority not in VALID_PRIORITIES:
            return error("Invalid priority.")
        if status not in VALID_STATUSES:
            return error("Invalid status.")
        issue = Issue(title=title, description=description, priority=priority,
                      status=status, assignee=assignee)
        db.session.add(issue)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return error("Could not save issue.", 500)
        return jsonify(issue.to_dict()), 201

    @app.get("/api/issues/<int:issue_id>")
    def get_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return error("Issue not found.", 404)
        return jsonify(issue.to_dict())

    @app.patch("/api/issues/<int:issue_id>")
    def update_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return error("Issue not found.", 404)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return error("Request body must be valid JSON.")
        if "title" in data:
            title = str(data["title"]).strip()
            if not title or len(title) > 160:
                return error("Title is required and must be 160 characters or fewer.")
            issue.title = title
        if "description" in data:
            issue.description = str(data["description"]).strip()
        if "assignee" in data:
            issue.assignee = str(data["assignee"]).strip() or "Unassigned"
        if "priority" in data:
            if data["priority"] not in VALID_PRIORITIES:
                return error("Invalid priority.")
            issue.priority = data["priority"]
        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                return error("Invalid status.")
            issue.status = data["status"]
        issue.updated_at = datetime.utcnow()
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return error("Could not update issue.", 500)
        return jsonify(issue.to_dict())

    @app.delete("/api/issues/<int:issue_id>")
    def delete_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return error("Issue not found.", 404)
        db.session.delete(issue)
        db.session.commit()
        return jsonify({"message": "Issue deleted.", "id": issue_id})

    # Expose model for tests without changing the public API.
    app.extensions["devtrack_issue_model"] = Issue
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
