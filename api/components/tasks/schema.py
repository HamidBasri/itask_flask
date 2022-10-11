from api.config.loader import marshmallow as ma
import marshmallow.validate as validate

from api.components.tasks.model import Task
from ..users.schema import UserSchema
from ..projects.schema import ProjectSchema


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    id: ma.auto_field()
    creator = ma.Nested(UserSchema(only=("id", "username", "email")), dump_only=True)
    assigned_users = ma.Nested(UserSchema(only=("id", "username", "email")), dump_only=True, many=True)
    for_project = ma.Nested(ProjectSchema(exclude=("assigned_users",)), dump_only=True)


class InputTaskSchema(ma.Schema):
    title = ma.Str(required=True, valdiate=validate.Length(max=100))
    description = ma.Str(required=True, valdiate=validate.Length(max=1000))
    assigned_users = ma.List(ma.Int())
