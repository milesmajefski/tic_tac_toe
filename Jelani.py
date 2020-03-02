import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from collections import namedtuple

kivy.require("1.11.1")  # replace with your current kivy version !
UserTuple = namedtuple("UserTuple", ["text", "value"])


class UserTypes:
    X = UserTuple("X", 1)
    O = UserTuple("O", -1)


class User:
    def __init__(self, user_tuple):
        self.text = user_tuple.text
        self.value = user_tuple.value


class Square(Button):
    def __init__(self, row, column, *args, **kwargs):
        self.value = 0
        self.row = row
        self.column = column
        super().__init__(*args, **kwargs)


class MyApp(App):
    def __init__(self, *args, **kwargs):
        self._gamestate = []
        self._first_user = User(UserTypes.X)
        self._second_user = User(UserTypes.O)
        self._currentuserIndex = 0
        self._users = [self._first_user, self._second_user]
        self.winner = False
        super().__init__(*args, **kwargs)

    def build(self):
        layout = self.generate_layout()
        return layout

    def generate_layout(self):
        layout = GridLayout(cols=3)
        for i in range(3):
            self._gamestate.append([])
            for j in range(3):
                square = Square(row=i, column=j)
                self._gamestate[i].append(square)
                layout.add_widget(square)
                square.bind(on_press=self.click_button)
        return layout

    def click_button(self, instance):
        # if this square has already been clicked
        if instance.value:
            return
        # If there is already a winner
        if self.winner:
            self.stop()
            return

        instance.text = self.get_current_user().text
        instance.value = self.get_current_user().value
        print(f"r,c: {instance.row}, {instance.column}")
        # switch user
        self._switch_users()
        self.print_state()
        self.win_check()

    def _switch_users(self):
        self._currentuserIndex += 1
        self._currentuserIndex %= len(self._users)

    def get_current_user(self):
        return self._users[self._currentuserIndex]

    def print_state(self):
        for i in self._gamestate:
            for j in i:
                print(f"{j.value:>3}", end=" ")
            print()

    def sum_squares(self, squares):
        total = 0
        for s in squares:
            total += s.value
        return total

    ### Make a list that is the first item from 3 lists
    def multilist_getter(self, lists, offset, step):
        for sublist in lists:
            yield sublist[offset]
            offset += step

    def win_check(self):
        gs = self._gamestate
        results = []

        # row results
        for i in range(3):
            results.append(self.sum_squares(gs[i]))

        # column results
        for i in range(3):
            results.append(self.sum_squares(self.multilist_getter(gs, i, 0)))

        # diagonal results
        results.append(self.sum_squares(self.multilist_getter(gs, 0, 1)))
        results.append(self.sum_squares(self.multilist_getter(gs, 2, -1)))

        if 3 in results:
            print('-- x wins')
            self.winner = True
        elif -3 in results:
            print('-- o wins')
            self.winner = True
        else:
            print('-- no winner')

        # check the rows
        row1 = gs[0][0].value + gs[0][1].value + gs[0][2].value
        row2 = gs[1][0].value + gs[1][1].value + gs[1][2].value
        row3 = gs[2][0].value + gs[2][1].value + gs[2][2].value
        # check the columns
        col1 = gs[0][0].value + gs[1][0].value + gs[2][0].value
        col2 = gs[0][1].value + gs[1][1].value + gs[2][1].value
        col3 = gs[0][2].value + gs[1][2].value + gs[2][2].value
        # check the diagonals
        diag1 = gs[0][0].value + gs[1][1].value + gs[2][2].value
        diag2 = gs[0][2].value + gs[1][1].value + gs[2][0].value

        if (
            row1 == 3
            or row2 == 3
            or row3 == 3
            or col1 == 3
            or col2 == 3
            or col3 == 3
            or diag1 == 3
            or diag2 == 3
        ):
            print("== First User wins")
            self.winner = True
        elif (
            row1 == -3
            or row2 == -3
            or row3 == -3
            or col1 == -3
            or col2 == -3
            or col3 == -3
            or diag1 == -3
            or diag2 == -3
        ):
            print("== Second User wins")
            self.winner = True
        else:
            print("== No winner")


if __name__ == "__main__":
    MyApp().run()
