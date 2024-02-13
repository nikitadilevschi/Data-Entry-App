from tkinter import *
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import mysql.connector 

#functions that add features to the program
def update(rows):
  trv.delete(*trv.get_children())
  for i in rows:
    trv.insert('', 'end', values=i)

def reload(lines):
  tbl.delete(*tbl.get_children())
  for e in lines:
    tbl.insert('', 'end', values=e)



#Let user to search team by the name or its members
def search():
  q2 = q.get()
  query = "SELECT id, name, members, score FROM team WHERE name LIKE '%"+q2+"%' OR members LIKE '%"+q2+"%'"
  cursor.execute(query)
  rows = cursor.fetchall()
  update(rows)


#Let user to search individual by the name or events
def search_individual():
  i2 = i.get()
  query1 = "SELECT id, name, events, score FROM individuals WHERE name LIKE '%"+i2+"%' OR events LIKE '%"+i2+"%'"
  cursor.execute(query1)
  lines = cursor.fetchall()
  reload(lines)




#Clears the table from data searched for Teams
def clear():
  query = "SELECT id, name, members, score FROM team"
  cursor.execute(query)
  rows = cursor.fetchall()
  update(rows)

#Clears the table from data searched for Individuals
def clear_individual():
  query1 = "SELECT id, name, events, score FROM individuals"
  cursor.execute(query1)
  lines = cursor.fetchall()
  reload(lines)



#Shows data of chosen team
def getrow(event):
  rowid = trv.identify_row(event.y)
  item = trv.item(trv.focus())
  t1.set(item['values'][0])
  t2.set(item['values'][1])
  t3.set(item['values'][2])
  t4.set(item['values'][3])


def getline(event):
  lineid = tbl.identify_row(event.y)
  indiv_item = tbl.item(tbl.focus())
  i1.set(indiv_item['values'][0])
  i2.set(indiv_item['values'][1])
  i3.set(indiv_item['values'][2])
  i4.set(indiv_item['values'][3])



#Update the chosen team
def update_team():
  tname = t2.get()
  mname = t3.get()
  score = t4.get()
  teamid = t1.get()

  if messagebox.askyesno("Confirm please", "Are you sure you want to update this team?"):
    query = "UPDATE team SET name = %s, members = %s, score = %s WHERE id = %s"
    cursor.execute(query,(tname, mname, score, teamid))
    mydb.commit()
    clear()
  else:
    return True



#Update the chosen individual
def update_individual():
  iname = i2.get()
  ievent = i3.get()
  iscore = i4.get()
  individ = i1.get()

  if messagebox.askyesno("Confirm please", "Are you sure you want to update this person?"):
    query1 = "UPDATE individuals SET name = %s, events = %s, score = %s WHERE id = %s"
    cursor.execute(query1,(iname, ievent, iscore, individ))
    mydb.commit()
    clear_individual()
  else:
    return True



#Add a new team
def add_team():
  tname = t2.get()
  mname = t3.get()
  score = t4.get()
  query = "INSERT INTO team(id, name, members, score) VALUES(NULL, %s, %s, %s)"
  cursor.execute(query, (tname, mname, score))
  mydb.commit()
  clear()


#Add new individual
def add_individual():
  iname = i2.get()
  ievent = i3.get()
  iscore = i4.get()
  query1 = "INSERT INTO individuals(id, name, events, score) VALUES(NULL, %s, %s, %s)"
  cursor.execute(query1, (iname, ievent, iscore))
  mydb.commit()
  clear_individual()


#Deletes the selected team
def delete_team():
  id =t1.get()
  if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this team?"):
    query = "DELETE FROM team WHERE id = "+id
    cursor.execute(query)
    mydb.commit()
    clear()
  else:
    return True



def delete_individual():
  id =i1.get()
  if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this person"):
    query1 = "DELETE FROM individuals WHERE id = "+id
    cursor.execute(query1)
    mydb.commit()
    clear_individual()
  else:
    return True



#Database Connection.
  
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="team",
  auth_plugin="mysql_native_password"
  )
cursor = mydb.cursor()

# creating variables for use of the code below.
root = Tk()
#Team Variables
q = StringVar()
t1 = StringVar() #id
t2 = StringVar() #name
t3 = StringVar() #members
t4 = StringVar() #score

#Individuals variables
i = StringVar()
i1 = StringVar() #id 
i2 = StringVar() #name
i3 = StringVar() #events
i4 = StringVar() #score


#creating spaces for tables
wrapper1 = LabelFrame(root, text="Team List",font=("Arial",20))
wrapper2 = LabelFrame(root, text="Individuals List",font=("Arial",20))
wrapper3 = LabelFrame(root, text="Event List",font=("Arial",20))
wrapper4 = LabelFrame(root, text="Modify Team OR Individuals",font=("Arial",20))

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper4.pack(fill="both", expand="yes", padx=20, pady=10)

