import tkinter as tk
import time
import random
import winsound
 
class MovingSquare:
    def __init__(self, canvas, x=100, y=100, size=40):
        #store variables
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.vx = 0
        self.vy = 0
        self.shooting_timer = 0
        self.shooting = False
 
        #create the rect for the class
        #self.id = canvas.create_rectangle(x, y, x + size, y + size, fill='red')
        self.id = canvas.create_image(x, y, image=p_image,anchor='nw')
 
    def move(self, dx, dy):
        global game_state
        self.vx *= 0.9
        self.vy *= 0.9
        self.vx = MaxSpeed(self.vx + dx,99999999999)
        self.vy = MaxSpeed(self.vy + dy,99999999999)
        self.canvas.move(self.id, self.vx, self.vy)
        coords = self.canvas.coords(self.id)
        coords.extend([coords[0] + self.size,coords[1] + self.size])
        if coords[0] < 0 or coords[2] > self.canvas.winfo_width():
            self.canvas.move(self.id, -self.vx, 0)
            self.vx = 0
 
        if coords[1] < 0 or coords[3] > self.canvas.winfo_height():
            self.canvas.move(self.id, 0, -self.vy)
            self.vy = 0
 
        coords = [coords[0] ,coords[1],coords[2],coords[3]]
        coords1 = [coords[0] +30 ,coords[1]+5,coords[2],coords[3] -5]
        coords2 = [coords[0] +5 ,coords[1] + 15,coords[2] - 5,coords[3] - 15]
        for object in objects:
            if object.state == True:
                if check_collision(object.getcoords(),coords1) or check_collision(object.getcoords(),coords2) :
                    canvas.itemconfig(game_over_text,state ="normal")
                    canvas.itemconfig(button_window,state ="normal")
                    game_state = False
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS| winsound.SND_ASYNC)
 
        for power in powerups:
            if check_collision(power.getcoords(),coords1) or check_collision(power.getcoords(),coords2) :
                self.canvas.delete(power.id)
                powerups.remove(power)
                self.shooting = True
                self.shooting_timer = 600
 
        if self.shooting == True:
            self.shooting_timer -= 1
            if self.shooting_timer < 0:
                self.shooting = False
 
 
    def reset (self):
        self.vx = 0
        self.vy = 0
        self.shooting = False
        #self.canvas.coords(self.id,self.x,self.y,self.x + self.size,self.y+ self.size)
        self.canvas.coords(self.id,self.x,self.y)
 
    def coords(self):
        return  self.canvas.coords(self.id)
 
class MovingObject:
    def __init__(self, canvas, x=1200, y=50, size=30):
        self.canvas = canvas
        #self.id = canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
        self.id = canvas.create_image(x, y, image=s_image,anchor='nw')
        self.x = x
        self.y = y
        self.size = size
        self.state = True
 
 
    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        coords = self.canvas.coords(self.id)
        if coords[0] < -self.canvas.winfo_width():
            self.canvas.move(self.id, self.canvas.winfo_width() * 3, 0)
            self.state = True
            self.canvas.itemconfig(self.id, state="normal")
 
    def getcoords(self):
        arr = self.canvas.coords(self.id)
        try:
            arr = [arr[0] + 5 ,arr[1] + 5 ,arr[0] + self.size - 5,arr[1] + self.size - 5]
        except:
            print(arr)
            print(self.id)
            return  arr
        return  arr
 
    def reset (self):
        #self.canvas.coords(self.id,self.x,self.y,self.x + self.size,self.y+ self.size)
        self.canvas.delete(self.id)
 
class PowerUp:
    def __init__(self, canvas, x=1200, y=50, size=64):
        self.canvas = canvas
        #self.id = canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
        self.id = canvas.create_image(x, y, image=c_image,anchor='nw')
        self.x = x
        self.y = y
        self.size = size
        self.dead = False
 
 
    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        coords = self.canvas.coords(self.id)
        if coords[0] < -self.canvas.winfo_width():
            self.canvas.move(self.id, self.canvas.winfo_width() * 3, 0)
            self.dead = True
 
    def getcoords(self):
        arr = self.canvas.coords(self.id)
 
        arr = [arr[0] - 5 ,arr[1] - 5 ,arr[0] + self.size + 5,arr[1] + self.size + 5]
 
        return  arr
 
    def reset (self):
        #self.canvas.coords(self.id,self.x,self.y,self.x + self.size,self.y+ self.size)
        self.canvas.delete(self.id)
 
