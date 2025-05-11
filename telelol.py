import telebot
from regions_dicts import regions, image, narod, test, questions, narodIm
from DatBase import Db_work
import weather
import pymorphy3

db = Db_work()
flag = True
bot = telebot.TeleBot("7738077069:AAHhp_iPvrurET3yU8y-XZPtwzxD9Xr_-LA")
morph = pymorphy3.MorphAnalyzer()
word1 = morph.parse('балл')[0]
word2 = morph.parse('бонус')[0]

users = {}
answer = []
correct_ans = 0
no_or_yes = {"1": "Да", "2": "Нет", "3": ""}
pol = {}
statistic = {}


def save_dat(message):
    f = open('stat.txt', encoding='utf8', mode='r')
    otv = f.readlines()
    f.close()
    res = []
    with open('stat.txt', encoding='utf8', mode='w') as file:
        for key in statistic:
            data = list(statistic[key].values())
            for el in otv:
                if str(key) in el:
                    el = list(map(int, el.split()))
                    for i in range(0, 5):
                        data[i] += el[i + 1]
                    break
            res.append(str(key) + ' ' + ' '.join(list(map(str, data))))
        for el in res:
            print(el, file=file)
    statistic.clear()
    testing(message)


def testing(message):
    if not message:
        return
    if message.from_user.id not in statistic:
        statistic[message.from_user.id] = {'ball': 0, "quest": 0, 'tru_utv': 0, 'open_reg': 0, 'open_nar': 0}


@bot.message_handler(func=lambda message: message.text == '🪙 Бонусы')
@bot.callback_query_handler(func=lambda call: 'ball' in call.data)
def balllll(call):
    if call.from_user.id in statistic:
        bal = statistic[call.from_user.id]['ball']
    else:
        testing(call)
        save_dat(call)
        with open('stat.txt', encoding='utf8', mode='r') as file:
            data = file.readlines()
            for el in data:
                el = el.rstrip()
                if str(call.from_user.id) in el:
                    el = el.split()
                    bal = el[1]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text=f"⏪ назад", callback_data=f'main'))
    if call.__class__.__name__ == 'Message':
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message_id,
                              text=f'У вас {bal}  {word2.make_agree_with_number(bal).word}\nВы можете потратить их на сайте:'
                                   f'\n<название и ссылка на сайт инвестора>', reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=f'У вас {bal}  {word2.make_agree_with_number(bal).word}\nВы можете потратить их на сайте:'
                                   f'\n<название и ссылка на сайт инвестора>', reply_markup=keyboard)


def set_narod_region(call, region):
    keyboard = telebot.types.InlineKeyboardMarkup()
    data = db.ret_reg_nar(region)
    for i in range(len(data)):
        keyboard.add(telebot.types.InlineKeyboardButton(text=f"{data[i]}", callback_data=f'narod_{data[i]}_{region}'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=f"⏪ назад", callback_data=f'region_{region}_back'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Выберите народ севера:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'main')
def set_main(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    txt = ['🪙 Бонусы', '🚩 Выбрать регион', '👨‍👩‍👧‍👦 Народы', '📊 Статистика', '⚙️ Спросить у AI', "📝 Тест"]
    otv = ['ball', 'selecr_reg', 'all_men', 'stat', '5', 'test_menu']
    for i in range(0, 6, 2):
        a = telebot.types.InlineKeyboardButton(text=f"{txt[i]}", callback_data=f'{otv[i]}')
        b = telebot.types.InlineKeyboardButton(text=f"{txt[i + 1]}", callback_data=f'{otv[i + 1]}')
        keyboard.add(a, b)
    if call.__class__.__name__ == 'Message':
        bot.send_message(call.from_user.id, 'Выберите действие', reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Выберите действие', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '📊 Статистика')
@bot.callback_query_handler(func=lambda call: 'stat' in call.data)
def print_stat(message):
    testing(message)
    save_dat(message)
    with open('stat.txt', encoding='utf8', mode='r') as file:
        data = file.readlines()
        for el in data:
            el = el.rstrip()
            if str(message.from_user.id) in el:
                el = el.split()
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'main'))
        if message.__class__.__name__ == 'Message':
            bot.send_message(chat_id=message.from_user.id,
                             text=f'Ваши результаты:\nБаллы: {el[1]}\nВсего твечего на вопросов: {el[2]}\nВсего'
                                  f' правильных ответов: {el[3]}\nКоличество раз открытия информации о регионе:'
                                  f' {el[4]}\nКоличество раз открытия информации о народе {el[5]}',
                             reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                  text=f'Ваши результаты:\nБаллы: {el[1]}\nВсего твечего на вопросов: {el[2]}'
                                       f'\nВсего правильных ответов: {el[3]}\nКоличество раз открытия информации о'
                                       f' регионе: {el[4]}\nКоличество раз открытия информации о народе {el[5]}',
                                  reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '🚩 Выбрать регион')
@bot.callback_query_handler(func=lambda call: 'selecr_reg' in call.data)
def set_regions(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    names = list(regions.keys())
    for i in range(0, 8, 2):
        a = telebot.types.InlineKeyboardButton(text=f"{names[i]}", callback_data=f'region_{i}')
        b = telebot.types.InlineKeyboardButton(text=f"{names[i + 1]}", callback_data=f'region_{i + 1}')
        keyboard.add(a, b)
    keyboard.add(telebot.types.InlineKeyboardButton(text=f"{names[8]}", callback_data=f'region_{8}'),
                 telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'main'))
    if message.__class__.__name__ == 'Message':
        bot.send_message(message.from_user.id, f'Выберите регион', reply_markup=keyboard)
    else:
        try:
            bot.delete_message(message.from_user.id, users[str(message.from_user.id)])
        except Exception:
            pass
        testing(message)
        statistic[message.from_user.id]['open_reg'] += 1
        bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                              text=f'Выберите регион', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'region_' in call.data)
