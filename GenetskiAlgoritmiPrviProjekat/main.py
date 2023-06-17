import random

import numpy as np
import json

x_r = [
    0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90,
    1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90,
    2.00, 2.10, 2.20, 2.30, 2.40, 2.50, 2.60, 2.70, 2.80, 2.90,
    3.00, 3.10, 3.20, 3.30, 3.40, 3.50, 3.60, 3.70, 3.80, 3.90,
    4.00, 4.10, 4.20, 4.30, 4.40, 4.50, 4.60, 4.70, 4.80, 4.90
]
y_l = [
    4.0000, 4.0100, 4.0395, 4.0873, 4.1516, 4.2298, 4.3188, 4.4150, 4.5146, 4.6136,
    4.7081, 4.7943, 4.8687, 4.9284, 4.9711, 4.9950, 4.9991, 4.9834, 4.9484, 4.8955,
    4.8268, 4.7451, 4.6537, 4.5561, 4.4563, 4.3582, 4.2657, 4.1827, 4.1122, 4.0572,
    4.0199, 4.0017, 4.0034, 4.0249, 4.0653, 4.1230, 4.1958, 4.2807, 4.3744, 4.4730,
    4.5728, 4.6696, 4.7596, 4.8394, 4.9055, 4.9556, 4.9874, 4.9998, 4.9923, 4.9652
]

L1N = 5
L2N = 3
layer1 = [[0], [0], [0], [0], [0]]
layer2 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
layer3 = [[0, 0, 0]]

bias1 = [0, 0, 0, 0, 0]
bias2 = [0, 0, 0]
bias3 = [0]

output0 = [0]
output1 = [0, 0, 0, 0, 0]
output2 = [0, 0, 0]

def calc_neuron(neurons, input_weights, input_values, bias):
    sum = bias
    for i in range(0, neurons):
        sum += input_weights[i] * input_values[i]
    return sum

def fitness_function(weights):
    ai = 0

    for i in range(0, L1N):
        layer1[i][0] = weights[ai]
        ai += 1

    for i in range(0, L2N):
        for j in range(0, L1N):
            layer2[i][j] = weights[ai]
            ai += 1

    for i in range(0, L2N):
        layer3[0][i] = weights[ai]
        ai += 1

    for i in range(0, L1N):
        bias1[i] = weights[ai]
        ai += 1

    for i in range(0, L2N):
        bias2[i] = weights[ai]
        ai += 1

    bias3[0] = weights[ai]

    mse = 0

    for k in range(0, 50):
        output0[0] = x_r[k]

        for i in range(0, L1N):
            output1[i] = calc_neuron(1, layer1[i], output0, bias1[i])

        for i in range(0, L2N):
            output2[i] = calc_neuron(L1N, layer2[i], output1, bias2[i])

        val = calc_neuron(L2N, layer3[0], output2, bias3[0])

        err = pow(y_l[k] - val, 2)
        mse += err

    return mse / 50
class Vrsta:

    def __init__(self):
        self.chromosome = None
        self.function_error = 0

    def calculatefitness(self):
        self.function_error = fitness_function(self.chromosome)

    def __str__(self):
        return str(self.chromosome) + "\nVrednost funkcije greske je: " + str(self.function_error)

def ukrstanje(a, b):
    global alfaBLX
    global chromosomes

    r = np.random.random(1)
    f = np.abs(a.chromosome - b.chromosome)

    if(a.function_error < b.function_error):
        min = a
    else:
        min = b

    child_chromosome = r * (1 + 2 * alfaBLX) * f - (min.chromosome - alfaBLX * f)

    vrsta_child = Vrsta()
    vrsta_child.chromosome = child_chromosome
    vrsta_child.calculatefitness()
    chromosomes.append(vrsta_child)

def mutiranje(i, mu, sigma):

    mutated_i = i.copy
    for x in range(len(mutated_i)):
        mutated_i[x] += random.gauss(mu ,sigma)
    return mutated_i

populacija = 100
vrstezaparenje = 30
vrstezamutacijuprocenat = 0.4
vrstezaizbacivanjeprocenat = 0.3
alfaBLX = 0.35
randomseed = 0
outputpath = ""

def load():

    global populacija
    global vrstezaparenje
    global vrstezaizbacivanjeprocenat
    global vrstezamutacijuprocenat
    global alfaBLX
    global outputpath
    global randomseed

    file = open("cfg.json")
    if file == None: return
    data = json.load(file)
    if data == None: return

    populacija = data["populacija"]
    vrstezaparenje = data["vrstezaparenje"]
    vrstezaizbacivanjeprocenat = data["vrstezaizbacivanjeprocenat"]
    vrstezamutacijuprocenat = data["vrstezamutacijuprocenat"]
    alfaBLX = data[alfaBLX]
    randomseed = data["randomseed"]
    outputpath = data["outputpath"]

def odsecanje():
    global chromosomes
    global populacija
    global vrstezaizbacivanjeprocenat

    chromosomes.sort(key=lambda x: x.function_error)

    chromosomes = chromosomes[:len(chromosomes) - round(populacija * vrstezaizbacivanjeprocenat)]

def mutiranje():
    global populacija
    global vrstezaparenje
    global vrstezamutacijuprocenat

    mutacija = np.random.randint(0, populacija, round(populacija * vrstezamutacijuprocenat))
    for i in mutacija:
        if i == 0 :
            continue
        chromosomes[i].chromosome = chromosomes[i].chromosome + np.random.uniform(0, 1, 32)
        chromosomes[i].calculatefitness()

def start():
    global chromosomes
    global populacija

    for i in range(0,populacija):
        vrsta = Vrsta()
        vrsta.chromosome = np.random.uniform(-10, 10, 32)
        vrsta.calculatefitness()

        chromosomes.append(vrsta)
def selekcija():
    global vrstezaparenje
    global chromosomes

    for j in range(0, vrstezaparenje):
        ukrstanje(chromosomes[j], chromosomes[j + 1])
        j += 1

if __name__ == '__main__':
    #load()
    chromosomes = []

    start()

    for i in range(0, 150):
        print("Trenutni broj jedinki je: " + str(len(chromosomes)))
        odsecanje()
        selekcija()
        mutiranje()
        chromosomes.sort(key=lambda x: x.funkcija_greske)
        print(chromosomes[0])


