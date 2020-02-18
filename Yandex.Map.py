import pygame
import requests
import os

map_request = 'http://static-maps.yandex.ru/1.x/'

longitude = '31.268856'
lattitude = '58.523656'
delta = 0.002

map_params = {
    'll': ','.join([longitude, lattitude]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": "map"
}


def map():
    map_params = {
        'll': ','.join([longitude, lattitude]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "map"
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

screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 265:
                if delta >= 0.012:
                    delta += 0.1
                else:
                    delta += 0.005
            if event.key == 259:
                if delta > 0.112:
                    delta -= 0.1
                else:
                    if delta - 0.005 > 0:
                        delta -= 0.005
    screen.blit(map(), (0, 0))
    pygame.display.flip()
