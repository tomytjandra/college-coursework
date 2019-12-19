from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def func(x):
    y = -1*(2*sin(x)-x**2/10)
    return y

def funcPrime(x):
    y = -1*(2*cos(x)-x/5)
    return y

def funcDoublePrime(x):
    y = -1*(-2*sin(x)-1/5)
    return y

def appendData(x, decimalPlaces):
    xList.append(round(x,decimalPlaces))
    yList.append(round(func(x),decimalPlaces))
    yPrimeList.append(round(funcPrime(x),decimalPlaces))
    yDoublePrimeList.append(round(funcDoublePrime(x),decimalPlaces))
    
#MAIN CODE STARTS HERE

#INITIALIZATION
xList = []
yList = []
yPrimeList = []
yDoublePrimeList = []
x0 = 2.5 #initial guess of x

print("Python code by Tomy 1801431662")
print("===============")
print("NEWTON'S METHOD")
print("===============")
print("Minimum value of f(x) = -2sin(x)+x^2/10 with initial guess x0 = 2.5")
decimalPlaces = int(input("Input decimal places (integer): "))
appendData(x0,decimalPlaces)

#NEWTON'S METHOD ITERATION
xOld = x0
iteration = 0
while True:
    iteration = iteration + 1
    xNew = xOld - funcPrime(xOld)/funcDoublePrime(xOld)
    appendData(xNew,decimalPlaces)

    diff = abs(xOld-xNew)
    if diff < 10E-5:
        break

    xOld = xNew

#PRINTING RESULTS
print("\n===============")
print("ITERATION TABLE")
print("===============")

print('i'.center(3), 'x'.center(15), 'f(x)'.center(15), 'f\'(x)'.center(15), 'f\"(x)'.center(15))    
for i in range(0,iteration+1):
    print(str(i).center(3),
          str(xList[i]).center(15),
          str(yList[i]).center(15),
          str(yPrimeList[i]).center(15),
          str(yDoublePrimeList[i]).center(15))

print("\n===============")
print("    RESULT")
print("===============")

print("Nearest extreme point from initial guess x0 = 2.5:")
print("x = ", xList[-1])
print("y = ", yList[-1], "(minimum value)")

#GRAPHING
fig, ax = plt.subplots()
x = np.arange(-2, 5, 0.01)

f = -1*(2*np.sin(x)-x**2/10)
line, = ax.plot(x, f, lw=3, color='black')
ax.text(-2,2.5,'f(x) = -2sin(x)+x^2/10')

def animatePoint(i): 
    line, = ax.plot(xList[i],yList[i],'ro',color='r')
    return line,

def animateLine(i):
    line, = ax.plot(x,yPrimeList[i]*(x-xList[i])+yList[i], lw=1)
    return line,

aniPoint = animation.FuncAnimation(fig, animatePoint, np.arange(0, iteration+1), interval=1000, blit=False, repeat=False)
aniLine = animation.FuncAnimation(fig, animateLine, np.arange(0, iteration+1), interval=1000, blit=False, repeat=False)

ax.annotate("x0 = %r" %(x0), xy=(xList[0],yList[0]), xytext=(xList[0]-1,yList[0]+2),
            arrowprops=dict(facecolor='black', shrink=0.05))
ax.annotate("nearest extreme point from x0\nx = %r\ny = %r (minimum value)" %(xList[-1],yList[-1]), xy=(xList[-1], yList[-1]), xytext=(xList[-1], yList[-1]-5),
            arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()
