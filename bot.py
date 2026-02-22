import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# আপনার প্রদান করা API টোকেন
TOKEN = '8508284133:AAHzxqRn20yIlToOnbRcl5IzYhokrj8F_0w'

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"📟 স্বাগতম {user_name}!\nআমি একটি সাইবার ডাউনলোডার বট। আমাকে যেকোনো ভিডিও লিঙ্ক পাঠান, আমি সেটি এক্সট্রাক্ট করে দিচ্ছি।")

# ভিডিও ডাউনলোড এবং সেন্ডিং লজিক
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    status_msg = await update.message.reply_text("📡 সিগন্যাল রিসিভড... ডেটা প্যাকেজ ডাউনলোড হচ্ছে...")

    # ফাইলের নাম ঠিক করা
    video_file = f"video_{chat_id}.mp4"

    try:
        # ডাউনলোড কনফিগারেশন
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_file,
            'max_filesize': 50 * 1024 * 1024, # টেলিগ্রাম বট লিমিট ৫০ এমবি
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [url])

        await status_msg.edit_text("📤 ডাউনলোড কমপ্লিট। এবার আপনার কাছে ফাইলটি ট্রান্সফার করা হচ্ছে...")

        # ভিডিও পাঠানো
        with open(video_file, 'rb') as video:
            await context.bot.send_video(
                chat_id=chat_id, 
                video=video, 
                caption="📟 মিশন সাকসেসফুল। আপনার ডেটা এখানে।"
            )
        
        # পিসি থেকে ফাইল ডিলিট করা
        os.remove(video_file)

    except Exception as e:
        await status_msg.edit_text(f"❌ এরর: সিস্টেম ফাইলটি প্রসেস করতে পারেনি। (ফাইলটি বড় হতে পারে বা লিঙ্কটি ইনভ্যালিড)")
        if os.path.exists(video_file):
            os.remove(video_file)

if __name__ == '__main__':
    # বট অ্যাপ্লিকেশন বিল্ড করা
    app = ApplicationBuilder().token(TOKEN).build()
    
    # হ্যান্ডলার যুক্ত করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_video))

    print("--- [ বটের সিস্টেম এখন অনলাইন ] ---")
    app.run_polling()
