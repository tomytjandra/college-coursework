from math import *
import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    f = -y+x+2*x**2+2*x*y+y**2
    return f

def g(x,y):
    gX = 1+4*x+2*y
    gY = -1+2*x+2*y
    return gX, gY

#QUADRATIC INTERPOLATION (QI) (WITH ITERATION)
def qi(a,fx,x,y,i,sX,sY):
    alphaTemp = np.array([a[0],a[1],a[2]])
    fxTemp = np.array([fx[0],fx[1],fx[2]])

    while True:
        alphaNew = (fxTemp[0]*(alphaTemp[1]**2-alphaTemp[2]**2) + fxTemp[1]*(alphaTemp[2]**2-alphaTemp[0]**2) + fxTemp[2]*(alphaTemp[0]**2-alphaTemp[1]**2))/(2*fxTemp[0]*(alphaTemp[1]-alphaTemp[2]) + 2*fxTemp[1]*(alphaTemp[2]-alphaTemp[0]) + 2*fxTemp[2]*(alphaTemp[0]-alphaTemp[1]))
        xNew = x[i] + alphaNew*sX
        yNew = y[i] + alphaNew*sY
        fxNew = f(xNew,yNew)
        
        indexMax = 0
        for j in range(0,3):
            if(fxTemp[j] == max(fxTemp)):
                indexMax = j
                break
            
        alphaTemp[indexMax] = alphaNew
        fxTemp[indexMax] = fxNew

        sortFX = np.sort(fxTemp)

        diff = abs(sortFX[0]-sortFX[1])
        if(diff < 10E-6):
            break

    return alphaNew

#MAIN CODE STARTS HERE
print("Python code by Tomy 1801431662")
print("=======================================================")
print("STEEPEST DESCENT METHOD (USING QUADRATIC INTERPOLATION)")
print("=======================================================")
print("Minimum value of f(x,y) = -y+x+2x^2+2xy+y^2\nwith initial guess x0 = 0 and y0 = 0")

print("\n===============")
print("ITERATION TABLE")
print("===============")

#INITIALIZATION
x = np.array([])
y = np.array([])
fx = np.array([0.0,0.0,0.0]) #for QI
flagPrint = 1 #print table column name

#initial guess
x0 = 0.0
y0 = 0.0
alpha = np.array([0.0,0.2,0.4])

x = np.append(x,x0)
y = np.append(y,y0)

i = 0 #counter for looping

#STEEPEST DESCENT METHOD
while True:
    gX, gY = g(x[i],y[i])
    sX = -1*gX
    sY = -1*gY

    for j in range(0,3):
        fx[j] = f(x[i] + alpha[j]*sX, y[i] + alpha[j]*sY)
        
    alphaNew = qi(alpha,fx,x,y,i,sX,sY)
    xNew = x[i] + alphaNew*sX
    yNew = y[i] + alphaNew*sY

    #PRINT TABLE
    if flagPrint == 1:
        print("--------------------------------------------------------------------------------------------------------------")
        print(str("i").center(4), str("Xi").center(16), str("Yi").center(16), str("f(Xi,Yi)").center(16), str("gXi").center(18), str("gYi").center(18), str("alphaMin").center(18))
        print("--------------------------------------------------------------------------------------------------------------")
        flagPrint = 0
    print(str(i+1).center(4), str(x[i]).center(16), str(y[i]).center(16), str(f(x[i],y[i])).center(16), str(gX).center(18), str(gY).center(18), str(alphaNew).center(18))

    x = np.append(x,xNew)
    y = np.append(y,yNew)
    
    diff = abs(x[i]-x[i-1])
    if(diff < 10E-6):
        break
    
    i=i+1
    

#PRINT RESULTS
print("\n===============")
print("    RESULT")
print("===============")
print("Minimum")
print("x =",x[i],"\t≈ ",round(x[i],3))
print("y =",y[i],"\t≈ ",round(y[i],3))
print("value =",f(x[i],y[i]),"\t≈ ",round(f(x[i],y[i]),3))

#PLOTTING
xPlot = np.linspace(-2,2,100)
yPlot = np.linspace(-2,2,100)

X,Y = np.meshgrid(xPlot,yPlot)
Z = f(X,Y)

plt.xlim(x[i]-0.25,x0+0.25)
plt.ylim(y0-0.25,y[i]+0.25)

import warnings
warnings.filterwarnings("ignore") #suppress warning for contour plotting

CS = plt.contour(X, Y, Z, 200, colors='black')
plt.clabel(CS)

plt.title("CONTOUR PLOTTING (ISOLINE)")
plt.plot(x,y,marker='o')
plt.xlabel("x")
plt.ylabel("y")
plt.annotate("MINIMUM POINT", xy=(x[i],y[i]), xytext=(x[i]+0.25,y[i]+0.15), color='red',arrowprops=dict(facecolor='red', shrink=0.05), verticalalignment='top',)
plt.show()
