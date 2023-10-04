import json
import random
import time
import tkinter
from pathlib import Path

import pyglet
import telebot

from app import App, customtkinter
from market_buy_account import lzt_api_buy_account
from market_list_request import lzt_api_get_market_list
from user_page_request import lzt_api_get_user_name

pyglet.options['win32_gdi_font'] = True
fontpath = Path(__file__).parent / 'microgrammad_boldexte.ttf'
pyglet.font.add_file(str(fontpath))
fontpath = Path(__file__).parent / 'CascadiaCode.ttf'
pyglet.font.add_file(str(fontpath))
fontpath = Path(__file__).parent / 'CascadiaMono.ttf'
pyglet.font.add_file(str(fontpath))


def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")


app = App()

app.bind_all("<Key>", _onKeyRelease, "+")


class DataValues:
    account_amount = 0
    curr_amount = 0
    money = 0
    token = '\"SOME TOKEN\"'
    link = '\"SOME LINK\"'
    lzt_name = ['', '', '', '']
    work_stage = 1
    telegram_id = -1
    balance = 0
    check = True
    TGtoken = "\"SOME TOKEN\""
    fastbuy = False
    error_text = ''
    request_text = ''
    accounts = ''
    bot = None
    toplevel_ = None
    account_info = None


class ToplevelWindowUsername(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.maxsize(400, 300)
        self.minsize(400, 300)
        self.title("Username Checker")
        self.textbox1 = customtkinter.CTkTextbox(self, width=300, height=220, font=app.CodeFont, text_color='gray')
        self.textbox1.insert("0.0", "Проверьте, пожалуйста, корректность следующих данных:\n"
                                    f"Ваш ник на форуме: {DataValues.lzt_name[0]}\n"
                                    f"Ссылка на вашу страницу: {DataValues.lzt_name[1]}\n"
                                    f"Ваш нынешний баланс: {DataValues.balance};\n\n"
                                    f"Если какая-либо из введённой информации неверна - нажмите на кнопку: \"Ошибка\", а затем заново введите её в соответствующем поле.")
        self.textbox1.place(x=50, y=20)
        self.confirm = customtkinter.CTkButton(self, text="Всё верно", command=self.confirmation, width=50,
                                               font=app.CodeFont,
                                               fg_color="green", hover_color="green")
        self.confirm.place(x=50, y=250)
        self.inconfirm = customtkinter.CTkButton(self, text="Ошибка", command=self.inconfirmation, width=50,
                                                 font=app.CodeFont,
                                                 fg_color="red", hover_color="red")
        self.inconfirm.place(x=290, y=250)

    def confirmation(self):
        self.destroy()
        check_number_2(True)

    def inconfirmation(self):
        self.destroy()
        DataValues.error_text += "[ERROR] | Неверный токен!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        check_number_2(False)


class ToplevelWindowLink(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.maxsize(400, 400)
        self.minsize(400, 400)
        self.title("Link Checker")
        account_info = lzt_api_get_market_list(DataValues.token, DataValues.link)
        request_log.insert("0.0",
                           f"[REQUEST] | GET {DataValues.link.replace('lzt.market', 'api.lzt.market')}\n[RESULT] | \"[TOO BIG]\"\n\n")
        self.textbox1 = customtkinter.CTkTextbox(self, width=300, height=300, font=app.CodeFont, text_color='gray')
        if account_info is None or account_info.get("totalItems") == 0:
            self.textbox1.insert("0.0",
                                 "На форуме не существует товаров, соответствующих предоставленному фильтру \ Произошла ошибка запроса из-за неверной ссылки или токена пользователя.\n\n"
                                 f"Если какая-либо из введённой информации неверна - нажмите на кнопку: \"Ошибка\", а затем заново введите её в соответствующем поле.")
        else:
            item = account_info.get("items")[
                random.randint(0, min(account_info.get("totalItems"),
                                      account_info.get("perPage")) - 1)]
            request_log.insert("0.0",
                               f"[SEMI-RESULT] | \"[{item}]\"\n\n")
            self.textbox1.insert("0.0",
                                 "Перед вами описание случайного товара с первой страницы товаров, соответствующих вашему фильтру:\n"
                                 f"Название товара: {item.get('title')}\n"
                                 f"Ссылка на страницу товара: https://lzt.market/{item.get('item_id')}/\n"
                                 f"Происхождение товара: {item.get('item_origin')}\n"
                                 f"Цена товара: {item.get('price')};\n\n"
                                 f"Если какая-либо из введённой информации неверна - нажмите на кнопку: \"Ошибка\", а затем заново введите её в соответствующем поле.")
        self.textbox1.place(x=50, y=20)
        self.confirm = customtkinter.CTkButton(self, text="Всё верно", command=self.confirmation, width=50,
                                               font=app.CodeFont,
                                               fg_color="green", hover_color="green")
        self.confirm.place(x=50, y=350)
        self.inconfirm = customtkinter.CTkButton(self, text="Ошибка", command=self.inconfirmation, width=50,
                                                 font=app.CodeFont,
                                                 fg_color="red", hover_color="red")
        self.inconfirm.place(x=290, y=350)
        print(1)

    def confirmation(self):
        self.destroy()
        check_number_3(True)

    def inconfirmation(self):
        self.destroy()
        DataValues.error_text += "[ERROR] | Неверный токен или ссылка!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        check_number_3(False)


for c in range(10):
    app.columnconfigure(index=c, weight=1)
for r in range(20):
    app.rowconfigure(index=r, weight=1)

program_name = customtkinter.CTkLabel(master=app, text=" | NEVERSELLER" * 10, bg_color="transparent", font=app.NameFont)
program_del = customtkinter.CTkLabel(master=app, text="-" * 1000, bg_color="transparent", font=app.NameFont)
program_del.place(x=0, y=20)
program_name.grid(row=0, column=0, columnspan=10, sticky="n")

program_name1 = customtkinter.CTkLabel(master=app, text=" | V 1.4.2" * 20, bg_color="transparent",
                                       font=app.NameFont)
program_del1 = customtkinter.CTkLabel(master=app, text="-" * 1000, bg_color="transparent", font=app.NameFont)
program_del1.grid(row=19, column=1, columnspan=10, sticky="s")
program_name1.grid(row=20, column=1, columnspan=10, sticky="s")

request_log = customtkinter.CTkTextbox(app, width=400, height=380, font=app.CodeFont, text_color='gray')
request_log.grid(row=16, column=1, columnspan=3, sticky='ns', padx=10)
request_label = customtkinter.CTkLabel(master=app, text="Request Logs", bg_color="transparent",
                                       font=app.Name2Font)
request_label.grid(row=16, column=1, columnspan=3, sticky="s", padx=30)

account_links = customtkinter.CTkTextbox(app, width=300, height=180, font=app.CodeFont, text_color='green')
account_links.grid(row=16, column=4, columnspan=2, sticky='n', padx=10)
account_label = customtkinter.CTkLabel(master=app, text="Account Links", bg_color="transparent",
                                       font=app.Name2Font)
account_label.grid(row=16, column=4, columnspan=2, padx=30, sticky="n", pady=155)

error_log = customtkinter.CTkTextbox(app, width=300, height=180, font=app.CodeFont, text_color='red')
error_log.grid(row=16, column=4, columnspan=2, sticky='s', padx=10)
account_label = customtkinter.CTkLabel(master=app, text="Error Logs", bg_color="transparent",
                                       font=app.Name2Font)
account_label.grid(row=16, column=4, columnspan=2, padx=30, sticky="s")

lolz_label = customtkinter.CTkLabel(master=app, text="Токен с LOLZ:", bg_color="transparent",
                                    font=app.CodeFont)
lolz_label.grid(row=16, column=6, columnspan=2, sticky="nw", padx=5)
lolz_token = customtkinter.CTkEntry(app, placeholder_text="LOLZ Token", font=app.CodeFont, width=300)
lolz_token.grid(row=16, column=7, columnspan=3, sticky="n", padx=30)

lolz_link_label = customtkinter.CTkLabel(master=app, text="Ссылка-Фильтр:", bg_color="transparent",
                                         font=app.CodeFont)
lolz_link_label.grid(row=16, column=6, columnspan=2, sticky="nw", pady=40, padx=5)
lolz_link = customtkinter.CTkEntry(app, placeholder_text="Account Filter Link", font=app.CodeFont, width=300)
lolz_link.grid(row=16, column=7, columnspan=3, sticky="n", pady=40, padx=30)

TG_id_label = customtkinter.CTkLabel(master=app, text="Telegram ID:", bg_color="transparent",
                                     font=app.CodeFont)
TG_id_label.grid(row=16, column=6, columnspan=2, sticky="nw", pady=80, padx=5)
TG_id = customtkinter.CTkEntry(app, placeholder_text="Telegram ID", font=app.CodeFont, width=300)
TG_id.grid(row=16, column=7, columnspan=3, sticky="n", pady=80, padx=30)

TG_token_label = customtkinter.CTkLabel(master=app, text="Telegram Token:", bg_color="transparent",
                                        font=app.CodeFont)
TG_token_label.grid(row=16, column=6, columnspan=2, sticky="nw", pady=120, padx=5)
TG_token = customtkinter.CTkEntry(app, placeholder_text="Telegram Bot Token", font=app.CodeFont, width=300)
TG_token.grid(row=16, column=7, columnspan=3, sticky="n", pady=120, padx=30)


def fast_slow_callback(value):
    DataValues.fastbuy = not DataValues.fastbuy


fs_buy = customtkinter.CTkSegmentedButton(app, values=["SLOW-BUY", "FAST-BUY"],
                                          command=fast_slow_callback, selected_color="gray", border_width=5,
                                          width=300, dynamic_resizing=True, selected_hover_color="gray",
                                          font=app.CodeFont)
fs_buy.set("SLOW-BUY")

fs_buy.grid(row=16, column=6, columnspan=2, sticky="n", pady=180, padx=5)


def b_check_callback(value):
    DataValues.check = not DataValues.check


b_check = customtkinter.CTkSegmentedButton(app, values=["FULL CHECK", "NO CHECK"],
                                           command=b_check_callback, selected_color="gray", border_width=5,
                                           width=400, dynamic_resizing=True, selected_hover_color="gray",
                                           font=app.CodeFont)
b_check.set("FULL CHECK")

b_check.grid(row=16, column=8, columnspan=3, sticky="nw", pady=180, padx=0)


def account_amount_callback(value):
    account_amo = value
    if value:
        progressbar_all.configure(determinate_speed=float(50) / value)
    else:
        progressbar_all.configure(determinate_speed=float(50))
    DataValues.account_amount = value
    account_amount_amo.configure(text=f"[{str(value)[:-2]}]")


account_amount = customtkinter.CTkSlider(app, from_=0, to=150, command=account_amount_callback, number_of_steps=100,
                                         width=220, button_color="gray", button_hover_color="white",
                                         progress_color="gray",
                                         )
account_amount.place(relx=0.71, rely=0.58)
account_amount.set(0)
account_amount_label = customtkinter.CTkLabel(master=app, text="Аккаунты:", bg_color="transparent",
                                              font=app.CodeFont)
account_amount_label.place(relx=0.564, rely=0.565)
account_amount_amo = customtkinter.CTkLabel(master=app, text="[0]", bg_color="transparent",
                                            font=app.CodeFont, text_color="gray")
account_amount_amo.place(relx=0.655, rely=0.565)


def preco_sleep(wait):
    timer = time.time()
    while timer + wait > time.time():  # wait is your sleep time
        pass
    return


def beautiful_step_anim(obj, time1):
    origin_speed = obj.cget("determinate_speed")
    step = float(obj.cget("determinate_speed")) / 100
    obj.configure(determinate_speed=step)
    time_to_go = float(time1) / 100
    print(time_to_go)
    for i in range(0, 100):
        obj.step()
        tkinter.Tk.after(app, int(time1))
        app.update()
    obj.configure(determinate_speed=origin_speed)


toplevel_ = None


def disable_everything():
    lolz_token.configure(state="disabled")
    lolz_link.configure(state="disabled")
    fs_buy.configure(state="disabled")
    b_check.configure(state="disabled")
    TG_id.configure(state="disabled")
    TG_token.configure(state="disabled")
    button.configure(state="disabled")
    account_amount.configure(state="disabled")


def enable_everything():
    lolz_token.configure(state="normal")
    lolz_link.configure(state="normal")
    fs_buy.configure(state="normal")
    b_check.configure(state="normal")
    TG_id.configure(state="normal")
    TG_token.configure(state="normal")
    button.configure(state="normal")
    account_amount.configure(state="normal")


def start_event():
    error_log.delete("0.0", "end")
    DataValues.token = lolz_token.get()
    DataValues.link = lolz_link.get()
    DataValues.telegram_id = TG_id.get()
    DataValues.TGtoken = TG_token.get()
    check = True
    if DataValues.token == '':
        DataValues.error_text += "[ERROR] | Отсутствует LOLZ Токен;\n"
        check = False
    if DataValues.link == '':
        DataValues.error_text += "[ERROR] | Отсутствует Фильтр-Ссылка;\n"
        check = False
    if DataValues.telegram_id == '':
        DataValues.error_text += "[ERROR] | Отсутствует Telegram ID;\n"
        check = False
    if DataValues.TGtoken == '':
        DataValues.error_text += "[ERROR] | Отсутствует Токен Telegram Бота;\n"
        check = False
    if not check:
        DataValues.error_text += "\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        return

    if DataValues.account_amount == 0:
        DataValues.error_text += "[ERROR] | Выбрано 0 аккаунтов для покупки!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        return

    try:
        DataValues.bot = telebot.TeleBot(DataValues.TGtoken)
    except:
        DataValues.error_text += "[ERROR] | Бота с данным токеном не сущестует / Вы не подключены к интернету!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        return

    try:
        DataValues.bot.send_message(chat_id=DataValues.telegram_id,
                                    text=f"<b>Данное сообщение служит для проверки корректности введённого токена бота и Telegram ID.\n</b>"
                                         f"<i>Если вам пришло данное сообщение, то это означает, что всё работает корректно.</i>\n\n"
                                         f"<i>Если вам пришло данное сообщение, то это означает, что всё работает корректно.</i>\n\n"
                                         f"<code>[NeverSeller v1.4.2]</code>",
                                    parse_mode='HTML')
    except:
        DataValues.error_text += "[ERROR] | Бота с данным токеном не сущестует / Вы не подключены к интернету!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        return

    DataValues.error_text += "[WARNING] | Пожалуйста, проверьте, свой Telegram аккаунт! Вам должно прийти сообщение от вашего бота. Если оно пришло - всё работает корректно, иначе - остановите работу программы и введите данные заново.\n\n"
    error_log.insert(text=DataValues.error_text, index="0.0")
    DataValues.error_text = ''

    DataValues.lzt_name = lzt_api_get_user_name(DataValues.token)
    print(DataValues.lzt_name)
    DataValues.balance = DataValues.lzt_name[2]
    request_log.insert("0.0", f"[REQUEST] | GET https://api.lzt.market/me\n[RESULT] | \"{DataValues.lzt_name[3]}\"\n\n")

    if DataValues.lzt_name[0] == "WRONG TOKEN / ERROR":
        DataValues.error_text += "[ERROR] | Неверный токен / Ошибка парса аккаунта / Вы не подключены к интернету!" \
                                 "\n\n[CONCLUSION] | Запуск не возможен!\n\n"
        error_log.insert(text=DataValues.error_text, index="0.0")
        DataValues.error_text = ''
        return

    if DataValues.check:
        if DataValues.toplevel_ is None or not DataValues.toplevel_.winfo_exists():
            DataValues.toplevel_ = ToplevelWindowUsername(app)
        DataValues.toplevel_.focus()
    else:
        check_number_2(True)
    return


def check_number_2(username_correct):
    if username_correct:
        disable_everything()
    else:
        return
    if DataValues.check:
        for i in range(0, 3):
            beautiful_step_anim(progressbar_request, 0.7)
            tkinter.Tk.after(app, 1000)
        progressbar_request.set(0)
        if DataValues.toplevel_ is None or not DataValues.toplevel_.winfo_exists():
            DataValues.toplevel_ = ToplevelWindowLink(app)
        DataValues.toplevel_.focus()
        return
    else:
        check_number_3(True)
    return


def check_number_3(link_correct):
    if link_correct:
        for i in range(0, 3):
            beautiful_step_anim(progressbar_request, 0.7)
            tkinter.Tk.after(app, 1000)

    else:
        enable_everything()
        return
    working()


def working():
    button.configure(text="WORKING")
    while DataValues.curr_amount < DataValues.account_amount:
        for i in range(0, 3):
            beautiful_step_anim(progressbar_request, 0.7)
            tkinter.Tk.after(app, 1000)
        accounts = lzt_api_get_market_list(DataValues.token, DataValues.link)
        request_log.insert("0.0",
                           f"[REQUEST] | {DataValues.link}.replace('lzt.market', 'api.lzt.market')\n[RESPONSE] | [TOO BIG]\n\n")
        if accounts is None:
            continue
        for iterable in range(0, min(accounts.get("totalItems"), accounts.get("perPage"))):
            item = accounts.get("items")[iterable]
            print(item)
            if DataValues.balance < item.get("price"):
                continue
            for i in range(0, 3):
                beautiful_step_anim(progressbar_request, 0.7)
                tkinter.Tk.after(app, 1000)
            res = lzt_api_buy_account(DataValues.token, item.get("item_id"), item.get("price"),
                                      DataValues.fastbuy)
            request_log.insert("0.0",
                               f"[REQUEST] | https://api.lzt.market/{item.get('item_id')}/fast-buy\n[RESPONSE] | {res}\n\n")
            if res is not False:
                request_log.insert('0.0', res)
                account_links.insert('0.0', f"https://lzt.market/{item.get('item_id')}/\n\n")
                DataValues.balance -= item.get("price")
                DataValues.money += item.get("price")
                DataValues.curr_amount += 1
                DataValues.bot.send_message(chat_id=DataValues.telegram_id,
                                            text=f"<i> - Аккаунт куплен! -\n</i>"
                                                 f"    └ <i>Название товара:</i> <code>{item.get('title')}</code>\n"
                                                 f"    └ <i>Цена товара:</i> <code>{item.get('price')}</code>\n"
                                                 f"    └ <i>Ссылка на товар:</i> https://lzt.market/{item.get('item_id')}/\n"
                                                 f"\n"
                                                 f"<i>- Обновление пользовательской информации! -</i>\n"
                                                 f"    └ <i>Ваш баланс:</i> <code>{DataValues.balance}</code>\n"
                                                 f"    └ <i>Общее кол-во денег, потраченных на аккаунты:</i> <code>{DataValues.money}</code>\n"
                                                 f"    └ <i>Куплено аккаунтов</i> <code>{DataValues.curr_amount}</code> <i>из</i> <code>{DataValues.account_amount}</code>!\n"
                                                 f"\n <code>NeverSeller v1.4.2</code>",
                                            parse_mode="html")
                progressbar_all.step()
                break
            else:
                error_log.insert("0.0", f"[LIST #{iterable}] [ACCOUNT ERROR | CHECKING NEW]")
    enable_everything()
    button.configure(text="START")


def save_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        data = {"token": lolz_token.get(),
                "link": lolz_link.get(),
                "tg_bot": TG_token.get(),
                "tg_id": TG_id.get()}
        json.dump(data, f, ensure_ascii=False, indent=4)


def open_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        DataValues.token = data["token"]
        DataValues.link = data["link"]
        DataValues.TGtoken = data["tg_bot"]
        DataValues.telegram_id = data["tg_id"]
    lolz_token.delete("0", "end")
    lolz_link.delete("0", "end")
    TG_token.delete("0", "end")
    TG_id.delete("0", "end")
    lolz_token.insert("end", DataValues.token)
    lolz_link.insert("end", DataValues.link)
    TG_token.insert("end", DataValues.TGtoken)
    TG_id.insert("end", DataValues.telegram_id)


button = customtkinter.CTkButton(app, text="START", command=start_event, width=150, font=app.NameFont,
                                 fg_color="gray", hover_color="black")
button.place(relx=0.58, rely=0.68)

save_b = customtkinter.CTkButton(app, text="SAVE", command=save_data, width=75, font=app.NameFont,
                                 fg_color="gray", hover_color="black")
save_b.place(relx=0.775, rely=0.68)

load_b = customtkinter.CTkButton(app, text="LOAD", command=open_data, width=75, font=app.NameFont,
                                 fg_color="gray", hover_color="black")
load_b.place(relx=0.88, rely=0.68)

progressbar_request = customtkinter.CTkProgressBar(app, orientation="horizontal", width=330, progress_color="gray",
                                                   determinate_speed=float(50) / 3, mode="determinate")
progressbar_request.set(0)
progressbar_request.place(relx=0.58, rely=0.78)

progressbar_all = customtkinter.CTkProgressBar(app, orientation="horizontal", width=330, progress_color="white",
                                               determinate_speed=50, mode="determinate")
progressbar_all.set(0)
progressbar_all.place(relx=0.58, rely=0.84)

app.mainloop()
