import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

os.chdir(current_dir)

import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF 
import Bullet
import DADcharacter
import Slave
import global_var
import Effect
import gameRule
import lightnessLevel
import DuelClassLevel
import menu

#define background
#branch test

def play_game():
    
    angle = 0
    FPS = 60 # 帧率 
    fpsClock = pygame.time.Clock()
    #global variable area 

    #initialize gaming
    frame = 0
    pygame.init() 
    pygame.font.init() #initialize font
    pygame.mixer.init()
    pygame.mixer.set_num_channels(30)
    size = width, height = 960, 720
    fullscreen = False 
    
    if fullscreen:
        screen = pygame.display.set_mode(size, FULLSCREEN | HWSURFACE | DOUBLEBUF)
    else:
        screen = pygame.display.set_mode(size, RESIZABLE | DOUBLEBUF)
        
    stage = pygame.Surface((660, 690)).convert_alpha()
    stage.set_clip(Rect(60, 30, 560, 660))
    global_var._init()

    #test functions 
    global_var.set_value('ifTest', False)
    global_var.set_value('spellNum', 1)
    global_var.set_value('ifSpellTest', True)
    testFire = 400
     
    #settings init
    if_highQuality_effect = True
    if_speedAdjusting = False
    global_var.set_value('if_highQuality_effect', if_highQuality_effect)
    global_var.set_value('if_speedAdjusting', if_speedAdjusting)

    #screen settings
    global_var.set_value('screen_width', width)
    global_var.set_value('screen_height', height)
    amplified_times = width / 640
    global_var.set_value('amplified_times', amplified_times)
    global_var.set_value('stage_left', round(30 * amplified_times))
    global_var.set_value('stage_width', round(384 * amplified_times))
    global_var.set_value('stage_height', round(448 * amplified_times))
    global_var.set_value('stage_vSlit', round(16 * amplified_times))

    pygame.display.set_caption("Touhou Star Salvation - 좌석 빼앗기")
    icon_img = pygame.image.load(os.path.join(current_dir, "star_salvation_enUS.ico"))
    pygame.display.set_icon(icon_img)
    
    back = pygame.image.load(os.path.join(current_dir, 'resource/background.jpg')).convert_alpha()
    point = pygame.image.load(os.path.join(current_dir, 'resource/point.png')).convert_alpha()
    point2 = pygame.image.load(os.path.join(current_dir, 'resource/point2.png')).convert_alpha()
    point = pygame.transform.smoothscale(point, (96, 96))
    point2 = pygame.transform.smoothscale(point2, (96, 96))
    point2.set_alpha(128)
    
    engFontPath = os.path.join(current_dir, 'resource/font/open-sans/OpenSans-Regular.ttf')
    myfont = pygame.font.Font(engFontPath, 12)
    bigfont = pygame.font.Font(engFontPath, 24)
    midfont = pygame.font.Font(engFontPath, 20)
    chfont = pygame.font.Font(os.path.join(current_dir, './resource/font/FeiHuaSongTi-2.ttf'), 20)
    smallfont = pygame.font.SysFont('arial', 16)
    bossMagic = pygame.image.load(os.path.join(current_dir, 'resource/bossMagic.png')).convert_alpha()

    back_up = pygame.image.load(os.path.join(current_dir, 'resource/up.jpg')).convert_alpha()
    global_var.set_value('up', back_up)
    back_down = pygame.image.load(os.path.join(current_dir, 'resource/down.jpg')).convert_alpha()
    global_var.set_value('down', back_down)
    back_left = pygame.image.load(os.path.join(current_dir, 'resource/left.jpg')).convert_alpha()
    global_var.set_value('left', back_left)
    back_right = pygame.image.load(os.path.join(current_dir, 'resource/right.jpg')).convert_alpha()
    global_var.set_value('right', back_right)

    global_var.set_value('grazeNum', 0)
    global_var.set_value('fpSec', 0)
    global_var.set_value('enemyPos', (0, 0, 10000))
    global_var.set_value('shift_down', False)
    global_var.set_value('pause', False)
    global_var.set_value('escPressing', False)
    global_var.set_value('pauseScreen', 0)
    global_var.set_value('ifStopPressing', False)
    global_var.set_value('menu', True)
    global_var.set_value('ifGameOver', False)
    global_var.set_value('bgmPauseFlag', 0)
    global_var.set_value('bgmContinuePos', [0, 0])
    global_var.set_value('boomStatu', 0)
    global_var.set_value('levelSign', 0)
    global_var.set_value('scoreShown', 0)
    global_var.set_value('DuelClassLevel_ifMidpath', False)
    global_var.set_value('DeulClassLevel_midpathFrame', 0)
    global_var.set_value('levelPassSign', False)

    try:
        with open(os.path.join(current_dir, 'resource/data/highScore_0.dat')) as f: hySc0 = int(f.read())
    except: hySc0 = 0
    try:
        with open(os.path.join(current_dir, 'resource/data/highScore_1.dat')) as f: hySc1 = int(f.read())
    except: hySc1 = 0

    global_var.set_value('highScore_0', hySc0)
    global_var.set_value('highScore_1', hySc1)
    log = open(os.path.join(current_dir, "./log.csv"), 'w+')

    gF.loadImage()
    playerNum = 0
    global_var.set_value('playerNum', playerNum)
    player = DADcharacter.Reimu() if playerNum == 0 else DADcharacter.Marisa()
    player.tx, player.ty = 357.0, 600.0
    player.power = 100
    diffLevel = 1
    mainMenu = menu.Menu()
    pressed_keys_last = pygame.key.get_pressed()
    global_var.set_value('getTicksLastFrame', 0)
    global_var.set_value('enemySum', 0)
    blinder = pygame.Surface((780, 200))
    blinder.fill((0, 0, 0))

    
    bullets, bullets2 = Group(), Group()
    playerGuns, enemys, slaves = Group(), Group(), Group()
    booms, effects, stars, items = Group(), Group(), Group(), Group()
    backgrounds, bosses, titleDec = Group(), Group(), Group()
    gameRule.addStars(screen, stars)

    enemy_sound_amplify = 1.5
    miss_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_pldead00.wav')); miss_sound.set_volume(0.2)
    shoot_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_plst00.wav')); shoot_sound.set_volume(0.15)
    hit_sound1 = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_damage00.wav')); hit_sound1.set_volume(0.2)
    global_var.set_value('hit_sound1', hit_sound1)
    hit_sound2 = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_damage01.wav')); hit_sound2.set_volume(0.2)
    global_var.set_value('hit_sound2', hit_sound2)
    enemyDead_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_enep00.wav')); enemyDead_sound.set_volume(0.15)
    global_var.set_value('enemyDead_sound', enemyDead_sound)
    bossDead_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_enep01.wav')); bossDead_sound.set_volume(0.30)
    global_var.set_value('bossDead_sound', bossDead_sound)
    
    enemyGun_sound1 = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_tan00.wav')); global_var.set_value('enemyGun_sound1', enemyGun_sound1)
    enemyGun_sound2 = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_tan01.wav')); global_var.set_value('enemyGun_sound2', enemyGun_sound2)
    enemyGun_sound3 = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_tan02.wav')); global_var.set_value('enemyGun_sound3', enemyGun_sound3)
    slash_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_slash.wav'))
    item_get = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_item00.wav')); global_var.set_value('item_get', item_get)
    life_get = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_extend.wav')); global_var.set_value('life_get', life_get)
    water_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_water.wav')); global_var.set_value('water_sound', water_sound)
    kira_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_kira00.wav')); global_var.set_value('kira_sound', kira_sound)
    kira1_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_kira01.wav')); global_var.set_value('kira1_sound', kira1_sound)
    powerup_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_powerup.wav')); global_var.set_value('powerup_sound', powerup_sound)
    ch00_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_ch00.wav')); global_var.set_value('ch00_sound', ch00_sound)
    timeout_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_timeout.wav')); global_var.set_value('timeout_sound', timeout_sound)
    bonus_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_bonus.wav')); global_var.set_value('bonus_sound', bonus_sound)
    spell_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_cat00.wav')); global_var.set_value('spell_sound', spell_sound)
    laser_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_lazer00.wav')); global_var.set_value('laser_sound', laser_sound)
    option_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_option.wav')); global_var.set_value('option_sound', option_sound)
    graze_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_graze.wav')); global_var.set_value('graze_sound', graze_sound)
    nep_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_nep00.wav')); global_var.set_value('nep_sound', nep_sound)
    spell_end = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_enep02.wav')); global_var.set_value('spell_end', spell_end)
    enemyBigGun_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_enep02.wav')); global_var.set_value('enemyBigGun_sound', enemyBigGun_sound)
    pause_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_pause.wav')); global_var.set_value('pause_sound', pause_sound)
    select_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_select00.wav')); global_var.set_value('select_sound', select_sound)
    ok_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_ok00.wav')); global_var.set_value('ok_sound', ok_sound)
    cancel_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_cancel00.wav')); global_var.set_value('cancel_sound', cancel_sound)
    invalid_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_invalid.wav')); global_var.set_value('invalid_sound', invalid_sound)
    reimuBoom_sound = pygame.mixer.Sound(os.path.join(current_dir, 'resource/sound/se_tan00.wav')); global_var.set_value('reimuBoom_sound', reimuBoom_sound)

    pygame.mixer.music.load(os.path.join(current_dir, 'resource/bgm/mainTitle.mp3'))
    pygame.mixer.music.set_volume(0.6)   
    pygame.mixer.music.play(loops=-1)

    global_var.set_value('ifBoss', False)
    global_var.set_value('pressingX', False)
    global_var.set_value('DELTA_T', 17)
    global_var.set_value('ifShaking', False)
    global_var.set_value('shakeFrame', 0)
    global_var.set_value('restarting', False)

    running = True
    won = False 

    while running:
        pressed_keys = pygame.key.get_pressed()
        
        if not global_var.get_value('menu'):
            if global_var.get_value('levelPassSign') == True: 
                running = False
            elif global_var.get_value('ifGameOver') == True: 
                won = False
                running = False

            gF.doPause(pressed_keys, stage)
            if not global_var.get_value('pause'):
                gameRule.checkLife(player, stage)
                gameRule.checkPass(player, stage)

        stage.fill((0, 0, 0))
        screen.fill((0, 0, 0))
        DELTA_T = fpsClock.tick(FPS)
        global_var.set_value('DELTA_T', DELTA_T)

        global_var.set_value('grazing', False)
        global_var.set_value('item_getting', False) 
        global_var.set_value('enemyFiring1', False)
        global_var.set_value('enemyFiring2', False)
        global_var.set_value('enemyFiring3', False)
        global_var.set_value('kiraing', False)
        global_var.set_value('hitting', False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pressed_keys[K_F11]:
            running = False

        if not global_var.get_value('menu'):
            bulletSum, enemySum, boomSum = 0, 0, 0
            if not global_var.get_value('pause'):
                frame += 1
                if global_var.get_value('restarting'):
                    frame = 0
                    global_var.set_value('restarting', False)
            
            frameText = myfont.render('F: ' + str(frame), True, (255, 255, 255))
            
            if frame >= 600 * 60: diffLevel = 5
            elif frame >= 300 * 60: diffLevel = 4
            elif frame >= 120 * 60: diffLevel = 3
            elif frame >= 60 * 60: diffLevel = 2

            global_var.set_value('escPressing', pressed_keys[K_ESCAPE])
            if not global_var.get_value('pause'):
                player.update(pressed_keys, frame) 
            global_var.set_value('player1x', player.cx)
            global_var.set_value('player1y', player.cy)

            if not global_var.get_value('pause'):
                if global_var.get_value('levelSign') == 0:
                    lightnessLevel.stageController(stage, frame, enemys, bullets, slaves, items, effects, backgrounds, bosses, player)
                elif global_var.get_value('levelSign') == 1:
                    DuelClassLevel.stageController(stage, frame, enemys, bullets, slaves, items, effects, backgrounds, bosses, player)

            if not global_var.get_value('ifBoss') and frame <= 10600:
                stage.fill((0, 0, 0))

            if not global_var.get_value('pause'):
                global_var.set_value('ifStopPressing', False)
                if pressed_keys[K_z]:
                    player.fire(frame, stage, playerGuns)
                    if frame % 5 == 0:
                        shoot_sound.stop()
                        shoot_sound.play()
                
                for background in backgrounds: background.update(stage)
                if pressed_keys[K_LSHIFT]:
                    angle = angle - 2
                    global_var.set_value('shift_down', True)
                    player.itemCollectDistance = 100
                    if angle <= 0: angle = 360
                    gF.drawRotation(point2, (player.rect.centerx - 48, player.rect.centery - 48), -angle, stage)
                else:
                    global_var.set_value('shift_down', False)
                    player.itemCollectDistance = 50

                for playerGun in playerGuns: playerGun.update(stage)
                for effect in effects:
                    if effect.lower: effect.update(stage)
                
                global_var.set_value('enemyPos', (0, 0, 10000))
                for enemy in enemys:
                    enemy.update(stage, frame, bullets, bullets2, effects, items)
                    enemySum += 1

                for boss in bosses:
                    boss.update(stage, frame, items, effects, bullets, backgrounds, enemys, slaves, player)

                gameRule.drawPlayer(stage, player, frame)
                gameRule.itemAllGet(items, player, effects)

                for item in items:
                    item.update(stage, player, effects)
                    if item.distance <= player.itemCollectDistance: item.followPlayer = 1
                    if item.type == 0 and player.power == 400:
                        item.type = 4; item.initial(item.tx, item.ty)
                    if item.type == 3 and player.power == 400:
                        item.type = 2; item.initial(item.tx, item.ty)
                
                if player.lastLevel <= 3 and player.power >= 400: effects.add(Effect.powerMaxText())
                if player.lastLife < player.life: effects.add(Effect.extendText())
                if player.lastGraze < player.graze:
                    new_effect = Effect.grazeEffect()
                    new_effect.initial((player.tx, player.ty), 4, random.randint(15, 20), (255, 255, 255), 5, 1, 20)
                    effects.add(new_effect)

                for effect in effects:
                    if not (effect.upper or effect.lower): effect.update(stage)
                for bullet in bullets:
                    bulletSum += 1; bullet.update(stage, bullets, effects)
                for effect in effects:
                    if effect.upper: effect.update(stage)
                for slave in slaves: slave.update(stage, frame, bullets, effects, items)

                gameRule.missDetect(player, bullets, enemys, effects, miss_sound, items, slaves)
                gameRule.doBoom(player, booms, pressed_keys, slash_sound, items)

                for boom in booms:
                    boom.update(stage, effects)
                    if player.__class__.__name__ == "Marisa":
                        if boom.lastFrame == 599 and boom.ifBoss == False:
                            gameRule.addLastingCancel(boom.tx, boom.ty, slaves, 20, True)
                            for enemy in enemys: enemy.health -= 2000
                            slash_sound.play()
                            global_var.get_value('nep_sound').stop()
                    if player.__class__.__name__ == "Reimu": boomSum += 1
                if player.__class__.__name__ == "Reimu" and boomSum == 0:
                    global_var.get_value("nep_sound").stop()
                    global_var.set_value('boomStatu', 0)

                if pressed_keys[K_LSHIFT]: gF.drawRotation(point, (player.rect.centerx - 48, player.rect.centery - 48), angle, stage)
                gameRule.hitEnemy(enemys, playerGuns, booms, bullets, effects, frame, player, items, bosses, slaves)
                
                global_var.set_value('pressingX', True if pressed_keys[K_x] else False)
                missText = myfont.render('Life: ' + str(player.life), True, (255, 255, 255))
                stage.blit(missText, (200, 0))

                gF.shakeScreen()
                if global_var.get_value('ifShaking'):
                    if frame % 2 == 0:
                        d_x, d_y = random.randint(-5, 5), random.randint(-8, 8)
                    screen.blit(stage, (0 + d_x, 0 + d_y))
                else:
                    screen.blit(stage, (60, 30), (60, 30, 600, 660))

            gF.pauseScreen(pressed_keys, pressed_keys_last, screen, frame, enemys, bullets, slaves, items, effects, backgrounds, bosses, player, booms, playerGuns, midfont)
            gF.drawBackground(screen)
            pygame.draw.rect(screen, (255, 255, 255), (58, 28, 563, 663), 2)
            gF.displayMenu(screen, stars)
            
            for boss in bosses:
                boss.drawHealthBar(screen)
                boss.drawTimer(screen, midfont)
                if not global_var.get_value('pause'):
                    if not boss.if_chSpellName: boss.drawSpellName(screen, midfont, player)
                    else: boss.drawSpellName(screen, chfont, player)
                    boss.drawCardBonus(screen, smallfont, player)
                boss.drawBossName(screen)
                boss.drawSpellNum(screen)
                boss.displayPercentHealth(screen, myfont)

            gF.showFpsBullet(screen, bigfont, frame, bulletSum, log)
            gameRule.displayUi(screen, player, bigfont, frame)
            screen.blit(frameText, (0, 0))

            global_var.set_value('enemySum', enemySum)
            global_var.set_value('bulletSum', bulletSum)
        else:
            mainMenu.update(screen, pressed_keys, pressed_keys_last, player, titleDec)
            if mainMenu.playerReset:
                player = DADcharacter.Reimu() if global_var.get_value('playerNum') == 0 else DADcharacter.Marisa()
                mainMenu.playerReset = False
                player.tx, player.ty = 337.0, 600.0
                player.power = 100
                if global_var.get_value('ifTest'):
                    player.power = testFire
                    frame = 10020 if global_var.get_value('levelSign') == 0 else 13020

        pressed_keys_last = pressed_keys
        pygame.display.flip()

    log.close()
    pygame.quit()
    return won