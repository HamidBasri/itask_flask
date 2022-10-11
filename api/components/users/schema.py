from api.config.loader import marshmallow as ma


class UserSchema(ma.Schema):

    """
    User schema returns only username, email and creation time. This was used in user handlers.
    """

    # Schema parameters.
    class Meta:
        fields = ("id", "username", "email", "created")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
