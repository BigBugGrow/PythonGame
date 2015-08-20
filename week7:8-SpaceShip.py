"""
An Introduction to Interactive Programming in Python (Part 2)
RiceRocks - 2015-08-01

Additional features not in the rubric:

levels			the difficulty increases every 10 score points, this affects
                the number of rocks, their speed and their initial distance to
                the ship
explosions		explosions move with the exploding object (rocks or the ship)
                exploding rocks destroy nearby rocks
acceleration	thrust and angular velocity of the ship use acceleration to
                smooth the motion
artwork			all provided images for rocks, explosions, nebula and debris are
                loaded and used randomly
                one explosion image is reserved for the ship so that the player
                always can identify this
sound			can be toggled by pressing "s"
pause			game can be paused by pressing "p"
sprite scaling	the size of the rocks varies, so does the size of their explosions
rock splitting	by pressing x instead of space, the ship shoots missiles that split
                rocks in half until they are too small and get fully destroyed
shields			by pressing down you can activate a shield that protects the ship
                the shield lives for a few seconds and needs some time to regenerate
inheritance		ship is a subclass of sprite, inherits all fields and most methods
"""

import simplegui
import math
import random

WIDTH = 800					# width of canvas
HEIGHT = 600				# height of canvas
FPS = 60.0					# frames per second of draw_handler
MIN_VEL = 0.05 * FPS		# minimum ship velocity, set vel to zero if below
FRICTION_FACTOR = 0.30		# deacceleration factor due to friction per second
FF_FPS = math.pow(FRICTION_FACTOR, 1.0/FPS)
                            # deacceleration factor per frame
USE_ACCELERATION = True		# the "Spaceship"-grading rubric required constant
                            # angular velocity.  This time acceleration for rotation
                            # and thrust is used when this value is set to True
if USE_ACCELERATION:
    MIN_T = 1.0	* FPS		# minimum thrust of ship in pixel/s
    MAX_T = 15.0 * FPS		# maximum thrust of ship in pixel/s
    DELTA_T = 20.0 * FPS	# thrust increase in pix/s for ship
    MIN_AV = math.pi / 2	# minimum angular velocity in rad/s for the ship
    MAX_AV = math.pi * 2	# maximum ang. vel. in rad/s for ship
    DELTA_AV = math.pi * 4	# ang. vel. increase in rad/s for ship
else:
    MIN_T = 10.0 * FPS		# minimum thrust of ship in pixel/s
    MAX_T = 10.0 * FPS		# maximum thrust of ship in pixel/s
    DELTA_T = 0	* FPS		# thrust increase in pix/s for ship
    MIN_AV = 1.5 * math.pi	# minimum angular velocity in rad/s for the ship
    MAX_AV = 1.5 * math.pi	# maximum ang. vel. in rad/s for ship
    DELTA_AV = 0			# ang. vel. increase in rad/s for ship
    
MIN_ROCK_VEL = 50			# min velocity of an asteroid in pixels/s
DELTA_ROCK_VEL = 25			# rock vel is increased by this value at every level
MISSILE_SPEED = 500			# speed of missile in pixels/s
UI_FONT = "monospace"		# font name fopr ui text
UI_FONT_SIZE = 24			# font size for ui text
UI_FONT_COLOR = "orange"	# color for ui text
UI_FLASH_COLOR = "yellow"	# color for highlighted ui text
UI_TEXT_MARGIN = 10			# right margin for ui text
NR_OF_LIVES = 3				# lives at start of game
MIN_ROCKS = 6				# allowed number of rocks at start of game
DELTA_SCORE = 10			# after how many points should the difficulty be increased
MAX_ROCK_SPAWN_DIST = 200	# minimum distance for a newly spawned rock from the ship
DELTA_ROCK_SPAWN_DIST = 10	# distanc-decrease per level for a newly spawned rock
SHIELD_LIFESPAN = 5 * FPS	# shield lasts for 5 seconds
SHIELD_REGEN = 15 * FPS		# 15 seconds before you can use the shield again

