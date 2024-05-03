from telebot import types
from config import questions, answer_weights
from Token import token

TOKEN = bot = token

@bot.message_handler(commands=['start', 'help'])
def gretings(message: types.Message):
    keboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text="О Московском зоопарке", url="https://moscowzoo.ru")
    btn2 = types.InlineKeyboardButton(text="О програме опеки", url="https://moscowzoo.ru/my-zoo/become-a-guardian/")
    keboard.add(btn1,btn2)
    logo = open('images/logo.jpg','rb')
    bot.send_photo(message.chat.id, photo=logo, caption="Приветсвие", reply_markup=keboard)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keboard.add(types.KeyboardButton(text="Начать викторину"))
    msg = bot.send_message(
        message.chat.id,
        text="Пройди викторину и узнай животное которое тебе подходит",
        reply_markup=keyboard)

    bot.register_next_step_handler(msg,ask_questions)

@bot.message_handler(content_types=['text'])
def ask_questions(message: types.Message, step=0, result=0):
    if step:
        result += answer_weights.get(message.text)

    question = questions.get(step)
    question_text = question.get('question')
    keyboard = create_keyboard(question)


    next_step = step + 1


    if next_step in questions:
        msg = bot.send_message(message.chat.id, text=question_text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_questions, next_step, result)
    else:
        msg = bot.send_message(message.chat.id,text=question_text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, show_result, result)


@bot.message_handler(content_types=['text'])
def show_result(message: types.Message, result):
    result += answer_weights.get(message.text)
    if result in range(0,20):
        text = (f"Викторина завершена!, \n Подходящее тебе животное АМУРСКИЙ ТИГР."
                f"\n вопросы по опекунству писать сюда: Опекунство +79629713875 zoofriends@moscowzoo.ru")
        image = open('images/71062cdc-ae27-432a-84ed-d3743afd903b.jpeg', 'rb' )
        bot.send_photo(message.chat.id, photo=image, caption=text, )
    elif result in range(21, 50):
        text = (f"Викторина завершена!, \n Подходящее тебе животное АЛЕКСАНДРИЙСКИЙ ПОПУГАЙ."
                f"\n вопросы по опекунству писать сюда: Опекунство +79629713875 zoofriends@moscowzoo.ru")
        image = open('images/3d4b82db-4161-421c-8f50-902b0f3b0240.jpg', 'rb')
        bot.send_photo(message.chat.id, photo=image, caption=text)
    elif result in range(51, 70):
        text = (f"Викторина завершена!, \n Подходящее тебе животное ДАЛЬНЕВОСТОЧНАЯ КВАКША."
                f"\nвопросы по опекунству писать сюда: Опекунство +79629713875 zoofriends@moscowzoo.ru")
        image = open('images/a288bb59-03f7-420c-9dd0-a11a105b23fc.jpeg', 'rb')
        bot.send_photo(message.chat.id, photo=image, caption=text)
    elif result in range(71, 90):
        text = (f"Викторина завершена!, \n Подходящее тебе животное НИЛЬСКИЙ КРОКОДИЛ."
                f"\n вопросы по опекунству писать сюда: Опекунство +79629713875 zoofriends@moscowzoo.ru")
        image = open('images/crorodil.jpeg', 'rb')
        bot.send_photo(message.chat.id, photo=image, caption=text)




    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Начать заново"))
    msg = bot.send_message(
        message.chat.id,
        text='Если хочешь пройти ещё раз, нажми "Начать заново',
        reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_questions)

def create_keyboard(questions):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for var in questions.get('variants'):
        buttons.append(types.KeyboardButton(text=var))
    keyboard.add(*buttons)
    return keyboard


if __name__ == '__main__':
    bot.polling(non_stop=True)