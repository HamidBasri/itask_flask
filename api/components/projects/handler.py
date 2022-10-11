import json
from turtle import title
from flask import request, jsonify
from flask_restful import Resource
from api.config.config import Permissions
from api.config.loader import db
from api.components.projects.model import Project
from api.components.users.model import User
from api.config.auth import has_permissions, token_required
import api.utils.errors as errors
import api.utils.logger as logger

from sqlalchemy import or_

from api.components.projects.schema import NewProjectSchema, projects_schema
from api.components.users.schema import UserSchema


class ProjectsHandler(Resource):
    method_decorators = [token_required]

    @staticmethod
    def get(user):
        # get projects created by user or projects assigned to user.
        related_projects = (
            Project.query.filter(or_(Project.assigned_users.contains(user), Project.creator == user))
            .order_by(Project.created.desc())
            .all()
        )

        return jsonify({"projects": json.loads(projects_schema.dumps(related_projects))})

    @staticmethod
    @has_permissions(Permissions.ProjectManager.value)
    def post(user):
        # get request params
        try:
            new_project_schema = NewProjectSchema()
            form_data = request.get_json()
            validate_err = new_project_schema.validate(form_data)
            if validate_err:
                return {"message": validate_err}, errors.HTTP_UNPROCESSABLE_ENTITY_422
        except Exception as e:
            logger.error(e)
            return errors.INVALID_INPUT_422

        # create new project and save
        try:
            assigned_users = [user for user in User.query.filter(User.id.in_(form_data["assigned_users"])).all()]
            for assigned_user in assigned_users:
                if Permissions.Developer.value not in [role.name for role in assigned_user.roles]:
                    return {
                        "message": f"Can not assign a project to a project manager (user: {assigned_user.id})"
                    }, errors.HTTP_UNPROCESSABLE_ENTITY_422

            new_project = Project(
                title=form_data["title"],
                description=form_data["description"],
                creator_id=user.id,
                assigned_users=assigned_users,
            )
            db.session.add(new_project)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return errors.SERVER_ERROR_500

        # response
        return {"message": "New project created successfully", "project_id": new_project.id}, errors.HTTP_SUCCESS_200


class ProjectHandler(Resource):
    method_decorators = [token_required]

    @staticmethod
    @has_permissions(Permissions.ProjectManager.value)
    def patch(user, project_id):
        # get project if exists
        try:
            project = ProjectHandler.check_project_exists(project_id)
        except Exception as e:
            logger.error(e)
            return errors.NOT_FOUND_404

        try:
            update_project_schema = NewProjectSchema(only=("assigned_users",))
            form_data = request.get_json()
            validate_err = update_project_schema.validate(form_data)
            if validate_err:
                return {"message": validate_err}, errors.HTTP_UNPROCESSABLE_ENTITY_422
        except Exception as e:
            logger.error(e)
            return errors.INVALID_INPUT_422

        # assign users to project and save
        try:
            assigned_users = [user for user in User.query.filter(User.id.in_(form_data["assigned_users"])).all()]
            for assigned_user in assigned_users:
                if Permissions.Developer.value not in [role.name for role in assigned_user.roles]:
                    return {
                        "message": f"Can not assign a project to a project manager (user: {assigned_user.id})"
                    }, errors.HTTP_UNPROCESSABLE_ENTITY_422

            project.assigned_users = assigned_users
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return errors.SERVER_ERROR_500

        # response
        return {"message": "Project updated successfully."}, errors.HTTP_SUCCESS_200

    @staticmethod
    def check_project_exists(project_id):
        # check project exists
        project = Project.query.get(project_id)
        if project_id is None or project is None:
            raise Exception("Not Found")
        return project

    # get request params


class ProjectUsersHandler(Resource):
    method_decorators = [token_required]

    @staticmethod
    def get(user, project_id):
        users_type = request.json.get("type")  # task, project
        if users_type not in ["tasks", "project"]:
            # Return invalid input error.
            return {"message": "`type` should be either `tasks` or `project`"}, errors.HTTP_UNPROCESSABLE_ENTITY_422

        # ge project if exists
        try:
            project = ProjectHandler.check_project_exists(project_id)
        except Exception as e:
            logger.error(e)
            return errors.NOT_FOUND_404

        users = []
        if users_type == "tasks":
            for task in project.tasks:
                users += task.assigned_users
        else:
            users = project.assigned_users

        user_schema = UserSchema(many=True)
        return jsonify({"users": json.loads(user_schema.dumps(list(set(users))))})
