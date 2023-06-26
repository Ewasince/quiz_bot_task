# импортируем классы, используемые для определения атрибутов модели
from enum import Enum, auto

from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, SmallInteger, CHAR

# импортируем объекты для создания отношения между объектами
from sqlalchemy.orm import relationship, backref, sessionmaker

# объект для подключения ядро базы данных
from sqlalchemy.ext.declarative import declarative_base

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


if __name__ == '__main__':
    test = is_exis_user(228)

    if test:
        pass
    else:
        initialize_user(228, 'pupa')
    pass

#
# def main():
#     """Main entry point of program"""
#     # book = session.query(Book).filter_by(Book.title == "The Stand").one_or_none()
#     # print(f"Authors name: {book.author.first_name} {book.author.last_name}")
#     #
#     # book = session.add().filter_by(Book.title == "The Stand").one_or_none()
#     # print(f"Authors name: {book.author.first_name} {book.author.last_name}")
#
#     # Определяем число книг, изданных каждым издательством
#     books_by_publisher = get_books_by_publishers(session, ascending=False)
#     for row in books_by_publisher:
#         print(f"Publisher: {row.name}, total books: {row.total_books}")
#     print()
#
#     # Определяем число авторов у каждого издательства
#     authors_by_publisher = get_authors_by_publishers(session)
#     for row in authors_by_publisher:
#         print(f"Publisher: {row.name}, total authors: {row.total_authors}")
#     print()
#
#     # Иерархический вывод данных
#     authors = get_authors(session)
#     output_author_hierarchy(authors)
#
#     # Добавляем новую книгу
#     add_new_book(
#         session,
#         author_name="Stephen King",
#         book_title="The Stand",
#         publisher_name="Random House",
#     )
#
#     # Вывод обновленных сведений
#     authors = get_authors(session)
#     output_author_hierarchy(authors)
