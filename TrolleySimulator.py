
from uib_inf100_graphics import *
import random as ran
from statistics import mode

# DONELIST
# * Lagd meny mode (menu_mode)
# * uuuuh lagd game_mode
# * uuuhhmmm lagd endscreen_mode og sånt

##########################################
# Felles Funksjoner
##########################################

def flatten(list_2d):
    return_list = []
    for list in list_2d:
        for obj in list:
            return_list.append(obj)
    return return_list


def move_background(app):
    app.buildings_pos[0] -= app.speed
    app.buildings_pos2[0] -= app.speed
    if app.buildings_pos[0] < -800:
        app.buildings_pos[0] += 2536
    if app.buildings_pos2[0] < -800:
        app.buildings_pos2[0] += 2536
    
    app.rail_pos_m[0] -= app.speed
    if app.rail_pos_m[0] < -200:
        app.rail_pos_m[0]+= 100

def bob_train(app):
    if app.train_room_up:
        app.train_room += 5
    else:
        app.train_room -= 5
    if not (55 < app.train_room < 70):
        app.train_room_up = not app.train_room_up

def pressstimer(app):
    if app.presss:
        app.pressstimer += 1
    else:
        app.pressstimer -= 1
    if not (0 < app.pressstimer < 10):
        app.presss = not app.presss


def create_rail(app, canvas, rail_x, rail_len, rail_y):
    rail_len = app.width + 100
    rail_x = app.rail_pos_m[0]
    while rail_x < rail_len:
        canvas.create_image(rail_x, rail_y, pil_image=app.img_rail)
        rail_x += 111

def create_box(app, canvas, box_x, box_y, content_list):
    canvas.create_image(box_x, box_y, pil_image=app.box)
    x_print = box_x - 100
    for key in content_list:
        canvas.create_image(x_print, box_y, pil_image=app.scale_image(app.char_imgs[key], 1/3))
        x_print += 60
        
def create_people(app, canvas, people_x, people_y):
    canvas.create_image(people_x, people_y, pil_image=app.people)


def create_random_choices(app):
    allowed_value_difference = 15
    app.value_d = 0
    app.value_u = 100 #placeholder values
    choice_d = []
    choice_u = [] # placeholder values
    while (abs(app.value_d - app.value_u) > allowed_value_difference) or (max(len(choice_d), len(choice_u)) > 4) or set(choice_u) == set(choice_d):
        choice_u = []
        choice_d = []
        while not(2 < len(choice_u) and 2 < len(choice_d)):
            append_to = ran.choice([choice_u, choice_d])
            random_char = ran.choice(list(app.char_values.keys()))
            append_to.append(random_char)
        app.value_u = 0
        for key in choice_u:
            app.value_u += app.char_values[key]
        app.value_d = 0
        for key in choice_d:
            app.value_d += app.char_values[key]
    return choice_d, choice_u


def heaven(app):
    points = 0
    points += app.choices_good
    points -= app.choices_bad/2
    gods_hate_list = []
    chars = list(app.char_values.keys())
    for _ in range(5):
        ran_char = chars.pop(ran.randint(0, len(chars)-1))
        gods_hate_list.append(ran_char)
    for char in app.char_saved:
        if char in gods_hate_list:
            points -= 0.4
    if points > 1:
        return True
    else:
        return False



##########################################
# Oppstart av applikasjonen
##########################################

def app_started(app):
    app.mode = "menu_mode"
    app.debug_mode = False

    app.img_buildings = app.load_image("Buildings.png") #dim: 1268 * 265
    app.img_buildings2 = app.load_image("Buildings.png")
    app.buildings_pos = [0, 30]
    app.buildings_pos2 = [1268, 30]
    app.img_rail = app.scale_image(app.load_image("rail.png"), 1/5) #dim 111 * 36
    app.rail_pos_m = [-100, 400]
    app.rail_m = True
    app.img_train = app.scale_image(app.load_image("train2.png"), 1/5) #dim: 1461/5 * 711/5
    app.train_room = 60
    app.train_room_up = True #sier om train skal bobbe opp eller ned lol
    app.train_pos = [250, app.rail_pos_m[1]]
    app.presss = True
    app.pressstimer = 0
    app.box = app.scale_image(app.load_image("box.png"), 1/2) #dim: 675/2 * 225/2

    app.char_values = {"baby": 20, "doctor": 80, "dog": 5, "lion": 3, 
    "man": 70, "woman": 70, "god": 100, "oldlady": 60}
    app.char_imgs = {
        "baby": app.load_image("baby.png"),
        "doctor": app.load_image("doctor.png"),
        "dog": app.load_image("dog.png"),
        "lion": app.load_image("lion.png"),
        "man": app.load_image("man.png"),
        "woman": app.load_image("woman.png"),
        "god": app.load_image("god.png"),
        "oldlady": app.load_image("oldlady.png")
        }
    app.char_saved = []
    app.char_killed = []

    app.exp_images = load_animated_gif('explosion.gif')
    app.exp_counter = 0
    app.exp_pos = [0, 0]
    app.exp = False

    app.speed = 25
    app.timer_delay = 40


