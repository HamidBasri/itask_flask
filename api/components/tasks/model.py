from api.config.loader import db
import enum
from datetime import datetime


class TaskStatus(enum.Enum):
    start = 0
    in_progress = 1
    postponed = 2
    done = 3


# Define the Task data-model.
class Task(db.Model):
    __tablename__ = "tasks"

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # title of project
    title = db.Column(db.String(length=180), nullable=False)

    description = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creator = db.relationship("User", backref="my_tasks")

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    for_project = db.relationship("Project", backref="tasks")

    assigned_users = db.relationship("User", secondary="assigned_tasks", backref="assigned_tasks")

    # Creation time for user.
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<Task(id='%s', title='%s', created='%s')>" % (
            self.id,
            self.title,
            self.start_date,
        )


# Define the AssignedTask table
class AssignedTask(db.Model):
    __tablename__ = "assigned_tasks"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    task_id = db.Column(db.Integer(), db.ForeignKey("tasks.id", ondelete="CASCADE"))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.Enum(TaskStatus), nullable=False, default=TaskStatus.start
    )  # start, in_progress, done, postponed