def open_reg(call):
    cnt = call.data.split('_')
    data = int(cnt[1])
    region = image[data][1]
    temper = weather.reg_weather(data)
    ret = False
    if len(cnt) == 3:
        ret = True
    keyboard = telebot.types.InlineKeyboardMarkup()
    names = ['👨‍👩‍👧‍👦 Народы', '🧑‍🏭 промыслы', '🗺️ освоение', '🎞️ история', '🕐 настоящие', '🥞 блюда', '⭐ перспективы',
             "⏪ назад"]
    db.reg_number(data)
    for i in range(0, 6, 2):
        a = telebot.types.InlineKeyboardButton(text=f"{names[i]}", callback_data=f'area_inf_{names[i]}_{data}')
        b = telebot.types.InlineKeyboardButton(text=f"{names[i + 1]}", callback_data=f'area_inf_{names[i + 1]}_{data}')
        keyboard.add(a, b)
    keyboard.add(telebot.types.InlineKeyboardButton(text=f"{names[6]}", callback_data=f'area_inf_{names[6]}_{data}'),
                 telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'selecr_reg_back'))
    if ret:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'{temper}\nЧто хотите узнать?', reply_markup=keyboard)
    else:
        bot.delete_message(call.from_user.id, call.message.message_id)
        res = bot.send_photo(call.from_user.id, open(f'regionIm\{image[data][0]}', 'rb'), caption=region)
        users[str(call.from_user.id)] = res.message_id
        bot.send_message(call.from_user.id, f'{temper}\n\nЧто хотите узнать?',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'area_inf_' in call.data)
def open_reg_inf(call):
    data = call.data.split('_')[2:]
    if '👨‍👩‍👧‍👦 Народы' in data[0]:
        set_narod_region(call, regions[image[int(data[1])][1]])
        return
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'region_{data[1]}_back'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{db.ret_regions(data[0])}', reply_markup=keyboard)


@bot.message_handler(commands=["start", "restart"])
def start(message):
    if message.from_user.id not in statistic:
        keyboardgostart = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboardgostart.add(
            *[telebot.types.KeyboardButton(name) for name in ['🪙 Бонусы', '🚩 Выбрать регион', '👨‍👩‍👧‍👦 Народы',
                                                              '📊 Статистика', '⚙️ Спросить у AI', "📝 Тест"]])
        text = f'Привет, меня зовут Хранитель Арктики. Я могу рассказать о коренных малых' \
               f' народах севера и регионах в которых они проживают. Также я могу проверить' \
               f' твои знания об Арктике  и за правильные ответы ты можешь получить бонусы,' \
               f' которые можно потратить у наших спонсоров для получения скидок и акций'
        bot.send_photo(message.chat.id, open(f'regionIm\startIm.jpg', 'rb'), caption=text, reply_markup=keyboardgostart)
    testing(message)
    set_main(message)


