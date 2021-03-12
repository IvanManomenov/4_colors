colours = input().split()
graf = []#двумерный массив, в котором для каждой вершины задаются вершины, с которыми он связан
cgraf = []#массив с покрашенным графом
while(True):
    pp = input().split()#на вход подаются ребра n-ной вершины
    p = []
    for i in pp:
        if(not(int(i) in p) and int(i) != len(graf)):
            p.append(int(i))
    graf.append(p)
    for i in range(len(graf)):
            if(i in p):
                graf[i].append(len(graf) - 1)#если у новой вершины есть ребро с i-й вершиной, в массив i-й вершины нужно добавить новую, т.к. граф у нас неориентированный
    print(graf)
    cgraf = []
    ccode = [4 for i in range(len(graf))]#массив с закодированно покрашенным графом
    ccode[0] = 0
    #BFS_begin
    c = []
    c.append(0)
    while len(c) != 0:
        for i in graf[c[0]]:
            if(ccode[i] == 4):
                for j in range(4):
                    g = True
                    for k in graf[i]:
                        if ccode[k] == j:
                            g = False
                            break
                    if(g == True):
                        ccode[i] = j
                        break
                c.append(i)
        c.pop(0)
    if(4 in ccode):
        print('ты такую хрень не нарисуешь')
        break
    for i in ccode:
        cgraf.append(colours[i])
    print(cgraf)
    
                    
                        
