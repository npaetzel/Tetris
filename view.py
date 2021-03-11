from tkinter import *
from tkinter import font, simpledialog, messagebox
import pyglet

class View(Canvas):
    """The View class creates a window and draws the game on it."""
    def __init__(self, root, grid):
        self.root = root
        self.grid = grid
        self.rows = grid.rows+1
        self.cols = grid.cols+2
        self.colors = ["#FF4040", "#7FFF00", "#FFA500", "#2F4F4F"]
        self.zoom = 0.6
        

        pyglet.font.add_file('EarlyGameBoy.ttf')
        self.scoreFont = font.Font(family='Early GameBoy', size=20)        

        screenHeight = root.winfo_screenheight()
        self.blocksize = int((screenHeight-100)/self.rows)
        if self.zoom <= 1 and self.zoom > 0:
            self.blocksize = int(self.blocksize*self.zoom)
        self.height = self.blocksize*self.rows-2
        self.width = self.blocksize*self.cols-2+200

        self.root.resizable(False, False)
        self.root.title("Shittytris")
        super().__init__(root, width=self.width, height=self.height)
        super().focus_set()

    def redraw(self):
        """Is called in the mainloop to delete the old frame and draw a new one."""
        self.delete(ALL)
        #self.drawGrid()
        self.drawTiles()
        self.drawText()
        self.pack()

    def drawText(self):
        """Draws the text elements with score level and cleared lines."""
        super().create_text(self.width-100, 100, text=str('SCORE\n' + str(self.grid.score)), font=self.scoreFont, justify=RIGHT)
        super().create_text(self.width-100, 200, text=str('LEVEL\n' + str(self.grid.level)), font=self.scoreFont, justify=RIGHT)
        super().create_text(self.width-100, 300, text=str('LINES\n' + str(self.grid.cleared)), font=self.scoreFont, justify=RIGHT)

    def drawGrid(self):
        """Draws the grid"""
        for y in range(1, self.rows):
            super().create_line(0, y*self.blocksize, self.width, y*self.blocksize)

        for x in range(1, self.cols):
            super().create_line(x*self.blocksize, 0, x*self.blocksize, self.height)

    def drawTiles(self):
        """Draws the tiles of the blocks."""
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                blockNumber = self.grid.content[row][col]
                if blockNumber > 0:
                    super().create_rectangle(
                        self.blocksize*(col+1),
                        self.blocksize*(row),
                        self.blocksize*(col+2),
                        self.blocksize*(row+1),
                        fill=self.colors[blockNumber%len(self.colors)]
                    )
        for tile in self.grid.currentBlock.tiles:
            super().create_rectangle(
                self.blocksize*(tile.x+1),
                self.blocksize*(tile.y),
                self.blocksize*(tile.x+2),
                self.blocksize*(tile.y+1),
                fill=self.colors[self.grid.blockNumber%len(self.colors)]
            )
    def askName(self):
        """Opens a dialog to ask for the player's name."""
        return simpledialog.askstring('New Highscore!', 'Who are you?')

    def askRestart(self):
        """Opens a dialog to ask if the player wants to try again."""
        return messagebox.askretrycancel('Play again', 'Want to play another game?')