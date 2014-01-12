from birds import *
from tkinter import *

DELAY_MS = 200

if __name__ == "__main__":

    master = Tk()
    
    w = Canvas(master, width=SKY_WIDTH, height=SKY_HEIGHT)
    w.pack()

    sky = Sky()
    birds = [Bird(sky) for i in range(200)]
    
    birds_dict = {
        bird: w.create_rectangle(bird.x, bird.y, bird.x+1, bird.y+1)
        for bird in birds
    }

    def draw_birds():
        for bird, rect in birds_dict.items():
            w.coords(rect, bird.x, bird.y, bird.x+1, bird.y+1)
    
    def tick():
        sky.tick()
        draw_birds()
        master.after(DELAY_MS, tick)

    master.after(DELAY_MS, tick)
    mainloop()