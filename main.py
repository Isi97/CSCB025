import kivy
import pickle

from functools import partial

from kivy.app import App

from itertools import combinations

from kivy.config import Config
Config.set('graphics', 'maximize', 1)

from mathe import Solver

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from megamatrix import Criterion
from megamatrix import DecisionProblem


Window.clearcolor = (0.1, 0.11, 0.1, 1)

class Widgets(Widget):
    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)
        self.editmode = False

    def button_show_megamatrix(self):
        show_popup(self)

    def get_criteria_importance(self):
        show = GridLayout(size_hint=(1,1))
        show.rows = 2

        if (self.editmode == True ):
            show.rows = 3

        glayout = GridLayout(size_hint=(1,1))
        glayout.cols = 2

        self.ccompare = []

        comb = combinations(self.cnames_r, 2)
        for i in list(comb):
            crow = []
            crow.append(TextInput(hint_text=i[0]))
            crow.append(TextInput(hint_text=i[1]))

            self.ccompare.append(crow)

        for i in range(len(self.ccompare)):
            for j in range(len(self.ccompare[i])):
                glayout.add_widget(self.ccompare[i][j])
        

        show.add_widget(glayout)
        
        submitbutton = Button(text="Done", size_hint=(0.5, 0.2))
        submitbutton.bind(on_release=self.save_criteria_importance)

        show.add_widget(submitbutton)

        self.popupWindow = Popup(size_hint=(0.6, 0.6), title="Criteria Importance", content=show)

        if (self.editmode == True):
            retainButton = Button(text="Use previous", size_hint=(0.5, 0.2))
            retainButton.bind(on_release=self.popupWindow.dismiss)
            show.add_widget(retainButton)

        self.popupWindow.open()

    def build_solver_ui(self):
        glayout = GridLayout()
        glayout.rows = 1
        glayout.pos = (300, 0)

        btnTopsis = Button(text="TOPSIS",size_hint_x=None, width=100)
        btnWSM = Button(text="WSM",size_hint_x=None, width=100)
        btnAHP = Button(text="AHP", size_hint_x=None, width=100)
        btnReset = Button(text="Reset", size_hint_x=None, width=100)
        btnMore = Button(text="More", size_hint_x=None, width=100)

        btnWSM.bind(on_release=self.solve_wsm)
        btnAHP.bind(on_release=self.solve_ahp)
        btnTopsis.bind(on_release=self.solve_topsis)
        btnReset.bind(on_release=self.resetmegamatrix)
        btnMore.bind(on_release=self.moreOptions)

        glayout.add_widget(btnReset)
        glayout.add_widget(btnTopsis)
        glayout.add_widget(btnWSM)
        glayout.add_widget(btnAHP)
        glayout.add_widget(btnMore)

        self.editmode = True
        self.add_widget(glayout)

    def moreOptions(self, instance):
        show = GridLayout(size_hint=(1,1))
        show.rows = 3

        self.inputFname = TextInput(hint_text="File Name", size_hint=(1, 0.4), multiline=False)
        btnSave = Button(text="Save")
        btnLoad = Button(text="Load")

        btnSave.bind(on_release=self.saveproblem)
        btnLoad.bind(on_release=self.loadproblem)

        show.add_widget(self.inputFname)
        show.add_widget(btnSave)
        show.add_widget(btnLoad)

        self.popupWindow = Popup(size_hint=(0.6, 0.6), title="More Options", content=show)
        self.popupWindow.open()

    def saveproblem(self, instance):
        f = open("problems/"+self.inputFname.text, "wb")
        pickle.dump(self.problem, f)
        f.close()
        self.popupWindow.dismiss()

    def loadproblem(self, instance):
        f = open("problems/"+self.inputFname.text, "rb")
        self.problem = pickle.load(f)

        self.ids.tb_count_criteria.text = str(len(self.problem.getCriteriaNames()))
        self.ids.tb_count_alternatives.text = str(len(self.problem.alternarives))

        f.close()
        self.popupWindow.dismiss()

    def resetmegamatrix(self, instance):
        self.editmode = False

    def solve_wsm(self, instance):
        solve = Solver()

        temporary_types = []
        for i in range(len(self.cnames_r)):
            if self.cnames_r[i] == "price":
                temporary_types.append(-1)
            else:
                temporary_types.append(1)

        result = solve.wsm(decisionproblem=self.problem)
        zippedresult = zip(result, self.anames_r)
        sortedzippedresult = sorted(zippedresult, key= lambda x: x[0])

        show = FloatLayout()

        for i in range(len(sortedzippedresult)):
            #print(sortedzippedresult[i])
            l = Label(text=str(len(sortedzippedresult)-i) + ".  " + sortedzippedresult[i][1] + " - " + str(sortedzippedresult[i][0]))
            l.pos = (10, 50+(i*40) )
            show.add_widget(l)

        a = Popup(size_hint=(1, 0.8), title="MegaMatrix", content=show)
        a.open()

    def solve_ahp(self, instance):
        solve = Solver()

        temporary_types = []
        for i in range(len(self.cnames_r)):
            if self.cnames_r[i] == "price":
                temporary_types.append(-1)
            else:
                temporary_types.append(1)

        result = solve.ahp(decisionproblem = self.problem)
        zippedresult = zip(result, self.anames_r)
        sortedzippedresult = sorted(zippedresult, key= lambda x: x[0])

        show = FloatLayout()

        for i in range(len(sortedzippedresult)):
            #print(sortedzippedresult[i])
            l = Label(text=str(len(sortedzippedresult)-i) + ".  " + sortedzippedresult[i][1] + " - " + str(sortedzippedresult[i][0])  )
            l.pos = (10, 50+(i*40) )
            show.add_widget(l)

        a = Popup(size_hint=(1, 0.8), title="MegaMatrix", content=show)
        a.open()


    def solve_topsis(self, instance):
        solve = Solver()

        temporary_types = []
        for i in range(len(self.cnames_r)):
            if self.cnames_r[i] == "price":
                temporary_types.append(-1)
            else:
                temporary_types.append(1)

        result = solve.topsis(decisionproblem=self.problem)
        
        zippedresult = zip(result, self.anames_r)
        sortedzippedresult = sorted(zippedresult, key= lambda x: x[0])

        show = FloatLayout()

        for i in range(len(sortedzippedresult)):
            #print(sortedzippedresult[i])
            l = Label(text=str(len(sortedzippedresult)-i) + ".  " + sortedzippedresult[i][1] + " - " + str(sortedzippedresult[i][0]))
            l.pos = (10, 50+(i*40) )
            show.add_widget(l)

        a = Popup(size_hint=(1, 0.8), title="MegaMatrix", content=show)
        a.open()
        

    def save_criteria_importance(self, instance):
        self.criteria_importance = []

        counter = 0
        for crow in range(len(self.cnames_r)):
            row = []
            for ccol in range(len(self.cnames_r)):
                if ccol < crow:
                    row.append("recip")
                elif ccol == crow:
                    row.append(1)
                else:
                    x = float(self.ccompare[counter][0].text) / float(self.ccompare[counter][1].text)
                    counter += 1
                    row.append(x)

            self.criteria_importance.append(row)

        for i in range(len(self.criteria_importance)):
            for j in range(len(self.criteria_importance)):
                if self.criteria_importance[i][j] == "recip":
                    self.criteria_importance[i][j] = 1 / self.criteria_importance[j][i]

        App.get_running_app().criteria_importance = self.criteria_importance
        self.problem.setCImportance(self.criteria_importance)

        self.popupWindow.dismiss()
        self.build_solver_ui()


    def saveMMdata(self,instance):
        

        self.cnames_r = []
        self.mmatrix_r = []
        self.anames_r = []
        temporaryCriteriaList = []

        for i in range(len(self.cnames)):
            self.cnames_r.append(self.cnames[i].text)
            temporaryCriteriaList.append(Criterion(self.cnames[i].text, "Quantitive", "Max"))

        for i in range(len(self.mmatrix)):
            temp = []
            for j in range(len(self.mmatrix[i])):
                temp.append(self.mmatrix[i][j].text)

            self.mmatrix_r.append(temp)

        for i in self.anames:
            self.anames_r.append(i.text)


        if ( self.editmode == False ):
            self.problem = DecisionProblem(temporaryCriteriaList, self.anames_r, self.mmatrix_r)
        else:
            self.problem.criteria = temporaryCriteriaList
            self.problem.alternatives = self.anames_r
            self.problem.decisionMatrix = self.mmatrix_r


        App.get_running_app().cnames = self.cnames_r
        App.get_running_app().mmatrix = self.mmatrix_r

        self.popupWindow_mm.dismiss()
        self.get_criteria_importance()



