from flask import request, jsonify
from flask_restful import Resource
import logging
from api.config.auth import create_token
from api.utils import errors
from api.components.users.model import User, Role
from api.config.loader import db
from api.components.users.schema import user_schema


class Register(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            username, password, email, roles = (
                request.json.get("username").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
                request.json.get("roles"),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return errors.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or password is None or email is None or roles is None:
            return errors.INVALID_INPUT_422

        valid_roles = [role.name for role in Role.query.all()]
        if not all([role in valid_roles for role in roles]):
            logging.info("Invalid Roles" + str(roles))
            return errors.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return errors.ALREADY_EXIST

        # Create a new user.
        user = User(username=username, password=password, email=email)

        for role in roles:
            user.roles.append(Role.query.filter_by(name=role).first())

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {"status": "registration completed."}


class Login(Resource):
    @staticmethod
    def post():

        try:
            # Get user email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return errors.INVALID_INPUT_422

        # Check if user information is none.
        if email is None or password is None:
            return errors.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is not existed.
        if user is None:
            return errors.UNAUTHORIZED

        # Check password.
        if not user.verify_password(password):
            return errors.UNAUTHORIZED

        token = create_token(user.id)

        return jsonify({"token": token})
