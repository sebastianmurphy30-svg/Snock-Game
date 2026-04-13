class Array2D:
    def __init__(self, XSize, YSize):
        self.XSize = XSize + 1
        self.YSize = YSize + 1
        self.Array = []

        for i in range(self.YSize):
            self.Array.append([])
            for k in range(self.XSize):
                self.Array[i].append(0)

    def PrintArray(self):
        for i in range(len(self.Array)):
            print(self.Array[i])

    def SetArrayValue(self, X, Y, Value):
        if self.YSize - 1 >= Y and self.XSize - 1 >= X:
            self.Array[Y][X] = Value

    def SetMultipleArrayValues(self, Coordinates, Values):
        for i in range(len(Coordinates)):
            if self.YSize > Coordinates[i].Y and self.XSize > Coordinates[i].X and self.YSize >= 0 and self.XSize >= 0:
                self.SetArrayValue(Coordinates[i].X, Coordinates[i].Y, Values[i])

    def GetArrayValue(self, X, Y):
        if Y >= self.YSize - 1 or Y < 0 or X >= self.XSize - 1 or X < 0:
            return -1
        else:
            return self.Array[Y][X]

class Vector2D:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def Inverse(self):
        return Vector2D(self.X * -1, self.Y * -1)

class Coordinate:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def AddVector(self, Vector):
        self.X += Vector.X
        self.Y += Vector.Y

    def ReturnAddVector(self, Vector):
        return Coordinate(self.X + Vector.X, self.Y + Vector.Y)

    def DistanceBetweenCoordinates(self, OtherCoordinate):
        return abs(self.X - OtherCoordinate.X) + abs(self.Y - OtherCoordinate.Y)


#G = Array2D(5,5)
#G.SetArrayValue(0,4, 2)
#G.PrintArray()