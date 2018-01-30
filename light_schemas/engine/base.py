from django.db.backends.postgresql.base import DatabaseWrapper
from .introspection import SchemaDatabaseIntrospection  # NOQA isort:skip
from .schema import SchemaDatabaseSchemaEditor  # NOQA isort:skip


class DatabaseWrapper(DatabaseWrapper):

    SchemaEditorClass = SchemaDatabaseSchemaEditor

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.introspection = SchemaDatabaseIntrospection(self)
