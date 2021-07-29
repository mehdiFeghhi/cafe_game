import random
import threading
import time

import schedule
from pyrogram import Client
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent, Message, ReplyKeyboardRemove
import pymongo
import pickle
import X_O
import datetime


class MyUser:
    def __init__(self, user_id, name=None, win=0, draw=0, lose=0, state=0):
        self.id = user_id
        self.state = state
        self.name = name
        self.Win = win
        self.Draw = draw
        self.Lose = lose

    def __str__(self):
        return "Name    " + "Win    " + "Draw   " + "Lose  " + "\n\n" + str(self.name) + "\n" + "     " + str(
            self.Win) + "    " + str(self.Draw) + "    " + str(self.Lose)


def IKM(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, cbd)] for text, cbd in data])


def test_game():
    number_one = input("number one code : ")
    number_two = input("number two code : ")
    name1 = input("name1: ")
    name2 = input("name2: ")
    game = X_O.XO((number_one, name1), (number_two, name2))

    while not game.end:
        game.show_ground()
        number_player = input("number player : ")
        place = input("enter number of place you want to select: ")
        recive = game.move(number_player, int(place) - 1)


def run_bot():
    client = Client('mybot')
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    member_data = mydb["Cafe_game"]

    return client, member_data


def make_new_name(mongo, name):
    f = mongo.find({}, {"name": name})
    if f is None:
        number = 1
        while (mongo.find({}, {"name": name + str(number)})) is not None:
            number += 1
        return name + str(number)

    else:
        return name


def chang_to_print(new_data):
    str_outPut = "\n" + "Name    " + "Win    " + "Draw   " + "Lose  "
    str_outPut = str_outPut
    i = 0
    for data in new_data:
        if i == 10:
            return str_outPut
        else:
            str_outPut += "\n\n" + str(data.get("name")) + "\n" + "     " + str(data.get("Num_Win")) + "    " + str(
                data.get("Num_Draw")) + "    " + str(data.get("Num_Lose"))
            i += 1
    return str_outPut


def cleaner(id_inline_str, game_handler, dict_game):
    if id_inline_str in game_handler.keys():
        game_handler.pop(id_inline_str)
    if id_inline_str in dict_game.keys():
        dict_game.pop(id_inline_str)


def win_save(member_data, winer, loser):
    number_win = member_data.find_one({"_id": winer}).get("Num_Win") + 1
    member_data.update_one({"_id": winer}, {"$set": {"Num_Win": number_win}})

    number_Lose = member_data.find_one({"_id": loser}).get("Num_Lose") + 1
    member_data.update_one({"_id": loser}, {"$set": {"Num_Lose": number_Lose}})


def draw_save(member_data, draw1, draw2):
    number_Draw = member_data.find_one({"_id": draw1}).get("Num_Draw") + 1
    member_data.update_one({"_id": draw1}, {"$set": {"Num_Draw": number_Draw}})

    number_Draw2 = member_data.find_one({"_id": draw2}).get("Num_Draw") + 1
    member_data.update_one({"_id": draw2}, {"$set": {"Num_Draw": number_Draw2}})


