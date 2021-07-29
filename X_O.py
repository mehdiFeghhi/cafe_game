from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class XO:

    def __init__(self, user_one, user_two):
        print(user_one)
        self.ground = [[" ", " ", " "] for i in range(3)]
        self.number_of_move = 0
        self.user_id_one = user_one[0]
        self.user_id_two = user_two[0]
        self.user_name_one = user_one[1]
        self.user_name_two = user_two[1]
        self.type_shape = {
            str(user_one[0]): 'O',
            str(user_two[0]): 'X'
        }
        self.step_player = (user_one, user_two)

        self.win = (False, (user_one), (user_two))
        self.draw = (False, (user_one), (user_two))
        self.end = False

    def move(self, user_id, place):

        if not self.win[0] and str(self.step_player[0][0]) == str(user_id) and self.ground[place // 3][place % 3] == " ":

            self.ground[place // 3][place % 3] = self.type_shape.get(str(user_id))
            self.number_of_move += 1
            print(self.number_of_move)
            self.step_player = (self.step_player[1], self.step_player[0])

            if self.is_win(self.step_player[1], self.step_player[0]):
                return [f"user {self.win[1][1]} win", True, self.ground]

            elif self.number_of_move == 9:
                self.draw = (True, self.step_player[0], self.step_player[1])
                return ["Draw game", False, self.ground]

            else:
                return [f"user{self.step_player[0][1]} do your act", True, self.ground]


        elif self.win[0]:
            return [f"this game wad ended because user{self.win[1][1]} wined", False, self.ground]


        elif self.number_of_move == 9:
            print("hi")
            self.draw = (True, self.step_player[0], self.step_player[1])
            return ["this game was ended because there isn't any choice for each player", False, self.ground]


        elif str(self.step_player[0][0]) != str(user_id):
            print(user_id)
            print(self.step_player[0][0])
            return [f"Wrong!!! \n Player {self.step_player[0][1]} must be choice.", False, self.ground]


        elif self.ground[place // 3][place % 3] != " ":
            return ["this place is not empty !!!", False, self.ground]

    def is_win(self, user_Win, user_Los):

        if self.ground[0][0] == self.ground[0][1] == self.ground[0][2] != ' ' or \
                self.ground[0][0] == self.ground[1][0] == self.ground[2][0] != ' ' or \
                self.ground[0][0] == self.ground[1][1] == self.ground[2][2] != ' ' or \
                self.ground[0][1] == self.ground[1][1] == self.ground[2][1] != ' ' or \
                self.ground[1][0] == self.ground[1][1] == self.ground[1][2] != ' ' or \
                self.ground[0][2] == self.ground[1][1] == self.ground[2][0] != ' ' or \
                self.ground[2][0] == self.ground[2][1] == self.ground[2][2] != ' ' or \
                self.ground[0][2] == self.ground[1][2] == self.ground[2][2] != ' ':

            self.win = (True, user_Win, user_Los)
            return True
        else:
            return False

    def show_ground(self):

        for i in self.ground:
            print(' | '.join(i))

            print("_   _   _  ")

    def show_markup(self):

        return InlineKeyboardMarkup([[InlineKeyboardButton(change_type(self.ground[0][0]), "CH_X_O_1"),
                                      InlineKeyboardButton(change_type(self.ground[0][1]), "CH_X_O_2"),
                                      InlineKeyboardButton(change_type(self.ground[0][2]), "CH_X_O_3")]
                                        , [InlineKeyboardButton(change_type(self.ground[1][0]), "CH_X_O_4"),
                                           InlineKeyboardButton(change_type(self.ground[1][1]), "CH_X_O_5"),
                                           InlineKeyboardButton(change_type(self.ground[1][2]), "CH_X_O_6")],
                                     [InlineKeyboardButton(change_type(self.ground[2][0]), "CH_X_O_7")
                                         , InlineKeyboardButton(change_type(self.ground[2][1]), "CH_X_O_8"),
                                      InlineKeyboardButton(change_type(self.ground[2][2]), "CH_X_O_9")
                                      ],
                                     [InlineKeyboardButton("End Game !!!", 'end_show_in_playing')]]
                                    )

    def show_markup_End(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton(change_type(self.ground[0][0]),"do_no_action"),
                                      InlineKeyboardButton(change_type(self.ground[0][1]), "do_no_action"),
                                      InlineKeyboardButton(change_type(self.ground[0][2]), "do_no_action")]
                                        , [InlineKeyboardButton(change_type(self.ground[1][0]), "do_no_action"),
                                           InlineKeyboardButton(change_type(self.ground[1][1]), "do_no_action"),
                                           InlineKeyboardButton(change_type(self.ground[1][2]), "do_no_action")],
                                     [InlineKeyboardButton(change_type(self.ground[2][0]), "do_no_action")
                                         , InlineKeyboardButton(change_type(self.ground[2][1]), "do_no_action"),
                                      InlineKeyboardButton(change_type(self.ground[2][2]), "do_no_action")
                                      ],
                                     [InlineKeyboardButton("End show !!!", 'end'),
                                      InlineKeyboardButton("شروع مجدد بازی", 'X_O_start')]]
                                    )


# return InlineKeyboardMarkup([[InlineKeyboardButton(text, cbd)] for text, cbd in data])

def change_type(string1):
    if string1 == 'O':
        return '🍎'
    elif string1 == 'X':
        return '🥭'
    else:
        return " "
