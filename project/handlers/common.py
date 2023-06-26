import time
from typing import List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import config
from db import is_exis_user, initialize_user, get_user_status, StatusEnum, update_user_status, get_winners_from_db, \
    clear_db
from keyboards.main_menu import start_markup, inline_btn_menu
from questions import questions
from states import States

router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
        start command hadler
    """
    await state.clear()
    await state.set_state(States.default_state)

    user_id = message.from_user.id
    is_exist_user = is_exis_user(user_id)

    if not is_exist_user:
        user_username = message.from_user.username
        initialize_user(user_id, user_username)
        pass

    user_status = get_user_status(user_id)

    if user_status == StatusEnum.REJECTED or user_status == StatusEnum.PASSED:
        await message.answer(
            f"Привет, <b>{message.from_user.full_name}</b>! Ты уже прошёл викторину, так что до новый встреч!")
    elif user_status == StatusEnum.ACTIVE:
        await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Меня зовут {config.bot_name}!"
                             f" У меня ты можешь принять участие в розыгрыше, "
                             f"если ответишь на {len(questions)} несложных вопросов😉",
                             reply_markup=start_markup)
    elif user_status == StatusEnum.LAST_ATTEMPT:
        await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Попробуем еще раз?",
                             reply_markup=start_markup)
        pass
    pass


@router.callback_query(F.data == inline_btn_menu.callback_data)
async def process_callback_main_menu(callback_query: CallbackQuery, state: FSMContext):
    """

    """
    user_id = callback_query.from_user.id
    user_status = get_user_status(user_id)

    if user_status == StatusEnum.REJECTED or user_status == StatusEnum.PASSED:
        return

    await state.clear()
    await state.set_state(States.quiz)
    await state.update_data(question=0, true_answers=0, update_time=time.time())
    # await answer_decorator(callback_query.message, "Вопрос 1", reply_markup=question_1.options_markup)
    await question(callback_query, state)
    return


# @router.message(FindCVEGroup.quiz)
@router.callback_query(States.quiz)
# @router.callback_query(F.data.isnumeric())
async def question(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    question_num = state_data['question']
    last_time = state_data['update_time']

    if question_num != 0:
        last_question = questions[question_num - 1]

        is_time_is_out = time.time() - last_time > last_question.time
        check_time = last_question.time != 0
        is_ansfer_is_true = int(callback_query.data) == last_question.true_option

        if is_time_is_out and check_time:
            await callback_query.message.answer('Ты не успел ответить на вопрос!')
        elif is_ansfer_is_true:
            await callback_query.message.answer('Ты ответил правильно!')
            state_data['true_answers'] += 1
            pass
        else:
            await callback_query.message.answer('Ты ответил неверно(')
        pass

    await state.update_data(state_data)

    if question_num == len(questions):
        await end_quiz(callback_query, state)
        return
        pass

    question = questions[question_num]

    markup = create_markup(question.options)

    state_data['question'] += 1
    state_data['update_time'] = time.time()
    await state.update_data(state_data)

    await callback_query.message.answer(question.question, reply_markup=markup)

    # await answer_decorator()

    pass


async def end_quiz(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(States.default_state)
    state_data = await state.get_data()
    true_answers = state_data['true_answers']
    total_questions = len(questions)

    false_answers = total_questions - true_answers

    # sample_text = f'Квиз закончился! Ты ответил правильно .'

    user_id = callback_query.from_user.id
    user_status = get_user_status(user_id)

    if false_answers == 0:
        sample_text = f'Поздравляю, ты ответил правильно на все вопросы! Жди от нас сообщения'
        update_user_status(user_id, StatusEnum.PASSED)
        pass
    elif false_answers == 1:
        if user_status == StatusEnum.LAST_ATTEMPT:
            sample_text = f'Ты ответил правильно почти на все вопросы! Но, к сожалению у тебя кончились попытки😔 ' \
                          f'Приходи на следующий квиз!'
            update_user_status(user_id, StatusEnum.REJECTED)
            pass
        else:
            sample_text = f'Ты ответил правильно почти на все вопросы! Хочешь попробовать еще раз? ' \
                          f'Просто отправь мне еще раз команду /start как будешь готов'
            update_user_status(user_id, StatusEnum.LAST_ATTEMPT)
            pass

        pass
    else:
        sample_text = f'К сожалению ты ответил правильно только на {true_answers} из {total_questions} вопросов('
        update_user_status(user_id, StatusEnum.REJECTED)
        pass
    await callback_query.message.answer(sample_text)

    # await command_start_handler(callback_query, state)

    pass


# @router.message(F.from_user.id == config.admin_id and Command(commands=["winners"]))
@router.message(Command(commands=["winners"]))
async def get_winners(message: Message, state: FSMContext):
    users_winners = get_winners_from_db()
    winners_usernames = [w.username for w in users_winners]
    winners_usernames_str = '\n'.join(winners_usernames)
    await message.answer(f"Вот список победителей:\n"
                         f"{winners_usernames_str}")


@router.message(Command(commands=["clear"]))
async def clearn_db(message: Message, state: FSMContext):
    clear_db()

    await message.answer(f"База данных успешно очищена")


def create_markup(options: List[str]):
    options_buttons = []

    for n, opt_text in enumerate(options):
        button = InlineKeyboardButton(
            text=opt_text,
            callback_data=str(n)
        )
        options_buttons.append(button)
        pass

    # markups
    options_markup = InlineKeyboardMarkup(
        inline_keyboard=[options_buttons]
    )

    return options_markup
