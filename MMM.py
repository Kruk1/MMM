import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_params():
    a[1] = float(entry_a1.get())
    a[0] = float(entry_a0.get())
    b[2] = float(entry_b2.get())
    b[1] = float(entry_b1.get())
    b[0] = float(entry_b0.get())
    k_gains[0] = float(entry_gain0.get())
    k_gains[1] = float(entry_gain1.get())
    lead_lag_poles[0] = float(entry_pole0.get())
    lead_lag_poles[1] = float(entry_pole1.get())
    lead_lag_zeros[0] = float(entry_zero0.get())
    lead_lag_zeros[1] = float(entry_zero1.get())


def get_input_params():
    global u
    
    signal_decision = choice.get()
    amplitude = float(entry_amp.get())
    frequency = float(entry_freq.get())
    if signal_decision == "Sine wave":
        uu = []
        for i in range(len(t)):
            uu.append((np.sin(frequency*2*np.pi*i*0.01))*amplitude);  
        u = uu
    elif signal_decision == "Square wave":
        duty = float(entry_duty.get())
        if 0 <= duty <= 1:
            u = sig.square(2*np.pi*frequency*t, duty)*amplitude
        else:
            print("Niepoprawna wartosc sprobuj jeszcze raz")
    elif signal_decision == "Sawtooth wave":
        u = sig.sawtooth(2*np.pi*frequency*t)*amplitude
    elif signal_decision == "Triangle wave":
        make_triangle_input(amplitude,frequency)
    else:
        u = amplitude*np.ones(len(t))

def make_triangle_input(amp, freq, lam=1, phi=0):
    global u
    u = (2*amp/np.pi)*np.arcsin(np.sin((2*np.pi*freq*t-phi)/lam))

def input_signal_visualization():
    get_input_params()
    plt.plot(t, u)
    plt.show()

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

def integration(m_stanu_A, m_stanu_B, x, h, u0, u1): #całkowanie metodą trapezów
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
    get_params()
    get_input_params()
    L, M = calculate_transmitation_parameters()
    Ax, Bu, Cx, Du = calculate_state_parameters(L,M)
    for i in range(1,len(t)):
        x = integration(Ax, Bu, x, 0.01, u[i-1], u[i])
        y[i] = Cx[0,0]*x[0,0] + Cx[0,1]*x[1,0] + Cx[0,2]*x[2,0] + Cx[0,3]*x[3,0] + Du*u[i]
    
    plt.plot(t,y)
    plt.show()

# parametry obiektu
a = [0, 0]
b = [0, 0, 0]

# parametry lead-lag       k_gains = [lead, lag]
k_gains = [1, 1]
lead_lag_zeros = [0, 0]
lead_lag_poles = [0, 0]

t = np.linspace(0, 10, 1000, endpoint=False)

#GUI
def combobox_selected(event=None):
    sig_type = choice.get()

    if sig_type != "Unit jump":
        freq_label.grid(column=2, row=10)
        entry_freq.grid(column=3, row=10)
    else:
        freq_label.grid_forget()
        entry_freq.grid_forget()

    if sig_type == "Square wave":
        duty_label.grid(column=4, row=10)
        entry_duty.grid(column=5, row=10)
    else:
        duty_label.grid_forget()
        entry_duty.grid_forget()

root = tk.Tk()
root.title("MMM-simulator")

diagram_img = tk.PhotoImage(file='MMM_diagram.png')
label_img = tk.Label(root, image=diagram_img)
label_img.grid(column=0, row=0, columnspan=7)

ttk.Label(root, text="Object parameters:").grid(column=0, row=1, sticky="w", columnspan=2)

ttk.Label(root, text="a1:").grid(column=0, row=2, sticky="w")
entry_a1 = ttk.Entry(root)
entry_a1.insert(0,"0")
entry_a1.grid(column=1, row=2)

ttk.Label(root, text="a0:").grid(column=2, row=2, sticky="w")
entry_a0 = ttk.Entry(root)
entry_a0.insert(0,"1")
entry_a0.grid(column=3, row=2)

ttk.Label(root, text="b2:").grid(column=0, row=3, sticky="w")
entry_b2 = ttk.Entry(root)
entry_b2.insert(0,"0")
entry_b2.grid(column=1, row=3)

ttk.Label(root, text="b1:").grid(column=2, row=3, sticky="w")
entry_b1 = ttk.Entry(root)
entry_b1.insert(0,"0")
entry_b1.grid(column=3, row=3)

ttk.Label(root, text="b0:").grid(column=4, row=3, sticky="w")
entry_b0 = ttk.Entry(root)
entry_b0.insert(0,"1")
entry_b0.grid(column=5, row=3)

ttk.Label(root, text="LEAD parameters:").grid(column=0, row=4, sticky="w", columnspan=2)

ttk.Label(root, text="gain(k):").grid(column=0, row=5, sticky="w")
entry_gain0 = ttk.Entry(root)
entry_gain0.insert(0,"1")
entry_gain0.grid(column=1, row=5)

ttk.Label(root, text="z:").grid(column=2, row=5, sticky="w")
entry_zero0 = ttk.Entry(root)
entry_zero0.insert(0,"0")
entry_zero0.grid(column=3, row=5)

ttk.Label(root, text="p:").grid(column=4, row=5, sticky="w")
entry_pole0 = ttk.Entry(root)
entry_pole0.insert(0,"0")
entry_pole0.grid(column=5, row=5)

ttk.Label(root, text="LAG parameters:").grid(column=0, row=6, sticky="w", columnspan=2)

ttk.Label(root, text="gain(k):").grid(column=0, row=7, sticky="w")
entry_gain1 = ttk.Entry(root)
entry_gain1.insert(0,"1")
entry_gain1.grid(column=1, row=7)

ttk.Label(root, text="z:").grid(column=2, row=7, sticky="w")
entry_zero1 = ttk.Entry(root)
entry_zero1.insert(0,"0")
entry_zero1.grid(column=3, row=7)

ttk.Label(root, text="p:").grid(column=4, row=7, sticky="w")
entry_pole1 = ttk.Entry(root)
entry_pole1.insert(0,"0")
entry_pole1.grid(column=5, row=7)

ttk.Label(root, text="Input parameters").grid(column=0, row=8, sticky="w", columnspan=2)

ttk.Label(root, text="Wave type:").grid(column=0, row=9, sticky="w")
options = ["Unit step","Sine wave", "Square wave", "Sawtooth wave", "Triangle wave"]
choice = ttk.Combobox(root, values=options)
choice.set("Unit step")
choice.grid(column=1, row = 9, columnspan=2)
choice.bind("<<ComboboxSelected>>", combobox_selected)

ttk.Label(root, text="Amplitude:").grid(column=0, row=10, sticky="w")
entry_amp = ttk.Entry(root)
entry_amp.insert(0,"1")
entry_amp.grid(column=1, row=10)

freq_label = ttk.Label(root, text="Frequency:")
entry_freq = ttk.Entry(root)
entry_freq.insert(0,"1")

duty_label = ttk.Label(root, text="Duty cycle:")
entry_duty = ttk.Entry(root)
entry_duty.insert(0,"0.5")

combobox_selected()

ttk.Button(root, text="Simulate", command=simulation).grid(column=5, row=11, columnspan=2, pady=10)
ttk.Button(root, text="Show input signal", command=input_signal_visualization).grid(column=0, row=11, columnspan=2, pady=10)

root.mainloop()