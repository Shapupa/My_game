from typing import Any
import pygame as pg
from random import randint
import os 
import copy 
import random
pg.font.init()
weight, hight = 1000, 600

class Hero():
    def __init__(self, imges):
        self.path = imges
        self.frames = os.listdir(self.path)
        self.surf = pg.image.load(f'{self.path}/{self.frames[0]}')
        self.surf = pg.transform.scale_by(self.surf, 0.4)
        self.img_fliped = False
        self.surf.set_colorkey('White')
        self.frame_change = 15
        self.timer = 0
        self.frame = 0
        self.rect = self.surf.get_rect(center = (weight/2, hight/2))
        self.x_cord = self.rect.x
        self.y_cord = self.rect.y
        self.hero_stop = True
        self.exp_len = 0 
        self.hero_lvl_up = False
        self.get_damage = False
        self.imortal_time = 40
        self.get_hit_time = 0
        self.hp_len = self.rect.width
        self.hero_max_hp = all_stat['hero']['Hp']

    def change_frame(self):
        if not self.hero_stop:
            self.timer += 1
            if self.timer > self.frame_change:
                self.timer = 0
                self.frame += 1 
                if self.frame == len(self.frames):
                    self.frame = 0
                self.surf = pg.image.load(f'{self.path}/{self.frames[self.frame]}')
                self.surf = pg.transform.scale_by(self.surf, 0.4)
        self.img_flip()
                
    def move(self):
        self.hero_stop = True
        self.key_bord = pg.key.get_pressed()
        if self.key_bord[pg.K_d]:
            self.hero_stop = False
            if self.rect.right <= 650:
                self.x_cord += all_stat['hero']['speed']
        elif self.key_bord[pg.K_a]:
            self.hero_stop = False
            if self.rect.left >= 350:
                self.x_cord += -all_stat['hero']['speed']
        if self.key_bord[pg.K_w]:
            self.hero_stop = False
            if self.rect.top >= 200:
                self.y_cord += -all_stat['hero']['speed']
        elif self.key_bord[pg.K_s]: 
            self.hero_stop = False
            if self.rect.bottom <= 400:
                self.y_cord += all_stat['hero']['speed']

    def img_flip(self):
        self.key_bord = pg.key.get_pressed()
        if self.key_bord[pg.K_a] and not self.img_fliped:
            self.img_fliped = True

        if self.key_bord[pg.K_d] and self.img_fliped:
            self.img_fliped = False

        if self.img_fliped:
            self.surf = pg.transform.flip(self.surf, True, False)   
        self.surf.set_colorkey('White')

    def exp_bar(self):
        if self.exp_len >= weight:
            self.hero_lvl_up = True
            all_stat['hero']['lvl'] += 1
            all_stat['hero']['hp_next_lvl'] *= 1.5
            self.exp_len -= weight

        pg.draw.rect(dis, 'white', [0, 0, weight, 10])
        pg.draw.rect(dis, 'blue', [0, 0, self.exp_len, 10])
    
    def enemy_col(self):
        for i in enemes:
            if self.rect.colliderect(i.rect) and not self.get_damage:
                all_stat['hero']['Hp'] -= i.damage
                if all_stat['hero']['Hp'] > 0:
                    self.hp_len -= (self.rect.width/self.hero_max_hp)*i.damage
                    self.get_damage = True
                    self.get_hit_time = timer
        if self.get_damage:
            if timer - self.get_hit_time >= self.imortal_time:
                self.get_damage = False 
        self.hp_bar()

    def hp_bar(self):
        pg.draw.rect(dis, 'red', [self.rect.x, self.rect.y - 20, self.rect.width, 10])
        pg.draw.rect(dis, 'white', [self.rect.x+1, self.rect.y - 19, self.hp_len-2, 8])

    def blit(self):
        if all_stat['hero']['Hp'] > 0:
            if not self.hero_lvl_up:
                self.change_frame()
                self.move()
                self.exp_bar()
                self.enemy_col()   
                self.rect.x = self.x_cord
                self.rect.y = self.y_cord


        return (self.surf, self.rect)
    
class Background(pg.sprite.Sprite):
    def __init__(self, img, x, y, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img)
        self.rect = self.image.get_rect(x=x, y=y)
        self.speed = speed

    def move(self):
        key_bord = pg.key.get_pressed()
        if key_bord[pg.K_d] and hero.rect.right >= 650:
            self.rect.x += -self.speed
        if key_bord[pg.K_a] and hero.rect.left <= 350:
            self.rect.x += self.speed
        if key_bord[pg.K_w] and hero.rect.top <= 200:
            self.rect.y += self.speed
        if key_bord[pg.K_s] and hero.rect.bottom >= 400:
            self.rect.y += -self.speed

    def delete(self):
        if self.rect.left >= weight+100:
            self.rect.center = (-50, self.rect.centery)
        if self.rect.right <= -100:
            self.rect.center = (weight+50, self.rect.centery)
        if self.rect.bottom <= -100:
            self.rect.center = (self.rect.centerx, hight+50)
        if self.rect.top >= hight+100:
            self.rect.center = (self.rect.centerx, -50)
        
    def update(self):
        self.delete()
        self.move()

