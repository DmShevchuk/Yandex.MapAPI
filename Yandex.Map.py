import pygame
import requests
import os

map_request = 'http://static-maps.yandex.ru/1.x/'

longitude = 31.268856
lattitude = 58.523656
delta = 0.002
foto = ''


def map():
    global foto
    map_params = {
        'll': ','.join([str(longitude), str(lattitude)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "map"
    }
    try:
        response = requests.get(map_request, params=map_params)
        map = 'map.png'
        with open(map, 'wb') as photo:
            photo.write(response.content)
        photo = pygame.image.load(map)
        os.remove(map)
        foto = photo

    except pygame.error:
        pass


map()

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
                if delta * 2 <= 66:
                    delta *= 2
            if event.key == 259:
                if delta / 2 >= 0.0005:
                    delta /= 2

            if event.key == pygame.K_UP:
                if lattitude + delta <= 83:
                    lattitude += delta

            if event.key == pygame.K_DOWN:
                if lattitude - delta >= -83:
                    lattitude -= delta

            if event.key == pygame.K_RIGHT:
                if longitude + delta > 180:
                    longitude = -180
                else:
                    longitude += delta

            if event.key == pygame.K_LEFT:
                if longitude - delta < -180:
                    longitude = 180
                else:
                    longitude -= delta
            map()

    screen.blit(foto, (0, 0))
    pygame.display.flip()
