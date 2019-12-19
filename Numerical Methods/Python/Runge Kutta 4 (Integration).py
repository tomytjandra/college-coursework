
import numpy as np
import matplotlib.pyplot as plt
import math

def fExact(x, y):
    return -0.5*x**4 + 4*x**3 - 10*x**2 + 8.5*x + 1

def fxy(x, y):
    return -2*x**3 + 12*x**2 - 20*x + 8.5

def RK4(dx, xf, y0):
    x = np.arange(0.0, xf+dx, dx)
    n = round(xf/dx)
    y = np.zeros(n+1)
    y[0] = y0
    sumError = 0
        
    if(xf/dx-math.floor(xf/dx)!=0):
        print("Try another value of dx, cannot compute xFinal")
        return y
    else:
        print("\n===============")
        print("ITERATION TABLE")
        print("===============")
        print("--------------------------------------------------------------------------------------------------------------------------------")
        print(str("i").center(4), str("Xi").center(10), str("K1").center(15), str("K2").center(15), str("K3").center(15), str("K4").center(15), str("Yi(RK)").center(15), str("yExact").center(15), str("Error").center(15))
        print("--------------------------------------------------------------------------------------------------------------------------------")
        
        for i in range(0,n+1):
            k1 = fxy(x[i], y[i])
            k2 = fxy(x[i]+0.5*dx, y[i]+0.5*k1*dx)
            k3 = fxy(x[i]+0.5*dx, y[i]+0.5*k2*dx)
            k4 = fxy(x[i]+dx, y[i]+k3*dx)

            if i<n:
                y[i+1] = y[i] + (k1+2*k2+2*k3+k4)/6*dx

            ye = fExact(x[i], y[i])
            error = abs(y[i]-ye)
            sumError = sumError + error
            print(str(i).center(4),
                  str(x[i]).center(10),
                  str(k1).center(15),
                  str(k2).center(15),
                  str(k3).center(15),
                  str(k4).center(15),
                  str(y[i]).center(15),
                  str(ye).center(15),
                  str(error).center(15))

        print("\n===============")
        print("    RESULT")
        print("===============")
        print("x: ", xf)
        print("y: ", y[-1])
        print("Sum of error: ", sumError)
        
        return y

#MAIN CODE STARTS HERE
print("Python code by Tomy 1801431662")
print("===============================")
print("FOURTH-ORDER RUNGE-KUTTA METHOD")
print("===============================")
print("Numerically integrate f(x,y) = -2x^3 + 12x^2 - 20x + 8.5\nfrom x=0 to x=4 with step size 0.4\nThe initial condition at x=0 is y=1")

dx = 0.4
xf = 4.0
y0 = 1.0

xRK = np.arange(0.0, xf+dx, dx)
yRK = RK4(dx, xf, y0)
x = np.linspace(0.0, xf, 100)

if(yRK.all()!=0):
    plt.plot(x, fExact(x,0), color='black')
    plt.plot(xRK, yRK, 'ro')
    plt.legend(['EXACT', 'NUMERIC'], loc='upper left')
    plt.title("PLOTTING EXACT & NUMERIC GRAPH")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

print("\n===============")
print("    NOTES")
print("===============")
print("You can use the Runge-Kutta function by using the following syntax:\n")
print("def fExact(x, y):\n\treturn (integrated function)\n\n")
print("def fxy(x, y):\n\treturn (function of dy/dx)\n\n")
print("RK4(step size, x final value, initial condition y0)")
