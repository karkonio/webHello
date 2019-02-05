import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from playhouse.shortcuts import model_to_dict

from models import Item, Cart, CartItem, Customer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
token = os.environ['BOT_TOKEN']
updater = Updater(token=token)
dispatcher = updater.dispatcher


def start(bot, update):
    # Бот просит представиться при каждом вызове старт
    try:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Здравствуйте! Как вас Зовут?'
            'Введите свое имя используя команду /name + Ваше имя, чтобы мы вас узнали :)'
        )
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )


def add_to_cart(bot, update, args):
    """
def buy(bot, update, args):
    try:
        if len(args) == 2:
            customer_name = args[1]
            customer = Customer.select().where(
                Customer.name == customer_name
            )[0]
        else:
            item_id = args[0]
            item = Item.select().where(Item.id == item_id)[0]
            cart = Cart(
                customer=customer
            )
            cart.save()
            cart_item = CartItem(
                cart=cart,
                item=item
            )
            cart_item.save()
            bot.send_message(
                chat_id=update.message.chat_id,
                text='{}, you succesfully bought {}'.
                format(cart.customer, cart_item.item)
            )
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )
    """


def name(bot, update, args):
    # Данная функция проверяет наличие пользователя в БД по имени.
    # Если такого пользователя нет, вносит его в БД.
    name = args[0]
    customers = Customer.select(Customer.name)
    customers = [model_to_dict(customer) for customer in customers]
    customers_list = []
    for customer in customers:
        customers_list.append(customer['name'])
    if name in customers_list:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='{}, мы нашли вас в базе.'.format(name)
        )
    elif name not in customers_list:
        customer = Customer(
            name=name,
            age=20
        )
        customer.save()
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Отлично, {}. Мы добавили вас в базу.'.format(name)
        )
    return name


def echo(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text
    )


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Такой команды не существует. Попробуйте что-нибудь другое :)'
    )


start_handler = CommandHandler('start', start)
buy_handler = CommandHandler('buy', buy, pass_args=True)
name_handler = CommandHandler('name', name, pass_args=True)
cart_handler = CommandHandler('cart', add_to_cart, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(buy_handler)
dispatcher.add_handler(name_handler)
dispatcher.add_handler(cart_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


if __name__ == '__main__':
    updater.start_polling()
