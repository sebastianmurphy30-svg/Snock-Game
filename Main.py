import pygame
from Helper import Vector2D
from Helper import Coordinate
from GameBoard import GameBoard
from Snake import Snake
from UserInputs import GetDirection
from UserInputs import CheckQuitGame

pygame.init()

Width = 30
Height = 25

Game = GameBoard(Width, Height, 30)

Game.Board.SetArrayValue(0,0,1)

Run = True
Direction = Vector2D(0, 1)
Player = Snake(0,0)
Clock = pygame.time.Clock()
SlowDownDuration = 0
InvisibleDuration = 0
TimeSinceLastSpawned = 100
PortalActive = False
NewSnakeCoordinates = []
NewSnakeCoordinateValues = []



while Run:
    Events = pygame.event.get()

    Direction = GetDirection(Direction, Events, Player.Length)
    NewSnakeHeadPosition = Coordinate(Player.SnakeHead.ReturnAddVector(Direction).X, Player.SnakeHead.ReturnAddVector(Direction).Y)

    TimeSinceLastSpawned = Game.WaveSpawn(len(Game.Apples), TimeSinceLastSpawned + 1, NewSnakeHeadPosition)

    Player.Eat(Game.Board.GetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y))

    if Game.Board.GetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y) > 2:
        Game.Board.SetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y, 0)
        Game.RemoveApple(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y)
    else:
        Game.Board.SetArrayValue(NewSnakeHeadPosition.X, NewSnakeHeadPosition.Y, 0)

    if not Player.Invisible:
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
