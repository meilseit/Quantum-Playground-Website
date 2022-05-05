from .models import Energies, Pair
from .functions import ExpectationValues, ProcessExpectationValues
import numpy as np

def presetTask(path):
    npzfile = np.load(path)
    x = npzfile["x"]
    psi = npzfile["psi"]
    E = npzfile["E"]
    p2Op = npzfile["p2Op"]
    arr = ExpectationValues(p2Op, x,psi,E)
    ProcessExpectationValues(arr)
    for n in range(len(E)):
        Energies.objects.create(n=n, Energy = E[n])
        for i in range(len(x)):
            Pair.objects.create(x = x[i], y = psi[i][n], state = n)
        

def storeEnergiesTask(E, psi, x):
    
    for n in range(len(E)):
        for i in range(len(x)):
            Pair.objects.create(x = x[i], y = psi[i, n], state = n)
        Energies.objects.create(n=n, Energy = E[n])