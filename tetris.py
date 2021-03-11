import grid, view, tkinter, time, sys

class Controller():
    """Handles all inputs and hands them over to the grid model. Takes changes from the grid model and hands them over to the view."""
    def __init__(self):
        self.root = tkinter.Tk()
        self.grid = grid.Grid(self.root, 10, 20)
        self.view = view.View(self.root, self.grid)
        self.view.bind('<Key>', self.handleKey)
        self.root.protocol("WM_DELETE_WINDOW", self.handleClose)
        self.closed = False
        self.timer = Timer()
        self.scoreName = ''
    def run(self):
        """It is the mainloop of the game. To imitate the speed of the original Gameboy Classic it refreshes every 59.73 times per second."""
        while not self.closed:
            if self.timer.getTime() >= 1/59.73:
                self.timer.restart()
                self.grid.run()
                self.view.redraw()
                self.endRound()
                self.root.update_idletasks()
                self.root.update()
    def endRound(self):
        """Checks if the game is over and asks the player to play again."""
        if not self.grid.active:
            if self.grid.newHighscore:
                self.grid.newHighscore = False
                name = self.view.askName()
                self.grid.setScoreName(name)
            if self.view.askRestart():
                self.grid.resetGame()
            else:
                self.handleClose()
    def handleKey(self, event):
        """Takes input from the player as an event and instructs the grid model to make the corrosponding movements."""
        if self.grid.active:
            if event.keysym == 'Left': self.grid.move(-1, 0)
            elif event.keysym == 'Right': self.grid.move(1, 0)
            elif event.keysym == 'Down': self.grid.move(0, 1)
            elif event.keysym == 'a': self.grid.currentBlock.turn(True)
            elif event.keysym == 'd': self.grid.currentBlock.turn()
            elif event.keysym == 'Escape': self.handleClose()
    def handleClose(self):
        """Destroys all GUI elements and ends the program."""
        self.closed = True
        self.root.destroy()
        sys.exit()
class Timer:
    """A timer to measure the time passed between two frames."""
    def __init__(self):
        self.restart()
    def getTime(self):
        return time.perf_counter()-self.start
    def restart(self):
        self.start = time.perf_counter() 

if __name__ == '__main__':
    control = Controller()
    control.run()