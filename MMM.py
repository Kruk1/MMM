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
    if chose == 1:
        simulation()
    elif chose == 2:
        print('a = ', a, 'b = ', b)
        print('lead-lag zeros = ', lead_lag_zeros, 'lead-lag poles = ', lead_lag_poles)
        print('lead-lag gains:', k_gains)
    elif chose == 3:
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
    global u
    print("\n 1. sinus")
    print("2. prostokatny")
    print("3. piloksztaltny")
    print("4. trojkatny")
    signal_decision = int(input("Na jaki sygnal zmienic: "))
    amplitude = float(input("Jaka chcesz amplitude sygnalu: "))
    frequency = float(input("Jaka czestotliwosc: "))
    if signal_decision == 1:
        uu = []
        for i in range(len(t)):
            uu.append((np.sin(frequency*2*np.pi*i*0.01))*amplitude);  #(2*np.pi/(len(t)/1000))
        u = uu
    elif signal_decision == 2:
        duty = float(input("Jakie wypelnienie sygnalu (0-1): "))
        if 0 <= duty <= 1:
            u = sig.square(2*np.pi*frequency*t, duty)*amplitude
        else:
            print("Niepoprawna wartosc sprobuj jeszcze raz")
    elif signal_decision == 3:
        u = sig.sawtooth(2*np.pi*frequency*t)*amplitude
    elif signal_decision == 4:
        make_triangle_input(amplitude,frequency)

def input_signal_visualization():
    plt.plot(t, u)
    plt.show()


def make_triangle_input(amp, freq, lam=1, phi=0):
    global u
    u = (2*amp/np.pi)*np.arcsin(np.sin((2*np.pi*freq*t-phi)/lam))


#parametry transmitancji (l3*s^3+l2*s^2...)/(m4*s^4+m3*s^3...)
def calculate_transmitation_parameters():
    if lead_lag_zeros[0] == lead_lag_poles[0]:
        lead_lag_zeros[0] = 0
        lead_lag_poles[0] = 0
    elif lead_lag_zeros[1] == lead_lag_poles[0]:
        lead_lag_zeros[1] = 0
        lead_lag_poles[0] = 0
    
    if lead_lag_zeros[0] == lead_lag_poles[1]:
        lead_lag_zeros[0] = 0
        lead_lag_poles[1] = 0
    elif lead_lag_zeros[1] == lead_lag_poles[1]:
        lead_lag_zeros[1] = 0
        lead_lag_poles[1] = 0

    l0 = k_gains[0]*k_gains[1]*a[0]*lead_lag_zeros[0]*lead_lag_zeros[1]
    l1 = k_gains[0]*k_gains[1]*(a[1]*lead_lag_zeros[0]*lead_lag_zeros[1] - a[0]*lead_lag_zeros[0] - a[0]*lead_lag_zeros[1])
    l2 = k_gains[0]*k_gains[1]*(a[0] - a[1]*lead_lag_zeros[0] - a[1]*lead_lag_zeros[1])
    l3 = k_gains[0]*k_gains[1]*a[1]
    m0 = b[0]*lead_lag_poles[0]*lead_lag_poles[1] + l0
    m1 = b[1]*lead_lag_poles[0]*lead_lag_poles[1] - b[0]*lead_lag_poles[0] - b[0]*lead_lag_poles[1] + l1
    m2 = b[2]*lead_lag_poles[0]*lead_lag_poles[1] + b[0] - b[1]*lead_lag_poles[0] - b[1]*lead_lag_poles[1] + l2
    m3 = b[1] - b[2]*lead_lag_poles[0] - b[2]*lead_lag_poles[1] + l3
    m4 = b[2]

    return [l0, l1, l2, l3], [m0, m1, m2, m3, m4]