def bot_do_job(game_handler, bot, member_data, dict_game):
    def save_in_data_base(id_cliet, first_name, last_name):
        if first_name is None:
            first_name = " "
        if last_name is None:
            last_name = " "
        new_name = make_new_name(member_data,
                                 first_name + " " + last_name)

        mydict = {"_id": id_cliet, "name": new_name, "Num_Win": 0, "Num_Draw": 0,
                  "Num_Lose": 0, "state": 0}
        member_data.insert_one(mydict)

    @bot.on_message()
    def my_handler(client: Client, message: Message):
        name = message.from_user.first_name
        last_name = message.from_user.last_name
        if name is None:
            name = " "
        if last_name is None:
            last_name = " "
        new_name = make_new_name(member_data,
                                 name + " " + last_name)

        user = check_user(message.from_user.id, new_name)
        if message.chat.type != 'private':
            return
        if message.text:
            if message.text == '/start':
                f = member_data.find_one({"_id": str(message.from_user.id)})
                if f is not None:
                    print(user.id)
                    client.send_message(message.from_user.id,
                                        "سلام" + "\n" + user.name + "\n" + "در خدمت هستم.😊",
                                        reply_markup=ReplyKeyboardMarkup([['دیدن لیست برترین ها', 'تغییر نام کاربری']],
                                                                         resize_keyboard=True))
                else:
                    mydict = {"_id": str(message.from_user.id), "name": user.name, "Num_Win": 0, "Num_Draw": 0,
                              "Num_Lose": 0, "state": 0}
                    member_data.insert_one(mydict)

                    client.send_message(message.from_user.id,
                                        f" اسم شما شما در حال حاظر{user.name} در نظر گرفتیم .\nاگر اسمت رو دوست نداری میتونم اسمت رو تغییر بدم. ",
                                        reply_markup=ReplyKeyboardMarkup([['از اسمم راضی هستم', 'تغییر نام کاربری']],
                                                                         resize_keyboard=True))


            elif message.text == 'دیدن لیست برترین ها':

                new_data = member_data.find().sort("Num_Win", -1)
                str_greater = chang_to_print(new_data)
                finall_str = "وضعیت شما :" + "\n" + str(user) + "\n نفرات برتر:" + str_greater + "\n\n"
                print(user.id)

                client.send_message(message.from_user.id, finall_str)

            elif message.text == 'از اسم قبلیم راضی هستم' or message.text == 'از اسمم راضی هستم':
                user.state = 0
                client.send_message(message.from_user.id, "با موفقیت ثبت نام شدید.❤️",
                                    reply_markup=ReplyKeyboardMarkup([['دیدن لیست برترین ها', 'تغییر نام کاربری']]))

            elif message.text == 'تغییر نام کاربری' or message.text == 'تلاش برای ایجاد یک نام جدید':

                user.state = 1
                member_data.update_one({"_id": str(user.id)}, {"$set": {"state": 1}})
                f = member_data.find_one({"_id": str(user.id)})
                client.send_message(message.from_user.id, "دوست داری توی بازی چه اسمی داشته باشی ؟",
                                    reply_markup=ReplyKeyboardRemove())

            elif user.state == 1:
                new_name = message.text
                find_name = make_new_name(member_data, new_name)
                user.state = 0
                member_data.update_one({"_id": str(user.id)}, {"$set": {"state": 0}})
                if new_name == find_name:
                    member_data.update_one({"_id": str(user.id)}, {"$set": {"name": new_name}})
                    client.send_message(message.from_user.id, "با موفقیت ثبت نام شدید.❤️")
                    user.name = new_name

                else:

                    client.send_message(user.id, 'متاسفانه اسم شما قبلا توسط یکی دیگر استفاده شده است.',
                                        reply_markup=ReplyKeyboardMarkup(
                                            [['تلاش برای ایجاد یک نام جدید'], ['از اسم قبلیم راضی هستم']],
                                            resize_keyboard=True))


            else:

                print(user.state)

    @bot.on_callback_query()
    def handle_callback_query(client: Client, query: CallbackQuery):
        id_cliet = str(query.from_user.id)
        id_inline = query.inline_message_id
        id_inline_str = str(id_inline)
        if query.data == 'start':
            client.edit_inline_text(id_inline, 'بازی موردنظر خودت رو از لیست بازی‌های زیر انتخاب کن:',
                                    reply_markup=IKM([('تیک تک تو', 'X_O')]))

        elif query.data == 'X_O':

            f = member_data.find_one({"_id": id_cliet})
            if f is None:
                save_in_data_base(id_cliet, query.from_user.first_name, query.from_user.last_name)
                f = member_data.find_one({"_id": id_cliet})
            name = f.get('name')
            game_handler[id_inline_str] = [(id_cliet, name)]

            with open('X_O_helper.text') as file:
                text = file.read()

            client.edit_inline_text(id_inline, text=text, reply_markup=IKM([(
                f' آره میخوام با  {name} بازی کنم 🙂.  ', 'X_O_start'),
                ("نه بابا مگه بیکارم 😂", "end_from_your_partner")]))


        elif query.data == 'X_O_start':

            if len(game_handler.get(id_inline_str)) == 1:
                f = member_data.find_one({"_id": id_cliet})
                if f is not None and id_cliet not in game_handler.get(id_inline_str)[:][0]:
                    name = f.get("name")
                    list_me = game_handler.pop(id_inline_str)
                    game_handler[id_inline_str] = list_me + [
                        (id_cliet, name)]

                    if random.randint(0, 1) == 0:
                        player_one = game_handler.get(id_inline_str)[0]
                        player_two = game_handler.get(id_inline_str)[1]
                    else:
                        player_one = game_handler.get(id_inline_str)[1]
                        player_two = game_handler.get(id_inline_str)[0]

                    game = X_O.XO(player_one, player_two)

                    dict_game[id_inline_str] = game

                    client.edit_inline_text(id_inline,
                                            text="💐  کافه گیم  💐" + "\n" + "player_one: " + player_one[
                                                1] + "\n" + "player_two: " + player_two[1],
                                            reply_markup=game.show_markup())

                elif id_cliet in game_handler.get(id_inline_str)[:][0]:
                    client.answer_callback_query(query.id, "this game must be have two player !!!")
                    print("No NO NO")

                else:
                    name = query.from_user.first_name
                    last_name = query.from_user.last_name
                    save_in_data_base(id_cliet, name, last_name)
                    list_me = game_handler.pop(id_inline_str)
                    new_name = member_data.find_one({"_id": id_cliet}).get("name")
                    game_handler[id_inline_str] = list_me + [
                        (id_cliet, new_name)]

                    if random.randint(0, 1) == 0:
                        player_one = game_handler.get(id_inline_str)[0]
                        player_two = game_handler.get(id_inline_str)[1]
                    else:
                        player_one = game_handler.get(id_inline_str)[1]
                        player_two = game_handler.get(id_inline_str)[0]

                    game = X_O.XO(player_one, player_two)

                    dict_game[id_inline_str] = game

                    client.edit_inline_text(id_inline,
                                            text="💐  کافه گیم  💐" + "\n" + "player_one: " + player_one[
                                                1] + "\n" + "player_two: " + player_two[1],
                                            reply_markup=game.show_markup())


            elif len(game_handler.get(id_inline_str)) == 2:

                if random.randint(0, 1) == 0:
                    player_one = game_handler.get(id_inline_str)[0]
                    player_two = game_handler.get(id_inline_str)[1]
                else:
                    player_one = game_handler.get(id_inline_str)[1]
                    player_two = game_handler.get(id_inline_str)[0]

                game = X_O.XO(player_one, player_two)

                dict_game[id_inline_str] = game

                client.edit_inline_text(id_inline,
                                        text="💐  کافه گیم  💐" + "\n" + "player_one: " + player_one[
                                            1] + "\n" + "player_two: " + player_two[1],
                                        reply_markup=game.show_markup())



        elif 'CH_X_O' in query.data:
            place = int(query.data.split('_')[-1]) - 1

            game: X_O.XO = dict_game.get(id_inline_str)
            move_describtion = game.move(id_cliet, place)
            if game.win[0]:

                win_save(member_data, winer=game.win[1][0], loser=game.win[2][0])
                client.answer_callback_query(query.id, move_describtion[0])
                bot.edit_inline_text(id_inline,
                                     text="💐 کافه گیم  💐" + "\n" +
                                          move_describtion[0], reply_markup=game.show_markup_End())
            elif game.draw[0]:

                draw_save(member_data, game.draw[1][0], game.draw[2][0])
                client.answer_callback_query(query.id, move_describtion[0])
                client.edit_inline_text(id_inline,
                                        text="💐  کافه گیم  💐" + "\n" + move_describtion[0],
                                        reply_markup=game.show_markup_End()
                                        )


            elif move_describtion[1] and not game.win[0]:

                client.edit_inline_text(id_inline,
                                        text="💐  کافه گیم  💐",
                                        reply_markup=game.show_markup())

            else:
                client.answer_callback_query(query.id, move_describtion[0])
                client.edit_inline_text(id_inline,
                                        "💐  کافه گیم  💐", reply_markup=game.show_markup())

        elif query.data == "end_show_in_playing":

            if id_cliet in game_handler.get(id_inline_str)[:][0] or \
                    id_cliet in game_handler.get(id_inline_str)[:][1]:

                if id_inline_str in game_handler.keys():
                    game_handler.pop(id_inline_str)
                if id_inline_str in dict_game:
                    dict_game.pop(id_inline_str)

                name = query.from_user.first_name + " " + query.from_user.last_name
                client.edit_inline_text(id_inline,
                                        text=name + "\n" + " رغبتی برای بازی باشما ندارد 😒 ")


        elif query.data == "end_from_your_partner":

            cleaner(id_inline_str, game_handler, dict_game)
            name = query.from_user.first_name + " " + query.from_user.last_name
            client.edit_inline_text(id_inline,
                                    text=name + "\n به بازی خاتمه داد !! 😒  \n")

        elif query.data == 'end':
            cleaner(id_inline_str, game_handler, dict_game)
            client.edit_inline_text(id_inline, 'بازی تمام شد!!')

    @bot.on_inline_query()
    def handle_inline_query(client: Client, query: InlineQuery):

        if not query.query:
            return
        results = [InlineQueryResultArticle('ورود به بازی ها', InputTextMessageContent('🌺 به کافه گیم خوش آمدید 🌺'),
                                            reply_markup=IKM(
                                                [('انتخاب بازی ها', 'start'), ('خسته‌ام خداحافظ', "end")]))]

        client.answer_inline_query(query.id, results)

    def check_user(user_id, name):
        f = member_data.find_one({"_id": str(user_id)})
        if f is not None:
            return MyUser(f.get("_id"), f.get("name"), f.get("Num_Win"), f.get("Num_Draw"), f.get("Num_Lose"),
                          f.get("state"))

        new_user = MyUser(user_id, name)

        return new_user

    bot.run()


