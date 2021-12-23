#!/usr/bin/python3
import random as R
import os


class GenerateKeys():
    def __init__(self,keylenght, verborse=False):
        self.keylenght = keylenght
        self.numberschar="0123456789"
        if os.getgid() != 0:
            print("[!] Run as sudo")
            #exit(2)
        if not self.pull():
            self.GetNumber()
        if verborse:
            self.verborse()

    def pull(self):
        ac = [i.rstrip() for i in  open("/etc/mucahit.conf","r").readlines()]
        alindi = 0
        for satir in ac:
            if "D" in satir:
                self.D = int(satir.split("=")[1])
                alindi += 1
            elif "N" in satir:
                self.N = int(satir.split("=")[1])
                alindi += 1
            elif "E" in satir:
                self.E = int(satir.split("=")[1])
                alindi += 1
        if alindi != 3:
            print("D,N,E degerlerin tumu okunamadi")
        else:
            print("okuma basari ile gerceklestirildi")
        return True


    def save(self):
        ac = open("/etc/mucahit.conf","r+") 
        ac.seek(0)
        ac.write(f"D={gen.D}\nN={gen.N}\nE={gen.E}")
        ac.close()

    def calc_d(self,e, phi):
        d_old = 0; r_old = phi
        d_new = 1; r_new = e
        while r_new > 0:
            a = r_old // r_new
            (d_old, d_new) = (d_new, d_old - a * d_new)
            (r_old, r_new) = (r_new, r_old - a * r_new)
        return d_old % phi if r_old == 1 else None



    def CreateNumber(self,sayi:int):
        return int(R.choice(self.numberschar[1:]) + "".join([ R.choice(self.numberschar)  for _ in range(sayi-1)]))

    def ebob(self,sayi0:int,sayi1:int):
        while True:
            k = sayi0 % sayi1
            if k == 0:
                ortak = sayi1
                break
            else:
                sayi0 = sayi1
                sayi1 = k
        return ortak

    def AAsal(self,sayi0,sayi1):
        return self.ebob(sayi0,sayi1) == 1


    def GetNumber(self):
        print("Generating Numbers, please wait...")
        while True:
            sayi1=self.CreateNumber(self.keylenght)
            sayi2=self.CreateNumber(self.keylenght)
            if self.AAsal(sayi1,sayi2):
                break
        print("Number was generated successfully!")
        self.magic_numbers = [sayi1,sayi2, sayi1*sayi2,(sayi1-1) * (sayi2 - 1)]
        self.fien = self.magic_numbers[3]
        self.GetE(self.fien)
        self.D = self.calc_d(self.E,self.fien)
        self.N = self.magic_numbers[2]

    def GetE(self,fien):
        print("Generating E, please wait...")
        while True:
            e = R.randint(int((fien/40)-(fien*0.01)),int(fien/40))
            if self.AAsal(fien,e):
                break
        print("Number was generated successfully!")
        self.E = e


    def verborse(self):
        print(f"N = {self.N}")
        print(f"E = {self.E}")
#        print(f"D = {self.D}")


class cryptor():
    def encryptor(self,e,n,mesaj:str):
        emsg = ""
        for i in mesaj:
            cmsg = ord(i)
            emsg += str((cmsg**e)%n) + " "
        return emsg[:-1]


    def decryptor(self,d,n,message:str):
        cmsg = ""
        for i in message.split(" "):
            sayi = int(i) ** d % n
            try:
                cmsg += chr(sayi)
                print(f"[DEBUG] {chr(sayi)}")
            except:
                continue

        print(cmsg)
        return cmsg

gen = GenerateKeys(3,True)
cr = cryptor()
metinim = "bu metin şifrelenip deşifrelenecek, sadece çalıştır ve izle, さようなら"
sifreli = cr.encryptor(gen.E,gen.N,metinim)
desifreli = cr.decryptor(gen.D,gen.N,sifreli)

