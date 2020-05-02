from tkinter import  *
from tkinter import filedialog
from PIL import ImageTk, Image 
from tkinter import messagebox 
import csv 
import subprocess 

def cal_nfiq1():
	'''
	Docstring: Calculate NFIQ1
	Input: Nothing
	Output: Score of NFIQ1 displayes in answer label
			If there are pictures in name list all the scores will	
			store in score list
	'''
	global selectAFile
	global answer
	global choose
	global folder
	global namelist
	global scores
	choose = 1
	
	if(folder==0):
		if(selectAFile.__str__() == '.!button'):
			messagebox.showerror('Error', 'Select A picture')
		else:
			answer = subprocess.getoutput("./nfiq" + ' ' + selectAFile + ' -d ')
			text_Input.set(answer)
	else:
		for item in namelist:
			print(item)
			answer = subprocess.getoutput("./nfiq" + ' ' + item + ' -d ')
			scores.append(answer)

		messagebox.showinfo('info','SAVED IN SCORES LIST')
		for i in scores:
			print(i)
		folder = 0
		

def cal_nfiq2():
	'''
	Docstring: Calculate NFIQ2
	Input: Nothing
	Output: Score of NFIQ2
	'''
	global selectAFile
	global answer
	global choose

	choose = 2	
	if(selectAFile.__str__() == '.!button'):
		messagebox.showerror('Error', 'Select A picture')
	else:
		# add the nfiq2 script answer=answer = subprocess.getoutput("./nfiq" + ' ' + selectAFile + ' -d ')
		text_Input.set(answer)

def open_a_file():
	'''
	Docstring: Open a dialog box for choosing a picture 
	Input: Nothing
	Output: The name of the picture usally *.png
	'''
	global win_pic
	global selectAFile
	global choose

	choose = -1
	win_pic = filedialog.askopenfile(initialdir="/home/orel/Documents/works/Python", title="Select A File", filetypes=(("png.files","*.png"),("all files","*.*")))
	selectAFile=win_pic.name
	

def open_a_folder():
	'''
	Docstring: Open a dialog box for choosing a pictures 
	Input: Nothing
	Output: Put all the pictures name in a list
	'''
	global win_pic
	global selectAFolder
	global choose
	global folder
	global namelist
	folder=1
	name=0

	choose=-1
	win_pic = filedialog.askopenfiles(initialdir="/home/orel/Documents/works/Python", title="Select A Folder", filetypes=(("png.files","*.png"),("all files","*.*")))
	
	for item in win_pic:
		print(item.name)
		namelist.append(item.name)


def saveresaultinExcel():
	'''
	Docstring: Save the name of the pic and the scores in excel file
	Input: Nothing
	Output: MetaData excel file
	'''
	global answer
	global selectAFile
	global choose
	global scores
	global namelist


	csvfile = open('metadata.csv','a')
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

	if(len(scores)==0):	
		if choose == 1:
			writer.writerow({'Path of pic': selectAFile,'Result nfiq1': answer})
			messagebox.showinfo('info','SAVED')
		if choose == 2:
			writer.writerow({'Path of pic': selectAFile,'Result nfiq2': answer})
			messagebox.showinfo('info','SAVED')
		if choose == -1:
			messagebox.showerror('Error', 'Select A picture')

		choose=-1
		csvfile.close()
	else:
		if choose == 1:
			for (a,b) in zip(scores,namelist):
				writer.writerow({'Path of pic': b,'Result nfiq1': a})
				
			messagebox.showinfo('info','SAVED')
			scores=[]
		if choose == 2:
			for (a,b) in zip(scores,namelist):
				writer.writerow({'Path of pic': b,'Result nfiq1': a})

			writer.writerow({'Path of pic': selectAFile,'Result nfiq2': answer})
			messagebox.showinfo('info','SAVED')
			scores=[]
		if choose == -1:
			messagebox.showerror('Error', 'Select A picture')


		choose=-1
		csvfile.close()


#main:
choose=-1 # 1=nfiq1,2=nfiq2
folder=0 # 0=a pic,1=At laest 2 pictures
namelist = []
scores=[]
win=Tk()
answer=""
text_Input=IntVar()
win.title("NFIQ SOFTWARE")
win.geometry("800x500")

#background picture
canvas=Canvas(win,width=800, height= 500)
my_bg = ImageTk.PhotoImage(Image.open(("/home/orel/Documents/works/Python/nfiqBg.png")))
canvas.create_image(0,0,anchor=NW,image=my_bg)
canvas.pack()

#open a file
selectAFile=Button(win, text='select a file', fg='black',command=open_a_file)
selectAFile.place(x=0,y=75)

#open a folder
selectAFolder=Button(win, text='select a folder', fg='black',command=open_a_folder)
selectAFolder.place(x=0,y=105)


#Buttons + score Label
nfiq1Button= Button(win, text='nfiq1', fg= 'black',command= cal_nfiq1)
nfiq1Button.place(x=0,y=0)
nfiq2Button= Button(win, text='nfiq2', fg= 'black',command=cal_nfiq2)
nfiq2Button.place(x=0,y=25)
scorlabel=Label(text='score: ',bg='white' , fg='black')
scorlabel.place(x=0,y=50)

displayScore=Entry(win,textvariable=text_Input, fg='black', justify='right')
displayScore.place(x=45, y=51)

saveResault= Button(win, text='Save', fg= 'black',command=saveresaultinExcel)
saveResault.place(x=120,y=75)


#create an excel file and save the result thier

with open('metadata.csv','w') as csvf:
	fieldnames = ['Path of pic', 'Result nfiq1', 'Result nfiq2']
	writer = csv.DictWriter(csvf,fieldnames=fieldnames)

	writer.writeheader()

	csvf.close()



win.mainloop()
	