from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackContext, CommandHandler, CallbackQueryHandler

from bot.config import BOT_TOKEN, bot_logger
from bot.handlers import mute_command_handler, unmute_command_handler, menu_command_handler, muted_expression_query_handler, affected_user_info, muted_expressions_list, unmute_expression, back_menu

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("mute", mute_command_handler))
    app.add_handler(CommandHandler("unmute", unmute_command_handler, has_args=1))
    app.add_handler(CommandHandler("menu", menu_command_handler, has_args=False))
    
    app.add_handler(CallbackQueryHandler(muted_expression_query_handler, pattern=r"wrd_.*"))
    app.add_handler(CallbackQueryHandler(affected_user_info, pattern=r"afct_.*"))
    app.add_handler(CallbackQueryHandler(muted_expressions_list, pattern=r"^muted$"))
    app.add_handler(CallbackQueryHandler(unmute_expression, pattern=r"unmute_.*"))
    app.add_handler(CallbackQueryHandler(back_menu, pattern=r"^menu$"))
    
    
    app.run_polling()
    bot_logger.info("Bot running...")
    
    