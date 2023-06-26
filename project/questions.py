from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    question: str
    options: List[str]
    true_option: int
    time: int

    pass


questions: List[Question] = [
    Question('Вопрос 1', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    Question('Вопрос 2', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    Question('Вопрос 3', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    Question('Вопрос 4', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    Question('Вопрос 5', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    # Question('Вопрос 6', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
    # Question('Вопрос 7', ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'], 1, 15),
]
