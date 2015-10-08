import pygame,sys
from pygame.locals import *
from random import randint
#Variables Globales
ancho=900
alto=480
listaEnemigos=[]
#clase nave espacial
#AGREGUE ALGO


### probando el cambio
#probando otro nuevo cambio
class naveEspacial(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                #atributos
                self.ImagenNave=pygame.image.load("Pictures\hunter.png")
                self.ImagenExplosion=pygame.image.load("Pictures\java2.png")
                self.rect=self.ImagenNave.get_rect()
                self.rect.centerx=ancho/2
                self.rect.centery=alto-30
                self.listaDisparo=[]
                self.Vida=True
                self.velocidad=20
                self.sonidoDisparo=pygame.mixer.Sound("Laser - Efecto de Sonido.ogg")
                self.sonidoExplosion=pygame.mixer.Sound("Laser - Efecto de Sonido.ogg")
                print self.rect


        def movimientoDerecha(self):
                self.rect.right+=self.velocidad
                self.__movimiento()
        def movimientoIzquierda(self):
                self.rect.right-=self.velocidad
                self.__movimiento()
                
        def __movimiento(self):
            if self.Vida==True:
                if self.rect.left <=0:
                    self.rect.left =0
                elif self.rect.right>870:
                    self.rect.right=869
       
        def disparar(self,x,y):
                miProyectil=Proyectil(x,y,"Pictures\disparo.png",True)
                self.listaDisparo.append(miProyectil)
                self.sonidoDisparo.play()
            
                
        def dibujar(self,superficie):#se dibujara si misma
                superficie.blit(self.ImagenNave,self.rect)

        def destruccion(self):
                self.sonidoExplosion.play()
                self.Vida=False
                self.velocidad=0
                self.ImagenNave=self.ImagenExplosion
                
        
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imagenProyectil= pygame.image.load(ruta)
        self.rect=self.imagenProyectil.get_rect()
        self.velocidadDisparo=2
        self.rect.top=posy
        self.rect.left=posx
        self.disparoPersonaje=personaje    

    def trayectoria(self):
        if self.disparoPersonaje==True:
                self.rect.top=self.rect.top - self.velocidadDisparo
                
        else:
                self.rect.top=self.rect.top + self.velocidadDisparo
                
    def dibujar(self,superficie):
        superficie.blit(self.imagenProyectil,self.rect)
        
class Invasor(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagenUno,imagenDos):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA= pygame.image.load(imagenUno)
        self.imagenB= pygame.image.load(imagenDos)
        self.listaImagenes=[self.imagenA,self.imagenB]
        self.posImagen=0 #para que arranque desde 0 la lista
        self.imagenInvasor=self.listaImagenes[self.posImagen]
        self.rect=self.imagenInvasor.get_rect()
        self.listaDisparo=[]
        self.velocidad=5
        self.rect.top=posy
        self.rect.left=posx
        self.tiempoCambio=1
        self.conquista=False
        self.rangoDisparo=2
        self.derecha=True
        self.contador=0
        self.MaxDescenso=self.rect.top+40
        self.limiteDerecha=posx+distancia
        self.limiteIzquierda=posx-distancia
   
    def dibujar(self,superficie):
        self.imagenInvasor=self.listaImagenes[self.posImagen]
        superficie.blit(self.imagenInvasor,self.rect)

    def comportamiento(self,tiempo):
            if self.conquista==False:
                self.__movimiento()
                self.__ataque()
                if self.tiempoCambio==tiempo: 
                        self.posImagen+=1
                        self.tiempoCambio+=1
                        if self.posImagen >len(self.listaImagenes)-1:
                                self.posImagen=0
    def __ataque(self):
            if(randint(0,100)<self.rangoDisparo):
                self.__disparo()
    def __disparo(self):
            x,y=self.rect.center
            miProyectil=Proyectil(x,y,"Pictures\disparo2.png", False)
            self.listaDisparo.append(miProyectil)
    def __movimiento(self):
            if self.contador<3:
                    self.__movimientoLateral()
            else:
                    self.__descenso()
    def __descenso(self):
            if self.MaxDescenso==self.rect.top:
                    self.contador=0
                    self.Maxdescenso=self.rect.top+40
            else:
                    self.rect.top+=1
    def __movimientoLateral(self):
            if self.derecha==True:
                    self.rect.left=self.rect.left+self.velocidad
                    if self.rect.left > self.limiteDerecha:
                            self.derecha=False
                            self.contador+= 1
            else:
                    self.rect.left=self.rect.left-self.velocidad
                    if self.rect.left<self.limiteIzquierda:
                            self.derecha=True
def detenerTodo():
        for enemigo in listaEnemigos:
                for disparo in enemigo.listaDisparo:
                        enemigo.listaDisparo.remove(disparo)
                enemigo.conquista=True
                          
def cargarEnemigos():
        posx=100
        for x in range(1,5):
                enemigo=Invasor(posx,50,40,'Pictures\marciano.png','Pictures\marcianoB.png',)
                listaEnemigos.append(enemigo)
                posx=posx+200
        posx=100
        for x in range(1,5):
                enemigo=Invasor(posx,0,40,'Pictures\marciano.png','Pictures\marcianoB.png',)
                listaEnemigos.append(enemigo)
                posx=posx+200
        posx=100
        for x in range(1,5):
                enemigo=Invasor(posx,100,40,'Pictures\marciano.png','Pictures\marcianoB.png',)
                listaEnemigos.append(enemigo)
                posx=posx+200
        
def SpaceInvader():
        pygame.init ()
        ventana = pygame.display.set_mode((ancho,alto)) #objeto ventana, set mode superficie
        pygame.display.set_caption("Space Invader") #set caption mensaje a la superficie

        ImagenFondo=pygame.image.load("Pictures\Fondo.png")
        pygame.mixer.music.load("Nivel X theme song Full.ogg")
        pygame.mixer.music.play(3) #para decir la cantidad de veces q se va a repetir
        miFuenteSistema=pygame.font.SysFont("Arial",30)
        Texto=miFuenteSistema.render("Fin del Juego",0,(120,100,40))
        jugador = naveEspacial()#mirar esto
        cargarEnemigos()
        #pasa saber si un jugador gano o perdio
        enJuego=True
        reloj=pygame.time.Clock()
#proyectil
#DemoProyectil=Proyectil(ancho/2,alto-30)
        while True:
#jugador.movimiento()
#DemoProyectil.trayectoria()
            reloj.tick(60)
            tiempo=pygame.time.get_ticks()/1000
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if enJuego==True:
                    if evento.type==pygame.KEYDOWN:
                        if evento.key==K_LEFT:
                            jugador.movimientoIzquierda()
                        elif evento.key==K_RIGHT:
                            jugador.movimientoDerecha()
                        elif evento.key==K_s:
                            x,y=jugador.rect.center
                            jugador.disparar(x,y)                                                                                       
            ventana.blit(ImagenFondo,(0,0))
            
#DemoProyectil.dibujar(ventana)
            jugador.dibujar(ventana)
            
            if len(jugador.listaDisparo)>0:
                    for x in jugador.listaDisparo:
                        x.dibujar(ventana)
                        x.trayectoria()
                        if x.rect.top<-10:
                            jugador.listaDisparo.remove(x)
                        else:
                                for enemigo in listaEnemigos:
                                        if x.rect.colliderect(enemigo.rect):
                                                listaEnemigos.remove(enemigo)
                                                jugador.listaDisparo.remove(x)
                                                
            if len(listaEnemigos)>0:
                    for enemigo in listaEnemigos:
                            enemigo.comportamiento(tiempo)
                            enemigo.dibujar(ventana)
                            if enemigo.rect.colliderect(jugador.rect):
                                    jugador.destruccion()
                                    enJuego=False
                                    detenerTodo() #se acaba el juego
                                    
                            if len(enemigo.listaDisparo)>0:
                                    for x in enemigo.listaDisparo:
                                        x.dibujar(ventana)
                                        x.trayectoria()
                                        if x.rect.colliderect(jugador.rect):
                                                jugador.destruccion()
                                                enJuego=False
                                                detenerTodo()

                                        if x.rect.top>900:
                                                enemigo.listaDisparo.remove(x)
                                        else:
                                                for disparo in jugador.listaDisparo:
                                                        if x.rect.colliderect(disparo.rect):
                                                                jugador.listaDisparo.remove(disparo)
                                                                enemigo.listaDisparo.remove(x)
            if enJuego==False:
                    pygame.mixer.music.fadeout(3000)
                    ventana.blit(Texto,(300,300))
            pygame.display.update()
            
SpaceInvader()
