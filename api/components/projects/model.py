from api.config.loader import db
from datetime import datetime


# Define the Project data-model.
class Project(db.Model):
    __tablename__ = "projects"

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # title of project
    title = db.Column(db.String(length=180), nullable=False)

    description = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    creator = db.relationship("User", backref="my_projects")

    assigned_users = db.relationship("User", secondary="assigned_projects", back_populates="assigned_projects")

    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<Project(id='%s', title='%s', created='%s')>" % (
            self.id,
            self.title,
            self.created,
        )


# Define the AssignedProject table
class AssignedProject(db.Model):
    __tablename__ = "assigned_projects"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    project_id = db.Column(db.Integer(), db.ForeignKey("projects.id", ondelete="CASCADE"))
    created = db.Column(db.DateTime, default=datetime.utcnow)
