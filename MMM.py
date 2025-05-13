import numpy as np
import scipy.signal as sig
import matplotlib as plot


def menu():
    print("Menu programu:")
    print("1. Start symulacji")
    print("2. Podglad parametrow")
    print("3. Zmiana parametrow obiektu")
    print("4. Zmiana parametrow lead-lag")
    print("5. Zmiana parametrow wejscia")
    chose = int(input("Wybierz co chcesz zrobic: "))
    if chose == 3:
        object_param_change()
    elif chose == 4:
        lead_lag_param_change()


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


# parametry obiektu
a = [3, 1]
b = [1, 2, 3]

# parametry lead-lag       k_gains = [lead, lag]
k_gains = [1, 1]
lead_lag_zeros = [1, 1]
lead_lag_poles = [1, 1]

while True:
    menu()
