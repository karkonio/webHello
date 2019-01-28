import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from models import Item, Cart, CartItem, Customer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
updater = Updater(token='704148322:AAE7A1WBjsovkDCbE6u-qwCI7CLASyXjm2M')
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Добро пожаловать! Ознакомьтесь с командами :)"
    )


def buy(bot, update, args):
    try:
        item_id = args[0]
        customer_name = args[1]
        item = Item.select().where(Item.id == item_id)
        customer = Customer.select().where(Customer.name == customer_name)
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
        logging.error(e)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )


def user(bot, update, args):
    try:
        name = args[0]
        age = args[1]
        user = Customer(
            name=name,
            age=age
        )
        user.save()
        bot.send_message(
            chat_id=update.message.chat_id,
            text='OK, {}! You are in database and can shopping now :)'
            .format(name)
        )
    except Exception as e:
        logging.error(e)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Fail {}'.format(e)
        )


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
user_handler = CommandHandler('user', user, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(buy_handler)
dispatcher.add_handler(user_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


if __name__ == '__main__':
    updater.start_polling()
