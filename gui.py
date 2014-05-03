import groups
import permutations
import front
import string

from Tkinter import *

def permcallback():
	e2.delete(0,END)
	e2.insert(0,str(front.str2perm(e1.get() ) ))

root = Tk()

class permsimp():
	def __init__(self,parent,xoffset,yoffset):
		self.tl =Label(parent, text="Perm simplifier").grid(row=yoffset, column=xoffset)
		self.l1 =Label(parent, text="Input").grid(row=yoffset+1, column=xoffset, sticky = W+N)
		self.l2 =Label(parent, text="Output").grid(row=yoffset+2, column=xoffset, sticky = W+N)
		self.e1 = Entry(parent)
		self.e1.grid(row=yoffset+1, column=xoffset+1,sticky=W+N)
		self.e2 = Entry(parent)
		self.e2.grid(row=yoffset+2, column=xoffset+1,sticky=W+N)
		self.b1 = Button(parent, text= "Ok", command= self.permcallback )
		self.b1.grid(row=yoffset+2, column=xoffset+2,sticky=E+N)
	def permcallback(self):
		self.e2.delete(0,END)
		self.e2.insert(0,str(front.str2perm(self.e1.get() ) ))

class groupentry():
	def __init__(self,parent,xoff,yoff):
		self.whyvar = Label(parent,text="Input a Set of Elements\n Ex. {1,2,3} for perm.s {(123),(13)}").grid(row=yoff, column=xoff, sticky = N)
		self.setbox = Text(parent, height=5, width=20,padx=3,pady=3)
		self.setbox.grid(row=yoff+1,column=xoff, sticky = W)
		self.opvar = StringVar(parent)
		self.opvar.set("func. comp")
		self.operation = OptionMenu(parent, self.opvar, "func. comp", "+", "*")
		self.operation.grid(row=yoff+1, column=xoff+1, sticky = E)
		self.gobutton = Button(parent,text="DO IT",command=self.grouphandoff)
		self.gobutton.grid(row=yoff+2, column=xoff+1, sticky = E)
		self.groupvar = 0
		self.groupcheck = Checkbutton(parent, text="Is a Group", variable=self.groupvar)
		self.groupcheck.grid(row=yoff+3, column=xoff+1, sticky = E)
		self.cyclicvar = 0
		self.cycliccheck = Checkbutton(parent, text="Is Cyclic", variable=self.cyclicvar)
		self.cycliccheck.grid(row=yoff+4, column=xoff+1, sticky = E)
	
	def grouphandoff(self):
		rawstring = str(self.setbox.get(0.0,END))
		print(rawstring)
		print(str(type(rawstring)))
		rawstring = rawstring.replace('{','')
		rawstring = rawstring.replace('}','')
		rawstring = rawstring.replace(' ','')
		for n in string.whitespace:
			rawstring = rawstring.replace('n','')
		rawstring = rawstring.strip()
		print(rawstring)
		for n in range(0,len(rawstring)):
			print(str(n)+"   :"+rawstring[n])
		
		permlist = []
		
	
g = groupentry(root,0,0)

a = permsimp(root,10,1)

mainloop()
