#(спрайты действуют пока я попадаю)#

import arcade
import random
import time

SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'sHitman 7'

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        #настройки игры#
        self.peoples = arcade.SpriteList()
        self.cross = None  #переменная для экземпляра класса прицела
        self.set_mouse_visible(False)
        self.score = 0
        self.lives = 10
        self.speed = 1
        self.frequency = 250 #частота, чем больше тем реже выбегают люди
        self.status = True 
        self.streak=0
        
        self.headshots = arcade.SpriteList()
        self.timer=0
        self.time_past=0

        
        #настройки игры#
        
        #общие переменные для оружия
        
        self.reloading=False #оружие щас не перезаряжается
        self.seconds_past=0 #для перезарядки, чтобы приплюсовать self.weapon.time_reloading к этому значению
        self.weapon=Pistol() #создание экземпляра класса оружия, изначально пистолета (1)
        
        self.pistol_ammo_left=5
        self.gun_ammo_left=3
        #общие переменные для оружия        

    def setup(self):
        self.cross = Cross()#создание экземпляра класса для прицела
        ##SOUNDS##
        
        #Main sounds#
        self.headshot_sound=arcade.load_sound("Music/headshot.mp3")
        #Main sounds#
        
        #Streaks sounds#
        self.killing_spree_sound=arcade.load_sound("Music/killing_spree.mp3")
        self.dominating_sound=arcade.load_sound("Music/dominating.mp3")
        self.multi_kill_sound=arcade.load_sound("Music/multi_kill.mp3")
        self.unstoppable_sound=arcade.load_sound("Music/unstoppable.mp3")
        self.wicked_sick_sound=arcade.load_sound("Music/wicked_sick.mp3")
        self.monster_kill_sound=arcade.load_sound("Music/monster_kill.mp3")
        self.godlike_sound=arcade.load_sound("Music/godlike.mp3")
        #Streaks sounds#
        
        #Weapon sounds#
        
        #pistol sounds
        self.pistol_shot_sound=arcade.load_sound("Music/pistol_shot.mp3")
        self.pistol_need_reload_sound=arcade.load_sound("Music/pistol_need_reload.mp3")
        self.pistol_reload_sound=arcade.load_sound("Music/pistol_reload.mp3")
        
        #shotgun sounds
        self.shotgun_shot_sound=arcade.load_sound("Music/shotgun_shot.mp3")
        self.shotgun_need_reload_sound=arcade.load_sound("Music/shotgun_need_reload.mp3")
        self.shotgun_reload_sound=arcade.load_sound("Music/shotgun_reload.mp3")
        
        #main weapon sounds
        self.shot_sound=self.pistol_shot_sound
        self.need_reload_sound=self.pistol_need_reload_sound
        self.reload_sound=self.pistol_reload_sound
        self.weapon_draw_sound=arcade.load_sound("Music/Weapons/Main_Weapon/weapon_draw.mp3")
        

    def update(self, delta_time):
        self.headshots.update_animation()
        self.headshots.update()
        self.timer+=0.02

        
        self.seconds=round(time.time()) #постоянное получение и округление секунд прошедших с 1970 года (лол)
        
        ##основной луп игры с созданием человечков##
        if self.status==True: #если мы не проиграли
            self.cross.update()
            self.rand=random.randint(0, self.frequency) #постоянно получает случайное число и когда совпадет с частотой (self.frequency) создает экземпляр класса чела
            
            if self.rand == self.frequency: #см строчку выше
                people = People()
                people.center_x = random.randint(-100,0) #появление по оси X и по сути время через которое появится, т.к чем больше X, тем дальше по экрану будет чел
                people.center_y = random.randint(0, 500) #появление по оси Y
                self.peoples.append(people)
                
            self.peoples.update_animation() #чтобы челики были анимированы
            self.peoples.update()
            
            #проигрыш
            if self.lives <= 0:
                self.status = False
            ##основной луп игры с созданием человечков##
                
            ##основной луп перезарядки## #ERROR: если у обоих оружий 0 патрон, то будут перезаряжаться сразу оба# 
            #перезарядка осуществилась#
            if self.seconds==self.seconds_past and self.weapon.reload==True: #срабатывает после нажатия R спустя self.weapon.reload_time
                    self.weapon.ammo=self.weapon.magazine #присваивание оружию его максимальный боезапас (self.weapon.magazine) #ERROR перезаряжает сразу все оружия
                    self.weapon.reload=False #перезарядка текущему оружию не нужна
                    self.reloading=False #перезарядка (действие) закончилась
                    self.weapon.n=0 #переменная переключатель перезарядки
                    
            #перезарядка; выдвигает требование о перезарядке и считывает начало её выполнение по переключателю self.n=1 передаваемому из нажатия клавиши R#
            if self.weapon.ammo==0:
                self.weapon.reload=True
                if self.weapon.n==1:
                    self.seconds_past=self.seconds+self.weapon.time_reload #время перезарядки time_reload 
                    self.weapon.n=self.weapon.n+1
            ##основной луп перезарядки##  
                
    def on_draw(self):
        #фон
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)

        self.headshots.draw()

        #спрайты
        self.peoples.draw()
        self.cross.draw()
        self.weapon.draw()

        #надписи
        arcade.draw_text(f"Streak: {self.streak}",window.width/2,window.height-40,arcade.color.BLACK,30) #проверка стрика
        arcade.draw_text(f'Score: {self.score}', 40, self.height-40, arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Lives: {self.lives}', self.width - 160, self.height - 40, arcade.color.BLACK, font_size=30)
        arcade.draw_text("Ammo: "+str(self.weapon.ammo*("I")), self.width-180, 40, arcade.color.BLACK, 30) #надо его сделать спрайтами с картинкой патрона
        

          ##тут можно тестить время (time) в проге
##        arcade.draw_text("Время: "+str(self.seconds), 0, 40, arcade.color.BLACK, 30)                           
##        arcade.draw_text("Времени прошло: "+str(self.seconds_past), 0, 80, arcade.color.BLACK, 30)             
##        arcade.draw_text("Времени прошло + 5: "+str(self.seconds_past+5), 0, 120, arcade.color.BLACK, 30)      


    def on_mouse_motion(self, x, y, dx, dy):
        if self.status==True: 
            self.cross.center_x = x
            self.cross.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):




        
        if self.status==True:


            
            
            if self.weapon.reload==False: #если оружие не требует перезарядки
                arcade.play_sound(self.shot_sound,0.5)
                self.weapon.ammo-=1
                self.weapon.ammo_left=self.weapon.ammo #сохранение значения оставшихся патрон в магазине
                self.aimed=False #типа не попали в хед изначально
                
                hits = arcade.check_for_collision_with_list(self.cross, self.peoples) #добавление задетых прицелом спрайтов в список hits
                for people in hits:
                    #если попал в хед
                    #в дальнейшем в этом if использовать разброс оружия self.weapon_shooting_range_x1,2 и _y1,2 а так тут подогнан под точечный выстрел в голову#
                    if (self.cross.center_x<=people.center_x+self.weapon.shooting_range[0] and self.cross.center_x>people.center_x+self.weapon.shooting_range[1]) and (self.cross.center_y<=people.top+self.weapon.shooting_range[2] and self.cross.center_y>people.top++self.weapon.shooting_range[3]):
                        people.kill()
                        ##кровяк##
                        self.time_past=self.timer+1
                        headshot=Headshot()
                        headshot.center_x=x
                        headshot.center_y=y
                        headshot.texture=headshot.textures[0]
                        self.headshots.append(headshot)
                        ##кровяк##
                        self.score += 10
                        self.aimed=True #типа попал в хед и стрик набираеца за счет True-шности этого переключателя
                        arcade.play_sound(self.headshot_sound,0.5)

                        #увеличение скорости в любом случае попадания каждые 2 очка
                        if self.score % 2 == 0:
                            self.speed += 0.01
                            self.frequency -= 1 #увеличение частоты появления челов, ведь чем меньше self.frequency, тем быстрее рандом подберет его значение 
                            
                        #набор стрика#
                        self.streak+=1
                        if self.streak==3:
                            arcade.play_sound(self.killing_spree_sound,0.5)
                        elif self.streak==4:
                            arcade.play_sound(self.dominating_sound,0.5)
                        elif self.streak==5:
                            arcade.play_sound(self.multi_kill_sound,0.5)
                        elif self.streak==6:
                            arcade.play_sound(self.unstoppable_sound,0.5)
                        elif self.streak==7:
                            arcade.play_sound(self.wicked_sick_sound,0.5)
                        elif self.streak==8:
                            arcade.play_sound(self.monster_kill_sound,0.5)
                        elif self.streak>=9:
                            arcade.play_sound(self.godlike_sound,0.5)
                        
                            
                    else: #не попал в хед#
                        people.kill()
                        self.score += 1
                        self.aimed=False #типо не попал в хед стрик сбился
                        
                        #увеличение скорости в любом случае попадания каждые 2 очка
                        if self.score % 2 == 0:
                            self.speed += 0.01
                            self.frequency -= 1  #увеличение частоты появления челов, ведь чем меньше self.frequency, тем быстрее рандом подберет его значение             
                    
            else:
                if self.weapon.n==0: #если клавиша R не была нажата и мы пытаемся выстрелить играется звук пустой обоймы оружия
                    arcade.play_sound(self.need_reload_sound,0.5) #нужно поменять в зависимости от оружия 
                    
        #сбитие стрика, если не попали в хед#
            if self.aimed==False:
                self.streak=0
                
        else: #обнуление всех параметров для новой игры в случае луза (if self.status==False)
            for people in self.peoples:
                people.kill()
                self.score = 0
                self.speed = 0.5
                self.frequency = 200
                self.status = True
                
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE: #закрытие окна по нажатию ESC
            window.close() 
            
        #начало перезарядки на R
        if key==arcade.key.R and self.status==True and self.weapon.reload==True:
            self.weapon.n=1 #переменная-переключатель, сообщающая о том, что перезарядка была нажата и эта переменная становится равна 1
            arcade.play_sound(self.reload_sound,0.5)
            self.reloading=True #перезарядка началась (еще 1 логическая переменная хз зачем я ее добавил, мб, потом вспомню, но я ее юзаю)
            
        #смена оружия по нажатию на 1-9
        if key==arcade.key.KEY_1 and self.status==True and self.reloading==False:
            arcade.play_sound(self.weapon_draw_sound,0.5)
            
            #смена звуков оружия на пистолет, нужно это все в классе сделать
            self.shot_sound=self.pistol_shot_sound
            self.need_reload_sound=self.pistol_need_reload_sound
            self.reload_sound=self.pistol_reload_sound

            self.gun_ammo_left=self.weapon.ammo #в дальнейшем тут будут прописаны значения всех других оружий ибо хз в какой момент на какой поменяет юзер
            #self.weapon.ammo_left=self.weapon.ammo #нужно как-то обменять значения оставшихся патрон и сохранить их
            self.weapon=Pistol()
            self.weapon.ammo=self.pistol_ammo_left
            
        if key==arcade.key.KEY_2 and self.status==True and self.reloading==False:
            arcade.play_sound(self.weapon_draw_sound,0.5)
            
            #смена звуков оружия на дробовик нужно это все в классе сделать
            self.shot_sound=self.shotgun_shot_sound
            self.need_reload_sound=self.shotgun_need_reload_sound
            self.reload_sound=self.shotgun_reload_sound

            self.pistol_ammo_left=self.weapon.ammo #в дальнейшем тут будут прописаны значения всех других оружий ибо хз в какой момент на какой поменяет юзер
            #self.weapon.ammo_left=self.weapon.ammo #нужно как-то обменять значения оставшихся патрон и сохранить их
            self.weapon=Gun()
            self.weapon.ammo=self.gun_ammo_left