class Particle:
    def __init__(self, canvas, x, y, imagearr, lifespan):
        self.canvas = canvas
        self.imagearr = imagearr
        self.id = canvas.create_image(x, y, image=imagearr[0])
        self.dx = -1
        self.dy = 0
        self.counter = 0
        self.birth_time = time.time()
        self.lifespan = lifespan
 
    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        #if x1 + self.dx < 0 or x2 + self.dx > self.canvas.winfo_width():
        #    self.dx = -self.dx
        #if y1 + self.dy < 0 or y2 + self.dy > self.canvas.winfo_height():
        #    self.dy = -self.dy
        self.canvas.move(self.id, -6 -(speed * 0.2),self.dy)
 
        #age = time.time() - self.birth_time
        #scale = 1 - age / self.lifespan
        #self.canvas.scale(self.id, x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, scale, scale)
 
    def is_dead(self):
        age = time.time() - self.birth_time
        scale = age / self.lifespan
        if scale > 0.80:
            self.birth_time = time.time()
            self.counter += 1
            if self.counter < 4:
                coords = self.canvas.coords(self.id)
                self.canvas.delete(self.id)
                self.id = canvas.create_image(coords[0], coords[1], image=self.imagearr[self.counter])
            else:
                return True
 
        return False
 
class Bullet:
    def __init__(self, canvas, x, y, imagearr, lifespan):
        self.canvas = canvas
        self.imagearr = imagearr
        self.id = canvas.create_image(x, y, image=imagearr)
        self.dx = -1
        self.dy = 0
        self.counter = 0
        self.birth_time = time.time()
        self.lifespan = lifespan
 
    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        #if x1 + self.dx < 0 or x2 + self.dx > self.canvas.winfo_width():
        #    self.dx = -self.dx
        #if y1 + self.dy < 0 or y2 + self.dy > self.canvas.winfo_height():
        #    self.dy = -self.dy
        self.canvas.move(self.id, 16 + (speed * 0.2),self.dy)
 
        for object in objects[:]:
            if check_collision(object.getcoords(),[x1,y1,x2,y2]):
                #canvas.itemconfig(game_over_text,state ="normal")
                #canvas.itemconfig(button_window,state ="normal")
                #game_state = False
                object.state = False
                self.canvas.itemconfig(object.id, state="hidden")
                #object.reset()
                #objects.remove(object)
                #winsound.PlaySound("SystemHand", winsound.SND_ALIAS| winsound.SND_ASYNC)
 
 
        #age = time.time() - self.birth_time
        #scale = 1 - age / self.lifespan
        #self.canvas.scale(self.id, x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, scale, scale)
 
    def is_dead(self):
        age = time.time() - self.birth_time
        if age > self.lifespan:
            return True
        else:
            return False
        #scale = age / self.lifespan
        #if scale > 0.80:
        #    self.birth_time = time.time()
        #    self.counter += 1
        #    if self.counter < 4:
        #        coords = self.canvas.coords(self.id)
        #        self.canvas.delete(self.id)
        #        self.id = canvas.create_image(coords[0], coords[1], image=self.imagearr[self.counter])
        #    else:
        #        return True
        #
        #return False
        #return random.random() > ((1 - (time.time() - self.birth_time)) / self.lifespan) 
        #return True
 
class Emitter:
    def __init__(self, canvas, x, y, image, rate, lifespan):
        self.canvas = canvas
        self.x = x
        self.xoff = x
        self.y = y
        self.yoff = y
        self.image = image
        self.rate = rate
        self.lifespan = lifespan
        self.particles = []
 
    def emit(self):
        self.particles.append(Particle(self.canvas, self.x, self.y, self.image, self.lifespan))
 
    def update(self):
        coords = square.coords()
        self.x = coords[0] + self.xoff
        self.y = coords[1] + self.yoff
        for particle in self.particles[:]:
            particle.move()
            if particle.is_dead():
                self.canvas.delete(particle.id)
                self.particles.remove(particle)
 
class Gun:
    def __init__(self, canvas, x, y, image, rate, lifespan):
        self.canvas = canvas
        self.x = x
        self.xoff = x
        self.y = y
        self.yoff = y
        self.image = image
        self.rate = rate
        self.lifespan = lifespan
        self.particles = []
 
    def emit(self):
        self.particles.append(Bullet(self.canvas, self.x, self.y, self.image, self.lifespan))
 
    def update(self):
        coords = square.coords()
        self.x = coords[0] + self.xoff
        self.y = coords[1] + self.yoff
        for particle in self.particles[:]:
            particle.move()
            if particle.is_dead():
                self.canvas.delete(particle.id)
                self.particles.remove(particle)
 