class enemy(pg.sprite.Sprite):
    def __init__(self, img, speed, hp, size, damage, exp):
        pg.sprite.Sprite.__init__(self)
        self.hp = hp
        self.speed = speed
        self.size = size 
        self.damage = damage
        self.exp = exp
        self.path = img
        self.frames = os.listdir(self.path)
        self.image = pg.image.load(f'{self.path}/{self.frames[0]}')
        self.image = pg.transform.scale_by(self.image, self.size)
        self.image.set_colorkey('White')
        self.frame_change = 5
        self.timer = 0
        self.frame = 0
        self.rect = self.image.get_rect(center = (self.rabdom_cord()))
        self.y_cord = self.rect.centery
        self.x_cord = self.rect.centerx
        self.img_fliped = False

    def change_farme(self):
        self.timer += 1
        if self.timer > self.frame_change:
            self.timer = 0
            self.frame += 1 
            if self.frame == len(self.frames):
                self.frame = 0
            self.image = pg.image.load(f'{self.path}/{self.frames[self.frame]}')
            self.image = pg.transform.scale_by(self.image, self.size)
            self.img_flip()  
            self.image.set_colorkey('White')

    def rabdom_cord(self):
        cekotor = randint(1,4)
        if cekotor == 1:
            x = randint(-200, -100)
            y = randint(-200, hight + 100)    
        elif cekotor == 2:
            x = randint(-100, weight+200)
            y = randint(-200, -100)  
        elif cekotor == 3:
            x = randint(weight+100, weight+200)      
            y = randint(-100, hight+200)
        elif cekotor == 4:
            x = randint(-200, weight+100)
            y = randint(hight+100, hight+200)
        return (x, y)
        
    def dyration(self):
        distance = 1 + ((hero.rect.centerx - self.rect.centerx)**2 + (hero.rect.centery -self.rect.centery)**2)**0.5
        steps = distance/self.speed
        self.x_speed = (hero.rect.centerx - self.rect.centerx)/steps
        self.y_speed = (hero.rect.centery - self.rect.centery)/steps

    def check_hero_move(self):
        key_bord = pg.key.get_pressed()
        if key_bord[pg.K_d] and hero.rect.right >= 650:
            self.x_cord += -all_stat['hero']['speed']
        if key_bord[pg.K_a] and hero.rect.left <= 350:
            self.x_cord += all_stat['hero']['speed']
        if key_bord[pg.K_w] and hero.rect.top <= 200:
            self.y_cord += all_stat['hero']['speed']
        if key_bord[pg.K_s] and hero.rect.bottom >= 400:
            self.y_cord += -all_stat['hero']['speed']

    def move(self):
        self.check_hero_move()
        self.x_cord += self.x_speed
        self.y_cord += self.y_speed

    def col_atack(self):
        for i in atacks:
            if self.rect.colliderect(i.rect):
                i.kill()
                self.hp -= all_stat['start_atack']['Damage']
                if self.hp <= 0:
                    self.kill()
                    exp_gain = self.exp
                    hero.exp_len += (weight/all_stat['hero']['hp_next_lvl'])*exp_gain

    def img_flip(self):
        if self.rect.centerx - hero.rect.centerx > 0 and not self.img_fliped:
                self.image = pg.transform.flip(self.image, True, False)
                self.img_flied = True

        elif self.rect.centerx - hero.rect.centerx < 0 and self.img_fliped:
                self.image = pg.transform.flip(self.image, True, False)
                self.img_fliped = False

    def update(self):
        self.change_farme()
        self.dyration()
        self.move()
        self.col_atack()
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord

