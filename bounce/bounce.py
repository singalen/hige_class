import tkinter

master = tkinter.Tk()

w = tkinter.Canvas(master, width=500, height=400)
w.pack()

x, y = 10, 10
diameter = 20
sx, sy = 3, 7

ball = w.create_oval(x, y, x+diameter, y+diameter, fill="green")


def tick():
    global x, y, sx, sy, ball

    x += sx
    y += sy
    w.coords(ball, x, y, x+diameter, y+diameter)

    if x+diameter >= w.winfo_width():
        sx = -abs(sx)
    if y+diameter >= w.winfo_height():
        sy = -abs(sy)
    if x <= 0:
        sx = abs(sx)
    if y <= 0:
        sy = abs(sy)

    w.after(50, tick)


tick()
tkinter.mainloop()