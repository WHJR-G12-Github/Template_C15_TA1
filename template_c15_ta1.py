import pygame, sys,random
import neat

pygame.init()
clock=pygame.time.Clock()

screen = pygame.display.set_mode((400,600))
images={}
images["bg1"] = pygame.image.load("bg1.png").convert_alpha()
images["base"] = pygame.image.load("base.png").convert_alpha()
images["bird"] = pygame.image.load("bird.png").convert_alpha()
images["pipe"] = pygame.image.load("pipe.png").convert_alpha()
images["invertedpipe"]=pygame.transform.flip(images["pipe"], False, True)
gen=0


class Bird:
    bird=pygame.Rect(100,250,30,30)
    speed=0
    gravity=0.5
    def moveup(self):
        self.speed=0
        self.speed=-10
    def movedown(self):
        global speed
        self.speed+=self.gravity
        self.bird.y +=self.speed
    def display(self):
        screen.blit(images["bird"],self.bird)
class Pipe:
    def __init__(self,x):
        self.height=random.randint(150, 400)
        self.tpipe=pygame.Rect(x,self.height-400,40,300)
        self.bpipe=pygame.Rect(x,self.height+100,40,300)
    def move(self):
        self.tpipe.x-=4
        self.bpipe.x-=4
        if self.tpipe.x<-40:
            self.tpipe.x=450
            self.bpipe.x=450
            self.height=random.randint(150, 400)
            self.tpipe.y=self.height-400
            self.bpipe.y=self.height+100
    def display(self):
        screen.blit(images["pipe"],self.bpipe)
        screen.blit(images["invertedpipe"],self.tpipe)
    

def eval_fitness(generation, config):
    global gen
    birdcount=0
    gen = gen+1
   
    for gid, genome in generation: 
        # Create a neural network using 'neat' library and pass 'genome' , 'config' as arguments. Naming it as 'net'
        
        pipe1 = Pipe(250)
        bird1 = Bird() 
        
        score_font=pygame.font.Font('freesansbold.ttf', 20)       
        groundx=0
        state="play"
        bird1.bird.y=200 
        
        while True:
            screen.fill((50,150,255))
            screen.blit(images["bg1"],[0,0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird1.moveup()
                        
                 
            pipe1.display()
            bird1.movedown()
            bird1.display()
            if bird1.bird.colliderect(pipe1.bpipe) or bird1.bird.colliderect(pipe1.tpipe) or bird1.bird.y > 600 or bird1.bird.y < 0:
                state="over"
            
                
            if groundx < -330:
                groundx=0
            if state=="play":
                groundx-=5
                pipe1.move()
                
           
       
            # Calculate 'output' by passing 'bird1.bird.y','pipe1.height' as inputs
            
            # Decision Making
            # Check if 'output[0]' is greater than 0.5 and making the bird moveup
            
                
               
            if state=="over":
               state="play"
               birdcount+=1
               break
            
            screen.blit(images["base"],[groundx,550])
            score_text=score_font.render("Gen:"+str(gen)+" Genome:"+str(birdcount), True, (0,0,255)) 
            screen.blit(score_text,[10,10])
           
            pygame.display.update()
            clock.tick(30)

    


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,'config-feedforward.txt')  
p = neat.Population(config)
p.run(eval_fitness,7) 


  

  
    
