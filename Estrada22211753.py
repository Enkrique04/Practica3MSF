"""
Práctica 3: Muscoesqueletico 

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Ian Enrique Estrada Castillo
Número de control: 22211753
Correo institucional: l22211753@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
import pandas as pd

x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
n= round((tend - t0)/dt) + 1 
t = np.linspace(t0, tend, n)
u = np.zeros(n); u[round(1/dt):round(2/dt)] =1

def musc (Cs,Cp,R,a):
    num = [Cs*R,1-a]
    den = [R*(Cp+Cs),1]
    sys=ctrl.tf(num,den)
    return sys
#Funcion de transferencia: Control
Cs,Cp,R,a = 10E-6,100E-6,100,0.25
syscon = musc(Cs,Cp,R,a)
print(f'Funcion de transferencia del Control: {syscon}')

#Funcion de transferencia: Caso
Cs,Cp,R,a = 10E-6,100E-6,10E3,0.25
syscas = musc(Cs,Cp,R,a)
print(f'Funcion de transferencia del caso: {syscas}')

_,Fs1 = ctrl.forced_response(syscon,t,u,x0)
_,Fs2 = ctrl.forced_response(syscas,t,u,x0)

fgl= plt.figure()
plt.plot(t,u,'-',linewidth = 1, color =[0.569,0.392,0.235],label='F(s)')
plt.plot(t,Fs1,'-',linewidth = 1, color =[0.902,0.224,0.274],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth = 1, color =[0.114,0.208,0.341],label='Fs2(t):Caso')

plt.grid(False) #Para poner una cuadricula en la grafica
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t[s]')
plt.ylabel('Fs[V]')
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3)
plt.show()
fgl.set_size_inches(w,h)
fgl.tight_layout()
fgl.savefig('Sistema Musculoesqueletico LA python.png',dpi=600,bbox_inches='tight')
fgl.savefig('Sistema Musculoesqueletico LA python.pdf')

def controlador (kP,kI,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI,denPI)
    X = ctrl.series(PI, sys)
    sysPI = ctrl.feedback(X,1,sign=-1)
    return sysPI
Tratamiento = controlador (0.0216974155806455,41824.9323264174,syscas)

_,Fs3 = ctrl.forced_response(Tratamiento,t,Fs1,x0)

fgl= plt.figure()
plt.plot(t,u,'-',linewidth = 1, color =[0.569,0.392,0.235],label='F(s)')
plt.plot(t,Fs1,'-',linewidth = 1, color =[0.902,0.224,0.274],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth = 1, color =[0.114,0.208,0.341],label='Fs2(t):Caso')
plt.plot(t,Fs3,':',linewidth = 1.5, color =[0.271,0.482,0.616],label='Fs3(t):Tratamiento')
plt.grid(False) #Para poner una cuadricula en la grafica
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t[s]')
plt.ylabel('Fs[V]')
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3)
plt.show()
fgl.tight_layout()
fgl.savefig('Sistema Musculoesqueletico LC python.png',dpi=600,bbox_inches='tight')
fgl.savefig('Sistema Musculoesqueletico LC python.pdf')

