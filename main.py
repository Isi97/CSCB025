import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyGrid(GridLayout):
    __criteriaCount = 1

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2

        #USER INPUT GRID
        self.userInputRoot = GridLayout()
        self.userInputRoot.cols = 1

        self.userCriteration = GridLayout()
        self.userCriteration.cols = self.__criteriaCount

        self.userCriteration.add_widget(Label(text="Criteria " + str(self.__criteriaCount)))
        
        self.userInputRoot.add_widget(self.userCriteration)
        
        self.name = TextInput(multiline=False)
        self.userInputRoot.add_widget(self.name)

        self.add_widget(self.userInputRoot)

        #CRITERATION BUTTONS
        self.criteration = GridLayout()
        self.criteration.cols = 2

        self.submit = Button(text="criteria +", font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.criteration.add_widget(self.submit)

        self.submit = Button(text="criteria -", font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.criteration.add_widget(self.submit)

        self.add_widget(self.criteration)

        #ALTERNATIVE BUTTONS
        self.alternative = GridLayout()
        self.alternative.cols = 2

        self.submit = Button(text="alternative +", font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.alternative.add_widget(self.submit)

        self.submit = Button(text="alternative -", font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.alternative.add_widget(self.submit)

        self.add_widget(self.alternative)


    def pressed(self, instance):
        name = self.name.text

        self.userInputRoot.add_widget(Label(text="Email2222: "))
        self.email = TextInput(multiline=False)
        self.userInputRoot.add_widget(self.email)

        print("Name:", name)
        self.name.text = ""

class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()