# parametry stanu
def calculate_state_parameters(L,M):
    if M[4] == 0:
        if (M[3] == 0) and (L[3] != 0):
            raise ValueError("Układ nie jest realizowalny fizycznie")
        elif (M[3] == 0) and (L[3] == 0):
            if (M[2] == 0) and (L[2] != 0):
                raise ValueError("Układ nie jest realizowalny fizycznie")
            elif (M[2] == 0) and (L[2] == 0):
                if (M[1] == 0) and (L[1] != 0):
                    raise ValueError("Układ nie jest realizowalny fizycznie")
                elif (M[1] == 0) and (L[1] == 0):
                    if (M[0] == 0):
                        raise ValueError("Układ nie jest realizowalny fizycznie")
                    else:
                        m_stanu_A = np.zeros((4,4))
                        m_stanu_B = np.zeros((4,1))
                        m_stanu_C = np.zeros((1,4))
                        m_stanu_D = L[0]/M[0]
                else:
                    m_stanu_A = np.array([[-M[0]/M[1],0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
                    m_stanu_B = np.array([[1],[0],[0],[0]])
                    m_stanu_C = np.array([[L[0]/M[1] - M[0]*L[1]/(M[1]**2),0,0,0]])
                    m_stanu_D = L[1]/M[1]
            else:
                m_stanu_A = np.array([[0,1,0,0],[-M[0]/M[2],-M[1]/M[2],0,0],[0,0,0,0],[0,0,0,0]])
                m_stanu_B = np.array([[0],[1],[0],[0]])
                m_stanu_C = np.array([[L[0]/M[2] - M[0]*L[2]/(M[2]**2), L[1]/M[2] - M[1]*L[2]/(M[2]**2),0,0]])
                m_stanu_D = L[2]/M[2]             
        else:
            m_stanu_A = np.array([[0,1,0,0],[0,0,1,0],[-M[0]/M[3],-M[1]/M[3],-M[2]/M[3],0], [0,0,0,0]])
            m_stanu_B = np.array([[0],[0],[1],[0]])
            m_stanu_C = np.array([[L[0]/M[3] - M[0]*L[3]/(M[3]**2), L[1]/M[3] - M[1]*L[3]/(M[3]**2), L[2]/M[3] - M[2]*L[3]/(M[3]**2),0]]) 
            m_stanu_D = L[3]/M[3]
    else:
        m_stanu_A = np.array([[0,1,0,0],[0,0,1,0],[0,0,0,1],[-M[0]/M[4],-M[1]/M[4],-M[2]/M[4],-M[3]/M[4]]])
        m_stanu_B = np.array([[0],[0],[0],[1]])
        m_stanu_C = np.array([[L[0]/M[4], L[1]/M[4], L[2]/M[4], L[3]/M[4]]])
        m_stanu_D = 0
    
    return m_stanu_A, m_stanu_B, m_stanu_C, m_stanu_D

def integration(m_stanu_A, m_stanu_B, x, h, u0, u1): 
    x_p = np.zeros((4,1))
    x_b = x
    for j in range(4):
        x_p[j,0] = x[j,0] + h*(m_stanu_A[j,0]*x[0,0] + m_stanu_A[j,1]*x[1,0] + m_stanu_A[j,2]*x[2,0] + m_stanu_A[j,3]*x[3,0] + m_stanu_B[j,0]*u0)
    
    for k in range(4):
        x[k,0] = x_b[k,0] + 0.5*h*(m_stanu_A[k,0]*x_b[0,0] + m_stanu_A[k,1]*x_b[1,0] + m_stanu_A[k,2]*x_b[2,0] + m_stanu_A[k,3]*x_b[3,0] + m_stanu_B[k,0]*u0 + m_stanu_A[k,0]*x_p[0,0] + m_stanu_A[k,1]*x_p[1,0] + m_stanu_A[k,2]*x_p[2,0] + m_stanu_A[k,3]*x_p[3,0] + m_stanu_B[k,0]*u1)
    
    return x

def simulation():
    x = np.zeros((4,1))
    y = np.zeros(len(t))
    L, M = calculate_transmitation_parameters()
    Ax, Bu, Cx, Du = calculate_state_parameters(L,M)
    for i in range(1,len(t)):
        x = integration(Ax, Bu, x, 0.01, u[i-1], u[i])
        y[i] = Cx[0,0]*x[0,0] + Cx[0,1]*x[1,0] + Cx[0,2]*x[2,0] + Cx[0,3]*x[3,0] + Du*u[i]
    
    plt.plot(t,y)
    plt.show()

# parametry obiektu
a = [3, 1]
b = [1, 2, 3]

# parametry lead-lag       k_gains = [lead, lag]
k_gains = [1, 1]
lead_lag_zeros = [0, 0]
lead_lag_poles = [0, 0]

# sygnal wejsciowy
t = np.linspace(0, 10, 1000, endpoint=False)
#u = sig.square(2*np.pi*5*t, 0.9)

while True:
    menu()