style=ttk.Style()
style.theme_use('clam')
trv = ttk.Treeview(wrapper1, columns=(1,2,3,4), show="headings", height="6")
trv.column("1",anchor=CENTER, stretch=NO)
trv.column("2",anchor=CENTER, stretch=NO)
trv.column("3",anchor=CENTER, stretch=NO)
trv.column("4",anchor=CENTER, stretch=NO, width=300)
trv.pack()

trv.heading(1, text="ID")
trv.heading(2, text="Name")
trv.heading(3, text="Members")
trv.heading(4, text="Score")

#Double click to select the data from the table
trv.bind('<Double 1>', getrow)

##############################
tbl = ttk.Treeview(wrapper2, columns=(1,2,3,4), show="headings", height="10")
tbl.column("1",anchor=CENTER, stretch=NO)
tbl.column("2",anchor=CENTER, stretch=NO)
tbl.column("3",anchor=CENTER, stretch=NO)
tbl.column("4",anchor=CENTER, stretch=NO, width=300)

tbl.pack()

tbl.heading(1, text=" ID")
tbl.heading(2, text="Name")
tbl.heading(3, text="Events")
tbl.heading(4, text="Score")

#Double click to select the data from the table
tbl.bind('<Double 1>', getline)


query1 = "SELECT id, name, events, score from individuals"
cursor.execute(query1)
lines = cursor.fetchall()
reload(lines)

#Search section for individuals
ilbl = Label(wrapper2, text="Search Individual")
ilbl.pack(side=tk.LEFT, padx=10)
ient = Entry(wrapper2, textvariable=i)
ient.pack(side=tk.LEFT, padx=6)
btn_search = Button(wrapper2, text="Search", command=search_individual)
btn_search.pack(side=tk.LEFT, padx=6)
btn_clear = Button(wrapper2, text="Clear", command=clear_individual)
btn_clear.pack(side=tk.LEFT, padx=6)


#Inserting the table with teams from the database to the program
query = "SELECT id, Name, Members, Score from Team"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

#Search Section for team.
lbl = Label(wrapper1, text="Search Team")
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper1, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper1, text="Search", command=search)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper1, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)


#Team data Section
lbl1 = Label(wrapper4, text="Team ID")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(wrapper4,justify='center', width=40,textvariable=t1)
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl2 = Label(wrapper4, text="Team Name")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 =Entry(wrapper4, justify='center', width=40, textvariable=t2) 
ent2.grid(row=1, column=1, padx=5, pady=3)

lbl3 = Label(wrapper4, text="Members")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper4, justify='center', width=40, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=3)

lbl4 = Label(wrapper4, text="Score")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(wrapper4, justify='center', width=40, textvariable=t4)
ent4.grid(row=3, column=1, padx=5, pady=3)

#buttons to operate with the team data
up_btn = Button(wrapper4, width=15, text="Update", command=update_team)
add_btn = Button(wrapper4, width=15, text="Add Team", command=add_team)
delete_btn = Button(wrapper4, width=15, text="Delete", command=delete_team)

add_btn.grid(row=4, column=0, padx=2, pady=7)
up_btn.grid(row=4, column=1, padx=2, pady=7)
delete_btn.grid(row=4, column=2, padx=2, pady=7)


#Individuals data section
ilbl1 = Label(wrapper4, text="Person ID")
ilbl1.place(x= 1360, y=1)
ient1 = Entry(wrapper4,justify='center', width=40,textvariable=i1)
ient1.place(x= 1270, y=20)

ilbl2 = Label(wrapper4, text="Person Name")
ilbl2.place(x=1350, y=40)
ient2 = Entry(wrapper4,justify='center', width=40,textvariable=i2)
ient2.place(x= 1270, y=60)

ilbl3 = Label(wrapper4, text="Events")
ilbl3.place(x=1370, y=80)
ient3 = Entry(wrapper4,justify='center', width=40,textvariable=i3)
ient3.place(x=1270, y=100)

ilbl4 = Label(wrapper4, text="Score")
ilbl4.place(x=1370, y=120)
ient4 = Entry(wrapper4,justify='center', width=40,textvariable=i4)
ient4.place(x=1270, y=140)


#buttons to operate with the individual data
up_btn2 = Button(wrapper4, width=15, text="Update", command=update_individual)
add_btn2 = Button(wrapper4, width=15, text="Add Individual", command=add_individual)
delete_btn2 = Button(wrapper4, width=15, text="Delete", command=delete_individual)

add_btn2.place(x=1170, y=180)
up_btn2.place(x=1325, y=180)
delete_btn2.place(x=1480, y=180)



root.title("Scoring Program")
root.geometry("1800x1020")
root.mainloop()