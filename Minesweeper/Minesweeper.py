import random
import pygame

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)

def main():
    # Make the map of mines and put it through the processing function.
    map = makeMines((20,20))
    pygame.init()

    colour = (25, 255, 10)
    colourb = (25, 200, 10)
    canvasColour = (120, 120, 120)

    canvas = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Minesweeper")
    

    spriteList = []
    spriteList = pygame.sprite.Group()

    def find_element(Intlist, searchObj):
        y = 0
        for i in range(len(Intlist)):
            if Intlist[i] == searchObj: y = i
        for i in range(len(refList)):
            for j in range(len(refList[i])):
                if refList[i][j] == y:
                    return [i, j]
        return -1

    colourchange = False

    for i in range(20):
        colourchange = not colourchange
        for j in range(20): 
            if colourchange: 
                intcolour = colour
            else: intcolour = colourb
            colourchange = not colourchange
            spriteList.add(Sprite(i*40, j*40, intcolour, 40, 40))


    refList = []
    x=0
    for i in range(20):
        inList = []
        for j in range(20):
            inList.append(x)
            x++1
        refList.append(inList.copy())
        inList.clear()

    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Left Click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in spriteList if s.rect.collidepoint(pygame.mouse.get_pos())]
                for i in clicked_sprites:
                    x, y = 0, 0
                    [x, y] == find_element(spriteList, i)
            # Right Click
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in spriteList if s.rect.collidepoint(pygame.mouse.get_pos())]
                for i in clicked_sprites:
                    if not i.immutable:
                        if i.clickable:
                            i.clickable = True
                            if i.cb:
                                pygame.draw.rect(i.image,
                                 (25, 200, 10),
                                 pygame.Rect(0, 0, i.width, i.height))
                            else:
                                pygame.draw.rect(i.image,
                                 (25, 255, 10),
                                 pygame.Rect(0, 0, i.width, i.height))
                        else:
                            i.clickable = False
                            pygame.draw.rect(i.image,
                                 (255, 20, 20),
                                 pygame.Rect(0, 0, i.width, i.height))
                   
        spriteList.draw(canvas)
        pygame.display.update()


def makeMines(size):
    # Make array of mines
    mineList = []
    for i in range(size[0]):
        inList = []
        for j in range(size[1]):
            if random.randint(1, 10) == 10:
                x = "#"
            else: x = 0
            inList.append(x)
        mineList.append(inList.copy())
        inList.clear()
    mineLoc = []
    tempMap = []
    # Find mines
    for i in range(len(mineList)):
        for j in range(len(mineList[i])):
            if mineList[i][j] == "#":
                mineLoc.append((i,j))
    # Find Adjacent spaces to mines and turn it into a map of where all of the adjacent squares are.
    for i in mineLoc:
        tempMap.append(find_adjacent_places(mineList, i[0], i[1]))
    # Use the tempmap to create a minemap.
    for i in range(len(tempMap)):
        for j in tempMap[i]:
            a, b = j[0], j[1]
            if mineList[a][b] != "#": mineList[a][b]+=1
    return mineList


# Thanks ChatGPT (shhh)
def find_adjacent_places(lst, row, col):
    adjacent_places = []
    rows = len(lst)
    cols = len(lst[0])

    # Define the neighboring positions
    positions = [
        (row - 1, col),     # Top
        (row + 1, col),     # Bottom
        (row, col - 1),     # Left
        (row, col + 1),     # Right
        (row - 1, col - 1), # Top Left
        (row - 1, col + 1), # Top Right
        (row + 1, col - 1), # Bottom Left
        (row + 1, col + 1)  # Bottom Right
    ]

    # Iterate over the neighboring positions
    for position in positions:
        r, c = position
        # Check if the neighboring position is within bounds
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_places.append([r,c])

    return adjacent_places

class Sprite(pygame.sprite.Sprite):
    def __init__(self, locx, locy, colour, height, width):
        super().__init__()
  
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)

        self.width = width
        self.height = height

        pygame.draw.rect(self.image,
                         colour,
                         pygame.Rect(0, 0, width, height))

        self.clickable = True
        self.immutable = False
        self.cb = False
        if colour != (25, 255, 10): self.cb = True

        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy

if __name__ == "__main__":
    main()