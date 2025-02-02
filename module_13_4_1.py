from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = ''


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Напишите 'Calories', чтобы начать расчет нормы калорий.")


@dp.message_handler(lambda message: message.text.lower() == 'calories')
async def set_age(message: types.Message):
    await message.reply('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.reply('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))


    bmr = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.reply(f'Ваша норма калорий: {bmr:.2f} ккал в день.')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)