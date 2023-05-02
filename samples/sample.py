
import pygame as pg
import csv
import os, moderngl, random
from array import array
import math, numpy as np
from player import Player


def main():
    camera = pg.math.Vector2(160, 160)
    screen_size = pg.math.Vector2(960, 640)
    internal_frame = 0
    animation_frame = 12

    tileMap = []
    with open(os.path.join("samples/assets/tilemap/test.csv")) as tiling:
        tiling = csv.reader(tiling, delimiter=",")
        for row in tiling:
            tileMap.append(row)
    pg.init()
    pg.font.init()
    font = pg.font.SysFont('Lato', 30)

    canvas = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
    display = pg.Surface((800, 600))
    ctx = moderngl.create_context()
    quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
    ]))
    # myImage = Image.open("src\img.png")
    # myImage = myImage.resize((32, 32))
    # myImage.save("newimg.png")
    image_surc = pg.image.load("samples/newimg.png")
    vert_shader = '''
    #version 330 core

    uniform float zoomFactor;
    uniform vec2 playerPos;

    in vec2 vert;
    in vec2 texcoord;
    out vec2 uvs;

    void main() {
        uvs = texcoord;
        uvs *= zoomFactor;
        uvs.x -= playerPos.x;
        gl_Position = vec4(vert, 0.0, 1.0);
    }
    '''

    frag_shader = '''
    #version 330 core

    uniform sampler2D tex;
    uniform float time;
    uniform float scareFactor;

    in vec2 uvs;
    out vec4 fragColor;

    void main() {
        float t = time;
        float s = scareFactor;
        vec3 current_color = texture(tex, uvs).rgb;
        vec2 zoomed_sample = vec2(uvs.x, uvs.y);
        vec4 shadow_color;
        vec2 sample_pos = vec2(uvs.x + cos(time) * scareFactor, uvs.y);
        fragColor = vec4(texture(tex, sample_pos).r, texture(tex, uvs).gb, 1.0);
        
        sample_pos = vec2(uvs.x, uvs.y + cos(time) * 0.002);
        fragColor += vec4(texture(tex, uvs).rg, texture(tex, sample_pos).b, 0.0); 
        if(uvs.y > sin(time*0.01) && uvs.y < sin(time*0.01)+0.001){
            fragColor.r = 1;
        }
        if(uvs.y > sin(time*0.01)+0.02 && uvs.y < sin(time*0.01)+0.021){
            fragColor.b = 1;
        }
        if(uvs.y > sin(time*0.01)+0.03 && uvs.y < sin(time*0.01)+0.031){
            fragColor.g = 1;
        }
        
        shadow_color = vec4(texture(tex, zoomed_sample).rg, texture(tex, zoomed_sample).b+10, 1.0);
        fragColor = mix(fragColor, shadowColor, 1.0);
        //fragColor = vec4(texture(tex, uvs).rgb, 1.0);
    }
    '''
    #uniform float time;
#vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 10 + time * 0.01) * 0.1, uvs.y);
    program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
    render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_texture(surf):
        tex = ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    def img_to_texture(surf):
        tex = ctx.texture((32, 32), 3)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex   
    def circle_surf(radius, color):
        surf = pg.Surface((radius * 2, radius * 2))
        pg.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf
    t = 1
    clock = pg.time.Clock()

    enemy = Player(.6)
    player = Player(3)
    player.setPos(screen_size.x/2, screen_size.y/2)
    enemy.setPos(32+camera.x + screen_size.x/2, 32)

    pg.display.set_caption("My Board")
    exit = False
    isLoading = True
    loading = font.render("Loading", True, pg.Color(255, 255, 255))
    canvas.convert_alpha()
    while not exit:
        t += 1
        internal_frame += 1
        
        text = font.render(
            str(clock.get_fps()) + " x:" +
            str(round((player.rect.x + camera.x)/ 32)) + " y:" +
            str(round(player.rect.y / 32)), True, pg.Color(255, 0, 255))
        # if isLoading:
        #     canvas.blit(loading, (160 - loading.get_rect().width/2, 160 - loading.get_rect().height/2))
        
        if internal_frame % animation_frame == 0:
            player.spriteY = 64 if player.spriteY == 0 else 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = True
            player.registerEvent(event)
        for x in range(len(tileMap)):
            for y in range(len(tileMap[x])):
                gxp = round((player.rect.x +camera.x) / 32)
                gyp = round(player.rect.y / 32) 
                color = pg.Color(0,0, 0)
                if (gxp == x and gyp == y) or (gxp-1 == x and gyp == y)or (gxp+1 == x and gyp == y)or (gxp == x and gyp-1 == y)or (gxp == x and gyp+1  == y) or int(tileMap[x][y]) > 1:
                    color = pg.Color((0,0, 0))
                pg.draw.rect(
                    canvas,
                    color,
                    pg.Rect((x*32 - camera.x, y*32, 32, 32))
                )
        enemyAngle = math.atan2(player.rect.y- enemy.rect.y, player.rect.x - enemy.rect.x)
        enemy.moveY = 1 if math.sin(enemyAngle) > 0 else -1
        enemy.moveX = 1 if math.cos(enemyAngle) > 0 else -1
        
        enemy.rect.x += enemy.moveX * enemy.speed 
        enemy.rect.y += enemy.moveY * enemy.speed

        enemyXoffset = enemy.rect.x - camera.x

        
        player.move(camera)
        
        pg.draw.circle(canvas, (150, 150, 150),(player.rect.centerx - player.width/2, player.rect.centery- player.height/2), 90)
        canvas.blit(circle_surf(100, (10, 10, 10)), (player.rect.centerx - player.width/2 - 100, player.rect.centery - 100 - player.height/2), special_flags=pg.BLEND_RGB_ADD)
        pg.draw.rect(canvas, pg.Color(255, 0, 0), pg.Rect(enemyXoffset, enemy.rect.y, 32, 32), 0)
        player.blitPlayer(canvas)

            # --- modify surface ---
    
        surface_mod = canvas.copy()
        surface_mod_rect = surface_mod.get_rect()

        # if zoom:
        scale = 1 #max(math.cos(t) * 1.05,1)
        surface_mod = pg.transform.rotozoom(surface_mod, 0, scale)
        surface_mod_rect = surface_mod.get_rect()
        # else:
        #     scale = 1
        
        # if follow_player:
        surface_mod_rect.x = (canvas.get_rect().centerx - player.rect.centerx*scale)
        surface_mod_rect.y = (canvas.get_rect().centery - player.rect.centery*scale)
        # else:
        #     surface_mod_rect.center = screen_rect.center

    # --- draw surface on screen ---
        canvas.fill((0, 0, 0, 0))
        canvas.blit(surface_mod, surface_mod_rect)
        canvas.blit(text, (0, 0))
        frame_tex = surf_to_texture(canvas)
        frame_tex.use(0)

        new_value = [0, 0]
        # new_value[0] = ((player.rect.x) / (800) ) * 1
        # new_value[1] = ((player.rect.y) / (600) ) * 1
        # new_value[0] = math.sin(max(0,t)) * 0.001
        

        program['tex'] = 0
        program['time'] = t
        zoomParam = 0
        program['zoomFactor'] = 1 #random.uniform(1-zoomParam, 1+zoomParam)
        program['scareFactor'] = math.sin(t) * (zoomParam * 1.5)

        program['playerPos'] = new_value

        render_object.render(mode=moderngl.TRIANGLE_STRIP)   

        enemy.blitPlayer(canvas)
        pg.display.flip()
        frame_tex.release()
        clock.tick(60)


if __name__ == "__main__":
    main()
