import math

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def mag(a):
    return math.sqrt(dot(a, a))
def norm(a):
    return [a[0] / mag(a), a[1] / mag(a), a[2] / mag(a)]

v = [1, 1, 0]
v2 = [50000, 1000000, 0]
ap_v2 = [0.26, 0.74, 0]

print(dot(norm(v), norm(v2)))

import pygame
from pygame import Vector2, Vector3

pygame.init()

scale = 1
WIDTH, HEIGHT = (800, 800)
screen_size = Vector2(WIDTH, HEIGHT)

scr = pygame.Surface(screen_size, pygame.SRCALPHA)
disp = pygame.display.set_mode((int(screen_size.x * scale), int(screen_size.y * scale)))
clock = pygame.time.Clock()

pos = Vector3(WIDTH, HEIGHT, 0.0) / 2.0
sc = Vector3(50.0, 50.0, 50.0)
tri = [
    Vector3(0, 0, 0),
    Vector3(1, 0, 0),
    Vector3(0, 1, 0),
]

while 1:
    dt = clock.tick(60)*.001
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE)):
            pygame.quit()
            quit()
        
    # update logic here
        
    scr.fill((30,20,30))

    brightness = 0.0

    mp = pygame.mouse.get_pos()
    light = Vector3(mp[0], mp[1], 1)

    transformed_tri = [p.elementwise() * sc + pos for p in tri]
    a = transformed_tri[0]
    b = transformed_tri[1]

    plane = (b - a).normalize()
    to_light = (light - a).normalize()
    brightness = to_light * plane
    brightness *= 255
    brightness = abs(brightness)
    print(brightness)

    # draw triangle
    # draw polygon
    tri_2d = [(p.x, p.y) for p in transformed_tri] 

    pygame.draw.polygon(scr, (brightness,)*3, tri_2d)

    # draw light
    pygame.draw.circle(scr, (255, 255, 255), (int(light.x), int(light.y)), 5)

    pairs = []
    for i, p in enumerate(transformed_tri):
        pairs.append((p, transformed_tri[(i+1) % 3]))
    for pair in pairs:
        pygame.draw.line(scr, (255, 0, 0), pair[0][:2], pair[1][:2])

    # draw to_light vector
    #pygame.draw.line(scr, (0, 255, 0), a.xy, light.xy) 

    #pygame.draw.line(scr, (0, 0, 255), a.xy, b.xy)
    plane = (b - a).normalize() * 50
    plane_end = a + plane
    pygame.draw.line(scr, (0, 0, 255), a.xy, plane_end.xy)
    pygame.draw.line(scr, (255, 0, 0), a.xy, (a+to_light*100).xy ) 

    na = light - a
    nb = plane.normalize()
    na_proj_nb = nb.elementwise() * (na * nb)
    na_p_nb_end = a + na_proj_nb
    pygame.draw.line(scr, (255, 255, 0), a.xy, na_p_nb_end.xy)


    
    pygame.transform.scale(scr, disp.get_size(), disp)
    pygame.display.flip()
    
