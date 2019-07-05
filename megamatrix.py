class Criterion:
    def __init__(self, name, critType, minMax):
        self.name = name
        self.critType = critType
        self.minMax = minMax


class DecisionProblem:
    def __init__(self, clist, alist, decisionM):
        self.criteria = clist
        self.alternarives = alist  # list of strings
        self.decisionMatrix = decisionM

    def setCImportance(self, c_importance):
        self.criteria_importance = c_importance

    def getCriterionTypes(self):
        temp = []
        for i in self.criteria:
            temp.append(i.critType)
        
        return temp

    def getCriteriaNames(self):
        temp = []
        for i in self.criteria:
            temp.append(i.name)
        
        return temp

    def getCriteriaMinOrMax(self):
        temp = []
        for i in self.criteria:
            temp.append(i.minMax)
        
        return temp