def load_animated_gif(path):
    # vi laster første bilde utenfor try/except slik at vi krasjer så fort
    # som mulig hvis vi ikke finner noe bilde i det hele tatt.
    exp_images = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            options = f'gif -index {i}'
            exp_images.append(PhotoImage(file=path, format=options))
            i += 1
        except Exception as e:
            return exp_images


##########################################
# menu_mode
##########################################

def menu_mode_timer_fired(app):
    move_background(app)
    bob_train(app)
    pressstimer(app)


def menu_mode_key_pressed(app, event):
    if event.key == "s":
        app.mode = "game_mode"
        game_mode_start(app)


def menu_mode_redraw_all(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="#B2BEB5", outline="")

    canvas.create_image(app.buildings_pos[0], app.buildings_pos[1], pil_image=app.img_buildings)
    canvas.create_image(app.buildings_pos2[0], app.buildings_pos2[1], pil_image=app.img_buildings2)

    rail_len = app.width + 100
    rail_x = app.rail_pos_m[0]
    while rail_x < rail_len:
        canvas.create_image(rail_x, app.rail_pos_m[1], pil_image=app.img_rail)
        rail_x += 111
    
    canvas.create_image(app.train_pos[0], app.train_pos[1] - app.train_room, pil_image=app.img_train)

    if app.presss:
        canvas.create_text(app.width/2, 200, text="PRESS S TO START", font="Times 30 bold", fill="white")



##########################################
# game_mode
##########################################

def game_mode_start(app):
    app.timer_delay = 30
    app.time = 0
    app.time_since = 0
    app.speed = 50
    app.deciding_time = 50
    app.time_till_choice = 50
    app.choices_total = 0
    app.choices_goal = 5 #hvor mange choices skal bli gjort i spillet?
    app.choices_good = 0
    app.choices_bad = 0

    app.img_rail_u = app.scale_image(app.load_image("rail.png"), 1/5) #dim 111 * 36
    app.rail_pos_u = [-100, 300]
    app.rail_u = False
    app.img_rail_d = app.scale_image(app.load_image("rail.png"), 1/5) #dim 111 * 36
    app.rail_pos_d = [-100, 500]
    app.rail_d = False

    app.game_state = "wait" #wait, choice, performing_choice, crashing også ny modus for end_screen
    app.rail_pos = 1 #0=d 1=m 2=u


def choice_start(app):
    app.rail_u = True
    app.rail_d = True
    app.rail_pos = 0
    app.rail_m = False
    app.game_state = "choice"
    app.time_till_choice = app.deciding_time
    app.choice_u, app.choice_d = create_random_choices(app)

def perform_choice(app):
    if app.rail_pos == 0:
        saved = app.choice_u[:]
        killed = app.choice_d[:]
        if app.value_u > app.value_d:
            app.choices_bad += 1
        else:
            app.choices_good += 1
    else:
        saved = app.choice_d[:]
        killed = app.choice_u[:]
        if app.value_d > app.value_u:
            app.choices_bad += 1
        else:
            app.choices_good += 1
    app.char_saved.append(saved)
    app.char_killed.append(killed)
    app.choices_total += 1
    

    app.game_state = "performing_choice"
    app.time_since = 0

    app.people = app.scale_image(app.load_image("people.png"), 1/3)
    app.people1_x = 1100
    app.p1 = True
    app.people2_x = 1100
    app.p2 = True

def choice_end(app):
    app.game_state = "wait"
    app.time_since = 0
    app.rail_u = False
    app.rail_d = False
    app.rail_m = True
    app.rail_pos = 1

def start_crash(app):
    app.game_state = "crash"
    app.god_person = app.scale_image(app.load_image("god_person.png"), 1/2)
    app.god_person_x = 1200
    app.time_since = 0


def move_people(app):
    app.people1_x -= 50
    app.people2_x -= 50
    if app.rail_pos == 2:
        if app.people1_x < app.train_pos[0] + 200: #crash_x
            app.p1 = False
            app.exp = True
            app.exp_pos = [app.people1_x, app.rail_pos_u[1]]
    if app.rail_pos == 0:
        if app.people2_x < app.train_pos[0] + 200: #crash_x
            app.p2 = False
            app.exp = True
            app.exp_pos = [app.people1_x, app.rail_pos_d[1]]
    if app.people1_x < -100 or app.people2_x < -100:
        app.p1 = False
        app.p2 = False

