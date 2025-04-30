import os, csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
CSV_FILE = 'report.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["日期", "銀行", "收入", "介紹人", "介紹費", "實拿"])

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bank, income, referrer, fee = update.message.text.strip().split()
        income, fee = float(income), float(fee)
        net = income - fee
    except:
        await update.message.reply_text("請用格式：銀行 收入 介紹人 介紹費\n例如：玉山 5000 小明 200")
        return

    row = [datetime.now().strftime("%Y-%m-%d"), bank, income, referrer, fee, net]
    with open(CSV_FILE, 'a', newline='') as f:
        csv.writer(f).writerow(row)

    await update.message.reply_text(f"✅ 記錄成功\n銀行：{bank}\n收入：{income}\n介紹人：{referrer}\n介紹費：{fee}\n實拿：{net}")

def main():
    init_csv()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
