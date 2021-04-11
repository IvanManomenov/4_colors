from tkinter import *
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
graph_canv = Canvas(root, bg='white')

k = 0
line_width = 5  # толщина рисуемой линии
radius_inter = 10
lines_in_polygon = []


# count_lines = 0
class Point(object):
    """
    Класс точки в полигоне
    Параметры: координаты x,y
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        return [self.x, self.y]

    def is_in_polygon(self, other):
        """
        Функция, определяющая, лежит ли данная точка внутри данного полигона
        :param other: полигон
        :return: True-точка лежит внутри полигона
                 False-точка лежит вне полигона
        """
        count_crossing = 0
        for i in other():
            if self.x == i.x and self.y > i.y:
                count_crossing += 1
        if count_crossing % 2 == 1:
            return True
        else:
            return False


class Polygon(object):
    """
    Класс полигона
    Параметры:coords-массив, содержащий точки, задающие полигон
              simpcoords-массив, содержащий координаты точек, лежащих в полигоне
    """

    def __init__(self, coord):
        self.coords = []
        self.simpcoords = []
        for i in coord:
            self.coords.append(i)
            self.simpcoords.append([i.x, i.y])

    def __call__(self):
        return self.coords

    def fill(self, colour, lw):
        """
        Функция, красящая полигон в заданный цвет
        :param colour: цвет полигона
        :param lw: толщина линии границы полигона(lw - line width)
        """
        canv.create_polygon(self.simpcoords, fill=colour, outline='black', width=lw)

    def app(self, dot):
        """
        Функция, добавляющая новую точку в полигон
        :param dot: добавляемая точка
        """
        self.coords.append(dot)
        self.simpcoords.append([dot.x, dot.y])


class App(object):
    """
    Класс приложения
    """

    def __init__(self):
        self.line_width = line_width
        self.x0 = -1
        self.y0 = -1
        self.x = -1
        self.y = -1
        self.cur_line = Polygon([])
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
        graph_canv.place(x=2 * ident_x + field_width + 20, y=ident_y, width=400, height=400)
        self.fw = StringVar()
        self.fh = StringVar()
        self.lw = StringVar()
        width_label = Label(text="Width of field: ")
        height_label = Label(text="Height of field: ")
        line_width_label = Label(text="Width of line: ")
        width2_label = Label(text="(from 100 to 1250)")
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
        self.line_width_entry.place(x=190, y=50)
        self.width_entry.insert(0, self.field_width)
        self.height_entry.insert(0, self.field_height)
        self.line_width_entry.insert(0, self.line_width)

    def start(self, event):
        self.x0 = event.x
        self.y0 = event.y
        # if len(a.find_overlapping(x0-2, y0-2, x0+2, y0+2)) > 0:
        self.cur_line = Polygon([])

    def sign(self, num):
        """
        функция, определяющая знак числа
        :param num: число
        :return: 1-число положительное
                 0-число 0
                 -1-число отрицательное
        """
        if num > 0:
            return 1
        if num == 0:
            return 0
        return -1

    def interpolation(self, cur_line_sliced):
        """
        Функция интерполяции линии, которую проводит пользователь
        :param cur_line_sliced: исходная линия
        :return: cur_line_inter: проинтерполированная линия
        """
        cur_line_inter = Polygon([])
        for i in range(len(cur_line_sliced) - 1):
            cur_line_inter.app(cur_line_sliced[i])
            # print(cur_line_sliced[i](), cur_line_sliced[i+1]())
            if cur_line_sliced[i].y == cur_line_sliced[i + 1].y:
                for j in range(abs(cur_line_sliced[i].x - cur_line_sliced[i + 1].x)):
                    cur_line_inter.app(
                        Point(min(cur_line_sliced[i].x, cur_line_sliced[i + 1].x) + j, cur_line_sliced[i].y))
                    # print(cur_line_inter.simpcoords[-1])
            else:
                tg = abs((cur_line_sliced[i].x - cur_line_sliced[i + 1].x) / (
                        cur_line_sliced[i].y - cur_line_sliced[i + 1].y))
                # print(tg)
                for j in range(1, abs(cur_line_sliced[i].y - cur_line_sliced[i + 1].y)):
                    cur_line_inter.app(Point(
                        int(cur_line_sliced[i].x - j * tg * self.sign(cur_line_sliced[i].x - cur_line_sliced[i + 1].x)),
                        cur_line_sliced[i].y - j * self.sign(cur_line_sliced[i].y - cur_line_sliced[i + 1].y)))
                    # print(cur_line_inter.simpcoords[-1])
        return cur_line_inter

    def draw(self, event):
        """
        функция, изображающая отрезок кривой при его проведении(срабатывает при движении мышкой с зажатой левой кнопкой)
        :param event: местоположение курсора
        """
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
        """
        Функция для изменения цвета закрашиваемых полигонов
        """
        colors[0] = askcolor()[1]
        button_color1['bg'] = colors[0]
        self.translate()

    def choose_colour2(self):
        """
        Функция для изменения цвета закрашиваемых полигонов
        """
        colors[1] = askcolor()[1]
        button_color2['bg'] = colors[1]
        self.translate()

    def choose_colour3(self):
        """
        Функция для изменения цвета закрашиваемых полигонов
        """
        colors[2] = askcolor()[1]
        button_color3['bg'] = colors[2]
        self.translate()

    def choose_colour4(self):
        """
        Функция для изменения цвета закрашиваемых полигонов
        """
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
        """
        Функция, создающая полигон, задающий границы канвы
        :return: field_line - полигон, задающий границы канвы
        """
        if self.num_bound == 0:  # создание элипсоидной границы
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
        if self.num_bound == 1:  # создание прямоугольной границы
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

    def draw_polygon(self):
        """
        рисование полигона, если стартовая точка пересечения с другим полигоном в его массиве находится раньше финальной
        """
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

    def draw_reverse_polygon(self):
        """
        рисование полигона, если финальная точка пересечения с другим полигоном в его массиве находится раньше стартовой
        """
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

    def is_array_inter(self, array1, array2):
        """
        Функция, определяющая, являются ли данные полигоны смежными(т.е. имеющими общую границу)
        :param array1:
        :param array2:
        :return:
        """
        for i in array1:
            if i in array2:
                return True
        return False

    def paint(self):
        """
        Функция, красящая граф
        """
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
        if not (4 in self.colored_graph):
            for i in range(len(self.lines)):
                self.lines[i].fill(colors[self.colored_graph[i]], self.line_width)
                self.count_recursion = 0
        if 4 in self.colored_graph:
            self.count_recursion += 1
            self.sliced_lines.append(self.sliced_lines[self.count_recursion // len(self.sliced_lines)])
            self.sliced_lines.pop(self.count_recursion // len(self.sliced_lines))
            #self.lines = self.lines[::-1].copy()
            self.translate()

    def draw_graph(self):
        graph_coords = []
        graph_canv.delete("all")
        for i in range(1, len(self.graph) + 1):
            x = 200 + 180 * cos(pi / len(self.graph) * (2 * i + 1))
            y = 200 + 180 * sin(pi / len(self.graph) * (2 * i + 1))
            graph_coords.append([x,y])

        for i in range(len(self.BFS_graph)):
            for j in self.BFS_graph[i]:
                graph_canv.create_line(graph_coords[i][0]+10,graph_coords[i][1]+10,graph_coords[j][0]+10,graph_coords[j][1]+5)
        for i in range(len(self.BFS_graph)):
            graph_canv.create_oval(graph_coords[i][0], graph_coords[i][1], graph_coords[i][0] + 20, graph_coords[i][1] + 20, fill=colors[self.colored_graph[i]])

    def translate(self):
        """
        Функция, переводящее изображение(планарный граф) в обычный граф
        """
        self.graph = []
        self.lines = self.lines[::-1].copy()
        for i in range(len(self.lines)):
            self.graph.append([])
            for j in range(len(self.sliced_lines)):
                if len(self.sliced_lines[j]()) == 0:
                    pass
                elif self.sliced_lines[j]()[len(self.sliced_lines[j]()) // 2] in self.lines[i].coords:
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
        self.draw_graph()

    def stop(self, event):  # окончание рисования линии, замыкание полигонов
        """
        Функция, замыкающая полигоны с учетом новой проведенной линии
        """
        if len(self.cur_line()) > 0:
            self.cur_line.coords.pop(0)
            # print(self.cur_line.simpcoords)
            self.cur_line = Polygon(self.interpolation(self.cur_line()).coords)
            print(self.cur_line.simpcoords)
            # self.cur_line.fill('orange', 15)
            self.st_inter = [-1, -1]
            self.fin_inter = [-1, -1]
            for i in range(len(self.lines)):
                for j in range(len(self.lines[i].coords)):
                    if (abs(self.cur_line()[0].x - self.lines[i]()[j].x) <= 5 and abs(
                            self.cur_line()[0].y - self.lines[i]()[j].y) <= 5) and self.cur_line()[1].is_in_polygon(self.lines[i]):
                        self.st_inter = [i, j]
                    if (abs(self.cur_line()[-1].x - self.lines[i]()[j].x) <= 5 and abs(
                            self.cur_line()[-1].y - self.lines[i]()[j].y) <= 5) and self.cur_line()[1].is_in_polygon(self.lines[i]):
                        self.fin_inter = [i, j]
                if self.st_inter[0] != -1 and self.st_inter[0] == self.fin_inter[0] and self.cur_line()[1].is_in_polygon(self.lines[self.st_inter[0]]):
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
        """
        Функция, перезапускающая программу(очистка холста, перерисовка границ с учетом новых данных)
        :return:
        """
        if 100 <= int(self.fw.get()) <= 1250:
            self.field_width = int(self.fw.get())
        if 100 <= int(self.fh.get()) <= 930:
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
        graph_canv.place(x=2 * ident_x + self.field_width + 20, y=ident_y, width=400, height=400)
        restart_button.place(x=self.field_width + 20 + ident_x, y=ident_y, width=50, height=50)
        self.lines = []
        self.sliced_lines = []
        canv.delete("all")
        graph_canv.delete("all")
        self.lines.append(self.create_bounds())
        self.sliced_lines.append(self.create_bounds())
        self.lines[0].fill("white", self.line_width)

    def change_bounds(self):
        self.num_bound = 1 - self.num_bound
        self.restart()
        if self.num_bound == 1:
            check_button['text'] = u'\u25EF'
            check_font = font.Font(size=25)
            check_button['font'] = check_font
        if self.num_bound == 0:
            check_button['text'] = u'\u25FB'
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
    button_color2.place(x=20, y=ident_y + 55, width=50, height=50)
    button_color3 = Button(bg=colors[2], command=app.choose_colour3)
    button_color3.place(x=20, y=ident_y + 110, width=50, height=50)
    button_color4 = Button(bg=colors[3], command=app.choose_colour4)
    button_color4.place(x=20, y=ident_y + 165, width=50, height=50)
    check_font = font.Font(size=30)
    check_button = Button(bg="grey", text=u'\u25FB', command=app.change_bounds)
    check_button['font'] = check_font
    check_button.place(x=20, y=290, width=50, height=50)
    root.mainloop()
