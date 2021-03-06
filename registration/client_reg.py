
from bot_create import dp, bot, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.db import MasterData
from keyboards import main_keyboard, sendAdmin_keyboard



class UserInfo(StatesGroup):
    sticker = State()
    photo=State()
    

class Photography(UserInfo):

    async def send_photo(message: types.Message, state:FSMContext):
        data = await state.get_data()
        await bot.send_message(chat_id=message.from_user.id, text=LANGUAGE[data['lang']]['SendSticker'], reply_markup=types.ReplyKeyboardRemove())
        await UserInfo.sticker.set()

    @dp.message_handler(content_types='photo',state=UserInfo.sticker)
    async def __get_sticker(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await state.update_data(photo_sticker = message.photo[-1].file_id)
        await message.answer(LANGUAGE[data['lang']]['PhotoKot'])
        await UserInfo.photo.set()
    
    @dp.message_handler(content_types='photo', state=UserInfo.photo)
    async def get_photo(message: types.Message, state:FSMContext):
        await state.update_data(photo = message.photo[-1].file_id)
        master_data = MasterData.get_master(message.from_user.id)
        data = await state.get_data()
        caption = f'''{LANGUAGE[data['lang']]['Master']} {master_data[1]}\n{LANGUAGE[data['lang']]['MasterPhone']} {master_data[2]}'''
        await bot.send_photo('-1001630122577', data['photo_sticker'], caption=caption)
        await bot.send_photo('-1001630122577', data['photo'], caption=caption, reply_markup=await sendAdmin_keyboard(message.from_user.id,data["lang"]))
        await main_keyboard(message, state)
        await state.reset_state(with_data=False)

    @dp.callback_query_handler(regexp='(.+)-(.+)-(.+)')
    async def accept(call: types.CallbackQuery):
        callback = call.data.split('-')
        master_info = MasterData.get_master(callback[1])
        caption = f'''{LANGUAGE['У́збекча']['Master']} {master_info[1]}\n{LANGUAGE['У́збекча']['MasterPhone']} {master_info[2]}'''
        if callback[0] == 'Accept':
            MasterData.update_master_point(callback[1])
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourAccepted'])
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Accepted"]}')
        elif callback[0] == 'Decline':
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourDecline'])
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Declined"]}')
        await call.answer()

            
        
        
            
            
            
