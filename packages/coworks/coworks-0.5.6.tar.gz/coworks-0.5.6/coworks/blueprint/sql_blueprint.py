import os
import sqlalchemy
from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.orm import sessionmaker

from ..coworks import Blueprint, entry


class SqlAlchemy(Blueprint):

    def __init__(self, env_dialect_var_name=None, env_port_var_name=None, env_host_var_name=None,
                 env_dbname_var_name=None, env_user_var_name=None, env_passwd_var_name=None, env_var_prefix="SQL",
                 **kwargs):
        super().__init__(name='sqlalchemy', **kwargs)
        self.dialect = self.port = self.host = self.dbname = self.user = self.password = None
        self.__session = None
        if env_var_prefix:
            self.env_dialect_var_name = f"{env_var_prefix}_DIALECT"
            self.env_port_var_name = f"{env_var_prefix}_PORT"
            self.env_host_var_name = f"{env_var_prefix}_HOST"
            self.env_dbname_var_name = f"{env_var_prefix}_DBNAME"
            self.env_user_var_name = f"{env_var_prefix}_USER"
            self.env_passwd_var_name = f"{env_var_prefix}_PASSWD"
        else:
            self.env_dialect_var_name = env_dialect_var_name
            self.env_port_var_name = env_port_var_name
            self.env_host_var_name = env_host_var_name
            self.env_dbname_var_name = env_dbname_var_name
            self.env_user_var_name = env_user_var_name
            self.env_passwd_var_name = env_passwd_var_name

        @self.before_first_activation
        def check_env_vars(event, context):
            self.dialect = os.getenv(self.env_dialect_var_name, 'psycopg2')
            self.port = os.getenv(self.env_port_var_name, 5432)
            self.host = os.getenv(self.env_host_var_name)
            if not self.host:
                raise EnvironmentError(f'{self.env_host_var_name} not defined in environment.')
            self.dbname = os.getenv(self.env_dbname_var_name)
            if not self.dbname:
                raise EnvironmentError(f'{self.env_dbname_var_name} not defined in environment.')
            self.user = os.getenv(self.env_user_var_name)
            if not self.user:
                raise EnvironmentError(f'{self.env_user_var_name} not defined in environment.')
            self.passwd = os.getenv(self.env_passwd_var_name)
            if not self.passwd:
                raise EnvironmentError(f'{self.env_passwd_var_name} not defined in environment.')

        @self.before_activation
        def begin_session(event, context):
            self.session.begin()

        @self.after_activation
        def commit_session(event, context):
            self.session.commit()

        @self.handle_exception
        def rollback_session(event, context):
            self.session.rollback()

    @property
    def session(self):
        if not self.__session:
            engine = create_engine(
                f'{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}', echo=False
            )
            self.__session = sessionmaker(bind=engine)()
        return self.__session

    @entry
    def get_version(self):
        """Returns SQLAlchemy version."""
        return sqlalchemy.__version__, {'content-type': 'text/plain'}

    def get_fetch(self, query: str = None, **kwargs):
        rows = self.session.execute(text(query), **kwargs).fetchall()
        return [dict(row) for row in rows]

    def reflect_tables(self, schema, tables):
        engine = self.session.get_bind()
        metadata = MetaData(bind=engine)
        return list(
            map(lambda table: Table(table, metadata, autoload=True, autoload_with=engine, schema=schema), tables))
