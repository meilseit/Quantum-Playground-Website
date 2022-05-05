
from .nuts_bolts.hub import Sandbox
from .nuts_bolts.pot import Pot
from .nuts_bolts.pot_int import Potint
from .models import PairNorm, ParticleSize, PotInt, Energies, TrapLengh, Pair, Xfactors, Pfactors,FlagStart
import numpy as np
from redis import Redis
from rq.command import send_stop_job_command



def generateE():
    try:
        trapLength = TrapLengh.objects.first().length
        particleSize = ParticleSize.objects.first().size
    except AttributeError:
        trapLength = 3e-10
        particleSize = 511000.0
    res = 1000
    quantumSandbox = Sandbox(Pot(populate()),trapLength, particleSize, res, extend=2 )
    x = quantumSandbox.x
    E, psi = quantumSandbox.produceEnergies()
    k0 = quantumSandbox.diagK
    k1 = quantumSandbox.offDiagK
    p2Op = (np.diag(k0) + np.diag(k1, k=1) + np.diag(k1, k=-1)) * particleSize * 2 
    return x, psi, E, p2Op


def generateV():
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



def clear(reg): #clears the data from the data base
    for job_id in reg.get_job_ids():
        send_stop_job_command(Redis(), job_id)
        print("success")
    Energies.objects.all().delete()
    Pair.objects.all().delete()
    Xfactors.objects.all().delete()
    Pfactors.objects.all().delete()
    setFlag()
    


def populate():
    output = []
    objects = list(PotInt.objects.all())
    for obj in objects:
        temp = Potint(obj.left_bound, obj.right_bound, obj.value)
        output.append(temp)
    return output


def GraphState(n):
    objList = list(Pair.objects.filter(state = n))
    if(len(objList) == 0):
        return [], [], []
    xyValues = [[objList[i].x ,objList[i].y] for i in range(len(objList))]
    xyValuesNorm = [[objList[i].x ,(objList[i].y)**2] for i in range(len(objList))]

    yf = np.fft.fft(np.array(xyValues)[:, 1])
    freq = np.fft.fftfreq(len(xyValues), d=(np.abs(xyValues[1][0] - xyValues[0][0])))
    yfNorm = (np.abs(yf))**2
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


def presetPotentialSetup(path):
    PotInt.objects.all().delete()
    npzfile = np.load(path)
    potLayout = npzfile["V"]
    for layouts in potLayout:
        PotInt.objects.create(value = layouts[0], right_bound = layouts[1], left_bound = layouts[2])


def setFlag():
    setupFlag = FlagStart.objects.first()
    setupFlag.flag = False
    setupFlag.save()






         

