#!/usr/bin/python3.5

import random

class Block():
 
    def __init__(self, index, données, somme_précédente, nonce):
        self._index = index
        self._données = données
        self._somme_précédente = somme_précédente
        self._nonce = nonce
        self.màj()

    def màj(self):
        self._somme = hash(str(self.index) + str(self.données) + str(self.somme_précédente) + str(self.nonce))        

    def _get_index(self):
        return(self._index)

    def _set_index(self, nindex):
        self._index = nindex
        self.màj()

    def _get_données(self):
        return(self._données)

    def _set_données(self, ndonnées):
        self._données = ndonnées
        self.màj()

    def _get_somme_précédente(self):
        return(self._somme_précédente)

    def _set_somme_précédente(self, nsomme_précédente):
        self._somme_précédente = nsomme_précédente
        self.màj()

    def _get_nonce(self):
        return(self._nonce)

    def _set_nonce(self, nnonce):
        self._nonce = nnonce
        self.màj()

    def _get_somme(self):
        return(self._somme)

    def _set_somme(self, nsomme):
        self._somme = nsomme
        self.màj()

    index = property(_get_index, _set_index)
    données = property(_get_données, _set_données)
    somme_précédente = property(_get_somme_précédente, _set_somme_précédente)
    nonce = property(_get_nonce, _set_nonce)
    somme = property(_get_somme, _set_somme)

    def données_utiles(self):
        données_liste = []
        for p in range(len(self.données)):
            if self.données[p] == "[":
                d = p
            if self.données[p] == ":":
                cf = p
            if self.données[p] == "]":
                données_liste.append([])
                données_liste[-1].append(self.données[d+1: cf])
                arguments = []
                liste_arguments = list(self.données[cf+1: p])
                while "," in liste_arguments:
                    arguments.append("".join(liste_arguments[:liste_arguments.index(",")]))
                    for x in range(liste_arguments.index(",")+1):
                        del liste_arguments[0]
                données_liste.append(arguments)
                return(données_liste)


class BlockChain():

    def __init__(self, règles, commandes):
        self.chaine = [Block(0, (règles, commandes), 0, 0)]
        self.règles = règles
        self.commandes = commandes

    def règles_respectées(self, block):
        for i in self.règles:
            if i(self, block) == False:
                return(False)
        return(True)

    def ajouterHASH(self, block):
        if not self.règles_respectées(block):
            return(False)
        print("Block n°{} ajouté avec succès".format(block.index))
        self.chaine.append(block)
        return(True)

    def carnet(self, longueur = 0):
        if longueur == 0:
            longueur = len(self.chaine)
        carnet = {}
        for i in self.données_utiles():
            for c in self.commandes:
                if c.__name__ == i[0]:
                    break
            carnet = c(carnet, i[1])
        return(carnet)

    def lire(self):
        for i in self.chaine:
            données = i.données
            print("\n\n\n----------\nBlock n°{}\n----------\n{}\n\nsomme_précédente = {}\nsomme = {}\n\n".format(i.index, i.données, i.somme_précédente, i.somme))

    def données_utiles(self, longueur = 0):
        if longueur == 0:
            longueur = len(self.chaine)
        liste_données = []
        for i in self.chaine[1:longueur]:
            liste_données.append(i.données_utiles())

        return(liste_données)


class Mineur():

    def __init__(self, nom):
        self.nom = nom

    def rajouter(self, blockchain, données):
        données += """[AJOUTERMONNAIE:{},20,]""".format(self.nom)
        bc = blockchain.chaine[-1]
        block = Block(bc.index+1, données, bc.somme, 1000000)
        print(block.somme)
        if self.vérifier(blockchain, block):
            self.miner(blockchain, block)

    def vérifier(self, blockchain, block):
        for i in blockchain.règles[1:]:
            if i(blockchain, block) == False:
                return(False)
            return(True)

    def miner(self, blockchain, block):
        while True:
            nonce = random.randint(1000000, 9999999)
            block.nonce = nonce
            print(block.somme)
            if blockchain.ajouterHASH(block):
                break



def r1(blockchain, block):
    if str(block.somme)[0:3] != "555":
        return(False)

def r2(blockchain, block):
    if block.index != blockchain.chaine[-1].index + 1:
        return(False)

def r3(blockchain, block):
    if block.somme_précédente != blockchain.chaine[-1].somme:
        return(False)

def r4(blockchain, block):
    if block.somme != hash(str(block.index) + str(block.données) + str(block.somme_précédente) + str(block.nonce)):
        return(False)

def r5(blockchain, block):
    if blockchain.carnet():
        pass

def r6(blockchain, block):
    pass

def r7(blockchain, block):
    pass
                    
Règles = [r1, r2, r3, r4, r5, r6, r7]


def AJOUTERHASH(carnet, arguments):
    """AJOUTERHASH(receveur, objet)"""
    if not arguments[0] in carnet:
        carnet[arguments[0]] = {"sommes" : []}
    carnet[arguments[0]]["sommes"].append(arguments[1])
    return(carnet)

def AJOUTERMONNAIE(carnet, arguments):
    """AJOUTERMONNAIE(receveur, objet)"""
    if not arguments[0] in carnet:
        carnet[arguments[0]] = {"monnaie" : 0}
    carnet[arguments[0]]["monnaie"] += int(arguments[1])
    return(carnet)

def DONNERHASH(carnet, arguments):
    """DONNERHASH(donneur, receveur, objet)"""
    if not arguments[0] in carnet:
        print("le donneur n'existe pas")
        return ValueError
    if not arguments[2] in carnet[arguments[0]]["sommes"]:
        print("le donneur ne peut pas donner la somme")
        return ValueError
    carnet[arguments[0]]["sommes"].remove(arguments[2])
    carnet = AJOUTERHASH(carnet, [arguments[1], arguments[2]])
    return(carnet)


Commandes = [AJOUTERHASH, AJOUTERMONNAIE, DONNERHASH]




#forme  =  "[commande:(argument,argument,...,argument,)]" (bien mettre la virgule à la fin et pas d'espaces)


def insérer(string1, string2, position):
    return(string1[:position+1] + string2 + string1[position+1:])

BC = BlockChain(Règles, Commandes)
Steve = Mineur("Steve")
