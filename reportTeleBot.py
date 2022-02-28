from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

# TODO: update if number of questions depends on report type
numQuestions = 18

repliesReport1 = {
    1: "Rank + Full Name:",
    2: "Date:",
    3: "Symptom:",
    4: "Location and Time:",
    5: "Last ART:",
    6: "RSN Protocol 3 date:", # to update if needed
    7: "Date of Close Contact:", # to update if needed
    8: "Date of Booster:",
    9: "NRIC:",
    10: "Service Status:",
    11: "Sex/Age:",
    12: "VOC:",
    13: "DOB:",
    14: "ORD:",
    15: "Last Location:",
    16: "Date at Last Location:",
    17: "Number of Close Contacts:", # add in if anticipate ops impact?
    18: "Recovery Buddy:",
    19: "Report being generated..."
}

repliesReport2 = {
    1: "Q1",
    2: "Q2",
    3: "Q3",
    4: "Q4",
    5: "Q5",
    6: "Q6",
    7: "Q7",
    8: "Q8",
    9: "Q9",
    10: "Q10",
    11: "Q11",
    12: "Q12",
    13: "Q13",
    14: "Q14",
    15: "Q15",
    16: "Q16",
    17: "Q17",
    18: "Q18",
    19: "Report being generated..."
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

# TODO: if/else based on answers I guess
def createReport1(chat_id):
    report = "Dear CNMO Sir,\n\nINCIDENT REPORT/NMS/"
    report += userReplies[chat_id][1] + "/Symptomatic Ag+ (P2PC)\n\n"
    report += "Background\n1. On "
    report += userReplies[chat_id][2] + ", " + userReplies[chat_id][1] + " developed " + userReplies[chat_id][3] + ". "
    report += userReplies[chat_id][1] + " reported sick at " + userReplies[chat_id][4] + " and was administered a PA-ART which returned positive. His last RRT-ART on "
    report += userReplies[chat_id][5] + " was negative.\n\n"
    # to update if needed
    report += "2. " + userReplies[chat_id][1] + " has been on RSN Protocol 3 since " + userReplies[chat_id][6]
    report += " as a result of close contact (HH member) to his brother that was placed on P2PC on " + userReplies[chat_id][7] + ".\n\n"
    #
    report += "3. " + userReplies[chat_id][1] + " is currently stable. He has completed his primary COVId-19 vaccination series, with a booster dose on " + userReplies[chat_id][8] + ".\n\n"
    report += "4. None of his family have any travel history, and none reported contact with any local clusters beyond their household.\n"
    report += "PARTICULARS OF SERVICE PERSON:\n"
    report += "NRIC: " + userReplies[chat_id][9] + "\n"
    report += "RANK/NAME: " + userReplies[chat_id][1] + "\n"
    report += "SERVICE STATUS: " + userReplies[chat_id][10] + "\n"
    report += "SEX/AGE: " + userReplies[chat_id][11] + "\n"
    report += "VOC: " + userReplies[chat_id][12] + "\n"
    report += "DOB: " + userReplies[chat_id][13] + "\n"
    report += "ORD: " + userReplies[chat_id][14] + "\n\n"
    report += "CLASSIFICATION AND ASSESSMENT:\n"
    report += "5. Given that " + userReplies[chat_id][1] + " is symptomatic with a positive PA-ART, he will be managed as per MOH Protocol 2 (Primary Care). No confirmatory PCR is required. Serviceman will self-isolate for 72 hours. After 72 hours, he will (a) conduct daily ART and continue to isolate until he tests negative OR (b) time-based discharge on D7 of illness. "
    report += userReplies[chat_id][1] + " will only return to work after he and all his household members have exited isolation.\n\n"
    report += "CONTACT MAPPING\n"
    report += "6. " + userReplies[chat_id][1] + " was last in " + userReplies[chat_id][15] + " on " + userReplies[chat_id][16] + ", there are "
    report += userReplies[chat_id][17] + " RSN close contact(s) based on S-2.\n\n"
    report += "OPS IMPACT\n"
    report += "7. There is anticipated ops impact to NMOC operations. NMOC will make the necessary adjustments to accomodate for the ops needs.\n\n"
    report += "8. NMS will maintain close contact and provide support to the serviceman. "
    report += userReplies[chat_id][18] + " has preliminary been appointed as the Recovery Buddy.\n\n"
    report += "9. Submitted for info, please."

    return report

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

# TODO: command to show types of reports and descriptions

def collectInfo(chat_id, i, ans):
    userReplies[chat_id][i] = ans
    userState[chat_id] += 1

def collectReportType(chat_id, ans):
    if ans not in reportDispatcher:
        return False
    userReplies[chat_id][0] = ans 
    userState[chat_id] += 1  
    return True

def infoHandler(update, context):
    chat_id = update.message.chat_id

    if (chat_id not in userReplies or chat_id not in userState or userState[chat_id] == -1): # report not yet started
        update.message.reply_text("pls start a new session with /start to generate a report")
        
    elif (userState[chat_id] == 0): # answer is the report type, ready to ask first question
        success = collectReportType(chat_id, update.message.text)
        if (success):
            update.message.reply_text(replies[userReplies[chat_id][0]][userState[chat_id]])
        else:
            update.message.reply_text("Report type invalid.")
            update.message.reply_text("what report type: ")

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


def options(update, context):
    button_list = [
        InlineKeyboardButton("Yes", callback_data="Yes"),
        InlineKeyboardButton("No", callback_data="No")
    ]
    # for each in ["yes", "no"]:
    #     button_list.append(InlineKeyboardButton(each, callback_data=each))
    reply_markup = InlineKeyboardMarkup([button_list])
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Are you sure you want to start a new report? This will erase all data from the ongoing report.",
                             reply_markup=reply_markup)
    
# def build_menu(buttons, n_cols=2, header_buttons=None, footer_buttons=None):
#     """
#     Returns a list of inline buttons used to generate inlinekeyboard responses
    
#     :param buttons: `List` of InlineKeyboardButton
#     :param n_cols: Number of columns (number of list of buttons)
#     :param header_buttons: First button value
#     :param footer_buttons: Last button value
#     :return: `List` of inline buttons
#     """
#     menu = [buttons]
#     # menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), 2)]
#     # if header_buttons:
#     #     menu.insert(0, header_buttons)
#     # if footer_buttons:
#     #     menu.append(footer_buttons)
#     return menu

def query_yes(update, context):
    # TODO: start the new report
    update.callback_query.edit_message_reply_markup(None)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='[query_yes] callback data: ' + update.callback_query.data)

def query_no(update, context):
    # TODO: say continuing on with the report, repeat prev question
    update.callback_query.edit_message_reply_markup(None)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='[query_no] callback data: ' + update.callback_query.data)




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

    dp.add_handler(CommandHandler('options', options))
    dp.add_handler(CallbackQueryHandler(query_yes, pattern='^Yes$'))
    dp.add_handler(CallbackQueryHandler(query_no,  pattern='^No$'))


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