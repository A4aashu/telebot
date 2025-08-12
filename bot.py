from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
from pyzbar.pyzbar import decode

import os

# Replace with your bot's token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles messages containing photos."""
    
    # Check if the message has a photo
    if not update.message.photo:
        return

    # Download the photo
    photo_file = await update.message.photo[-1].get_file()
    
    # Save the photo to a temporary file
    await photo_file.download_to_drive("temp_photo.jpg")
    
    try:
        # Open the image and decode for QR codes
        image = Image.open("temp_photo.jpg")
        decoded_objects = decode(image)

        # Check if a QR code was found
        if decoded_objects:
            print("QR code detected!")
            
            # Get the sender's user ID
            user_id = update.message.from_user.id
            
            # Check if the user is an admin
            is_admin = await is_user_admin(update.effective_chat.id, user_id, context)

            if not is_admin:
                print("Sender is not an admin. Deleting message.")
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
            else:
                print("Sender is an admin. Message allowed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
async def is_user_admin(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Checks if a user is a group admin."""
    
    # Get a list of all admins in the chat
    admins = await context.bot.get_chat_administrators(chat_id=chat_id)
    
    # Check if the user ID is in the list of admin IDs
    admin_ids = [admin.user.id for admin in admins]
    return user_id in admin_ids

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register the photo message handler
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo_message))

    # Start the bot
    print("Bot started. Listening for messages...")
    application.run_polling()

if __name__ == "__main__":
    main()