class Atack(pg.sprite.Sprite):
    def __init__(self, img):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img)
        self.image = pg.transform.scale_by(self.image, 0.10)
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect(center = (hero.rect.center))
        self.speed = all_stat['start_atack']['speed']
        self.target()
        self.angel = 0
        self.x_cord = self.rect.centerx
        self.y_cord = self.rect.centery

    def target(self):
        mouse_target = pg.mouse.get_pos()
        distance = ((hero.rect.x - mouse_target[0])**2 + (hero.rect.y - mouse_target[1])**2)**0.5
        steps = distance/self.speed
        self.x_speed = (hero.rect.centerx - mouse_target[0])/steps
        self.y_speed = (hero.rect.centery - mouse_target[1])/steps
        # min_distance = 10000000
        # for i in enemes:
        #     distance = ((hero.rect.x - i.rect.x)**2 + (hero.rect.y - i.rect.y)**2)**0.5
        #     if distance < min_distance:
        #         self.closest_target = i
        #         min_distance = distance
        # self.auto_target()

    def auto_target(self): 
        if self.closest_target in enemes:    
            self.target_cord = self.closest_target.rect.center
            distance = ((self.rect.x - self.closest_target.rect.x)**2 + (self.rect.y - self.closest_target.rect.y)**2)**0.5
            self.steps = distance/self.speed
            self.x_speed = (self.rect.centerx - self.target_cord[0])/self.steps
            self.y_speed = (self.rect.centery - self.target_cord[1])/self.steps
        # else:
        #     for i in background:
        #         if not self.rect.colliderect(i.rect):
                    # self.kill
        # else:
        #     min_distance = 10000000
        #     for i in enemes:
        #         distance = ((self.rect.x - i.rect.x)**2 + (self.rect.y - i.rect.y)**2)**0.5
        #         if distance < min_distance:
        #             self.closest_target = i
        #             min_distance = distance

    def check_hero_move(self):
        key_bord = pg.key.get_pressed()
        if key_bord[pg.K_d] and hero.rect.right >= 650:
            self.x_cord += -all_stat['hero']['speed']
        if key_bord[pg.K_a] and hero.rect.left <= 350:
            self.x_cord += all_stat['hero']['speed']
        if key_bord[pg.K_w] and hero.rect.top <= 200:
            self.y_cord += all_stat['hero']['speed']
        if key_bord[pg.K_s] and hero.rect.bottom >= 400:
            self.y_cord += -all_stat['hero']['speed']

    def update(self):
        # self.auto_target()
        self.check_hero_move()
        self.x_cord -= self.x_speed
        self.y_cord -= self.y_speed
        self.rect.centerx = self.x_cord
        self.rect.centery = self.y_cord

all_stat = {'hero':{'speed': 1, 'Hp':10,'Damage':15, 'lvl':0, 'hp_next_lvl':5},
            'start_atack': {'atack_speed': 40, 'speed': 10,'Damage':10}, 
            'enemy_green': {'speed':2,'Hp':10,'Damage':3, 'enemy_spawn':55, 'Exp':1, 'chance': 4}}

all_stat_start = copy.deepcopy(all_stat)

dis = pg.display.set_mode((weight, hight))
clock = pg.time.Clock()
on = True 
timer = 0
start_atack_time = 0
green_enemy_spawn = 0 

hero = Hero('my_rog/Char_frames')
lvl_up_choes = False
font = pg.font.Font(None, 24)

background = pg.sprite.Group()
enemes = pg.sprite.Group()
upgrade_rate = 600
atacks = pg.sprite.Group()

game_over_img = pg.image.load('my_rog/game_over.png')
game_over_img_rect = game_over_img.get_rect(center = (weight/2, hight/2.5))

restart_img = pg.image.load('my_rog/restart_button.png')
restart_img = pg.transform.scale_by(restart_img, 0.08)
restart_img.set_colorkey('white')
restart_img_rect = restart_img.get_rect(center = (weight/2, hight/2.5 + game_over_img_rect.height + 20))

upgrades_img = []
for i in os.listdir('my_rog/level_ups'):
    upgrades_img.append([pg.image.load(f'my_rog/level_ups/{i}'), i.replace('.png', '')])


back_img = 'my_rog/1677366330_foni-club-p-piksel-art-trava-3.png'
for i in range(-100, weight+100, 100): 
    for b in range(-100, hight+100, 100):
        back = Background(back_img, i, b, all_stat['hero']['speed'])
        background.add(back)

