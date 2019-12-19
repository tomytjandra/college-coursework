# LIBRARY FOR UI
from PyQt5 import QtCore, QtGui, QtWidgets
import decimal

# LIBRARY FOR IMPORT EXPORT
import pandas as pd
import os

# LIBRARY FOR COMPUTATION
import numpy as np
import math
from random import random

# LIBRARY FOR PLOTTING
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import mplcursors
from mpldatacursor import datacursor

# SETTINGS
np.set_printoptions(formatter={'float_kind':'{:f}'.format}) # scientific to float

# PARENT CLASS MATH MODEL
class TumorGrowth():
    def __init__(self, **kwargs):
        # SET PARAMETERS
        allowed_param = ['growthType', 'L1', 'L2', 'L3', 'Dg', 'Dw', 'x0', 'C0', 'rho', 'tf']
        self.__dict__.update((key, val) for key, val in kwargs.items() if key in allowed_param)
    
        self.xf = self.L1 + self.L2 + self.L3 # spatial axis
        # DISCRETIZATION
        self.dx = 0.5 # space step
        self.dt = 1 # time step
        self.nx = int(self.xf/self.dx) + 1 # no. of space grid P
        self.nt = int(self.tf/self.dt) + 1 # no. of time grid Q

        # RESULT MATRIX
        self.C = np.zeros((self.nt, self.nx)) # concentration, C(t,x)

        # INITIAL CONDITION
        for j in range(self.nx):
            # GAUSSIAN INITIAL TUMOR PROFILE
            self.C[0, j] = self.C0 * np.exp(-0.5*np.power((j*self.dx - self.x0)*(math.sqrt(2*math.pi) * self.C0), 2))
            
        # ZONE POINT (FOR SPLITTING)
        self.zone_point = [0,
                           int(self.L1/self.dx),
                           int((self.L1+self.L2)/self.dx),
                           self.nx-1]

        # TEMPORARY VARIABLE FOR NEWTON ITERATION
        self.R = self.dt/(2*self.dx**2)
        self.S = self.dt*self.rho/2

    # SPATIAL HETEROGENEITY
    def coefD(self, j):
        x = j*self.dx
        if 0 <= x <= self.L1:
            return self.Dg # Grey region
        elif x <= self.L1+self.L2:
            return self.Dw # White region
        else:
            return self.Dg # Grey region

    # SPLIT AND TRANSPOSE MATRIX C
    # index: 0 -> total, 1 -> zone 1, 2 -> zone 2, 3 -> zone 3
    def CxtByZone(self):
        self.Cxt_by_zone = []

        for zone in range(4):
            if zone == 0:
                self.Cxt_by_zone.append(self.C.T)
            else:
                self.Cxt_by_zone.append(self.C.T[self.zone_point[zone-1]:self.zone_point[zone]+1])

        return self.Cxt_by_zone
    
    # ADDITIONAL INFORMATION, OVERALL ZONE [0] + EACH ZONE [1:3]
    def maxConcentration(self):
        self.max_C = []
        for zone in range(4):
            Ctx = self.Cxt_by_zone[zone].T
            self.max_C.append([max(Ctx[n]) for n in range(self.nt)])
        
        return np.array(self.max_C)

    def numberCell(self):
        self.number_cell = []
        for zone in range(4):
            Ctx = self.Cxt_by_zone[zone].T
            self.number_cell.append([self.simpsonsIntegration(Ctx[n], self.dx) for n in range(self.nt)])
        
        return np.array(self.number_cell)

    def radialDistance(self):
        self.radial_dist = []
        for zone in range(4):
            # CALCULATE x*C(t,x)
            if zone == 0 or zone == 1:
                tempList = [j*self.dx*C for j,C in enumerate(self.Cxt_by_zone[zone])]
            else:
                tempList = [(j+self.zone_point[zone-1])*self.dx*C for j,C in enumerate(self.Cxt_by_zone[zone])]
            xC = np.array(tempList).T
            
            # INTEGRATE
            self.radial_dist.append([self.simpsonsIntegration(xC[n], self.dx)/self.number_cell[zone][n] for n in range(0, self.nt)])

        return np.array(self.radial_dist)

    def growthSpeed(self):
        self.growth_speed = []
        for zone in range(4):
            L = self.radial_dist[zone]
            tempList = [(L[n+1] - L[n-1])/(2*self.dt) for n in range(1, self.nt-1)]
            tempList = [tempList[0]] + tempList + [tempList[-1]]
            self.growth_speed.append(tempList)
        return np.array(self.growth_speed)

    # SIMPSON'S INTEGRATION
    def simpsonsIntegration(self, C, dx):
        n = C.shape[0]
        n_panel = n - 1

        if n_panel%2 == 0:
            # Simpson's 3/8 is not needed
            I_1 = 0
            # Simpson's 1/3 from index 0 to end
            start = 0
        else:
            # Simpson's 3/8 from index 0 to 3 (first 3 panel)
            I_1 = (C[0] + sum(3*C[1:3]) + C[3])*(3*dx/8)
            # Simpson's 1/3 from index 3 to end
            start = 3
        
        I_2 = C[start] + C[-1]
        for j in range(start+1, n-1):
            if (j-start)%2 == 1:
                I_2 += 4*C[j]
            else:
                I_2 += 2*C[j]
        I_2 *= dx/3
        
        return I_1 + I_2

# CHiLD CLASS
class Linear(TumorGrowth):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.calculateC()
        self.Cxt_by_zone = self.CxtByZone()
        self.max_C = self.maxConcentration()
        self.number_cell = self.numberCell()
        self.radial_dist = self.radialDistance()
        self.growth_speed = self.growthSpeed()

    def constructAinvB(self):
        A = np.zeros((self.nx, self.nx))
        B = np.zeros((self.nx, self.nx))

        for j in range(1, self.nx-1):
            # TEMPORARY VARIABLE

            U = -self.R * self.coefD(j+0.5)
            V = -self.S + self.R * (self.coefD(j+0.5) + self.coefD(j-0.5))
            W = -self.R * self.coefD(j-0.5)

            # SET UP MATRIX A
            A[j, j] = 1+V
            A[j, j+1] = U
            A[j, j-1] = W

            # SET UP MATRIX B
            B[j, j] = 1-V
            B[j, j+1] = -U
            B[j, j-1] = -W

            # BOUNDARY CONDITION
            if j == 1:
                A[j, j+1] += W # U+W
                B[j, j+1] += -W # -U-W
            elif j == self.nx-2:
                A[j, j-1] += U # U+W
                B[j, j-1] += -U # -U-W

        # SLICE THE MATRIX (j=0 and j=nx)
        A = A[1:-1, 1:-1]
        B = B[1:-1, 1:-1]

        A_inv = np.linalg.inv(A)
        return np.dot(A_inv, B)

    def calculateC(self):
        AinvB = self.constructAinvB()

        # TIME ITERATION
        for n in range(self.nt-1):
            # PROGRESS BAR
            ui.progressBar.setProperty("value", n/(self.nt-2)*100)
            ui.lblProgressPercentage.setText(str(round(n/(self.nt-2)*100, 1))+"%")
            
            self.C[n+1, 1:-1] = np.dot(AinvB, self.C[n, 1:-1])

        # BOUNDARY CONDITION
        self.C[:, 0] = self.C[:, 2]
        self.C[:, -1] = self.C[:, -3]

        return self.C


class NonLinear(TumorGrowth):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # SET ADDITIONAL PARAMETER
        if self.growthType == "Logistic":
            additional_param = ['Cmax']
        elif self.growthType == "Gompertzian":
            additional_param = ['k', 'd']
        self.__dict__.update((key, val) for key, val in kwargs.items() if key in additional_param)

        # ADDITIONAL TEMPORARY VARIABLE FOR NEWTON ITERATION
        if self.growthType == "Logistic":
            self.T = self.S/(2*self.Cmax)
        elif self.growthType == "Gompertzian":
            self.E = self.S*self.k/self.d
            self.carryingCap = math.exp(self.k/self.d)
            
        self.calculateC()
        self.Cxt_by_zone = self.CxtByZone()
        self.max_C = self.maxConcentration()
        self.number_cell = self.numberCell()
        self.radial_dist = self.radialDistance()
        self.growth_speed = self.growthSpeed()

    # NEWTON RHAPSON RANDOM INITIALIZATION
    def randomInitialGuess(self, minVal, maxVal):
        C_init = np.zeros(self.nx-2)
        for i in range(self.nx-2):
            C_init[i] = minVal+random()*(maxVal-minVal)
        return C_init

    def constructDeltaC(self, C_pair):
        jacobian = np.zeros((self.nx, self.nx))
        F = np.zeros(self.nx)

        for j in range(1, self.nx-1):
            # TEMPORARY VARIABLE
            U = -self.R * self.coefD(j+0.5)
            if self.growthType == "Logistic":
                V = -self.S + self.R * (self.coefD(j+0.5)+self.coefD(j-0.5))
            elif self.growthType == "Gompertzian":
                V = -self.E + self.R * (self.coefD(j+0.5)+self.coefD(j-0.5))
            W = -self.R * self.coefD(j-0.5)

            # SET UP JACOBIAN MATRIX
            if self.growthType == "Logistic":
                jacobian[j, j] = 2*self.T*(C_pair[1, j] + C_pair[0, j])
            elif self.growthType == "Gompertzian":
                jacobian[j, j] = self.S * math.log((C_pair[1, j] + C_pair[0, j])/2) + self.S
            jacobian[j, j] += V + 1
            jacobian[j, j+1] = U
            jacobian[j, j-1] = W

            # SET UP F VECTOR
            if self.growthType == "Logistic":
                F[j] = self.T*(C_pair[1, j] + C_pair[0, j])**2
            elif self.growthType == "Gompertzian":
                F[j] = self.S*(C_pair[1, j] + C_pair[0, j])*math.log((C_pair[1, j] + C_pair[0, j])/2)
            F[j] +=   U*C_pair[1, j+1] + (V+1)*C_pair[1, j] + W*C_pair[1, j-1] \
                    + U*C_pair[0, j+1] + (V-1)*C_pair[0, j] + W*C_pair[0, j-1]

            # BOUNDARY CONDITION
            if j == 1:
                jacobian[j, j+1] += W # U+W
                F[j] += W*C_pair[1, j+1] - W*C_pair[1, j-1] # replacing W*C_pair[1, j-1]
            elif j == self.nx-2:
                jacobian[j, j-1] += U # U+W
                F[j] += U*C_pair[1, -3] - U*C_pair[1, -1] # replacing U*C_pair[1, j+1]

        # SLICE THE MATRIX AND VECTOR (j=0 and j=nx)
        jacobian = jacobian[1:-1, 1:-1]
        F = F[1:-1]
        
        jacobian_inv = np.linalg.inv(jacobian)
        return -np.dot(jacobian_inv, F)

    def calculateC(self):
        # ERROR TOLERANCE
        tol_relative = 1E-10
        tol_absolute = 1E-5

        # TIME ITERATION
        for n in range(self.nt-1):
            # PROGRESS BAR
            ui.progressBar.setProperty("value", n/(self.nt-2)*100)
            ui.lblProgressPercentage.setText(str(round(n/(self.nt-2)*100, 1))+"%")
            
            # NEWTON ITERATION
            isDivergent = False
            while True:
                iteration = 0
                err = math.inf
                tol_combined = tol_relative*np.linalg.norm(self.C[n, 1:-1]) + tol_absolute
                
                # SET INITIAL GUESS
                if self.growthType == "Logistic":
                    # if not divergent then initial guess C is from previous time step,
                    # else random value from 0 to Cmax
                    #self.C[n+1, 1:-1] = self.C[n, 1:-1] if not isDivergent else self.randomInitialGuess(0, self.Cmax)
                    self.C[n+1, 1:-1] = self.randomInitialGuess(0, self.Cmax)
                elif self.growthType == "Gompertzian":
                    # value of initial guess must not 0, because ln(0) is indeterminate
                    self.C[n+1, 1:-1] = self.randomInitialGuess(0, self.carryingCap)
                
                while err > tol_combined:
                    before = np.copy(self.C[n+1, 1:-1])
                    after = before + self.constructDeltaC(self.C[n:(n+1)+1]) # pairwise
                    self.C[n+1, 1:-1] = np.copy(after)

                    err = np.linalg.norm(after-before)
                    iteration += 1

                    if iteration == 100: # divergence case
                        isDivergent = True
                        break

                if err <= tol_combined:
                    break
                
        # BOUNDARY CONDITION
        self.C[:, 0] = self.C[:, 2]
        self.C[:, -1] = self.C[:, -3]

        return self.C
    

# STYLESHEETS FOR UI
PROGRESSBAR_STYLE = """
QProgressBar{
    border: 3px solid black;
    border-radius: 10px;
}
QProgressBar::chunk {
    background-color: blue;
    width: 15px;
    margin: 0px;
}
"""

NAVTOOLBAR_STYLE = """
QToolBar{
    border: 0px;
}
"""

QTOOLTIP_STYLE = """
QToolTip{
    background-color: white; 
    color: black; 
    border: black solid 1px;
    font: bold 15px "Sitka";
}
"""

