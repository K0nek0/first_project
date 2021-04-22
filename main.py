import interaction as i
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button


class Object(Widget):
    def __init__(self, **kw):
        super(Object, self).__init__()

        self.step = kw['step']
        self.color = kw['color']
        self.pos = kw['pos']
        self.vel = kw['vel']
        self.size = kw['size']
        self.COORDS_small = []

        self.interect_small = i.Interaction_small(x0=self.pos[0],
                                                  vx0=self.vel[0],
                                                  y0=self.pos[1],
                                                  vy0=self.vel[1])

        for j in range(self.step):
            self.COORDS_small.append(
                (float(self.interect_small.solve_func()[0][j]) * 100 + 250,
                 float(self.interect_small.solve_func()[1][j]) * 100 + 250))


    def draw_small(self):
        self.canvas.add(self.color)
        self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.ellipse_c = Ellipse(pos=(250, 250), size=(20, 20))
        self.canvas.add(self.ellipse)
        self.canvas.add(self.ellipse_c)

    def move_small(self, k):
        self.pos = Vector(self.COORDS_small[k])
        self.ellipse.pos = self.pos

class PainterWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            # Color(1,0,0,1)
            # self.ellipse = Ellipse(pos=(touch.x, touch.y), size = (10,10))

            self.x1 = touch.x
            self.y1 = touch.y
            print('x1_self: ',self.x1)
            print('y1_self: ',self.y1)

    def on_touch_up(self, touch):

            self.k=200
            self.x2 = touch.x
            self.y2 = touch.y
            # Color(0,0,0,1)
            # self.ellipse = Ellipse(pos=(self.x1, self.y1), size = (10,10))

            # x и y векторы 
            self.x_vector = self.x1 - self.x2
            self.y_vector = self.y1 - self.y2
            print('x2_self: ',self.x2)
            print('y2_self: ',self.y2)

            # модуль
            self.vector_modul = (self.x_vector**2+self.y_vector**2)**(1/2)

            try:
                self.cos_phi = self.x_vector/self.vector_modul
            except ZeroDivisionError:
                self.cos_phi = 0

            try:
                self.sin_phi = self.y_vector/self.vector_modul
            except ZeroDivisionError:
                self.sin_phi = 0


            self.v_modul = self.k*self.vector_modul
            # скорости
            self.vx = self.v_modul*self.cos_phi
            self.vy = self.v_modul*self.sin_phi
            print('vx: ',self.vx)
            print('vy: ',self.vy)
            self.object = Move()
            self.object.create_small(color=Color(1, 0, 0),
                                    pos=(self.x1* 149 * 10**6, self.y1* 149 * 10**7),
                                    vel=(self.vx, self.vy),
                                    size=(8, 8))
            Clock.schedule_interval(self.object.update_small, .04)
            self.parent.add_widget(self.object)


class Move(Widget):
    def __init__(self):
        super(Move, self).__init__()
        self.counter = 0
        self.n = i.T

    def update_small(self, dt):
        if self.counter == self.n - 1:
            self.counter = 0
        self.counter += 1
        self.object.move_small(self.counter)

    def create_small(self, color, pos, size, vel):
        self.object = Object(step=self.n,
                             color=color,
                             pos=pos,
                             vel=vel,
                             size=size)
        self.object.draw_small()
        self.add_widget(self.object)


class PlanetApp(App):

    def build(self):
        return PainterWidget()


PlanetApp().run()