@bot.message_handler(func=lambda message: message.text == '👨‍👩‍👧‍👦 Народы')
@bot.callback_query_handler(func=lambda call: call.data == 'all_men')
def set_narod_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    names = list(narod.keys())
    for i in range(0, 12, 3):
        a = telebot.types.InlineKeyboardButton(text=f"{names[i]}", callback_data=f'narod_{names[i]}')
        b = telebot.types.InlineKeyboardButton(text=f"{names[i + 1]}", callback_data=f'narod_{names[i + 1]}')
        c = telebot.types.InlineKeyboardButton(text=f"{names[i + 2]}", callback_data=f'narod_{names[i + 2]}')
        keyboard.add(a, b, c)
    a = telebot.types.InlineKeyboardButton(text=f"{names[12]}", callback_data=f'narod_{names[12]}')
    keyboard.add(a, b, telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'main'))
    if message.__class__.__name__ == 'Message':
        bot.send_message(message.from_user.id, f'Выберите народ', reply_markup=keyboard)
    else:
        try:
            bot.delete_message(message.from_user.id, users[message.from_user.id])
        except Exception:
            pass
        testing(message)
        statistic[message.from_user.id]['open_nar'] += 1
        bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                              text=f'Выберите народ', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'narod_' in call.data)
def print_narod(call):
    type = call.data.split('_')
    ret = False
    if len(type) == 3:
        ret = True
    type = type[1]
    keyboard = telebot.types.InlineKeyboardMarkup()
    a = telebot.types.InlineKeyboardButton(text='💡 Информация', callback_data=f'info_nar_{type}_💡 Информация')
    b = telebot.types.InlineKeyboardButton(text='🎞️ История', callback_data=f'info_nar_{type}_🎞️ История')
    c = telebot.types.InlineKeyboardButton(text='👺 Традиции', callback_data=f'info_nar_{type}_👺 Традиции')
    d = telebot.types.InlineKeyboardButton(text='🥞 Фирменные блюда', callback_data=f'info_nar_{type}_🥞 Фирменные '
                                                                                   f'блюда')
    keyboard.add(a, b, c)
    keyboard.add(d, telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data='all_men'))
    if ret:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Информация о народе {type}\nЧто хотите узнать?', reply_markup=keyboard)
    else:
        bot.delete_message(call.from_user.id, call.message.message_id)
        res = bot.send_photo(call.from_user.id, narodIm[type])
        users[call.from_user.id] = res.message_id
        bot.send_message(call.from_user.id, f'Информация о народе {type}\nЧто хотите узнать?',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'info_nar_' in call.data)
def print_narod_info(call):
    type = call.data.split('_')[2:]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'narod_{type[0]}_back'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{db.ret_nar(type)}', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '📝 Тест')
@bot.callback_query_handler(func=lambda call: call.data == 'test_menu')
def menu_test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    b = telebot.types.InlineKeyboardButton(text=f"Начать тест", callback_data=f'start_test_3')
    keyboard.add(b)
    keyboard.add(telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'main'))
    if message.__class__.__name__ == 'Message':
        bot.send_message(message.from_user.id, f'Пройдите Тест', reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                              text=f'Пройдите Тест', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'start_test' in call.data)
def test_start(call):
    global answer, pol, no_or_yes, last_ans
    if call.from_user.id in pol:
        pol[call.from_user.id] += 1
    else:
        pol[call.from_user.id] = 0
    if pol[call.from_user.id] <= 13:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(1):
            a = telebot.types.InlineKeyboardButton(text=f"Да", callback_data=f'start_test_1')
            b = telebot.types.InlineKeyboardButton(text=f"Нет", callback_data=f'start_test_2')
            keyboard.add(a, b)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'{questions[pol[call.from_user.id]]}', reply_markup=keyboard)
        data = call.data.split('_')[2]
        answer.append(no_or_yes[str(data)])
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(1):
            a = telebot.types.InlineKeyboardButton(text=f"Да", callback_data=f'congratul_test_1')
            b = telebot.types.InlineKeyboardButton(text=f"Нет", callback_data=f'congratul_test_2')
            keyboard.add(a, b)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'{questions[pol[call.from_user.id]]}', reply_markup=keyboard)
        data = call.data.split('_')[2]
        answer.append(no_or_yes[str(data)])


@bot.callback_query_handler(func=lambda call: 'congratul_test' in call.data)
def congratulation(call):
    data = call.data.split('_')[2]
    morph = pymorphy3.MorphAnalyzer()
    comment = morph.parse('вопрос')[0]
    global answer, correct_ans
    answer.append(no_or_yes[str(data)])
    for i in range(1, 16):
        if test[i] == answer[i - 1]:
            correct_ans += 1
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⏪ назад", callback_data=f'main'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Поздравляю! Вы прошли тест!\n'
                               f'Вы ответили правильно на {correct_ans}'
                               f' {comment.make_agree_with_number(correct_ans).word}',
                          reply_markup=keyboard)
    testing(call)
    statistic[call.from_user.id]['ball'] += correct_ans
    statistic[call.from_user.id]['quest'] += 15
    statistic[call.from_user.id]['tru_utv'] += correct_ans
    pol[call.from_user.id] = 0
    answer = []
    correct_ans = 0


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()

message = None
save_dat(message)