class BackGround:
    def __init__(self, canvas, x=0, y=0, size=1128):
        self.canvas = canvas
        #self.id = canvas.create_rectangle(x, y, x + size, y + size, fill='blue')
        self.id = canvas.create_image(x, y, image=b_image,anchor='nw')
        self.x = x
        self.y = y
        self.size = size
 
 
    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        coords = self.canvas.coords(self.id)
        if coords[0] < -self.size:
            self.canvas.move(self.id, self.size * 2, 0)
 
    def getcoords(self):
        arr = self.canvas.coords(self.id)
        arr.extend([arr[0] + self.size,arr[1] + self.size])
        return  arr
 
    def reset (self):
        #self.canvas.coords(self.id,self.x,self.y,self.x + self.size,self.y+ self.size)
        self.canvas.delete(self.id)
 
def update_fps_counter():
    global start_time, game_state, score, highscore,speed,idle_time,diffscaling,score_to_power
    #get time between this frame and previous one and display it
    cur_time = time.time()
    elapsed_time = cur_time - start_time
    if elapsed_time != 0:
        fps = 1 / elapsed_time 
    else:
        fps = 0
    root.title(f"Skysweeper     FPS: {fps:.0f}")
 
    #increment Score and display it
    score += 10
    canvas.itemconfig(score_text, text="Score: " + str(score))
 
    #increment gamespeed and add obstacle
 
 
    if score % diffscaling == 0:
        if score > 150000:
            diffscaling = 15000
        if score > 100000:
            diffscaling = 5000
        elif score > 70000:
            diffscaling = 4000
        elif score > 50000:
            diffscaling = 2000
        elif score > 30000:
            diffscaling = 1000
        elif score > 10000:
            diffscaling = 800
        elif score > 5000:
            diffscaling = 600
        else:         
             diffscaling = 400
        if (cur_time - idle_time) > 10 and random.randint(0,4) == 1:
            objects.append(MovingObject(canvas,1200,square.coords()[1]+10))
        else:
            objects.append(MovingObject(canvas,1200,random.randint(15,685)))
 
        speed *= 1.01
 
    score_to_power -= 10
    if score_to_power < 0:
        score_to_power = 20000 + random.randint(0,20000)
        powerups.append(PowerUp(canvas,1200,random.randint(50,650)))
        powerup = powerups[len(powerups)-1]
        for object in objects:
            if check_collision(object.getcoords(),powerup.getcoords()):
                object.state = False
                object.canvas.itemconfig(object.id, state="hidden")
 
    #set start time to previous frame
    start_time = cur_time
 
    #reset movement
    dx = 0
    dy = 0
 
    #if key is set velocity in a direction
    if key_states["Up"]:
        dy = -1
        idle_time = cur_time
    elif key_states["Down"]:
        dy = 1
        idle_time = cur_time
    if key_states["Left"]:
        dx = -1
    elif key_states["Right"]:
        dx = 1
    if key_states["Shift_L"]:
        dx *= 0.5
        dy *= 0.5
 
    if dx != 0 and dy != 0:
        dx *= 0.7
        dy *= 0.7
 
 
    #moves player character based on Input
    square.move(dx, dy)
 
    emitter1.emit()
    emitter1.update()
    emitter2.emit()
    emitter2.update()
 
    if score % 30 == 0 and square.shooting == True:
        gun1.emit()
        gun2.emit()
    gun1.update()
    gun2.update()
 
 
    for back in background_arr:
        back.move(-speed *2,0)
 
    #moves all obstacles by the increasing speed
    for object in objects:
        object.move(-speed,0)
 
    for power in powerups:
        power.move(-speed,0)
        if power.dead == True:
            powerups.remove(power)
 
 
    if game_state == True: #if Game still running call the same function in 10ms
        root.after(10, update_fps_counter)
    else:
        #if Game no longer running toggle UI elements
        canvas.itemconfig(score_text, text="Score: " + str(score),state = "hidden")
        canvas.itemconfig(score_2text, text="Score: " + str(score),state = "normal")
        canvas.itemconfig(button_window,state ="normal")
        canvas.itemconfig(highscore_text,state ="normal",text="High Score: " + str(highscore))
 
        #if new highscore display a new highscore message instead of previous highscore
        if score > highscore:
            highscore = score
            save_highscore(highscore)
            canvas.itemconfig(highscore_text,state ="normal",text="New High Score !!")        
 
def on_key_press(event): #Store Keys Pressed
    global key_states, game_state
    key_states[event.keysym] = True
    #if event.keysym == "<Return>" and game_state:
    #    start_game()
 
 
def on_key_release(event): #Store Keys Released
    global key_states
    key_states[event.keysym] = False
 
