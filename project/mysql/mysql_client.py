import sqlalchemy
from mysql.models.models import UserModel
from sqlalchemy.orm import sessionmaker


class MysqlClient:

    def __init__(self, host, port, db_name, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def _execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def insert_user(self, name, surname, middle_name, username, password, email, access=1, active=1,
                    start_active_time=None):
        user = UserModel(
            name=name,
            surname=surname,
            middle_name=middle_name,
            username=username,
            password=password,
            email=email,
            access=access,
            active=active,
            start_active_time=start_active_time
        )

        self.session.add(user)
        self.session.commit()

        return user

    def select_user(self, username):
        res = self.session.query(UserModel).filter_by(username=username).first()
        return res

    def delete_user(self, username):
        self.session.query(UserModel).filter_by(username=username).delete()
        self.session.commit()

    def update_user(self, username, **kwargs):
        user = self.select_user(username)

        for k, v in kwargs.items():
            if k == 'active':
                user.active = v
            elif k == 'access':
                user.access = v

        self.session.commit()
