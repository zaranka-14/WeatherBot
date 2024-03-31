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
    if len(line) != 5:
        return False, 0, 0
    if line[0].isnumeric() and line[1].isnumeric():
        x = line[0:2]
    else:
        return False, 0, 0
    line.removeprefix(x)
    if line[0] != ':':
        return False, 0, 0
    else:
        line.removeprefix(':')
    if line[0].isnumeric() and line[1].isnumeric():
        y = line[0:2]
    else:
        return False, 0, 0
    if int(x) >= 30 or int(y) >= 30:
        return False, int(x), int(y)
    return True, int(x), int(y)


@router.message(StateFilter(ChoosePlaceAndDay.coordinates))
async def choose_coordinate(message: Message, state: FSMContext):
    correction, x, y = await correct_input(message.text)
    if correction:
        await message.answer(
            text=f"Отлично, выбранные координаты: {x}:{y}\n"
            "Теперь нажатием на кнопку выберите день",
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


@router.callback_query(StateFilter(ChoosePlaceAndDay.day), F.data.in_(available_day_callback))
async def choose_day(callback: CallbackQuery, state: FSMContext):
    day = int(callback.data)
    x_y_dict = await state.get_data()
    x = x_y_dict["x_value"]
    y = x_y_dict["y_value"]
    info = get_info(x, y, day)

    await callback.message.edit_text(
        text=f"Всё, что известно об этом месте на {day} день:\n"
             f"Высоты над уровнем моря в метрах: {info['elevation']}\n"
             f"Температура воздуха (С): {info['temperature']}\n"
             f"Атмосферное давление (hPa): {info['pressure']}\n"
             f"Влажность в %: {info['humidity']}\n"
             f"Скорость ветра (км/ч): {info['wind_speed']}\n"
             f"Направление ветра (в градусах): {info['wind_dir']}\n"
             f"Облачность (в процентах): {info['cloud_cover']}\n"
             "Для получения информации о новой точке начните работу заново при помощи /start"
    )
    await state.clear()
