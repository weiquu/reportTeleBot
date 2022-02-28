from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

numQuestions = 3

repliesReport1 = {
    1: "taking your info... first question: (type any ans pls)",
    2: "u r 1, moving on to q2: (type any ans pls)",
    3: "u r 2, moving on to q3: (type any ans pls)",
    4: "u r 3, and r done"
}

repliesReport2 = {
    1: "taking your info... first question: (type any ans pls)",
    2: "u r 1, moving on to q2: (type any ans pls)",
    3: "u r 2, moving on to q3: (type any ans pls)",
    4: "u r 3, and r done"
}

replies = {
    "1": repliesReport1,
    "2": repliesReport2
}

# state = -1 means new report, no info at all
# state = 0 means report type has been asked, ready to ask first question
# state = i means question i has been asked, ready to ask question i + 1
userState = {}

# [0] contains report type, [i] contains info for question i
userReplies = {}

def createReport1(chat_id):
    yourInfo = "Q1: " + userReplies[chat_id][1] + "\nQ2: " + userReplies[chat_id][2] + "\nQ3: " + userReplies[chat_id][3]
    return "report1\n" + yourInfo

def createReport2(chat_id):
    yourInfo = "Q1: " + userReplies[chat_id][1] + "\nQ2: " + userReplies[chat_id][2] + "\nQ3: " + userReplies[chat_id][3]
    return "report2:\n" + yourInfo  

# helps to dispatch which report format to use
reportDispatcher = {
    "1": createReport1,
    "2": createReport2
}

# starts a new report
# note that this clears all previous answers
def startHandler(update, context):
    # TODO: confirm start new report

    chat_id = update.message.chat_id
    userReplies[chat_id] = {}
    userState[chat_id] = 0

    update.message.reply_text("what report type: ")

def helpHandler(update, context):
    update.message.reply_text("to start a new report, use /start\n to restart midway through, use /start as well!!\n reviewing and changing answers gimme a while")

def collectInfo(chat_id, i, ans):
    userReplies[chat_id][i] = ans
    userState[chat_id] += 1

def collectReportType(chat_id, ans):
    # TODO: checking
    userReplies[chat_id][0] = ans 
    userState[chat_id] += 1  

def infoHandler(update, context):
    chat_id = update.message.chat_id

    if (chat_id not in userReplies or chat_id not in userState or userState[chat_id] == -1): # report not yet started
        update.message.reply_text("pls start a new session with /start to generate a report")
        
    elif (userState[chat_id] == 0): # answer is the report type, ready to ask first question
        collectReportType(chat_id, update.message.text)
        userReplies[chat_id][0] = update.message.text 
        update.message.reply_text(replies[userReplies[chat_id][0]][userState[chat_id]])

    elif (userState[chat_id] >= 1 and userState[chat_id] < numQuestions): # report is in progress
        collectInfo(chat_id, userState[chat_id], update.message.text)
        update.message.reply_text(replies[userReplies[chat_id][0]][userState[chat_id]])

    elif (userState[chat_id] == numQuestions): # report has ended
        userReplies[chat_id][numQuestions] = update.message.text
        update.message.reply_text(replies[userReplies[chat_id][0]][userState[chat_id]+1])
        update.message.reply_text(reportDispatcher[userReplies[chat_id][0]](chat_id))
        userState[chat_id] = -1

    else: # code should never reach here
        userState[chat_id] = -1
        update.message.reply_text("uhhh we resetting ur status sorry\npls type /start")

def main():
    # Get bot's token
    token = ""
    with open("token.txt" , "r") as s:
        for line in s:
            token = line.rstrip()

    # Create the Updater and pass it your bot's token.
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handler for commands
    dp.add_handler(CommandHandler("start", startHandler))
    dp.add_handler(CommandHandler("help", helpHandler))

    # Handler for messages (non-commands)
    dp.add_handler(MessageHandler(Filters.text, infoHandler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()