game_started = False		# False while the splash screen is shown
level = 1					# difficulty level
level_change_counter = 0	# counter for flashing level text
score = 0					# game score
lives = NR_OF_LIVES			# lives remaining
time = 0					# time measured in frames
rock_group = set()			# rocks
missile_group = set()		# missiles
explosion_group = set()		# explosions
direction = 1				# direction of debris image, set to 1 or -1
rock_vel = MIN_ROCK_VEL		# current velocity for newly spawned rocks, increases with score
rocks_allowed = MIN_ROCKS	# current number of allowed rocks, increases with score
rock_spawn_dist = MAX_ROCK_SPAWN_DIST
                            # current minimum distance for newly spawned rocks
difficulty_jump = 0			# score at which the difficulty was last increased
sound = True				# play sound
paused = False				# game is paused

class ImageInfo:
    """ class to store info about an image resource """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
    def get_center(self):
        return self.center
    def get_size(self):
        return self.size
    def get_radius(self):
        return self.radius
    def get_lifespan(self):
        return self.lifespan
    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
asset_url = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/"    
sound_url = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/"

def load_artwork (image_names):
    """ load a list of image names and return a list of image objects """
    return [simplegui.load_image(asset_url + img + ".png") for img in image_names]
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_images = load_artwork (["debris1_blue", "debris2_blue", "debris1_brown", "debris2_brown", "debris_blend"])
debris_image = random.choice(debris_images)
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_images = load_artwork (["nebula_blue.f2014", "nebula_brown"])
nebula_image = random.choice(nebula_images)
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(asset_url + "splash.png")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(asset_url + "double_ship.png")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_images = load_artwork (["shot2", "shot1"])
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_images = load_artwork (["asteroid_blue", "asteroid_brown", "asteroid_blend"])
# animated explosion - explosion_orange.png, explosion_blue.png, 
# explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_images = load_artwork (["explosion_blue", "explosion_blue2", "explosion_alpha"])
# one explosion image is reserved for the ship being hit
ship_explosion_image = simplegui.load_image(asset_url + "explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(sound_url + "soundtrack.mp3")
missile_sound = simplegui.load_sound(sound_url + "missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(sound_url + "thrust.mp3")
explosion_sound = simplegui.load_sound(sound_url + "explosion.mp3")

def angle_to_vector(ang):
    """ return a unit vector corresponding to the given angle """
    return [math.cos(ang % (2 * math.pi)), math.sin(ang % (2 * math.pi))]

def vector_to_angle(vec):
    """ return an angle corresponding to a give vector """
    return math.atan2(vec[1],vec[0])

def dist(p,q):
    """ return the distance between points p and q """
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

class Sprite:
    """ class for image resources """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.scale = 1
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()		# this is in frames
        self.animated = info.get_animated()
        self.age = 0
        self.type = ""							# additional info for a sprite
        if sound:
            sound.rewind()
            sound.play()
   
    def get_pos (self):
        return self.pos
    def set_pos (self, pos):
        self.pos = pos
    def get_vel (self):
        return self.vel
    def set_vel (self, vel):
        self.vel = vel
    def get_angle (self):
        return self.angle
    def set_angle (self, angle):
        self.angle = angle
    def get_angle_vel (self):
        return self.angle_vel
    def set_angle_vel (self, angle_vel):
        self.angle_vel = angle_vel
    def get_age (self):
        return self.age
    def get_scale (self):
        return self.scale
    def set_scale (self, scale):
        self.scale = scale
    def get_radius (self):
        return self.radius * self.scale
    def get_lifespan (self):
        return self.lifespan
    def get_type (self):
        return self.type
    def set_type (self, type):
        self.type = type
    def is_alive (self):
        return self.age <= self.lifespan
    
    def draw(self, canvas):
        """ draw the sprite if the lifespan is not yet reached """
        if self.lifespan != None and self.age <= self.lifespan:
            # if this is an animated image we use an offset into the image to
            # find the image corresponding to the age
            img_offset = (0 if not self.animated else self.age * self.image_size[0])
            canvas.draw_image(self.image, 
                              (self.image_center[0] + img_offset, self.image_center[1]), 
                              self.image_size, self.pos, 
                              [self.image_size[0] * self.scale, self.image_size[1] * self.scale], 
                              self.angle_vel * self.age / FPS)
    
    def update(self):
        """ update age and pos of the sprite """
        self.age += 1
        self.pos[0] = (self.pos[0] + self.vel[0] / FPS) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1] / FPS) % HEIGHT
        
    def collide(self, other):
        """ returns true if our distance to the other object is too small """
        return dist(self.pos, other.get_pos()) <= self.radius + other.get_radius()

