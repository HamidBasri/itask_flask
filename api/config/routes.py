from flask_restful import Api
from api.components.base.handler import Index
from api.components.users.handler import Register, Login
from api.components.projects.handler import ProjectsHandler, ProjectHandler, ProjectUsersHandler
from api.components.tasks.handler import TasksHandler


def generate_routes(app):

    # Create api.
    api = Api(app)

    # Index Resource.
    api.add_resource(Index, "/")

    # Register Resource.
    api.add_resource(Register, "/v1/auth/register")

    # Login Resource
    api.add_resource(Login, "/v1/auth/login")

    # Project Resource
    api.add_resource(ProjectsHandler, "/v1/projects")

    # Assign Developers to Project Resource
    api.add_resource(ProjectHandler, "/v1/projects/<int:project_id>")

    # Tasks in a Project Resource
    api.add_resource(TasksHandler, "/v1/project/<int:project_id>/tasks")

    # Users in a Project Resource
    api.add_resource(ProjectUsersHandler, "/v1/project/<int:project_id>/users")
