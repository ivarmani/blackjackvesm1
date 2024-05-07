from machine import Pin, SoftI2C, PWM
from I2C_LCD import I2cLcd
from time import sleep_ms
import random
#
p1takki_green = Pin(13, Pin.IN, Pin.PULL_UP)
p1ljos_green = Pin(14, Pin.OUT)
p1takki_red = Pin(2, Pin.IN, Pin.PULL_UP)
p1ljos_red = Pin(1, Pin.OUT)

p2takki_green = Pin(11, Pin.IN, Pin.PULL_UP)
p2ljos_green = Pin(12, Pin.OUT)
p2takki_red = Pin(41, Pin.IN, Pin.PULL_UP)
p2ljos_red = Pin(42, Pin.OUT)

# Skjárinn nota I2C tengingu til að tala við ESP
i2c = SoftI2C(scl=Pin(47), sda=Pin(48), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd2 = I2cLcd(i2c, 0x21, 2, 16)

p1ljos1 = Pin(4, Pin.OUT)
p1ljos2 = Pin(5, Pin.OUT)
p1ljos3 = Pin(6, Pin.OUT)
p1ljos4 = Pin(7, Pin.OUT)
p1ljos5 = Pin(8, Pin.OUT)

p2ljos1 = Pin(9, Pin.OUT)
p2ljos2 = Pin(15, Pin.OUT)
p2ljos3 = Pin(16, Pin.OUT)
p2ljos4 = Pin(17, Pin.OUT)
p2ljos5 = Pin(18, Pin.OUT)

TIGULL = [0x00,0x04,0x0E,0x1F,0x0E,0x04,0x00,0x00]

HJARTA =  [0x00,0x0A,0x1F,0x1F,0x0E,0x04,0x00,0x00]

SPADI = [0x00,0x04,0x0E,0x1F,0x1F,0x0A,0x04,0x0E]

LAUF = [0x04,0x0E,0x15,0x15,0x15,0x0E,0x04,0x0E]


tigulmerki = chr(0)
hjartamerki = chr(1)
spadimerki = chr(2)
laufmerki = chr(3)

lcd.custom_char(0, TIGULL) # chr(0)
lcd.custom_char(1, HJARTA)
lcd.custom_char(2, SPADI)
lcd.custom_char(3, LAUF)

lcd2.custom_char(0, TIGULL) # chr(0)
lcd2.custom_char(1, HJARTA)
lcd2.custom_char(2, SPADI)
lcd2.custom_char(3, LAUF)

class Spil():
    def __init__(self, t, n):
        self.tegund = t
        self.nr = n

    def __str__(self):  # Lætur nafnið á mannspilunum þegar þau eru prentuð
        if self.nr > 9:
            if self.nr == 10:
                nr = "T"
            if self.nr == 11:
                nr = "J"
            elif self.nr == 12:
                nr = "Q"
            elif self.nr == 13:
                nr = "K"
        else:
            nr = str(self.nr)
        return self.tegund+nr

class Spilastokkur():
    def __init__(self):
        self.stokkur = []

    def smidaStokk(self): # Smíðar stokk
        for y in range(4): # Skiptir spilum í tegund
            if y == 0: #
                tegund = f"{hjartamerki}"
            elif y == 1:
                tegund = f"{spadimerki}"
            elif y == 2:
                tegund = f"{tigulmerki}"
            elif y == 3:
                tegund = f"{laufmerki}"
            for x in range(1, 14): # Lætur inn 14 spil af hverri tegund í stokk
                s1 = Spil(tegund, x)
                self.stokkur.append(s1)
        
    
    def gefaSpil(self): # Gefur spil út úr stokk
        randomtala=random.randint(0,len(self.stokkur) - 1)
        return self.stokkur.pop(randomtala)

while True:
    Spila = Spilastokkur()
    Spila.smidaStokk()
    
    p1listi=[]
    p2listi=[]
    
    for i in range(2):
        spil=f"{Spila.gefaSpil()}"
        p1listi.append(spil)
        spil2=f"{Spila.gefaSpil()}"
        p2listi.append(spil2)
    
    while True:
        lcd.move_to(0, 0)
        lcd.putstr(''.join(p1listi))
        lcd.move_to(0, 1)
        lcd.putstr(p2listi[0])

        
        lcd2.move_to(0, 0)
        lcd2.putstr(''.join(p2listi))
        lcd2.move_to(0, 1)
        lcd2.putstr(p1listi[0])
