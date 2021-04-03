from tkinter import *
# from tkinter import colorchooser
from tkinter.colorchooser import askcolor
from math import *
import tkinter.font as font
colors = ['blue', 'red', 'green', 'yellow']
root = Tk()
field_height = 600
field_width = 1000
ident_x = 100  # отступ поля от левого края канвы
ident_y = 70  # отступ поля от верхнего края канвы
root.geometry('1890x1050')
canv = Canvas(root, bg='white')
k = 0
line_width = 10  # толщина рисуемой линии
radius_inter = 10
lines_in_polygon = []


# count_lines = 0
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        return [self.x, self.y]

    def is_in_polygon(self, other):
        count_crossing = 0
        for i in other():
            if (self.x == i.x and self.y > i.y):
                count_crossing += 1
        return count_crossing
        if (count_crossing % 2 == 1):
            return True
        else:
            return False


class Polygon(object):
    def __init__(self, coord):
        self.xcoords = []
        self.ycoords = []
        self.coords = []
        self.simpcoords = []
        for i in coord:
            self.xcoords.append(i.x)
            self.ycoords.append(i.y)
            self.coords.append(i)
            self.simpcoords.append([i.x, i.y])

    def __call__(self):
        return self.coords

    def fill(self, colour, lw):
        canv.create_polygon(self.simpcoords, fill=colour, outline='black', width=lw)

    def app(self, dot):
        self.xcoords.append(dot.x)
        self.ycoords.append(dot.y)
        self.coords.append(dot)
        self.simpcoords.append([dot.x, dot.y])