def move_god(app):
    app.god_person_x -= 50
    if app.god_person_x < app.train_pos[0] + 300:
        app.mode = "endscreen_mode"
        endscreen_mode_start(app)


def correct_variables(app):
    if app.rail_pos == 0:
        app.train_pos[1] = app.rail_pos_d[1]
    if app.rail_pos == 1:
        app.train_pos[1] = app.rail_pos_m[1]
    if app.rail_pos == 2:
        app.train_pos[1] = app.rail_pos_u[1]


def game_mode_timer_fired(app):
    correct_variables(app)
    app.time += 1
    app.time_since += 1
    move_background(app)
    bob_train(app)
    if app.game_state == "wait" and app.time_since == 40 and app.choices_total < app.choices_goal:
        choice_start(app)

    if app.game_state == "choice":
        app.time_till_choice -= 1
    if app.game_state == "choice" and app.time_till_choice == 0:
        perform_choice(app)
    
    if app.game_state == "performing_choice":
        move_people(app)
    if app.game_state == "performing_choice" and app.time_since == 35:
        choice_end(app)
    
    if app.game_state == "wait" and app.time_since == 40 and app.choices_total >= app.choices_goal:
        start_crash(app)
    
    if app.game_state == "crash":
        move_god(app)
    
    if app.exp:
        app.exp_counter = (1 + app.exp_counter) % len(app.exp_images)
        if app.exp_counter >= len(app.exp_images)-1:
            app.exp = False


def game_mode_key_pressed(app, event):
    if event.key == "d":
        app.debug_mode = not app.debug_mode
    if app.game_state == "choice":
        if event.key == "Up" and app.rail_pos < 2:
            app.rail_pos = 2
        if event.key == "Down" and app.rail_pos > 0:
            app.rail_pos = 0


def game_mode_redraw_all(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="#B2BEB5", outline="")
    canvas.create_image(app.buildings_pos[0], app.buildings_pos[1], pil_image=app.img_buildings)
    canvas.create_image(app.buildings_pos2[0], app.buildings_pos2[1], pil_image=app.img_buildings2)

    if app.rail_m:
        create_rail(app, canvas, app.rail_pos_m[0], app.width + 100, app.rail_pos_m[1])
    if app.rail_u:
        create_rail(app, canvas, app.rail_pos_u[0], app.width + 100, app.rail_pos_u[1])
    if app.rail_d:
        create_rail(app, canvas, app.rail_pos_d[0], app.width + 100, app.rail_pos_d[1])
    canvas.create_image(app.train_pos[0], app.train_pos[1] - app.train_room, pil_image=app.img_train)

    if app.game_state == "choice":   
        create_box(app, canvas, 700, app.rail_pos_u[1], app.choice_u)
        create_box(app, canvas, 700, app.rail_pos_d[1], app.choice_d)
        canvas.create_text(app.width/2, 200, text=f"{(app.time_till_choice // 10) + 1}",
             font="Times 30 bold", fill="white")
    if app.game_state == "performing_choice":
        if app.p1:
            create_people(app, canvas, app.people1_x, app.rail_pos_u[1])
        if app.p2:
            create_people(app, canvas, app.people2_x, app.rail_pos_d[1])
    if app.game_state == "crash":
        canvas.create_image(app.god_person_x, app.train_pos[1] - app.train_room, pil_image=app.god_person) #create_god

    if app.exp:
        exp_image = app.exp_images[app.exp_counter]
        canvas.create_image(app.exp_pos[0], app.exp_pos[1]-100, image=exp_image)

    if app.debug_mode:
        canvas.create_text(app.width/2, 200, 
        text=f"""{app.time=} {app.time_since=} {app.timer_delay=} {app.speed=}
{app.mode=} {app.game_state=} {app.time_till_choice=} {app.rail_pos=}
{app.choices_total=} {app.choices_good=} {app.choices_bad=}""",
        font="Calibri 13 bold", fill="white")



##########################################
# endscreen_mode
##########################################

def endscreen_mode_start(app):
    app.game_state = "heaven_or_hell" # heaven_or_hell, book
    app.time_since = 0

    app.exp = True
    app.exp_pos = app.train_pos

    app.bubble = app.load_image("bubble.png")
    app.bubble_pos = [700, 100]
    app.bubble_exist = False

    app.book = app.scale_image(app.load_image("book.png"), 2.7)


def get_loved_and_hated_char(app):
    loved_chars = []
    hated_chars = []
    loves = flatten(app.char_saved[:])
    hates = flatten(app.char_killed[:])
    while len(loved_chars) < 3 and len(loves) > 0 and len(hates) > 0:
        love = mode(loves)
        hate = mode(hates)
        loved_chars.append(love)
        hated_chars.append(hate)
        new_loves = [r for r in loves if r != love]
        new_hates = [r for r in hates if r != hate]
        loves = new_loves
        hates = new_hates
    hated_chars = [r for r in hated_chars if r not in loved_chars]
    return loved_chars, hated_chars


