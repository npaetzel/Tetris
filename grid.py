import tkinter, random, math, tetris, fileScores

class Grid:
    """The Grid class is the actual model of the game. """
    def __init__(self, root, cols, rows):
        self.root = root
        self.cols = cols
        self.rows = rows
        self.content = [[0 for col in range(self.cols)] for row in range(self.rows)]
        self.rowsFilled = [0 for row in range(self.rows)]
        self.blockNumber= 1
        self.currentBlock = None
        self.newBlock()

        self.highscores = fileScores.loadFile()
        self.newHighscore = False

        self.startLevel = self.level = 5
        self.cleared = 0
        self.score = 0

        self.timer = tetris.Timer()
        self.active = True
        self.frameCount = 0
        self.run()
    def run(self):
        """Is called in the mainloop but acts only after x frames. x depends on the current level."""
        if self.active and self.frameCount >= [53, 49, 45, 41, 37, 33, 28, 22, 17, 11, 10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3][self.level]:
            self.move(0, 1)
            self.frameCount = 0
        else:
            self.frameCount += 1
    def move(self, x, y):
        """Gets the order to let the current block move in the direction (x, y) relative to its current position and checks if the new position is legal and/or if the block has landed.
        x : int
            The horizontal direction the block has to move. A positive number makes it move to the right, a negative number makes it move to the left.
        y : int
            The vertical direction the block has to move. A positive number makes it fall down, a negative number makes the function end."""
        if x > 0: x=1
        elif x < 0: x=-1
        if y > 0: y=1
        elif y < 0: return False

        for tile in self.currentBlock.tiles:
            newX, newY = tile.x+x, tile.y+y
            if newX < 0 or newX > self.cols-1:
                #Checks if the new position hits the left or right edge of the Grid.
                return False
            elif y > 0 and (newY > self.rows-1 or self.content[newY][newX] > 0):
                #Checks if when falling down the block hits the lower edge of the grid or a former block.
                self.newBlock()
                self.checkRows()
                return False       
            elif self.content[newY][newX] > 0:
                #Checks if while not falling the block hits a former block.
                return False    
        self.currentBlock.move(x, y)
        return True
    def newBlock(self):
        """Saves the current block in the Grid's content and creates a new one."""
        if self.currentBlock != None:
            for tile in self.currentBlock.tiles:
                self.content[tile.y][tile.x] = self.blockNumber
            self.blockNumber += 1
        self.currentBlock = Block.createBlock(int(self.cols/2-1), 0)
        if self.isLost():
            self.active = False
            if self.highscores.checkScore(self.score):
                self.newHighscore = True
    def isLost(self):
        """Checks if the space beneath the new block is empty so the game isn't lost."""
        for tile in self.currentBlock.tiles:
            if self.content[tile.y+1][tile.x] > 0:
                return True
        return False
    def setScoreName(self, name):
        """Takes the name and calls fileScores.py to save the new highscore."""
        self.highscores.addScore(fileScores.Score(name, self.score))
        fileScores.saveFile(self.highscores)
        for score in iter(self.highscores):
            print(score.name, ': ', score.points)
    def checkRows(self):
        """Checks if and how many rows have to be deleted and also calculates the resulting points for the score and if the level has to be changed."""
        toDelete = 0
        self.rowsFilled = [0 for row in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.content[row][col] > 0:
                    self.rowsFilled[row] += 1
            if self.rowsFilled[row] >= self.cols:
                self.deleteRow(row)
                toDelete += 1
        if toDelete > 0:
            self.score += ([40, 100, 300, 1200][toDelete-1])*(self.level+1)
            self.cleared += toDelete
            self.level = min(int(self.cleared/10)+self.startLevel, 20)
        
    def deleteRow(self, rowToDelete):
        """Deletes a row and makes all upper rows fall down.
        rowToDelete : int
            The number of the row that has to be deleted."""
        for row in range(rowToDelete, 0, -1):
            for col in range(self.cols):
                self.content[row][col] = self.content[row-1][col]
            self.rowsFilled[row] = self.rowsFilled[row-1]
    def resetGame(self):
        """Resets the field and everything the player has achieved"""
        self.content = [[0 for col in range(self.cols)] for row in range(self.rows)]
        self.rowsFilled = [0 for row in range(self.rows)]

        self.level = self.startLevel
        self.cleared = 0
        self.score = 0
        self.active = True


class Tile:
    """A tile is a square that that fills one point of the Grid.
    x: int
        The horizontal position of the tile.
    y: int
        The vertical position of the tile."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def move(self, x, y):
        """Makes the tile move in the direction (x, y).
        x : int
            The horizontal direction the tile has to move. A positive value makes it move to the right, a negative value makes it move to the left.
        y : int
            The vertical direction the tile has to move. A positive value makes it move downwards, a negative value makes it move upwards."""
        self.x += x
        self.y += y

class Block:
    """A block is a list of multiple squares.
    x : int
        The horizontal position of the center point of the block.
    y : int
        The vertical position of the center point of the block.
    tiles : list
        A list of tiles that belong to the block."""
    def __init__(self, x, y, tiles=[]):
        self.x = x
        self.y = y
        self.tiles = tiles
    def move(self, x, y):
        """Makes the block move in the direction (x, y).
        x : int
            The horizontal direction the block has to move. A positive value makes it move to the right, a negative value makes it move to the left.
        y : int
            The vertical direction the block has to move. A positive value makes it move downwards, a negative value makes it move upwards."""
        self.x += x
        self.y += y
        for tile in self.tiles:
            tile.move(x, y)
    def turn(self, counterClockwise=False):
        """Makes the block turn 90 degrees.
        counterClockwise : boolean
            If true the block turns counterclockwise. If false it turns clockwise. If not specified it is false."""
        for tile in self.tiles:
            oldX, oldY = tile.x, tile.y
            relX, relY = oldX-self.x, oldY-self.y
            if counterClockwise:
                tile.move(round(self.x+relY-oldX), round(self.y-relX-oldY))
            else:
                tile.move(round(self.x-relY-oldX), round(self.y+relX-oldY))

    def createBlock(x, y):
        """Randomly creates a new block with one of the seven block forms.
        x : int
            The horizontal position of center point of the block.
        y : int
            The vertical position of the center point of the block."""
        return random.choice([
            OrangeRicky(x, y),
            BlueRicky(x, y),
            ClevelandZ(x, y),
            RhodeIslandZ(x, y),
            Hero(x, y),
            Teewee(x, y),
            Smashboy(x, y)])

class OrangeRicky(Block):
    """A sub class of Block that is formed like a L."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x-1, y+1),
            Tile(x,   y+1),
            Tile(x+1, y+1),
            Tile(x+1, y)
        ])

