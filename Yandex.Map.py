import pygame
import requests
import os

map_request = 'http://static-maps.yandex.ru/1.x/'

longitude = '31.268856'
lattitude = '58.523656'
delta = 0.002
type_map = 'map'
map_params = {
    'll': ','.join([longitude, lattitude]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": type_map
}


def map():
    map_params = {
        'll': ','.join([longitude, lattitude]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": type_map
    }
    response = requests.get(map_request, params=map_params)
    map = 'map.png'
    with open(map, 'wb') as photo:
        photo.write(response.content)
    photo = pygame.image.load(map)
    os.remove(map)
    return photo


pygame.init()

SIZE = [600, 450]
font = pygame.font.Font(None, 20)
screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))
text = font.render('Схема', 1, (0, 0, 0))
text_x, text_y = 425, 10
screen.blit(text, (text_x, text_y))
text = font.render('Гибрид', 1, (0, 0, 0))
text_x, text_y = 540, 10
screen.blit(text, (text_x, text_y))
text = font.render('Спутник', 1, (0, 0, 0))
text_x, text_y = 475, 10
screen.blit(text, (text_x, text_y))
pygame.draw.rect(screen, (0, 0, 0), (5, 5, 150, 30), 1)
text = font.render('Поиск', 1, (0, 0, 0))
text_x, text_y = 57, 14
screen.blit(text, (text_x, text_y))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 265:
                if delta >= 0.012:
                    delta *= 2
                else:
                    delta += 0.005
            if event.key == 259:
                if delta > 0.112:
                    delta -= 0.1
                else:
                    if delta - 0.005 > 0:
                        delta -= 0.005
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if 425 <= x <= 465 and 0 <= y <= 35:
                    type_map = 'map'
                if 475 <= x <= 530 and 0 <= y <= 35:
                    type_map = 'sat'
                if 540 <= x <= 590 and 0 <= y <= 35:
                    type_map = 'sat,skl'
                if 5 <= x <= 155 and 5 <= y <= 35:
                    pass
    screen.blit(map(), (0, 40))
    pygame.display.flip()
