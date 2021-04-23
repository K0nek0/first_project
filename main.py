import interaction as i
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from random import randint


class Object(Widget):
    def __init__(self, **kw):
        super(Object, self).__init__()

        self.step = kw['step']
        self.pos = kw['pos']
        self.vel = kw['vel']
        self.COORDS = []

        self.interect = i.Interaction(x0=self.pos[0],
                                      vx0=self.vel[0],
                                      y0=self.pos[1],
                                      vy0=self.vel[1])

        for j in range(self.step):
            self.COORDS.append(
                (float(self.interect.solve_func()[0][j])*100+250,
                 float(self.interect.solve_func()[1][j])*100+250))

    def draw(self):
        self.ellipse = Ellipse(pos=self.pos, size=(15, 15))
        self.ellipse_c = Ellipse(pos=(250, 250), size=(50, 50))
        self.canvas.add(self.ellipse)
        self.canvas.add(self.ellipse_c)

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

    def create(self, pos, vel):
        self.object = Object(step=self.n,
                             pos=pos,
                             vel=vel)
        self.object.draw()
        self.add_widget(self.object)


class PainterWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, randint(0,1), randint(0,1), 1)
            self.ellipse = Ellipse(pos=(touch.x, touch.y), size = (15,15))

        self.x1 = touch.x
        self.y1 = touch.y
        # print('x1_self: ',self.x1)
        # print('y1_self: ',self.y1)

    def on_touch_up(self, touch):
        self.x2 = touch.x
        self.y2 = touch.y

        # убирание начального эллипса
        self.canvas.children.remove(self.ellipse)
        
        # x и y векторы 
        self.x_vector = self.x1 - self.x2
        self.y_vector = self.y1 - self.y2
        # print('x2_self: ',self.x2)
        # print('y2_self: ',self.y2)

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
        # print('vx: ',self.vx)
        # print('vy: ',self.vy)

        # задавание данных объекту
        self.object = Move()
        self.object.create(pos=(((self.x1-250)/100)*i.ae, ((self.y1-250)/100)*i.ae),
                           vel=(self.vx, self.vy))
        Clock.schedule_interval(self.object.update, .04)
        self.parent.add_widget(self.object)


class PlanetApp(App):
    def build(self):
        return PainterWidget()
PlanetApp().run()