TABLEHEADER_STYLE = """
QHeaderView{
    font: bold 12px;
}
"""


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, winTitle, title, subtitle, icon, btnList):
        super(CustomDialog, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)

        # WIDGET
        self.setObjectName("CustomDialog")
        self.resize(350, 150)
        self.setFixedSize(self.size())
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(180, 110, 161, 32))
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.lblTitle = QtWidgets.QLabel(self)
        self.lblTitle.setGeometry(QtCore.QRect(80, 30, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.lblSubtitle = QtWidgets.QLabel(self)
        self.lblSubtitle.setGeometry(QtCore.QRect(80, 60, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lblSubtitle.setFont(font)
        self.lblSubtitle.setObjectName("lblSubtitle")
        self.lblIcon = QtWidgets.QLabel(self)
        self.lblIcon.setGeometry(QtCore.QRect(10, 40, 55, 50))
        self.lblIcon.setText("")
        self.lblIcon.setScaledContents(True)
        self.lblIcon.setObjectName("lblIcon")

        # EVENT
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        # CUSTOMIZATION
        self.setWindowTitle(winTitle)
        self.lblTitle.setText(title)
        self.lblSubtitle.setText(subtitle)
        iconDict = {"Warning": QtGui.QPixmap("asset/warning.png"),
                    "Error": QtGui.QPixmap("asset/error.png"),
                    "Question": QtGui.QPixmap("asset/question.png"),
                    "Success": QtGui.QPixmap("asset/success.png")}
        self.lblIcon.setPixmap(iconDict[icon])
        self.buttonBox.setStandardButtons(btnList)

    def accept(self):
        super(CustomDialog, self).accept()
        self.choice = True
        
    def reject(self):
        super(CustomDialog, self).reject()
        self.choice = False
        
    def exec_(self):
        super(CustomDialog, self).exec_()
        return self.choice


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setStyleSheet(QTOOLTIP_STYLE)

        # FLAG
        self.canLeavePage = True
        self.inputSubmitted = False

        # STORE SAMPLE DATA
        self.sampleData1 = {'L1':7.5, 'L2':35, 'L3':7.5, 'Dg':0.13, 'Dw':0.65, 'x0':25, 'C0':39.89, 'rho':0.012, 'Cmax':62.5, 'tf':250, 'k':4, 'd':1}
        self.sampleData2 = {'L1':7.5, 'L2':35, 'L3':7.5, 'Dg':0.13, 'Dw':0.65, 'x0':25, 'C0':39.89, 'rho':0.012, 'Cmax':62.5, 'tf':365*3, 'k':10, 'd':2}
        self.sampleData = [self.sampleData1, self.sampleData2]
        self.data_idx = 0

        # ICON
        self.icon = {'q': QtGui.QPixmap("asset/questionmark.png"),
                     'e': QtGui.QPixmap("asset/errormark.png")}

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setupUi(self)

    # --------------------------------- MAIN ---------------------------------
    def setupUi(self, MainWindow):
        # MAIN WINDOW
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setFixedSize(self.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        # MENU BAR
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        # FILE
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew_Simulation = QtWidgets.QMenu(self.menuFile)
        self.menuNew_Simulation.setObjectName("menuNew_Simulation")
        self.actionExponential = QtWidgets.QAction(MainWindow)
        self.actionExponential.setObjectName("actionExponential")
        self.actionLogistic = QtWidgets.QAction(MainWindow)
        self.actionLogistic.setObjectName("actionLogistic")
        self.actionGompertzian = QtWidgets.QAction(MainWindow)
        self.actionGompertzian.setObjectName("actionGompertzian")
        self.actionBack_to_Home = QtWidgets.QAction(MainWindow)
        self.actionBack_to_Home.setObjectName("actionBack_to_Home")
        self.menuNew_Simulation.addAction(self.actionExponential)
        self.menuNew_Simulation.addAction(self.actionLogistic)
        self.menuNew_Simulation.addAction(self.actionGompertzian)
        self.menuFile.addAction(self.menuNew_Simulation.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionBack_to_Home)
        # HELP
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.actionView_Help = QtWidgets.QAction(MainWindow)
        self.actionView_Help.setObjectName("actionView_Help")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionView_Help)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        MainWindow.setMenuBar(self.menubar)

        # SET MENU ACTION
        self.setMenubarAction()

        # STATUS BAR
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # SETUP UI
        self.setupUi_Home(MainWindow)
        self.setupUi_Help(MainWindow)
        self.setupUi_About(MainWindow)
        self.setupUi_Expo(MainWindow)
        self.setupUi_Logistic(MainWindow)
        self.setupUi_Gompertzian(MainWindow)
        self.setupUi_Loading(MainWindow)
        self.setupUi_Result(MainWindow)
        
        # RETRANSLATE UI
        self.retranslateUi(MainWindow)
        self.retranslateUi_Home(MainWindow)
        self.retranslateUi_Help(MainWindow)
        self.retranslateUi_About(MainWindow)
        self.retranslateUi_Expo(MainWindow)
        self.retranslateUi_Logistic(MainWindow)
        self.retranslateUi_Gompertzian(MainWindow)
        self.retranslateUi_Loading(MainWindow)
        self.retranslateUi_Result(MainWindow)

        # START: HOME PAGE
        self.showHome()
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.txtExpoTime.setMaximum(2500)
        self.txtLogisticTime.setMaximum(2500)
        self.txtGompertzianTime.setMaximum(2500)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Glioma Growth Simulation"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuNew_Simulation.setTitle(_translate("MainWindow", "&New Simulation"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.actionView_Help.setText(_translate("MainWindow", "View &Help"))
        self.actionView_Help.setShortcut(_translate("MainWindow", "Ctrl+?"))
        self.actionAbout.setText(_translate("MainWindow", "&About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionBack_to_Home.setText(_translate("MainWindow", "Back to &Home"))
        self.actionBack_to_Home.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionExponential.setText(_translate("MainWindow", "&Exponential"))
        self.actionExponential.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionLogistic.setText(_translate("MainWindow", "&Logistic"))
        self.actionLogistic.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionGompertzian.setText(_translate("MainWindow", "&Gompertzian"))
        self.actionGompertzian.setShortcut(_translate("MainWindow", "Ctrl+G"))

    # --------------------------------- PAGE CONTROL ---------------------------------
    def setMenubarAction(self):
        # FILE
        self.actionBack_to_Home.triggered.connect(self.showHome)

        # SIMULATION
        self.actionExponential.triggered.connect(lambda: self.showExpo(flagReset = True, popUpResetDialog = False))
        self.actionLogistic.triggered.connect(lambda: self.showLogistic(flagReset = True, popUpResetDialog = False))
        self.actionGompertzian.triggered.connect(lambda: self.showGompertzian(flagReset = True, popUpResetDialog = False))

        # HELP
        self.actionView_Help.triggered.connect(self.showHelp)
        self.actionAbout.triggered.connect(self.showAbout)

    def hideAllPage(self):
        self.frameHome.hide()
        self.frameHelp.hide()
        self.frameAbout.hide()
        self.frameExpo.hide()
        self.frameLogistic.hide()
        self.frameGompertzian.hide()
        self.frameLoading.hide()
        self.frameResult.hide()

    def checkCanLeavePage(self, frame):
        if self.canLeavePage == False:
            dialog = CustomDialog("Leave",
                                  "Are you sure you want to leave?",
                                  "Unsaved data will be lost.",
                                  "Warning",
                                  QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            if dialog.exec_():  
                self.canLeavePage = True

        if self.canLeavePage == True:
            self.hideAllPage()
            frame.show()

    def showHome(self):
        self.checkCanLeavePage(self.frameHome)

    def showHelp(self):
        self.checkCanLeavePage(self.frameHelp)
        
    def showAbout(self):
        self.checkCanLeavePage(self.frameAbout)

    def showExpo(self, flagReset, popUpResetDialog):
        self.checkCanLeavePage(self.frameExpo)
        self.canLeavePage = False
        self.resetInputExpo(flagReset, popUpResetDialog)
        self.data_idx = 0

    def showLogistic(self, flagReset, popUpResetDialog):
        self.checkCanLeavePage(self.frameLogistic)
        self.canLeavePage = False
        self.resetInputLogistic(flagReset, popUpResetDialog)
        self.data_idx = 0

    def showGompertzian(self, flagReset, popUpResetDialog):
        self.checkCanLeavePage(self.frameGompertzian)
        self.canLeavePage = False
        self.resetInputGompertzian(flagReset, popUpResetDialog)
        self.data_idx = 0

    def showLoading(self):
        self.canLeavePage = True
        self.checkCanLeavePage(self.frameLoading)
        self.retranslateUi_Loading(self)
        self.canLeavePage = False

    def showResult(self):
        self.inputSubmitted = True
        self.canLeavePage = True
        self.checkCanLeavePage(self.frameResult)
        self.retranslateUi_Result(self)
        self.canLeavePage = False

    def closeEvent(self, event):
        dialog = CustomDialog("Exit",
                              "Are you sure you want to exit?",
                              "Unsaved data will be lost.",
                              "Warning",
                              QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        if dialog.exec_():
            event.accept()
        else:
            event.ignore()

    # INPUT FORM ERROR MESSAGE
    def setErrorMessage(self, errMsg, lblInfo):
        lblInfo.setPixmap(self.icon['e'])
        lblInfo.setToolTip(errMsg)        
        return False

    # BTNSAMPLEDATA EVENT
    def useSampleData(self, txtList, varList, growthType):
        self.data_idx = self.data_idx % len(self.sampleData)
        
        dialog = CustomDialog("Sample Data",
                              "Do you want to use sample data-"+str(self.data_idx+1)+"?",
                              "Current input data will be overwritten.",
                              "Question",
                              QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        if dialog.exec_():
            for i in range(len(txtList)):
                 txtList[i].setValue(self.sampleData[self.data_idx][varList[i]])
                 
            self.data_idx += 1

            if growthType == "Exponential":
                self.retranslateUi_Expo(self)
            elif growthType == "Logistic":
                self.retranslateUi_Logistic(self)
            elif growthType == "Gompertzian":
                self.retranslateUi_Gompertzian(self)

    def runSimulation(self, growthType):
        if growthType == "Exponential":
            self.runSimulationExpo()
        elif growthType == "Logistic":
            self.runSimulationLogistic()
        elif growthType == "Gompertzian":
            self.runSimulationGompertzian()

    # --------------------------------- HOME ---------------------------------
    def setupUi_Home(self, MainWindow):
        # FRAME
        self.frameHome = QtWidgets.QFrame(self.centralwidget)
        self.frameHome.setGeometry(QtCore.QRect(0, 0, 800, 550))
        self.frameHome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHome.setObjectName("frameHome")

        # LAYOUT
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frameHome)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 70, 800, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # APPLICATION TITLE
        self.lblHomeTitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblHomeTitle.setFont(font)
        self.lblHomeTitle.setObjectName("lblHomeTitle")
        self.verticalLayout.addWidget(self.lblHomeTitle, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # DEVELOPED BY
        self.lblDevSubtitle = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.lblDevSubtitle.setFont(font)
        self.lblDevSubtitle.setObjectName("lblDevSubtitle")
        self.verticalLayout.addWidget(self.lblDevSubtitle, 0, QtCore.Qt.AlignHCenter)
        self.lblDevName = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.lblDevName.setFont(font)
        self.lblDevName.setObjectName("lblDevName")
        self.verticalLayout.addWidget(self.lblDevName, 0, QtCore.Qt.AlignHCenter)
        self.lblDevNim = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.lblDevNim.setFont(font)
        self.lblDevNim.setObjectName("lblDevNim")
        self.verticalLayout.addWidget(self.lblDevNim, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        # FOOTER
        self.lblFooterBinus = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lblFooterBinus.setPixmap(QtGui.QPixmap("asset/logobinus.png"))
        self.lblFooterBinus.setObjectName("lblFooterBinus")
        self.verticalLayout.addWidget(self.lblFooterBinus, 0, QtCore.Qt.AlignHCenter)
        self.lblFooterYear = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.lblFooterYear.setFont(font)
        self.lblFooterYear.setObjectName("lblFooterYear")
        self.verticalLayout.addWidget(self.lblFooterYear, 0, QtCore.Qt.AlignHCenter)

    def retranslateUi_Home(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblHomeTitle.setText(_translate("MainWindow", "GLIOMA GROWTH SIMULATION"))
        self.lblDevSubtitle.setText(_translate("MainWindow", "DEVELOPED BY"))
        self.lblDevName.setText(_translate("MainWindow", "TOMY"))
        self.lblDevNim.setText(_translate("MainWindow", "1801431662"))
        self.lblFooterYear.setText(_translate("MainWindow", "2019"))

    # --------------------------------- ABOUT ---------------------------------
    def setupUi_About(self, MainWindow):
        self.frameAbout = QtWidgets.QFrame(self.centralwidget)
        self.frameAbout.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameAbout.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAbout.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameAbout.setObjectName("frameAbout")
        self.lblAboutTitle = QtWidgets.QLabel(self.frameAbout)
        self.lblAboutTitle.setGeometry(QtCore.QRect(10, 10, 443, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblAboutTitle.setFont(font)
        self.lblAboutTitle.setObjectName("lblAboutTitle")
        self.tabAbout = QtWidgets.QTabWidget(self.frameAbout)
        self.tabAbout.setGeometry(QtCore.QRect(10, 70, 775, 491))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tabAbout.setFont(font)
        self.tabAbout.setObjectName("tabAbout")
        self.tabDeveloper = QtWidgets.QWidget()
        self.tabDeveloper.setObjectName("tabDeveloper")
        self.aboutDeveloper = QtWidgets.QScrollArea(self.tabDeveloper)
        self.aboutDeveloper.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.aboutDeveloper.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.aboutDeveloper.setWidgetResizable(True)
        self.aboutDeveloper.setObjectName("aboutDeveloper")
        self.scrollAreaWidgetDeveloper = QtWidgets.QWidget()
        self.scrollAreaWidgetDeveloper.setGeometry(QtCore.QRect(0, 0, 752, 449))
        self.scrollAreaWidgetDeveloper.setObjectName("scrollAreaWidgetDeveloper")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetDeveloper)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblDeveloper = QtWidgets.QLabel(self.scrollAreaWidgetDeveloper)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblDeveloper.setFont(font)
        self.lblDeveloper.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblDeveloper.setWordWrap(True)
        self.lblDeveloper.setObjectName("lblDeveloper")
        self.verticalLayout_3.addWidget(self.lblDeveloper)
        self.aboutDeveloper.setWidget(self.scrollAreaWidgetDeveloper)
        self.tabAbout.addTab(self.tabDeveloper, "")
        self.tabPurpose = QtWidgets.QWidget()
        self.tabPurpose.setObjectName("tabPurpose")
        self.aboutPurpose = QtWidgets.QScrollArea(self.tabPurpose)
        self.aboutPurpose.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.aboutPurpose.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.aboutPurpose.setWidgetResizable(True)
        self.aboutPurpose.setObjectName("aboutPurpose")
        self.scrollAreaWidgetPurpose = QtWidgets.QWidget()
        self.scrollAreaWidgetPurpose.setGeometry(QtCore.QRect(0, 0, 752, 449))
        self.scrollAreaWidgetPurpose.setObjectName("scrollAreaWidgetPurpose")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetPurpose)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblPurpose = QtWidgets.QLabel(self.scrollAreaWidgetPurpose)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblPurpose.setFont(font)
        self.lblPurpose.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblPurpose.setWordWrap(True)
        self.lblPurpose.setObjectName("lblPurpose")
        self.verticalLayout.addWidget(self.lblPurpose)
        self.aboutPurpose.setWidget(self.scrollAreaWidgetPurpose)
        self.tabAbout.addTab(self.tabPurpose, "")
        self.tabMathModel = QtWidgets.QWidget()
        self.tabMathModel.setObjectName("tabMathModel")
        self.aboutMathModel = QtWidgets.QScrollArea(self.tabMathModel)
        self.aboutMathModel.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.aboutMathModel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.aboutMathModel.setWidgetResizable(True)
        self.aboutMathModel.setObjectName("aboutMathModel")
        self.scrollAreaWidgetMathModel = QtWidgets.QWidget()
        self.scrollAreaWidgetMathModel.setGeometry(QtCore.QRect(0, 0, 752, 1613))
        self.scrollAreaWidgetMathModel.setObjectName("scrollAreaWidgetMathModel")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetMathModel)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblMathModel_1 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblMathModel_1.setFont(font)
        self.lblMathModel_1.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblMathModel_1.setWordWrap(True)
        self.lblMathModel_1.setOpenExternalLinks(True)
        self.lblMathModel_1.setObjectName("lblMathModel_1")
        self.verticalLayout_2.addWidget(self.lblMathModel_1)
        self.imgMathModel_1 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        self.imgMathModel_1.setText("")
        self.imgMathModel_1.setPixmap(QtGui.QPixmap("asset/mathequation/reactiondiffusion.png"))
        self.imgMathModel_1.setScaledContents(False)
        self.imgMathModel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.imgMathModel_1.setObjectName("imgMathModel_1")
        self.verticalLayout_2.addWidget(self.imgMathModel_1)
        self.lblMathModel_2 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblMathModel_2.setFont(font)
        self.lblMathModel_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblMathModel_2.setWordWrap(True)
        self.lblMathModel_2.setOpenExternalLinks(True)
        self.lblMathModel_2.setObjectName("lblMathModel_2")
        self.verticalLayout_2.addWidget(self.lblMathModel_2)
        self.imgMathModel_2 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        self.imgMathModel_2.setText("")
        self.imgMathModel_2.setPixmap(QtGui.QPixmap("asset/mathequation/diffusioncoef.png"))
        self.imgMathModel_2.setScaledContents(False)
        self.imgMathModel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.imgMathModel_2.setObjectName("imgMathModel_2")
        self.verticalLayout_2.addWidget(self.imgMathModel_2)
        self.lblMathModel_3 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblMathModel_3.setFont(font)
        self.lblMathModel_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblMathModel_3.setWordWrap(True)
        self.lblMathModel_3.setOpenExternalLinks(True)
        self.lblMathModel_3.setObjectName("lblMathModel_3")
        self.verticalLayout_2.addWidget(self.lblMathModel_3)
        self.imgMathModel_3 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        self.imgMathModel_3.setText("")
        self.imgMathModel_3.setPixmap(QtGui.QPixmap("asset/mathequation/growthfunction.png"))
        self.imgMathModel_3.setScaledContents(False)
        self.imgMathModel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.imgMathModel_3.setObjectName("imgMathModel_3")
        self.verticalLayout_2.addWidget(self.imgMathModel_3)
        self.lblMathModel_4 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblMathModel_4.setFont(font)
        self.lblMathModel_4.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblMathModel_4.setWordWrap(True)
        self.lblMathModel_4.setOpenExternalLinks(True)
        self.lblMathModel_4.setObjectName("lblMathModel_4")
        self.verticalLayout_2.addWidget(self.lblMathModel_4)
        self.imgMathModel_4 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        self.imgMathModel_4.setText("")
        self.imgMathModel_4.setPixmap(QtGui.QPixmap("asset/mathequation/tumorattribute.png"))
        self.imgMathModel_4.setScaledContents(False)
        self.imgMathModel_4.setAlignment(QtCore.Qt.AlignCenter)
        self.imgMathModel_4.setObjectName("imgMathModel_4")
        self.verticalLayout_2.addWidget(self.imgMathModel_4)
        self.lblMathModel_5 = QtWidgets.QLabel(self.scrollAreaWidgetMathModel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblMathModel_5.setFont(font)
        self.lblMathModel_5.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblMathModel_5.setWordWrap(True)
        self.lblMathModel_5.setOpenExternalLinks(True)
        self.lblMathModel_5.setObjectName("lblMathModel_5")
        self.verticalLayout_2.addWidget(self.lblMathModel_5)
        self.aboutMathModel.setWidget(self.scrollAreaWidgetMathModel)
        self.tabAbout.addTab(self.tabMathModel, "")

    def retranslateUi_About(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblAboutTitle.setText(_translate("MainWindow", "ABOUT"))
        self.lblDeveloper.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:115%;\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">Developed by Tomy, a student of Binus University in Jakarta, Indonesia, this application is submitted as one of the requirements for a bachelor’s degree in Computer Science and Mathematics study program.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:115%;\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The application was developed on Microsoft Windows 10 by using Python 3.7.2 with the help of QtDesigner 5.11.2 for building the user interface. Also, tested on Intel core i7 quad-core processor @ 2.40 GHz and 4 GB of RAM.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:115%;\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">List of external Python packages that are used: numpy, matplotlib, mplcursors, mpldatacursor, PyQt5, and pandas.</span></p></body></html>"))
        self.tabAbout.setTabText(self.tabAbout.indexOf(self.tabDeveloper), _translate("MainWindow", "Developer"))
        self.lblPurpose.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">Up until now, there is one type of medical procedure that can be done to detect abnormalities in body tissue namely biopsy. But there is lack of medical device to predict on how tumor will grow in the future.</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">One of prognosis technique is to approach it from mathematical perspective by utilizing differential equation, which can be used as a model for hypothesis testing of tumor cell growth, confirming the experiment that have been carried out, and providing simulations of prediction in relatively short time without requiring a large experimental costs.</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The biological variations can be achieved by integrating the mathematical equation with clinical data, such as diffusion coefficient, proliferation rate, and carrying capacity.</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">This application is developed to numerically simulate the glioma growth using exponential, logistic, and Gompertzian function by Finite Difference Method. The mathematical model and method is further explained in “Mathematical Model” tab.</span></p></body></html>"))
        self.tabAbout.setTabText(self.tabAbout.indexOf(self.tabPurpose), _translate("MainWindow", "Purpose"))
        self.lblMathModel_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">MODEL</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The mathematical model used for the simulation is from </span><a href=\"https://web.itu.edu.tr/ozugurlue/paper8.pdf\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">Ozugurlu (2015)</span></a><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> as the main reference research paper. Glioma growth is modeled by simple </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">reaction-diffusion</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> equation which defined by:</span></p></body></html>"))
        self.lblMathModel_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">c(t,x)</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> represents the concentration of glioma at space </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">x</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> and time </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">t</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. The first term refers to the diffusion process of glioma along one dimensional heterogeneous space, and the second term refers to the reaction/growth process of glioma either by exponential, logistic, or Gompertzian function.</span><br/></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">spatial heterogenity</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is determined by the grey and white matter of the brain which defined by:</span></p></body></html>"))
        self.lblMathModel_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">D</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:sub;\">g</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> and </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">D</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:sub;\">w</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> represents the diffusion coefficient of the grey and white matter, respectively.</span><br/></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">reaction function </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">r(c)</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is determined by the exponential, logistic, or Gompertzian growth function, respectively:</span></p></body></html>"))
        self.lblMathModel_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-style:italic;\">ρ </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">represent the net proliferation rate of glioma, </span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">C</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:sub;\">max</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> and </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">e</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:super;\">k/d</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is the carrying capacity of glioma where </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">k</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is the growth rate and </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">d</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is the density coefficient of glioma.</span></p><p><br/></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; text-decoration: underline;\">METHODS</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The equations are then solved numerically by using Finite Difference Method </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Crank-Nicolson</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> implicit scheme with zero flux </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Neumann</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> boundary condition and </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Gaussian</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> function as the initial condition.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">The exponential growth model is categorized as linear partial differential equation, while logistic and Gompertzian growth model are categorized as non-linear partial differential equation. The discretization of linear PDE can be solved just by using regular linear algebra, while the discretization of non-linear PDE solved by using </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Newton-Rhapson</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> iteration. Thus, the process will be much slower when simulating the non-linear PDE compared to the linear PDE.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">In order to gain more insight regarding the growth of glioma, several tumor attributes are being calculated, such as: maximum glioma concentration, average number of cell, mean radial distance, and growth speed by using the following formula, respectively:</span></p></body></html>"))
        self.lblMathModel_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">where </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">Z</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is the interval of corresponding zone. Since, the concentration of glioma is discretized, the above formula is then approximated by using </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Simpson’s 1/3 and 3/8</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> integration rule.</span></p></body></html>"))
        self.tabAbout.setTabText(self.tabAbout.indexOf(self.tabMathModel), _translate("MainWindow", "Mathematical Model"))

    # --------------------------------- HELP ---------------------------------
    def setupUi_Help(self, MainWindow):
        self.frameHelp = QtWidgets.QFrame(self.centralwidget)
        self.frameHelp.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameHelp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameHelp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameHelp.setObjectName("frameHelp")
        self.lblHelpTitle = QtWidgets.QLabel(self.frameHelp)
        self.lblHelpTitle.setGeometry(QtCore.QRect(10, 10, 443, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblHelpTitle.setFont(font)
        self.lblHelpTitle.setObjectName("lblHelpTitle")
        self.tabHelp = QtWidgets.QTabWidget(self.frameHelp)
        self.tabHelp.setGeometry(QtCore.QRect(10, 70, 775, 491))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tabHelp.setFont(font)
        self.tabHelp.setObjectName("tabHelp")
        self.tabHow = QtWidgets.QWidget()
        self.tabHow.setObjectName("tabHow")
        self.helpHow = QtWidgets.QScrollArea(self.tabHow)
        self.helpHow.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.helpHow.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.helpHow.setWidgetResizable(True)
        self.helpHow.setObjectName("helpHow")
        self.scrollAreaWidgetHow = QtWidgets.QWidget()
        self.scrollAreaWidgetHow.setGeometry(QtCore.QRect(0, 0, 752, 673))
        self.scrollAreaWidgetHow.setObjectName("scrollAreaWidgetHow")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetHow)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblHow = QtWidgets.QLabel(self.scrollAreaWidgetHow)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblHow.setFont(font)
        self.lblHow.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblHow.setWordWrap(True)
        self.lblHow.setOpenExternalLinks(True)
        self.lblHow.setObjectName("lblHow")
        self.verticalLayout_3.addWidget(self.lblHow)
        self.helpHow.setWidget(self.scrollAreaWidgetHow)
        self.tabHelp.addTab(self.tabHow, "")
        self.tabSimulationType = QtWidgets.QWidget()
        self.tabSimulationType.setObjectName("tabSimulationType")
        self.helpSimulationType = QtWidgets.QScrollArea(self.tabSimulationType)
        self.helpSimulationType.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.helpSimulationType.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.helpSimulationType.setWidgetResizable(True)
        self.helpSimulationType.setObjectName("helpSimulationType")
        self.scrollAreaWidgetSimulationType = QtWidgets.QWidget()
        self.scrollAreaWidgetSimulationType.setGeometry(QtCore.QRect(0, -401, 752, 1456))
        self.scrollAreaWidgetSimulationType.setObjectName("scrollAreaWidgetSimulationType")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetSimulationType)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblSimulationTypeExpo = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblSimulationTypeExpo.setFont(font)
        self.lblSimulationTypeExpo.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblSimulationTypeExpo.setWordWrap(True)
        self.lblSimulationTypeExpo.setObjectName("lblSimulationTypeExpo")
        self.verticalLayout.addWidget(self.lblSimulationTypeExpo)
        self.imgSimulationTypeExpo = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.imgSimulationTypeExpo.setText("")
        self.imgSimulationTypeExpo.setPixmap(QtGui.QPixmap("asset/exponential.png"))
        self.imgSimulationTypeExpo.setAlignment(QtCore.Qt.AlignCenter)
        self.imgSimulationTypeExpo.setObjectName("imgSimulationTypeExpo")
        self.verticalLayout.addWidget(self.imgSimulationTypeExpo)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lblSimulationTypeLogistic = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.lblSimulationTypeLogistic.setWordWrap(True)
        self.lblSimulationTypeLogistic.setObjectName("lblSimulationTypeLogistic")
        self.verticalLayout.addWidget(self.lblSimulationTypeLogistic)
        self.imgSimulationTypeLogistic = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.imgSimulationTypeLogistic.setText("")
        self.imgSimulationTypeLogistic.setPixmap(QtGui.QPixmap("asset/logistic.png"))
        self.imgSimulationTypeLogistic.setAlignment(QtCore.Qt.AlignCenter)
        self.imgSimulationTypeLogistic.setObjectName("imgSimulationTypeLogistic")
        self.verticalLayout.addWidget(self.imgSimulationTypeLogistic)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.lblSimulationTypeGompertzian = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.lblSimulationTypeGompertzian.setWordWrap(True)
        self.lblSimulationTypeGompertzian.setObjectName("lblSimulationTypeGompertzian")
        self.verticalLayout.addWidget(self.lblSimulationTypeGompertzian)
        self.imgSimulationTypeGompertzian = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.imgSimulationTypeGompertzian.setText("")
        self.imgSimulationTypeGompertzian.setPixmap(QtGui.QPixmap("asset/gompertzian.png"))
        self.imgSimulationTypeGompertzian.setAlignment(QtCore.Qt.AlignCenter)
        self.imgSimulationTypeGompertzian.setObjectName("imgSimulationTypeGompertzian")
        self.verticalLayout.addWidget(self.imgSimulationTypeGompertzian)
        self.lblSimulationTypeReferences = QtWidgets.QLabel(self.scrollAreaWidgetSimulationType)
        self.lblSimulationTypeReferences.setWordWrap(True)
        self.lblSimulationTypeReferences.setObjectName("lblSimulationTypeReferences")
        self.verticalLayout.addWidget(self.lblSimulationTypeReferences)
        self.helpSimulationType.setWidget(self.scrollAreaWidgetSimulationType)
        self.tabHelp.addTab(self.tabSimulationType, "")
        self.tabInputParameter = QtWidgets.QWidget()
        self.tabInputParameter.setObjectName("tabInputParameter")
        self.helpInputParameter = QtWidgets.QScrollArea(self.tabInputParameter)
        self.helpInputParameter.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.helpInputParameter.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.helpInputParameter.setWidgetResizable(True)
        self.helpInputParameter.setObjectName("helpInputParameter")
        self.scrollAreaWidgetInputParameter = QtWidgets.QWidget()
        self.scrollAreaWidgetInputParameter.setGeometry(QtCore.QRect(0, 0, 752, 1051))
        self.scrollAreaWidgetInputParameter.setObjectName("scrollAreaWidgetInputParameter")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetInputParameter)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.lblInputTitle = QtWidgets.QLabel(self.scrollAreaWidgetInputParameter)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        self.lblInputTitle.setFont(font)
        self.lblInputTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInputTitle.setObjectName("lblInputTitle")
        self.verticalLayout_2.addWidget(self.lblInputTitle)

        self.imgBrainIllustration = QtWidgets.QLabel(self.scrollAreaWidgetInputParameter)
        self.imgBrainIllustration.setText("")
        self.imgBrainIllustration.setPixmap(QtGui.QPixmap("asset/illustration/brain.png"))
        self.imgBrainIllustration.setAlignment(QtCore.Qt.AlignCenter)
        self.imgBrainIllustration.setObjectName("imgBrainIllustration")
        self.verticalLayout_2.addWidget(self.imgBrainIllustration)

        self.imgInputParameterIllustration = QtWidgets.QLabel(self.scrollAreaWidgetInputParameter)
        self.imgInputParameterIllustration.setText("")
        self.imgInputParameterIllustration.setPixmap(QtGui.QPixmap("asset/illustration/parameter.png"))
        self.imgInputParameterIllustration.setAlignment(QtCore.Qt.AlignCenter)
        self.imgInputParameterIllustration.setObjectName("imgInputParameterIllustration")
        self.verticalLayout_2.addWidget(self.imgInputParameterIllustration)
        
        self.lblInputParameter = QtWidgets.QLabel(self.scrollAreaWidgetInputParameter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblInputParameter.setFont(font)
        self.lblInputParameter.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblInputParameter.setWordWrap(True)
        self.lblInputParameter.setOpenExternalLinks(True)
        self.lblInputParameter.setObjectName("lblInputParameter")
        self.verticalLayout_2.addWidget(self.lblInputParameter)

        self.lblInputParameterReferences = QtWidgets.QLabel(self.scrollAreaWidgetInputParameter)
        self.lblInputParameterReferences.setWordWrap(True)
        self.lblInputParameterReferences.setObjectName("lblInputParameterReferences")
        self.verticalLayout_2.addWidget(self.lblInputParameterReferences)
        
        self.helpInputParameter.setWidget(self.scrollAreaWidgetInputParameter)
        self.tabHelp.addTab(self.tabInputParameter, "")
        self.tabOutputInformation = QtWidgets.QWidget()
        self.tabOutputInformation.setObjectName("tabOutputInformation")
        self.helpOutputInformation = QtWidgets.QScrollArea(self.tabOutputInformation)
        self.helpOutputInformation.setGeometry(QtCore.QRect(0, 0, 771, 451))
        self.helpOutputInformation.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.helpOutputInformation.setWidgetResizable(True)
        self.helpOutputInformation.setObjectName("helpOutputInformation")
        self.scrollAreaWidgetOutputInformation = QtWidgets.QWidget()
        self.scrollAreaWidgetOutputInformation.setGeometry(QtCore.QRect(0, 0, 752, 462))
        self.scrollAreaWidgetOutputInformation.setObjectName("scrollAreaWidgetOutputInformation")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetOutputInformation)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblOutputInformation = QtWidgets.QLabel(self.scrollAreaWidgetOutputInformation)
        self.lblOutputInformation.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblOutputInformation.setWordWrap(True)
        self.lblOutputInformation.setObjectName("lblOutputInformation")
        self.verticalLayout_7.addWidget(self.lblOutputInformation)
        self.helpOutputInformation.setWidget(self.scrollAreaWidgetOutputInformation)
        self.tabHelp.addTab(self.tabOutputInformation, "")

    def retranslateUi_Help(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblHelpTitle.setText(_translate("MainWindow", "HELP"))
        self.lblHow.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">Here is step-by-step process on how you can use the application to start simulating the glioma growth:</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">1.</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> Go to </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">File &gt; New Simulation</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">2</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. Choose the </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">menu</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> based on the growth function to be used: </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">exponential, logistic, or Gompertzian</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. The explanation of each function can be found in “Simulation Type” tab.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">3</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Input all the numerical data</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. Hover over the question mark (?) symbol to read the brief explanation of each data. Hover over the input text box to read the validation of each data. The explanation of each input can be found in “Input Parameter” tab.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">4</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. As an alternative, you can </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">import Excel file</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> as your data input. The Excel template is provided on </span><a href=\"https://drive.google.com/drive/folders/1LWBo43D2WYdd0RHgyaWW89M5xThjuMDy?usp=sharing\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">Google Drive</span></a><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. Make sure sheet name is the same as the growth function you want to simulate.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">5</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. As an other alternative, you can simply click </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Sample Data</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> button so that all text boxes are filled automatically with built-in data.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">6</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. Click the </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Simulate</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> button when you are already sure of the input.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">7</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Wait</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> until the application has finished the computational process. </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600; color:#ff0000;\">Warning</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: don’t interact with the screen while loading, the application might not be responding.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">8</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. On the result page, you can choose the </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">output type</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> to be displayed: Table, 2D Graph, 3D Graph, or 2D Animation. You can also choose the corresponding </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">tumor attribute</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> to be displayed. The output detail can be found in “Output Information” tab.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">9</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. By clicking </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Save Table</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> button, you can save the table result as Excel file. Both two and three dimensional graph can be saved by clicking </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Save icon</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">, located at the toolbox above the graph. Two dimensional animation can be saved as .mp4 file by clicking </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Save Animation</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> button.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">10</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. If you want to make slight changes on the input, you can click </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Resimulate</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> button and repeat the same process again from step 3 to 9.</span></p></body></html>"))
        self.tabHelp.setTabText(self.tabHelp.indexOf(self.tabHow), _translate("MainWindow", "How to Use"))
        self.lblSimulationTypeExpo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">Population ecologists use various method to model the population dynamics. An accurate model should be able to describe changes that occur in a population and to predict changes in the future (prognosis). In this application, the model uses deterministic equation as the reaction function to describe the level of change in the concentration of glioma over time. This equation do not take into account random event.</span></p><p><span style=\" font-family:\'Sitka,serif\'; font-size:16pt;\">1</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">. </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600;\">Exponential</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">, describes a concentration that continues to grow in number without any limits. In the theory of natural selection by Charles Darwin, population with sufficient resources will grow dramatically fast. Thus, this growth can only occur when there is a small population and a lot of resources. When population size is drawn from time to time, it will form a J-shaped curve as shown: </span></p></body></html>"))
        self.lblSimulationTypeLogistic.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">2</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">. </span><span style=\" font-family:\'Sitka,serif\';\">Logistic</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, describes an increase of concentration with a carrying capacity which represents a maximum concentration that can be accomodated by an environment. The S-shaped curve of logistic growth consists of three different parts. Initially, the growth is exponential because only a few individuals and resources are available. Then, when the resourse start to be limited, the growth rate begins to decline. Finally, the growth rate will decrease when the concentration approaching the carrying capacity.</span></p></body></html>"))
        self.lblSimulationTypeGompertzian.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">3</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">. </span><span style=\" font-family:\'Sitka,serif\';\">Gompertzian</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, was developed by Benjamin Gompertz in 1938, used to describe solid tumor growth assuming that the growth rate decreases non-linearly as the mass increase. The greater the mass, the smaller the growth rate will be. Similar to logistic, this growth will also decrease when the concentration approaching the carrying capacity.</span></p></body></html>"))
        self.lblSimulationTypeReferences.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">References</span><span style=\" font-size:12pt; font-weight:400;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\">Fowler, S., Roush, R., &amp; Wise, J. (2013). Concepts of Biology. Houston: OpenStax.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\">Longo, D. L. (2017). Harrison\'s Hematology and Oncology, Third Edition. New York: McGraw-Hill Education Medical. </span></p></body></html>"))
        self.tabHelp.setTabText(self.tabHelp.indexOf(self.tabSimulationType), _translate("MainWindow", "Simulation Type"))
        self.lblInputParameter.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Input template available on </span><a href=\"https://drive.google.com/drive/folders/1LWBo43D2WYdd0RHgyaWW89M5xThjuMDy?usp=sharing\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">Google Drive</span></a></p><p><br/><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600; text-decoration: underline;\">BRAIN TISSUE ANATOMY</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">1</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: The length of left grey region or zone 1 (mm)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">2</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: The length of center white region or zone 2 (mm)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">3</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: The length of right grey region or zone 3 (mm)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">where L = L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">1</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> + L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">2</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> + L</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">3</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> is the length of brain tissue from cortex to ventricle</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">D</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">g</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: The diffusion coefficient of grey matter for zone 1 and zone 3 (mm-sq/day)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">D</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">w</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: The diffusion coefficient of white matter for zone 2 (mm-sq/day)</span><br/></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600; text-decoration: underline;\">TUMOR PROFILE</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">x</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: Initial location of the tumor along </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">x</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> axis, between 0 and L (mm)</span></p><p align=\"justify\"><a href=\"https://id.wikipedia.org/wiki/Rho\"><span style=\" font-size:14pt; font-style:italic; color:#000000;\">ρ</span></a><span style=\" font-size:14pt; color:#000000;\"> (r</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; color:#000000;\">ho): </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; color:#000000;\">Proliferation</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\"> rate of tumor (/day)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">C</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">0</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: Initial glioma concentration (cells/mm)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; text-decoration: underline;\">Specifically for logistic growth:</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">C</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; vertical-align:sub;\">max</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: Carrying capacity of tumor (cells/mm)</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; text-decoration: underline;\">Specifically for Gompertz growth:</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">k</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: Growth rate of tumor</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">d</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">: Density coefficient of tumor</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">where </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic;\">e</span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-style:italic; vertical-align:super;\">k/d </span><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">is the carrying capacity of tumor, e is Euler\'s number.</span><br/></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt; font-weight:600; text-decoration: underline;\">OBSERVATION TIME</span></p><p align=\"justify\"><span style=\" font-family:\'Sitka,serif\'; font-size:14pt;\">Time: Time to observe the tumor growth (days)</span></p></body></html>"))
        self.tabHelp.setTabText(self.tabHelp.indexOf(self.tabInputParameter), _translate("MainWindow", "Input Parameter"))
        self.lblOutputInformation.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">There are four types of output:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">1</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">. </span><span style=\" font-family:\'Sitka,serif\';\">Table</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, which displays the result of simulation: glioma concentration and the summary of other tumor attributes.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">The rows represent time from zero to observation time with time step = 1 day.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">The columns of glioma concentration represent spatial axis from zero to L with space step = 0.5 mm.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">The columns of summary table represent each tumor attributes by overall zone and each zone.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">The table can be exported to Excel file, to be analyzed further, by clicking &quot;Save Table&quot; button.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400;\"><br /></span><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">2</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">. </span><span style=\" font-family:\'Sitka,serif\';\">Two dimensional graph</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, which displays a plot of glioma concentration and other tumor attributes.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">Concentration graph displays a plot for glioma concentration against spatial axis by each time step. You can plot the time by a desired step and at a specific time by using the toolbox below the graph.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">Other tumor attributes display plot for the attribute against time by each zone.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">Output can be saved as an image by clicking the Save icon above the plot.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400;\"><br /></span><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">3</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">. </span><span style=\" font-family:\'Sitka,serif\';\">Three dimensional graph</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, which displays a plot of spatial axis, time, and glioma concentration. Output can be saved as an image by clicking Save icon above the plot.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sitka,serif\'; font-weight:400;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">Both two and three dimensional graph can be manipulated using the available toolbar located on the above and below the plot. Top toolbar is used to undo, redo, move, zoom in/out, configure subplots, edit axis, curve, image parameters and save. Bottom toolbar is used to enable annotation and legend/colorbar.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sitka,serif\'; font-weight:400;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sitka,serif\'; font-size:16pt; font-weight:400;\">4. </span><span style=\" font-family:\'Sitka,serif\';\">Two dimensional animation</span><span style=\" font-family:\'Sitka,serif\'; font-weight:400;\">, which display a dynamic plot of glioma concentration against spatial axis over time. Output can be saved as a .mp4 file by clicking &quot;Save Animation&quot; button below the plot.</span></p></body></html>"))
        self.tabHelp.setTabText(self.tabHelp.indexOf(self.tabOutputInformation), _translate("MainWindow", "Output Information"))

        self.lblInputTitle.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" text-decoration: underline;\">PARAMETER ILLUSTRATION</span></p></body></html>"))
        self.lblInputParameterReferences.setText(_translate("MainWindow","<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\"><br>Reference</span><span style=\" font-size:12pt; font-weight:400;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\">Marieb, E. N., & Hoehn, K. (2018). Human Anatomy & Physiology (11th Edition). Pearson.</span></p>\n"))

    # --------------------------------- EXPONENTIAL ---------------------------------
    def setupUi_Expo(self, MainWindow):
        self.frameExpo = QtWidgets.QFrame(self.centralwidget)
        self.frameExpo.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameExpo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameExpo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameExpo.setObjectName("frameExpo")
        self.lblExpoTitle = QtWidgets.QLabel(self.frameExpo)
        self.lblExpoTitle.setGeometry(QtCore.QRect(10, 10, 443, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblExpoTitle.setFont(font)
        self.lblExpoTitle.setObjectName("lblExpoTitle")
        self.imgIllustrationExpo = QtWidgets.QLabel(self.frameExpo)
        self.imgIllustrationExpo.setGeometry(QtCore.QRect(30, 80, 361, 211))
        self.imgIllustrationExpo.setFrameShape(QtWidgets.QFrame.Panel)
        self.imgIllustrationExpo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imgIllustrationExpo.setText("")
        self.imgIllustrationExpo.setPixmap(QtGui.QPixmap("asset/illustration/parameter.png"))
        self.imgIllustrationExpo.setScaledContents(True)
        self.imgIllustrationExpo.setObjectName("imgIllustrationExpo")
        self.btnExpoSimulate = QtWidgets.QPushButton(self.frameExpo)
        self.btnExpoSimulate.setEnabled(True)
        self.btnExpoSimulate.setGeometry(QtCore.QRect(600, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnExpoSimulate.setFont(font)
        self.btnExpoSimulate.setObjectName("btnExpoSimulate")
        self.btnExpoReset = QtWidgets.QPushButton(self.frameExpo)
        self.btnExpoReset.setGeometry(QtCore.QRect(490, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnExpoReset.setFont(font)
        self.btnExpoReset.setObjectName("btnExpoReset")
        self.lblExpoObservationTime = QtWidgets.QLabel(self.frameExpo)
        self.lblExpoObservationTime.setGeometry(QtCore.QRect(420, 310, 177, 29))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblExpoObservationTime.setFont(font)
        self.lblExpoObservationTime.setObjectName("lblExpoObservationTime")
        self.layoutWidget = QtWidgets.QWidget(self.frameExpo)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 350, 321, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayoutExpoBrain = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayoutExpoBrain.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayoutExpoBrain.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutExpoBrain.setObjectName("gridLayoutExpoBrain")
        self.lblInputExpoL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoL2.setFont(font)
        self.lblInputExpoL2.setObjectName("lblInputExpoL2")
        self.gridLayoutExpoBrain.addWidget(self.lblInputExpoL2, 1, 0, 1, 1)
        self.lblInputExpoL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoL3.setFont(font)
        self.lblInputExpoL3.setObjectName("lblInputExpoL3")
        self.gridLayoutExpoBrain.addWidget(self.lblInputExpoL3, 2, 0, 1, 1)
        self.lblInfoExpoDw = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoExpoDw.setText("")
        self.lblInfoExpoDw.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoDw.setObjectName("lblInfoExpoDw")
        self.gridLayoutExpoBrain.addWidget(self.lblInfoExpoDw, 4, 3, 1, 1)
        self.lblUnitExpoL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoL1.setFont(font)
        self.lblUnitExpoL1.setObjectName("lblUnitExpoL1")
        self.gridLayoutExpoBrain.addWidget(self.lblUnitExpoL1, 0, 2, 1, 1)
        self.lblInputExpoDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoDw.setFont(font)
        self.lblInputExpoDw.setWordWrap(True)
        self.lblInputExpoDw.setObjectName("lblInputExpoDw")
        self.gridLayoutExpoBrain.addWidget(self.lblInputExpoDw, 4, 0, 1, 1)
        self.txtExpoL3 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtExpoL3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoL3.setDecimals(3)
        self.txtExpoL3.setMaximum(100.0)
        self.txtExpoL3.setSingleStep(0.5)
        self.txtExpoL3.setObjectName("txtExpoL3")
        self.gridLayoutExpoBrain.addWidget(self.txtExpoL3, 2, 1, 1, 1)
        self.lblUnitExpoDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoDw.setFont(font)
        self.lblUnitExpoDw.setObjectName("lblUnitExpoDw")
        self.gridLayoutExpoBrain.addWidget(self.lblUnitExpoDw, 4, 2, 1, 1)
        self.txtExpoDw = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtExpoDw.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoDw.setDecimals(3)
        self.txtExpoDw.setMaximum(10.0)
        self.txtExpoDw.setSingleStep(0.01)
        self.txtExpoDw.setObjectName("txtExpoDw")
        self.gridLayoutExpoBrain.addWidget(self.txtExpoDw, 4, 1, 1, 1)
        self.lblInfoExpoL2 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoExpoL2.setText("")
        self.lblInfoExpoL2.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoL2.setObjectName("lblInfoExpoL2")
        self.gridLayoutExpoBrain.addWidget(self.lblInfoExpoL2, 1, 3, 1, 1)
        self.lblInfoExpoDg = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoExpoDg.setText("")
        self.lblInfoExpoDg.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoDg.setObjectName("lblInfoExpoDg")
        self.gridLayoutExpoBrain.addWidget(self.lblInfoExpoDg, 3, 3, 1, 1)
        self.txtExpoL2 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtExpoL2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoL2.setDecimals(3)
        self.txtExpoL2.setMaximum(100.0)
        self.txtExpoL2.setSingleStep(0.5)
        self.txtExpoL2.setObjectName("txtExpoL2")
        self.gridLayoutExpoBrain.addWidget(self.txtExpoL2, 1, 1, 1, 1)
        self.lblUnitExpoL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoL3.setFont(font)
        self.lblUnitExpoL3.setObjectName("lblUnitExpoL3")
        self.gridLayoutExpoBrain.addWidget(self.lblUnitExpoL3, 2, 2, 1, 1)
        self.txtExpoDg = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtExpoDg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoDg.setDecimals(3)
        self.txtExpoDg.setMaximum(10.0)
        self.txtExpoDg.setSingleStep(0.01)
        self.txtExpoDg.setObjectName("txtExpoDg")
        self.gridLayoutExpoBrain.addWidget(self.txtExpoDg, 3, 1, 1, 1)
        self.lblInfoExpoL1 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoExpoL1.setText("")
        self.lblInfoExpoL1.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoL1.setObjectName("lblInfoExpoL1")
        self.gridLayoutExpoBrain.addWidget(self.lblInfoExpoL1, 0, 3, 1, 1)
        self.lblUnitExpoL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoL2.setFont(font)
        self.lblUnitExpoL2.setObjectName("lblUnitExpoL2")
        self.gridLayoutExpoBrain.addWidget(self.lblUnitExpoL2, 1, 2, 1, 1)
        self.lblInfoExpoL3 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoExpoL3.setText("")
        self.lblInfoExpoL3.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoL3.setObjectName("lblInfoExpoL3")
        self.gridLayoutExpoBrain.addWidget(self.lblInfoExpoL3, 2, 3, 1, 1)
        self.lblUnitExpoDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoDg.setFont(font)
        self.lblUnitExpoDg.setObjectName("lblUnitExpoDg")
        self.gridLayoutExpoBrain.addWidget(self.lblUnitExpoDg, 3, 2, 1, 1)
        self.lblInputExpoL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoL1.setFont(font)
        self.lblInputExpoL1.setObjectName("lblInputExpoL1")
        self.gridLayoutExpoBrain.addWidget(self.lblInputExpoL1, 0, 0, 1, 1)
        self.lblInputExpoDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoDg.setFont(font)
        self.lblInputExpoDg.setWordWrap(True)
        self.lblInputExpoDg.setObjectName("lblInputExpoDg")
        self.gridLayoutExpoBrain.addWidget(self.lblInputExpoDg, 3, 0, 1, 1)
        self.txtExpoL1 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtExpoL1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoL1.setPrefix("")
        self.txtExpoL1.setDecimals(3)
        self.txtExpoL1.setMaximum(100.0)
        self.txtExpoL1.setSingleStep(0.5)
        self.txtExpoL1.setObjectName("txtExpoL1")
        self.gridLayoutExpoBrain.addWidget(self.txtExpoL1, 0, 1, 1, 1)
        self.gridLayoutExpoBrain.setColumnStretch(1, 1)
        self.lblExpoBrain = QtWidgets.QLabel(self.frameExpo)
        self.lblExpoBrain.setGeometry(QtCore.QRect(40, 310, 319, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblExpoBrain.setFont(font)
        self.lblExpoBrain.setObjectName("lblExpoBrain")
        self.lblExpoTumor = QtWidgets.QLabel(self.frameExpo)
        self.lblExpoTumor.setGeometry(QtCore.QRect(420, 80, 349, 37))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblExpoTumor.setFont(font)
        self.lblExpoTumor.setObjectName("lblExpoTumor")
        self.layoutWidget1 = QtWidgets.QWidget(self.frameExpo)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 120, 351, 91))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayoutExpoTumor = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayoutExpoTumor.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutExpoTumor.setObjectName("gridLayoutExpoTumor")
        self.txtExpoC0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtExpoC0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoC0.setDecimals(3)
        self.txtExpoC0.setMaximum(1000.0)
        self.txtExpoC0.setSingleStep(0.1)
        self.txtExpoC0.setObjectName("txtExpoC0")
        self.gridLayoutExpoTumor.addWidget(self.txtExpoC0, 2, 1, 1, 1)
        self.lblUnitExpoRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoRho.setFont(font)
        self.lblUnitExpoRho.setObjectName("lblUnitExpoRho")
        self.gridLayoutExpoTumor.addWidget(self.lblUnitExpoRho, 1, 2, 1, 1)
        self.lblInfoExpoC0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoExpoC0.setText("")
        self.lblInfoExpoC0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoC0.setObjectName("lblInfoExpoC0")
        self.gridLayoutExpoTumor.addWidget(self.lblInfoExpoC0, 2, 3, 1, 1)
        self.txtExpoRho = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtExpoRho.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoRho.setDecimals(3)
        self.txtExpoRho.setMaximum(10.0)
        self.txtExpoRho.setSingleStep(0.001)
        self.txtExpoRho.setObjectName("txtExpoRho")
        self.gridLayoutExpoTumor.addWidget(self.txtExpoRho, 1, 1, 1, 1)
        self.lblInputExpoRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoRho.setFont(font)
        self.lblInputExpoRho.setObjectName("lblInputExpoRho")
        self.gridLayoutExpoTumor.addWidget(self.lblInputExpoRho, 1, 0, 1, 1)
        self.lblUnitExpoX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoX0.setFont(font)
        self.lblUnitExpoX0.setObjectName("lblUnitExpoX0")
        self.gridLayoutExpoTumor.addWidget(self.lblUnitExpoX0, 0, 2, 1, 1)
        self.lblUnitExpoC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoC0.setFont(font)
        self.lblUnitExpoC0.setObjectName("lblUnitExpoC0")
        self.gridLayoutExpoTumor.addWidget(self.lblUnitExpoC0, 2, 2, 1, 1)
        self.lblInputExpoX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoX0.setFont(font)
        self.lblInputExpoX0.setObjectName("lblInputExpoX0")
        self.gridLayoutExpoTumor.addWidget(self.lblInputExpoX0, 0, 0, 1, 1)
        self.lblInputExpoC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoC0.setFont(font)
        self.lblInputExpoC0.setObjectName("lblInputExpoC0")
        self.gridLayoutExpoTumor.addWidget(self.lblInputExpoC0, 2, 0, 1, 1)
        self.lblInfoExpoRho = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoExpoRho.setText("")
        self.lblInfoExpoRho.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoRho.setObjectName("lblInfoExpoRho")
        self.gridLayoutExpoTumor.addWidget(self.lblInfoExpoRho, 1, 3, 1, 1)
        self.lblInfoExpoX0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoExpoX0.setText("")
        self.lblInfoExpoX0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoX0.setObjectName("lblInfoExpoX0")
        self.gridLayoutExpoTumor.addWidget(self.lblInfoExpoX0, 0, 3, 1, 1)
        self.txtExpoX0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtExpoX0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoX0.setDecimals(3)
        self.txtExpoX0.setMaximum(300.0)
        self.txtExpoX0.setSingleStep(0.5)
        self.txtExpoX0.setObjectName("txtExpoX0")
        self.gridLayoutExpoTumor.addWidget(self.txtExpoX0, 0, 1, 1, 1)
        self.gridLayoutExpoTumor.setColumnStretch(1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.frameExpo)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(420, 350, 351, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutExpoTime = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutExpoTime.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutExpoTime.setObjectName("gridLayoutExpoTime")
        self.lblUnitExpoTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitExpoTime.setFont(font)
        self.lblUnitExpoTime.setObjectName("lblUnitExpoTime")
        self.gridLayoutExpoTime.addWidget(self.lblUnitExpoTime, 0, 2, 1, 1)
        self.lblInputExpoTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputExpoTime.setFont(font)
        self.lblInputExpoTime.setObjectName("lblInputExpoTime")
        self.gridLayoutExpoTime.addWidget(self.lblInputExpoTime, 0, 0, 1, 1)
        self.txtExpoTime = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.txtExpoTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtExpoTime.setDecimals(3)
        self.txtExpoTime.setMaximum(1500.0)
        self.txtExpoTime.setSingleStep(1.0)
        self.txtExpoTime.setObjectName("txtExpoTime")
        self.gridLayoutExpoTime.addWidget(self.txtExpoTime, 0, 1, 1, 1)
        self.lblInfoExpoTime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblInfoExpoTime.setText("")
        self.lblInfoExpoTime.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoExpoTime.setObjectName("lblInfoExpoTime")
        self.gridLayoutExpoTime.addWidget(self.lblInfoExpoTime, 0, 3, 1, 1)
        self.gridLayoutExpoTime.setColumnStretch(1, 1)
        self.groupBoxExpo = QtWidgets.QGroupBox(self.frameExpo)
        self.groupBoxExpo.setGeometry(QtCore.QRect(420, 410, 351, 80))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxExpo.setFont(font)
        self.groupBoxExpo.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxExpo.setObjectName("groupBoxExpo")
        self.btnExpoSampleData = QtWidgets.QPushButton(self.groupBoxExpo)
        self.btnExpoSampleData.setGeometry(QtCore.QRect(70, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnExpoSampleData.setFont(font)
        self.btnExpoSampleData.setObjectName("btnExpoSampleData")
        self.btnExpoImport = QtWidgets.QPushButton(self.groupBoxExpo)
        self.btnExpoImport.setGeometry(QtCore.QRect(180, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnExpoImport.setFont(font)
        self.btnExpoImport.setObjectName("btnExpoImport")

        MainWindow.setTabOrder(self.txtExpoL1, self.txtExpoL2)
        MainWindow.setTabOrder(self.txtExpoL2, self.txtExpoL3)
        MainWindow.setTabOrder(self.txtExpoL3, self.txtExpoDg)
        MainWindow.setTabOrder(self.txtExpoDg, self.txtExpoDw)
        MainWindow.setTabOrder(self.txtExpoDw, self.txtExpoX0)
        MainWindow.setTabOrder(self.txtExpoX0, self.txtExpoRho)
        MainWindow.setTabOrder(self.txtExpoRho, self.txtExpoC0)
        MainWindow.setTabOrder(self.txtExpoC0, self.txtExpoTime)
        MainWindow.setTabOrder(self.txtExpoTime, self.btnExpoSimulate)
        MainWindow.setTabOrder(self.btnExpoSimulate, self.btnExpoReset)
        MainWindow.setTabOrder(self.btnExpoReset, self.btnExpoSampleData)
        MainWindow.setTabOrder(self.btnExpoSampleData, self.btnExpoImport)

        self.txtExpo = [self.txtExpoL1, self.txtExpoL2, self.txtExpoL3, self.txtExpoDg, self.txtExpoDw, self.txtExpoX0, self.txtExpoRho, self.txtExpoC0, self.txtExpoTime]
        self.varExpo = ['L1', 'L2', 'L3', 'Dg', 'Dw', 'x0', 'rho', 'C0', 'tf']
        self.lblInfoExpo = [self.lblInfoExpoL1, self.lblInfoExpoL2, self.lblInfoExpoL3, self.lblInfoExpoDg, self.lblInfoExpoDw, self.lblInfoExpoX0, self.lblInfoExpoRho, self.lblInfoExpoC0, self.lblInfoExpoTime]

        self.btnExpoSimulate.clicked.connect(lambda: self.runSimulation("Exponential"))
        self.btnExpoSimulate.setAutoDefault(True)
        self.btnExpoReset.clicked.connect(lambda: self.resetInputExpo(popUpResetDialog = True))
        self.btnExpoReset.setAutoDefault(True)
        self.btnExpoSampleData.clicked.connect(lambda: self.useSampleData(self.txtExpo, self.varExpo, "Exponential"))
        self.btnExpoSampleData.setAutoDefault(True)
        self.btnExpoImport.clicked.connect(lambda: self.importData("Exponential"))
        self.btnExpoImport.setAutoDefault(True)

        self.txtExpoL1.setMinimum(1)
        self.txtExpoL2.setMinimum(1)
        self.txtExpoL3.setMinimum(1)

    def retranslateUi_Expo(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblExpoTitle.setText(_translate("MainWindow", "EXPONENTIAL GROWTH"))
        self.imgIllustrationExpo.setToolTip(_translate("MainWindow", "Parameter Illustration"))
        self.btnExpoSimulate.setToolTip(_translate("MainWindow", "Simulate using current data"))
        self.btnExpoSimulate.setText(_translate("MainWindow", "Simulate"))
        self.btnExpoReset.setToolTip(_translate("MainWindow", "Reset all field to default value"))
        self.btnExpoReset.setText(_translate("MainWindow", "Reset"))
        self.lblExpoObservationTime.setText(_translate("MainWindow", "OBSERVATION TIME"))
        self.lblInputExpoL2.setText(_translate("MainWindow", "Zone 2 Length (L2)"))
        self.lblInputExpoL3.setText(_translate("MainWindow", "Zone 3 Length (L3)"))
        self.lblInfoExpoDw.setToolTip(_translate("MainWindow", "Diffusion coefficient for Zone 2\n"
"- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblUnitExpoL1.setText(_translate("MainWindow", "mm"))
        self.lblInputExpoDw.setText(_translate("MainWindow", "Diffusion Coefficient of White Matter (Dw)"))
        self.txtExpoL3.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitExpoDw.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.txtExpoDw.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblInfoExpoL2.setToolTip(_translate("MainWindow", "Length of center white region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblInfoExpoDg.setToolTip(_translate("MainWindow", "Diffusion coefficient for both Zone 1 and Zone 3\n"
"- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.txtExpoL2.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitExpoL3.setText(_translate("MainWindow", "mm"))
        self.txtExpoDg.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.lblInfoExpoL1.setToolTip(_translate("MainWindow", "Length of left grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitExpoL2.setText(_translate("MainWindow", "mm"))
        self.lblInfoExpoL3.setToolTip(_translate("MainWindow", "Length of right grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitExpoDg.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.lblInputExpoL1.setText(_translate("MainWindow", "Zone 1 Length (L1)"))
        self.lblInputExpoDg.setText(_translate("MainWindow", "Diffusion Coefficient of Grey Matter (Dg)"))
        self.txtExpoL1.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblExpoBrain.setText(_translate("MainWindow", "BRAIN TISSUE ANATOMY"))
        self.lblExpoTumor.setText(_translate("MainWindow", "TUMOR PROFILE"))
        self.txtExpoC0.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblUnitExpoRho.setText(_translate("MainWindow", "/day"))
        self.lblInfoExpoC0.setToolTip(_translate("MainWindow", "Initial concentration of tumor\n"
"- Must not be zero"))
        self.txtExpoRho.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblInputExpoRho.setText(_translate("MainWindow", "Proliferation Rate (ρ)"))
        self.lblUnitExpoX0.setText(_translate("MainWindow", "mm"))
        self.lblUnitExpoC0.setText(_translate("MainWindow", "cells/mm"))
        self.lblInputExpoX0.setText(_translate("MainWindow", "Initial Location (X0)"))
        self.lblInputExpoC0.setText(_translate("MainWindow", "Initial Concentration (C0)  "))
        self.lblInfoExpoRho.setToolTip(_translate("MainWindow", "Proliferation rate of tumor\n"
"- Must not be zero"))
        self.lblInfoExpoX0.setToolTip(_translate("MainWindow", "Initial location of tumor along X axis\n"
"- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.txtExpoX0.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.lblUnitExpoTime.setText(_translate("MainWindow", "days      "))
        self.lblInputExpoTime.setText(_translate("MainWindow", "Time                                    "))
        self.txtExpoTime.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be an integer"))
        self.lblInfoExpoTime.setToolTip(_translate("MainWindow", "Time to observe the tumor growth\n"
"- Must not be zero\n"
"- Has to be an integer"))
        self.groupBoxExpo.setTitle(_translate("MainWindow", "USE EXISTING DATA"))
        self.btnExpoSampleData.setToolTip(_translate("MainWindow", "Use sample data"))
        self.btnExpoSampleData.setText(_translate("MainWindow", "Sample Data"))
        self.btnExpoImport.setToolTip(_translate("MainWindow", "Import data from Excel File"))
        self.btnExpoImport.setText(_translate("MainWindow", "Import"))

        for i in range(len(self.lblInfoExpo)):
            self.lblInfoExpo[i].setPixmap(self.icon['q'])
        
    def runSimulationExpo(self):
        self.retranslateUi_Expo(self)
        inputFlag = True

        dx = decimal.Decimal('0.5')
        
        L1 = round(self.txtExpoL1.value(), 3)
        L2 = round(self.txtExpoL2.value(), 3)
        L3 = round(self.txtExpoL3.value(), 3)
        Dg = round(self.txtExpoDg.value(), 3)
        Dw = round(self.txtExpoDw.value(), 3)
        x0 = round(self.txtExpoX0.value(), 3)
        C0 = round(self.txtExpoC0.value(), 3)
        rho = round(self.txtExpoRho.value(), 3)
        tf = round(self.txtExpoTime.value(), 3)

        if decimal.Decimal(L1) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoExpoL1)

        if decimal.Decimal(L2) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoExpoL2)

        if decimal.Decimal(L3) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoExpoL3)

        if Dg == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoDg)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be smaller than white matter diffusion coefficient (Dw)", self.lblInfoExpoDg)

        if Dw == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoDw)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be greater than grey matter diffusion coefficient (Dg)", self.lblInfoExpoDw)

        if x0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoX0)
        elif decimal.Decimal(x0) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoExpoX0)
        elif not(x0 < (L1+L2+L3)):
            inputFlag = self.setErrorMessage("Input must be between 0 and L, where L is the total length of Zone 1, 2, 3", self.lblInfoExpoX0)

        if C0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoC0)

        if rho == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoRho)

        if tf == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoExpoTime)
        elif tf % 1 != 0:
            inputFlag = self.setErrorMessage("Input has to be an integer", self.lblInfoExpoTime)

        if inputFlag == False:
            dialog = CustomDialog("Input Error",
                                  "Invalid input.",
                                  "Please recheck your input and try again.",
                                  "Error",
                                  QtWidgets.QDialogButtonBox.Ok)
            dialog.exec_()
        else:
            self.showLoading()

            dataInput = np.array([
                ["Zone 1 Length", "L1", L1, "mm"],
                ["Zone 2 Length", "L2", L2, "mm"],
                ["Zone 3 Length", "L3", L3, "mm"],
                ["Diffusion Coef. Grey Region", "Dg", Dg, "mm-sq/day"],
                ["Diffusion Coef. White Region", "Dw", Dw, "mm-sq/day"],
                ["Tumor Initial Position", "x0", x0, "mm"],
                ["Tumor Proliferation Rate", "rho", rho, "/day"],
                ["Tumor Initial Concentration", "C0", C0, "cells/mm"],
                ["Observation Time", "tf", tf, "days"]])

            self.lblResultTitle.setText(QtCore.QCoreApplication.translate("MainWindow", "RESULT FOR EXPONENTIAL GROWTH"))
            self.setTableInput(dataInput)
            
            self.tumor = Linear(
                growthType = "Exponential",
                L1 = L1,
                L2 = L2,
                L3 = L3,
                Dg = Dg,
                Dw = Dw,
                x0 = x0,
                C0 = C0,
                rho = rho,
                tf = tf)

            self.outputTypeChanged("Table")
            self.setTableOutput(self.frameOutputConcentrationTable, "outputConcentration")
            self.initiateSpinBoxPlot2D()
            self.showResult()

    def resetInputExpo(self, flagReset=True, popUpResetDialog=True):
        if popUpResetDialog:
            dialog = CustomDialog("Reset",
                                  "Are you sure you want to reset?",
                                  "All input data will be set to default.",
                                  "Warning",
                                  QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            flagReset = dialog.exec_()
            
        if flagReset:
            self.retranslateUi_Expo(self)
            
            for i in range(len(self.txtExpo)):
                self.txtExpo[i].setValue(0)

    # --------------------------------- IMPORT DATA & OPEN FILE ---------------------------------
    def importData(self, growthType):
        inputDict = self.openFile(growthType)
        txtList = {'Exponential': self.txtExpo,
                   'Logistic': self.txtLogistic,
                   'Gompertzian': self.txtGompertzian}
        varList = {'Exponential': self.varExpo,
                   'Logistic': self.varLogistic,
                   'Gompertzian': self.varGompertzian}
        lblList = {'Exponential': self.lblInfoExpo,
                   'Logistic': self.lblInfoLogistic,
                   'Gompertzian': self.lblInfoGompertzian}
        
        if inputDict:
            notFoundVar = []

            if growthType == "Exponential":
                self.resetInputExpo(flagReset=True, popUpResetDialog=False)
            elif growthType == "Logistic":
                self.resetInputLogistic(flagReset=True, popUpResetDialog=False)
            elif growthType == "Gompertzian":
                self.resetInputGompertzian(flagReset=True, popUpResetDialog=False)
            
            for i in range(len(txtList[growthType])):
                val = inputDict[varList[growthType][i]]

                if np.isnan(val):
                    notFoundVar.append(i)
                else:
                    try:
                        txtList[growthType][i].setValue(val)
                    except Exception as ex:
                        notFoundVar.append(i)

            if len(notFoundVar) == 0:
                dialog = CustomDialog("Import Success",
                                      "Import file success.",
                                      "All data have been input successfully.",
                                      "Success",
                                      QtWidgets.QDialogButtonBox.Ok)
                dialog.exec_()
            else:
                #Partial fail

                for i in notFoundVar:
                    self.setErrorMessage("Input is not recognized from file", lblList[growthType][i])

                dialog = CustomDialog("Import Incomplete",
                                      "Some input is not recognized.",
                                      "Please input the missing value(s).",
                                      "Warning",
                                      QtWidgets.QDialogButtonBox.Ok)
                dialog.exec_()
                
        
    def openFile(self, growthType):
        file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                     "Open File",
                                                     "",
                                                     "Excel Workbook (*.xlsx);;Excel 97-2003 Workbook (*.xls)")
        if file[0]:
            try:
                if file[1] in ["Excel Workbook (*.xlsx)", "Excel 97-2003 Workbook (*.xls)"]:
                    df = pd.read_excel(file[0], sheet_name = growthType)
                elif file[1] == "CSV (*.csv)":
                    df = pd.read_csv(file[0])

                return df["Value"].rename(index = df["Symbol"]).to_dict()
            except Exception as ex:
                dialog = CustomDialog("Import Error",
                                      "Import file error.",
                                      str(ex),
                                      "Error",
                                      QtWidgets.QDialogButtonBox.Ok)
                dialog.exec_()
                return False

    # --------------------------------- LOGISTIC ---------------------------------
    def setupUi_Logistic(self, MainWindow):
        self.frameLogistic = QtWidgets.QFrame(self.centralwidget)
        self.frameLogistic.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameLogistic.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLogistic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLogistic.setObjectName("frameLogistic")
        self.lblLogisticTitle = QtWidgets.QLabel(self.frameLogistic)
        self.lblLogisticTitle.setGeometry(QtCore.QRect(10, 10, 443, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblLogisticTitle.setFont(font)
        self.lblLogisticTitle.setObjectName("lblLogisticTitle")
        self.imgIllustrationLogistic = QtWidgets.QLabel(self.frameLogistic)
        self.imgIllustrationLogistic.setGeometry(QtCore.QRect(30, 80, 361, 211))
        self.imgIllustrationLogistic.setFrameShape(QtWidgets.QFrame.Panel)
        self.imgIllustrationLogistic.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imgIllustrationLogistic.setText("")
        self.imgIllustrationLogistic.setPixmap(QtGui.QPixmap("asset/illustration/parameter.png"))
        self.imgIllustrationLogistic.setScaledContents(True)
        self.imgIllustrationLogistic.setObjectName("imgIllustrationLogistic")
        self.lblLogisticObservationTime = QtWidgets.QLabel(self.frameLogistic)
        self.lblLogisticObservationTime.setGeometry(QtCore.QRect(420, 310, 177, 29))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblLogisticObservationTime.setFont(font)
        self.lblLogisticObservationTime.setObjectName("lblLogisticObservationTime")
        self.layoutWidget = QtWidgets.QWidget(self.frameLogistic)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 350, 321, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayoutLogisticBrain = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayoutLogisticBrain.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayoutLogisticBrain.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLogisticBrain.setObjectName("gridLayoutLogisticBrain")
        self.lblInputLogisticL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticL2.setFont(font)
        self.lblInputLogisticL2.setObjectName("lblInputLogisticL2")
        self.gridLayoutLogisticBrain.addWidget(self.lblInputLogisticL2, 1, 0, 1, 1)
        self.lblInputLogisticL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticL3.setFont(font)
        self.lblInputLogisticL3.setObjectName("lblInputLogisticL3")
        self.gridLayoutLogisticBrain.addWidget(self.lblInputLogisticL3, 2, 0, 1, 1)
        self.lblInfoLogisticDw = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoLogisticDw.setText("")
        self.lblInfoLogisticDw.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticDw.setObjectName("lblInfoLogisticDw")
        self.gridLayoutLogisticBrain.addWidget(self.lblInfoLogisticDw, 4, 3, 1, 1)
        self.lblUnitLogisticL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticL1.setFont(font)
        self.lblUnitLogisticL1.setObjectName("lblUnitLogisticL1")
        self.gridLayoutLogisticBrain.addWidget(self.lblUnitLogisticL1, 0, 2, 1, 1)
        self.lblInputLogisticDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticDw.setFont(font)
        self.lblInputLogisticDw.setWordWrap(True)
        self.lblInputLogisticDw.setObjectName("lblInputLogisticDw")
        self.gridLayoutLogisticBrain.addWidget(self.lblInputLogisticDw, 4, 0, 1, 1)
        self.txtLogisticL3 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtLogisticL3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticL3.setDecimals(3)
        self.txtLogisticL3.setMaximum(100.0)
        self.txtLogisticL3.setSingleStep(0.5)
        self.txtLogisticL3.setObjectName("txtLogisticL3")
        self.gridLayoutLogisticBrain.addWidget(self.txtLogisticL3, 2, 1, 1, 1)
        self.lblUnitLogisticDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticDw.setFont(font)
        self.lblUnitLogisticDw.setObjectName("lblUnitLogisticDw")
        self.gridLayoutLogisticBrain.addWidget(self.lblUnitLogisticDw, 4, 2, 1, 1)
        self.txtLogisticDw = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtLogisticDw.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticDw.setDecimals(3)
        self.txtLogisticDw.setMaximum(10.0)
        self.txtLogisticDw.setSingleStep(0.01)
        self.txtLogisticDw.setObjectName("txtLogisticDw")
        self.gridLayoutLogisticBrain.addWidget(self.txtLogisticDw, 4, 1, 1, 1)
        self.lblInfoLogisticL2 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoLogisticL2.setText("")
        self.lblInfoLogisticL2.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticL2.setObjectName("lblInfoLogisticL2")
        self.gridLayoutLogisticBrain.addWidget(self.lblInfoLogisticL2, 1, 3, 1, 1)
        self.lblInfoLogisticDg = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoLogisticDg.setText("")
        self.lblInfoLogisticDg.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticDg.setObjectName("lblInfoLogisticDg")
        self.gridLayoutLogisticBrain.addWidget(self.lblInfoLogisticDg, 3, 3, 1, 1)
        self.txtLogisticL2 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtLogisticL2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticL2.setDecimals(3)
        self.txtLogisticL2.setMaximum(100.0)
        self.txtLogisticL2.setSingleStep(0.5)
        self.txtLogisticL2.setObjectName("txtLogisticL2")
        self.gridLayoutLogisticBrain.addWidget(self.txtLogisticL2, 1, 1, 1, 1)
        self.lblUnitLogisticL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticL3.setFont(font)
        self.lblUnitLogisticL3.setObjectName("lblUnitLogisticL3")
        self.gridLayoutLogisticBrain.addWidget(self.lblUnitLogisticL3, 2, 2, 1, 1)
        self.txtLogisticDg = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtLogisticDg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticDg.setDecimals(3)
        self.txtLogisticDg.setMaximum(10.0)
        self.txtLogisticDg.setSingleStep(0.01)
        self.txtLogisticDg.setObjectName("txtLogisticDg")
        self.gridLayoutLogisticBrain.addWidget(self.txtLogisticDg, 3, 1, 1, 1)
        self.lblInfoLogisticL1 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoLogisticL1.setText("")
        self.lblInfoLogisticL1.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticL1.setObjectName("lblInfoLogisticL1")
        self.gridLayoutLogisticBrain.addWidget(self.lblInfoLogisticL1, 0, 3, 1, 1)
        self.lblUnitLogisticL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticL2.setFont(font)
        self.lblUnitLogisticL2.setObjectName("lblUnitLogisticL2")
        self.gridLayoutLogisticBrain.addWidget(self.lblUnitLogisticL2, 1, 2, 1, 1)
        self.lblInfoLogisticL3 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoLogisticL3.setText("")
        self.lblInfoLogisticL3.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticL3.setObjectName("lblInfoLogisticL3")
        self.gridLayoutLogisticBrain.addWidget(self.lblInfoLogisticL3, 2, 3, 1, 1)
        self.lblUnitLogisticDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticDg.setFont(font)
        self.lblUnitLogisticDg.setObjectName("lblUnitLogisticDg")
        self.gridLayoutLogisticBrain.addWidget(self.lblUnitLogisticDg, 3, 2, 1, 1)
        self.lblInputLogisticL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticL1.setFont(font)
        self.lblInputLogisticL1.setObjectName("lblInputLogisticL1")
        self.gridLayoutLogisticBrain.addWidget(self.lblInputLogisticL1, 0, 0, 1, 1)
        self.lblInputLogisticDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticDg.setFont(font)
        self.lblInputLogisticDg.setWordWrap(True)
        self.lblInputLogisticDg.setObjectName("lblInputLogisticDg")
        self.gridLayoutLogisticBrain.addWidget(self.lblInputLogisticDg, 3, 0, 1, 1)
        self.txtLogisticL1 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtLogisticL1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticL1.setPrefix("")
        self.txtLogisticL1.setDecimals(3)
        self.txtLogisticL1.setMaximum(100.0)
        self.txtLogisticL1.setSingleStep(0.5)
        self.txtLogisticL1.setObjectName("txtLogisticL1")
        self.gridLayoutLogisticBrain.addWidget(self.txtLogisticL1, 0, 1, 1, 1)
        self.gridLayoutLogisticBrain.setColumnStretch(1, 1)
        self.lblLogisticBrain = QtWidgets.QLabel(self.frameLogistic)
        self.lblLogisticBrain.setGeometry(QtCore.QRect(40, 310, 319, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblLogisticBrain.setFont(font)
        self.lblLogisticBrain.setObjectName("lblLogisticBrain")
        self.lblLogisticTumor = QtWidgets.QLabel(self.frameLogistic)
        self.lblLogisticTumor.setGeometry(QtCore.QRect(420, 80, 349, 37))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblLogisticTumor.setFont(font)
        self.lblLogisticTumor.setObjectName("lblLogisticTumor")
        self.layoutWidget1 = QtWidgets.QWidget(self.frameLogistic)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 120, 351, 121))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayoutLogisticTumor = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayoutLogisticTumor.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLogisticTumor.setObjectName("gridLayoutLogisticTumor")
        self.txtLogisticC0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtLogisticC0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticC0.setDecimals(3)
        self.txtLogisticC0.setMaximum(10000.0)
        self.txtLogisticC0.setSingleStep(0.1)
        self.txtLogisticC0.setObjectName("txtLogisticC0")
        self.gridLayoutLogisticTumor.addWidget(self.txtLogisticC0, 2, 1, 1, 1)
        self.lblUnitLogisticC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticC0.setFont(font)
        self.lblUnitLogisticC0.setObjectName("lblUnitLogisticC0")
        self.gridLayoutLogisticTumor.addWidget(self.lblUnitLogisticC0, 2, 2, 1, 1)
        self.lblUnitLogisticX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticX0.setFont(font)
        self.lblUnitLogisticX0.setObjectName("lblUnitLogisticX0")
        self.gridLayoutLogisticTumor.addWidget(self.lblUnitLogisticX0, 0, 2, 1, 1)
        self.lblInfoLogisticC0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoLogisticC0.setText("")
        self.lblInfoLogisticC0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticC0.setObjectName("lblInfoLogisticC0")
        self.gridLayoutLogisticTumor.addWidget(self.lblInfoLogisticC0, 2, 3, 1, 1)
        self.lblInputLogisticCmax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticCmax.setFont(font)
        self.lblInputLogisticCmax.setObjectName("lblInputLogisticCmax")
        self.gridLayoutLogisticTumor.addWidget(self.lblInputLogisticCmax, 3, 0, 1, 1)
        self.lblUnitLogisticRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticRho.setFont(font)
        self.lblUnitLogisticRho.setObjectName("lblUnitLogisticRho")
        self.gridLayoutLogisticTumor.addWidget(self.lblUnitLogisticRho, 1, 2, 1, 1)
        self.txtLogisticRho = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtLogisticRho.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticRho.setDecimals(3)
        self.txtLogisticRho.setMaximum(10.0)
        self.txtLogisticRho.setSingleStep(0.001)
        self.txtLogisticRho.setObjectName("txtLogisticRho")
        self.gridLayoutLogisticTumor.addWidget(self.txtLogisticRho, 1, 1, 1, 1)
        self.lblInputLogisticRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticRho.setFont(font)
        self.lblInputLogisticRho.setObjectName("lblInputLogisticRho")
        self.gridLayoutLogisticTumor.addWidget(self.lblInputLogisticRho, 1, 0, 1, 1)
        self.lblInfoLogisticRho = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoLogisticRho.setText("")
        self.lblInfoLogisticRho.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticRho.setObjectName("lblInfoLogisticRho")
        self.gridLayoutLogisticTumor.addWidget(self.lblInfoLogisticRho, 1, 3, 1, 1)
        self.txtLogisticCmax = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtLogisticCmax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticCmax.setDecimals(3)
        self.txtLogisticCmax.setMaximum(10000.0)
        self.txtLogisticCmax.setSingleStep(0.1)
        self.txtLogisticCmax.setObjectName("txtLogisticCmax")
        self.gridLayoutLogisticTumor.addWidget(self.txtLogisticCmax, 3, 1, 1, 1)
        self.lblUnitLogisticCmax = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticCmax.setFont(font)
        self.lblUnitLogisticCmax.setObjectName("lblUnitLogisticCmax")
        self.gridLayoutLogisticTumor.addWidget(self.lblUnitLogisticCmax, 3, 2, 1, 1)
        self.lblInputLogisticC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticC0.setFont(font)
        self.lblInputLogisticC0.setObjectName("lblInputLogisticC0")
        self.gridLayoutLogisticTumor.addWidget(self.lblInputLogisticC0, 2, 0, 1, 1)
        self.lblInfoLogisticCmax = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoLogisticCmax.setText("")
        self.lblInfoLogisticCmax.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticCmax.setObjectName("lblInfoLogisticCmax")
        self.gridLayoutLogisticTumor.addWidget(self.lblInfoLogisticCmax, 3, 3, 1, 1)
        self.txtLogisticX0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtLogisticX0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticX0.setDecimals(3)
        self.txtLogisticX0.setMaximum(300.0)
        self.txtLogisticX0.setSingleStep(0.5)
        self.txtLogisticX0.setObjectName("txtLogisticX0")
        self.gridLayoutLogisticTumor.addWidget(self.txtLogisticX0, 0, 1, 1, 1)
        self.lblInfoLogisticX0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoLogisticX0.setText("")
        self.lblInfoLogisticX0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticX0.setObjectName("lblInfoLogisticX0")
        self.gridLayoutLogisticTumor.addWidget(self.lblInfoLogisticX0, 0, 3, 1, 1)
        self.lblInputLogisticX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticX0.setFont(font)
        self.lblInputLogisticX0.setObjectName("lblInputLogisticX0")
        self.gridLayoutLogisticTumor.addWidget(self.lblInputLogisticX0, 0, 0, 1, 1)
        self.gridLayoutLogisticTumor.setColumnStretch(1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.frameLogistic)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(420, 350, 351, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutLogisticTime = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutLogisticTime.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLogisticTime.setObjectName("gridLayoutLogisticTime")
        self.lblUnitLogisticTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitLogisticTime.setFont(font)
        self.lblUnitLogisticTime.setObjectName("lblUnitLogisticTime")
        self.gridLayoutLogisticTime.addWidget(self.lblUnitLogisticTime, 0, 2, 1, 1)
        self.lblInputLogisticTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputLogisticTime.setFont(font)
        self.lblInputLogisticTime.setObjectName("lblInputLogisticTime")
        self.gridLayoutLogisticTime.addWidget(self.lblInputLogisticTime, 0, 0, 1, 1)
        self.txtLogisticTime = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.txtLogisticTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtLogisticTime.setDecimals(3)
        self.txtLogisticTime.setMaximum(1500.0)
        self.txtLogisticTime.setSingleStep(1.0)
        self.txtLogisticTime.setObjectName("txtLogisticTime")
        self.gridLayoutLogisticTime.addWidget(self.txtLogisticTime, 0, 1, 1, 1)
        self.lblInfoLogisticTime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblInfoLogisticTime.setText("")
        self.lblInfoLogisticTime.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoLogisticTime.setObjectName("lblInfoLogisticTime")
        self.gridLayoutLogisticTime.addWidget(self.lblInfoLogisticTime, 0, 3, 1, 1)
        self.gridLayoutLogisticTime.setColumnStretch(1, 1)
        self.btnLogisticReset = QtWidgets.QPushButton(self.frameLogistic)
        self.btnLogisticReset.setGeometry(QtCore.QRect(490, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogisticReset.setFont(font)
        self.btnLogisticReset.setObjectName("btnLogisticReset")
        self.btnLogisticSimulate = QtWidgets.QPushButton(self.frameLogistic)
        self.btnLogisticSimulate.setEnabled(True)
        self.btnLogisticSimulate.setGeometry(QtCore.QRect(600, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogisticSimulate.setFont(font)
        self.btnLogisticSimulate.setObjectName("btnLogisticSimulate")
        self.groupBoxLogistic = QtWidgets.QGroupBox(self.frameLogistic)
        self.groupBoxLogistic.setGeometry(QtCore.QRect(420, 410, 351, 80))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxLogistic.setFont(font)
        self.groupBoxLogistic.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxLogistic.setObjectName("groupBoxLogistic")
        self.btnLogisticSampleData = QtWidgets.QPushButton(self.groupBoxLogistic)
        self.btnLogisticSampleData.setGeometry(QtCore.QRect(70, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogisticSampleData.setFont(font)
        self.btnLogisticSampleData.setObjectName("btnLogisticSampleData")
        self.btnLogisticImport = QtWidgets.QPushButton(self.groupBoxLogistic)
        self.btnLogisticImport.setGeometry(QtCore.QRect(180, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnLogisticImport.setFont(font)
        self.btnLogisticImport.setObjectName("btnLogisticImport")

        MainWindow.setTabOrder(self.txtLogisticL1, self.txtLogisticL2)
        MainWindow.setTabOrder(self.txtLogisticL2, self.txtLogisticL3)
        MainWindow.setTabOrder(self.txtLogisticL3, self.txtLogisticDg)
        MainWindow.setTabOrder(self.txtLogisticDg, self.txtLogisticDw)
        MainWindow.setTabOrder(self.txtLogisticDw, self.txtLogisticX0)
        MainWindow.setTabOrder(self.txtLogisticX0, self.txtLogisticRho)
        MainWindow.setTabOrder(self.txtLogisticRho, self.txtLogisticC0)
        MainWindow.setTabOrder(self.txtLogisticC0, self.txtLogisticCmax)
        MainWindow.setTabOrder(self.txtLogisticCmax, self.txtLogisticTime)
        MainWindow.setTabOrder(self.txtLogisticTime, self.btnLogisticSimulate)
        MainWindow.setTabOrder(self.btnLogisticSimulate, self.btnLogisticReset)
        MainWindow.setTabOrder(self.btnLogisticReset, self.btnLogisticSampleData)
        MainWindow.setTabOrder(self.btnLogisticSampleData, self.btnLogisticImport)

        self.txtLogistic = [self.txtLogisticL1, self.txtLogisticL2, self.txtLogisticL3, self.txtLogisticDg, self.txtLogisticDw, self.txtLogisticX0, self.txtLogisticRho, self.txtLogisticC0, self.txtLogisticCmax, self.txtLogisticTime]
        self.varLogistic = ['L1', 'L2', 'L3', 'Dg', 'Dw', 'x0', 'rho', 'C0', 'Cmax', 'tf']
        self.lblInfoLogistic = [self.lblInfoLogisticL1, self.lblInfoLogisticL2, self.lblInfoLogisticL3, self.lblInfoLogisticDg, self.lblInfoLogisticDw, self.lblInfoLogisticX0, self.lblInfoLogisticRho, self.lblInfoLogisticC0, self.lblInfoLogisticCmax, self.lblInfoLogisticTime]

        self.btnLogisticSimulate.clicked.connect(lambda: self.runSimulation("Logistic"))
        self.btnLogisticSimulate.setAutoDefault(True)
        self.btnLogisticReset.clicked.connect(lambda: self.resetInputLogistic(popUpResetDialog = True))
        self.btnLogisticReset.setAutoDefault(True)
        self.btnLogisticSampleData.clicked.connect(lambda: self.useSampleData(self.txtLogistic, self.varLogistic, "Logistic"))
        self.btnLogisticSampleData.setAutoDefault(True)
        self.btnLogisticImport.clicked.connect(lambda: self.importData("Logistic"))
        self.btnLogisticImport.setAutoDefault(True)

        self.txtLogisticL1.setMinimum(1)
        self.txtLogisticL2.setMinimum(1)
        self.txtLogisticL3.setMinimum(1)
        
    def retranslateUi_Logistic(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblLogisticTitle.setText(_translate("MainWindow", "LOGISTIC GROWTH"))
        self.imgIllustrationLogistic.setToolTip(_translate("MainWindow", "Parameter Illustration"))
        self.lblLogisticObservationTime.setText(_translate("MainWindow", "OBSERVATION TIME"))
        self.lblInputLogisticL2.setText(_translate("MainWindow", "Zone 2 Length (L2)"))
        self.lblInputLogisticL3.setText(_translate("MainWindow", "Zone 3 Length (L3)"))
        self.lblInfoLogisticDw.setToolTip(_translate("MainWindow", "Diffusion coefficient for Zone 2\n"
"- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblUnitLogisticL1.setText(_translate("MainWindow", "mm"))
        self.lblInputLogisticDw.setText(_translate("MainWindow", "Diffusion Coefficient of White Matter (Dw)"))
        self.txtLogisticL3.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitLogisticDw.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.txtLogisticDw.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblInfoLogisticL2.setToolTip(_translate("MainWindow", "Length of center white region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblInfoLogisticDg.setToolTip(_translate("MainWindow", "Diffusion coefficient for both Zone 1 and Zone 3\n"
"- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.txtLogisticL2.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitLogisticL3.setText(_translate("MainWindow", "mm"))
        self.txtLogisticDg.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.lblInfoLogisticL1.setToolTip(_translate("MainWindow", "Length of left grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitLogisticL2.setText(_translate("MainWindow", "mm"))
        self.lblInfoLogisticL3.setToolTip(_translate("MainWindow", "Length of right grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitLogisticDg.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.lblInputLogisticL1.setText(_translate("MainWindow", "Zone 1 Length (L1)"))
        self.lblInputLogisticDg.setText(_translate("MainWindow", "Diffusion Coefficient of Grey Matter (Dg)"))
        self.txtLogisticL1.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblLogisticBrain.setText(_translate("MainWindow", "BRAIN TISSUE ANATOMY"))
        self.lblLogisticTumor.setText(_translate("MainWindow", "TUMOR PROFILE"))
        self.txtLogisticC0.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be smaller than maximum concentration of tumor (Cmax)"))
        self.lblUnitLogisticC0.setText(_translate("MainWindow", "cells/mm"))
        self.lblUnitLogisticX0.setText(_translate("MainWindow", "mm"))
        self.lblInfoLogisticC0.setToolTip(_translate("MainWindow", "Initial concentration of tumor\n"
"- Must not be zero\n"
"- Must be smaller than maximum concentration of tumor (Cmax)"))
        self.lblInputLogisticCmax.setText(_translate("MainWindow", "Max Concentration (Cmax)"))
        self.lblUnitLogisticRho.setText(_translate("MainWindow", "/day"))
        self.txtLogisticRho.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblInputLogisticRho.setText(_translate("MainWindow", "Proliferation Rate (ρ)"))
        self.lblInfoLogisticRho.setToolTip(_translate("MainWindow", "Proliferation rate of tumor\n"
"- Must not be zero"))
        self.txtLogisticCmax.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblUnitLogisticCmax.setText(_translate("MainWindow", "cells/mm"))
        self.lblInputLogisticC0.setText(_translate("MainWindow", "Initial Concentration (C0)"))
        self.lblInfoLogisticCmax.setToolTip(_translate("MainWindow", "Act as a carrying capacity of the tumor\n"
"- Must not be zero"))
        self.txtLogisticX0.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.lblInfoLogisticX0.setToolTip(_translate("MainWindow", "Initial location of tumor along X axis\n"
"- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.lblInputLogisticX0.setText(_translate("MainWindow", "Initial Location (X0)"))
        self.lblUnitLogisticTime.setText(_translate("MainWindow", "days      "))
        self.lblInputLogisticTime.setText(_translate("MainWindow", "Time                                    "))
        self.txtLogisticTime.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be an integer"))
        self.lblInfoLogisticTime.setToolTip(_translate("MainWindow", "Time to observe the tumor growth\n"
"- Must not be zero\n"
"- Has to be an integer"))
        self.btnLogisticReset.setToolTip(_translate("MainWindow", "Reset all field to default value"))
        self.btnLogisticReset.setText(_translate("MainWindow", "Reset"))
        self.btnLogisticSimulate.setToolTip(_translate("MainWindow", "Simulate using current data"))
        self.btnLogisticSimulate.setText(_translate("MainWindow", "Simulate"))
        self.groupBoxLogistic.setTitle(_translate("MainWindow", "USE EXISTING DATA"))
        self.btnLogisticSampleData.setToolTip(_translate("MainWindow", "Use sample data"))
        self.btnLogisticSampleData.setText(_translate("MainWindow", "Sample Data"))
        self.btnLogisticImport.setToolTip(_translate("MainWindow", "Import data from Excel File"))
        self.btnLogisticImport.setText(_translate("MainWindow", "Import"))

        for i in range(len(self.lblInfoLogistic)):
            self.lblInfoLogistic[i].setPixmap(self.icon['q'])
 
    def runSimulationLogistic(self):
        self.retranslateUi_Logistic(self)
        inputFlag = True

        dx = decimal.Decimal('0.5')
        
        L1 = round(self.txtLogisticL1.value(), 3)
        L2 = round(self.txtLogisticL2.value(), 3)
        L3 = round(self.txtLogisticL3.value(), 3)
        Dg = round(self.txtLogisticDg.value(), 3)
        Dw = round(self.txtLogisticDw.value(), 3)
        x0 = round(self.txtLogisticX0.value(), 3)
        C0 = round(self.txtLogisticC0.value(), 3)
        rho = round(self.txtLogisticRho.value(), 3)
        Cmax = round(self.txtLogisticCmax.value(), 3)
        tf = round(self.txtLogisticTime.value(), 3) 

        if decimal.Decimal(L1) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoLogisticL1)

        if decimal.Decimal(L2) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoLogisticL2)

        if decimal.Decimal(L3) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoLogisticL3)

        if Dg == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticDg)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be smaller than white matter diffusion coefficient (Dw)", self.lblInfoLogisticDg)

        if Dw == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticDw)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be greater than grey matter diffusion coefficient (Dg)", self.lblInfoLogisticDw)

        if x0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticX0)
        elif decimal.Decimal(x0) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoLogisticX0)
        elif not(x0 < (L1+L2+L3)):
            inputFlag = self.setErrorMessage("Input must be between 0 and L, where L is the total length of Zone 1, 2, 3", self.lblInfoLogisticX0)

        if C0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticC0)
        elif not(C0 < Cmax):
            inputFlag = self.setErrorMessage("Input must be smaller than maximum concentration of tumor (Cmax)", self.lblInfoLogisticC0)

        if rho == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticRho)

        if Cmax == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticCmax)

        if tf == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoLogisticTime)
        elif tf % 1 != 0:
            inputFlag = self.setErrorMessage("Input has to be an integer", self.lblInfoLogisticTime)

        if inputFlag == False:
            dialog = CustomDialog("Input Error",
                                  "Invalid input.",
                                  "Please recheck your input and try again.",
                                  "Error",
                                  QtWidgets.QDialogButtonBox.Ok)
            dialog.exec_()
        else:
            self.showLoading()
            
            dataInput = np.array([
                ["Zone 1 Length", "L1", L1, "mm"],
                ["Zone 2 Length", "L2", L2, "mm"],
                ["Zone 3 Length", "L3", L3, "mm"],
                ["Diffusion Coef. Grey Region", "Dg", Dg, "mm-sq/day"],
                ["Diffusion Coef. White Region", "Dw", Dw, "mm-sq/day"],
                ["Tumor Initial Position", "x0", x0, "mm"],
                ["Tumor Proliferation Rate", "rho", rho, "/day"],
                ["Tumor Initial Concentration", "C0", C0, "cells/mm"],
                ["Tumor Max. Concentration", "Cmax", Cmax, "cells/mm"],
                ["Observation Time", "tf", tf, "days"]])

            self.tumor = NonLinear(
                growthType = "Logistic",
                L1 = L1,
                L2 = L2,
                L3 = L3,
                Dg = Dg,
                Dw = Dw,
                x0 = x0,
                C0 = C0,
                rho = rho,
                Cmax = Cmax,
                tf = tf)

            self.lblResultTitle.setText(QtCore.QCoreApplication.translate("MainWindow", "RESULT FOR LOGISTIC GROWTH"))
            self.setTableInput(dataInput)
            self.outputTypeChanged("Table")
            self.setTableOutput(self.frameOutputConcentrationTable, "outputConcentration")
            self.initiateSpinBoxPlot2D()
            self.showResult()

    def resetInputLogistic(self, flagReset=True, popUpResetDialog=True):
        if popUpResetDialog:
            dialog = CustomDialog("Reset",
                      "Are you sure you want to reset?",
                      "All input data will be set to default.",
                      "Warning",
                      QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            flagReset = dialog.exec_()
            
        if flagReset:
            self.retranslateUi_Logistic(self)

            for i in range(len(self.txtLogistic)):
                self.txtLogistic[i].setValue(0)

    # --------------------------------- GOMPERTZIAN ---------------------------------
    def setupUi_Gompertzian(self, MainWindow):
        self.frameGompertzian = QtWidgets.QFrame(self.centralwidget)
        self.frameGompertzian.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameGompertzian.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameGompertzian.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameGompertzian.setObjectName("frameGompertzian")
        self.lblGompertzianTitle = QtWidgets.QLabel(self.frameGompertzian)
        self.lblGompertzianTitle.setGeometry(QtCore.QRect(10, 10, 443, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblGompertzianTitle.setFont(font)
        self.lblGompertzianTitle.setObjectName("lblGompertzianTitle")
        self.imgIllustrationGompertzian = QtWidgets.QLabel(self.frameGompertzian)
        self.imgIllustrationGompertzian.setGeometry(QtCore.QRect(30, 80, 361, 211))
        self.imgIllustrationGompertzian.setFrameShape(QtWidgets.QFrame.Panel)
        self.imgIllustrationGompertzian.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imgIllustrationGompertzian.setText("")
        self.imgIllustrationGompertzian.setPixmap(QtGui.QPixmap("asset/illustration/parameter.png"))
        self.imgIllustrationGompertzian.setScaledContents(True)
        self.imgIllustrationGompertzian.setObjectName("imgIllustrationGompertzian")
        self.lblGompertzianObservationTime = QtWidgets.QLabel(self.frameGompertzian)
        self.lblGompertzianObservationTime.setGeometry(QtCore.QRect(420, 310, 177, 29))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblGompertzianObservationTime.setFont(font)
        self.lblGompertzianObservationTime.setObjectName("lblGompertzianObservationTime")
        self.layoutWidget = QtWidgets.QWidget(self.frameGompertzian)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 350, 321, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayoutGompertzianBrain = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayoutGompertzianBrain.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayoutGompertzianBrain.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutGompertzianBrain.setObjectName("gridLayoutGompertzianBrain")
        self.lblInputGompertzianL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianL2.setFont(font)
        self.lblInputGompertzianL2.setObjectName("lblInputGompertzianL2")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInputGompertzianL2, 1, 0, 1, 1)
        self.lblInputGompertzianL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianL3.setFont(font)
        self.lblInputGompertzianL3.setObjectName("lblInputGompertzianL3")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInputGompertzianL3, 2, 0, 1, 1)
        self.lblInfoGompertzianDw = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoGompertzianDw.setText("")
        self.lblInfoGompertzianDw.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianDw.setObjectName("lblInfoGompertzianDw")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInfoGompertzianDw, 4, 3, 1, 1)
        self.lblUnitGompertzianL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianL1.setFont(font)
        self.lblUnitGompertzianL1.setObjectName("lblUnitGompertzianL1")
        self.gridLayoutGompertzianBrain.addWidget(self.lblUnitGompertzianL1, 0, 2, 1, 1)
        self.lblInputGompertzianDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianDw.setFont(font)
        self.lblInputGompertzianDw.setWordWrap(True)
        self.lblInputGompertzianDw.setObjectName("lblInputGompertzianDw")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInputGompertzianDw, 4, 0, 1, 1)
        self.txtGompertzianL3 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtGompertzianL3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianL3.setDecimals(3)
        self.txtGompertzianL3.setMaximum(100.0)
        self.txtGompertzianL3.setSingleStep(0.5)
        self.txtGompertzianL3.setObjectName("txtGompertzianL3")
        self.gridLayoutGompertzianBrain.addWidget(self.txtGompertzianL3, 2, 1, 1, 1)
        self.lblUnitGompertzianDw = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianDw.setFont(font)
        self.lblUnitGompertzianDw.setObjectName("lblUnitGompertzianDw")
        self.gridLayoutGompertzianBrain.addWidget(self.lblUnitGompertzianDw, 4, 2, 1, 1)
        self.txtGompertzianDw = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtGompertzianDw.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianDw.setDecimals(3)
        self.txtGompertzianDw.setMaximum(10.0)
        self.txtGompertzianDw.setSingleStep(0.01)
        self.txtGompertzianDw.setObjectName("txtGompertzianDw")
        self.gridLayoutGompertzianBrain.addWidget(self.txtGompertzianDw, 4, 1, 1, 1)
        self.lblInfoGompertzianL2 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoGompertzianL2.setText("")
        self.lblInfoGompertzianL2.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianL2.setObjectName("lblInfoGompertzianL2")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInfoGompertzianL2, 1, 3, 1, 1)
        self.lblInfoGompertzianDg = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoGompertzianDg.setText("")
        self.lblInfoGompertzianDg.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianDg.setObjectName("lblInfoGompertzianDg")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInfoGompertzianDg, 3, 3, 1, 1)
        self.txtGompertzianL2 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtGompertzianL2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianL2.setDecimals(3)
        self.txtGompertzianL2.setMaximum(100.0)
        self.txtGompertzianL2.setSingleStep(0.5)
        self.txtGompertzianL2.setObjectName("txtGompertzianL2")
        self.gridLayoutGompertzianBrain.addWidget(self.txtGompertzianL2, 1, 1, 1, 1)
        self.lblUnitGompertzianL3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianL3.setFont(font)
        self.lblUnitGompertzianL3.setObjectName("lblUnitGompertzianL3")
        self.gridLayoutGompertzianBrain.addWidget(self.lblUnitGompertzianL3, 2, 2, 1, 1)
        self.txtGompertzianDg = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtGompertzianDg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianDg.setDecimals(3)
        self.txtGompertzianDg.setMaximum(10.0)
        self.txtGompertzianDg.setSingleStep(0.01)
        self.txtGompertzianDg.setObjectName("txtGompertzianDg")
        self.gridLayoutGompertzianBrain.addWidget(self.txtGompertzianDg, 3, 1, 1, 1)
        self.lblInfoGompertzianL1 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoGompertzianL1.setText("")
        self.lblInfoGompertzianL1.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianL1.setObjectName("lblInfoGompertzianL1")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInfoGompertzianL1, 0, 3, 1, 1)
        self.lblUnitGompertzianL2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianL2.setFont(font)
        self.lblUnitGompertzianL2.setObjectName("lblUnitGompertzianL2")
        self.gridLayoutGompertzianBrain.addWidget(self.lblUnitGompertzianL2, 1, 2, 1, 1)
        self.lblInfoGompertzianL3 = QtWidgets.QLabel(self.layoutWidget)
        self.lblInfoGompertzianL3.setText("")
        self.lblInfoGompertzianL3.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianL3.setObjectName("lblInfoGompertzianL3")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInfoGompertzianL3, 2, 3, 1, 1)
        self.lblUnitGompertzianDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianDg.setFont(font)
        self.lblUnitGompertzianDg.setObjectName("lblUnitGompertzianDg")
        self.gridLayoutGompertzianBrain.addWidget(self.lblUnitGompertzianDg, 3, 2, 1, 1)
        self.lblInputGompertzianL1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianL1.setFont(font)
        self.lblInputGompertzianL1.setObjectName("lblInputGompertzianL1")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInputGompertzianL1, 0, 0, 1, 1)
        self.lblInputGompertzianDg = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianDg.setFont(font)
        self.lblInputGompertzianDg.setWordWrap(True)
        self.lblInputGompertzianDg.setObjectName("lblInputGompertzianDg")
        self.gridLayoutGompertzianBrain.addWidget(self.lblInputGompertzianDg, 3, 0, 1, 1)
        self.txtGompertzianL1 = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.txtGompertzianL1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianL1.setPrefix("")
        self.txtGompertzianL1.setDecimals(3)
        self.txtGompertzianL1.setMaximum(100.0)
        self.txtGompertzianL1.setSingleStep(0.5)
        self.txtGompertzianL1.setObjectName("txtGompertzianL1")
        self.gridLayoutGompertzianBrain.addWidget(self.txtGompertzianL1, 0, 1, 1, 1)
        self.gridLayoutGompertzianBrain.setColumnStretch(1, 1)
        self.lblGompertzianBrain = QtWidgets.QLabel(self.frameGompertzian)
        self.lblGompertzianBrain.setGeometry(QtCore.QRect(40, 310, 319, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblGompertzianBrain.setFont(font)
        self.lblGompertzianBrain.setObjectName("lblGompertzianBrain")
        self.lblGompertzianTumor = QtWidgets.QLabel(self.frameGompertzian)
        self.lblGompertzianTumor.setGeometry(QtCore.QRect(420, 80, 349, 37))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lblGompertzianTumor.setFont(font)
        self.lblGompertzianTumor.setObjectName("lblGompertzianTumor")
        self.layoutWidget1 = QtWidgets.QWidget(self.frameGompertzian)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 120, 351, 176))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayoutGompertzianTumor = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayoutGompertzianTumor.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutGompertzianTumor.setObjectName("gridLayoutGompertzianTumor")
        self.txtGompertzianC0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtGompertzianC0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianC0.setDecimals(3)
        self.txtGompertzianC0.setMaximum(1000.0)
        self.txtGompertzianC0.setSingleStep(0.1)
        self.txtGompertzianC0.setObjectName("txtGompertzianC0")
        self.gridLayoutGompertzianTumor.addWidget(self.txtGompertzianC0, 2, 1, 1, 1)
        self.lblUnitGompertzianX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianX0.setFont(font)
        self.lblUnitGompertzianX0.setObjectName("lblUnitGompertzianX0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertzianX0, 0, 2, 1, 1)
        self.lblUnitGompertzianRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianRho.setFont(font)
        self.lblUnitGompertzianRho.setObjectName("lblUnitGompertzianRho")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertzianRho, 1, 2, 1, 1)
        self.lblUnitGompertzianC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianC0.setFont(font)
        self.lblUnitGompertzianC0.setObjectName("lblUnitGompertzianC0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertzianC0, 2, 2, 1, 1)
        self.lblInfoGompertzianC0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoGompertzianC0.setText("")
        self.lblInfoGompertzianC0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianC0.setObjectName("lblInfoGompertzianC0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInfoGompertzianC0, 2, 3, 1, 1)
        self.txtGompertziank = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtGompertziank.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertziank.setDecimals(3)
        self.txtGompertziank.setMaximum(1000.0)
        self.txtGompertziank.setSingleStep(0.1)
        self.txtGompertziank.setObjectName("txtGompertziank")
        self.gridLayoutGompertzianTumor.addWidget(self.txtGompertziank, 3, 1, 1, 1)
        self.txtGompertzianRho = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtGompertzianRho.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianRho.setDecimals(3)
        self.txtGompertzianRho.setMaximum(10.0)
        self.txtGompertzianRho.setSingleStep(0.001)
        self.txtGompertzianRho.setObjectName("txtGompertzianRho")
        self.gridLayoutGompertzianTumor.addWidget(self.txtGompertzianRho, 1, 1, 1, 1)
        self.lblInputGompertzianRho = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianRho.setFont(font)
        self.lblInputGompertzianRho.setObjectName("lblInputGompertzianRho")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInputGompertzianRho, 1, 0, 1, 1)
        self.lblInputGompertziank = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertziank.setFont(font)
        self.lblInputGompertziank.setObjectName("lblInputGompertziank")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInputGompertziank, 3, 0, 1, 1)
        self.lblInfoGompertzianRho = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoGompertzianRho.setText("")
        self.lblInfoGompertzianRho.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianRho.setObjectName("lblInfoGompertzianRho")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInfoGompertzianRho, 1, 3, 1, 1)
        self.lblInfoGompertziank = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoGompertziank.setText("")
        self.lblInfoGompertziank.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertziank.setObjectName("lblInfoGompertziank")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInfoGompertziank, 3, 3, 1, 1)
        self.lblInputGompertzianC0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianC0.setFont(font)
        self.lblInputGompertzianC0.setObjectName("lblInputGompertzianC0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInputGompertzianC0, 2, 0, 1, 1)
        self.lblUnitGompertziank = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertziank.setFont(font)
        self.lblUnitGompertziank.setObjectName("lblUnitGompertziank")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertziank, 3, 2, 1, 1)
        self.lblInfoGompertzianX0 = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoGompertzianX0.setText("")
        self.lblInfoGompertzianX0.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianX0.setObjectName("lblInfoGompertzianX0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInfoGompertzianX0, 0, 3, 1, 1)
        self.lblInputGompertzianX0 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianX0.setFont(font)
        self.lblInputGompertzianX0.setObjectName("lblInputGompertzianX0")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInputGompertzianX0, 0, 0, 1, 1)
        self.txtGompertziand = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtGompertziand.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertziand.setDecimals(3)
        self.txtGompertziand.setMaximum(1000.0)
        self.txtGompertziand.setSingleStep(0.1)
        self.txtGompertziand.setObjectName("txtGompertziand")
        self.gridLayoutGompertzianTumor.addWidget(self.txtGompertziand, 4, 1, 1, 1)
        self.lblInputGompertziand = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertziand.setFont(font)
        self.lblInputGompertziand.setObjectName("lblInputGompertziand")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInputGompertziand, 4, 0, 1, 1)
        self.txtGompertzianX0 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.txtGompertzianX0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianX0.setDecimals(3)
        self.txtGompertzianX0.setMaximum(300.0)
        self.txtGompertzianX0.setSingleStep(0.5)
        self.txtGompertzianX0.setObjectName("txtGompertzianX0")
        self.gridLayoutGompertzianTumor.addWidget(self.txtGompertzianX0, 0, 1, 1, 1)
        self.lblUnitGompertziand = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertziand.setFont(font)
        self.lblUnitGompertziand.setObjectName("lblUnitGompertziand")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertziand, 4, 2, 1, 1)
        self.lblInfoGompertziand = QtWidgets.QLabel(self.layoutWidget1)
        self.lblInfoGompertziand.setText("")
        self.lblInfoGompertziand.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertziand.setObjectName("lblInfoGompertziand")
        self.gridLayoutGompertzianTumor.addWidget(self.lblInfoGompertziand, 4, 3, 1, 1)
        self.lblGompertzianCC = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblGompertzianCC.setFont(font)
        self.lblGompertzianCC.setObjectName("lblGompertzianCC")
        self.gridLayoutGompertzianTumor.addWidget(self.lblGompertzianCC, 5, 0, 1, 1)
        self.lblGompertzianCCValue = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblGompertzianCCValue.setFont(font)
        self.lblGompertzianCCValue.setObjectName("lblGompertzianCCValue")
        self.gridLayoutGompertzianTumor.addWidget(self.lblGompertzianCCValue, 5, 1, 1, 1, QtCore.Qt.AlignRight)
        self.lblUnitGompertzianCC = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianCC.setFont(font)
        self.lblUnitGompertzianCC.setObjectName("lblUnitGompertzianCC")
        self.gridLayoutGompertzianTumor.addWidget(self.lblUnitGompertzianCC, 5, 2, 1, 2)
        self.gridLayoutGompertzianTumor.setColumnStretch(1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.frameGompertzian)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(420, 350, 351, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutGompertzianTime = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutGompertzianTime.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutGompertzianTime.setObjectName("gridLayoutGompertzianTime")
        self.lblUnitGompertzianTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblUnitGompertzianTime.setFont(font)
        self.lblUnitGompertzianTime.setObjectName("lblUnitGompertzianTime")
        self.gridLayoutGompertzianTime.addWidget(self.lblUnitGompertzianTime, 0, 2, 1, 1)
        self.lblInputGompertzianTime = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(13)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.lblInputGompertzianTime.setFont(font)
        self.lblInputGompertzianTime.setObjectName("lblInputGompertzianTime")
        self.gridLayoutGompertzianTime.addWidget(self.lblInputGompertzianTime, 0, 0, 1, 1)
        self.txtGompertzianTime = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.txtGompertzianTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtGompertzianTime.setDecimals(3)
        self.txtGompertzianTime.setMaximum(1500.0)
        self.txtGompertzianTime.setSingleStep(1.0)
        self.txtGompertzianTime.setObjectName("txtGompertzianTime")
        self.gridLayoutGompertzianTime.addWidget(self.txtGompertzianTime, 0, 1, 1, 1)
        self.lblInfoGompertzianTime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lblInfoGompertzianTime.setText("")
        self.lblInfoGompertzianTime.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoGompertzianTime.setObjectName("lblInfoGompertzianTime")
        self.gridLayoutGompertzianTime.addWidget(self.lblInfoGompertzianTime, 0, 3, 1, 1)
        self.gridLayoutGompertzianTime.setColumnStretch(1, 1)
        self.btnGompertzianReset = QtWidgets.QPushButton(self.frameGompertzian)
        self.btnGompertzianReset.setGeometry(QtCore.QRect(490, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnGompertzianReset.setFont(font)
        self.btnGompertzianReset.setObjectName("btnGompertzianReset")
        self.btnGompertzianSimulate = QtWidgets.QPushButton(self.frameGompertzian)
        self.btnGompertzianSimulate.setEnabled(True)
        self.btnGompertzianSimulate.setGeometry(QtCore.QRect(600, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnGompertzianSimulate.setFont(font)
        self.btnGompertzianSimulate.setObjectName("btnGompertzianSimulate")
        self.groupBoxGompertzian = QtWidgets.QGroupBox(self.frameGompertzian)
        self.groupBoxGompertzian.setGeometry(QtCore.QRect(420, 410, 351, 80))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxGompertzian.setFont(font)
        self.groupBoxGompertzian.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxGompertzian.setObjectName("groupBoxGompertzian")
        self.btnGompertzianSampleData = QtWidgets.QPushButton(self.groupBoxGompertzian)
        self.btnGompertzianSampleData.setGeometry(QtCore.QRect(70, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnGompertzianSampleData.setFont(font)
        self.btnGompertzianSampleData.setObjectName("btnGompertzianSampleData")
        self.btnGompertzianImport = QtWidgets.QPushButton(self.groupBoxGompertzian)
        self.btnGompertzianImport.setGeometry(QtCore.QRect(180, 30, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnGompertzianImport.setFont(font)
        self.btnGompertzianImport.setObjectName("btnGompertzianImport")

        MainWindow.setTabOrder(self.txtGompertzianL1, self.txtGompertzianL2)
        MainWindow.setTabOrder(self.txtGompertzianL2, self.txtGompertzianL3)
        MainWindow.setTabOrder(self.txtGompertzianL3, self.txtGompertzianDg)
        MainWindow.setTabOrder(self.txtGompertzianDg, self.txtGompertzianDw)
        MainWindow.setTabOrder(self.txtGompertzianDw, self.txtGompertzianX0)
        MainWindow.setTabOrder(self.txtGompertzianX0, self.txtGompertzianRho)
        MainWindow.setTabOrder(self.txtGompertzianRho, self.txtGompertzianC0)
        MainWindow.setTabOrder(self.txtGompertzianC0, self.txtGompertziank)
        MainWindow.setTabOrder(self.txtGompertziank, self.txtGompertziand)
        MainWindow.setTabOrder(self.txtGompertziand, self.txtGompertzianTime)
        MainWindow.setTabOrder(self.txtGompertzianTime, self.btnGompertzianSimulate)
        MainWindow.setTabOrder(self.btnGompertzianSimulate, self.btnGompertzianReset)
        MainWindow.setTabOrder(self.btnGompertzianReset, self.btnGompertzianSampleData)
        MainWindow.setTabOrder(self.btnGompertzianSampleData, self.btnGompertzianImport)

        self.txtGompertzian = [self.txtGompertzianL1, self.txtGompertzianL2, self.txtGompertzianL3, self.txtGompertzianDg, self.txtGompertzianDw, self.txtGompertzianX0, self.txtGompertzianRho, self.txtGompertzianC0, self.txtGompertziank, self.txtGompertziand, self.txtGompertzianTime]
        self.varGompertzian = ['L1', 'L2', 'L3', 'Dg', 'Dw', 'x0', 'rho', 'C0', 'k', 'd', 'tf']
        self.lblInfoGompertzian = [self.lblInfoGompertzianL1, self.lblInfoGompertzianL2, self.lblInfoGompertzianL3, self.lblInfoGompertzianDg, self.lblInfoGompertzianDw, self.lblInfoGompertzianX0, self.lblInfoGompertzianRho, self.lblInfoGompertzianC0, self.lblInfoGompertziank, self.lblInfoGompertziand, self.lblInfoGompertzianTime]

        self.btnGompertzianSimulate.clicked.connect(lambda: self.runSimulation("Gompertzian"))
        self.btnGompertzianSimulate.setAutoDefault(True)
        self.btnGompertzianReset.clicked.connect(lambda: self.resetInputGompertzian(popUpResetDialog = True))
        self.btnGompertzianReset.setAutoDefault(True)
        self.btnGompertzianSampleData.clicked.connect(lambda: self.useSampleData(self.txtGompertzian, self.varGompertzian, "Gompertzian"))
        self.btnGompertzianSampleData.setAutoDefault(True)
        self.btnGompertzianImport.clicked.connect(lambda: self.importData("Gompertzian"))
        self.btnGompertzianImport.setAutoDefault(True)

        self.txtGompertziank.valueChanged.connect(self.updateCarryingCapacityValue)
        self.txtGompertziand.valueChanged.connect(self.updateCarryingCapacityValue)

        self.txtGompertzianL1.setMinimum(1)
        self.txtGompertzianL2.setMinimum(1)
        self.txtGompertzianL3.setMinimum(1)

    def retranslateUi_Gompertzian(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblGompertzianTitle.setText(_translate("MainWindow", "GOMPERTZIAN GROWTH"))
        self.imgIllustrationGompertzian.setToolTip(_translate("MainWindow", "Parameter Illustration"))
        self.lblGompertzianObservationTime.setText(_translate("MainWindow", "OBSERVATION TIME"))
        self.lblInputGompertzianL2.setText(_translate("MainWindow", "Zone 2 Length (L2)"))
        self.lblInputGompertzianL3.setText(_translate("MainWindow", "Zone 3 Length (L3)"))
        self.lblInfoGompertzianDw.setToolTip(_translate("MainWindow", "Diffusion coefficient for Zone 2\n"
"- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblUnitGompertzianL1.setText(_translate("MainWindow", "mm"))
        self.lblInputGompertzianDw.setText(_translate("MainWindow", "Diffusion Coefficient of White Matter (Dw)"))
        self.txtGompertzianL3.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitGompertzianDw.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.txtGompertzianDw.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be greater than grey matter diffusion coefficient (Dg)"))
        self.lblInfoGompertzianL2.setToolTip(_translate("MainWindow", "Length of center white region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblInfoGompertzianDg.setToolTip(_translate("MainWindow", "Diffusion coefficient for both Zone 1 and Zone 3\n"
"- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.txtGompertzianL2.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblUnitGompertzianL3.setText(_translate("MainWindow", "mm"))
        self.txtGompertzianDg.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Must be smaller than white matter diffusion coefficient (Dw)"))
        self.lblInfoGompertzianL1.setToolTip(_translate("MainWindow", "Length of left grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitGompertzianL2.setText(_translate("MainWindow", "mm"))
        self.lblInfoGompertzianL3.setToolTip(_translate("MainWindow", "Length of right grey region in millimeter\n"
"- Has to be a multiple of 0.5"))
        self.lblUnitGompertzianDg.setText(_translate("MainWindow", "<html><head/><body><p>mm<span style=\" vertical-align:super;\">2</span>/day</p></body></html>"))
        self.lblInputGompertzianL1.setText(_translate("MainWindow", "Zone 1 Length (L1)"))
        self.lblInputGompertzianDg.setText(_translate("MainWindow", "Diffusion Coefficient of Grey Matter (Dg)"))
        self.txtGompertzianL1.setToolTip(_translate("MainWindow", "- Has to be a multiple of 0.5"))
        self.lblGompertzianBrain.setText(_translate("MainWindow", "BRAIN TISSUE ANATOMY"))
        self.lblGompertzianTumor.setText(_translate("MainWindow", "TUMOR PROFILE"))
        self.txtGompertzianC0.setToolTip(_translate("MainWindow", "- Must not be zero\n- Must be smaller than carring capacity exp(k/d)"))
        self.lblUnitGompertzianX0.setText(_translate("MainWindow", "mm"))
        self.lblUnitGompertzianRho.setText(_translate("MainWindow", "/day"))
        self.lblUnitGompertzianC0.setText(_translate("MainWindow", "cells/mm"))
        self.lblInfoGompertzianC0.setToolTip(_translate("MainWindow", "Initial concentration of tumor\n- Must not be zero\n- Must be smaller than carring capacity exp(k/d)"))
        self.txtGompertziank.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.txtGompertzianRho.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblInputGompertzianRho.setText(_translate("MainWindow", "Proliferation Rate (ρ)"))
        self.lblInputGompertziank.setText(_translate("MainWindow", "Growth Rate (k)"))
        self.lblInfoGompertzianRho.setToolTip(_translate("MainWindow", "Proliferation rate of tumor\n"
"- Must not be zero"))
        self.lblInfoGompertziank.setToolTip(_translate("MainWindow", "One of carrying capacity factor of the tumor, which is exp(k/d)\n"
"- Must not be zero"))
        self.lblInputGompertzianC0.setText(_translate("MainWindow", "Initial Concentration (C0)"))
        self.lblUnitGompertziank.setText(_translate("MainWindow", "-"))
        self.lblInfoGompertzianX0.setToolTip(_translate("MainWindow", "Initial location of tumor along X axis\n"
"- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.lblInputGompertzianX0.setText(_translate("MainWindow", "Initial Location (X0)"))
        self.txtGompertziand.setToolTip(_translate("MainWindow", "- Must not be zero"))
        self.lblInputGompertziand.setText(_translate("MainWindow", "Density Coefficient (d)"))
        self.txtGompertzianX0.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be a multiple of 0.5\n"
"- Must be between 0 and L, where L is the total length of Zone 1, 2, 3"))
        self.lblUnitGompertziand.setText(_translate("MainWindow", "-"))
        self.lblInfoGompertziand.setToolTip(_translate("MainWindow", "One of carrying capacity factor of the tumor, which is exp(k/d)\n"
"- Must not be zero"))
        self.lblGompertzianCC.setText(_translate("MainWindow", "Carrying Capacity exp(k/d)"))
        self.lblGompertzianCCValue.setText(_translate("MainWindow", "undefined"))
        self.lblUnitGompertzianCC.setText(_translate("MainWindow", "cells/mm"))
        self.lblUnitGompertzianTime.setText(_translate("MainWindow", "days      "))
        self.lblInputGompertzianTime.setText(_translate("MainWindow", "Time                                    "))
        self.txtGompertzianTime.setToolTip(_translate("MainWindow", "- Must not be zero\n"
"- Has to be an integer"))
        self.lblInfoGompertzianTime.setToolTip(_translate("MainWindow", "Time to observe the tumor growth\n"
"- Must not be zero\n"
"- Has to be an integer"))
        self.btnGompertzianReset.setToolTip(_translate("MainWindow", "Reset all field to default value"))
        self.btnGompertzianReset.setText(_translate("MainWindow", "Reset"))
        self.btnGompertzianSimulate.setToolTip(_translate("MainWindow", "Simulate using current data"))
        self.btnGompertzianSimulate.setText(_translate("MainWindow", "Simulate"))
        self.groupBoxGompertzian.setTitle(_translate("MainWindow", "USE EXISTING DATA"))
        self.btnGompertzianSampleData.setToolTip(_translate("MainWindow", "Use sample data"))
        self.btnGompertzianSampleData.setText(_translate("MainWindow", "Sample Data"))
        self.btnGompertzianImport.setToolTip(_translate("MainWindow", "Import data from Excel File"))
        self.btnGompertzianImport.setText(_translate("MainWindow", "Import"))

        for i in range(len(self.lblInfoGompertzian)):
            self.lblInfoGompertzian[i].setPixmap(self.icon['q'])

        self.updateCarryingCapacityValue()

    def updateCarryingCapacityValue(self):
        k = round(self.txtGompertziank.value(), 3)
        d = round(self.txtGompertziand.value(), 3)

        try:
            # round down to 3 decimal places, eg: 4.56789 -> 4.567
            cc = str(math.floor(math.exp(k/d)*1000)/1000)
        except:
            cc = "undefined"

        self.lblGompertzianCCValue.setText(cc)

    def runSimulationGompertzian(self):
        self.retranslateUi_Gompertzian(self)
        inputFlag = True

        dx = decimal.Decimal('0.5')
        
        L1 = round(self.txtGompertzianL1.value(), 3)
        L2 = round(self.txtGompertzianL2.value(), 3)
        L3 = round(self.txtGompertzianL3.value(), 3)
        Dg = round(self.txtGompertzianDg.value(), 3)
        Dw = round(self.txtGompertzianDw.value(), 3)
        x0 = round(self.txtGompertzianX0.value(), 3)
        C0 = round(self.txtGompertzianC0.value(), 3)
        rho = round(self.txtGompertzianRho.value(), 3)
        k = round(self.txtGompertziank.value(), 3)
        d = round(self.txtGompertziand.value(), 3)
        tf = round(self.txtGompertzianTime.value(), 3)

        if decimal.Decimal(L1) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoGompertzianL1)

        if decimal.Decimal(L2) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoGompertzianL2)

        if decimal.Decimal(L3) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoGompertzianL3)

        if Dg == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianDg)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be smaller than white matter diffusion coefficient (Dw)", self.lblInfoGompertzianDg)

        if Dw == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianDw)
        elif not(Dg < Dw):
            inputFlag = self.setErrorMessage("Input must be greater than grey matter diffusion coefficient (Dg)", self.lblInfoGompertzianDw)

        if x0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianX0)
        elif decimal.Decimal(x0) % dx != 0:
            inputFlag = self.setErrorMessage("Input has to be a multiple of " + str(dx), self.lblInfoGompertzianX0)
        elif not(x0 < (L1+L2+L3)):
            inputFlag = self.setErrorMessage("Input must be between 0 and L, where L is the total length of Zone 1, 2, 3", self.lblInfoGompertzianX0)

        if rho == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianRho)

        try:
            carryingCap = float(self.lblGompertzianCCValue.text())
        except:
            carryingCap = -math.inf
            
        if C0 == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianC0)
        elif C0 > carryingCap:
            inputFlag = self.setErrorMessage("Input must be smaller than the carrying capacity, which is {}".format(self.lblGompertzianCCValue.text()), self.lblInfoGompertzianC0) 

        if k == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertziank)

        if d == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertziand)
        
        if tf == 0:
            inputFlag = self.setErrorMessage("Input must not be zero", self.lblInfoGompertzianTime)
        elif tf % 1 != 0:
            inputFlag = self.setErrorMessage("Input has to be an integer", self.lblInfoGompertzianTime)

        if inputFlag == False:
            dialog = CustomDialog("Input Error",
                                  "Invalid input.",
                                  "Please recheck your input and try again.",
                                  "Error",
                                  QtWidgets.QDialogButtonBox.Ok)
            dialog.exec_()
        else:
            self.showLoading()
            
            dataInput = np.array([
                ["Zone 1 Length", "L1", L1, "mm"],
                ["Zone 2 Length", "L2", L2, "mm"],
                ["Zone 3 Length", "L3", L3, "mm"],
                ["Diffusion Coef. Grey Region", "Dg", Dg, "mm-sq/day"],
                ["Diffusion Coef. White Region", "Dw", Dw, "mm-sq/day"],
                ["Tumor Initial Position", "x0", x0, "mm"],
                ["Tumor Proliferation Rate", "rho", rho, "/day"],
                ["Tumor Initial Concentration", "C0", C0, "cells/mm"],
                ["Growth Rate", "k", k, "-"],
                ["Density Coefficient", "d", d, "-"],
                ["Observation Time", "tf", tf, "days"]])

            self.tumor = NonLinear(
                growthType = "Gompertzian",
                L1 = L1,
                L2 = L2,
                L3 = L3,
                Dg = Dg,
                Dw = Dw,
                x0 = x0,
                C0 = C0,
                rho = rho,
                k = k,
                d = d,
                tf = tf)

            self.lblResultTitle.setText(QtCore.QCoreApplication.translate("MainWindow", "RESULT FOR GOMPERTZIAN GROWTH"))
            self.setTableInput(dataInput)
            self.outputTypeChanged("Table")
            self.setTableOutput(self.frameOutputConcentrationTable, "outputConcentration")
            self.initiateSpinBoxPlot2D()
            self.showResult()

    def resetInputGompertzian(self, flagReset=True, popUpResetDialog=True):
        if popUpResetDialog:
            dialog = CustomDialog("Reset",
                      "Are you sure you want to reset?",
                      "All input data will be set to default.",
                      "Warning",
                      QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            flagReset = dialog.exec_()
            
        if flagReset:
            self.retranslateUi_Gompertzian(self)
            for i in range(len(self.txtGompertzian)):
                self.txtGompertzian[i].setValue(0)

    # --------------------------------- LOADING ---------------------------------
    def setupUi_Loading(self, MainWindow):
        self.frameLoading = QtWidgets.QFrame(self.centralwidget)
        self.frameLoading.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameLoading.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLoading.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLoading.setObjectName("frameLoading")
        self.lblLoadingTitle = QtWidgets.QLabel(self.frameLoading)
        self.lblLoadingTitle.setGeometry(QtCore.QRect(0, 120, 801, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.lblLoadingTitle.setFont(font)
        self.lblLoadingTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLoadingTitle.setObjectName("lblLoadingTitle")
        self.progressBar = QtWidgets.QProgressBar(self.frameLoading)
        self.progressBar.setGeometry(QtCore.QRect(210, 220, 381, 41))
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.lblProgressPercentage = QtWidgets.QLabel(self.frameLoading)
        self.lblProgressPercentage.setGeometry(QtCore.QRect(0, 270, 801, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblProgressPercentage.setFont(font)
        self.lblProgressPercentage.setAlignment(QtCore.Qt.AlignCenter)
        self.lblProgressPercentage.setObjectName("lblProgressPercentage")
        self.lblLoadingWarning = QtWidgets.QLabel(self.frameLoading)
        self.lblLoadingWarning.setGeometry(QtCore.QRect(240, 400, 311, 130))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lblLoadingWarning.setFont(font)
        self.lblLoadingWarning.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLoadingWarning.setWordWrap(True)
        self.lblLoadingWarning.setObjectName("lblLoadingWarning")

        self.progressBar.setStyleSheet(PROGRESSBAR_STYLE)
        
    def retranslateUi_Loading(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lblLoadingTitle.setText(_translate("MainWindow", "LOADING"))
        self.lblProgressPercentage.setText(_translate("MainWindow", "0.0%"))
        self.lblLoadingWarning.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sitka\'; font-size:15pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0004;\">Warning:</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0004;\">Don\'t interact with the screen while loading, the application might not be responding</span></p></body></html>"))

    # --------------------------------- RESULT ---------------------------------
    def setupUi_Result(self, MainWindow):
        self.frameResult = QtWidgets.QFrame(self.centralwidget)
        self.frameResult.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frameResult.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameResult.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameResult.setObjectName("frameResult")
        self.lblResultTitle = QtWidgets.QLabel(self.frameResult)
        self.lblResultTitle.setGeometry(QtCore.QRect(10, 10, 750, 48))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.lblResultTitle.setFont(font)
        self.lblResultTitle.setObjectName("lblResultTitle")
        self.lblDataInput = QtWidgets.QLabel(self.frameResult)
        self.lblDataInput.setGeometry(QtCore.QRect(450, 80, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lblDataInput.setFont(font)
        self.lblDataInput.setObjectName("lblDataInput")
        self.lblOutputType = QtWidgets.QLabel(self.frameResult)
        self.lblOutputType.setGeometry(QtCore.QRect(450, 330, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lblOutputType.setFont(font)
        self.lblOutputType.setObjectName("lblOutputType")
        self.cbOutputType = QtWidgets.QComboBox(self.frameResult)
        self.cbOutputType.setGeometry(QtCore.QRect(450, 360, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        self.cbOutputType.setFont(font)
        self.cbOutputType.setObjectName("cbOutputType")
        self.cbOutputType.addItem("")
        self.cbOutputType.addItem("")
        self.cbOutputType.addItem("")
        self.cbOutputType.addItem("")
        self.btnSaveInput = QtWidgets.QPushButton(self.frameResult)
        self.btnSaveInput.setGeometry(QtCore.QRect(710, 290, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnSaveInput.setFont(font)
        self.btnSaveInput.setObjectName("btnSaveInput")
        self.cbTumorAtt = QtWidgets.QComboBox(self.frameResult)
        self.cbTumorAtt.setGeometry(QtCore.QRect(450, 440, 181, 29))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(12)
        self.cbTumorAtt.setFont(font)
        self.cbTumorAtt.setObjectName("cbTumorAtt")
        self.lblTumorAtt = QtWidgets.QLabel(self.frameResult)
        self.lblTumorAtt.setGeometry(QtCore.QRect(450, 410, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lblTumorAtt.setFont(font)
        self.lblTumorAtt.setObjectName("lblTumorAtt")
        self.btnResimulate = QtWidgets.QPushButton(self.frameResult)
        self.btnResimulate.setGeometry(QtCore.QRect(590, 500, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnResimulate.setFont(font)
        self.btnResimulate.setObjectName("btnResimulate")

        # ------------------------------- FRAME TABLE CONCENTRATION
        self.frameOutputConcentrationTable = QtWidgets.QFrame(self.frameResult)
        self.frameOutputConcentrationTable.setGeometry(QtCore.QRect(10, 80, 420, 450))
        self.frameOutputConcentrationTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputConcentrationTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputConcentrationTable.setObjectName("frameOutputConcentrationTable")

        self.btnSaveTableConcentration = QtWidgets.QPushButton(self.frameOutputConcentrationTable)
        self.btnSaveTableConcentration.setGeometry(QtCore.QRect(310, 260, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnSaveTableConcentration.setFont(font)
        self.btnSaveTableConcentration.setObjectName("btnSaveTableConcentration")

        self.lblTableConcentrationExplanation = QtWidgets.QLabel(self.frameOutputConcentrationTable)
        self.lblTableConcentrationExplanation.setGeometry(QtCore.QRect(10, 310, 391, 161))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblTableConcentrationExplanation.setFont(font)
        self.lblTableConcentrationExplanation.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblTableConcentrationExplanation.setWordWrap(True)
        self.lblTableConcentrationExplanation.setObjectName("lblTableConcentrationExplanation")

        # ------------------------------- FRAME TABLE CONCENTRATION
        self.frameOutputSummaryTable = QtWidgets.QFrame(self.frameResult)
        self.frameOutputSummaryTable.setGeometry(QtCore.QRect(10, 80, 420, 450))
        self.frameOutputSummaryTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputSummaryTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputSummaryTable.setObjectName("frameOutputSummaryTable")

        self.btnSaveTableSummary = QtWidgets.QPushButton(self.frameOutputSummaryTable)
        self.btnSaveTableSummary.setGeometry(QtCore.QRect(310, 260, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnSaveTableSummary.setFont(font)
        self.btnSaveTableSummary.setObjectName("btnSaveTableSummary")

        self.lblTableSummaryExplanation = QtWidgets.QLabel(self.frameOutputSummaryTable)
        self.lblTableSummaryExplanation.setGeometry(QtCore.QRect(10, 310, 391, 161))
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblTableSummaryExplanation.setFont(font)
        self.lblTableSummaryExplanation.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lblTableSummaryExplanation.setWordWrap(True)
        self.lblTableSummaryExplanation.setObjectName("lblTableSummaryExplanation")


        # ------------------------------- FRAME GRAPH 2D
        self.frameOutputGraph2D = QtWidgets.QFrame(self.frameResult)
        self.frameOutputGraph2D.setGeometry(QtCore.QRect(10, 55, 420, 500))
        self.frameOutputGraph2D.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputGraph2D.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputGraph2D.setObjectName("frameOutputGraph2D")

        self.verticalLayout2D = QtWidgets.QVBoxLayout(self.frameOutputGraph2D)
        self.verticalLayout2D.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2D.setObjectName("verticalLayout2D")

        self.gridLayoutWidget2D = QtWidgets.QWidget()
        self.gridLayoutWidget2D.setGeometry(QtCore.QRect(10, 340, 401, 160))
        self.gridLayoutWidget2D.setObjectName("gridLayoutWidget")
        self.gridLayoutOutput2D = QtWidgets.QGridLayout(self.gridLayoutWidget2D)
        self.gridLayoutOutput2D.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutOutput2D.setObjectName("gridLayoutOutput2D")
        #check boxes
        self.cbAnnotation2D = QtWidgets.QCheckBox(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.cbAnnotation2D.setFont(font)
        self.cbAnnotation2D.setObjectName("cbAnnotation2D")
        self.gridLayoutOutput2D.addWidget(self.cbAnnotation2D, 0, 0, 1, 1)
        self.cbLegend2D = QtWidgets.QCheckBox(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.cbLegend2D.setFont(font)
        self.cbLegend2D.setObjectName("cbLegend2D")
        self.gridLayoutOutput2D.addWidget(self.cbLegend2D, 0, 1, 1, 1)

        #by step
        self.horizontalLayoutPlot2DByStep = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPlot2DByStep.setObjectName("horizontalLayoutPlot2DByStep")
        self.lblPlot2DByStep = QtWidgets.QLabel(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblPlot2DByStep.setFont(font)
        self.lblPlot2DByStep.setObjectName("lblPlot2DByStep")
        self.horizontalLayoutPlot2DByStep.addWidget(self.lblPlot2DByStep)
        self.spinBoxPlot2DByStep = QtWidgets.QSpinBox(self.gridLayoutWidget2D)
        self.spinBoxPlot2DByStep.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxPlot2DByStep.setObjectName("spinBoxPlot2DByStep")
        self.horizontalLayoutPlot2DByStep.addWidget(self.spinBoxPlot2DByStep)
        self.btnPlot2DByStep = QtWidgets.QPushButton(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnPlot2DByStep.setFont(font)
        self.btnPlot2DByStep.setObjectName("btnPlot2DByStep")
        self.horizontalLayoutPlot2DByStep.addWidget(self.btnPlot2DByStep)
        self.gridLayoutOutput2D.addLayout(self.horizontalLayoutPlot2DByStep, 1, 0, 1, 2)
        
        # by day
        self.horizontalLayoutPlot2DByDay = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPlot2DByDay.setObjectName("horizontalLayoutPlot2DByDay")
        self.lblPlot2DByDay = QtWidgets.QLabel(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblPlot2DByDay.setFont(font)
        self.lblPlot2DByDay.setObjectName("lblPlot2DByDay")
        self.horizontalLayoutPlot2DByDay.addWidget(self.lblPlot2DByDay)
        self.spinBoxPlot2DByDay = QtWidgets.QSpinBox(self.gridLayoutWidget2D)
        self.spinBoxPlot2DByDay.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxPlot2DByDay.setObjectName("spinBoxPlot2DByDay")
        self.horizontalLayoutPlot2DByDay.addWidget(self.spinBoxPlot2DByDay)
        self.btnPlot2DByDay = QtWidgets.QPushButton(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnPlot2DByDay.setFont(font)
        self.btnPlot2DByDay.setObjectName("btnPlot2DByDay")
        self.horizontalLayoutPlot2DByDay.addWidget(self.btnPlot2DByDay)
        self.gridLayoutOutput2D.addLayout(self.horizontalLayoutPlot2DByDay, 2, 0, 1, 2)
        
        # clear all plot
        self.btnClearPlot2D = QtWidgets.QPushButton(self.gridLayoutWidget2D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnClearPlot2D.setFont(font)
        self.btnClearPlot2D.setObjectName("btnClearPlot2D")
        self.gridLayoutOutput2D.addWidget(self.btnClearPlot2D, 3, 0, 1, 2)
        
        self.spinBoxPlot2DByStep.setMinimum(1)
        self.spinBoxPlot2DByStep.setValue(10)

        self.graph2d = Graph2D()
        self.verticalLayout2D.addWidget(self.graph2d.toolbar)
        self.verticalLayout2D.addWidget(self.graph2d.canvas)
        self.verticalLayout2D.addWidget(self.gridLayoutWidget2D)
        
        # -------------------------------- FRAME GRAPH 3D
        self.frameOutputGraph3D = QtWidgets.QFrame(self.frameResult)
        self.frameOutputGraph3D.setGeometry(QtCore.QRect(10, 55, 420, 480))
        self.frameOutputGraph3D.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputGraph3D.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputGraph3D.setObjectName("frameOutputGraph3D")

        self.verticalLayout3D = QtWidgets.QVBoxLayout(self.frameOutputGraph3D)
        self.verticalLayout3D.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout3D.setObjectName("verticalLayout2D")

        self.gridLayoutWidget3D = QtWidgets.QWidget()
        self.gridLayoutWidget3D.setGeometry(QtCore.QRect(10, 340, 401, 160))
        self.gridLayoutWidget3D.setObjectName("gridLayoutWidget")
        self.gridLayoutOutput3D = QtWidgets.QGridLayout(self.gridLayoutWidget3D)
        self.gridLayoutOutput3D.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutOutput3D.setObjectName("gridLayoutOutput3D")
        self.cbAnnotation3D = QtWidgets.QCheckBox(self.gridLayoutWidget3D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.cbAnnotation3D.setFont(font)
        self.cbAnnotation3D.setObjectName("cbAnnotation3D")
        self.gridLayoutOutput3D.addWidget(self.cbAnnotation3D, 0, 0, 1, 1)
        self.cbColorBar3D = QtWidgets.QCheckBox(self.gridLayoutWidget3D)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.cbColorBar3D.setFont(font)
        self.cbColorBar3D.setObjectName("cbLegend2D")
        self.gridLayoutOutput3D.addWidget(self.cbColorBar3D, 0, 1, 1, 1)

        self.graph3d = Graph3D()
        self.verticalLayout3D.addWidget(self.graph3d.toolbar)
        self.verticalLayout3D.addWidget(self.graph3d.canvas)
        self.verticalLayout3D.addWidget(self.gridLayoutWidget3D)

        
        # -------------------------------- FRAME ANIMATION 2D
        self.frameOutputAnimation2D = QtWidgets.QFrame(self.frameResult)
        self.frameOutputAnimation2D.setGeometry(QtCore.QRect(10, 55, 420, 500))
        self.frameOutputAnimation2D.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOutputAnimation2D.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOutputAnimation2D.setObjectName("frameOutputAnimation2D")

        self.verticalLayoutAnimation2D = QtWidgets.QVBoxLayout(self.frameOutputAnimation2D)
        self.verticalLayoutAnimation2D.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutAnimation2D.setObjectName("verticalLayoutAnimation2D")

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frameResult)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(300, 60, 331, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutDuration = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayoutDuration.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutDuration.setObjectName("horizontalLayoutDuration")
        self.lblAnimationDuration = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lblAnimationDuration.setFont(font)
        self.lblAnimationDuration.setObjectName("lblAnimationDuration")
        self.horizontalLayoutDuration.addWidget(self.lblAnimationDuration)
        self.spinBoxAnimationDuration = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBoxAnimationDuration.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxAnimationDuration.setMinimum(3000)
        self.spinBoxAnimationDuration.setMaximum(15000)
        self.spinBoxAnimationDuration.setSingleStep(500)
        self.spinBoxAnimationDuration.setObjectName("spinBoxAnimationDuration")
        self.horizontalLayoutDuration.addWidget(self.spinBoxAnimationDuration)
        self.lblInfoAnimationDuration = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.lblInfoAnimationDuration.setText("")
        self.lblInfoAnimationDuration.setPixmap(QtGui.QPixmap("asset/questionmark.png"))
        self.lblInfoAnimationDuration.setObjectName("lblInfoAnimationDuration")
        self.horizontalLayoutDuration.addWidget(self.lblInfoAnimationDuration)
        self.horizontalLayoutDuration.setStretch(1, 1)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frameResult)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(300, 20, 326, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutAnimation = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutAnimation.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutAnimation.setObjectName("horizontalLayoutAnimation")
        self.btnStartAnimation = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnStartAnimation.setFont(font)
        self.btnStartAnimation.setObjectName("btnStartAnimation")
        self.horizontalLayoutAnimation.addWidget(self.btnStartAnimation)
        self.btnStopAnimation = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnStopAnimation.setFont(font)
        self.btnStopAnimation.setObjectName("btnStopAnimation")
        self.horizontalLayoutAnimation.addWidget(self.btnStopAnimation)
        self.btnSaveAnimation = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnSaveAnimation.setFont(font)
        self.btnSaveAnimation.setObjectName("btnSaveAnimation")
        self.horizontalLayoutAnimation.addWidget(self.btnSaveAnimation)

        self.animation2d = Graph2D()
        self.verticalLayoutAnimation2D.addWidget(self.animation2d.toolbar)
        self.verticalLayoutAnimation2D.addWidget(self.animation2d.canvas)
        self.verticalLayoutAnimation2D.addWidget(self.horizontalLayoutWidget_2)
        self.verticalLayoutAnimation2D.addWidget(self.horizontalLayoutWidget)
        
        # EVENT LEFT LAYOUT
        self.cbTumorAttItems = {'Table': ["Concentration", "Summary"],
                               '2D Graph': ["Concentration", "Max. Concentration", "Number of Cells", "Mean Radial Distance", "Average Growth Speed"],
                               '3D Graph': ["Concentration"],
                                '2D Animation': ["Concentration"]}

        # -- EVENT FRAME TABLE
        self.btnSaveTableConcentration.clicked.connect(self.exportOutput)
        self.btnSaveTableSummary.clicked.connect(self.exportOutput)

        # -- EVENT FRAME GRAPH 2D
        self.cbAnnotation2D.stateChanged.connect(self.cbAnnotation2DChanged)
        self.cbLegend2D.stateChanged.connect(self.cbLegend2DChanged)
        self.btnPlot2DByStep.clicked.connect(lambda: self.plot2DByStep(plotFlag = False, popUpFlag = True, timeStep = int(self.spinBoxPlot2DByStep.value())))
        self.btnPlot2DByDay.clicked.connect(lambda: self.plot2DByDay(int(self.spinBoxPlot2DByDay.value())))
        self.btnClearPlot2D.clicked.connect(self.clearAllPlot2D)

        # -- EVENT FRAME GRAPH 3D
        self.cbAnnotation3D.stateChanged.connect(self.cbAnnotation3DChanged)
        self.cbColorBar3D.stateChanged.connect(self.cbColorBar3DChanged)

        # -- EVENT FRAME ANIMATION 2D
        self.btnStartAnimation.clicked.connect(self.startAnimation2D)
        self.btnStopAnimation.clicked.connect(self.stopAnimation2D)
        self.btnSaveAnimation.clicked.connect(self.saveAnimation2D)

        # EVENT RIGHT LAYOUT
        self.cbOutputType.activated[str].connect(self.outputTypeChanged)
        self.cbTumorAtt.activated[str].connect(self.tumorAttChanged)
        self.btnSaveInput.clicked.connect(lambda: self.exportTable(self.tableInput))
        self.btnResimulate.clicked.connect(self.resimulatePage)
        self.btnResimulate.setAutoDefault(True)
        
    def retranslateUi_Result(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        #self.lblResultTitle.setText(_translate("MainWindow", "RESULT"))
        self.lblDataInput.setText(_translate("MainWindow", "DATA INPUT"))
        self.lblOutputType.setText(_translate("MainWindow", "OUTPUT TYPE"))
        self.cbOutputType.setItemText(0, _translate("MainWindow", "Table"))
        self.cbOutputType.setItemText(1, _translate("MainWindow", "2D Graph"))
        self.cbOutputType.setItemText(2, _translate("MainWindow", "3D Graph"))
        self.cbOutputType.setItemText(3, _translate("MainWindow", "2D Animation"))
        self.btnSaveInput.setToolTip(_translate("MainWindow", "Save the data input table above as Excel file"))
        self.btnSaveInput.setText(_translate("MainWindow", "Save Table"))
        self.lblTumorAtt.setText(_translate("MainWindow", "TUMOR ATTRIBUTE"))
        self.btnResimulate.setToolTip(_translate("MainWindow", "Back to simulation page"))
        self.btnResimulate.setText(_translate("MainWindow", "Resimulate"))

        self.cbOutputType.setCurrentIndex(0)
        self.cbTumorAtt.setCurrentIndex(0)

        #----- FRAME TABLE CONCENTRATION
        self.btnSaveTableConcentration.setToolTip(_translate("MainWindow", "Save the concentration table above as Excel file"))
        self.btnSaveTableConcentration.setText(_translate("MainWindow", "Save Table"))
        self.lblTableConcentrationExplanation.setText(_translate("MainWindow", "The table above displays the value of glioma concentration in cells/mm, arranged in rows and columns. The rows represent the time from range zero to observation time with time step = 1 day. The columns represent the spatial axis from range zero to the total length of brain tissue (L) with space step = 0.5 mm."))

        #----- FRAME TABLE SUMMARY
        self.btnSaveTableSummary.setToolTip(_translate("MainWindow", "Save the summary table above as Excel file"))
        self.btnSaveTableSummary.setText(_translate("MainWindow", "Save Table"))
        self.lblTableSummaryExplanation.setText(_translate("MainWindow", "The table above displays the summary of glioma evolution. The rows represent the time from range zero to observation time with time step = 1 day. The columns represent insights of glioma evolution which covers: maximum concentration (cells/mm), number of cells (cells), mean radial distance (mm), and average growth speed (mm/day) for each zone and overall zone."))
                                                           
        #----- FRAME 2D
        self.lblPlot2DByDay.setText(_translate("MainWindow", "Plot at Day:"))
        self.spinBoxPlot2DByDay.setToolTip(_translate("MainWindow", "Plot at specific time (day)"))
        self.btnPlot2DByDay.setToolTip(_translate("MainWindow", "Plot at specific time"))
        self.btnPlot2DByDay.setText(_translate("MainWindow", "Plot by Day"))
        self.cbAnnotation2D.setToolTip(_translate("MainWindow", "Provides data label when hovering over the line"))
        self.cbAnnotation2D.setText(_translate("MainWindow", "Enable Annotation"))
        self.cbLegend2D.setToolTip(_translate("MainWindow", "Provides data legend inside the graph"))
        self.cbLegend2D.setText(_translate("MainWindow", "Display Legend"))
        self.btnClearPlot2D.setToolTip(_translate("MainWindow", "Clear all existing plot in the graph"))
        self.btnClearPlot2D.setText(_translate("MainWindow", "Clear All Plot"))
        self.lblPlot2DByStep.setText(_translate("MainWindow", "Plot All with Step:"))
        self.spinBoxPlot2DByStep.setToolTip(_translate("MainWindow", "Plot for all time with desired step (day)"))
        self.btnPlot2DByStep.setToolTip(_translate("MainWindow", "Plot for all time with desired step"))
        self.btnPlot2DByStep.setText(_translate("MainWindow", "Plot by Step"))

        self.cbAnnotation2D.setChecked(True)
        self.cbLegend2D.setChecked(True)

        #----- FRAME 3D
        self.cbAnnotation3D.setToolTip(_translate("MainWindow", "Provides data label when hovering over the surface"))
        self.cbAnnotation3D.setText(_translate("MainWindow", "Enable Annotation"))
        self.cbColorBar3D.setToolTip(_translate("MainWindow", "Provides color bar inside the graph"))
        self.cbColorBar3D.setText(_translate("MainWindow", "Display Color Bar"))

        #----- FRAME 2D ANIMATION
        self.btnStartAnimation.setToolTip(_translate("MainWindow", "Start animation from the beginning"))
        self.btnStartAnimation.setText(_translate("MainWindow", "Start"))
        self.btnStopAnimation.setToolTip(_translate("MainWindow", "Stop animation at current frame"))
        self.btnStopAnimation.setText(_translate("MainWindow", "Stop"))
        self.btnSaveAnimation.setToolTip(_translate("MainWindow", "Save animation as mp4"))
        self.btnSaveAnimation.setText(_translate("MainWindow", "Save Animation"))
        self.lblAnimationDuration.setText(_translate("MainWindow", "Animation Duration (millisecs):"))
        self.spinBoxAnimationDuration.setToolTip(_translate("MainWindow", "Input animation duration in milliseconds"))
        self.lblInfoAnimationDuration.setToolTip(_translate("MainWindow", "Animation duration may not be applied for the plot above,\n"
"because of the application's writer limitation.\n"
"But always applied when you save the animation."))


    # EVENT HANDLER LEFT LAYOUT

    # --- TABLE RESULT
    def setTableInput(self, dataInput):
        self.tableInput = TableResult(frame = self.frameResult,
                                      data = dataInput,
                                      resultType = "input")
        self.tableInput.setGeometry(QtCore.QRect(450, 110, 340, 170))
        self.tableInput.setObjectName("tableInput")

    def setTableOutput(self, frame, resultType):
        self.tableOutput = TableResult(frame = frame,
                                       data = self.dataOutput,
                                       dx = self.tumor.dx,
                                       resultType = resultType)
        self.tableOutput.setGeometry(QtCore.QRect(10, 10, 401, 241))
        self.tableOutput.setObjectName("tableOutput")

    def exportOutput(self):
        self.exportTable(self.tableOutput)

    # --- GRAPH 2D
    def showPlot2DFeature(self, flagShow):
        if flagShow:
            self.lblPlot2DByStep.show()
            self.spinBoxPlot2DByStep.show()
            self.btnPlot2DByStep.show()
            self.lblPlot2DByDay.show()
            self.spinBoxPlot2DByDay.show()
            self.btnPlot2DByDay.show()
            self.btnClearPlot2D.show()
        else:
            self.lblPlot2DByStep.hide()
            self.spinBoxPlot2DByStep.hide()
            self.btnPlot2DByStep.hide()
            self.lblPlot2DByDay.hide()
            self.spinBoxPlot2DByDay.hide()
            self.btnPlot2DByDay.hide()
            self.btnClearPlot2D.hide()
            
    def initiateSpinBoxPlot2D(self):
        defaultPlot2DStep = math.ceil(self.tumor.tf/math.log(self.tumor.tf, 2)) if not(self.tumor.tf == 1) else 1
            
        self.spinBoxPlot2DByStep.setMaximum(math.floor(self.tumor.tf/2))
        self.spinBoxPlot2DByStep.setValue(defaultPlot2DStep)

        self.spinBoxPlot2DByDay.setMaximum(self.tumor.tf)
        self.spinBoxPlot2DByDay.setValue(0)
        
    def enableCheckboxPlot2D(self, flag):
        self.cbAnnotation2D.setEnabled(flag)
        self.cbLegend2D.setEnabled(flag)
        self.cbAnnotation2DChanged()
        self.cbLegend2DChanged()
        
    def cbAnnotation2DChanged(self):
        tumorAtt = self.cbTumorAtt.currentText()

        annotationText = "{}\n$x$: {:.3f} mm\n$C$: {:.3f} cells/mm"

        if tumorAtt == "Concentration":
            annotationText = "{}\n$x$: {:.3f} mm\n$C$: {:.3f} cells/mm"
        elif tumorAtt == "Max. Concentration":
            annotationText = "{}\n$t$: Day {:.3f}\n$MaxC$: {:.3f} cells/mm"
        elif tumorAtt == "Number of Cells":
            annotationText = "{}\n$t$: Day {:.3f}\n$N$: {:.3f} cells"
        elif tumorAtt == "Mean Radial Distance":
            annotationText = "{}\n$t$: Day {:.3f}\n$L$: {:.3f} mm"
        elif tumorAtt == "Average Growth Speed":
            annotationText = "{}\n$t$: Day {:.3f}\n$S$: {:.3f} mm/day"
        
        if self.cbAnnotation2D.isChecked():
            self.graph2d.enableAnnotation(True, annotationText)
        else:
            self.graph2d.enableAnnotation(False, annotationText)

    def cbLegend2DChanged(self):
        if self.cbLegend2D.isChecked():
            self.graph2d.enableLegend(True)
        else:
            self.graph2d.enableLegend(False)

    def clearAllPlot2D(self):
        dialog = CustomDialog("Clear All Plot",
                              "Do you want to clear all plot?",
                              "Unsaved graph will be lost.",
                              "Warning",
                              QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        if dialog.exec_():
            self.graph2d.clearAllPlot()
            
            self.cbAnnotation2D.setChecked(False)
            self.cbLegend2D.setChecked(False)
            self.enableCheckboxPlot2D(False)
            
            self.tf_plot = np.array([])

    def plot2DByStep(self, plotFlag = False, popUpFlag = False, timeStep = 10):
        if popUpFlag:
            dialog = CustomDialog("Plot by Step",
                                  "Plot all time with step {} day(s)?".format(timeStep),
                                  "Current graph will be overwritten.",
                                  "Question",
                                  QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            if dialog.exec_():
                plotFlag = True

        if plotFlag:
            self.xf_plot = np.linspace(0, self.tumor.xf, self.tumor.nx)
            self.tf_plot = np.array([n for n in range(0, int(self.tumor.tf)+1, timeStep)]).astype(int)
            if self.tumor.tf not in self.tf_plot:
                self.tf_plot = np.sort(np.append(self.tf_plot, self.tumor.tf))

            self.graph2d.plotConcentration(self.xf_plot, self.tf_plot, self.dataOutput)

            self.enableCheckboxPlot2D(True)

    def plot2DByDay(self, tf):
        if tf not in self.tf_plot:
            self.tf_plot = np.sort(np.append(self.tf_plot, tf))
            self.graph2d.plotConcentration(self.xf_plot, self.tf_plot, self.dataOutput)

            self.enableCheckboxPlot2D(True)
        else:
            dialog = CustomDialog("Error Plot",
                                  "Day {} has been plotted.".format(tf),
                                  "Please try another value.",
                                  "Error",
                                  QtWidgets.QDialogButtonBox.Ok)
            dialog.exec_()

    # --- GRAPH 3D
    def cbAnnotation3DChanged(self):
        if self.cbAnnotation3D.isChecked():
            self.graph3d.enableAnnotation(True)
        else:
            self.graph3d.enableAnnotation(False)

    def cbColorBar3DChanged(self):
        if self.cbColorBar3D.isChecked():
            self.graph3d.enableColorBar(True)
        else:
            self.graph3d.enableColorBar(False)

    # --- ANIMATION 2D
    def startAnimation2D(self):
        xf_plot = np.linspace(0, self.tumor.xf, self.tumor.nx)
        duration = self.spinBoxAnimationDuration.value()
        self.animation2d.plotConcentrationAnimation(xf_plot, self.dataOutput, duration)

    def stopAnimation2D(self):
        if hasattr(self.animation2d, 'anim'):
            if not self.animation2d.anim == None:
                self.animation2d.anim.event_source.stop()

    def saveAnimation2D(self):
        if hasattr(self.animation2d, 'anim'):
            if not self.animation2d.anim == None:
                file = QtWidgets.QFileDialog.getSaveFileName(None,
                                                             "Save Animation",
                                                             self.tumor.growthType + "Animation",
                                                             "MP4 File (*.mp4)")

                if file[0]:
                    self.animation2d.anim.save(file[0], writer="ffmpeg")
                    
                    dialog = CustomDialog("Save Animation Success",
                                          "Do you want to open your file?",
                                          "File will be opened immediately.",
                                          "Question",
                                          QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
                    if dialog.exec_():
                        os.startfile(file[0])
            else:
                dialog = CustomDialog("Save Animation Error",
                                      "Animation has not been played.",
                                      "Play the animation minimal once.",
                                      "Error",
                                      QtWidgets.QDialogButtonBox.Ok)
                dialog.exec_()
        else:
            dialog = CustomDialog("Save Animation Error",
                                      "Animation has not been played.",
                                      "Play the animation minimal once.",
                                      "Error",
                                      QtWidgets.QDialogButtonBox.Ok)
            dialog.exec_()

    # EVENT HANDLER RIGHT LAYOUT

    # Combobox Event
    def outputTypeChanged(self, outputType):
        # Change tumor att combobox based on selected output type
        self.cbTumorAtt.clear()
        self.cbTumorAtt.addItems(self.cbTumorAttItems[outputType])
        self.tumorAttChanged(self.cbTumorAttItems[outputType][0])

        # CHANGE OUTPUT FRAME
        self.hideAllOutputFrame()
        if outputType == "Table":
            self.frameOutputConcentrationTable.show()
        elif outputType == "2D Graph":
            self.frameOutputGraph2D.show()
        elif outputType == "3D Graph":
            self.frameOutputGraph3D.show()
        elif outputType == "2D Animation":
            self.frameOutputAnimation2D.show()

    def tumorAttChanged(self, tumorAtt):
        # CHANGE DATA
        sliceIdx = [n for n in range(0, self.tumor.nt, int(1/self.tumor.dt))]
        if tumorAtt == "Concentration":
            self.dataOutput = self.tumor.C[sliceIdx]
        elif tumorAtt == "Max. Concentration":
            self.dataOutput = self.tumor.max_C
        elif tumorAtt == "Number of Cells":
            self.dataOutput = self.tumor.number_cell
        elif tumorAtt == "Mean Radial Distance":
            self.dataOutput = self.tumor.radial_dist
        elif tumorAtt == "Average Growth Speed":
            self.dataOutput = self.tumor.growth_speed
        elif tumorAtt == "Summary":
            self.dataOutput = np.concatenate((self.tumor.max_C[:, sliceIdx],
                                                self.tumor.number_cell[:, sliceIdx],
                                                self.tumor.radial_dist[:, sliceIdx],
                                                self.tumor.growth_speed[:, sliceIdx])).T
        else:
            self.dataOutput = np.array([])

            
        # SHOW OUTPUT BASED ON CHOICE
        outputType = self.cbOutputType.currentText()
        if outputType == "Table":
            if tumorAtt == "Concentration":
                self.setTableOutput(self.frameOutputConcentrationTable, "outputConcentration")
                self.frameOutputConcentrationTable.show()
                self.frameOutputSummaryTable.hide()

            elif tumorAtt == "Summary":
                self.setTableOutput(self.frameOutputSummaryTable, "outputSummary")
                self.frameOutputConcentrationTable.hide()
                self.frameOutputSummaryTable.show()
                
        elif outputType == "2D Graph":
            if tumorAtt == "Max. Concentration":
                ylab = "Max. Concentration (cells/mm)"
                title = "Max. Concentration Over Time Per Zone"
            elif tumorAtt == "Number of Cells":
                ylab = "Number of Cells (cells)"
                title = "Number of Cells Over Time Per Zone"
            elif tumorAtt == "Mean Radial Distance":
                ylab = "Mean Radial Distance (mm)"
                title = "Mean Radial Distance Over Time Per Zone"
            elif tumorAtt == "Average Growth Speed":
                ylab = "Average Growth Speed (mm/day)"
                title = "Average Growth Speed Over Time Per Zone"
            
            if tumorAtt == "Concentration":
                timeStep = int(self.spinBoxPlot2DByStep.value())
                self.plot2DByStep(plotFlag = True, popUpFlag = False, timeStep = timeStep)
                self.showPlot2DFeature(True)
                self.cbAnnotation2D.setChecked(False)
                self.enableCheckboxPlot2D(True)
            else:
                tf_plot = np.linspace(0, self.tumor.tf, self.tumor.nt)
                xlab = "Time (days)"
    
                self.graph2d.plotTumorAttribute(self.dataOutput, tf_plot, xlab, ylab, title)
                self.showPlot2DFeature(False)
                self.enableCheckboxPlot2D(True)
        elif outputType == "3D Graph":
            self.cbColorBar3D.setChecked(False)
            self.graph3d.plotConcentration(self.dataOutput, self.tumor.xf, self.tumor.tf)
            self.cbColorBar3D.setChecked(True)
        elif outputType == "2D Animation":
            self.animation2d.initializeAnimationPlot()

    def exportTable(self, table):
        resultType = "input" if table.resultType == "input" else "output"
        file = QtWidgets.QFileDialog.getSaveFileName(None,
                                                     "Save "+resultType.capitalize(),
                                                     table.resultType + self.tumor.growthType,
                                                     "Excel Workbook (*.xlsx);;Excel 97-2003 Workbook (*.xls)")
        if file[0]:
            if resultType == "output":
                df = pd.DataFrame(table.data, index=table.rowNames, columns=table.colNames)
                sheet_name = self.cbTumorAtt.currentText()
            elif resultType == "input":
                df = pd.DataFrame(table.data, columns=table.colNames)
                sheet_name = self.tumor.growthType

            if file[1] == "Excel Workbook (*.xlsx)":
                with pd.ExcelWriter(file[0]) as writer:
                    df.to_excel(writer, index=table.rowNames, sheet_name = sheet_name)
                    writer.save()
                    
            elif file[1] == "Excel 97-2003 Workbook (*.xls)":
                with pd.ExcelWriter(file[0]) as writer:
                    df.to_excel(writer, index=table.rowNames, sheet_name = sheet_name, engine = "xlwt")
                    writer.save()
                    
            elif file[1] == "CSV (*.csv)":
                #np.savetxt(file[0], table.data, delimiter=",", fmt='%s')
                df.to_csv(file[0], index=False)

            dialog = CustomDialog("Save "+resultType.capitalize()+" Success",
                                  "Do you want to open your file?",
                                  "File will be opened immediately.",
                                  "Question",
                                  QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
            if dialog.exec_():
                os.startfile(file[0])

    def resimulatePage(self):
        dialog = CustomDialog("Resimulate",
                              "Are you sure you want to go back?",
                              "Unsaved data will be lost.",
                              "Warning",
                              QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        if dialog.exec_():
            self.canLeavePage = True
            
            if self.tumor.growthType == "Exponential":
                self.showExpo(flagReset = False, popUpResetDialog = False)
            elif self.tumor.growthType == "Logistic":
                self.showLogistic(flagReset = False, popUpResetDialog = False)
            elif self.tumor.growthType == "Gompertzian":
                self.showGompertzian(flagReset = False, popUpResetDialog = False)

    def hideAllOutputFrame(self):
        self.frameOutputConcentrationTable.hide()
        self.frameOutputSummaryTable.hide()
        self.frameOutputGraph2D.hide()
        self.frameOutputGraph3D.hide()
        self.frameOutputAnimation2D.hide()

plt.rcParams['animation.ffmpeg_path'] = 'C:\\FFmpeg\\bin\\ffmpeg.exe'
writer = animation.FFMpegWriter(fps=30)

class TableResult(QtWidgets.QTableWidget):
    def __init__(self, **kwargs):
        # SET ATTRIBUTES
        allowed_param = ['frame', 'dx', 'data', 'resultType']
        self.__dict__.update((key, val) for key, val in kwargs.items() if key in allowed_param)

        super(TableResult, self).__init__(self.frame)

        self.rowCount = self.data.shape[0]
        self.colCount = self.data.shape[1]
        self.setRowCount(self.rowCount)
        self.setColumnCount(self.colCount)
        
        if self.resultType == "outputConcentration":
            self.setOutputConcentrationHeader()
        if self.resultType == "outputSummary":
            self.setOutputSummaryHeader()    
        elif self.resultType == "input":
            self.setInputHeader()
        self.fillTableWithData()
        
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.horizontalHeader().setStyleSheet(TABLEHEADER_STYLE)
        self.verticalHeader().setStyleSheet(TABLEHEADER_STYLE)

    def setOutputConcentrationHeader(self):
        self.rowNames = ["Day " + str(round(n,2)) for n in range(self.rowCount)]
        self.colNames = [str(round(j*self.dx,2)) + " mm" for j in range(self.colCount)]
        self.setVerticalHeaderLabels(self.rowNames)
        self.setHorizontalHeaderLabels(self.colNames)

    def setOutputSummaryHeader(self):
        self.rowNames = ["Day " + str(round(n,2)) for n in range(self.rowCount)]
        self.colNames = []
        for att in ["Max. Concentration", "Number of Cells", "Mean Radial Distance", "Average Growth Speed"]:
            for zone in ["Overall Zone", "Zone 1", "Zone 2", "Zone 3"]:
                self.colNames.append(att + "\nfor " + zone)
        self.setVerticalHeaderLabels(self.rowNames)
        self.setHorizontalHeaderLabels(self.colNames)

    def setInputHeader(self):
        self.rowNames = False
        self.colNames = ["Parameter", "Symbol", "Value", "Unit"]
        self.setHorizontalHeaderLabels(self.colNames)
        self.verticalHeader().hide()

    def fillTableWithData(self):
        for n in range(self.rowCount):
            for j in range(self.colCount):
                if self.resultType == "outputConcentration" or self.resultType == "outputSummary":
                    tableWidgetItem = QtWidgets.QTableWidgetItem("{:.6f}".format(self.data[n,j]))
                elif self.resultType == "input":
                    try:
                        tableWidgetItem = QtWidgets.QTableWidgetItem("{:.3f}".format(float(self.data[n,j])))
                    except:
                        tableWidgetItem = QtWidgets.QTableWidgetItem(str(self.data[n,j]))

                self.setItem(n, j, tableWidgetItem)

class Graph2D(QtWidgets.QDialog):
    def __init__(self):
        super(Graph2D, self).__init__(parent = None)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111, position = [0.15, 0.15, 0.8, 0.75])
        self.toolbar = NavigationToolbar(self.canvas, None)
        self.toolbar.setStyleSheet(NAVTOOLBAR_STYLE)

        # LEGEND FOR TUMOR ATTRIBUTE
        self.line_style = ['-', ':', '--', '-.']
        self.zone_label = ["Overall Zone", "Zone 1 (Grey)", "Zone 2 (White)", "Zone 3 (Grey)"]

    def plotConcentration(self, xf_plot, tf_plot, data):
        self.axes.cla()
        
        for n in tf_plot:
            self.axes.plot(xf_plot, data[int(n)], label = "Day {}".format(str(int(n))))
        
        self.axes.set_xlabel("$x$ (mm)")
        self.axes.set_ylabel("$C$ (cells/mm)")
        self.axes.set_title("Concentration")

        self.canvas.flush_events()
        self.canvas.draw()

    def plotTumorAttribute(self, data, tf_plot, xlab, ylab, title):
        self.axes.cla()

        for zone in range(4):
            self.axes.plot(tf_plot, data[zone],
                           linestyle = self.line_style[zone],
                           label = "{}".format(self.zone_label[zone]))

        self.axes.set_xlabel(xlab)
        self.axes.set_ylabel(ylab)
        self.axes.set_title(title)

        self.figure.tight_layout()

        self.canvas.flush_events()
        self.canvas.draw()

    def plotConcentrationAnimation(self, xf_plot, data, duration):
        self.axes.cla()

        plot_list = []
        for i in range(len(data)):
            line, = self.axes.plot(xf_plot, data[i], "b")
            title = self.axes.text(0.5, 1.05, "Day {}".format(i),
                                   size = plt.rcParams["axes.titlesize"],
                                   ha = "center",
                                   transform = self.axes.transAxes)
            plot_list.append([line, title])

        interval = math.floor((duration-1000)/(len(data)-1))
        
        self.anim = animation.ArtistAnimation(self.figure, plot_list, interval=interval, repeat=False, blit=False)

        self.axes.set_xlabel("$x$ (mm)")
        self.axes.set_ylabel("$C$ (cells/mm)")

        self.canvas.blit()
        self.canvas.draw()

    def enableAnnotation(self, flag, text):
        if flag:
            self.cursor = mplcursors.cursor(self.axes, hover = True, highlight = True)
            self.cursor.connect(
                "add", lambda sel: sel.annotation.set_text(
                    text.format(
                        sel.artist.get_label(), sel.target[0], sel.target[1]
                        )
                    )
                )
        else:
            self.cursor.remove()

    def enableLegend(self, flag):
        if flag:
            if len(self.figure.gca().lines) > 0:
                self.axes.legend()
        else:
            self.axes.legend().remove()
        self.canvas.draw()

    def clearAllPlot(self):
        for artist in self.figure.gca().lines + self.figure.gca().collections:
            artist.remove()
        self.canvas.draw()

    def initializeAnimationPlot(self):
        self.axes.cla()

        self.anim = None

        self.axes.set_xlabel("$x$ (mm)")
        self.axes.set_ylabel("$C$ (cells/mm)")

        self.canvas.draw()
        
class Graph3D(QtWidgets.QDialog):
    def __init__(self):
        super(Graph3D, self).__init__(parent = None)
        self.figure = Figure(tight_layout = True)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111, projection = '3d')
        self.toolbar = NavigationToolbar(self.canvas, None)
        self.toolbar.setStyleSheet(NAVTOOLBAR_STYLE)

    def plotConcentration(self, data, xf, tf):
        self.axes.cla()

        x_plot = np.linspace(0, xf, len(data[0]))
        t_plot = np.linspace(0, tf, len(data))

        x_plot, t_plot = np.meshgrid(x_plot, t_plot)
        
        self.surface = self.axes.plot_surface(
            x_plot, t_plot, data, cmap = "coolwarm"
            )
        
        self.axes.set_xlabel("$x$ (mm)")
        self.axes.set_ylabel("$t$ (days)")
        self.axes.set_zlabel("$C$ (cells/mm)")
        self.axes.set_title("Concentration")

        self.canvas.flush_events()
        self.canvas.draw()

    def enableAnnotation(self, flag):
        if flag:
            self.cursor = datacursor(self.surface, hover=True,
                       formatter="$x$ = {x:.3f}\n$t$ = {y:.3f}\n$C$ = {z:.3f}".format)
        else:
            self.cursor.hide()
            self.cursor.disable()

    def enableColorBar(self, flag):
        if flag:
            self.colorbar = self.figure.colorbar(self.surface,
                                                 ax = self.axes,
                                                 fraction = 0.035,
                                                 pad = 0.01)
        else:
            self.colorbar.remove()
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
