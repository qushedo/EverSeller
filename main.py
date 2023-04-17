import random
import time
import telebot
import os
import dearpygui.dearpygui as dpg
from user_page_request import lzt_api_get_user_name
from market_list_request import lzt_api_get_market_list
from market_buy_account import lzt_api_buy_account
from colorama import Fore
from colorama import Style


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


dpg.create_context()
dpg.font(file="noto-mono.regular.ttf", size=14, glyph_ranges='cyrillic')


class DataValues():
    account_amount = 0
    curr_amount = 0
    money = 0
    token = '\"SOME TOKEN\"'
    link = '\"SOME LINK\"'
    lzt_name = []
    work_stage = 1
    telegram_id = -1
    balance = 0
    check = True
    TGtoken = "\"SOME TOKEN\""
    fastbuy = False
    bot = None


def TGId(sender):
    DataValues.work_stage = 1
    dpg.configure_item(item="Button", label="[START WORK]", callback=callback_x)
    try:
        DataValues.telegram_id = int(dpg.get_value(sender))
    except:
        dpg.set_value("Checker", "[TELEGRAM ID SHOULD BE A NUMBER]")
        return
    dpg.set_value("Checker", "[ERROR LOG]")


def Token(sender):
    DataValues.work_stage = 1
    dpg.configure_item(item="Button", label="[START WORK]", callback=callback_x)
    DataValues.token = dpg.get_value(sender)
    if DataValues.token != '\"SOME TOKEN\"':
        dpg.set_value("Checker", "[ERROR LOG]")
        return


def TGToken(sender):
    DataValues.work_stage = 1
    dpg.configure_item(item="Button", label="[START WORK]", callback=callback_x)
    DataValues.TGtoken = dpg.get_value(sender)
    if DataValues.token != '\"SOME TOKEN\"':
        dpg.set_value("Checker", "[ERROR LOG]")
        return


def Link(sender):
    DataValues.work_stage = 1
    dpg.set_value("Checker", "[ERROR LOG]")
    DataValues.link = dpg.get_value(sender)


def print_val(sender):
    value = dpg.get_value(sender)
    DataValues.eff = value[0]
    DataValues.time = value[1]


def account(sender):
    DataValues.account_amount = dpg.get_value(sender)


def callback_y(sender):
    DataValues.work_stage = 1


def working(sender):
    dpg.configure_item(item="Button", label="[WORKING]", callback=None)
    while DataValues.curr_amount < DataValues.account_amount:
        time.sleep(3)
        accounts = lzt_api_get_market_list(DataValues.token, DataValues.link)
        print(accounts)
        time.sleep(3)
        if accounts is None:
            continue
        for iterable in range(0, min(accounts.get("totalItems"), accounts.get("perPage")) - 1):
            item = accounts.get("items")[iterable]
            if DataValues.balance < item.get("price"):
                continue
            res = lzt_api_buy_account(DataValues.token, item.get("item_id"), item.get("price"),
                                      DataValues.fastbuy)
            if res is not False:
                dpg.set_value("Log", f"[LIST #{iterable}] {res}")
                DataValues.balance -= item.get("price")
                DataValues.money += item.get("price")
                DataValues.curr_amount += 1
                DataValues.bot.send_message(chat_id=DataValues.telegram_id,
                                 text=f"<b> ~ NeverSeller ~ </b>\n\n"
                                      f"<i> - Аккаунт куплен! -\n</i>"
                                      f"    └ <i>Название товара:</i> <code>{item.get('title')}</code>\n"
                                      f"    └ <i>Цена товара:</i> <code>{item.get('price')}</code>\n"
                                      f"    └ <i>Ссылка на товар:</i> https://lzt.market/{item.get('item_id')}/\n"
                                      f"\n"
                                      f"<i>- Обновление пользовательской информации! -</i>\n"
                                      f"    └ <i>Ваш баланс:</i> <code>{DataValues.balance}</code>\n"
                                      f"    └ <i>Общее кол-во денег, потраченных на аккаунты:</i> <code>{DataValues.money}</code>\n"
                                      f"    └ <i>Куплено аккаунтов</i> <code>{DataValues.curr_amount}</code> <i>из</i> <code>{DataValues.account_amount}</code>!",
                                 parse_mode="html")
                break
            else:
                dpg.set_value("Log", f"[LIST #{iterable}] [ACCOUNT ERROR | CHECKING NEW]")
    dpg.set_value("Log", ":: {Work Completed} ::")
    dpg.configure_item(item="Button", label="[START WORK]", callback=callback_x)


def flag(sender):
    DataValues.fastbuy = not DataValues.fastbuy


def buy_flag(sender):
    DataValues.check = not DataValues.check


