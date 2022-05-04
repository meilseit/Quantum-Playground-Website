from .pot import Pot
import numpy as np
import scipy.linalg as sc

class Sandbox():
    """
    when we intialize our sandbox we want to pass in the well parementer for the given problem
    """
    def __init__(self, potentials, trapLength , particleSize, res, extend = 1):
       self.dx = self.setdX(res, trapLength, extend)
       self.x =  self.setX(trapLength, extend, res)
       self.particleSize = particleSize
       self.constants = self.setConstant(particleSize)
       self.V = self.setV(self.x, potentials)
       self.diagK = self.setDiag(self.constants, self.dx, res)
       self.offDiagK = self.setOffDiag(self.constants, self.dx, res)
       self.potentials = potentials
       
            
    
    def setdX(self, res, trapLength, extend):
        x0, xf = self.wellSize(trapLength, extend)
        dx = (xf-x0)/(res-1)
        return dx 

    def setX(self, trapLength, extend, res):
        x0, xf = self.wellSize(trapLength, extend)
        return np.linspace(x0, xf, res)
    
    def setV(self, x, potentials):
        V = np.zeros(len(x))
        for i, xi in enumerate(x):
            V[i] = potentials.parse(xi)
        return V

    def setConstant(self, particleSize):
        hbarc = 197E-9
        return hbarc**2/particleSize

    def wellSize(self, trapLength, extend):
        x0 = -trapLength*extend
        xf = trapLength*(1+extend)
        return x0, xf

    def setDiag(self,constants, dx, res):
        d = np.zeros(res)
        for i in range(len(d)): 
            d[i] += constants/dx**2
        return d

    def setOffDiag(self, constants, dx, res):
        e = np.zeros(res-1)
        for i in range(len(e)):
            e[i] += -constants*0.5/dx**2
        return e


    def setEigValEigVectors(self, offDiag, diags):
        diag = diags[0] + diags[1]
        self.min, self.max = self.potentials.get_extrema()
        try:
            return sc.eigh_tridiagonal(diag, offDiag, select = "v", select_range=(self.min, 0))
        except ValueError:
            return [], []


    def produceEnergies(self):
        return self.setEigValEigVectors(self.offDiagK, [self.diagK, self.V])

    def produceKineticEnergies(self):
        return self.setEigValEigVectors(self.offDiagK, [self.diagK])

    
        

   