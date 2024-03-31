from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_inline_keyboard(items: list[str], callbacks: list[str]) -> InlineKeyboardMarkup:
    buttons = []
    for index in range(len(items)):
        buttons.append([InlineKeyboardButton(text=items[index], callback_data=callbacks[index])])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