def get_highscore():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0
 
def save_highscore(score): #Saves Highscore to file
    with open('highscore.txt', 'w') as file:
        file.write(str(score))
 
def MaxSpeed(value, max_value): #Clamps the value between the absolute value of max
 
    return max(min(value, max_value), -max_value)
 
def check_collision(rect1, rect2): #checks if there is an intersection between two rects on the screen
    x1_1, y1_1, x2_1, y2_1 = rect1
    x1_2, y1_2, x2_2, y2_2 = rect2
 
    # Check for overlap in x-axis
    if x1_1 > x2_2 or x1_2 > x2_1:
        return False
 
    # Check for overlap in y-axis
    if y1_1 > y2_2 or y1_2 > y2_1:
        return False
 
    # Rectangles overlap
    return True
 
def start_game_enter(event):
    global game_state
    if not game_state:
        start_game()
 
def start_game(): # game starts after this button pressed
    global game_state, score, highscore,objects,speed, diffscaling,score_to_power,powerups
 
    #Hide of Display UI elemtns
    canvas.itemconfig(button_window,state ="hidden")
    canvas.itemconfig(game_over_text, text="GAME OVER",state ="hidden")
    canvas.itemconfig(highscore_text, text="High Score: " + str(highscore),state = "hidden")
    canvas.itemconfig(score_2text,state = "hidden")
    canvas.itemconfig(score_text, text="Score: " + str(score),state = "normal")
    #winsound.PlaySound("Ring05.wav",winsound.SND_ASYNC| winsound.SND_LOOP)
 
    #sets highscore
    if score > highscore:
        highscore = score
 
    #resets variables
    score = 0
    speed = 3
    score_to_power = 15000 + random.randint(0,20000)
    game_state = True
    diffscaling = 1000
 
    #resets gameObjects
    square.reset()
    for object in objects:
        object.reset()
    objects = []
    for power in powerups:
        power.reset()
    powerups = []
 
    #runs game loop
    update_fps_counter()
 
root = tk.Tk()
 
# Sets up Input
key_states = {'Up': False, 'Down': False, 'Left': False, 'Right': False, 'Shift_L': False}
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)
root.bind('<Return>', start_game_enter)
 
#Creates the canvas
canvas = tk.Canvas(root, width=1000, height=700)
canvas.pack()
 
#global variables
highscore = get_highscore()
objects = []
powerups = []
score = 0
speed = 2
time_shooting = 300
game_state = False
start_time = time.time() - 0.01
idle_time = start_time
 
 
 
#Creates Game Objects
s_image = tk.PhotoImage(file="Assets/spike_s_w.png")
c_image = tk.PhotoImage(file="Assets/crate.png")
p_image = tk.PhotoImage(file="Assets/3d_plane_d.png")
b_image = tk.PhotoImage(file="Assets/back_t_s.png")
t1_image = tk.PhotoImage(file="Assets/fuzz.png")
t2_image = tk.PhotoImage(file="Assets/fuzz_75.png")
t3_image = tk.PhotoImage(file="Assets/fuzz_50.png")
t4_image = tk.PhotoImage(file="Assets/fuzz_25.png")
bul_image = tk.PhotoImage(file="Assets/bullet.png")
t_image = [t1_image,t2_image,t3_image,t4_image]
 
 
background1 = BackGround(canvas)
background2 = BackGround(canvas,x=1128)
background_arr = [background1,background2]
 
square = MovingSquare(canvas)
emitter1 = Emitter(canvas, 24, 0, t_image, 5, 0.1)
emitter2 = Emitter(canvas, 24, 45, t_image, 5, 0.1)
gun1 = Gun(canvas, 24, 15, bul_image, 5, 1)
gun2 = Gun(canvas, 24, 30, bul_image, 5, 1)
 
 
# All UI Elements
start_button = tk.Button(canvas, text="Start Game", command=start_game)
button_window = canvas.create_window(500, 350, window=start_button)
game_over_text = canvas.create_text(500, 300, anchor="center",font=("Arial", 32))
canvas.itemconfig(game_over_text, text="Skysweeper")
score_text = canvas.create_text(10, 10, anchor="nw",font=("Arial", 16))
canvas.itemconfig(score_text, text="Score: " + str(score))
score_2text = canvas.create_text(420, 400, anchor="nw",font=("Arial", 16))
canvas.itemconfig(score_2text, text="Score: " + str(score),state = "hidden")
highscore_text = canvas.create_text(420, 430, anchor="nw",font=("Arial", 16))
canvas.itemconfig(highscore_text, text="High Score: " + str(highscore))
 
 
 
root.mainloop()