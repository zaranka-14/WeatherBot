import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from keyboards.making_keyboards import make_inline_keyboard
from dicts_and_strings import available_day, available_day_callback, get_info

router = Router()


class ChoosePlaceAndDay(StatesGroup):
    coordinates = State()
    day = State()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ChoosePlaceAndDay.coordinates)
    await message.answer(
        text="Привет, это метеорологический бот.\n"
             "Для выбора координаты напиши сообщение в формате XX:YY, например 01:29.\n"
             "Координаты могут быть от 0 до 29!"
    )


async def correct_input(line: str) -> (bool, int, int):
    if ":" not in line:
        return False, 0, 0
    x, y = line.split(":")
    if (int(x) >= 30 or int(y) >= 30) or (int(x) < 0 or int(y) < 0):
        return False, 0, 0
    return True, x, y


@router.message(StateFilter(ChoosePlaceAndDay.coordinates))
async def choose_coordinate(message: Message, state: FSMContext):
    correction, x, y = await correct_input(message.text)
    if correction:
        await message.answer(
            text=f"Отлично, выбранные координаты: {x}:{y}\n"
                 "Теперь нажатием на кнопку выберите час",
            reply_markup=make_inline_keyboard(available_day, available_day_callback)
        )
        await state.update_data(x_value=x, y_value=y)
        await state.set_state(ChoosePlaceAndDay.day)
    else:
        await message.answer(
            text="Что-то пошло не так, вы уверены, что ввели координаты в формате XX:YY?\n"
                 "Пример: 09:28, координаты могут принимать значения от 0 до 29."
        )
        await state.set_state(ChoosePlaceAndDay.coordinates)


def degree_to_dir(degree: float):
    if 355 >= degree >= 15:
        return "Восток"
    elif 15 > degree > 85:
        return "Северо-Восток"
    elif 85 < degree <= 95:
        return "Север"
    elif 95 < degree < 175:
        return "Северо-Запад"
    elif 175 <= degree <= 185:
        return "Запад"
    elif 185 < degree < 265:
        return "Юго-Запад"
    elif 265 <= degree <= 275:
        return "Юг"
    else:
        return "Юго-Восток"


@router.callback_query(StateFilter(ChoosePlaceAndDay.day),
                       F.data.in_(available_day_callback))
async def choose_day(callback: CallbackQuery, state: FSMContext):
    day = callback.data
    x_y_dict = await state.get_data()
    x = x_y_dict["x_value"]
    y = x_y_dict["y_value"]
    info = await get_info(int(x), int(y), int(day.split("_")[1]))

    await callback.message.edit_text(
        text=f"Всё, что известно об этом месте на {int(day.split('_')[1])} час:\n\n"
             f"Высоты над уровнем моря в метрах: {info['elevation'].to_list()[0]}\n"
             f"Температура воздуха: {round(info['temperature'].to_list()[0], 2)}°C\n"
             f"Атмосферное давление: {round(info['pressure'].to_list()[0], 2)} hpa\n"
             f"Влажность: {round(info['humidity'].to_list()[0], 2)}%\n"
             f"Скорость ветра: {round(info['wind_speed'].to_list()[0], 2)} км/ч\n"
             f"Направление ветра: {degree_to_dir(info['wind_dir'].to_list()[0])}\n"
             f"Облачность: {round(info['cloud_cover'].to_list()[0], 2)}%\n\n"
             "Для получения информации о новой точке начните работу заново при помощи "
             "/start"
    )
    await state.clear()