class Ship (Sprite):
    """ a ship is simply a sprite with a few additional fields and methods """
    def __init__(self, pos, vel, ang, ang_vel, image, info):
        Sprite.__init__(self, pos, vel, ang, ang_vel, image, info)
        self.thrust = 0
        self.shield = False
        self.shield_last_toggled = -1 * SHIELD_REGEN
        
    def get_thrust (self):
        return self.thrust
    def set_thrust (self, thrust):
        self.thrust = thrust
    def get_shield (self):
        return self.shield
    def get_shield_fraction (self):
        if not self.shield:
            fraction = max(min((time - self.shield_last_toggled) / SHIELD_REGEN, 1), 0)
        else:
            fraction = max(min(1 - ((time - self.shield_last_toggled) / SHIELD_LIFESPAN), 1), 0)
        return (int(fraction * 100) // 10 * 10) / 100.0
        
    def shoot (self, rubric_behaviour):
        """ create a missile with initial pos at the tip of the ship and a velocity
        that is equal to the ship's velocity plus the speed of the missile """
        uv = angle_to_vector (self.angle)
        dist = self.radius + 2 * missile_info.get_radius()
        # use a different image for "DESTROY" and "SPLIT" missiles
        image = missile_images[0] if rubric_behaviour else missile_images[1]
        missile = Sprite([self.pos[0] + uv[0] * dist, self.pos[1] + uv[1] * dist],
                         [self.vel[0] + uv[0] * MISSILE_SPEED, 
                          self.vel[1] + uv[1] * MISSILE_SPEED], 
                         self.angle, 0, image, missile_info, missile_sound)
        missile.set_type ("DESTROY" if rubric_behaviour else "SPLIT")
        return missile
    
    def shields_up(self):
        if not self.shield and time - self.shield_last_toggled > SHIELD_REGEN:
            self.shield = True
            self.shield_last_toggled = time
    
    def draw(self,canvas):
        """ draw the ship - use alternate image when thrust is not zero """
        img_offset = (0 if self.thrust == 0 else self.image_size[0])
        canvas.draw_image(self.image, 
                          (self.image_center[0] + img_offset, self.image_center[1]),
                          self.image_size, self.pos, self.image_size, self.angle)
        if self.shield:
            alpha = 0.5 * self.get_shield_fraction()
            canvas.draw_circle (self.pos, self.radius * 1.2, 3, 
                                "RGBA(255, 0, 0, " + str(2 * alpha) + ")", 
                                "RGBA(255, 255, 255, " + str(alpha) + ")")

    def update(self):
        """ called from the draw handler FPS times per second to update pos, vel and angle """
        if self.angle_vel != 0:
            self.angle += self.angle_vel / FPS
            if self.angle_vel < 0:
                self.angle_vel = max(self.angle_vel - DELTA_AV / FPS, -MAX_AV)
            else:
                self.angle_vel = min(self.angle_vel + DELTA_AV / FPS, MAX_AV)
        delta_vel = angle_to_vector(self.angle)
        # update ship pos using current velocity and friction
        self.vel[0] = (self.vel[0] + self.thrust * delta_vel[0] / FPS) * FF_FPS
        self.vel[1] = (self.vel[1] + self.thrust * delta_vel[1] / FPS) * FF_FPS
        self.pos[0] = (self.pos[0] + self.vel[0] / FPS) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1] / FPS) % HEIGHT
        # if the velocity drops below MIN_VEL set vel to zero
        if abs(self.vel[0]) < MIN_VEL and self.thrust == 0:
            self.vel[0] = 0
        if abs(self.vel[1]) < MIN_VEL and self.thrust == 0:
            self.vel[1] = 0
        if self.thrust != 0:
            self.thrust = min(self.thrust + DELTA_T / FPS, MAX_T)
        if self.shield and time - self.shield_last_toggled > SHIELD_LIFESPAN:
            self.shield = False
            self.shield_last_toggled = time
    
