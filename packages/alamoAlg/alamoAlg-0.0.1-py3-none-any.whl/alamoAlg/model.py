import numpy as np

class alamoModel:
    #initializing model with input parameters and data
    def __init__(self, currErrorBound, currMaxIter, currInitialData, currTargetVector):
        self.errorBound = currErrorBound
        self.maxIter = currMaxIter
        self.initialData = currInitialData
        self.trainingSet = currInitialData          #training set is initially set to the initial data
        self.targetVector = currTargetVector


    #function to perform adaptive sampling
    def adaptiveSampling(self, currN):
        print(currN)

    #function to update the training set
    def updateTrainingSet(self, currN):
        print(currN)

    def checkErrorBound(self):
        print(f"checking inequality compared to error bound {self.errorBound}")

    def runSimulation(self):
        self.checkErrorBound()
        self.checkErrorBound()


