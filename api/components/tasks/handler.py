from email import message
import json
from turtle import title
from flask import request, jsonify
from flask_restful import Resource
from api.config.config import Permissions
from api.config.loader import db
from api.components.tasks.model import Task
from api.components.users.model import User
from api.config.auth import has_permissions, token_required
from api.utils import logger, errors
from sqlalchemy import or_
from api.components.projects.handler import ProjectHandler
from api.components.tasks.schema import InputTaskSchema, TaskSchema


class TasksHandler(Resource):
    method_decorators = [token_required]

    @staticmethod
    def get(user, project_id):
        # check project exists
        try:
            project = TasksHandler._get_project_if_access(user, project_id)
        except Exception as why:
            return why.args[0]

        tasks_schema = TaskSchema(many=True)
        return jsonify({"tasks": json.loads(tasks_schema.dumps(project.tasks))})

    @staticmethod
    def post(user, project_id):
        try:
            project = TasksHandler._get_project_if_access(user, project_id)
        except Exception as why:
            return why.args[0]

        # get request params
        try:
            input_task_schema = InputTaskSchema()
            form_data = request.get_json()
            validate_err = input_task_schema.validate(form_data)
            if validate_err:
                return {"message": validate_err}, errors.HTTP_UNPROCESSABLE_ENTITY_422
        except Exception as e:
            logger.error(e)
            return errors.INVALID_INPUT_422

        # create new task and save
        try:
            project_users = [u.id for u in project.assigned_users]
            for assigned_user in form_data["assigned_users"]:
                if assigned_user not in project_users:
                    return {
                        "message": f"Can not assign a task to a user who is not in the project (user: {assigned_user})"
                    }, errors.HTTP_UNPROCESSABLE_ENTITY_422

            # check all users are developers
            assigned_users_for_task = [
                user for user in User.query.filter(User.id.in_(form_data["assigned_users"])).all()
            ]
            for assigned_user in assigned_users_for_task:
                if Permissions.Developer.value not in [role.name for role in assigned_user.roles]:
                    return {
                        "message": f"Can not assign a task to a user who is not a {Permissions.Developer.value} (user: {assigned_user.id})"
                    }, errors.HTTP_UNPROCESSABLE_ENTITY_422

            new_task = Task(
                title=form_data["title"],
                description=form_data["description"],
                creator_id=user.id,
                project_id=project.id,
                assigned_users=assigned_users_for_task,
            )
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return errors.SERVER_ERROR_500

        # response
        return {"message": "New task created successfully", "task_id": new_task.id}, errors.HTTP_SUCCESS_200

    @staticmethod
    def _get_project_if_access(user, project_id):
        # check project exists
        try:
            project = ProjectHandler.check_project_exists(project_id)
        except Exception as e:
            logger.error(e)
            raise Exception(errors.NOT_FOUND_404)

        # check if user is creator project or is one of the assigned users
        if (project.creator.id != user.id) and (user.id not in [user.id for user in project.assigned_users]):
            raise Exception(errors.PERMISSION_DENIED_403)

        return project
