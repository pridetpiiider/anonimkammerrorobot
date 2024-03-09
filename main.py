import logging, config
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=config.token, parse_mode="html")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class User(StatesGroup):
    text = State()
    userId = State()

@dp.message_handler(commands=['start'])
async def handlerStart(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args:
       if int(args) == message.from_user.id:
          await message.answer("⛔️ Извините, но вы не можете задать вопрос самому себе.")
          return

       await message.answer("Через этого бота ты можешь задать вопрос человеку, который опубликовал эту ссылку.\n\nНапиши свой вопрос:") 
       await state.update_data(userId=args)
       await User.text.set()

    else:
       await message.answer(f"<b>🔗 Вот твоя личная ссылка:</b>\n\nt.me/{config.name}?start={message.from_user.id}\n\nОпубликуй её и получай анонимные вопросы")

@dp.message_handler(state=User.text)
async def stateText(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.send_message(data["userId"], f"<b>Получен новый вопрос!</b>\n\n{message.text}\n\n(<a href='t.me/{config.name}?start={message.from_user.id}'>Ответить</a>)")
        await message.answer(f"☑️ Твой вопрос успешно отправлен, дождись ответа!\n\nА пока ты ждёшь...\n\n<b>🔗 Вот твоя личная ссылка:</b>\n\nhttp://t.me/{config.name}?start={message.from_user.id}\n\nОпубликуй её и получай анонимные вопросы")
        await state.finish()

    except:
        await message.answer("⛔ Данный пользователь не пользуется этим ботом.")
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)