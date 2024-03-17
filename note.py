import telebot
from telebot import types

API_TOKEN = '7196577274:AAEkvQDi-mkQ3jJuhoYjK5tsjWm8f-lxJws'
bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store notes
notes = {}

# Start command with a custom keyboard
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('/newnote', '/mynotes', '/deletenote')
    bot.send_message(message.chat.id, "Welcome to your note-taking bot. Choose an option:", reply_markup=markup)

# Command handler to create a new note
@bot.message_handler(commands=['newnote'])
def new_note(message):
    msg = bot.send_message(message.chat.id, 'What would you like to note down?')
    bot.register_next_step_handler(msg, save_note)

# Function to save the note
def save_note(message):
    note_id = str(len(notes) + 1)
    notes[note_id] = message.text
    bot.send_message(message.chat.id, f'Note saved! ID: {note_id}')

# Command handler to view all notes
@bot.message_handler(commands=['mynotes'])
def my_notes(message):
    if not notes:
        bot.send_message(message.chat.id, 'You have no notes.')
    else:
        response = 'Your notes:\n'
        for note_id, note in notes.items():
            response += f'{note_id}: {note}\n'
        bot.send_message(message.chat.id, response)

# Command handler to delete a note
@bot.message_handler(commands=['deletenote'])
def delete_note(message):
    if not notes:
        bot.send_message(message.chat.id, 'You have no notes to delete.')
    else:
        msg = bot.send_message(message.chat.id, 'Enter the ID of the note you want to delete:')
        bot.register_next_step_handler(msg, perform_delete)

# Function to perform the deletion of a note
def perform_delete(message):
    note_id = message.text
    if note_id in notes:
        del notes[note_id]
        bot.send_message(message.chat.id, f'Note {note_id} deleted.')
    else:
        bot.send_message(message.chat.id, 'Note ID not found.')

# Error handling
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "I didn't understand that. Try /start to see available commands.")

# Polling
bot.polling()
