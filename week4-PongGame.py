# Implementation of classic arcade game Pong

import simplegui
import random
import math
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [2, 2]
    ball_vel[1] = -random.randrange(60, 180)
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)
    else:
        ball_vel[0] = -random.randrange(120, 240)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    randomnum = random.randrange(0,2)
    if randomnum == 0:
        direction = RIGHT
    else:
        direction = LEFT
    spawn_ball(direction)
    
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH,HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
def button_handler():
    new_game()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0] * 0.01
    ball_pos[1] += ball_vel[1] * 0.01
    if(ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    if(ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    if(ball_pos[0] >= WIDTH-4-20):
        if(math.fabs(ball_pos[1]-paddle2_pos[1]) <= HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0]*1.1)
        else:
            spawn_ball(LEFT)
            score1 = score1 + 1
    
    if(ball_pos[0] <= 4+20):
        if(math.fabs(ball_pos[1]-paddle1_pos[1]) <= HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]*1.1
        else:
            spawn_ball(RIGHT)
            score2 = score2 + 1


# draw ball
canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    # update paddle's vertical position, keep paddle on the screen
    
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    if paddle1_pos[1] >= HEIGHT - HALF_PAD_HEIGHT or paddle1_pos[1] <= HALF_PAD_HEIGHT:
        paddle1_vel = 0
if paddle2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT or paddle2_pos[1] <= HALF_PAD_HEIGHT:
    paddle2_vel = 0
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0]-4,paddle1_pos[1]-40], [paddle1_pos[0]+4,paddle1_pos[1]-40], [paddle1_pos[0]+4,paddle1_pos[1]+40], [paddle1_pos[0]-4,paddle1_pos[1]+40]], 1, 'White', 'White')
    canvas.draw_polygon([[paddle2_pos[0]-4,paddle2_pos[1]-40], [paddle2_pos[0]+4,paddle2_pos[1]-40], [paddle2_pos[0]+4,paddle2_pos[1]+40], [paddle2_pos[0]-4,paddle2_pos[1]+40]], 1, 'White', 'White')
    
    # determine whether paddle and ball collide
    
    # draw scores
    count1 = str(score1)
    count2 = str(score2)
    canvas.draw_text(count1, (250, 50), 30, 'White')
    canvas.draw_text(count2, [350, 50], 30, 'White')
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -2
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 2
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -2
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 2

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', button_handler,100)


# start frame
new_game()
frame.start()