class App(object):
    def __init__(self):
        self.line_width = line_width
        self.x0 = -1
        self.y0 = -1
        self.x = -1
        self.y = -1
        self.cur_line = Polygon([])
        self.k = 0
        self.st_inter = []
        self.fin_inter = []
        self.lines = []
        self.sliced_lines = []
        self.field_width = field_width
        self.field_height = field_height
        self.line_width = line_width
        # print(lines[0])
        self.num_bound = 0
        self.lines.append(self.create_bounds())
        self.sliced_lines.append(self.create_bounds())
        self.lines[0].fill("white", self.line_width)
        canv.bind('<Button-1>', self.start)
        canv.bind('<B1-Motion>', self.draw)
        canv.bind('<ButtonRelease-1>', self.stop)
        canv.place(x=ident_x, y=ident_y, width=field_width + 20, height=field_height + 20)
        self.fw = StringVar()
        self.fh = StringVar()
        self.lw = StringVar()
        width_label = Label(text="Width of field: ")
        height_label = Label(text="Height of field: ")
        line_width_label = Label(text="Width of line: ")
        width2_label = Label(text="(from 100 to 1720)")
        height2_label = Label(text="(from 100 to 930)")
        line_width2_label = Label(text="(from 2 to 20)")
        width_label.place(x=100, y=10)
        height_label.place(x=100, y=30)
        line_width_label.place(x=100, y=50)
        width2_label.place(x=330, y=10)
        height2_label.place(x=330, y=30)
        line_width2_label.place(x=330, y=50)
        self.width_entry = Entry(textvariable=self.fw)
        self.height_entry = Entry(textvariable=self.fh)
        self.line_width_entry = Entry(textvariable=self.lw)
        self.width_entry.place(x=190, y=10)
        self.height_entry.place(x=190, y=30)
        self.line_width_entry.place(x = 190, y = 50)
        self.width_entry.insert(0, self.field_width)
        self.height_entry.insert(0, self.field_height)
        self.line_width_entry.insert(0, self.line_width)

    def start(self, event):
        self.x0 = event.x
        self.y0 = event.y
        # if len(a.find_overlapping(x0-2, y0-2, x0+2, y0+2)) > 0:
        self.cur_line = Polygon([])

    def interpolation(self, cur_line_sliced):
        cur_line_inter = Polygon([])
        for i in range(len(cur_line_sliced()) - 1):
            cur_line_inter.app(cur_line_sliced()[i])
            if abs(cur_line_sliced.coords[i].x - cur_line_sliced.coords[i + 1].x) > 1 or abs(
                    cur_line_sliced.coords[i].y - cur_line_sliced.coords[i + 1].y) > 1:
                cir = cur_line_sliced.coords[i].x - cur_line_sliced.coords[i + 1].x
                for j in range(abs(cir)):
                    # if abs(cur_line_inter.coords[-1].y - cur_line_sliced.coords[i + 1].y) == 0:

                    koef = (cur_line_inter.coords[-1].y - cur_line_sliced.coords[i + 1].y) // abs(
                        cur_line_inter.coords[-1].x - cur_line_sliced.coords[i + 1].x)
                    if (cir < 0):
                        cur_line_inter.app(
                            Point(cur_line_inter.coords[-1].x - 1, cur_line_inter.coords[-1].y + int(koef)))
                    else:
                        cur_line_inter.app(
                            Point(cur_line_inter.coords[-1].x + 1, cur_line_inter.coords[-1].y + int(koef)))
        # print(cur_line_sliced.coords)
        return cur_line_inter

    def draw(self, event):  # рисование кривой
        self.x = event.x
        self.y = event.y
        if 10 <= self.x <= self.field_width + 10 and 10 <= self.y <= self.field_height + 10:
            self.cur_line.app(Point(self.x, self.y))
            print(len(self.cur_line()))
            #            if len(self.cur_line.coords) > 0:
            canv.create_line(self.x0, self.y0, self.x, self.y, width=self.line_width, tag='recent')
            self.x0 = self.x
            self.y0 = self.y

    def choose_colour1(self):
        colors[0] = askcolor()[1]
        button_color1['bg'] = colors[0]
        self.translate()

    def choose_colour2(self):
        colors[1] = askcolor()[1]
        button_color2['bg'] = colors[1]
        self.translate()

    def choose_colour3(self):
        colors[2] = askcolor()[1]
        button_color3['bg'] = colors[2]
        self.translate()

    def choose_colour4(self):
        colors[3] = askcolor()[1]
        button_color4['bg'] = colors[3]
        self.translate()

    def check_point(self, event):
        x = event.x
        y = event.y
        p = Point(x, y)
        if p.is_in_polygon(self.lines[0]) % 2 == 1:
            check_button['bg'] = "green"
        else:
            check_button['bg'] = "red"
        check_button['text'] = p.is_in_polygon(self.lines[0])


    def create_bounds(self):
        if self.num_bound == 0:
            field_line = Polygon([])
            a = self.field_height // 2
            b = self.field_width // 2
            for i in range(4 * b):
                if i < b:
                    y = int(sqrt((a ** 2) * abs((1 - (i / b) ** 2))))
                    field_line.app(Point(10 + b + i, 10 + y + a))
                elif i < 2 * b:
                    y = -int(sqrt((a ** 2) * abs((1 - ((i - 2 * b) / b) ** 2))))
                    field_line.app(Point(10 + 3 * b - i, 10 + y + a))
                elif i < 3 * b:
                    y = -int(sqrt((a ** 2) * abs((1 - ((i - 2 * b) / b) ** 2))))
                    field_line.app(Point(10 + 3 * b - i, 10 + y + a))
                else:
                    y = int(sqrt((a ** 2) * abs((1 - ((i - 4 * b) / b) ** 2))))
                    field_line.app(Point(10 - 3 * b + i, 10 + y + a))
            return field_line
        if self.num_bound == 1:
            field_line = Polygon([])
            for i in range(self.field_width):
                field_line.app(Point(10 + i, 10))
            for i in range(self.field_height):
                field_line.app(Point(10 + self.field_width, 10 + i))
            for i in range(self.field_width):
                field_line.app(Point(10 + self.field_width - i, 10 + self.field_height))
            for i in range(self.field_height):
                field_line.app(Point(10, 10 + self.field_height - i))
            return field_line
    def draw_circle(self):  # рисование замкнутого на себя полигона
        self.k += 1
        if self.k == 4:
            self.k = 0
        self.cur_line.fill(colors[self.k], self.line_width)
        self.lines.append(self.cur_line)
        cur_line = Polygon([])

    def draw_polygon(
            self):  # рисование полигона, если стартовая точка пересечения с другим полигоном в его массиве находится раньше финальной
        new_polyg1 = Polygon([])
        for i in self.lines[self.st_inter[0]]()[self.fin_inter[1]:self.st_inter[1] + 1]:
            new_polyg1.app(i)

        for i in range(len(self.cur_line())):
            new_polyg1.app(self.cur_line()[i])
        new_polyg2 = Polygon([])

        for i in self.lines[self.st_inter[0]]()[self.st_inter[1]: len(self.lines[self.st_inter[0]]())]:
            new_polyg2.app(i)
        for i in self.lines[self.st_inter[0]]()[0:self.fin_inter[1] + 1]:
            new_polyg2.app(i)
        for i in range(len(self.cur_line())):
            new_polyg2.app(self.cur_line()[len(self.cur_line()) - i - 1])
        self.lines.append(new_polyg1)
        self.lines.append(new_polyg2)
        self.lines.pop(self.st_inter[0])

    def draw_reverse_polygon(
            self):  # рисование полигона, если финальная точка пересечения с другим полигоном в его массиве находится раньше стартовой
        new_polyg1 = Polygon([])
        for i in self.lines[self.st_inter[0]]()[self.st_inter[1]:self.fin_inter[1] + 1]:
            new_polyg1.app(i)
        for i in range(len(self.cur_line())):
            new_polyg1.app(self.cur_line()[len(self.cur_line()) - i - 1])
        new_polyg2 = Polygon([])
        for i in self.lines[self.st_inter[0]]()[self.fin_inter[1]: len(self.lines[self.st_inter[0]]())]:
            new_polyg2.app(i)
        for i in self.lines[self.st_inter[0]]()[0:self.st_inter[1] + 1]:
            new_polyg2.app(i)
        for i in range(len(self.cur_line())):
            new_polyg2.app(self.cur_line()[i])
        self.lines.pop(self.st_inter[0])
        self.lines.append(new_polyg1)
        self.lines.append(new_polyg2)

    def is_array_inter(self, array1, array2):#
        for i in array1:
            if i in array2:
                return True
        return False

    def paint(self):
        self.colored_graph = [4 for i in range(len(self.BFS_graph))]
        BFS_control = []
        BFS_control.append(0)
        while len(BFS_control) != 0:
            for i in self.BFS_graph[BFS_control[0]]:
                if self.colored_graph[i] == 4:
                    for j in range(4):
                        g = True
                        for k in self.BFS_graph[i]:
                            if self.colored_graph[k] == j:
                                g = False
                                break
                        if g:
                            self.colored_graph[i] = j
                            break
                    BFS_control.append(i)
            BFS_control.pop(0)
        if not(4 in self.colored_graph):
            for i in range(len(self.lines)):
                self.lines[i].fill(colors[self.colored_graph[i]], self.line_width)
        if 4 in self.colored_graph:
            self.new_sliced_lines = [self.sliced_lines[-1]]
            for i in self.sliced_lines[:len(self.sliced_lines)-1]:
                self.new_sliced_lines.append(i)
            self.sliced_lines = self.new_sliced_lines.copy()
            self.paint()

    def translate(self):
        self.graph = []
        for i in range(len(self.lines)):
            self.graph.append([])
            for j in range(len(self.sliced_lines)):
                # print(self.sliced_lines[j].coords)
                if self.sliced_lines[j]()[len(self.sliced_lines[j]()) // 2] in self.lines[i].coords:
                    self.graph[i].append(j)
        self.BFS_graph = [[] for i in range(len(self.graph))]
        for i in range(len(self.graph)):
            for j in range(len(self.graph)):
                if i == j:
                    break
                if self.is_array_inter(self.graph[i], self.graph[j]):
                    self.BFS_graph[i].append(j)
                    self.BFS_graph[j].append(i)
        self.paint()
        print(self.graph)

    def stop(self, event):  # окончание рисования линии, замыкание полигонов
        self.k = 0
        if len(self.cur_line.coords) > 0:
            self.cur_line.coords.pop(0)
            if (abs(self.cur_line()[0].x - self.cur_line()[-1].x) <= 5 and abs(
                    self.cur_line()[0].y - self.cur_line()[-1].y) <= 5):
                self.draw_circle()
            else:
                self.st_inter = [-1, -1]
                self.fin_inter = [-1, -1]
                for i in range(len(self.lines)):
                    for j in range(len(self.lines[i].coords)):
                        if (abs(self.cur_line()[0].x - self.lines[i]()[j].x) <= 5 and abs(
                                self.cur_line()[0].y - self.lines[i]()[j].y) <= 5):
                            self.st_inter = [i, j]
                        if (abs(self.cur_line()[-1].x - self.lines[i]()[j].x) <= 5 and abs(
                                self.cur_line()[-1].y - self.lines[i]()[j].y) <= 5):
                            self.fin_inter = [i, j]
                        if self.st_inter[0] != -1 and self.st_inter[0] == self.fin_inter[0]:
                            break
                if self.st_inter[0] == -1 or self.fin_inter[0] == -1 or self.st_inter[0] != self.fin_inter[0]:
                    canv.delete('recent')
                else:
                    sliced_coord_st = [-1, -1]
                    sliced_coord_fin = [-1, -1]
                    for i in range(len(self.sliced_lines)):
                        for j in range(len(self.sliced_lines[i]())):
                            if (abs(self.cur_line()[0].x - self.sliced_lines[i]()[j].x) <= 5 and abs(
                                    self.cur_line()[0].y - self.sliced_lines[i]()[j].y) <= 5):
                                sliced_coord_st = [i, j]
                            if (abs(self.cur_line()[-1].x - self.sliced_lines[i]()[j].x) <= 5 and abs(
                                    self.cur_line()[-1].y - self.sliced_lines[i]()[j].y) <= 5):
                                sliced_coord_fin = [i, j]
                    if sliced_coord_st[0] == sliced_coord_fin[0]:
                        self.sliced_lines.append(Polygon(self.sliced_lines[sliced_coord_st[0]]()[
                                                         :min(sliced_coord_st[1], sliced_coord_fin[1])]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]]()[
                                    min(sliced_coord_st[1], sliced_coord_fin[1]):max(sliced_coord_st[1],
                                                                                     sliced_coord_fin[1])]))
                        self.sliced_lines.append(Polygon(self.sliced_lines[sliced_coord_fin[0]]()[
                                                         max(sliced_coord_st[1], sliced_coord_fin[1]):]))
                        self.sliced_lines.pop(sliced_coord_st[0])
                    else:
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]]()[:sliced_coord_st[1]]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]]()[sliced_coord_st[1]:]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_fin[0]]()[:sliced_coord_fin[1]]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_fin[0]]()[sliced_coord_fin[1]:]))
                        if sliced_coord_st[0] > sliced_coord_fin[0]:
                            self.sliced_lines.pop(sliced_coord_st[0])
                            self.sliced_lines.pop(sliced_coord_fin[0])
                        else:
                            self.sliced_lines.pop(sliced_coord_fin[0])
                            self.sliced_lines.pop(sliced_coord_st[0])
                    self.sliced_lines.append(self.cur_line)
                    print(len(self.sliced_lines))
                    if self.st_inter[1] > self.fin_inter[1]:
                        self.draw_polygon()
                    else:
                        self.draw_reverse_polygon()
                    self.translate()

        print(self.cur_line.coords[0]())

    def restart(self):
        if 100 <= int(self.fw.get()) <= 1720:
            self.field_width = int(self.fw.get())
        if 100<= int(self.fh.get()) <= 930:
            self.field_height = int(self.fh.get())
        if 2 <= int(self.lw.get()) <= 20:
            self.line_width = int(self.lw.get())
        self.width_entry.delete(0, self.field_width)
        self.height_entry.delete(0, self.field_height)
        self.line_width_entry.delete(0, self.line_width)
        self.width_entry.insert(0, self.field_width)
        self.height_entry.insert(0, self.field_height)
        self.line_width_entry.insert(0, self.line_width)
        canv.place(x=ident_x, y=ident_y, width=self.field_width + 20, height=self.field_height + 20)
        restart_button.place(x=self.field_width + 20 + ident_x, y=ident_y, width=50, height=50)
        self.lines = []
        self.sliced_lines = []
        canv.delete("all")
        self.lines.append(self.create_bounds())
        self.sliced_lines.append(self.create_bounds())
        self.lines[0].fill("white", self.line_width)
        

    def change_bounds(self):
        self.num_bound = 1 - self.num_bound
        self.restart()
        if self.num_bound == 1:
            check_button['text'] =u'\u25EF'
            check_font = font.Font(size=25)
            check_button['font'] = check_font
        if self.num_bound == 0:
            check_button['text'] =u'\u25FB'
            check_font = font.Font(size=30)
            check_button['font'] = check_font


if __name__ == "__main__":
    app = App()
    line_width = app.line_width
    restart_font = font.Font(size=30)
    restart_button = Button(bg="red", text=u'\u2B6E', command=app.restart)
    restart_button['font'] = restart_font
    restart_button.place(x=field_width + 20 + ident_x, y=ident_y, width=50, height=50)
    button_color1 = Button(bg=colors[0], command=app.choose_colour1)
    button_color1.place(x=20, y=ident_y, width=50, height=50)
    button_color2 = Button(bg=colors[1], command=app.choose_colour2)
    button_color2.place(x=20, y=ident_y+55, width=50, height=50)
    button_color3 = Button(bg=colors[2], command=app.choose_colour3)
    button_color3.place(x=20, y=ident_y+110, width=50, height=50)
    button_color4 = Button(bg=colors[3], command=app.choose_colour4)
    button_color4.place(x=20, y=ident_y + 165, width=50, height=50)
    check_font = font.Font(size=30)
    check_button = Button(bg="grey", text = u'\u25FB', command = app.change_bounds)
    check_button['font'] = check_font
    check_button.place(x=20, y=600, width=50, height=50)
    root.mainloop()
