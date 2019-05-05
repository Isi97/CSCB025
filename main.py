import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.checkbox import CheckBox


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
        self.userInputRoot = GridLayout(size_hint_x=None, width=650)
        self.userInputRoot.cols = 2

        test = Label(text="Alternative / Criteria ",size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.userInputRoot.add_widget(test)

        #USER CRITERIAS
        self.userCriteration = GridLayout(size_hint_x=None, size_hint_y=None, width=450, height = 50)
        self.userCriteration.cols = self.__criteriaCount
        self.userCriteration.add_widget(Label(text="Criteria " + str(self.__criteriaCount),size_hint_x=None, width = 100))
        self.userInputRoot.add_widget(self.userCriteration) 
 
        #USE ALTERNATIVES
        self.userAlternative = GridLayout(size_hint_x=None, width=100)
        self.userAlternative.cols = 1
        self.userAlternative.add_widget(Label(text="Alternative " + str(self.__alternativeCount),size_hint_y=None, height = 50))
        self.userInputRoot.add_widget(self.userAlternative)

        #USE ALTERNATIVES INPUT
        self.userAlternativeInput = GridLayout(size_hint_x=None, width=450)
        self.userAlternativeInput.cols = 1
        self.userAlternativeInput.add_widget(TextInput(multiline=False,size_hint_y=None, height = 50,size_hint_x=None, width = 100))
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
        self.alternative = GridLayout(size_hint_y=None,size_hint_x=None, height = 100, width=155)
        self.alternative.cols = 2

        self.submit = Button(text="alternative +", font_size=25, size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.submit.bind(on_press=self.alternativePlus)
        self.alternative.add_widget(self.submit)

        self.result = Label(text="",size_hint_x=None, size_hint_y=None, width=300, height = 50, font_size=20)
        self.alternative.add_widget(self.result)

        self.submit = Button(text="alternative -", font_size=25, size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.submit.bind(on_press=self.alternativeMinus)
        self.alternative.add_widget(self.submit)

        self.add_widget(self.alternative)

        #RESULT
        resultGrid = GridLayout(size_hint_x=None, size_hint_y=None, width=200, height = 200)
        resultGrid.cols = 1
        self.submit = Button(text="CALCULATE", font_size=25, size_hint_x=None, size_hint_y=None, width=150, height = 50)
        self.submit.bind(on_press=self.calculate)
        

        btn1 = ToggleButton(text='AHP', group='method',state='down')
        btn2 = ToggleButton(text='TOPSIS', group='method' )
        resultGrid.add_widget(btn1)
        resultGrid.add_widget(btn2)

        resultGrid.add_widget(self.submit)

        self.add_widget(resultGrid)


    def criteriaPlus(self, instance):
        #name = self.name.text
        
        self.__criteriaCount += 1
        self.userCriteration.add_widget(Label(text="Criteria " + str(self.__criteriaCount),size_hint_x=None, width = 100))
        self.userCriteration.cols = self.__criteriaCount

        self.__updateUserInput(self.__alternativeCount, self.__criteriaCount-1)

        #print(self.__criteriaCount)

        #print("Name:", name)
        #self.name.text = ""

    def criteriaMinus(self, instance):
        if self.__criteriaCount == 1:
            return
        self.__criteriaCount -= 1
        self.userCriteration.cols = self.__criteriaCount
        self.userCriteration.remove_widget(self.userCriteration.children[0])

        self.__updateUserInput(self.__alternativeCount, self.__criteriaCount+1)

    def alternativePlus(self, instance):
        self.__alternativeCount += 1
        self.userAlternative.add_widget(Label(text="Alternative " + str(self.__alternativeCount),size_hint_y=None, height = 50))

        self.__updateUserInput(self.__alternativeCount-1, self.__criteriaCount)
    
    def alternativeMinus(self, instance):
        if self.__alternativeCount == 1:
            return
        self.__alternativeCount -= 1
        self.userAlternative.remove_widget(self.userAlternative.children[0])

        self.__updateUserInput(self.__alternativeCount+1, self.__criteriaCount)

    def __updateUserInput(self, oldAltCount, oldCriCount):
        toAdd = True
        if oldAltCount * oldCriCount > self.__criteriaCount * self.__alternativeCount :
            toAdd = False
        
        count = abs(oldAltCount * oldCriCount - self.__criteriaCount * self.__alternativeCount)

        for i in range(count):
            if toAdd:
                self.userAlternativeInput.add_widget(TextInput(multiline=False,size_hint_y=None, height = 50,size_hint_x=None, width = 100))
            else:
                self.userAlternativeInput.remove_widget(self.userAlternativeInput.children[0])

        self.userAlternativeInput.cols = self.__criteriaCount
    
    def calculate(self, instance):
        #print only for now
        #self.result.text += "DSADASDAS"
        self.result.text = ""

        #for i in range(self.__criteriaCount * self.__alternativeCount):
        count = 0
        for i in reversed(self.userAlternativeInput.children):
            count += 1
            self.result.text += i.text
            self.result.text += " "
            if count % self.__criteriaCount == 0:
                self.result.text += "\n"

class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()