import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("歡迎使用報帳機器人！請輸入格式：銀行 收入 介紹人 介紹費")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        parts = text.split()
        if len(parts) != 4:
            raise ValueError("輸入格式錯誤，請輸入：銀行 收入 介紹人 介紹費")
        bank, income_str, introducer, fee_str = parts
        income = int(income_str)
        fee = int(fee_str)
        net_income = income - fee
        response = (
            f"✅ 記錄成功\n"
            f"銀行：{bank}\n"
            f"收入：{income}\n"
            f"介紹人：{introducer}\n"
            f"介紹費：{fee}\n"
            f"實拿：{net_income}"
        )
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(str(e))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
