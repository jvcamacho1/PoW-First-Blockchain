
import pickle
from hashlib import sha256
from datetime import datetime
import os
import random  
import string
import time

class block:
    def __init__(self, index, timestamp, data, previousHash = '', nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = nonce
        self.hash = self.CalculateHash()
        
    #Calcula o hash do bloco, que está em formato de uma string de tupla
    def CalculateHash(self):
        block = '{}:{}:{}:{}:{}'.format(
            self.index, self.timestamp, self.data, self.previousHash, self.nonce
        )
        return sha256(block.encode()).hexdigest()

    #Minera novos blocos
    def MineBlock(self, difficulty):
        while(self.hash[0:difficulty] != '0'*difficulty):
            self.nonce +=1
            self.hash = self.CalculateHash()

        print("block mined: " + self.hash)


class BlockChain:
    def __init__(self):
         #Verifica se a blockchain está presente nos objetos da memória ou no arquivo, e inicia a blockchain
        if os.path.exists('chain.pkl'):
             try:
                 self.GetChain()
                 self.dificulty = 1
             except:
                print("Algum erro aconteceu")
        else:
            try:
                self.chain = [self.GenesisBlock()]
                self.dificulty = 1
            except:
                print("Erro ao criar bloco Genesis")
    
    def GenesisBlock(self):
        return block(0,datetime.fromtimestamp(datetime.utcnow().timestamp()), 'Genesis block','0')
        
    #Verifica se a blockchain está presente nos objetos da memória ou no arquivo, e pega o ultimo bloco
    def LatestBlock(self):
        if os.path.exists('chain.pkl'):
            try:
                self.GetChain()
                return self.chain[-1]
            except:
                print("Erro ao buscar ultimo bloco")
        else:
            return self.chain[-1]
    
    #Verifica se a blockchain está presente nos objetos da memória ou no arquivo, verifica sua validade e tenta adionar um novo bloco
    def addBlock(self,block):
        if os.path.exists('chain.pkl'):
            if(self.chainValid()):
                try:
                    self.GetChain()
                    block.previousHash = self.LatestBlock().hash
                    block.MineBlock(self.dificulty)
                    self.chain.append(block)
                    self.SetChain()
                except:
                    print("Erro ao adicionar bloco a")
            else:
                print("Blockchain invalida 1")
        else:
            try:
                if(self.chainValid()):
                    block.previousHash = self.LatestBlock().hash
                    block.MineBlock(self.dificulty)
                    self.chain.append(block)
                    self.SetChain()
                else:
                    print("Blockchain invalida 2")
            except:
                print("Erro ao adicionar bloco")

    #Esta função pega os valores salvos da blockchain no arquivo e os adiciona no objeto chain
    def GetChain(self):
        if os.path.exists('chain.pkl'):
            with open('chain.pkl', 'rb') as inp:
                self.chain = pickle.load(inp)
        else:
            print("Nenhuma blockchain encontrada")

    #Esta função pega os valores que estao no objeto e os salva no arquivo
    def SetChain(self):
        try:
            with open('chain.pkl', 'wb') as outp:
                pickle.dump(self.chain, outp, pickle.HIGHEST_PROTOCOL)
        except:
            print("Algo de errado aconteceu ao salvar a blockchain ao arquivo")

    #Verifica se a blockchain está presente nos objetos da memória ou no arquivo e checa se todos blocos são validos
    def chainValid(self):
        if os.path.exists('chain.pkl'):
            try:
                self.GetChain()
                for i in range(1,len(self.chain)):
                    currentlblock = self.chain[i]
                    previousblock = self.chain[i-1]

                    if currentlblock.hash != currentlblock.CalculateHash():
                        return False
                    if currentlblock.previousHash != previousblock.hash:
                        return False
                return True
            except:
                return False
        else:
            try:
                for i in range(1,len(self.chain)):
                    currentlblock = self.chain[i]
                    previousblock = self.chain[i-1]

                    if currentlblock.hash != currentlblock.CalculateHash():
                        return False
                    if currentlblock.previousHash != previousblock.hash:
                        return False
                return True
            except:
                return False

    #Verifica se a blockchain está presente nos objetos da memória ou no arquivo e printa na tela
    def GetValuesChain(self):
        if os.path.exists('chain.pkl'):
            try:
                self.GetChain()
                for i in range(0,len(self.chain)):
                    print(self.chain[i].index,self.chain[i].timestamp,self.chain[i].data,self.chain[i].previousHash)
            except:
                print("Algo de errado aconteceu ao printar os dados dos arquivos de blockchain")
        else:
            try:
                for i in range(0,len(self.chain)):
                    print(self.chain[i].index,self.chain[i].timestamp,self.chain[i].data,self.chain[i].previousHash)
            except:
                print("Algo de errado aconteceu ao printar os dados da blockchain")

BROCK = BlockChain()

print("Esta blockchain apenas salva Strings, para fins de testes serão geradas strings aleatorias")

inicio = time.time()
for i in range(0,10):
    print("mineirando bloco:",i)
    result = ''.join((random.choice(string.ascii_uppercase) for x in range(5)))
    BROCK.addBlock(block(i, datetime.fromtimestamp(datetime.utcnow().timestamp()), result ))
fim = time.time()
BROCK.GetValuesChain()
print("A blockchain é valida:", BROCK.chainValid())
print(fim-inicio)