def save_game(dict_game, game_handler):
        outfile = open("game", 'wb')
        save_one = dict_game.copy()
        pickle.dump(save_one, outfile)
        outfile.close()
        print(dict_game)

        save_two = game_handler.copy()
        outfile_2 = open("helper", 'wb')
        pickle.dump(save_two, outfile_2)
        outfile_2.close()
        print(game_handler)


def first_open():
    try:
        infile = open("game", 'rb')
        dict_game = pickle.load(infile)
        infile.close()
    except:
        dict_game = {}
        outfile = open("game", 'wb')
        pickle.dump({}, outfile)
        outfile.close()

    try:
        infile_2 = open("helper", "rb")
        game_handler = pickle.load(infile_2)
        infile_2.close()
    except:
        game_handler = {}
        outfile_2 = open("helper", 'wb')
        pickle.dump({}, outfile_2)
        outfile_2.close()

    return dict_game, game_handler


def use_theard(dict_game,game_handler):

    schedule.every(40).seconds.do(save_game,dict_game= dict_game,game_handler= game_handler)
    while True:
        schedule.run_pending()
        time.sleep(20)




def main():
    dict_game, game_handler = first_open()
    bot, member_data = run_bot()
    # thread = threading.Thread(target=use_theard,args=
    # (dict_game,game_handler,))
    # thread.start()
    bot_do_job(game_handler,bot,member_data,dict_game)
if __name__ == '__main__':
    main()
