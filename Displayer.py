from BaseDisplayer import BaseDisplayer
import platform

# 256-color background mapping
# Reference: https://jonasjacek.github.io/colors/
colorMap = {
    0       : 254,
    2       : 252,
    4       : 250,
    8       : 138,
    16      : 204,
    32      : 197,
    64      : 202,
    128     : 208,
    256     : 220,
    512     : 226,
    1024    : 148,
    2048    : 112,
    4096    : 43,
    8192    : 117,
    16384   : 39,
    32768   : 33,
    65536   : 135,
    131072  : 129,
}


def get_text_color(bg_code):
    # These colors are too light for white text
    return 0 if bg_code in {254, 252, 250, 220, 226, 228, 229} else 15

def ansi256_tile(bg_code, text):
    fg_code = get_text_color(bg_code)
    return f"\x1b[38;5;{fg_code};48;5;{bg_code}m{text}\x1b[0m"

def balanced_center(s, width=7):
    total_padding = width - len(s)
    right = total_padding // 2
    left = total_padding - right
    return " " * left + s + " " * right

class Displayer(BaseDisplayer):
    def __init__(self):
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def winDisplay(self, grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")

    def unixDisplay(self, grid):
        hgap = "  "  # 2-space horizontal gap between tiles
        for row in grid.map:
            for line in range(3):  # 3 lines per tile for vertical height
                row_line = []
                for v in row:
                    color = colorMap.get(v, 15)
                    if line == 1:
                        text = balanced_center(str(v) if v != 0 else "", 7)
                    else:
                        text = " " * 7
                    row_line.append(ansi256_tile(color, text))
                print(hgap.join(row_line))
            print("")  # Vertical spacing between tile rows


