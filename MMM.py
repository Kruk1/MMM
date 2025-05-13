import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt


def menu():
    print("Menu programu:")
    print("1. Start symulacji")
    print("2. Podglad parametrow")
    print("3. Zmiana parametrow obiektu")
    print("4. Zmiana parametrow lead-lag")
    print("5. Zmiana parametrow wejscia")
    print("6. Wizualizacja sygnalu wejsciowego")
    chose = int(input("Wybierz co chcesz zrobic: "))
    if chose == 3:
        object_param_change()
    elif chose == 4:
        lead_lag_param_change()
    elif chose == 5:
        input_param_change()
    elif chose == 6:
        input_signal_visualization()


def object_param_change():
    print("\n")
    print(a, b)
    which_one = input("Jaki parametr zmienic (a lub b): ")
    which_index = int(input("Ktory parametr zmienic: "))
    param_num = int(input("Jaka wartosc wpisac: "))
    if which_one == "a":
        if which_index < len(a):
            a[which_index] = param_num
    elif which_one == "b":
        if which_index < len(b):
            b[which_index] = param_num
    print(a, b)
    print("\n")


def lead_lag_param_change():
    print("\n")
    print(k_gains, lead_lag_zeros, lead_lag_poles)
    which_one = input("Jaki parametr zmienic (k, z lub p): ")
    which_index = int(input("Ktory parametr zmienic: "))
    param_num = int(input("Jaka wartosc wpisac: "))
    if which_one == "k":
        if which_index < len(k_gains):
            k_gains[which_index] = param_num
    elif which_one == "z":
        if which_index < len(lead_lag_zeros):
            lead_lag_zeros[which_index] = param_num
    elif which_one == "p":
        if which_index < len(lead_lag_poles):
            lead_lag_poles[which_index] = param_num
    print(k_gains, lead_lag_zeros, lead_lag_poles)
    print("\n")


def input_param_change():
    global y
    print(len(y), len(t))
    print("\n 1. sinus")
    print("2. prostokatny")
    print("3. piloksztaltny")
    print("4. trojkatny")
    signal_decision = int(input("Na jaki sygnal zmienic: "))
    amplitude = int(input("Jaka chcesz amplitude sygnalu: "))
    if signal_decision == 1:
        yy = []
        for i in range(len(t)):
            yy.append(np.sin((np.pi/(len(t)/25))*i*5)*amplitude);
        y = yy
    elif signal_decision == 2:
        duty = float(input("Jakie wypelnienie sygnalu (0-1): "))
        if 0 <= duty <= 1:
            y = sig.square(2*np.pi*5*t, duty)*amplitude
        else:
            print("Niepoprawna wartosc sprobuj jeszcze raz")
    elif signal_decision == 3:
        y = sig.sawtooth(2*np.pi*5*t)*amplitude
    elif signal_decision == 4:
        make_triangle_input(amplitude)

def input_signal_visualization():
    plt.plot(t, y)
    plt.ylim(-2, 2)
    plt.show()


def make_triangle_input(amp, lam=1, phi=0):
    global y
    y = (2*amp/np.pi)*np.arcsin(np.sin((2*np.pi*5*t-phi)/lam))

# parametry obiektu
a = [3, 1]
b = [1, 2, 3]

# parametry lead-lag       k_gains = [lead, lag]
k_gains = [1, 1]
lead_lag_zeros = [1, 1]
lead_lag_poles = [1, 1]

# sygnal wejsciowy
t = np.linspace(0, 1, 1000, endpoint=False)
y = sig.square(2*np.pi*5*t, 0.9)

while True:
    menu()
