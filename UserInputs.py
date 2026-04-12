import pygame
from Helper import Vector2D

def GetDirection(OldDirection, Events, SnakeLength):
    for event in Events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (OldDirection.Y != 1 or SnakeLength == 0):
                return Vector2D(0, -1)
            elif event.key == pygame.K_DOWN and (OldDirection.Y != -1 or SnakeLength == 0):
                return Vector2D(0, 1)
            elif event.key == pygame.K_LEFT and (OldDirection.X != 1 or SnakeLength == 0):
                return Vector2D(-1, 0)
            elif event.key == pygame.K_RIGHT and (OldDirection.X != -1 or SnakeLength == 0):
                return Vector2D(1, 0)

    return OldDirection

def CheckQuitGame(Events):
    for event in Events:
        if event.type == pygame.QUIT:
            return True

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        return True

    return False


