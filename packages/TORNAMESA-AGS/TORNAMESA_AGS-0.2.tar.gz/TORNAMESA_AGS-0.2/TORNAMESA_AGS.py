"""
@author: ADOLFO
"""
from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT
import time
import math as ma


class Tornamesa():
    def __init__(self, puerto):
        #INICIO COMUNICACION SERIAL
        self.port=puerto
        self.board=Arduino(self.port)
        it = util.Iterator(self.board)
        it.start()
        #DIFINICION PUERTOS DE SALIDA
        self.board.digital[13].mode =OUTPUT
        self.board.digital[2].mode =OUTPUT
        self.board.digital[3].mode =OUTPUT
        self.board.digital[4].mode =OUTPUT
        self.board.digital[5].mode =OUTPUT
        #INICIALIZACIONVARIABLES
        self.sentido=0
        self.periodo=0.03
        self.board.digital[2].write(1)
        
        
    def blink(self, delay):
        self.board.digital[13].write(1)
        time.sleep(delay)
        self.board.digital[13].write(0)
        time.sleep(delay)
        
    def poseAngulo(self,posicion):
        self.pasos_sp=self.SetPoint(ma.fabs(posicion))
        print(self.pasos_sp)
        if posicion <0:
            self.sentido=0
        else:
            self.sentido=1
        self.board.digital[5].write(self.sentido)  # DIRECCION
        time.sleep(0.5)
        self.board.digital[2].write(0)  #ENABLE
        self.board.digital[3].write(1)  #MEDIO PASO
        
        for i in range( int(self.pasos_sp)):	#// 512*4 = 2048 pasos
            self.board.digital[4].write(1)
            time.sleep(self.periodo)
            self.board.digital[4].write(0)
            time.sleep(self.periodo)
        
        time.sleep(0.1)
        self.board.digital[2].write(1)  #ENAB90LE
        self.board.digital[3].write(0)  #MEDIO PASO
        self.board.digital[5].write(self.sentido)  # DIRECCION
    
    def giroTiempo(self, delay):
                
        if delay <0:
            self.sentido=0
        else:
            self.sentido=1
        self.board.digital[5].write(self.sentido)  # DIRECCION
        time.sleep(0.5)
        self.board.digital[2].write(0)  #ENABLE
        self.board.digital[3].write(1)  #MEDIO PASO
        
        self.tiempo_inicial=time.time()
        self.tiempo_actual=time.time()
        self.tiempo_final=self.tiempo_inicial+ma.fabs(delay)
        
        while self.tiempo_actual <= self.tiempo_final:
            self.board.digital[4].write(1)
            time.sleep(self.periodo)
            self.board.digital[4].write(0)
            time.sleep(self.periodo)
            self.tiempo_actual=time.time()
            
        time.sleep(0.1)
        self.board.digital[2].write(1)  #ENAB90LE
        self.board.digital[3].write(0)  #MEDIO PASO
        self.board.digital[5].write(self.sentido)  # DIRECCION
        
        
    def SetPoint(self,angulo):
        if ((angulo*400)%360) == 0.0:
            pasos=((angulo*400)/360)
        else:
            up= ma.ceil(((angulo*400)/360))
            sp=((angulo*400)/360)
            floor=ma.floor(((angulo*400)/360))
            if  (sp-floor)>=(up-sp):
                pasos=up
            else:
                pasos=floor
        return pasos
    
    def alterVelocidad(self, velocidad):
        if velocidad >15:
            velocidad=15
        if velocidad<1:
            velocidad=1
        
        self.periodo=60/(velocidad*800)
    
    def restaurarValores(self):
        self.sentido=0
        self.periodo=0.03
        self.board.digital[2].write(1)
        
        
    def close(self):
        self.board.digital[13].write(0)
        self.board.exit()
        self.board.digital[2].write(1)  #ENAB90LE
        