class megamatrixApp(App):
    def build(self):
        return Widgets()

    def stop(self, *largs):
        super(megamatrixApp, self).stop(*largs)



def show_popup(self):
    show = FloatLayout()

    App.get_running_app().count_criteria = self.ids.tb_count_criteria.text
    App.get_running_app().count_alternatives = self.ids.tb_count_alternatives.text

    layoutgrid = GridLayout()
    layoutgrid.cols = 1

    inputgrid = GridLayout(size_hint_x=1, size_hint_y=1)
    inputgrid.cols = int(self.ids.tb_count_criteria.text) + 1
    rows = int(self.ids.tb_count_alternatives.text) + 1

    self.cnames = []
    self.anames = []
    self.mmatrix = []

    for i in range(rows):
        temp = []

        for j in range(inputgrid.cols):
            if i == 0 and j != 0:
                if ( self.editmode == False ):
                    self.cnames.append(TextInput(multiline=False, hint_text="Criterion Name"))
                else:
                    self.cnames.append(TextInput(multiline=False, hint_text="Criterion Name", text=self.problem.getCriteriaNames()[j-1]))

                inputgrid.add_widget(self.cnames[len(self.cnames)-1])
            elif j == 0 and i != 0:
                if (self.editmode == False):
                    self.anames.append(TextInput(multiline=False, hint_text="Alternative name"))
                else:
                    self.anames.append(TextInput(multiline=False, hint_text="Alternative name", text=self.problem.alternarives[i-1]))
                
                inputgrid.add_widget(self.anames[len(self.anames)-1])
            elif j == 0 and i == 0:
                inputgrid.add_widget(Label(text=""))
            else:
                if (self.editmode == False):
                    temp.append(TextInput(multiline=False, hint_text="Value"))
                else:
                    temp.append(TextInput(multiline=False, hint_text="Value", text=str(self.problem.decisionMatrix[i-1][j-1])))
                
                inputgrid.add_widget(temp[len(temp)-1])

        if len(temp) != 0:
            self.mmatrix.append(temp)

    layoutgrid.add_widget(inputgrid)

    self.btnrdy = Button(text="Ready", size_hint=(0.25,0.25))
    self.btnrdy.bind(on_release=self.saveMMdata)
    layoutgrid.add_widget(self.btnrdy)

    show.add_widget(layoutgrid)

    self.popupWindow_mm = Popup(size_hint=(1, 1), title="MegaMatrix", content=show)
    self.popupWindow_mm.open()

if __name__ == "__main__":
    megamatrixApp().run()