class BlueRicky(Block):
    """A sub class of Block that is formed like a J."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x-1, y+1),
            Tile(x,   y+1),
            Tile(x+1, y+1),
            Tile(x-1, y)
        ])

class ClevelandZ(Block):
    """A sub class of Block that is formed like a Z."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x,   y+1),
            Tile(x+1, y+1),
            Tile(x-1, y),
            Tile(x,   y,)
        ])

class RhodeIslandZ(Block):
    """A sub class of Block that is formed like a mirrored Z."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x-1,  y+1),
            Tile(x,   y+1),
            Tile(x,   y),
            Tile(x+1, y)
        ])

class Hero(Block):
    """A sub class of Block that is formed like a I."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x-1, y),
            Tile(x,   y),
            Tile(x+1, y),
            Tile(x+2, y)
        ])

class Teewee(Block):
    """A sub class of Block that is formed like a T."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x-1, y+1),
            Tile(x,   y+1),
            Tile(x+1, y+1),
            Tile(x,   y)
        ])

class Smashboy(Block):
    """A sub class of Block that is formed like a big block."""
    def __init__(self, x, y):
        super().__init__(x, y, [
            Tile(x,   y+1),
            Tile(x+1, y+1),
            Tile(x,   y),
            Tile(x+1, y)
        ])