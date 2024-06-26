import os
import random
import sys
import pygame as pg # type: ignore


WIDTH, HEIGHT = 1200, 600
D={pg.K_UP: (0, -5),
   pg.K_DOWN: (0, +5),
   pg.K_LEFT: (-5, 0),
   pg.K_RIGHT: (+5, 0),}
# A = {
#     (+5, 0): pg.transform.rotozoom(pg.image, 0, 2.0),
#     (+5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
#     (0, +5): pg.transform.rotozoom(),
#     (-5, +5): pg.transform.rotozoom(),
#     (-5, 0): pg.transform.rotozoom(),
#     (-5, -5): pg.transform.rotozoom(),
#     (0,  -5): pg.transform.rotozoom(),
#     (+5, -5): pg.transform.rotozoom(),
#     }

angle = 0

accs = [a for a in range(1,11)]
for r in range(1, 11):
    bb_img = pg.Surface((20*r,20*r))
    pg.draw.circle(bb_img, (255,0,0),(10*r, 10*r), 10*r)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen, kk_rct):

    font = pg.font.Font(None, 100)
    text = font.render("Game over",True, (255,0,0))
    text_rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))
    black=pg.Surface((WIDTH,HEIGHT))
    black.set_alpha(128)
    black.fill((0,0,0))
    cry= pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    cryrct= cry.get_rect(center=kk_rct.center)
    cry2= pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    cryrct2= cry.get_rect(center=(WIDTH-kk_rct[0],HEIGHT-kk_rct[1]))#対角線にこうかとんが位置する
    screen.blit(black,(0,0))
    screen.blit(cry,cryrct)
    screen.blit(cry2,cryrct2)
    screen.blit(text,text_rect)
    pg.display.update()#画面の更新
    pg.time.wait(5000)#これで５秒間表示

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:#pg.Rectを書くことでこの型だと記入したことになる
    """
    引数:こうかとんRectが爆弾Rect
    戻り値：タプル（縦横判定結果）
    画面内ならTrue,外ならFalse
    """
    yo, ta = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yo = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        ta = False
    return yo, ta


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))#一辺が20の空のsurfaceを作成
    pg.draw.circle(bb_img, (255,0,0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0,HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    # avx = vx*bb_accs[min(tmr//500, 9)]
    # bb_img = bb_imgs[min(tmr//500, 9)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 
        if kk_rct.colliderect(bb_rct):
            return gameover(screen, kk_rct)
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in D.items():
            if key_lst[k]: #辞書から常に取り出される
                 sum_mv[0] += v[0]
                 sum_mv[1] += v[1]
                 
                 
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#画面外に行けないように設定
            
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yo,ta = check_bound(bb_rct)
        if not yo:
            vx *= -1
        if not ta:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        # avx = vx*accs[min(tmr//500, 9)]
        # bb_img = bb_img[min(tmr//500, 9)]
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
