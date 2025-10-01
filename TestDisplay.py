from Displayer import Displayer

class MockGrid:
    def __init__(self):
        self.size = 4
        self.map = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 131072],
        ]

if __name__ == "__main__":
    grid = MockGrid()
    displayer = Displayer()
    displayer.display(grid)
