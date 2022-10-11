from api.config.loader import db, bcrypt

from datetime import datetime

# Define the User data-model.
class User(db.Model):
    __tablename__ = "users"

    # User id.
    id = db.Column(db.Integer, primary_key=True)

    # User name.
    username = db.Column(db.String(length=80), nullable=False)

    # User password.
    password = db.Column(db.String(length=80), nullable=False)

    # User email address.
    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation="NOCASE"), nullable=False, unique=True)

    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship to Role via UserRoles
    roles = db.relationship("Role", secondary="user_roles")

    assigned_projects = db.relationship("Project", secondary="assigned_projects", back_populates="assigned_users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = bcrypt.generate_password_hash(self.password).decode("utf8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.email,
            self.created,
        )


# Define the Role data-model
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
