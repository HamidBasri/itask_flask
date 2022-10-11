from api.config.loader import marshmallow as ma
import marshmallow.validate as validate

from api.components.projects.model import Project
from ..users.schema import UserSchema


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True

    id: ma.auto_field()
    creator = ma.Nested(UserSchema(only=("id", "username", "email")), dump_only=True)
    assigned_users = ma.Nested(UserSchema(only=("id", "username", "email")), dump_only=True, many=True)


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


class NewProjectSchema(ma.Schema):
    title = ma.Str(required=True, valdiate=validate.Length(max=100))
    description = ma.Str(required=True, valdiate=validate.Length(max=1000))
    assigned_users = ma.List(ma.Int())
