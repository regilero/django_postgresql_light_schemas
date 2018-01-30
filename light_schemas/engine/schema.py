from django.db.backends.postgresql.schema import DatabaseSchemaEditor


class SchemaDatabaseSchemaEditor(DatabaseSchemaEditor):

    def _create_fk_sql(self, model, field, suffix):
        """Support of our hackish foo\".\"bar table names on FK.

        Base copy/paste of base _create_fk_sql with character replacement added
        """
        from_table = model._meta.db_table
        from_column = field.column
        to_table = field.target_field.model._meta.db_table
        to_column = field.target_field.column
        suffix = suffix % {
            "to_table": to_table.replace('"."', "__"),
            "to_column": to_column.replace('"."', "__"),
        }

        return self.sql_create_fk % {
            "table": self.quote_name(from_table),
            "name": self.quote_name(self._create_index_name(
                model, [from_column], suffix=suffix)),
            "column": self.quote_name(from_column),
            "to_table": self.quote_name(to_table),
            "to_column": self.quote_name(to_column),
            "deferrable": self.connection.ops.deferrable_sql(),
        }
