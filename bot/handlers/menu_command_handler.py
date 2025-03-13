from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from data import db_controller

async def menu_command_handler(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🔇 Palavras bloqueadas", callback_data="muted")],
        [InlineKeyboardButton("📖 Histórico", callback_data="historico")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            "<b>Selecione a opção desejada abaixo.</b>", 
            reply_markup=reply_markup, 
            parse_mode="HTML"
        )
    else:  # Se for um comando /menu
        await update.message.reply_text(
            "<b>Selecione a opção desejada abaixo.</b>", 
            reply_markup=reply_markup, 
            parse_mode="HTML"
        )