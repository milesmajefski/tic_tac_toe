import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from collections import namedtuple
kivy.require('1.11.1')  # replace with your current kivy version ! v1.11.1

UserTuple = namedtuple('UserTuple', ['text', 'value'])


class UserTypes:
    X = UserTuple('X', 1)
    O = UserTuple('O', -1)


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
        self._currentuserindex = 0
        self._users = [self._first_user, self._second_user]
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
                square.bind(on_press=self.click_square)

        return layout

    def click_square(self, instance):
        if instance.value:
            return

        instance.text = self.get_current_user().text
        instance.value = self.get_current_user().value
        print(f'r,c: {instance.row}, {instance.column}')
        self.print_state()

        # switch users
        self._switch_users()

    def _switch_users(self):
        self._currentuserindex += 1
        self._currentuserindex %= len(self._users)

    def get_current_user(self):
        return self._users[self._currentuserindex]

    def print_state(self):
        for i in self._gamestate:
            for j in i:
                print(f'{j.value:>3}', end=' ')
            print()


if __name__ == '__main__':
    MyApp().run()