def callback_x(sender):
    if DataValues.token == '\"SOME TOKEN\"':
        dpg.set_value("Checker", "[THAT'S EXAMPLE TOKEN]")
        return
    elif DataValues.telegram_id == -1:
        dpg.set_value("Checker", "[THAT'S EXAMPLE TELEGRAM ID]")
        return
    elif DataValues.link == '\"SOME LINK\"':
        dpg.set_value("Checker", "[THAT'S EXAMPLE LINK]")
        return
    elif DataValues.TGtoken == '\"SOME TOKEN\"':
        dpg.set_value("Checker", "[THAT'S EXAMPLE TELEGRAM TOKEN]")
        return

    if DataValues.account_amount == 0:
        dpg.set_value("Checker", "[ZERO ACCOUNTS]")
        return

    try:
        DataValues.bot = telebot.TeleBot(DataValues.TGtoken)
    except:
        dpg.set_value("Checker", "[NO INTERNET CONNECTION ON YOUR PC / WRONG TELEGRAM BOT TOKEN]")
        return

    try:
        DataValues.bot.send_message(chat_id=DataValues.telegram_id, text=f"<b>Автоскуп начал свою работу!</b>", parse_mode='HTML')
    except:
        dpg.set_value("Checker", "[NO INTERNET CONNECTION ON YOUR PC / WRONG TELEGRAM ID]")
        return

    DataValues.work_stage += 1
    dpg.configure_item(item="Button", label="[CHECKING TOKEN]", callback=None)
    DataValues.lzt_name = lzt_api_get_user_name(DataValues.token)
    DataValues.balance = DataValues.lzt_name[2]
    time.sleep(3)
    if DataValues.check:
        with dpg.window(label="[LOLZ USERNAME CHECKER]", width=420, height=170) as my_window:
            dpg.configure_item(my_window, show=True)
            dpg.add_input_text(label=f"[LOLZ USERNAME]", default_value=f"{DataValues.lzt_name[0]}")
            dpg.add_input_text(label=f"[LOLZ LINK]", default_value=f"https://zelenka.guru/{DataValues.lzt_name[1]}/")
            dpg.add_input_text(label=f"[LOLZ BALANCE]", default_value=f"{DataValues.balance}")
            dpg.add_text("")
            dpg.add_text(f"If any of following information is incorrect, then")
            dpg.add_text(f"re-open the program and re-enter your LOLZ token.")

    if DataValues.lzt_name[0] == "WRONG TOKEN / ERROR":
        dpg.set_value("Checker", "[WRONG TOKEN | ACCOUNT PARSE ERROR]")
        dpg.configure_item(item="Button", label="[START WORK]", callback=callback_x)
        return
    else:
        time.sleep(3)
        account_info = lzt_api_get_market_list(DataValues.token, DataValues.link)
        if account_info is None or account_info.get("totalItems") == 0:
            dpg.set_value("Checker", "[WRONG LINK / NO ITEMS] :: CHANGING LINK IS RECOMMENDED")
        if DataValues.check:
            with dpg.window(label="[LOLZ ITEM CHECKER]", width=420, height=215, pos=[0, 170]) as my_window:
                dpg.configure_item(my_window, show=True)
                if account_info is None or account_info.get("totalItems") == 0:
                    dpg.add_text("[WRONG LINK / NO ITEMS]")
                    dpg.add_text("")
                    dpg.add_text(f"This is a random account by your filters.")
                    dpg.add_text(f"If any of following information is incorrect, then")
                    dpg.add_text(f"re-open the program and re-enter your link.")
                else:
                    item = account_info.get("items")[
                        random.randint(0, min(account_info.get("totalItems"), account_info.get("perPage")) - 1)]
                    print(item)
                    dpg.add_input_text(label=f"[ITEM NAME]", default_value=item.get("title"))
                    dpg.add_input_text(label=f"[ITEM PRICE]", default_value=str(item.get("price")))
                    dpg.add_input_text(label=f"[ITEM ORIGIN]", default_value=str(item.get("item_origin")))
                    dpg.add_input_text(label=f"[ITEM LINK]", default_value=f"https://lzt.market/{item.get('item_id')}/")
                    dpg.add_text("")
                    dpg.add_text(f"This is a random account by your filters.")
                    dpg.add_text(f"If any of following information is incorrect, then")
                    dpg.add_text(f"re-open the program and re-enter your link.")

    dpg.configure_item(item="Button", label="[ALL INFO IS CORRECT] [START WORK]", callback=working)
    return


with dpg.window(tag="Primary Window", label="Tutorial", width=200, height=200):
    dpg.add_text("[PRIVATE USE ONLY] [MADE BY NVRTHLSH] [CONTACT IF ANY PROBLEMS OCCUR]\n\n\n\n\n")
    slider_int = dpg.add_slider_int(label="[ACCOUNT AMMOUNT]", width=324, default_value=0, max_value=100,
                                    callback=account)
    dpg.add_checkbox(label="[FAST-BUY] [NO CHECK FOR VALID] [FASTER]", callback=flag)
    dpg.add_checkbox(label="[NO ITEM AND USER BEFORE BUYING CHECK]", callback=buy_flag)
    dpg.add_text(" ")
    dpg.add_input_text(label="[LOLZ TOKEN]", default_value="\"SOME TOKEN\"", callback=Token)
    dpg.add_input_text(label="[TELEGRAM ID]", default_value="\"SOME ID\"", callback=TGId)
    dpg.add_input_text(label="[ACCOUNTS LINK]", default_value="\"SOME LINK\"", callback=Link)
    dpg.add_input_text(label="[TELEGRAM BOT TOKEN]", default_value="\"SOME TOKEN\"", callback=TGToken)
    dpg.add_text(" ")
    dpg.add_text("[ERROR LOG]", tag="Checker")
    dpg.add_text(" ")
    dpg.add_text(":: {Print-Log} ::", tag="Log")
    dpg.add_text(" ")
    dpg.add_button(label="[START WORK]", width=484, height=50, callback=callback_x, tag="Button")

dpg.create_viewport(title='NeverSeller V1.2.2 (e14134111)', width=515, height=476)
dpg.setup_dearpygui()
dpg.set_viewport_resizable(False)
dpg.set_viewport_clear_color(2)
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
