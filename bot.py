#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser 

'''reading config file'''

configParser = configparser.ConfigParser()   
configParser.read('config.ini')





'''importing data from config file'''
api_key = configParser.get('BOTAPI', 'API_KEY')

name = configParser.get('MyInfo', 'name')
institution = configParser.get('MyInfo', 'institution')
degree = configParser.get('MyInfo', 'degree')
year = configParser.get('MyInfo', 'year')
dept = configParser.get('MyInfo', 'dept')
country = configParser.get('MyInfo', 'country')


phone = configParser.get('contacts', 'phone')
discord = configParser.get('contacts', 'discord')
mail = configParser.get('contacts', 'mail')
linkedin = configParser.get('contacts', 'linkedin')
youtube = configParser.get('contacts', 'youtube')
github = configParser.get('contacts', 'github')
myblog = configParser.get('contacts', 'myblog')



# Enable logging in the backend
logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




def start(update, context):
    update.message.reply_text(f'Hi and welcome! I am {name}.\nWell, actually I am a bot. blip. blup.\nWhatever, My dev completed his {degree} in {dept} from {institution}, {country}. \n\nTo know more about him or get in touch with him please enter /contact.\n\nFor more please enter /help or /tools')

def contact(update, context):
    update.message.reply_text(f'If you want to know him better or have any query you can contact him:\nPhone: {phone}\nDiscord: {discord}\nMail: {mail}\nLinkedIn: {linkedin}\nYoutube: {youtube}\nGithub: {github}\nMyblog: {myblog}\n\nNot sure what to do? use /help or /tools.')


def help(update, context):
    update.message.reply_text('This is a bot. Enter the commands as needed:\n/about to know about me\n/help print this help message\n/tools to see available tools and their usage')


def tools(update, context):
    update.message.reply_text('Available tools:\nUse /set <seconds> to set a timer\nUse /unset to cancel any existing timer')




def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(api_key, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("contact", contact))

    dp.add_handler(CommandHandler("tools", tools))
    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("unset", unset))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
