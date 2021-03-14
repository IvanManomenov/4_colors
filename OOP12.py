from tkinter import *
# from tkinter import colorchooser
from tkinter.colorchooser import askcolor

colors = ['blue', 'red', 'green', 'yellow']
root = Tk()
field_height = 600
field_width = 1000
ident_x = 100  # отступ поля от левого края канвы
ident_y = 30  # отступ поля от верхнего края канвы
root.geometry('1200x720')
canv = Canvas(root, bg='white')
k = 0
line_width = 10  # толщина рисуемой линии
radius_inter = 10
crossing = []  # массив для пересечений(пока не используется)
lines_in_polygon = []
canv.place(x=ident_x, y=ident_y, width=field_width + 20, height=field_height + 20)


# count_lines = 0
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_in_polygon(self, other):
        count_crossing = 0
        for i in other.coords:
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

    def fill(self, colour):
        canv.create_polygon(self.simpcoords, fill=colour, outline='black', width=line_width)

    def app(self, dot):
        self.xcoords.append(dot.x)
        self.ycoords.append(dot.y)
        self.coords.append(dot)
        self.simpcoords.append([dot.x, dot.y])


class App(object):
    def __init__(self):
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
        # print(lines[0])
        self.lines.append(self.create_bounds())
        self.sliced_lines.append(self.create_bounds())
        self.lines[0].fill("white")
        canv.bind('<Button-1>', self.start)
        canv.bind('<B1-Motion>', self.draw)
        canv.bind('<ButtonRelease-1>', self.stop)

    def start(self, event):
        self.x0 = event.x
        self.y0 = event.y
        # if len(a.find_overlapping(x0-2, y0-2, x0+2, y0+2)) > 0:
        self.cur_line = Polygon([])

    def interpolation(self, cur_line_sliced):
        cur_line_inter = Polygon([])
        for i in range(len(cur_line_sliced.coords) - 1):
            cur_line_inter.app(cur_line_sliced.coords[i])
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
        if 10 <= self.x <= field_width + 10 and 10 <= self.y <= field_height + 10:
            self.cur_line.app(Point(self.x, self.y))
            print(len(self.cur_line.coords))
            #            if len(self.cur_line.coords) > 0:
            canv.create_line(self.x0, self.y0, self.x, self.y, width=line_width, tag='recent')
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

    def create_bounds(self):  # создание границ поля
        field_line = Polygon([])
        for i in range(field_width):
            field_line.app(Point(10 + i, 10))
        for i in range(field_height):
            field_line.app(Point(10 + field_width, 10 + i))
        for i in range(field_width):
            field_line.app(Point(10 + field_width - i, 10 + field_height))
        for i in range(field_height):
            field_line.app(Point(10, 10 + field_height - i))
        return field_line

    def draw_circle(self):  # рисование замкнутого на себя полигона
        self.k += 1
        if self.k == 4:
            self.k = 0
        self.cur_line.fill(colors[self.k])
        self.lines.append(self.cur_line)
        cur_line = Polygon([])

    def draw_polygon(
            self):  # рисование полигона, если стартовая точка пересечения с другим полигоном в его массиве находится раньше финальной
        new_polyg1 = Polygon([])
        for i in self.lines[self.st_inter[0]].coords[self.fin_inter[1]:self.st_inter[1] + 1]:
            new_polyg1.app(i)

        for i in range(len(self.cur_line.coords)):
            new_polyg1.app(self.cur_line.coords[i])
        new_polyg2 = Polygon([])

        for i in self.lines[self.st_inter[0]].coords[self.st_inter[1]: len(self.lines[self.st_inter[0]].coords)]:
            new_polyg2.app(i)
        for i in self.lines[self.st_inter[0]].coords[0:self.fin_inter[1] + 1]:
            new_polyg2.app(i)
        for i in range(len(self.cur_line.coords)):
            new_polyg2.app(self.cur_line.coords[len(self.cur_line.coords) - i - 1])
        self.lines.append(new_polyg1)
        self.lines.append(new_polyg2)
        self.lines.pop(self.st_inter[0])

    def draw_reverse_polygon(
            self):  # рисование полигона, если финальная точка пересечения с другим полигоном в его массиве находится раньше стартовой
        new_polyg1 = Polygon([])
        for i in self.lines[self.st_inter[0]].coords[self.st_inter[1]:self.fin_inter[1] + 1]:
            new_polyg1.app(i)
        for i in range(len(self.cur_line.coords)):
            new_polyg1.app(self.cur_line.coords[len(self.cur_line.coords) - i - 1])
        new_polyg2 = Polygon([])
        for i in self.lines[self.st_inter[0]].coords[self.fin_inter[1]: len(self.lines[self.st_inter[0]].coords)]:
            new_polyg2.app(i)
        for i in self.lines[self.st_inter[0]].coords[0:self.st_inter[1] + 1]:
            new_polyg2.app(i)
        for i in range(len(self.cur_line.coords)):
            new_polyg2.app(self.cur_line.coords[i])
        self.lines.pop(self.st_inter[0])
        self.lines.append(new_polyg1)
        self.lines.append(new_polyg2)

    def is_array_inter(self, array1, array2):
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
        for i in range(len(self.BFS_graph)):
            self.lines[i].fill(colors[self.colored_graph[i]])

    def translate(self):
        self.graph = []
        for i in range(len(self.lines)):
            self.graph.append([])
            for j in range(len(self.sliced_lines)):
                # print(self.sliced_lines[j].coords)
                if self.sliced_lines[j].coords[len(self.sliced_lines[j].coords) // 2] in self.lines[i].coords:
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

        print(self.BFS_graph)

    def stop(self, event):  # окончание рисования линии, замыкание полигонов
        self.k = 0
        if len(self.cur_line.coords) > 0:
            self.cur_line.coords.pop(0)
            if (abs(self.cur_line.coords[0].x - self.cur_line.coords[-1].x) <= 30 and abs(
                    self.cur_line.coords[0].y - self.cur_line.coords[-1].y) <= 30):
                self.draw_circle()
            else:
                self.st_inter = [-1, -1]
                self.fin_inter = [-1, -1]
                for i in range(len(self.lines)):
                    for j in range(len(self.lines[i].coords)):
                        if (abs(self.cur_line.coords[0].x - self.lines[i].coords[j].x) <= 30 and abs(
                                self.cur_line.coords[0].y - self.lines[i].coords[j].y) <= 30):
                            self.st_inter = [i, j]
                        if (abs(self.cur_line.coords[-1].x - self.lines[i].coords[j].x) <= 30 and abs(
                                self.cur_line.coords[-1].y - self.lines[i].coords[j].y) <= 30):
                            self.fin_inter = [i, j]
                        if self.st_inter[0] != -1 and self.st_inter[0] == self.fin_inter[0]:
                            break
                if self.st_inter[0] == -1 or self.fin_inter[0] == -1 or self.st_inter[0] != self.fin_inter[0]:
                    canv.delete('recent')
                else:
                    sliced_coord_st = [-1, -1]
                    sliced_coord_fin = [-1, -1]
                    for i in range(len(self.sliced_lines)):
                        for j in range(len(self.sliced_lines[i].coords)):
                            if (abs(self.cur_line.coords[0].x - self.sliced_lines[i].coords[j].x) <= 10 and abs(
                                    self.cur_line.coords[0].y - self.sliced_lines[i].coords[j].y) <= 10):
                                sliced_coord_st = [i, j]
                            if (abs(self.cur_line.coords[-1].x - self.sliced_lines[i].coords[j].x) <= 10 and abs(
                                    self.cur_line.coords[-1].y - self.sliced_lines[i].coords[j].y) <= 10):
                                sliced_coord_fin = [i, j]
                    self.sliced_lines.append(self.cur_line)
                    if sliced_coord_st[0] == sliced_coord_fin[0]:
                        self.sliced_lines.append(Polygon(self.sliced_lines[sliced_coord_st[0]].coords[
                                                         :min(sliced_coord_st[1], sliced_coord_fin[1])]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]].coords[
                                    min(sliced_coord_st[1], sliced_coord_fin[1]):max(sliced_coord_st[1],
                                                                                     sliced_coord_fin[1])]))
                        self.sliced_lines.append(Polygon(self.sliced_lines[sliced_coord_fin[0]].coords[
                                                         max(sliced_coord_st[1], sliced_coord_fin[1]):]))
                        self.sliced_lines.pop(sliced_coord_st[0])
                    else:
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]].coords[:sliced_coord_st[1]]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_st[0]].coords[sliced_coord_st[1]:]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_fin[0]].coords[:sliced_coord_fin[1]]))
                        self.sliced_lines.append(
                            Polygon(self.sliced_lines[sliced_coord_fin[0]].coords[sliced_coord_fin[1]:]))
                        if sliced_coord_st[0] > sliced_coord_fin[0]:
                            self.sliced_lines.pop(sliced_coord_st[0])
                            self.sliced_lines.pop(sliced_coord_fin[0])
                        else:
                            self.sliced_lines.pop(sliced_coord_fin[0])
                            self.sliced_lines.pop(sliced_coord_st[0])
                    print(len(self.sliced_lines))
                    if self.st_inter[1] > self.fin_inter[1]:
                        self.draw_polygon()
                    else:
                        self.draw_reverse_polygon()
                self.translate()

        print('')


if __name__ == "__main__":
    app = App()
    escape_button = Button(bg="grey", text="cancel")
    escape_button.place(x=field_width + 20 + ident_x, y=field_height + ident_y - 35, width=50, height=50)
    button_color1 = Button(bg=colors[0], command=app.choose_colour1)
    button_color1.place(x=20, y=20, width=50, height=50)
    button_color2 = Button(bg=colors[1], command=app.choose_colour2)
    button_color2.place(x=20, y=75, width=50, height=50)
    button_color3 = Button(bg=colors[2], command=app.choose_colour3)
    button_color3.place(x=20, y=130, width=50, height=50)
    button_color4 = Button(bg=colors[3], command=app.choose_colour4)
    button_color4.place(x=20, y=185, width=50, height=50)
    check_button = Button(bg="grey")
    check_button.place(x=20, y=600, width=50, height=50)
    canv.bind('<Button-3>', app.check_point)
    root.mainloop()
