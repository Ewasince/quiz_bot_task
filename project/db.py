# импортируем классы, используемые для определения атрибутов модели
from enum import Enum
from typing import List

from sqlalchemy import Column, Integer, String, create_engine, CHAR
# объект для подключения ядро базы данных
from sqlalchemy.ext.declarative import declarative_base
# импортируем объекты для создания отношения между объектами
from sqlalchemy.orm import sessionmaker

from config import config

# создаем класс, от которого будут наследоваться модели
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    status = Column(CHAR)
    pass


# Подключение к базе данных через SQLAlchemy
engine = create_engine(f"sqlite:///{config.database_filename}")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base.metadata.create_all(engine)


class StatusEnum(Enum):
    # def __init__(self, arg):
    #     super().__init__(int(arg))
    #     pass

    ACTIVE = 'A'
    LAST_ATTEMPT = 'L'
    PASSED = 'P'
    REJECTED = 'R'

    pass


def is_exis_user(user_id: int):
    user = session.query(Users).filter_by(user_id=user_id).one_or_none()

    if user is None:
        return False
    else:
        return True

    pass


def initialize_user(user_id: int, username: str):
    artist = Users(user_id=user_id, username=username, status=StatusEnum.ACTIVE.value)
    session.add(artist)
    session.commit()
    pass


def update_user_status(user_id: int, status: StatusEnum):
    # user = session.query(Users).filter_by(user_id=user_id).update()
    user = session.query(Users).filter_by(user_id=user_id).one()

    assert user is not None, 'cant find user'

    user.status = status.value
    session.commit()

    pass


def get_user_status(user_id: int) -> StatusEnum:
    user = session.query(Users).filter_by(user_id=user_id).one()

    return StatusEnum(user.status)

    pass


def get_winners_from_db() -> List[Users]:
    users = session.query(Users).filter_by(status=StatusEnum.PASSED.value).all()

    return users
    pass


def clear_db():
    session.query(Users).delete()
    session.commit()
    pass


if __name__ == '__main__':
    test = is_exis_user(228)

    if test:
        pass
    else:
        initialize_user(228, 'pupa')
    pass
