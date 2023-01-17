import math
from random import randint, uniform
import pandas as pd

AMOUNT_OF_BEES = [4,    #random_moving_bees
                  1,    #slow_moving_bees
                  0,    #inside_moving_bees
                  0     #outside_moving_bees
                 ] 
AMOUNT_OF_MOVES = 200
BORDER_RADIUS = 200 #not all code is ready to change this!


class Bee:
    def check_border(self): #ckeck of de bij de grens overschrijd
        if ((self.pos[0]-BORDER_RADIUS)**2 + (self.pos[1]-BORDER_RADIUS)**2)**0.5 > BORDER_RADIUS:               #als de bij buiten een circle met straal BORDER_RADIUS van het midden komt.
            if self.pos[0] > BORDER_RADIUS:                                                                         #als self.pos is groter dan BORDER RADIUS : rechter half van het scherm
                angle = math.degrees(math.atan((self.pos[1]-BORDER_RADIUS)/(self.pos[0]-BORDER_RADIUS)))                #hoek van de bij ten opzichte van het midden voor de rechter helft van het scherm
            elif self.pos[0] < BORDER_RADIUS:                                                                       #als self.pos is kleiner dan BORDER RADIUS : linker half van het scherm
                angle = math.degrees(math.atan((self.pos[1]-BORDER_RADIUS)/(self.pos[0]-BORDER_RADIUS)))+180            #hoek van de bij ten opzichte van het midden voor het linker helft van het scherm
        
            else:                                                                                                   #als x pos is precies BORDER_RADIUS 
                if self.pos[1] < BORDER_RADIUS:                                                                         #als de y pos is kleiner dan BORDER_RADIUS
                    angle = 270                                                                                             
                else:                                                                                                   #als de y pos is groter dan BORDER_RADIUS
                    angle = 90

            #De bij wordt terug op de circle gezet. dit wordt gedaan dmv de angle die het is berekent. 
            pos_on_circle = (math.cos(math.radians(angle))*(BORDER_RADIUS-0)+BORDER_RADIUS,math.sin(math.radians(angle))*(BORDER_RADIUS-10)+BORDER_RADIUS)

            #als de angle precies 90 of 270 is, word de pos_on_circle vast gezet omdat de berekening dit niet precies kan uitrekenen. 
            if angle == 90:
                pos_on_circle = (BORDER_RADIUS,BORDER_RADIUS*2)

            elif angle == 270:
                pos_on_circle = (BORDER_RADIUS,0)
            
            #in het volgende stuk worden de de uiteindelijke positie en rotatie uitgerekent.
            # afhankelijk van de hoek moet de bij naar rechts of links afslaan. hiervoor is de hoek met de kleinste aanpassing gekozen.
            if self.rotation < angle: 
                self.pos = (pos_on_circle[0]+(math.cos(math.radians(angle-90))*self.speed),pos_on_circle[1]+(math.sin(math.radians(angle-90))*self.speed))
                self.rotation = int(angle-90)

            elif self.rotation > angle: 
                self.pos = (pos_on_circle[0]+(math.cos(math.radians(angle+90))*self.speed),pos_on_circle[1]+(math.sin(math.radians(angle+90))*self.speed))
                self.rotation = int(angle+90)

    def change_rotation(self): #E = 0, S = 90, W = 180, N = 270
        self.rotation += randint(-self.turn_speed,self.turn_speed)

    def change_speed(self):
        self.speed += uniform(-self.accelaretion,self.accelaretion)
        self.speed += (self.avarege_speed - self.speed)/20

    def move(self):
        #In deze functie word de bij verplaatst. Dit wordt in twee simpele stappen gedaan:
        #   1) het verplaatsen van de bij aan de hand van de snelheid en de rotatie.
        #   2) het veranderen van de rotatie voor de volgende stap.  
        if self.speed > 0:
            self.pos = (self.pos[0]+self.speed*math.cos(math.radians(self.rotation)),self.pos[1]+self.speed*math.sin(math.radians(self.rotation)))
        #Hier word de border check uitgevoerd.
        self.check_border()

        self.change_rotation()
        self.change_speed()

        #tot slot wordt de stap opgeslagen in de lijst. hiervoor worden x positie, y positie, rotatie en id opgeslagen
        self.path[0].append(self.pos[0])
        self.path[1].append(self.pos[1])
        self.path[2].append(self.rotation)
        self.path[3].append(self.id)
    
    def smoothen(self):
        for feature in range(2): # x and y cordinates
            for frame in range(len(self.path[0])-2):
                point_A = self.path[feature][frame]
                point_C = self.path[feature][frame+2]

                new_point_B = ((point_A+point_C)//2)
                self.path[feature][frame+1] = new_point_B


class slow_moving_bee(Bee):
    def __init__(self,pos,id):
        self.pos = pos #(x,y)
        self.id = id # int(n)
        self.rotation = randint(0,360) #degrees:  East = 0, clockwise
        
        self.avarege_speed = 5 #pix/frame
        self.speed = 0 #startspeed 
        self.turn_speed = 30 #max degrees/frame
        self.accelaretion = 0.8 #pix/frame^2

        self.path = [[self.pos[0]],[self.pos[1]],[self.rotation],[self.id]]

class random_moving_bee(Bee):
    def __init__(self,pos,id):
        self.pos = pos #(x,y)
        self.id = id # int(n)
        self.rotation = randint(0,360) #degrees:  East = 0, clockwise
        
        self.avarege_speed = 6 #pix/frame
        self.speed = 0 #startspeed 
        self.turn_speed = 30 #max degrees/frame
        self.accelaretion = 0.8 #pix/frame^2

        self.path = [[self.pos[0]],[self.pos[1]],[self.rotation],[self.id]]
        

#hier worden AMOUNT_OF_BEES geinitialiseerd
bees = []
for i in range(len(AMOUNT_OF_BEES)):
    for ii in range(AMOUNT_OF_BEES[0]):
        bees.append(random_moving_bee((201,201),ii+1))
    for ii in range(AMOUNT_OF_BEES[1]):
        bees.append(slow_moving_bee((201,201),ii+1+AMOUNT_OF_BEES[0]))
    #for ii in range(AMOUNT_OF_BEES[2]):
    #    bees.append(random_moving_bee((201,201),ii+1))
    #for ii in range(AMOUNT_OF_BEES[3]):
    #    bees.append(random_moving_bee((201,201),ii+1))

#Hier worden voor elke bij AMOUND_OF_MOVES gezet.
for i in range(AMOUNT_OF_MOVES):
    for bee in bees:
        bee.move()
        if i == AMOUNT_OF_MOVES-1:
            bee.smoothen()

#Tot slot wordt de gegenereerde data in een .csv bestand opgeslagen. 
generated_paths = [[],[],[],[]]
labels = [[],[]]
for i in range(sum(AMOUNT_OF_BEES)):
    if i < AMOUNT_OF_BEES[0]:
        movement_pattern = 0
        labels = [labels[0] + [1],labels[1] + [0]]
    elif i < AMOUNT_OF_BEES[0]+AMOUNT_OF_BEES[1]:
        movement_pattern = 1
        labels = [labels[0] + [0],labels[1] + [1]]

    generated_paths = [generated_paths[0] + bees[i].path[0], generated_paths[1] + bees[i].path[1], generated_paths[2] + bees[i].path[2], generated_paths[3] + bees[i].path[3]]
    

generated_paths = pd.DataFrame({"x_position"        : generated_paths[0],
                                "y_position"        : generated_paths[1],
                                "rotation"          : generated_paths[2],
                                "bee_id"            : generated_paths[3]})

labels = pd.DataFrame({"Class 1"  : labels[0],
                       "Class 2"  : labels[1]})

generated_paths.to_csv(r'Project_offline\movement_paterns\generated_path.csv', index=False)
labels.to_csv(r'Project_offline\movement_paterns\labels.csv', index=False)


