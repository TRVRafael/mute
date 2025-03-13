from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from data import db_controller
from bot.utils import get_timestamp
from bot.config import bot_logger
from bot.handlers import menu_command_handler

async def muted_expression_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    expression = query.data.split("_", 1)[1]
    keyboard = [
        [InlineKeyboardButton("🔔 Desmutar", callback_data=f"unmute_{expression}")]
    ]

    affecteded_list = db_controller.get_affected(expression)
    for affect in affecteded_list:
        keyboard.append([InlineKeyboardButton(f"{affect[0]}", callback_data=f"afct_{expression}_{affect[0]}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Voltar ao menu", callback_data="menu")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    responsable_info = db_controller.get_expression_responsable(expression)[0]
    responsable_username = responsable_info[0]
    timestamp = responsable_info[1]
    await query.edit_message_text(f"<b>Lista de pessoas banidas por usarem '{expression}':</b>\n<i>(Clique para ver as informações do usuário)\n\n<b>-- Adicionais --</b>\n👤 Responsável: {responsable_username}\n⏰Timestamp: {timestamp}</i>", parse_mode="HTML", reply_markup=reply_markup)
    
async def affected_user_info(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    expression = query.data.split("_")[1]
    affected = query.data.split("_")[2]
    
    affected_user = db_controller.get_affected_info(expression, affected)[0]
    affected_user_username = affected_user[0]
    affected_user_message = affected_user[1]
    affected_user_timestamp = affected_user[2]
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar ao menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"<b><i>Informações:\n\n👤 Nickname: {affected_user_username}\n💬 Mensagem enviada: {affected_user_message}\n⏰Timestamp: {affected_user_timestamp}</i></b>", parse_mode="HTML", reply_markup=reply_markup)
    
async def muted_expressions_list(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    muted_expressions = db_controller.get_muted_expressions()
    
    for expr in muted_expressions:
        word = expr[0]  # Pegando o primeiro elemento da tupla
        keyboard.append([InlineKeyboardButton(f"{word}", callback_data=f"wrd_{word}")])
    
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("<b>Lista de palavras bloqueadas atualmente:</b>", reply_markup=reply_markup, parse_mode="HTML")
    
async def unmute_expression(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    expression = query.data.split("_", 1)[1]
    db_controller.remove_muted_expression(query.from_user.username, expression, get_timestamp())
    bot_logger.info(f"Unmuted {expression}. By: {query.from_user.username}")
    await query.edit_message_text(f"Palavra '{expression}' desmutada.")
    
async def expression_record(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
async def back_menu(update: Update, context: CallbackContext):
    await menu_command_handler(update, context)
    