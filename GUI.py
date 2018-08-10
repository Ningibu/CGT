### Version 1.0 of animation.py for PKU 2018 CGT
### by Dan Garcia (ddgarcia@cs.berkeley.edu)

from tkinter import *
import random

master = Tk()
SLOT = 100 ## slot size (square on the board)
NUMSTEPS = 10 ## Number of steps, or "frames" per animation (fewer=faster)
STEP = SLOT/NUMSTEPS ## How much the piece moves every step
POSITION = 0 ## This would be the current position
ROWS = 3
COLS = 5

WIN = "win"
LOSE = "lose"
TIE = "tie"
DRAW = "draw"
VALUE_TO_COLOR = {WIN:"darkgreen", LOSE:"darkred", TIE:"yellow", DRAW:"yellow"}
turn = 1
count = 0
Label(master, text = "Welcome to Hounds and Hare").pack()
start =Button(master, text= "renew").pack()
frm =Frame(master).pack()
fram1 =Frame(frm)
fram1.pack(anchor=NW)
v1=IntVar()
v2=IntVar()
v3=IntVar()

Label(fram1, text= "Hounds:").grid(row=0,column=0)
Button1=Radiobutton(fram1, text ="human",variable=v1,value=1).grid(row=0,column=100)
Button2=Radiobutton(fram1, text ="computer",variable=v1,value=2).grid(row=0,column=200)

Label(fram1, text= "Hare:").grid(row=3)
Button5=Radiobutton(fram1, text ="human",variable=v3,value=1).grid(row=3,column=100)
Button6=Radiobutton(fram1, text ="computer",variable=v3,value=2).grid(row=3,column=200)

Label(fram1, text= "Which hound do you want to move:").grid(row=5)
button_1 =Radiobutton(fram1,text="Hound_1",variable=v2,value=1).grid(row=5,column=100)
button_2 =Radiobutton(fram1,text="Hound_2",variable=v2,value=2).grid(row=5,column=200)
button_3 =Radiobutton(fram1,text="Hound_3",variable=v2,value=3).grid(row=5,column=300)


c = Canvas(master, width=COLS*SLOT, height=ROWS*SLOT)
c.pack()

def GetColor(position):
	"""Here, you would display the color based on the value from your database"""
	value = random.choice([WIN, LOSE, TIE, DRAW]) ## your DB query
	return VALUE_TO_COLOR[value]

def GetRemotenessViz(position):
	"""Here, you would display the remoteness based on your database.
	We categorize remoteness into four categories, best move, 2nd, 3rd, 4th best.
	Best remoteness would be "" (solid line)
	2nd best remoteness would be "20 5" (almost solid), etc."""
	solid = str(SLOT//10)+" "
	dash1 = str(SLOT//10-1*SLOT//40)
	dash2 = str(SLOT//10-2*SLOT//40)
	dash3 = str(SLOT//10-3*SLOT//40)
	return random.choice(["", solid+dash1, solid+dash2, solid+dash3])
def Choice():
        if turn == 0:
                return Hare
        elif v2==1:
                return Hound_1
        elif v2==2:
                return Hound_2
        else:
                return Hound_3
              
def MakeAnimateHandler(fr,to,frsignx,frsigny):
	def AnimateHandler(someevent):
		c.itemconfig(fr, state="hidden")

		def Animate(dx,dy,n):
                        
			c.move(Choice(),dx,dy)
			if n > 1:
				c.after(1,Animate,dx,dy,n-1)
			else:
				c.itemconfig(to, state="normal")
		Animate(STEP*frsignx,STEP*frsigny,NUMSTEPS)
	return AnimateHandler

def CreateArrows():
	arrowwidth = 0.25 * (0.4 * SLOT)
	arrowshape = str(2*arrowwidth)+" "+str(2*arrowwidth)+" "+str(arrowwidth)
	for fri in range(ROWS*COLS):
		for toi in range(ROWS*COLS):
			frrow, frcol, torow, tocol = fri // COLS, fri % COLS, toi // COLS, toi % COLS
			if fri == toi or abs(frrow-torow) > 1 or abs(frcol-tocol) > 1:
				pass
			else:
				a = c.create_line(SLOT/2+frcol*SLOT,SLOT/2+frrow*SLOT,SLOT/2+tocol*SLOT,SLOT/2+torow*SLOT, width=arrowwidth, fill=GetColor(POSITION), dash=GetRemotenessViz(POSITION), activefill="black", arrowshape=arrowshape, arrow="last", state="hidden", tags=("arrow"+str(fri)))
				c.tag_bind(a, sequence="<Button-1>",func=MakeAnimateHandler("arrow"+str(fri),"arrow"+str(toi),tocol-frcol,torow-frrow))

def CreateBoard():
	"""Create the ROWS * COLS rectangles that make up the board"""
	for col in range(1,4):
		for row in range(ROWS):
			c.create_rectangle(col*SLOT, row*SLOT, (col+1)*SLOT, (row+1)*SLOT, fill="grey")

def arrows():

        if turn == 0:
                return c.itemconfig("arrow9", state="normal")
        elif v2==1:
                return c.itemconfig("arrow5", state="normal")
        elif v2==2:
                return c.itemconfig("arrow1", state="normal")
        else:
                return c.itemconfig("arrow11", state="normal")

                
CreateBoard()
c.create_rectangle(0*SLOT, 1*SLOT, 1*SLOT, 2*SLOT, fill="grey")
c.create_rectangle(4*SLOT, 1*SLOT, 5*SLOT, 2*SLOT, fill="grey")
CreateArrows() ## These all start hidden
c.tag_raise("piece") ## Put the piece above the arrows
arrows()


Hound_1=c.create_oval(15, SLOT+15, SLOT-15, 2*SLOT-15, fill="red", outline="red", tags=("piece"))
Hound_2=c.create_oval(SLOT+15, 15, 2*SLOT-15, SLOT-15, fill="red", outline="red", tags=("piece"))
Hound_3=c.create_oval(SLOT+15, 2*SLOT+15, 2*SLOT-15, 3*SLOT-15, fill="red", outline="red", tags=("piece"))
Hare= c.create_oval(4*SLOT+15, SLOT+15, 5*SLOT-15, 2*SLOT-15, fill="blue", outline="blue", tags=("piece"))

Label(master,text ="Rule").pack(pady=10)
Label(master,text ="One player represents the three Hounds, which try to corner the other player's Hare as it seeks to win by escaping them.\n Each player can move one piece one step in each turn. \n The Hounds can only move forward or diagonally (left to right) or vertically (up and down). The Hare can move in any direction.\n The Hounds win if they trap the Hare so that it can no longer move.\n The Hare wins if it escape (gets to the left of all the Hounds).\n Variants: If the Hounds move vertically ten moves in a row, they are considered to be stalling and the Hare wins.").pack()


mainloop()

