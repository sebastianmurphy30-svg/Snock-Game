import pygame
from Scripts.Helper import Array2D
from Scripts.Helper import Coordinate
import random
import numpy as np
import math

class GameBoard():
    def __init__(self, Width, Height, GridBlockSize):
        #Pygame
        pygame.init()
        pygame.display.set_caption('Snock')
        self.Screen = pygame.display.set_mode((Width * GridBlockSize, Height * GridBlockSize))

        #Board
        self.Width = Width
        self.Height = Height
        self.Board = Array2D(Width, Height)

        #Visual Sizes
        self.GridBlockSize = GridBlockSize

        #Colors
        self.Red = (255, 0, 0)
        self.Green = (0, 255, 0)
        self.DarkGreen = (0, 200, 0)
        self.Blue = (0, 0, 255)
        self.White = (255,255,255)
        self.Orange = (255, 165, 0)
        self.Yellow = (255, 223, 0)
        self.Cyan = (0, 255, 255)
        self.Pink = (255,77,225)

        #Apples
        self.Apples = []
        self.AppleTypes = []
        self.AllAppleTypes = [3,4,5,6,7,8]

        #Wave
        self.Wave = 1
        self.Portal = False

    def DrawBoard(self):
        self.Screen.fill((0, 0, 0))

        for Y in range(len(self.Board.Array)):
            for X in range(len(self.Board.Array[Y])):
                if self.Board.GetArrayValue(X, Y) != 0:
                    if self.Board.GetArrayValue(X, Y) == -2:
                        pygame.draw.rect(self.Screen, self.Cyan, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 1:
                        pygame.draw.rect(self.Screen, self.DarkGreen, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 2:
                        pygame.draw.rect(self.Screen, self.Green, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 3:
                        pygame.draw.rect(self.Screen, self.Red, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 4:
                        pygame.draw.rect(self.Screen, self.Blue, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 5:
                        pygame.draw.rect(self.Screen, self.White, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 6:
                        pygame.draw.rect(self.Screen, self.Orange, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 7:
                        pygame.draw.rect(self.Screen, self.Yellow, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))
                    elif self.Board.GetArrayValue(X, Y) == 8:
                        pygame.draw.rect(self.Screen, self.Pink, pygame.Rect(X * self.GridBlockSize, Y * self.GridBlockSize, self.GridBlockSize, self.GridBlockSize))

        pygame.display.update()

    def ClearBoard(self):
        for Y in range(len(self.Board.Array)):
            for X in range(len(self.Board.Array[Y])):
                self.Board.SetArrayValue(X, Y, 0)

    def SpawnApple(self, PositionX, PositionY, Type):
        self.Apples.append(Coordinate(PositionX, PositionY))
        self.AppleTypes.append(Type)

    def RemoveApple(self, PositionX, PositionY):
        for i in reversed(range(len(self.Apples))):
            if self.Apples[i].X == PositionX and self.Apples[i].Y == PositionY:
                self.Apples.pop(i)
                self.AppleTypes.pop(i)

    def UpdateApples(self):
        self.Board.SetMultipleArrayValues(self.Apples, self.AppleTypes)

    def SpawnAppleAtRandom(self, SnakeHeadPosition, Type):
        ApplePosition = Coordinate(random.randint(0, self.Width - 1), random.randint(0, self.Height - 1))
        while self.Board.GetArrayValue(ApplePosition.X, ApplePosition.Y) != 0 or ApplePosition.DistanceBetweenCoordinates(SnakeHeadPosition) <= 5:
            ApplePosition = Coordinate(random.randint(0, self.Width - 1), random.randint(0, self.Height - 1))

        self.SpawnApple(ApplePosition.X, ApplePosition.Y, Type)

        pygame.display.update()

    def SelectRandomApple(self):
        #RegularAppleProbability = 100 - ((min(self.Wave * 25, 75) + 15 * (min(max(self.Wave - 3, 0), 1))))
        #DoubleAppleProbability = 25
        #BombAppleProbability = 10 * min(max(self.Wave - 2, 0), 2)
        #GambleAppleProbability = (15 * min(max(self.Wave - 1, 0), 1)) + 10 * min(max((self.Wave - 2), 0), 1)
        #TimeAppleProbability = (5 * min(max(self.Wave - 2, 0), 2)) + 10 * min(max(self.Wave - 1, 0), 1)

        RegularAppleProbability = [65, 50, 35, 25, 20]
        DoubleAppleProbability = [35, 40, 35, 30, 30]
        BombAppleProbability = [0, 0, 5, 10, 10]
        TimeAppleProbability = [0, 5, 10, 10, 10]
        GambleAppleProbability = [0, 10, 15, 20, 20]
        InvisibleAppleProbability = [0, 0, 0, 5, 10]

        Probabilities  = []

        if self.Wave <= 5:
            Weights = [RegularAppleProbability[self.Wave - 1] / 100, DoubleAppleProbability[self.Wave - 1] / 100, BombAppleProbability[self.Wave - 1] / 100, GambleAppleProbability[self.Wave - 1] / 100, TimeAppleProbability[self.Wave - 1] / 100, InvisibleAppleProbability[self.Wave - 1] / 100]
        else:
            Weights = [RegularAppleProbability[-1] / 100, DoubleAppleProbability[-1] / 100, BombAppleProbability[-1] / 100, GambleAppleProbability[-1] / 100, TimeAppleProbability[-1] / 100, InvisibleAppleProbability[-1] / 100]

        for i in range(len(Weights)):
            Probabilities.append(Weights[i] / sum(Weights))

        return np.random.choice(self.AllAppleTypes, p=Probabilities)

    def SpawnFullyRandomApple(self, SnakeHeadPosition):
        self.SpawnAppleAtRandom(SnakeHeadPosition, self.SelectRandomApple())

    def WaveSpawn(self, CurrentlySpawned, LastTimeSpawned, SnakeHeadPosition):
        if CurrentlySpawned < min(self.Wave * 4, 16) and LastTimeSpawned > 35:
            for i in range(random.randint(1,3)):
                self.SpawnFullyRandomApple(SnakeHeadPosition)
            return 0
        else:
            return LastTimeSpawned

    def CheckSpawnPortal(self, WaveHighestSnakeLength):
        if WaveHighestSnakeLength > self.Wave * 6 - math.floor(4 * self.Wave / 3):
            return True
        else:
            return False

    def SpawnPortal(self):
        self.Portal = True

    def UpdatePortal(self):
        if self.Portal:
            self.Board.SetArrayValue(29,0, -2)

    def NextWave(self):
        self.Wave += 1
        self.ClearBoard()
        self.Apples.clear()
        self.AppleTypes.clear()



"""
G = GameBoard(30, 25, 30)
G.Board.SetArrayValue(0,0,1)
G.Board.SetArrayValue(1,0,2)
G.Board.SetArrayValue(2,0,2)
Run  = True

while Run:
    if CheckQuitGame():
        Run = False
        pygame.quit()

    G.DrawBoard()
    
"""


