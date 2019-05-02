import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle



class MyGrid(GridLayout):
    __criteriaCount = 1
    __alternativeCount = 1

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2

        #self.width = 1000
        #self.height = 1000

        #with self.canvas:
            #Color(.3, .4, .8, 0.5)
            #self.rect = Rectangle(size=self.size,pos=self.pos)

        #USER INPUT GRID
        self.userInputRoot = GridLayout(size_hint_x=None, size_hint_y=None, width=500, height = 400)
        self.userInputRoot.cols = 2

        test = Label(text="Alternative / Criteria ",size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.userInputRoot.add_widget(test)

        #USER CRITERIAS
        self.userCriteration = GridLayout(size_hint_x=None, size_hint_y=None, width=450, height = 50)
        self.userCriteration.cols = self.__criteriaCount
        self.userCriteration.add_widget(Label(text="Criteria " + str(self.__criteriaCount),size_hint_x=None, width = 100))
        self.userInputRoot.add_widget(self.userCriteration) 
 
        #USE ALTERNATIVES
        self.userAlternative = GridLayout(size_hint_x=None, size_hint_y=None, width=100, height = 500)
        self.userAlternative.cols = 1
        self.userAlternative.add_widget(Label(text="Alternative " + str(self.__alternativeCount),size_hint_y=None, height = 50))
        self.userInputRoot.add_widget(self.userAlternative)

        #USE ALTERNATIVES INPUT
        self.userAlternativeInput = GridLayout(size_hint_x=None, size_hint_y=None, width=100, height = 500)
        self.userAlternativeInput.cols = 1
        self.userAlternativeInput.add_widget(TextInput(multiline=False,size_hint_y=None, height = 50))
        self.userInputRoot.add_widget(self.userAlternativeInput)

        #TextInput(multiline=False)

        #ADD USER INPUT
        self.add_widget(self.userInputRoot)

        #CRITERATION BUTTONS
        self.criteration = GridLayout()
        self.criteration.cols = 1

        self.submit = Button(text="criteria +", font_size=30, size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.submit.bind(on_press=self.criteriaPlus)
        self.criteration.add_widget(self.submit)

        self.submit = Button(text="criteria -", font_size=30, size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.submit.bind(on_press=self.criteriaMinus)
        self.criteration.add_widget(self.submit)

        self.add_widget(self.criteration)

        #ALTERNATIVE BUTTONS
        self.alternative = GridLayout()
        self.alternative.cols = 1

        self.submit = Button(text="alternative +", font_size=30, size_hint_x=None, size_hint_y=None, width=170, height = 50)
        self.submit.bind(on_press=self.alternativePlus)
        self.alternative.add_widget(self.submit)

        self.submit = Button(text="alternative -", font_size=30, size_hint_x=None, size_hint_y=None, width=170, height = 50)
        self.submit.bind(on_press=self.alternativeMinus)
        self.alternative.add_widget(self.submit)

        self.add_widget(self.alternative)


    def criteriaPlus(self, instance):
        #name = self.name.text
        
        self.__criteriaCount += 1
        self.userCriteration.add_widget(Label(text="Criteria " + str(self.__criteriaCount),size_hint_x=None, width = 100))
        self.userCriteration.cols = self.__criteriaCount

        #print(self.__criteriaCount)

        #print("Name:", name)
        #self.name.text = ""

    def criteriaMinus(self, instance):
        if self.__criteriaCount == 1:
            return
        self.__criteriaCount -= 1
        self.userCriteration.cols = self.__criteriaCount
        self.userCriteration.remove_widget(self.userCriteration.children[0])

    def alternativePlus(self, instance):
        self.__alternativeCount += 1
        self.userAlternative.add_widget(Label(text="Alternative " + str(self.__alternativeCount),size_hint_y=None, height = 50))
    
    def alternativeMinus(self, instance):
        if self.__alternativeCount == 1:
            return
        self.__alternativeCount -= 1
        self.userAlternative.remove_widget(self.userAlternative.children[0])


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()