while on:
    timer += 1 
    mouse_pos = pg.mouse.get_pos()
    mouse_push = pg.mouse.get_pressed()

    if timer - upgrade_rate >= 0:
        all_stat['enemy_green']['Damage'] *= 1.1
        all_stat['enemy_green']['Hp'] *= 1.1 
        all_stat['enemy_green']['speed'] *= 1.1
        all_stat['enemy_green']['enemy_spawn'] -= 1
        all_stat['enemy_green']['Exp'] += 1
        upgrade_rate += timer

    for event in pg.event.get():
        if event.type == pg.QUIT:
            on = False

    background.draw(dis)
    
    if all_stat['hero']['Hp'] > 0 and not hero.hero_lvl_up:
        if timer - start_atack_time <= all_stat['start_atack']['atack_speed']:
            reloud_time = (hero.rect.width/all_stat['start_atack']['atack_speed'])*(timer - start_atack_time)
        pg.draw.rect(dis, 'Blue', [hero.rect.x, hero.rect.y - 5, reloud_time, 5])
         
        if len(enemes) > 0 and timer - start_atack_time >= all_stat['start_atack']['atack_speed']:
            if mouse_push[0]:
                atack = Atack('my_rog/Stones.png')
                atacks.add(atack)
                start_atack_time = timer

        if timer - green_enemy_spawn >= all_stat['enemy_green']['enemy_spawn'] and len(enemes) < 50:
            enemy_teg = random.randint(1, 100)
            if enemy_teg <= all_stat['enemy_green']['chance']:
                enemy_big_bat = enemy(
                                'my_rog/Enemy_big_bat_frames', 
                                all_stat['enemy_green']['speed'] * 1.1, 
                                all_stat['enemy_green']['Hp'] * 5, 
                                0.4, 
                                all_stat['enemy_green']['Damage'] * 3, 
                                all_stat['enemy_green']['Exp'] * 5)    
                enemes.add(enemy_big_bat)
            else:
                enemy_bat = enemy(
                            'my_rog/Enemy_bat_frames', 
                            all_stat['enemy_green']['speed'], 
                            all_stat['enemy_green']['Hp'], 
                            0.1, 
                            all_stat['enemy_green']['Damage'], 
                            all_stat['enemy_green']['Exp'])
                enemes.add(enemy_bat)
                
            green_enemy_spawn = timer

    atacks.draw(dis)
    enemes.draw(dis)
    dis.blit(hero.blit()[0],hero.blit()[1])
    lvl_show = font.render(f'LVL: {all_stat["hero"]["lvl"]}', True, 'Blue')
    dis.blit(lvl_show, (480, 20))

    if all_stat['hero']['Hp'] > 0:
        if not hero.hero_lvl_up:
            background.update()
            atacks.update()
            enemes.update()
            if mouse_push[0]:
                alredy_presed = True
        
        else:
            if not lvl_up_choes: 
                lvl_up_choes = True
                upgrades = random.choices(upgrades_img, k = 2)
                if upgrades[0][0] == upgrades[1][0]:
                    lvl_up_choes = False
            chose_ability = font.render(f'Make choice', True, 'Red')
            dis.blit(chose_ability, (weight/2 - 50, hight/2 - 180))
            dis.blit(upgrades[0][0], upgrades[0][0].get_rect(center = (weight/2 + 70, hight/2 - 100)))
            dis.blit(upgrades[1][0], upgrades[1][0].get_rect(center = (weight/2 - 70, hight/2 - 100)))
            multiply = 1.2

            if alredy_presed and not mouse_push[0]:
                alredy_presed = False

            if upgrades[0][0].get_rect(center = (weight/2 + 70, hight/2 - 100)).collidepoint(mouse_pos):
                if mouse_push[0] and not alredy_presed:
                    if upgrades[0][1] == 'Atack': all_stat['start_atack']['Damage'] *= multiply
                    if upgrades[0][1] == 'bulets': all_stat['start_atack']['atack_speed'] /= multiply
                    if upgrades[0][1] == 'Hp': 
                        all_stat['hero']['Hp'] = (hero.hero_max_hp*multiply) - (hero.hero_max_hp - all_stat['hero']['Hp'])
                        hero.hero_max_hp *= multiply
                        hero.hp_len = (hero.rect.width/hero.hero_max_hp)*all_stat['hero']['Hp']
                    if upgrades[0][1] == 'Speed': all_stat['hero']['speed'] *= multiply
                    hero.hero_lvl_up = False
                    lvl_up_choes = False
            elif upgrades[1][0].get_rect(center = (weight/2 - 70, hight/2 - 100)).collidepoint(mouse_pos):
                if mouse_push[0] and not alredy_presed:
                    if upgrades[1][1] == 'Atack': all_stat['start_atack']['Damage'] *= multiply
                    if upgrades[1][1] == 'bulets': all_stat['start_atack']['atack_speed'] /= multiply
                    if upgrades[1][1] == 'Hp': 
                        all_stat['hero']['Hp'] = (hero.hero_max_hp*multiply) - (hero.hero_max_hp - all_stat['hero']['Hp'])
                        hero.hero_max_hp *= multiply
                        hero.hp_len = (hero.rect.width/hero.hero_max_hp)*all_stat['hero']['Hp']
                    if upgrades[1][1] == 'Speed': all_stat['hero']['speed'] *= multiply
                    hero.hero_lvl_up = False
                    lvl_up_choes = False

    else: 
        dis.blit(game_over_img, game_over_img_rect)
        dis.blit(restart_img, restart_img_rect)
        if restart_img_rect.collidepoint(mouse_pos):
            if mouse_push[0]:
                all_stat = copy.deepcopy(all_stat_start)    
                enemes.remove(enemes)
                atacks.remove(atacks)
                hero = Hero('my_rog/Char_frames')
                
    clock.tick(40)

    pg.display.update()

pg.display.quit()