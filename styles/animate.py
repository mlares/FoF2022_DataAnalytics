from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randint
import numpy as np
import sys
from tools import set_style

def Lk(xdatos, x, k):
    L=1
    for i in range(len(xdatos)):
        if i!=k:
            L = L*(x-xdatos[i])/(xdatos[k]-xdatos[i])
    return L

def animate(i, x, func, ax, plot_l=False, plot_norm=False):

    y = func(x)
    t = np.linspace(min(x), max(x), 100)
    # plot
    ax.clear()
    ax.plot(t, func(t), '-', color='gray',
            alpha=0.3, linewidth=5)
    ax.axhline(0, color='k', linestyle='--', marker='None')

    N = len(x)
    ind = list(range(N))
    ind.pop(i)
    if plot_l:
        for j in ind:
            f = Lk(x, t, j)
            ax.plot(t, f, ':', color='cornflowerblue', linewidth=1)
        f = Lk(x, t, i)
        ax.plot(t, f, '-', color='cornflowerblue', linewidth=2)
    if plot_norm:
        for j in ind:
            f = Lk(x, t, j)*func(x[j])
            ax.plot(t, f, '-', color='coral', linewidth=0.5)
        f = Lk(x, t, i)*func(x[i])
        ax.plot(t, f, '-', color='coral', linewidth=2)

    ax.plot(x, y, 'o', markersize=4, color='k', mfc='k')
    ax.plot(x, np.repeat(0, N), 'o', markersize=5, color='k', mfc='white')
    ax.plot(x, np.repeat(1, N), 'o', markersize=5, color='k', mfc='white')
    ax.grid()
    ax.set_xlabel('x')
    ax.set_xlabel('x, in An example figure.')
    ax.set_ylabel('f(x)')

def f(x):
    return 1/x

def show_animation():

    x = np.array([.5, 1.5, 2.5, 3.5, 4.5])
    fargs = (x, f, True, True)

    # create the figure and axes objects
    fig, ax = plt.subplots()
    # call animation
    ani = FuncAnimation(fig, animate, frames=list(range(len(x)))*10,
                        fargs=(x, f, ax, True, True), interval=2000, repeat=False)
    plt.show()

def show_static(i, **kwargs):

    x = np.array([.5, 1.5, 2.5, 3.5, 4.5])
    fargs = (x, f, True, True)
    # create the figure and axes objects
    fig, ax = plt.subplots()
    # call plot
    animate(i, x, f, ax, True, False)
    fig.savefig('plot.pdf')
    plt.show()
    plt.close()


if __name__ == '__main__':

    set_style(sys.argv)
    #show_animation()
    show_static(2)
