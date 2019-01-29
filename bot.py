import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models import Item, Cart, CartItem, Customer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
updater = Updater(token='704148322:AAE7A1WBjsovkDCbE6u-qwCI7CLASyXjm2M')
dispatcher = updater.dispatcher


def build_menu(buttons, n_cols):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu


def start(bot, update):
    button_list = [
        InlineKeyboardButton("col1", callback_data="1"),
        InlineKeyboardButton("col2", callback_data="2"),
        InlineKeyboardButton("row 2", callback_data="3")
    ]
    reply_markup = InlineKeyboardMarkup(
        build_menu(button_list, n_cols=2)
    )
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Добро пожаловать! Ознакомьтесь с командами :)",
        reply_markup=reply_markup
    )


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


def customer(bot, update, args):
    try:
        name = args[0]
        age = args[1]
        customer = Customer(
            name=name,
            age=age
        )
        customer.save()
        bot.send_message(
            chat_id=update.message.chat_id,
            text='OK, {}! You are in database and can shopping now :)'
            .format(name)
        )
    except Exception as e:
        logging.error(e, exc_info=True)
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
customer_handler = CommandHandler('customer', customer, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(buy_handler)
dispatcher.add_handler(customer_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)


if __name__ == '__main__':
    updater.start_polling()
