import pygame
from Scripts.Helper import Vector2D
from Scripts.Helper import Coordinate
from Scripts.GameBoard import GameBoard
from Scripts.Snake import Snake
from Scripts.UserInputs import GetDirection
from Scripts.UserInputs import CheckQuitGame
import os
import sys

pygame.init()
pygame.mixer.init()

def ResourcePath(RelativePath):
    try:
        BasePath = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        BasePath = os.path.abspath(".")

    return os.path.join(BasePath, RelativePath)

Width = 30
Height = 25

Game = GameBoard(Width, Height, 30)

Game.Board.SetArrayValue(0,0,1)

Run = True
Direction = Vector2D(1, 0)
Player = Snake(0,0)
Clock = pygame.time.Clock()
SlowDownDuration = 0
InvisibleDuration = 0
TimeSinceLastSpawned = 100
PortalActive = False
NewSnakeCoordinates = []
NewSnakeCoordinateValues = []

pygame.mixer.music.load(ResourcePath("Music/BackgroundMusic.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

while Run:
    Events = pygame.event.get()

    Direction = GetDirection(Direction, Events, Player.Length, Player.State)
    NewSnakeHeadPosition = Coordinate(Player.SnakeHead.ReturnAddVector(Direction).X, Player.SnakeHead.ReturnAddVector(Direction).Y)

    TimeSinceLastSpawned = Game.WaveSpawn(len(Game.Apples), TimeSinceLastSpawned + 1, NewSnakeHeadPosition)

    Player.Eat(Game.Board.GetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y), Game.Wave)

    if Game.Board.GetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y) > 2:
        Game.Board.SetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y, 0)
        Game.RemoveApple(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y)
    else:
        Game.Board.SetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y, 0)

    if Player.State == 2:
        if Direction.X == 1 and Direction.Y == 0:
            Run, NewSnakeCoordinates, NewSnakeCoordinateValues = Player.Update(Direction)
            NewSnakeCoordinates.pop(0)
            NewSnakeCoordinateValues.pop(0)

            for i in range(len(NewSnakeCoordinates)):
                NewSnakeCoordinates[i].AddVector(Player.SegmentVectors[i])
        else:
            Run, NewSnakeCoordinates, NewSnakeCoordinateValues = Player.Update(Direction)

    elif not Player.Invisible:
        Run, NewSnakeCoordinates, NewSnakeCoordinateValues = Player.Update(Direction)
    else:
        Run, NewSnakeCoordinates, NewSnakeCoordinateValues = Player.Update(Direction)
        NewSnakeCoordinates.clear()
        NewSnakeCoordinateValues.clear()

        InvisibleDuration += 1

        if InvisibleDuration >= 25:
            Player.Invisible = False


    Game.ClearBoard()
    Game.UpdateApples()
    Game.Board.SetMultipleArrayValues(NewSnakeCoordinates, NewSnakeCoordinateValues)
    Game.UpdatePortal()

    if Player.Speed != 16:
        SlowDownDuration += 1

        if SlowDownDuration >= 65:
            Player.Speed = 16
            SlowDownDuration = 0
            print(Player.Speed)


    if Game.CheckSpawnPortal(Player.WaveGreatestLength) == True and not PortalActive:
        PortalActive = True
        Game.SpawnPortal()

    if PortalActive and Player.Length == 0 and Player.State != 0:
        Player.SnakeHead = Coordinate(0,0)
        Game.NextWave()
        Player.WaveGreatestLength = 0
        Game.Portal = False
        PortalActive = False
        Direction = Vector2D(1, 0)

    if CheckQuitGame(Events):
        Run = False
        print(Player.Points)
        pygame.quit()
        break

    if Player.State != 0:
        pygame.display.set_caption(f"    Wave: {Game.Wave}   Length: {Player.Length}   Points: {Player.Points}                                                                     Snock")
    Game.DrawBoard()

    Clock.tick(Player.Speed)

while True:
    Events = pygame.event.get()

    pygame.display.set_caption(
        f"    Wave: {Game.Wave}   Length: {Player.SnakeLengthTransfer}   Points: {Player.Points}                                                                   Game Over")

    if CheckQuitGame(Events):
        Run = False
        print(Player.Points)
        pygame.quit()
        break

    Game.DrawBoard()
