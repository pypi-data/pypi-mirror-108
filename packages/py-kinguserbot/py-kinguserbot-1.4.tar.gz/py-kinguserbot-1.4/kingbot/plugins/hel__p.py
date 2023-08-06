from uti.misc import paginate_modules
from pyrogram import idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , InlineQuery ,Message, CallbackQuery, InlineQueryResultPhoto
from pyrogram import filters 
from kingbot import kingbot ,setbot , vr,Adminsettings
from uti.serra import ser
import re
Admins= Adminsettings
Msge={}
@kingbot.on_message(filters.command("help",".") & filters.user(Adminsettings))
async def h_lp(_ , message):
  booet= await setbot.get_me()
  res=await kingbot.get_inline_bot_results(booet.username, "hlpin")
  mg= await kingbot.send_inline_bot_result(message.chat.id, res.query_id, res.results[0].id)
@setbot.on_inline_query(filters.regex("hlpin") & filters.user(Adminsettings))
async def in_h_lp(_ , inline_query):
  keboard= InlineKeyboardMarkup(
                  [  [
                        InlineKeyboardButton(
                            "Admin 👮",
                            callback_data= "_admin_h"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Tools 🧰",
                            callback_data= "_util_h"
                        ),
                        InlineKeyboardButton(
                            "Assistant ⚙️",
                            callback_data= "_ast_h"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Owner 🤹‍♀️",
                            callback_data= "_own_h"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
                  )]])
  await inline_query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url= "https://telegra.ph/file/040062841c541079a538c.jpg",
                title="Help",
                caption=f"You are accessing help for **King Userbot** \n __Everyone is a king. Until the real king arrives.__",
                reply_markup=keboard,
            ),
        ]
    )
def cowner(func):
        async def wrapper(_, cbq: CallbackQuery):
            if cbq.from_user.id in AdminSettings:
                pass
            else:
                userr = await setbot.get_user(Owner)
                await cbq.answer(
                    f"Only {userr.first_name} Can Access this...! Get yourself a Userbot🤘",
                    show_alert=True)
        return wrapper

@setbot.on_callback_query(filters.user(Adminsettings))
async def cbire(_ , cbq: CallbackQuery):
   HELP_COMMANDU = ser.HU
   HELP_COMMANDA = ser.HA
   HELP_COMMANDO = ser.HO
   HELP_COMMANDAST = ser.HAT
   HELP_COMMANDS = ser.HC
   print(cbq) 
   cid=cbq.id
   cdt=cbq.data
   if cdt == "_admin_h":
      keyboard = paginate_modules(0, HELP_COMMANDA, "help")
      keyboard.append([InlineKeyboardButton(
                            "Back ◀️",
                            callback_data= "b_k"
             )])
      keyboard.append([InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
             )])
      await cbq.edit_message_caption(
                            caption=f"This is the help for admin commmands to manage your group efficiently",
                            )
      await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
      return
   if cdt == "_util_h":
      keyboard = paginate_modules(0, HELP_COMMANDU, "help")
      keyboard.append([InlineKeyboardButton(
                            "Back ◀️",
                            callback_data= "b_k"
             )])
      keyboard.append([InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
             )])
      await cbq.edit_message_caption(
                            caption="This is the help for util commmands to make your life easy peasy",
                            )
      await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
      return
   if cdt == "_ast_h":
      keyboard = paginate_modules(0, HELP_COMMANDAST, "help")
      keyboard.append([InlineKeyboardButton(
                            "Back ◀️",
                            callback_data= "b_k"
             )])
      keyboard.append([InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
             )])
      await cbq.edit_message_caption(
                            caption="This is the help for assistant commmands to manage your userbot",
                            )
      await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
      return
   if cdt == "_own_h":
      keyboard =   paginate_modules(0, HELP_COMMANDO, "help")
      keyboard.append([InlineKeyboardButton(
                            "Back ◀️",
                            callback_data= "b_k"
             )])
      keyboard.append([InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
             )])
      await cbq.edit_message_caption(
                            caption="This is the help for owner commmands ",
                            )
      await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
      return
   if cdt == "b_k":
        keyboard=[[InlineKeyboardButton(
                            "Admin 👮",
                            callback_data= "_admin_h"
                        )],
                        [InlineKeyboardButton(
                            "Tools 🧰",
                            callback_data= "_util_h"
                        ),
                        InlineKeyboardButton(
                            "Assistant ⚙️",
                            callback_data= "_ast_h"
                        )],
                        [InlineKeyboardButton(
                            "Owner 🤹‍♀️",
                            callback_data= "_own_h"
                        )],
                        [InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
                  )]]
        await cbq.edit_message_caption(
                            caption=f"You are accessing help for **King Userbot** \n __Everyone is a king. Until the real king arrives.__",
                            )
        await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
        return
   if cdt == "kloz":
        await kingbot.delete_messages(chat_id=cbq.message.chat.id,message_ids=cbq.message.message_id) 
        
   HELP_COMMANDS = ser.HC 
   mod_match = re.match(r"help_module\((.+?)\)", cbq.data)
   data=cbq.data
   module=data[data.index("(")+1:len(data)-1]
   back_match = re.match(r"b_k", cbq.data)
   if mod_match:
        if module in HELP_COMMANDS:
           modulee= module
        else:
           return
        text = (
            "This is help for the plugins **{}**:\n".format(
                modulee
            )
            + HELP_COMMANDS[modulee]
        )

        await cbq.edit_message_caption(caption=text)
        await cbq.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Back ◀️",    
                            callback_data="b_k"
                        )
                    ]
                ]
            )
        )
                  

   elif back_match:
        keyboard=[[InlineKeyboardButton(
                            "Admin 👮",
                            callback_data= "_admin_h"
                        )],
                        [InlineKeyboardButton(
                            "Tools 🧰",
                            callback_data= "_util_h"
                        ),
                        InlineKeyboardButton(
                            "Assistant ⚙️",
                            callback_data= "_ast_h"
                        )],
                        [InlineKeyboardButton(
                            "Owner 🤹‍♀️",
                            callback_data= "_own_h"
                        )],
                        [InlineKeyboardButton(
                            "Close ❌",
                            callback_data= "kloz"
                  )]]
        await cbq.edit_message_caption(
                            caption=f"You are accessing help for **King Userbot** \n __Everyone is a king. Until the real king arrives.__",
                            )
        await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
   await cbq.answer()
# async def help_button_callback(_, __, query):
#     if re.match(r"help_", query.data):
#         return True


# help_button_create = filters.create(help_button_callback)
#@setbot.on_callback_query(filters.user(1359459092))
#async def help_button(_, query):  


