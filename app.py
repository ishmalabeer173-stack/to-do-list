
import json
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "todo-list-local-secret"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "tasks.json"

PRIORITIES = ["Low", "Medium", "High"]


def load_tasks():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
        return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


@app.route("/")
def index():
    tasks = load_tasks()

    filter_by = request.args.get("filter", "all")
    if filter_by not in ("all", "pending", "completed"):
        filter_by = "all"

    if filter_by == "pending":
        visible_tasks = [t for t in tasks if not t["completed"]]
    elif filter_by == "completed":
        visible_tasks = [t for t in tasks if t["completed"]]
    else:
        visible_tasks = tasks

    total = len(tasks)
    completed_count = sum(1 for t in tasks if t["completed"])

    return render_template(
        "index.html",
        tasks=visible_tasks,
        filter_by=filter_by,
        total=total,
        completed_count=completed_count,
        pending_count=total - completed_count,
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium")

    if not title:
        flash("Please enter a task title.", "error")
    elif priority not in PRIORITIES:
        flash("Please select a valid priority.", "error")
    else:
        tasks = load_tasks()
        task_id = max(
            (task.get("id", 0) for task in tasks),
            default=0,
        ) + 1

        tasks.append({
            "id": task_id,
            "title": title,
            "priority": priority,
            "completed": False,
        })

        save_tasks(tasks)
        flash("Task added successfully!", "success")

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            save_tasks(tasks)
            break

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [
        task for task in tasks if task["id"] != task_id
    ]

    if len(updated_tasks) != len(tasks):
        save_tasks(updated_tasks)
        flash("Task deleted.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
