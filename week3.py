# template for "Stopwatch: The Game"
import simplegui
# define global variables
global t
t = 0
global x
x = 0
global y
y = 0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    t = t - D
    
    t = t/10
    C = t % 10
    t = t - C
    
    B = (t%60)/10
    t = t - B*10
    
    A = (t / 60) % 10
    
    return str(A) + ':' + str(B) + str(C) + '.' + str(D)



# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    timer.start()

def Stop():
    global t,x,y
    timer.stop()
    y = y + 1
    if(t % 10 == 0):
        x = x + 1

def Reset():
    timer.stop()
    global t,x,y
    t = 0
    x = 0
    y = 0


# define event handler for timer with 0.1 sec interval
def D_handler():
    global t
    t += 1
#print t

# define draw handler
def draw_handler(canvas):
    global t,x,y
    count = str(x) + '/' + str(y)
    canvas.draw_text(format(t), (75,55), 25, 'White')
    canvas.draw_text(count,(170,15), 15, 'Red')



# create frame
frame = simplegui.create_frame("Stopwatch",200,100)

# register event handlers
timer = simplegui.create_timer(100, D_handler)

button1 = frame.add_button('Start', Start, 100)
button2 = frame.add_button('Stop', Stop, 100)
button3 = frame.add_button('Reset', Reset, 100)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()


# Please remember to review the grading rubric