def process_sprite_group(canvas, sprite_group):
    """ update and draw a sprite group """
    global paused
    for sprite in sprite_group:
        sprite.draw (canvas)
        if not paused:
            sprite.update()

def remove_dead_objects():
    """ remove all objects that have reached their lifespan """
    for sprite_set in [missile_group, explosion_group]:
        remove_set = set()
        for sprite in sprite_set:
            if not sprite.is_alive():
                remove_set.add (sprite)
        sprite_set.difference_update(remove_set)

def group_group_collide (g1, g2, collide_func):
    """ generic function for handling collisions between set of objects
        collide_func returns a tuple of booleans to indicate if the two
        objects should be removed from their groups """
    g1_collide_set = set()
    for o1 in g1:
        g2_collide_set = set()
        for o2 in g2:
            if o1.collide(o2):
                remove = collide_func(o1, o2) if collide_func else (False, False)
                if (remove[0]):
                    g1_collide_set.add (o1)
                if (remove[1]):
                    g2_collide_set.add (o2)
            g2.difference_update(g2_collide_set)
        g1.difference_update(g1_collide_set)

def add_explosion (pos, vel, scale, image):
    """ create and add an explosion to the group """
    explosion = Sprite(pos, vel, 0, 0, image, explosion_info, explosion_sound)
    explosion.set_scale (scale)
    explosion_group.add (explosion)
                         
def missile_rock (missile, rock):
    """ handle a single collsion between a missile and a rock """
    global score
    score += 1
    # increase the difficulty after DELTA_SCORE points
    if score - difficulty_jump == DELTA_SCORE:
        increase_difficulty()
    # create an explosion with the rock's pos, vel and scale
    add_explosion (rock.get_pos(), rock.get_vel(), rock.get_scale(), 
                   random.choice(explosion_images)) 
    # if missile is of type "SPLIT" and the rock is not already small,
    # create two new smaller rocks and give them a random velocity
    if missile.get_type() == "SPLIT" and rock.get_scale() != 0.5:
            rock_angle = vector_to_angle (rock.get_vel())
            new_rock1 = create_rock(rock.get_pos(), rock.get_vel(), 
                                    rock.get_angle(), 
                                    rock.get_angle_vel() * random.choice([-1, 1]),
                                    rock.image)
            vel = angle_to_vector(rock_angle + random.random() * math.pi)
            new_rock1.set_vel ([vel[0] * FPS, vel[1] * FPS])
            new_rock2 = create_rock(rock.get_pos(), rock.get_vel(), 
                                    -1 * rock.get_angle(), 
                                    rock.get_angle_vel() * random.choice([-1, 1]),
                                    rock.image)
            vel = angle_to_vector(rock_angle - random.random() * math.pi)
            new_rock2.set_vel ([vel[0] * FPS, vel[1] * FPS])
            new_scale = 0.75 if rock.get_scale() == 1 else 0.5
            new_rock1.set_scale(new_scale)
            new_rock2.set_scale(new_scale)
            rock_group.add (new_rock1)
            rock_group.add (new_rock2)
    return (True, True)
    
def explosion_rock (explosion, rock):
    """ handle a single collsion between an explosion and a rock """
    global score
    # if a rock was just created by splitting a larger rock, don't immediately
    # destroy it in the explosion of the parent rock
    if rock.get_age() <= explosion_info.get_lifespan() and rock.get_scale() < 1:
        return (False, False)
    score += 1
    # increase the difficulty after DELTA_SCORE points
    if score - difficulty_jump == DELTA_SCORE:
        increase_difficulty()
    # create an explosion with the rock's pos, vel and scale
    add_explosion (rock.get_pos(), rock.get_vel(), rock.get_scale(), 
                   random.choice(explosion_images)) 
    return (False, True)
    
def ship_rock (ship, rock):
    """ handle a single collision between the ship and a rock """
    global lives
    # a ship can be hit by more than one rock at the same time, so prevent
    # lives becoming negative
    lives = max (lives - 1, 0)
    # create an explosion with the ships's pos, vel and scale
    add_explosion (ship.get_pos(), ship.get_vel(), 1, ship_explosion_image) 
    # make shield available immediately
    ship.shields = False
    ship.shields_last_toggled = -1 * SHIELD_LIFESPAN
    return (False, True)

