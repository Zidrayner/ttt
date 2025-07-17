import os

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, PreCheckoutQuery
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from utils.constant import PRICE
from keyboards.fsm_kb import make_fsm_kb

fsm_router = Router()

room_chs = ['Обычный', 'Люксовый', 'Президентский']

class ReservState(StatesGroup):
    time = State()
    num = State()
    room = State()
    email = State()
    all_inclusive = State()


@fsm_router.message(StateFilter(None), Command('cancel'))
@fsm_router.message(default_state, F.text.lower() == 'отмена')
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer('Нечего удалять', reply_markup=ReplyKeyboardRemove())


@fsm_router.message(Command('cancel'))
@fsm_router.message(F.text.lower() == 'отмена')
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Данные очищены', reply_markup=ReplyKeyboardRemove())


@fsm_router.message(Command('book'))
async def get_name(message: Message, state: FSMContext):
    await state.set_state(ReservState.time)
    await message.answer('Выберите дату для бронирования.')


@fsm_router.message(ReservState.time)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer('Сколько человек будет на бронировании?')
    await state.set_state(ReservState.num)


@fsm_router.message(ReservState.num)
async def get_room(message: Message, state: FSMContext):
    await state.update_data(num=message.text)
    await message.answer('Хотите выбрать место около окна?', reply_markup=make_fsm_kb(room_chs))
    await state.set_state(ReservState.room)




@fsm_router.message(ReservState.room)
async def payment_handler(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    data = await state.get_data()
    await message.answer(f'Бронь:\n'
                         f'Дата: {data["time"]}\n'
                         f'Количество человек: {data["num"]}\n'
                         f'Место у окна: {data["room"]}')
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title='Бронь',
        description=f'Оплатите бронь',
        payload='premium-access',
        provider_token=os.getenv('PAYMENT_TOKEN'),
        currency='RUB',
        prices=PRICE,
    )
    await state.clear()

@fsm_router.pre_checkout_query()
async def checkout_handler(query: PreCheckoutQuery):
    print(query.invoice_payload)
    await query.answer(ok=True)


@fsm_router.message(lambda message: message.successful_payment is not None)
async def success_payment(message: Message):

    await message.answer('Спасибо что выбрали нас❤️❤️❤️')