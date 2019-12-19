from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def fourier(x,dx,t,dt,k):
    #BANYAK KOTAK X
    nx = int(x/dx)+1

    #BANYAK KOTAK T
    nt = int(t/dt)+1

    #MATRIX AWAL
    T = np.zeros([nt,nx])
    T[:,0] = 100
    T[:,-1] = 50
    
    Lambda = k*dt/(dx)**2
    
    #i -> space
    #j -> time
    for j in range(0,nt-1):
        for i in range(1,nx-1):
            T[j+1,i] = T[j,i] + Lambda*(T[j,i+1]-2*T[j,i]+T[j,i-1])

    #PRINT HEADER
    print("=========================================================================================================================")
    print(str("t \ x").center(8),end='')
    for j in range(nx):
        print((str(j*dx)+" cm").center(20),end='')
    print()
    print("=========================================================================================================================")

    #PRINT ISI MATRIX
    for i in range(nt): 
        print((str("%.2f"%(i*dt))+" s").center(8),end='')
        for j in range(nx):
            print(str(T[i,j]).center(20),end='')
        print()

    #PLOTTING 3D GRAPH
    xx = np.arange(0, x+dx, dx)
    yy = np.arange(0, t+dt, dt)
    X, Y = np.meshgrid(xx, yy)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, T, cmap='coolwarm', linewidth=0, antialiased=False)

    ax.set_xlabel("Panjang Batang (cm)")
    ax.set_ylabel("Waktu (s)")
    ax.set_zlabel("Temperatur (Celcius)")

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def main():
    #PANJANG BATANG
    x = 10
    #JARAK PARTISI GRID X
    dx = 2

    #WAKTU
    t = 12
    #JARAK PARTISI GRID T
    dt = 0.1

    #KONSTANTA
    k = 0.835

    fourier(x,dx,t,dt,k)    

main()
