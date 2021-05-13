import interaction as i
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

from kivy.config import Config
Config.set('graphics', 'resizable', 1)

from kivy.lang import Builder
Builder.load_file('center.kv')

DRAG_START = ()
DRAG_END = ()
DRAGGING = False

class Object(Widget):
    def __init__(self, **kw):
        super(Object, self).__init__()
        self.step = kw['step']
        self.color = kw['color']
        self.pos = kw['pos']
        self.vel = kw['vel']
        self.COORDS = []

        self.interect = i.Interaction(x0=self.pos[0],
                                      vx0=self.vel[0],
                                      y0=self.pos[1],
                                      vy0=self.vel[1])

        for j in range(self.step):
            self.COORDS.append(
                (float(self.interect.solve_func(j)[0])*100+225,
                 float(self.interect.solve_func(j)[1])*100+419))

    def draw(self):
        self.canvas.add(self.color)
        self.ellipse = Ellipse(pos=self.pos, size=(i.r, i.r))
        self.canvas.add(self.ellipse)

    def move(self, c):
        self.pos = Vector(self.COORDS[c])
        self.ellipse.pos = self.pos

    
class Move(Widget):
    def __init__(self):
        super(Move, self).__init__()
        self.counter = 0
        self.n = i.T

    def update(self, dt):
        if self.counter == self.n - 1:
            self.counter = 0
        self.counter += 1
        self.object.move(self.counter)

    def create(self, color, pos, vel):
        self.object = Object(key=True,
                             color=color,
                             step=self.n,
                             pos=pos,
                             vel=vel)
        self.object.draw()
        self.add_widget(self.object)


class Painter(Widget):
    def __init__(self, **kw):
        super(Painter, self).__init__(**kw)
        Window.bind(mouse_pos=self.mouse_pos)
        self.start = []
        
    def mouse_pos(self, window, pos):
        if DRAGGING == True:
            self.drawLine(pos)

    def drawLine(self, mPos):
        self.mPos = mPos

        # x и y векторы 
        self.x_vector = self.x1 - self.mPos[0]
        self.y_vector = self.y1 - self.mPos[1]

        # модуль векторов
        self.vector_modul = (self.x_vector**2+self.y_vector**2)**(1/2)

        try:
            self.cos_phi = self.x_vector/self.vector_modul
        except ZeroDivisionError:
            self.cos_phi = 0
        try:
            self.sin_phi = self.y_vector/self.vector_modul
        except ZeroDivisionError:
            self.sin_phi = 0

        self.v_modul = i.k*self.vector_modul

        # скорости
        self.vx = self.v_modul*self.cos_phi
        self.vy = self.v_modul*self.sin_phi

        self.canvas.after.clear()
        with self.canvas.after:
            self.label = Label(text=f'Скорость: {int(self.v_modul)} м/с', pos=(self.x1, self.y1))

        self.canvas.clear()
        with self.canvas:
            self.line = Line(points=[DRAG_START[0]+i.r/2, DRAG_START[1]+i.r/2, mPos[0], mPos[1]],
                             width=1.4)

    def on_touch_down(self, touch):
        with self.canvas.before:
            self.color = Color(1, randint(0,1), randint(0,1), 1)
            self.ellipse = Ellipse(pos=(touch.x, touch.y), size=(i.r, i.r))

        self.x1 = touch.x
        self.y1 = touch.y

        global DRAGGING, DRAG_START
        DRAGGING = True
        DRAG_START = touch.pos

    def on_touch_up(self, touch):
        # убирание начальных элементов
        self.canvas.children.remove(self.line)
        self.canvas.before.remove(self.ellipse)
        self.canvas.after.clear()

        # задавание данных объекту
        self.object = Move()
        self.object.create(color=self.color,
                           pos=(((self.x1-225)/100)*i.ae, ((self.y1-419)/100)*i.ae),
                           vel=(self.vx, self.vy))
        Clock.schedule_interval(self.object.update, .04)
        self.parent.add_widget(self.object)

        global DRAGGING, DRAG_START
        DRAGGING = False
        DRAG_END = touch.pos


class PlanetApp(App):
    def build(self):
        return Painter()

if __name__ == '__main__':
    PlanetApp().run()

#self.center