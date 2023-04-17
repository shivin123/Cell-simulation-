import random
from matplotlib import pyplot as plt
import time

board=[]
s=30 #side length

for i in range(s):
    temp=[]
    for e in range(s):
        temp.append([])
    board.append(temp)

def board_all(board=board):
    for i in range(s):
        print(board[i])
        print("\n")

#cell vars
cell_list=[]
cell_obj=[]
name_to_obj={}
intial_cell=2
rep_food_rej=1000


#food vars
food_val=30
food_gen_amount=3

#gen vars
move_dif=1

#name convention 
namebase="00000"
current_name=namebase
def next_name():
    global current_name
    temp = int(current_name)
    temp+=1
    temp=str(temp)
    while len(temp)<len(current_name):
        temp="0"+temp
    current_name=temp
    return temp

class cell:
    global board
    def __init__(self, x_pos, y_pos, speed_gene=1, food_store=25, age=0):
        try:
            self.name = next_name()
            self.age = age
            self.food_store = food_store
            self.speed_gene = speed_gene
            self.speed_overflow = 0
            self.x_pos = x_pos
            self.y_pos = y_pos
            global cell_list
            cell_list.append(self.name)
            board[x_pos][y_pos].append(self.name)
            board[x_pos][y_pos].append("has_cell")
        except:
            print("Error: Cell Gen")
            
        

def cell_move_amount(cell):
    global move_dif
    cell.speed_overflow+=cell.speed_gene
    move=cell.speed_overflow//1
    cell.speed_overflow=cell.speed_overflow%1
    cell.food_store-=(cell.speed_gene*cell.speed_gene*move_dif)
    return int(move)

def cell_move_direction(cell):
    global board,s
    try:
        board[cell.x_pos][cell.y_pos].remove(cell.name)
        board[cell.x_pos][cell.y_pos].remove("has_cell")
    except:
        # print("Error: Cell not at expected location")
        return 0
    adj_arr=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    while True:
        selected_move=adj_arr[random.randint(0, 8)]
        while (cell.x_pos+selected_move[0])<0 or (cell.x_pos+selected_move[0])>(s-1) or (cell.y_pos+selected_move[1])<0 or (cell.y_pos+selected_move[1])>(s-1):
            selected_move=adj_arr[random.randint(0, 8)]
        if not "has_cell" in board[cell.x_pos+selected_move[0]][cell.y_pos+selected_move[1]]:
            break
    cell.x_pos+=selected_move[0]
    cell.y_pos+=selected_move[1]
    board[cell.x_pos][cell.y_pos].append(cell.name)
    board[cell.x_pos][cell.y_pos].append("has_cell")
    return 1


def food_gen():
    global food_gen_amount, board, s
    temp_food=food_gen_amount
    max_att=6
    while temp_food!=0:
        max_att-=1
        if max_att<0:
            break
        x=[random.randint(0, s-1),random.randint(0, s-1)]
        if not "f" in board[x[0]][x[1]]:
            board[x[0]][x[1]].append("f")
            temp_food-=1
        else:
            continue

def cell_reproduce(cell_c):
    global board,s,cell_obj,name_to_obj
    adj_arr=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    selected_move=adj_arr[random.randint(0, 7)]
    max_att_2=5
    while selected_move[0]+cell_c.x_pos<0 or selected_move[0]+cell_c.x_pos>(s-1) or selected_move[1]+cell_c.y_pos<0 or selected_move[1]+cell_c.y_pos>(s-1):
        max_att_2-=1
        selected_move=adj_arr[random.randint(0, 7)]
        if max_att_2==0:
            print("Cell unable to repreduce")
            return 2
    try:
        while "has_cell" in board[selected_move[0]+cell_c.x_pos][selected_move[1]+cell_c.y_pos]:
            selected_move=adj_arr[random.randint(0, 7)]
    except:
        print(selected_move[0]+cell_c.x_pos)
        print(selected_move[1]+cell_c.y_pos)
        print("Error: New cell placement")
    food_bal=cell_c.food_store-750
    cell_c.food_store=round(food_bal/2)
    m_speed=cell_c.speed_gene+(cell_c.speed_gene*(random.randint(-5, 5)/100))
    obj = cell(selected_move[0]+cell_c.x_pos,selected_move[1]+cell_c.y_pos, speed_gene=m_speed, food_store=round(food_bal/2))
    cell_obj.append(obj)
    name_to_obj[obj.name]=obj
    print("A cell was born") 