def endscreen_mode_timer_fired(app):
    app.time += 1
    app.time_since += 1

    if app.game_state == "heaven_or_hell" and app.time_since == 30:
        app.heaven = heaven(app)
        app.bubble_exist = True
        if app.heaven:
            app.bubble_content = "CONGRATULATIONS!\nYOU ARE DESERVING OF ETERNAL LIFE!"
        else:
            app.bubble_content = "GO TO HELL FOOL!\nYOU KILLED SO MANY COOL FOLKS!"
    
    if app.game_state == "heaven_or_hell" and app.time_since == 80:
        app.game_state = "book"
        app.bubble_exist = False
        app.book_exist = True
        if app.heaven:
            head_liner = "YOU ARE A GOOD PERSON"
        else:
            head_liner = "YOU ARE A BAD PERSON"
        app.loved_chars, app.hated_chars = get_loved_and_hated_char(app)
        app.book_page1 = f"""\
{head_liner}


YOU LOVE:




YOU HATE:


"""
        app.book_page2 = f"""\
        CHOICES MADE

Saved:                          Killed:











      Press M to retry
"""
    if app.exp:
        app.exp_counter = (1 + app.exp_counter) % len(app.exp_images)
        if app.exp_counter >= len(app.exp_images)-1:
            app.exp = False

def endscreen_mode_key_pressed(app, event):
    if event.key == "d":
        app.debug_mode = not app.debug_mode
    if app.game_state == "book":
        if event.key.capitalize() == "M":
            app_started(app)

def endscreen_mode_redraw_all(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="#B2BEB5", outline="")
    canvas.create_image(app.buildings_pos[0], app.buildings_pos[1], pil_image=app.img_buildings)
    canvas.create_image(app.buildings_pos2[0], app.buildings_pos2[1], pil_image=app.img_buildings2)
    if app.rail_m:
        create_rail(app, canvas, app.rail_pos_m[0], app.width + 100, app.rail_pos_m[1])
    if app.rail_u:
        create_rail(app, canvas, app.rail_pos_u[0], app.width + 100, app.rail_pos_u[1])
    if app.rail_d:
        create_rail(app, canvas, app.rail_pos_d[0], app.width + 100, app.rail_pos_d[1])
    canvas.create_image(app.train_pos[0], app.train_pos[1] - app.train_room, pil_image=app.img_train)
    canvas.create_image(app.god_person_x, app.train_pos[1] - app.train_room, pil_image=app.god_person) #create_god

    if app.exp:
        exp_image = app.exp_images[app.exp_counter]
        canvas.create_image(app.exp_pos[0], app.exp_pos[1]-100, image=exp_image)
    
    if app.bubble_exist:
        canvas.create_image(app.bubble_pos[0], app.bubble_pos[1], pil_image=app.bubble)
        canvas.create_text(app.bubble_pos[0], app.bubble_pos[1]-30, text=app.bubble_content, font="Calibri 17 bold")


    if app.game_state == "book":
        canvas.create_image(app.width/2, app.height/2, pil_image=app.book)

        canvas.create_text(250, app.height/2, text=app.book_page1, font="Calibri 18 bold")
        print_x = 150
        print_y = 300
        for key in app.loved_chars:
            canvas.create_image(print_x, print_y, pil_image=app.scale_image(app.char_imgs[key], 1/3))
            print_x += 80
        print_x = 150
        print_y = 430
        for key in app.hated_chars:
            canvas.create_image(print_x, print_y, pil_image=app.scale_image(app.char_imgs[key], 1/3))
            print_x += 80
        
        canvas.create_text(650, app.height/2, text=app.book_page2, font="Calibri 18 bold")
        print_y = 200
        count = 1
        for list in app.char_saved:
            print_x = 550
            canvas.create_text(print_x-40, print_y, text=f"{count}.")
            for key in list:
                canvas.create_image(print_x, print_y, pil_image=app.scale_image(app.char_imgs[key], 1/6))
                print_x += 40
            print_y += 50
            count += 1
        print_y = 200
        for list in app.char_killed:
            print_x = 730
            for key in list:
                canvas.create_image(print_x, print_y, pil_image=app.scale_image(app.char_imgs[key], 1/6))
                print_x += 40
            print_y += 50
        

    if app.debug_mode:
        canvas.create_text(app.width/2, 200, 
        text=f"""{app.time=} {app.time_since=} {app.timer_delay=} {app.speed=}
{app.mode=} {app.game_state=} {app.time_till_choice=} {app.rail_pos=}
{app.choices_total=} {app.choices_good=} {app.choices_bad=}""",
        font="Calibri 13 bold", fill="white")



run_app(width=1000, height=600, title="TrolleySimulator")
