import random

BROJ_POPULACIJE = 60
BROJ_GENERACIJA = 120
PROCENAT_MUTACIJE = 0.2
NAJMANJI_TROSAK_FUNKCIJE = 0
PROSECNI_TROSAK_FUNKCIJE = 0

def pocetna_populacija(broj_poslova):
    populacija = []
    for _ in range(BROJ_POPULACIJE):
        hromozom = random.sample(range(1, broj_poslova + 1), broj_poslova)
        populacija.append(hromozom)
    return populacija

def funkcija_troska(hromozom, matrica_udaljenosti, matrica_vremena):
    trosak = 0
    broj_poslova = len(hromozom)

    for i in range(broj_poslova):
        posao = hromozom[i]
        prethodni_posao = hromozom[i - 1] if i > 0 else hromozom[broj_poslova - 1]

        trosak += matrica_udaljenosti[prethodni_posao - 1][posao - 1] + matrica_vremena[prethodni_posao - 1][posao - 1]

    return trosak

def ukrstanje(roditelj1, roditelj2):
    velicina = len(roditelj1)
    dete = [None] * velicina
    p1, p2 = [0] * velicina, [0] * velicina

    indeks1 = random.randint(0, velicina - 2)
    indeks2 = random.randint(indeks1 + 1, velicina - 1)

    dete[indeks1:indeks2+1] = roditelj1[indeks1:indeks2+1]
    p1 = roditelj1[indeks1:indeks2+1]
    p2 = roditelj2[indeks1:indeks2+1]

    for i in range(velicina):
        if i < indeks1 or i > indeks2:
            gen = roditelj2[i]
            while gen in p1:
                indeks = p1.index(gen)
                gen = p2[indeks]
            dete[i] = gen

    return dete

def mutiranje(hromozom):
    broj_poslova = len(hromozom)
    mutirani_hromozom = hromozom.copy()

    poz1 = random.randint(0, broj_poslova - 1)
    poz2 = random.randint(0, broj_poslova - 1)
    while poz1 == poz2:
        poz2 = random.randint(0, broj_poslova - 1)

    pocetak = min(poz1, poz2)
    kraj = max(poz1, poz2)
    mutirani_hromozom[pocetak:kraj+1] = list(reversed(mutirani_hromozom[pocetak:kraj+1]))

    return mutirani_hromozom

def genetski_algoritam(broj_poslova, matrica_udaljenosti, matrica_vremena):
    global NAJMANJI_TROSAK_FUNKCIJE
    global PROSECNI_TROSAK_FUNKCIJE
    populacija = pocetna_populacija(broj_poslova)
    najbolji_trosak = float('inf')
    najbolji_hromozom = None

    for generacija in range(BROJ_GENERACIJA):
        offspring = []

        for _ in range(BROJ_POPULACIJE // 2):
            roditelj1 = random.choice(populacija)
            roditelj2 = random.choice(populacija)

            dete1 = ukrstanje(roditelj1, roditelj2)
            dete2 = ukrstanje(roditelj2, roditelj1)

            dete1 = mutiranje(dete1)
            dete2 = mutiranje(dete2)

            offspring.append(dete1)
            offspring.append(dete2)

        populacija += offspring

        populacija = sorted(populacija, key=lambda x: funkcija_troska(x, matrica_udaljenosti, matrica_vremena))
        populacija = populacija[:BROJ_POPULACIJE]

        trenutni_najbolji_trosak = funkcija_troska(populacija[0], matrica_udaljenosti, matrica_vremena)
        if trenutni_najbolji_trosak < najbolji_trosak:
            najbolji_trosak = trenutni_najbolji_trosak
            najbolji_hromozom = populacija[0]

        if generacija == 1:
            NAJMANJI_TROSAK_FUNKCIJE = najbolji_trosak
        if najbolji_trosak < NAJMANJI_TROSAK_FUNKCIJE:
            NAJMANJI_TROSAK_FUNKCIJE = najbolji_trosak
        PROSECNI_TROSAK_FUNKCIJE = PROSECNI_TROSAK_FUNKCIJE + najbolji_trosak

        print("Generacija:", generacija + 1, "Najbolji trosak:", najbolji_trosak)


    return najbolji_hromozom

# Test
# att48.in
# bayg29.in
# eli101.in
# gr24.in
# ulysses16.in

# Test 1
#with open('att48.in', 'r') as file:
#    linija = file.readlines()
# Test 2
with open('bayg29.in', 'r') as file:
    linija = file.readlines()
# Test 3
#with open('eil101.in', 'r') as file:
#    linija = file.readlines()
# Test 4
#with open('gr24.in', 'r') as file:
#    linija = file.readlines()
# Test 5
#with open('ulysses16.in', 'r') as file:
#    linija = file.readlines()

broj_poslova = int(linija[0])

matrica_udaljenosti = []
for i in range(1, broj_poslova + 1):
    matrica_udaljenosti.append(list(map(int, linija[i].split())))

matrica_vremena = []
for i in range(broj_poslova + 1, broj_poslova * 2 + 1):
    matrica_vremena.append(list(map(int, linija[i].split())))

print("Broj poslova =", broj_poslova)
print("Matrica udaljenosti =", matrica_udaljenosti)
print("Matrica vremena =", matrica_vremena)

najbolje_resenje = genetski_algoritam(broj_poslova, matrica_udaljenosti, matrica_vremena)

PROSECNI_TROSAK_FUNKCIJE = PROSECNI_TROSAK_FUNKCIJE / BROJ_GENERACIJA

print("Najbolji trosak funkcije: ", NAJMANJI_TROSAK_FUNKCIJE)
print("Prosecni trosak funkcije: ", PROSECNI_TROSAK_FUNKCIJE)
print("Najbolje resenje:", najbolje_resenje)