#classes for main sprites
#прицел            
class Cross(arcade.Sprite):
    def __init__(self):
        super().__init__("images/cross3.png", 0.1)

        self.center_x = window.width / 2
        self.center_y = window.height / 2

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

#челики
class People(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()
        self.textures.append(arcade.load_texture("images/test11.png"))
        self.textures.append(arcade.load_texture("images/test22.png"))
        self.change_x=2

    def update(self):
        self.center_x += self.change_x

        if self.left >= window.width:
            self.kill()
            window.lives -= 1
         
#classes for weapons#
            
#пестик
class Pistol(arcade.Sprite):
    def __init__(self): 
        super().__init__("images/pistol.png",0.05)
        self.center_x=40
        self.center_y=40
        self.ammo=5
        self.ammo_left=5
        self.magazine=5
        self.reload=False
        self.time_reload=2
        self.n=0
        self.shooting_range=[15,-5,-5,-25] #+x1,+x2,+y1,+y2 #разброс оружия, который пишу в ифе для расчета хедшота и попадания; у пистолета маленькие числа в разбросе

#шотган
class Gun(arcade.Sprite):
    def __init__(self): 
        super().__init__("images/shotgun.png",0.15)
        self.center_x=45
        self.center_y=40
        self.ammo=3
        self.ammo_left=3
        self.magazine=3
        self.reload=False
        self.time_reload=4
        self.n=0
        self.shooting_range=[25,-15,5,-35] #+x1,+x2,+y1,+y2 #разброс оружия, который пишу в ифе для расчета хедшота и попадания; а тут большой разброс


class Headshot(arcade.AnimatedTimeSprite): 
    def __init__(self):
        super().__init__()
        for i in range(1,16):
            self.textures.append(arcade.load_texture("images/hsblood"+str(i)+".png"))
    def update(self):
        if window.timer>window.time_past:
            self.kill()


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
