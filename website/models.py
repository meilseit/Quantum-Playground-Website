from django.db import models

# Create your models here.
class PotInt(models.Model):
    value = models.FloatField()
    right_bound = models.FloatField()
    left_bound = models.FloatField()
    def sci_not(num):
        return "{:e}".format(num)

    def __str__(self):
        return "The potential from " + str(self.left_bound) + " to " + str(self.right_bound) + " is " + str(self.value)

class TrapLengh(models.Model):
    length = models.FloatField(default=1.0e-10)
    

class ParticleSize(models.Model):
    size = models.FloatField()

class Energies(models.Model):
    n = models.IntegerField(default=0)
    Energy = models.FloatField(default=0)

class Pair(models.Model):
    state = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

class PairNorm(models.Model):
    stateNorm = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

class Xfactors(models.Model):
    state = models.IntegerField()
    deltaX = models.FloatField()
    expX = models.FloatField()

class Pfactors(models.Model):
    state = models.IntegerField()
    deltaP = models.FloatField()
    expP = models.FloatField()

class FlagStart(models.Model):
    flag = models.BooleanField(default=True)
