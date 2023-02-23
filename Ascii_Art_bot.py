import telebot
import time

import PIL.ImageEnhance
import PIL.Image

TOKEN = '5775902335:AAFvagZD-W0vQkdInGxF-EWGg09CdtiS6s8'
bot = telebot.TeleBot('%s' % TOKEN)
black_list = []
requests = []


def spam_test(req, message):
    flag = False
    if len(req) <= 1:
        pass
    else:
        pair = []
        for i in req:
            if len(pair) != 2:
                pair.append(i)
            else:
                if (pair[1] - pair[0]) <= 0.3:
                    flag = True
                    break

    if flag:
        time.sleep(1)
        #1
        print(f'[WARNING] Too many reqests SPAM_USER: {message.from_user.first_name}')


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Начнем")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я бот для создания ASCII артов из изображений".format(
                         message.from_user), reply_markup=markup)

    print(f"[INFO USER] User's ID {message.chat.id}")
    print(f"[INFO USER] User's name {message.from_user.first_name}")
    print(f"[INFO USER] User's nick {message.from_user.username}")
    print('---------------------------------------------------------')


@bot.message_handler(content_types=['text'])
def func(message):
    requests.append(time.time())
    if message.text in ["Маленький (50sb)", "Средний (100sb)", "Большой (150sb)", "Очень большой (200sb)", "Полноразмерный"]:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(" ")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Давай выберем формат вывода", reply_markup=markup)
        global current_size
        if message.text == "Маленький (50sb)":
            current_size = 50
            print('[USER] Size: small')
        elif message.text == "Средний (100sb)":
            current_size = 100
            print('[USER] Size: medium')
        elif message.text == "Большой (150sb)":
            current_size = 150
            print('[USER] Size: big')
        elif message.text == "Очень большой (200sb)":
            current_size = 200
            print('[USER] Size: large')
        elif message.text == "Полноразмерный":
            current_size = 500
            print('[USER] Size: Full')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("txt")
        btn2 = telebot.types.KeyboardButton("PDF")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Давай выберем формат вывода", reply_markup=markup)
    elif message.text in ['txt', 'PDF']:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn0 = telebot.types.KeyboardButton(" ")
        markup.add(btn0)
        bot.send_message(message.chat.id, text="Теперь скидывай изображение", reply_markup=markup)
        print(f'[USER] Format: {message.text}')
        print('---------------------------------------------------------')
    elif message.text == 'Начнем' or message.text == 'Еще один арт':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("Маленький (50sb)")
        btn2 = telebot.types.KeyboardButton("Средний (100sb)")
        btn3 = telebot.types.KeyboardButton("Большой (150sb)")
        btn4 = telebot.types.KeyboardButton("Очень большой (200sb)")
        btn5 = telebot.types.KeyboardButton("Полноразмерный")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Давай выберем размер будущего арта", reply_markup=markup)
        if message.text == 'Еще один арт':
            print(f'[USER] Came back')


    spam_test(requests, message)


@bot.message_handler(commands=['help'])
def get_user_test(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['photo'])
def message_post(message):
    requests.append(time.time())
    ASCII_CHARS = ["@", "#", "$", "%", "?", "+", ";", ",", ".", " "]

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, text="Вот твой арт", reply_markup=markup)

    if message.chat.type == 'private':
        f_id = message.photo[-1].file_id
        file_info = bot.get_file(f_id)
        down_file = bot.download_file(file_info.file_path)
        with open('img.jpg', 'wb') as file:
            file.write(down_file)
        image = PIL.Image.open('img.jpg')
        print('[INFO] File open succsessfully')


        def resize(img):
            try:
                width, height = img.size
                new_height = current_size * height // width // 2
                print('''[INFO] Resized open succsessfully,
                Current_size=''' + str(current_size))
                return img.resize((current_size, new_height))
            except NameError:
                width, height = img.size
                new_height = int(int(100) * height / width / 2)
                print('''[INFO] Resized open succsessfully,
                Current_size=''' + str(100))
                return img.resize((100, new_height))


        def to_greyscale(image):
            print('[INFO] Done in monochrome succsessfully')
            return image.convert("L")

        def pixel_to_ascii(image):
            pixels = image.getdata()
            ascii_str = ""
            print('[INFO] Conversion is in progress')
            for pixel in pixels:
                ascii_str += ASCII_CHARS[pixel // 22 if (pixel // 22) < 10 else -1]
            print('[INFO] Converted succsessfully')
            return ascii_str

        image = resize(image)
        greyscale_image = to_greyscale(image)
        ascii_str = pixel_to_ascii(greyscale_image)
        img_width = greyscale_image.width
        ascii_str_len = len(ascii_str)
        ascii_img = ""
        for i in range(0, ascii_str_len, img_width):
            ascii_img += ascii_str[i:i + img_width] + "\n"

        with open("ascii_image.txt", "w") as f:
            f.write(ascii_img)
            print('[INFO] ASII art saved succsessfully')

        bot.send_document(message.chat.id, open('ascii_image.txt'))
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("Еще один арт")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Вернуться в начало, для создания нового арта или продолжить с теми же настройками?", reply_markup=markup)
        print('[INFO] ASII sent succsessfully')
        print('[INFO] All processes completed successfully')
        print('#########################################################')
    spam_test(requests, message)

bot.polling()