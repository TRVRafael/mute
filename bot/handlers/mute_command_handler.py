from telegram import Update
from telegram.ext import CallbackContext

from data import db_controller
from bot.utils import get_timestamp
from bot.config import bot_logger

async def mute_command_handler(update : Update, context : CallbackContext):
    args = context.args
    muted_expression = " ".join(args)
    db_controller.insert_muted_expression(update.effective_user.username, muted_expression, get_timestamp())
    bot_logger.info(f"Command /mute used by {update.effective_user.username}. Added {muted_expression} to database")
    await update.message.reply_text("Palavra bloqueada.")
    
    
async def unmute_command_handler(update : Update, context : CallbackContext):
    args = context.args
    db_controller.remove_muted_expression(update.effective_user.username, args[0], get_timestamp())
    bot_logger.info(f"Command /unmute used by {update.effective_user.username}. Removed {args[0]} from database")
    await update.message.reply_text("Palavra desbloqueada.")