from api.components.users.model import Role, User
from api.utils import logger
from api.components.projects.model import Project
from api.config.config import Permissions


def initialize_database(db):
    try:
        # initialize database
        # TODO it can be in a different file
        db.session.add(Role(name=Permissions.Developer.value))
        db.session.add(Role(name=Permissions.ProjectManager.value))
        db.session.commit()

        developer = Role.query.filter_by(name=Permissions.Developer.value).first()
        projectManager = Role.query.filter_by(name=Permissions.ProjectManager.value).first()

        developer = User(username="developer", password="developer", email="developer@example.com", roles=[developer])

        db.session.add(developer)
        db.session.add(
            User(username="manager", password="manager", email="manager@example.com", roles=[projectManager])
        )

        project = Project(title="test", description="test", creator=developer, assigned_users=[developer])
        db.session.add(project)

        db.session.commit()

    except Exception as e:
        logger.error(e)
        raise Exception("Failed initialize database")
