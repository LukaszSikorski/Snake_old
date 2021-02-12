import pygame, sys,time
import random,time
#Funkcja konczaca gre
def EXIT(game):
    E_font = pygame.font.SysFont("comicsansms", 72)
    game.file.save_scores(game.snake.score)#Zapis pliku
    #game.file.file.close()#Zamkniecie pliku z danymi
    game.screen.fill((0,0,0))#Tlo jest czarne
    game.screen.blit(E_font.render(str(game.snake.score), True, game.colors.red),(300,180))
    pygame.display.flip()#Zamiana buforow
    flag =1
    #Czeka tak dlugo az jaka kolwiek zostanie wcisniety
  #  print(game.snake.my_key)
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                flag=0
    time.sleep(1)
    sys.exit(0)#Koniec aplikacji

#Klasa przechowuje parametry do gry
class Parameters:
    def __init__(self):
        self.offset_heigth=0 #Offset dla piont
        self.offset_width=160 #Offset dla poziomy
        self.snake_size =25 #Rozmiar weza
        self.snake_jump = self.snake_size #Przeskok weza, jak duze
        self.fps=10 #Szybkosc odzwiezania klatek, co ile mS*10
        self.delay_move=40#Co ile mS*10 ruch weza
        self.size_heigth = 500#Rozmiar obszaru do gry pion
        self.size_width = 500#Rozmiar obszaru do gry poziom
        self.faster = 4
class Food:
    def __init__(self):
        self.conf=Parameters()
        #Twprzenie jedzenia o podanych parametrach
        self.body = [pygame.Rect((100,150,self.conf.snake_size,self.conf.snake_size))]
        self.position = [self.body[0].x,self.body[0].y]#Zmienna pomocnicza 

class Snake:
    def __init__(self):
        self.conf = Parameters()#Zmienna conf przechowuje parametry konfiguracyjne gry
        #Dodanie pierwszych trzech elementow weza do ciala
        self.body = [pygame.Rect((100,100,self.conf.snake_size,self.conf.snake_size))]
        self.body.append(pygame.Rect((self.body[0].x,self.body[0].y-self.conf.snake_size,self.conf.snake_size,self.conf.snake_size)))
        self.body.append(pygame.Rect((self.body[1].x,self.body[1].y-self.conf.snake_size,self.conf.snake_size,self.conf.snake_size)))
        self.body_color = (0,255,255)#Kolor weza(Jeszcze nie uzywany)
        self.head = []# [x,y] Zmienna przechowujaca polozenie glowy obecnie
        self.tail = []# [x,y] Zmienna przechowujaca polzenie ogona przed przesunieciem, potrzebne do dodawania ogona po zjedzeniu
        self.my_key = pygame.K_s #Przechowywanie klawisza
        self.score = 0 #Punkty
        #Flaga odpowiedzialna za prawidlowe ruch weza, jesli waz sie dopiero mozna ponownie pobrac
        #klawisz
        self.flag_move=1
      #  self.apple = Food()
        #Metoda odpowiada za poruszanie całego weza oraz jego czesci,
        #czesci poruszaja sie za poprzednikiem
    def move(self):
        #Przesuniecie calego weza w strone glowy
        self.tail =[self.body[-1].x,self.body[-1].y]#Zapisanie polozenia ogona do zmiennej tail
        for ind in reversed(range(1,len(self.body))):
            self.body[ind].x = self.body[ind-1].x
            self.body[ind].y = self.body[ind-1].y
        #Zapisywanie obecnego ogony, potrzebny do metody eat
        #Funckje odpowiedzialne za przesuniecie glowy zaleznego od przycisku
        if self.my_key == pygame.K_d:#Jesli my_key = d to przesun w prawo
            self.body[0].x+= self.conf.snake_size
        elif self.my_key == pygame.K_a:
            self.body[0].x-=self.conf.snake_size
        elif self.my_key == pygame.K_w:
            self.body[0].y -=self.conf.snake_size
        elif self.my_key == pygame.K_s:
            self.body[0].y +=self.conf.snake_size
        #self.colision()#sprawdzanie czy glowa nie uderzyla w przeszkode
        self.head =[self.body[0].x,self.body[0].y]#Zapisanie polozenie glowy do zmiennej head
        self.flag_move=1#Po ruchu mozna dopiera pobrac kolejmy klawisz
    #Metoda sprawdza czy doszlo do kolizji
    def colision(self):
        end =0
        for ind in range(1,len(self.body)):
            #Sprawdzanie czy glowa zrownala sie z czescia ciala
            if self.body[0].x == self.body[ind].x and self.body[0].y == self.body[ind].y:
                end =1#Jesli tak 1
        if self.body[0].x <0 or self.body[0].y<0 or self.body[0].x>=self.conf.size_width or self.body[0].y>=self.conf.size_heigth:
                end =1#Jesli waz wyszedl poza obszar rozgrywki to tez 1
        if end:#Jesli prawda to wyswietl Koniec i zwroc 1
         #   print("Koniec")
            return 1
        else:
            return 0 #Jesli nie doszlo do kolizji lub wyjscia poza obszar to jest ok i zwroc 0
    #Klasa odpowiedzialna za zapis i przetwarzanie plikow z wynikami
