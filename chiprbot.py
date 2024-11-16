import telebot
import random

# Ваш токен бота
API_TOKEN = '6276301682:AAGPI8XR39oh5_QSjjnwjGzcfzxPlfed-LQ'

bot = telebot.TeleBot(API_TOKEN)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ#Z@₽*!?£€$¢^°~`|•√π÷×§∆%✓{}"
shift = 0

def create_key(shift, alphabet):
    """Создает ключ - сдвинутый алфавит"""
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    return shifted_alphabet

def shuffle_alphabet(alphabet):
    """Перемешивает алфавит для большей надежности"""
    alphabet_list = list(alphabet)
    random.shuffle(alphabet_list)
    return ''.join(alphabet_list)

def encrypt(text, shift, alphabet):
    """Шифрует текст с помощью сдвинутого и перемешанного алфавита"""
    key = create_key(shift, alphabet)
    ciphertext = ""
    for letter in text:
        if letter.upper() in alphabet:
            index = alphabet.index(letter.upper())
            encrypted_letter = key[index]
            if letter.islower():
                encrypted_letter = encrypted_letter.lower()
            ciphertext += encrypted_letter
        else:
            ciphertext += letter
    return ciphertext

def decrypt(ciphertext, shift, alphabet):
    """Расшифровывает текст с помощью сдвинутого и перемешанного алфавита"""
    key = create_key(shift, alphabet)
    plaintext = ""
    for letter in ciphertext:
        if letter.upper() in key:
            index = key.index(letter.upper())
            decrypted_letter = alphabet[index]
            if letter.islower():
                decrypted_letter = decrypted_letter.lower()
            plaintext += decrypted_letter
        else:
            plaintext += letter
    return plaintext

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для шифрования и дешифровки текста. \n Введите /setshift <значение>, чтобы задать сдвиг. \n Или вы можете задать рандомный сдвиг с помощью /randomshift \n  Введите /add <символы>, чтобы добавить символы в шифр, что бы его было труднее взломать \n Введите /encrypt что бы зашифровать и /descrypt чтобы расшифровать текст \n \n ВАЖНО, Следите за сдвигом, если вы зададтте неверный сдвиг бот не расшифрует сообзение корректно. \n Изначальный сдвиг равен 0")

@bot.message_handler(commands=['setshift'])
def set_shift(message):
    global shift
    try:
        shift_value = int(message.text.split()[1])
        if shift_value < 1 or shift_value >= len(alphabet):
            bot.reply_to(message, f"Пожалуйста, введите значение сдвига от 1 до {len(alphabet)-1}.")
        else:
            shift = shift_value
            bot.reply_to(message, f"Сдвиг установлен на {shift}.")
    except (IndexError, ValueError):
        bot.reply_to(message, "Использование: /setshift <значение>")

@bot.message_handler(commands=['randomshift'])
def random_shift(message):
    global shift
    shift = random.randint(1, len(alphabet) - 1)
    bot.reply_to(message, f"Случайный сдвиг установлен на {shift}.")
    bot.reply_to(message, f"Ключ для шифрования: {create_key(shift, alphabet)}")

@bot.message_handler(commands=['add'])
def add_to_alphabet(message):
    global alphabet
    new_symbols = message.text[len('/add '):]
    alphabet += new_symbols
    bot.reply_to(message, f"Новые символы добавлены в алфавит. Текущий алфавит: {alphabet}")

@bot.message_handler(commands=['shuffle'])
def shuffle_alphabet_command(message):
    global alphabet
    alphabet = shuffle_alphabet(alphabet)
    bot.reply_to(message, f"Алфавит перемешан. Текущий алфавит: {alphabet}")

@bot.message_handler(commands=['encrypt'])
def encrypt_message(message):
    text_to_encrypt = message.text[len('/encrypt '):]
    encrypted_text = encrypt(text_to_encrypt, shift, alphabet)
    bot.reply_to(message, f"Зашифрованный текст: {encrypted_text}")

@bot.message_handler(commands=['decrypt'])
def decrypt_message(message):
    text_to_decrypt = message.text[len('/decrypt '):]
    decrypted_text = decrypt(text_to_decrypt, shift, alphabet)
    bot.reply_to(message, f"Расшифрованный текст: {decrypted_text}")

bot.polling()