def gen_init_cells():
    global board,s,intial_cell
    for i in range(intial_cell):
        while True:
            selected_move=[random.randint(0, s-1),random.randint(0, s-1)]
            if not "has_cell" in board[selected_move[0]][selected_move[1]]:
                break
        obj = cell(selected_move[0],selected_move[1])
        cell_obj.append(obj)
        name_to_obj[obj.name]=obj


def check_eat(cell):
    global board,food_val
    try:
        if "f" in board[cell.x_pos][cell.y_pos]:
            board[cell.x_pos][cell.y_pos].remove("f")
            cell.food_store+=food_val
    except:
        print("Error: Eat error")

def cell_death(cell_c):
    global board,cell_obj
    try:
        board[cell_c.x_pos][cell_c.y_pos].remove("has_cell")
        board[cell_c.x_pos][cell_c.y_pos].remove(cell_c.name)
        board[cell_c.x_pos][cell_c.y_pos].append("f")
        cell_obj.remove(cell_c)
        print("A cell has died")
    except:
        print("Error: Cell not at expected location")
        print("Cell Name: "+cell_c.name)
        try:
            cell_obj.remove(cell_c)
        except:
            print("Error: obj list clean failed")
    if len(cell_obj)==0:
        print("All cells are dead")
        return 0
    else:
        return 1

def cell_turn(cell_c):
    global board,rep_food_rej, s
    cell_c.age+=1
    movement_points=cell_move_amount(cell_c)
    if cell_c.food_store<0:
        cell_death(cell_c)
    check_eat(cell_c)
    for i in range(movement_points):
        cell_move_direction(cell_c)
        check_eat(cell_c)
    if cell_c.food_store>rep_food_rej:
        cell_reproduce(cell_c)
    return 1

def vis_board(close=True):
    global board,s
    vis=[]
    for i in range(s):
        temp=[]
        for e in range(s):
            if "f" in board[i][e] and not "has_cell" in board[i][e]:
                temp.append(5)
            elif "has_cell" in board[i][e]:
                temp.append(10)
            else:
                temp.append(0)
        vis.append(temp)
    
    plt.imshow(vis, interpolation='nearest')
    plt.show()
    if close:
        time.sleep(1)
        plt.close()

#main

gen_init_cells()
for i in range(30):
    food_gen()
vis_board()

for i in range(25000):
    # if i%10==0:
    #     print(".")
    food_gen()
    for obj in cell_obj:
        x=cell_turn(obj)
        if x==0:
            break
    if x==0:
        break

vis_board(False)

s_age=0
s_food_store=0
s_speed_gene=0
for i in cell_obj:
    print("name: "+str(i.name))
    print("age: "+str(i.age))
    s_age+=i.age
    print("food_store: "+str(i.food_store))
    s_food_store+=i.food_store
    print("speed_gene: "+str(i.speed_gene))
    s_speed_gene+=i.speed_gene
    print("_______________________")

print("XXXXXXXXXXXXXXXXXXXXXXXX")
print("Avg age: " + str(s_age/len(cell_obj)))
print("Avg food_store: " + str(s_food_store/len(cell_obj)))
print("Avg speed_gene: " + str(s_speed_gene/len(cell_obj)))
print("XXXXXXXXXXXXXXXXXXXXXXXX")




