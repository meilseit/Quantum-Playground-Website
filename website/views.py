
from django.shortcuts import render
import django_rq
from .forms import CreateForm
from .models import ParticleSize, Pfactors, TrapLengh, Pair,Energies, PairNorm, Xfactors, PotInt, FlagStart
from .functions import GraphState, clear, generateE, generateV, ExpectationValues, ProcessExpectationValues, loadPreset, presetPotentialSetup, setFlag
from .tasks import presetTask, storeEnergiesTask
import numpy as np
import time



# Create your views here.
def home(request):  

    flag = True
    if(FlagStart.objects.first != None):
        flag = False

    queue = django_rq.get_queue('default', default_timeout=800) #intialize a redis queue in the background
    queueLen = len(queue) #keep track of queue length during every refresh

    xyValues = []
    xyValuesNorm = []
    xyPValuesNorm = []
    xyPot = []
    formPot = CreateForm()
    energyLevel = []
    energy = "...."
    deltaX = "...."
    deltaP = "...."
    expX = 0.0

    if request.method =="POST":
        #this is the first drop down menu
        if "smallWell" in request.POST: #When the preset of QFW is chosen
            clear(queue)
            path = "./website/static/website/presets/square_sm.npz"
            TrapLengh.objects.create(length=10.0e-10)
            presetPotentialSetup(path)
            queue.enqueue(presetTask, args=(path,))
            time.sleep(5.0)
        elif "bigWell" in request.POST:  #when the perset of QHO is chosen
            clear(queue)
            path = "./website/static/website/presets/square_lg.npz"
            TrapLengh.objects.create(length=100.0e-10)
            presetPotentialSetup(path)
            queue.enqueue(presetTask, args=(path,))
            time.sleep(5.0)
        elif "perturbationWell" in request.POST:  #when the perset of QHO is chosen
            clear(queue)
            path = "./website/static/website/presets/pertubation.npz"
            TrapLengh.objects.create(length=9.0e-10)
            presetPotentialSetup(path)
            queue.enqueue(presetTask, args=(path,))
            time.sleep(5.0)
        elif "quadWell" in request.POST:  #when the perset of QHO is chosen
            clear(queue)
            path = "./website/static/website/presets/quad.npz"
            TrapLengh.objects.create(length=16.0e-10)
            presetPotentialSetup(path)
            queue.enqueue(presetTask, args=(path,))
            time.sleep(5.0)

        elif "wellSize" in request.POST: #when a well size is entered
            TrapLengh.objects.all().delete()
            length = float(request.POST["length"])
            model = TrapLengh()
            model.length = length*1e-10
            model.save()


        #this is the second drop down menu
        elif "electron" in request.POST:  #when we have an elctron preset
            ParticleSize.objects.all().delete()
            size = 511000.0
            model = ParticleSize()
            model.size = size
            model.save()
        elif "proton" in request.POST: #when we have an proton preset 
            ParticleSize.objects.all().delete()
            size = 938000000.0
            model = ParticleSize()
            model.size = size
            model.save()
        elif "muon" in request.POST: #when we have muon preset
            ParticleSize.objects.all().delete()
            size = 106000000.0
            model = ParticleSize()
            model.size = size
            model.save()
        elif "particleSize" in request.POST: #when a costume particle is being handled
            ParticleSize.objects.all().delete()
            size = float(request.POST["size"])
            model = ParticleSize()
            model.size = size
            model.save()


        #this is the third drop down menu
        elif "pot" in request.POST:  #when we enter out potentials
            formPot = CreateForm(request.POST) #form is the form object 
            max = float(request.POST.get("right_bound"))
            min = float(request.POST.get("left_bound")) 
            if(min < max and min >= 0): #check values to make sure the bounds are correct
                formPot.save()


        #this is the fourth drop down menu
        elif "energy" in request.POST: #when we want to generate the energies 
            clear(queue)
            x, psi, E, p2Op = generateE()
            queue.enqueue(storeEnergiesTask, args=(E, psi, x))
            arr = ExpectationValues(p2Op, x, psi, E)
            ProcessExpectationValues(arr)
            time.sleep(10.0)


        elif "state" in request.POST: #when we want to generate the momentums
            state = int(request.POST["state"])
            psi, psiNorm, psiNormP = GraphState(state - 1)
            xyValues.extend(psi)
            xyValuesNorm.extend(psiNorm)
            xyPValuesNorm.extend(psiNormP)
            xmax = xyValues[-1][0] 
            xmin = xyValues[0][0]
            modelE = Energies.objects.get(n = state - 1)
            modelX = Xfactors.objects.get(state = state -1)
            modelP = Pfactors.objects.get(state = state -1 )
            deltaX = "{:.3f}".format(modelX.deltaX * 1e10 )
            deltaP = "{:.3f}".format(modelP.deltaP)
            energy = "{:.3f}".format(modelE.Energy)
            expX = modelX.expX
            energyLevel = [[xmin, float(energy)],[xmax, float(energy)]]


        elif "clear" in request.POST:
            clear(queue)
            


    x, V = generateV()
    potPairs = [[x[i],V[i]] for i in range(len(x))]
    xyPot.extend(potPairs)


    if(flag):
        npzfile = np.load('./website/static/website/presets/setup.npz')
        xyValues = npzfile['psi'].tolist()
        xyValuesNorm = npzfile['psiNorm'].tolist()
        xyPValuesNorm = npzfile['psiNormP'].tolist()
        xyPot = npzfile['potPairs'].tolist()
        energyLevel = npzfile['energyLevel'].tolist()
        energy = npzfile['energy']
        deltaX = npzfile['deltaX']
        deltaP = npzfile['deltaP']
        expX = npzfile['expX']

    energies = ["{:.3f}".format(energy.Energy) for energy in Energies.objects.all()]
    states = range(1, len(list(energies)) + 1) 

    #this is what i am delivering to the template
    context = {
        "energyLevel":energyLevel,
        "energy": energy,
        "xyValues":xyValues,
        "xyValuesNorm":xyValuesNorm,
        "formPot":formPot,
        "xyPot":xyPot,
        "states": states,
        "deltaX": deltaX, 
        "deltaP": deltaP,
        "expX": expX,
        "xyPValuesNorm":xyPValuesNorm,
        "queueLen":queueLen,
    }
     
    return render(request, "website/base.html", context)


