#voor de visualisatie wordt de module pygame gebruikt. Hiermee kan een nieuw window worden geopend en kan de data hierop geplot worden.
#voor de documentatie van pygame volg deze link: https://www.pygame.org/docs/ 
import pygame
import pandas as pd
from math import sin, cos, pi

#hieronder worden de standaard onderdelen van pygame aangeroepen. de WIN is het window van pygame waar alles op geplot kan worden.
pygame.init()
WIN = pygame.display.set_mode((400,400))            #aanmaken van een window met afmetingen
pygame.display.set_caption('bee path generation')   #titel van de window

#*** settings
draw_path_enabled = False
draw_bee_enabled = True
#***

bee_image = pygame.image.load("Project_offline\movement_paterns/bee.png")
bee_image = pygame.transform.rotate(bee_image,-90)
bee_image_width,bee_image_heigth = bee_image.get_size()


#het inlezen van de gegenereerde data
generated_paths = pd.read_csv(r'Project_offline\movement_paterns\generated_path.csv')

#hieronder wordt de dataset opgedeeld per bij id. 
generated_path_per_bee = []
for bee in range(max(generated_paths.bee_id)):
    generated_path_per_bee.append(generated_paths[generated_paths.bee_id == bee+1].values.tolist())

# hier worden een aantal constanten aangemaakt voor de kleuren van de paden van de bijen. 
start_color = (100,0,0) #Rood
end_color = (0,100,0)   #Groen
colors = []

for i in range(len(generated_path_per_bee[0])): #deze loop zorgd dat de lijst 'colors' wordt gevuld met de kleuren tussen de start en end color.
    deel = (i+1)/len(generated_path_per_bee[0])
    R_dif, G_dif, B_dif = start_color[0]-end_color[0], start_color[1]-end_color[1], start_color[2]-end_color[2]
    colors.append((int(start_color[0]-deel*R_dif),int(start_color[1]-deel*G_dif),int(start_color[2]-deel*B_dif)))

#hierna de funcie om het één path te tekenen. de lengte van het path is afhankelijk van de frame die word laten zien.
def draw_path(frame,path):
    for i in range(frame):
        pygame.draw.line(WIN,colors[i],(path[i][0],path[i][1]),(path[i+1][0],path[i+1][1]))

def draw_bee(frame,bee_index):
    temp_bee_image = pygame.transform.rotate(bee_image,generated_path_per_bee[bee_index][frame][2]*-1)

    x = generated_path_per_bee[bee_index][frame][0]
    y = generated_path_per_bee[bee_index][frame][1]
    rotation = generated_path_per_bee[bee_index][frame][2]

    x = x-(abs(sin(rotation/360*2*pi)*bee_image_heigth)+abs(cos(rotation/360*2*pi)*bee_image_width))/2
    y = y-(abs(cos(rotation/360*2*pi)*bee_image_heigth)+abs(sin(rotation/360*2*pi)*bee_image_width))/2

    WIN.blit(temp_bee_image,(x,y))

def main():
    run = True  #zolang als run waar is, wordt de loop uitgevoerd.
    FPS = 10    #het maximale aantal frames per seconde dat wordt laten zien.(aantal keer dat de while loop gestart kan worden elke seconde)
    clock = pygame.time.Clock()
    frame = 0

    # hierna de main loop. zolang als de mainloop actief is, wordt het window van pygame geupdate. 
    while run:
        clock.tick(FPS)
        # door de volgende loop werkt de afsluitknop van de window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # elk frame wordt begonnen met het zwart maken van de achtergrond.
        WIN.fill((255,255,255))

        #hierna worden de paden van elke bij getekent.
        if draw_path_enabled:
            for path in generated_path_per_bee:
                draw_path(frame,path)
        
        if draw_bee_enabled:
            for i in range(len(generated_path_per_bee)):
                draw_bee(frame,i)


        #tot slot wordt het huidige frame geupdate.
        frame += 1
        if frame >= len(generated_path_per_bee[0]):
            frame = 0

        #pas als alles op de window is gezet wordt het met deze functie daadwerkelijk geupdate op het window.
        pygame.display.update()

    # zodra de while loop stopt wordt hier het scherm afgesloten.
    pygame.quit()

main()
