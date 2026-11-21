import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
import tempfile

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا! أرسلي أي نص وأحوله لك فيديو")

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("جاري صنع الفيديو... ⏳")
    try:
        duration = 5
        bg = ColorClip(size=(1080, 1920), color=(0,0,0), duration=duration)
        txt = TextClip(text, fontsize=70, color='white', method='caption', size=(900, None))
        txt = txt.set_position('center').set_duration(duration)
        final = CompositeVideoClip([bg, txt])
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            path = f.name
        final.write_videofile(path, fps=24, codec='libx264', verbose=False, logger=None)
        await update.message.reply_video(video=open(path, 'rb'))
        os.unlink(path)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_video))
app.run_polling()
