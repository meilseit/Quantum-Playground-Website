
from .nuts_bolts.hub import Sandbox
from .nuts_bolts.pot import Pot
from .nuts_bolts.pot_int import Potint
from .models import PairNorm, ParticleSize, PotInt, Energies, TrapLengh, Pair, Xfactors, Pfactors,FlagStart
import numpy as np






def generateE():
    try:
        trapLength = TrapLengh.objects.first().length
        particleSize = ParticleSize.objects.first().size
    except AttributeError:
        trapLength = 3e-10
        particleSize = 5110000.0
    res = 1000
    quantumSandbox = Sandbox(Pot(populate()),trapLength, particleSize, res, extend=2 )
    x = quantumSandbox.x
    E, psi = quantumSandbox.produceEnergies()
    k0 = quantumSandbox.diagK
    k1 = quantumSandbox.offDiagK
    p2Op = (np.diag(k0) + np.diag(k1, k=1) + np.diag(k1, k=-1)) * particleSize * 2 
    return x, psi, E, p2Op


def generateV():
    #TrapLengh(length = 3e-10).save()
    trapLength = 3e-10
    particleSize = 511000.0
    if(TrapLengh.objects.first() != None):
        trapLength = TrapLengh.objects.first().length   
    if(ParticleSize.objects.first() != None):  
        particleSize = ParticleSize.objects.first().size
    res = 1000
    quantumSandbox = Sandbox(Pot(populate()), trapLength, particleSize, res, extend=2)
    x = quantumSandbox.x
    V = quantumSandbox.V
    return x, V



def clear(): #clears the data from the data base
    Energies.objects.all().delete()
    Pair.objects.all().delete()
    PairNorm.objects.all().delete()
    Xfactors.objects.all().delete()
    Pfactors.objects.all().delete()


def populate():
    output = []
    objects = list(PotInt.objects.all())
    for obj in objects:
        temp = Potint(obj.left_bound, obj.right_bound, obj.value)
        output.append(temp)
    return output


def GraphState(n):
    objList = list(Pair.objects.filter(state = n))
    xyValues = [[objList[i].x ,objList[i].y] for i in range(len(objList))]
    objList = list(PairNorm.objects.filter(stateNorm = n))
    xyValuesNorm = [[objList[i].x ,objList[i].y] for i in range(len(objList))]
    
    yf = np.fft.fft(np.array(xyValues)[:, 1])
    freq = np.fft.fftfreq(len(xyValues), d=1/1000.0)
    print(freq[-50:])
    yfNorm = (np.abs(yf))**2
    print(yfNorm[-50:])
    xyPValuesNorm = [[freq[i], float(yfNorm[i])] for i in range(len(freq))]
    return xyValues, xyValuesNorm, xyPValuesNorm

def ExpectationValues(p2Op, x, psi, E):
    ExpX = []
    ExpX2 = []
    ExpP2 = []
    x2 = np.square(x)
    xOp = np.diag(x)
    x2Op = np.diag(x2)
    for n in range(len(E)):
        rc = psi[:, n] #1000x1
        cr = np.transpose(psi[:, n]) #1x1000
        ExpX2.append(np.dot(cr, np.dot(x2Op,rc)))
        ExpP2.append(np.dot(cr, np.dot(p2Op,rc)))
        ExpX.append(np.dot(cr, np.dot(xOp,rc)))
    ExpP = list(np.zeros(len(ExpP2)))
    return [ExpX, ExpP, ExpX2, ExpP2]

def ProcessExpectationValues(arr):
    for i in range(len(arr[0])):
        modelX = Xfactors()
        modelP = Pfactors()
        modelX.state = i
        modelX.deltaX = np.sqrt(arr[2][i] - arr[0][i]**2)
        modelX.expX = arr[0][i]
        modelP.state = i
        modelP.deltaP = np.sqrt(arr[3][i] - arr[1][i]**2)
        modelP.expP = arr[1][i]
        modelX.save()
        modelP.save()
        print(np.sqrt(arr[3][i] - arr[1][i]**2)* np.sqrt(arr[2][i] - arr[0][i]**2))
        
def loadPreset(fn):
    clear()
    PotInt.objects.all().delete()
    npzfile = np.load(fn)
    x = npzfile["x"]
    psi = npzfile["psi"]
    E = npzfile["E"]
    p2Op = npzfile["p2Op"]
    potLayout = npzfile["V"]
    for layouts in potLayout:
        PotInt.objects.create(value = layouts[0], right_bound = layouts[1], left_bound = layouts[2])
    arr = ExpectationValues(p2Op, x,psi,E)
    ProcessExpectationValues(arr)
    for n in range(len(E)):
        Energies.objects.create(n=n, Energy = E[n])
        for i in range(len(x)):
            y1 = (psi[i][n])**2
            y2 = psi[i][n]
            PairNorm.objects.create(x = x[i], y = y1, stateNorm = n)
            Pair.objects.create(x = x[i], y = y2, state = n)

def setFlag():
    FlagStart.objects.all().delete()
    setupFlag = FlagStart.objects.create()
    setupFlag.flag = False
    setupFlag.save()






         

