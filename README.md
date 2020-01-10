# FlappyBird
My code for the mobile game Flappy Bird using pygame.

## PyGame
Pygame is a python library used commonly to add graphics to python programs(especially in game developement).

### Installation 
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame.
```bash
pip install pygame
```
### Usage

```python
import pygame

font = pygame.font.SysFont("comicsans", 50)   #To set default font for any text
win=pygame.display.set_mode((width,height))   #To create a external window to display the game
pygame.display.set_caption("Flappy Bird")     #To display a title for the window

win.blit(bg,(0,0))                            
base.draw(win)                                #To refresh the diaplay window with the background starting from the top-left corner(0,0)
score = font.render("Score: " + str(score),1,(255,255,255))     
win.blit(score, (width - score.get_width() - 15, 10))           #To display score a little above the middle of the window
win.blit(font.render("Game Over",3,(255,255,255)), (200,400))

keys=pygame.key.get_pressed()                 #To read which key has been pressed
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

