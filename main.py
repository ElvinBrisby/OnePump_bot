
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# Admin ID
ADMIN_USERNAME = "@iamshokhruz"

# Bosqichlar
LANG, MENU, FORM_NAME, FORM_FULLNAME, FORM_CONTACT, CALLBACK_PHONE = range(6)

# Tillar
languages = {
    "Uz": "O'zbekcha",
    "Eng": "English",
    "Rus": "Русский"
}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Uz", "Eng", "Rus"]]
    await update.message.reply_text("Please select your language:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return LANG

# Til tanlangach
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    context.user_data["lang"] = lang
    text = {
        "Uz": "Assalomu alaykum! Quyidagi xizmatlardan birini tanlang:",
        "Eng": "Welcome! Please choose one of the services below:",
        "Rus": "Здравствуйте! Пожалуйста, выберите одну из услуг:"
    }
    keyboard = [["Apply for Fuel Card", "Request a CallBack"]]
    await update.message.reply_text(text.get(lang, "Choose option:"), reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return MENU

# Menyu tanlash
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Apply for Fuel Card":
        await update.message.reply_text("Your Company Name:")
        return FORM_NAME
    elif text == "Request a CallBack":
        await update.message.reply_text("Please enter your phone number:")
        return CALLBACK_PHONE
    else:
        await update.message.reply_text("Iltimos, menyudan birini tanlang.")
        return MENU

# Forma bosqichlari
async def get_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["company"] = update.message.text
    await update.message.reply_text("Your Full Name:")
    return FORM_FULLNAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fullname"] = update.message.text
    await update.message.reply_text("Your Contact Info (phone/email):")
    return FORM_CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text

    msg = (
        f"New Fuel Card Request:\n"
        f"Company: {context.user_data['company']}\n"
        f"Full Name: {context.user_data['fullname']}\n"
        f"Contact: {context.user_data['contact']}"
    )
    await context.bot.send_message(chat_id=ADMIN_USERNAME, text=msg)
    await update.message.reply_text("Thank you! We will contact you soon.")
    return ConversationHandler.END

# Callback raqam
async def get_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    msg = f"Callback Request:\nPhone: {phone}"
    await context.bot.send_message(chat_id=ADMIN_USERNAME, text=msg)
    await update.message.reply_text("Thank you! We will call you back soon.")
    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token("8030022815:AAHei4J7lQH-pvqbZ7uvc8svF_EJVe_v8LE").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            FORM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_company_name)],
            FORM_FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            FORM_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            CALLBACK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_callback)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()