class Scores:
    def __init__(self):
        try:
            self.file = open("top5.txt", "r")#Otwieram plik z danymi
            self.tmp = self.file.readlines()#Zapis pliku do tmp
            self.txt = [int(x) for x in (self.tmp)]#Konwersja lini pliku do tablicy int
        #Jezeli plik nie istnieje to stworz tablice z piecioma 0, do tablicy wynikow, w zapisie i tak zostanie
        #stwrzony nowy pusty plik(malo efektywne)
        except:
            #self.file = open("top5.txt", "w+")#Otwieram plik z danymi
            #[self.file.write("{}\n".format(x*0)) for x in range(5)]
            self.txt = [int(x*0) for x in range(5)]
    #Zapis punktow do pliku
    def save_scores(self,x):
        #Sprawdzenie czy punkty weza sa wieksze niz te w pliku
        tmp=0
        #Sprawdzanie czy ktorys ze elementow jest mniejszy od wyniku, jesl tak to zamien go z wynikiem weza
        for y in range(len(self.txt)):
            if self.txt[y] <x:
                tmp =self.txt[y]
                self.txt[y]=x
                x=tmp
        try:
            self.file = open("top5.txt", "w+")#Wymazanie zawartosci pliku
            #Zapis zawartosci tablicy do pliku z nowej lini kazda wartosc
            for val in self.txt:
                self.file.write(str("{}\n".format(val)))
            self.file.close()
        except:
            print("Zmiena prawa dotepu do pliku")

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Snake by Lukasz :)')
        #Tworzenie obiketu font z ustawieniem fontu i wielkosci czcionki
        font = pygame.font.SysFont("comicsansms", 24)
        self.conf = Parameters()#Tworzenie obiekty z parametrami gry
        #Tworzenie okna gry, rozmiar okna jest powiekszony o offset ktory pozwoli mi wypisac punkty zycia i godzine itp.
        self.screen = pygame.display.set_mode((self.conf.size_width+self.conf.offset_width,self.conf.size_heigth+self.conf.offset_heigth))#Tworzenie okna o wymiar 500x500
        self.snake = Snake()#Tworze weza
        self.food = Food()
        self.colors = Colors()
        self.time = 0#Przechowuje czas rozgrywki
        self.seconds = 0
        self.clock = pygame.time.Clock()#Zegar do odpowiedniego synchronizowania
        self.file = Scores()
        timer =[0,0] #0 To move, 1 to renderowanie
        delta=0
        while True:
            delta += self.clock.tick()#Zapisywanie czasu do zmiennej
            self.seconds = time.time()
            self.time += self.clock.get_rawtime()
            #Jesli minie 5 mS to zwieksz kazdy timer o jeden
            if delta >5:#Timer programowy
                timer[0]+=1
                timer[1]+=1
                delta=0
            if timer[0] > self.conf.delay_move: #Jesli czas mod 250 ==0 to rusz weza za pomoca metody
                self.snake.move()#Rusz weza
                if self.snake.colision():
                    #self.file.save_scores(self.snake.score)#Wywolanie zapisu do pliku z punktami weza
                    #self.file.file.close()#Zamkniecie pliku
                    EXIT(self)
                self.eat()#Sprawdz czy dodac punkty
                timer[0]=0#Wyzerowanie timera
            #Wyswietlenie calej grafki
            if timer[1]>self.conf.fps:
                #if delta % self.conf.fps == 0:
                self.screen.fill((0,0,0))#Tlo jest czarne
                #To na dole jest do modyfikacji
                for ind,snak in enumerate(self.snake.body):
                    if ind ==0:#Glowe rysuje osobno, aby zapewnic odmienny kolor
                        pygame.draw.rect(self.screen,(0,0,255),snak)#Rysowanie glowy weza
                    else:
                        pygame.draw.rect(self.screen,(255,150,255),snak)#Rysowanie ciala weza po glowa
                for apple in self.food.body:
                    pygame.draw.rect(self.screen,(255,0,0),apple)#Rysowanie ciala weza po glowa
                #Rysowanie bialej linii ktora oddziela obszar gry od obaszaru napisow
                pygame.draw.line(self.screen,(255,255,255),(self.conf.size_width,0),(self.conf.size_width,self.conf.size_heigth))
                #Wypisywanie ilosci zdobytych punktów
                self.screen.blit(font.render(str("Scories {}".format(self.snake.score)), True, self.colors.red),(self.conf.size_width+5,10))
                #Wypisywanie czasy gry
                self.screen.blit(font.render(str("Time of game"), True, self.colors.white),(self.conf.size_width+5,40))
                self.screen.blit(font.render(str("{}".format(round(self.time/1000,2))), True, self.colors.white),(self.conf.size_width+5,65))
                #Wyswietlanie czasu w polsce
                self.screen.blit(font.render(str("{}".format(time.ctime(self.seconds))[11:20]), True, self.colors.green),(self.conf.size_width+5,100))
                #self.screen.blit(font.render(str(int(a[0])), True, self.colors.green),(self.conf.size_width+5,140))
                self.screen.blit(font.render(str("TOP5"), True, self.colors.white),(self.conf.size_width+5,120))
                for ind, txt in enumerate(self.file.txt):
                    self.screen.blit(font.render(str("{}. {}".format(ind+1,txt)).encode('utf-8'), True, self.colors.white),(self.conf.size_width+5,140+ind*20))
                pygame.display.flip()#Zamiana buforow
                self.get_event()#Funkcja odpowiedzialna za przechwytywanie zdarzen
                timer[1]=0
            
    #Metoda Do pobierania zdarzen i przypisywania ich odpowiednim polom
    def get_event(self):
        #Sprawdzanie w petli zdarzen, jesli ESC lub krzyzyk to wyjscie z gry(poki co)
        #oraz zapisanie klawisze do zmiennej w wezu odpowiedzialnej za ruch
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT(self)
            elif event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                EXIT(self)
            #Poprawic ponizszy kod, dalej waz moze sie cofnac w siebie
            #Kod zostal poprawiony
            if event.type == pygame.KEYDOWN and self.snake.flag_move:
                if event.key == pygame.K_d:#Jesli klawisz wcisniety to d, przejdz dalej
                    if self.snake.my_key != pygame.K_a:#Jesli klawisz w snake jest jako a, to nie napisze go poniewaz waz cofnalbym sie w siebie
                        self.snake.my_key = event.key
                     #   print("Klikam d",event.key)
                elif event.key == pygame.K_s:
                    if self.snake.my_key != pygame.K_w:
                        self.snake.my_key = event.key
                     #   print("Klikam s",event.key)
                elif event.key == pygame.K_w:
                    if self.snake.my_key != pygame.K_s:
                        self.snake.my_key = event.key
                     #   print("Klikam w",event.key)
                elif event.key == pygame.K_a:
                    if self.snake.my_key != pygame.K_d:
                        self.snake.my_key = event.key
                    #  print("Klikam a",event.key)
                self.snake.flag_move=0
                break

                    

    
    #Zapisanie klawisze do weza
    #Metoda odpowiedzialna za zbieranie
    def eat(self):
        flag=1
       # position = [random.randrange(0,500,25),random.randrange(0,500,25)]
        while flag:
            #Losowanie pozycji dla nowego punktu
            position = [random.randrange(0,500,25),random.randrange(0,500,25)]
            flag=0
            for tmp in self.snake.body:
                if position == [tmp.x,tmp.y]:#Jesli pozycja punktu jest rowna czesci weza
                    #to flaga =1 i od nowa bedzie losowana pozycja
                    #jesli pozycja jest ok,to flaga zostanie 0 i wyjscie z while
                    flag=1
                    break
        if self.snake.head == self.food.position:#Jesli glowa jest na pozycji
            #To dodaj do konca weza nowy element
            self.snake.body.append(pygame.Rect((self.snake.tail[0],self.snake.tail[1],self.conf.snake_size,self.conf.snake_size)))#R
            #Zmiana polozenia punktu
            #Ta linie zostawie na wszelki wypadek
            #self.food.body[0]=pygame.Rect((position[0],position[1],self.conf.snake_size,self.conf.snake_size))
            self.food.body[0].x=position[0]
            self.food.body[0].y=position[1]
            #Wylosowana pozycja zostanie zapisana do pola w food
            self.food.position = position
            #Zwiekszenie wyniku gracz po trafieniu
            self.snake.score+=1
            #Zwiekszenie predkosci weza, po zjedzeniu odpowiedniej ilosci punktow
            self.faster()
            #Linia testowa
            #print("Trafil ",self.food.body[0].x," ",self.food.body[0].y)
    #Metoda odpowiada za przyszpieszenia weza po kazdym zdobyciu 5 punktow
    def faster(self):
        if self.snake.score % self.conf.faster ==0 and self.conf.delay_move > self.conf.fps:
            self.conf.delay_move-=1
class Colors():
    def __init__(self):
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.green = (0,255,0)

#Zrobic jutro liste wynikow z zapisem do pliku ok
#Stworzyc tekstury dla weza 
#Stworzyc menu

Game()