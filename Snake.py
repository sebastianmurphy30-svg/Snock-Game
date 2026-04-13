from Scripts.Helper import Coordinate
import random
import math

class Snake():
    def __init__(self, StartingX, StartingY):
        self.SnakeHead = Coordinate(StartingX, StartingY)
        self.Length = 20 #Excludes Head
        self.GreatestLength = 0
        self.WaveGreatestLength = 0
        self.SegmentVectors = []
        self.State = 1
        self.Speed = 18
        self.Points = 0
        self.SnakeLengthTransfer = 0
        self.SaveLength = True
        self.Invisible = False

    def Move(self, Direction):
        self.SnakeHead.AddVector(Direction)
        self.SegmentVectors.append(Direction)

        if len(self.SegmentVectors) > self.Length:
            for i in range(len(self.SegmentVectors) - self.Length):
                self.SegmentVectors.pop(0)

    def ReturnCoordinates(self):
        Coordinates = []
        CoordinateValues = []

        NewCoordinate = Coordinate(self.SnakeHead.X, self.SnakeHead.Y)
        Coordinates.append(NewCoordinate)
        CoordinateValues.append(1)
        for i in reversed(range(len(self.SegmentVectors))):
            NewCoordinate = NewCoordinate.ReturnAddVector(self.SegmentVectors[i].Inverse())
            Coordinates.append(NewCoordinate)
            CoordinateValues.append(2)

        return Coordinates, CoordinateValues

    def NextPosition(self, Direction):
        return self.SnakeHead.ReturnAddVector(Direction)

    def Grow(self, GrowthAmount):
        self.Length = self.Length + GrowthAmount

    def Shrink(self, ShrinkAmount):
        if self.Length == 0:
            pass
        else:
            self.Length = max(0, self.Length - ShrinkAmount)
            for i in range(min(ShrinkAmount, len(self.SegmentVectors))):
                self.SegmentVectors.pop(0)

    def Eat(self, Object, CurrentWave):
        #-1 = Wall; 1 = Snake Head; 2 = Snake Body
        if Object == -1  or Object == 1 or Object == 2:
            self.State = 0
        elif Object == -2:
            self.State = 2
        elif Object > 2:
            if Object == 3:
                self.Grow(1)
                self.Points += 1 * max(math.floor(CurrentWave) / 5, 1)
            elif Object == 4:
                if random.randint(1,2) == 1:
                    self.Grow(1)
                    self.Points += 2 * max(math.floor(CurrentWave) / 5, 1)
                else:
                    self.Grow(2)
                    self.Points += 1 * max(math.floor(CurrentWave) / 5, 1)
            elif Object == 5:
                if random.randint(1,4) == 1:
                    self.State = 0
                    print("HI")
                else:
                    self.Shrink(3)
                    print("Bye")
            elif Object == 6:
                self.Grow(random.randint(0,3))
                self.Points += random.randint(0,5) * max(math.floor(CurrentWave) / 5, 1)
            elif Object == 7:
                self.Speed = (self.Speed / 2)
                self.Points = max(0, self.Points - 2) * max(math.floor(CurrentWave) / 5, 1)
            elif Object == 8:
                self.Invisible = True
                self.Points += 5 * max(math.floor(CurrentWave) / 5, 1)



    def Update(self, Direction):
        if self.Length > self.GreatestLength:
            self.GreatestLength = self.Length

        if self.Length > self.WaveGreatestLength:
            self.WaveGreatestLength = self.Length

        if self.State == 1:
            self.Move(Direction)
        elif self.State == 2:
            if self.SaveLength:
                self.SnakeLengthTransfer = self.Length
                self.SaveLength = False
            if self.Length > 0:
                self.Shrink(1)
            else:
                self.State = 1
                self.Length = self.SnakeLengthTransfer
                self.SaveLength = True
        else:
            if self.Length > 0:
                self.Shrink(1)
            else:
                NewCoordinates, NewCoordinateValues = self.ReturnCoordinates()
                return False, NewCoordinates, NewCoordinateValues

        NewCoordinates, NewCoordinateValues = self.ReturnCoordinates()
        return True, NewCoordinates, NewCoordinateValues

"""
G = Snake(1,0)
G.Move(Vector2D(1,0))
G.Move(Vector2D(0,1))
Coordinates = G.ReturnCoordinates()

for i in range(len(Coordinates)):
    print("(", Coordinates[i].X, ",", Coordinates[i].Y, ")")

input("Press ENTER to continue...")

print("")

G.Eat(3)
G.Move(Vector2D(1,0))
Coordinates = G.ReturnCoordinates()

for i in range(len(Coordinates)):
    print("(", Coordinates[i].X, ",", Coordinates[i].Y, ")")

input("Press ENTER to continue...")

print("")

G.Shrink(1)
G.Move(Vector2D(1,0))
Coordinates = G.ReturnCoordinates()

for i in range(len(Coordinates)):
    print("(", Coordinates[i].X, ",", Coordinates[i].Y, ")")
print(G.Length)

"""