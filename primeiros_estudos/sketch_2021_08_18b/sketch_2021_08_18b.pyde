from __future__ import print_function, division, unicode_literals

"""
TO DO:
 [X] imagem no fundo  
     [ ] imagem cabe na tela?
         [ ] qual o tamanho da tela?
     [ ] se não cabe, qual o fator de escala?
     [ ] redimensionar a tela 
     [ ] pensar sistema de coordenadas tela / base-planta
 [X] adicionar pontos yay!
 [ ]  melhorar interface de remover pontos
 [ ] salvar e carregar planilha
 [X] Perguntar ao Yorik sobre ler DXF... 
 [ ] fazer menu de modos
 [ ] encapsular mais coisas na classe Grid

"""

from graph import Graph
from grid import Grid, dim_grid
from helpers import is_img_ext

thread_running = False
viz_stat = False
selected_v = None
mode = 0
modes = ('move', 'connect', 'disconnect', 'path', 'swap', 'add', 'remove')
found_path = []
NUM = 4 * 4

imagem = None

def setup():
    size(600, 600)
    print(displayWidth, displayHeight)
    textAlign(CENTER, CENTER)
    f = createFont("Source Code Pro Bold", 12)
    textFont(f)
    global margin, w, h, cols, rows
    graph = Graph.empty_graph(range(NUM))
    margin = width / 40
    cols, rows = dim_grid(len(graph))
    w, h = (width - margin * 2) / cols, (height - margin * 2) / rows
    setup_grid(cols, rows, graph)

def setup_grid(cols, rows, graph):
    global grid
    # create grid postions for graph vertices
    grid = Grid(graph, cols, rows)
    print("Cyclic: " + str(graph.is_cyclic()))
    global gx, gy



def draw():
    colorMode(RGB)
    background(128)
    if imagem:  # if imagem != None:   
        image(imagem, 0, 0)

    for ia, ja, ib, jb, da, db in grid.edge_coords():
        # za e zb são relaciodos ao "grau" numero de conexoes
        stroke(2)
        xa, ya = ij_to_xy(ia, ja)
        xb, yb = ij_to_xy(ib, jb)
        line(xa, ya, xb, yb)
        strokeWeight(1)
        colorMode(HSB)
        fill(da * 8, 255, 255)
        circle(xa, ya, da * 5)
        fill(db * 8, 255, 255)
        circle(xb, yb, db * 5)        
                             
    if selected_v:
        i, j = grid[selected_v]
        x, y = ij_to_xy(i, j)
        stroke(255)
        strokeWeight(5)
        line(x, y, mouseX, mouseY)


    for v in grid.keys():
        i, j = grid[v]  # (123, 12312)
        x, y = ij_to_xy(*grid[v])

        colorMode(RGB)
        stroke(255)
        if v == selected_v:
            fill(0)
        elif mouse_near(v):
            fill(255, 0, 0)
        elif v in found_path:
            fill(0, 255, 0)
        else:
            noFill()
        strokeWeight(1)
        circle(x, y, 10)
        if viz_stat:
            colorMode(RGB)
            fill(0)
            textSize(24)
            i, j = grid[v]  # (0.2312312312, 12,312123)
            # text("{:.2f}, {:.2f}".format(i, j), x, y)
            text("{}".format(v), x, y)

    fill(255)
    text(modes[mode], 40, 40)

def keyTyped():
    global gx, gy, viz_stat, grid, graph, mode
    if key  == ' ':
        mode = (mode + 1) % len(modes)
    elif key == 'r':
        grid.graph = Graph.random_graph(grid.graph.vertices())
    elif key == 'v':
        viz_stat = not viz_stat
        print(grid.graph)
    elif key == 'p':
        saveFrame("####.png")
    elif key == 'b':
        selectInput("Selecione um arquivo de imagem", "carregar_imagem")

def carregar_imagem(selection):
    global imagem
    if selection == None:
        print("Seleção cancelada.")
    else:
        path = selection.getAbsolutePath() 
        if is_img_ext(path):
            imagem = loadImage(path)
        else:
            alerta("Imagem não carregada", "Você não selecionou uma imagem!")

def mouse_near(v):
    x, y = ij_to_xy(*grid[v])
    return dist(x, y, mouseX, mouseY) < 20

def mousePressed():
    global selected_v
    for v in grid.keys():
        if mouse_near(v):
            selected_v = v
            return

def mouseDragged():
    if selected_v is not None and mode == 0: # move
        dx = mouseX - pmouseX
        dy = mouseY - pmouseY
        i, j = grid[selected_v]
        i += dx / float(w)
        j += dy / float(h)
        grid[selected_v] = [i, j]
        print(grid[selected_v])
        

def mouseReleased():
    global selected_v
    if selected_v is not None and mode == 1:  # connect
        for v in grid.keys():
            if mouse_near(v):
                grid.graph.add_edge((v, selected_v))
                
    if selected_v is not None and mode == 2:  # disconnect
        for v in grid.keys():
            if mouse_near(v):
                grid.graph.remove_edge((v, selected_v))

    if selected_v is not None and mode == 3:  # path
        for v in grid.keys():
            if mouse_near(v):
                path = grid.graph.find_shortest_path(v, selected_v)
                found_path[:] = path if path else []
                
                                                
    if selected_v is not None and mode == 4:  # swap
        for v in grid.keys():
            if mouse_near(v):
                grid[selected_v], grid[v] = grid[v], grid[selected_v]

    if  mode == 5:  # add
        for i in range(len(grid) + 1):
            if i not in grid:
                grid.add_vertex(i, xy_to_ij(mouseX, mouseY))
                break

    if  mode == 6:  # remove
        for v in grid.keys():
            if mouse_near(v):
                grid.remove_vertex(v)
    print(len(grid)) 
    selected_v = None
    
def ij_to_xy(i, j):
    return (
        margin + w / 2 + i * w,
        margin + h / 2 + j * h
        )

def xy_to_ij(x, y):
    return ((x - margin - w / 2) / float(w),
            (y - margin - h / 2) / float(h))
    
def alerta(title, message):
    from javax.swing import JOptionPane
    return JOptionPane.showMessageDialog(None,
                                         message,
                                         title,
                                         JOptionPane.WARNING_MESSAGE,
                                         )    
    