def draw(canvas):
    """ draw handler for canvas """
    global time, game_started, lives, score, rock_group, missile_group, explosion_group
    global direction, difficulty_jump, level_change_counter, paused
    
    # game is in progress and we lost all our lives -> game ends
    if game_started and lives == 0:
        display_splash_screen()
    
    # animiate background
    time += 1
    wtime = (WIDTH if direction == -1 else 0) + ((time / 4) % WIDTH) * direction
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if game_started and not paused:
        remove_dead_objects()
        # check the various collsions between ship / rocks / explosions
        if not my_ship.get_shield():
            group_group_collide (set([my_ship]), rock_group, ship_rock)
        group_group_collide (missile_group, rock_group, missile_rock)
        group_group_collide (explosion_group, rock_group, explosion_rock)

    # draw and update ship and sprites
    process_sprite_group (canvas, rock_group)
    my_ship.draw(canvas)
    if not paused:
        my_ship.update()
    process_sprite_group (canvas, missile_group)
    process_sprite_group (canvas, explosion_group)
    
    # ui text
    level_change_counter = max(level_change_counter - 1, 0)
    texts = ui_texts()
    canvas.draw_text (texts[0], (UI_TEXT_MARGIN, UI_FONT_SIZE), 
                      UI_FONT_SIZE, UI_FONT_COLOR, UI_FONT)
    canvas.draw_text (texts[1], (UI_TEXT_MARGIN, 2 * UI_FONT_SIZE), 
                      UI_FONT_SIZE, UI_FONT_COLOR, UI_FONT)
    level_factor = 1 if level_change_counter > 0 else 2.0 / 3.0
    text_width = frame.get_canvas_textwidth(texts[2], UI_FONT_SIZE*level_factor, UI_FONT)
    canvas.draw_text (texts[2], ((WIDTH - text_width)/2, UI_FONT_SIZE), UI_FONT_SIZE*level_factor, 
                      UI_FLASH_COLOR if level_change_counter > 0 else UI_FONT_COLOR,
                      UI_FONT)
    text_width = frame.get_canvas_textwidth(texts[3], UI_FONT_SIZE, UI_FONT)
    canvas.draw_text (texts[3], (WIDTH - text_width - UI_TEXT_MARGIN, UI_FONT_SIZE), 
                      UI_FONT_SIZE, UI_FONT_COLOR, UI_FONT)

    if paused:
        paused_text = "Game paused - press p to continue"
        text_width = frame.get_canvas_textwidth(paused_text, UI_FONT_SIZE, UI_FONT)
        canvas.draw_text (paused_text, ((WIDTH - text_width)/2, HEIGHT / 2), 
                          UI_FONT_SIZE, UI_FLASH_COLOR, UI_FONT)
        
    if not game_started:
        canvas.draw_image (splash_image, splash_info.get_center(), splash_info.get_size(), 
                           [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        for line in range(4, len(texts)):
            text_width = frame.get_canvas_textwidth(texts[line], UI_FONT_SIZE, UI_FONT)
            canvas.draw_text (texts[line], ((WIDTH - text_width)/2, HEIGHT - (line - 3) * UI_FONT_SIZE), 
                              UI_FONT_SIZE, UI_FONT_COLOR, UI_FONT)
        
def create_rock(pos, vel, angle, angle_vel, image = None):
    """ create a new rock with a fixed (for splitting larger rocks) or random image """
    if not image:
        image = random.choice(asteroid_images)
    rock = Sprite(pos, vel, angle, angle_vel, image, asteroid_info)
    return rock
    
def rock_spawner():
    """ timer handler that spawns a rock """
    global my_ship, rock_group, rock_vel, rocks_allowed, paused
    if not game_started or len(rock_group) >= rocks_allowed or paused:
        return
    # create a new position for the rock that is at least rock_spawn_dist
    # from the ship
    pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    while dist(pos, my_ship.get_pos()) < rock_spawn_dist:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    # use some nice random values for the rock's vel, angle, and angle_vel
    vel = [random.randrange(-rock_vel, rock_vel), random.randrange(-rock_vel, rock_vel)]
    angle = random.random() * math.pi * random.choice([-1, 1])
    angle_vel = random.random() * math.pi * 2 * random.choice([-1, 1])
    rock_group.add(create_rock(pos, vel, angle, angle_vel))

def toggle_sound():
    global sound
    sound = not sound
    soundtrack.set_volume (1 if sound else 0)
    missile_sound.set_volume (.5 if sound else 0)
    ship_thrust_sound.set_volume (1 if sound else 0)
    explosion_sound.set_volume (1 if sound else 0)

def toggle_pause():
    global paused
    paused = not paused

def keydown(key):
    """ keydown event handler """
    global my_ship, missile_group, game_started, paused
    if not game_started or paused and key != simplegui.KEY_MAP["p"]:
        return False
    # the x - key is used to shoot "rock-splitting" missiles, this way you don't 
    # have to switch between modes to implement the "classic" game behaviour
    if key == simplegui.KEY_MAP["space"]:
        missile_group.add (my_ship.shoot(True))
    elif key == simplegui.KEY_MAP["x"]:
        missile_group.add (my_ship.shoot(False))
    elif key == simplegui.KEY_MAP["s"]:
        toggle_sound()
    elif key == simplegui.KEY_MAP["p"]:
        toggle_pause()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(-MIN_AV)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(MIN_AV)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(MIN_T)
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP["down"]:
        my_ship.shields_up()
  
def keyup(key):
    """ keyup event handler """
    global my_ship
    if key == simplegui.KEY_MAP["left"] and my_ship.angle_vel < 0:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP["right"] and my_ship.angle_vel > 0:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(0)
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()

def mouse_clicked(position):
    """ mouse click handler for dismissing the splash screen """
    global game_started
    if not game_started:
        start_new_game()
    
def ui_texts ():
    """ return a list of texts used for the ui display """
    global my_ship
    shield_percent = int(my_ship.get_shield_fraction() * 100)
    shield_text = "Ready" if shield_percent == 100 else str(shield_percent) + "%"
    return ["Lives:  " + str(lives),
            "Shield: " + shield_text, 
            "Level: " + str(level) + " (" + str(rocks_allowed) + " Rocks, " +
                "speed " + str(rock_vel) + ")",
            " Score: " + str(score),
            "press down for shields, p for pause, s for sound on/off",
            "press x to split rocks (classic mode)",
            "press space to destroy rocks (grading rubric mode)"]
            

def display_splash_screen ():
    """ clear all sprite groups and display the splash screen in the next draw-handler """
    global rock_group, missile_group, explosions_group, game_started, my_ship
    rock_group = set()
    missile_group = set()
    explosion_group = ()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info)
    game_started = False
    # pause the background sound so that it doesn't continue playing when the
    # frame is closed while displaying the splash screen
    ship_thrust_sound.pause()
    ship_thrust_sound.rewind()
    soundtrack.pause()

def increase_difficulty():
    """ increase the level and the difficulty of the game """
    global rocks_allowed, difficulty_jump, rock_vel, rock_spawn_dist
    global score, level, level_change_counter, my_ship
    level += 1
    level_change_counter = 2 * FPS
    rocks_allowed += 1
    rock_vel = rock_vel + DELTA_ROCK_VEL
    rock_spawn_dist = max(rock_spawn_dist-DELTA_ROCK_SPAWN_DIST, my_ship.get_radius())
    difficulty_jump = score
    
def start_new_game  ():
    """ reset all variables and start a new game """
    global score, lives, game_started, debris_image, nebula_image, level
    global direction, rocks_allowed, rock_vel, difficulty_jump, my_ship
    global rock_spwan_dist
    level = 1
    score = 0
    lives = NR_OF_LIVES
    game_started = True
    # select a random background
    debris_image = random.choice(debris_images)
    nebula_image = random.choice(nebula_images)
    direction = random.choice ([1, -1])
    # reset level and difficulty
    difficulty_jump = 0
    rocks_allowed = MIN_ROCKS
    rock_vel = MIN_ROCK_VEL
    rock_spawn_dist = MAX_ROCK_SPAWN_DIST
    soundtrack.rewind()
    soundtrack.play()
    
# initialize frame and register timers
frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_clicked)
timer = simplegui.create_timer(1000.0, rock_spawner)
display_splash_screen ()
frame.start()
timer.start()