import pygame
import requests
import os


map_request = 'http://static-maps.yandex.ru/1.x/'

longitude = '31.268856'
lattitude = '58.523656'
delta = '0.002'

map_params = {
    'll': ','.join([longitude, lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}


response = requests.get(map_request, params=map_params)

map = 'map.png'
with open(map, 'wb') as photo:
    photo.write(response.content)


pygame.init()

SIZE = [400, 400]

screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))

photo = pygame.image.load(map)
os.remove(map)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(photo, (0, 0))

    pygame.display.flip()
