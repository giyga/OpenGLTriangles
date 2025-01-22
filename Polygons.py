import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import *

def mapValue(currentMin, currentMax, newMin, newMax, val):
    currentRange = currentMax - currentMin
    newRange = newMax - newMin
    return newMin + newRange * ((val - currentMin)/currentRange)

def z_rotation2D(n, rPointX, rPointY, angle):
    global points
    new_x = (points[TrianguloEscogido[n]][0] - rPointX) * math.cos(math.radians(angle)) - (points[TrianguloEscogido[n]][1] - rPointY) * math.sin(math.radians(angle)) + rPointX
    new_y = (points[TrianguloEscogido[n]][0] - rPointX) * math.sin(math.radians(angle)) + (points[TrianguloEscogido[n]][1] - rPointY) * math.cos(math.radians(angle)) + rPointY
    points[TrianguloEscogido[n]][0], points[TrianguloEscogido[n]][1], = new_x, new_y

def reescalar():
    if modoElegido == "reescalado" and len(TrianguloEscogido) == 3:
        global points
        p1, p2, p3 = points[TrianguloEscogido[0]], points[TrianguloEscogido[1]], points[TrianguloEscogido[2]]
        if keys[pygame.K_LEFT]: #Encojer
            #Definir los vectores
            if (p1[0] > 0 and p2[0] < 0) or (p2[0] > 0 and p1[0] < 0):
                v1x = abs(p1[0]) + abs(p2[0])     
            elif (p1[0] >= 0 and p2[0] >= 0) or (p1[0] <= 0 and p2[0] <= 0):
                v1x = max(p1[0], p2[0]) - min(p1[0],p2[0])
            if (p1[1] > 0 and p2[1] < 0) or (p2[1] > 0 and p1[1] < 0):
                v1y = abs(p1[1]) + abs(p2[1])
            elif (p1[1] >= 0 and p2[1] >= 0) or (p1[1] <= 0 and p2[1] <= 0):
                v1y = max(p1[1], p2[1]) - min(p1[1], p2[1])
            if (p1[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p1[0] < 0):
                v2x = abs(p1[0]) + abs(p3[0])
            elif (p1[0] >= 0 and p3[0] >= 0) or (p1[0] <= 0 and p3[0] <= 0):
                v2x = max(p1[0], p3[0]) - min(p1[0], p3[0])
            if (p1[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p1[1] < 0):
                v2y = abs(p1[1]) + abs(p3[1])
            elif (p1[1] >= 0 and p3[1] >= 0) or (p1[1] <= 0 and p3[1] <= 0):
                v2y = max(p1[1], p3[1]) - min(p1[1], p3[1])
            if (p2[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p2[0] < 0):
                v3x = abs(p2[0]) + abs(p3[0])
            elif (p2[0] >= 0 and p3[0] >= 0) or (p2[0] <= 0 and p3[0] <= 0):
                v3x = max(p2[0], p3[0]) - min(p2[0], p3[0])
            if (p2[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p2[1] < 0):
                v3y = abs(p2[1]) + abs(p3[1])
            elif (p2[1] >= 0 and p3[1] >= 0) or (p2[1] <= 0 and p3[1] <= 0):
                v3y = max(p2[1], p3[1]) - min(p2[1], p3[1])
       
            v1, v2, v3 = math.sqrt((v1x)**2 + (v1y)**2), math.sqrt((v2x)**2 + (v2y)**2), math.sqrt((v3x)**2 + (v3y)**2)
            if min(v1, v2, v3) > 1:
                a, b, c, d, e, f = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
                if v1 > v2 and v1 > v3:
                    if v2 > v3:     
                        p3[0] = c
                        p3[1] = d
                        p2[0] = e
                        p2[1] = f
                        r1 = v2 / v1
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 =  p2xt / v2, p2yt / v2 
                    else:
                        p1[0] = c
                        p1[1] = d       
                        p3[0] = a
                        p3[1] = b
                        p2[0] = e
                        p2[1] = f
                        r1 = v3 / v1
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 = p2xt / v3, p2yt / v3
                elif v2 > v1 and v2 > v3:
                    if v3 > v1:
                        p1[0] = e
                        p1[1] = f      
                        p3[0] = a
                        p3[1] = b
                        r1 = v3 / v2
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 = p2xt / v3, p2yt / v3
                    else:
                        r1 = v1 / v2
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 = p2xt / v1, p2yt / v1
                elif v3 > v2 and v3 > v1:
                    if v1 > v2:
                        p1[0] = c
                        p1[1] = d
                        p2[0] = a
                        p2[1] = b
                        r1 = v1 / v3
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 = p2xt / v1, p2yt / v1
                    else:
                        p1[0] = e
                        p1[1] = f      
                        p3[0] = c
                        p3[1] = d
                        p2[0] = a
                        p2[1] = b
                        r1 = v2 / v3
                        p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                        r2, r3 = p2xt / v2, p2yt / v2
                #Acortamiento del vertice mas largo
                p3xt = p3[0] - p1[0]
                r4 = p3xt / max(v1, v2, v3)
                p3yt = p3[1] - p1[1]
                r5 = p3yt / max(v1, v2, v3)
                p3xt, p3yt = (max(v1, v2, v3) - 1) * r4, (max(v1, v2, v3) - 1) * r5
                p3xt, p3yt = p3xt + p1[0], p3yt + p1[1]

                #Acortamiento del 2do vertice mas largo
                L = (max(v1, v2, v3) - 1) * r1
                p2xt, p2yt = L * r2, L * r3
                p2xt, p2yt = p2xt + p1[0], p2yt + p1[1]


                points[TrianguloEscogido[1]][0], points[TrianguloEscogido[1]][1], points[TrianguloEscogido[2]][0], points[TrianguloEscogido[2]][1] = p2xt, p2yt, p3xt, p3yt
            #return nuevosPuntos
        if keys[pygame.K_RIGHT]: #Agrandar
            #Definir los puntos
            if (p1[0] > 0 and p2[0] < 0) or (p2[0] > 0 and p1[0] < 0):
                v1x = abs(p1[0]) + abs(p2[0])     
            elif (p1[0] >= 0 and p2[0] >= 0) or (p1[0] <= 0 and p2[0] <= 0):
                v1x = max(p1[0], p2[0]) - min(p1[0],p2[0])
            if (p1[1] > 0 and p2[1] < 0) or (p2[1] > 0 and p1[1] < 0):
                v1y = abs(p1[1]) + abs(p2[1])
            elif (p1[1] >= 0 and p2[1] >= 0) or (p1[1] <= 0 and p2[1] <= 0):
                v1y = max(p1[1], p2[1]) - min(p1[1], p2[1])
            if (p1[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p1[0] < 0):
                v2x = abs(p1[0]) + abs(p3[0])
            elif (p1[0] >= 0 and p3[0] >= 0) or (p1[0] <= 0 and p3[0] <= 0):
                v2x = max(p1[0], p3[0]) - min(p1[0], p3[0])
            if (p1[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p1[1] < 0):
                v2y = abs(p1[1]) + abs(p3[1])
            elif (p1[1] >= 0 and p3[1] >= 0) or (p1[1] <= 0 and p3[1] <= 0):
                v2y = max(p1[1], p3[1]) - min(p1[1], p3[1])
            if (p2[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p2[0] < 0):
                v3x = abs(p2[0]) + abs(p3[0])
            elif (p2[0] >= 0 and p3[0] >= 0) or (p2[0] <= 0 and p3[0] <= 0):
                v3x = max(p2[0], p3[0]) - min(p2[0], p3[0])
            if (p2[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p2[1] < 0):
                v3y = abs(p2[1]) + abs(p3[1])
            elif (p2[1] >= 0 and p3[1] >= 0) or (p2[1] <= 0 and p3[1] <= 0):
                v3y = max(p2[1], p3[1]) - min(p2[1], p3[1])
       
            v1, v2, v3 = math.sqrt((v1x)**2 + (v1y)**2), math.sqrt((v2x)**2 + (v2y)**2), math.sqrt((v3x)**2 + (v3y)**2)

            a, b, c, d, e, f = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]
            if v1 > v2 and v1 > v3:
                if v2 > v3:     
                    p3[0] = c
                    p3[1] = d
                    p2[0] = e
                    p2[1] = f
                    r1 = v2 / v1
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 =  p2xt / v2, p2yt / v2 
                else:
                    p1[0] = c
                    p1[1] = d       
                    p3[0] = a
                    p3[1] = b
                    p2[0] = e
                    p2[1] = f
                    r1 = v3 / v1
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 = p2xt / v3, p2yt / v3
            elif v2 > v1 and v2 > v3:
                if v3 > v1:
                    p1[0] = e
                    p1[1] = f      
                    p3[0] = a
                    p3[1] = b
                    r1 = v3 / v2
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 = p2xt / v3, p2yt / v3
                else:
                    r1 = v1 / v2
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 = p2xt / v1, p2yt / v1
            elif v3 > v2 and v3 > v1:
                if v1 > v2:
                    p1[0] = c
                    p1[1] = d
                    p2[0] = a
                    p2[1] = b
                    r1 = v1 / v3
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 = p2xt / v1, p2yt / v1
                else:
                    p1[0] = e
                    p1[1] = f      
                    p3[0] = c
                    p3[1] = d
                    p2[0] = a
                    p2[1] = b
                    r1 = v2 / v3
                    p2xt, p2yt = p2[0] - p1[0], p2[1] - p1[1]
                    r2, r3 = p2xt / v2, p2yt / v2
            nuevosPuntos = []
                #Alargamiento del vertice mas largo
            p3xt = p3[0] - p1[0]
            r4 = p3xt / max(v1, v2, v3)
            p3yt = p3[1] - p1[1]
            r5 = p3yt / max(v1, v2, v3)
            p3xt, p3yt = (max(v1, v2, v3) + 1) * r4, (max(v1, v2, v3) + 1) * r5
            p3xt, p3yt = p3xt + p1[0], p3yt + p1[1]

                #Alargamiento del 2do vertice mas largo
            L = (max(v1, v2, v3) + 1) * r1
            p2xt, p2yt = L * r2, L * r3
            p2xt, p2yt = p2xt + p1[0], p2yt + p1[1]

            nuevosPuntos.append(p2xt)
            nuevosPuntos.append(p2yt)
            nuevosPuntos.append(p3xt)
            nuevosPuntos.append(p3yt)
            points[TrianguloEscogido[1]][0], points[TrianguloEscogido[1]][1], points[TrianguloEscogido[2]][0], points[TrianguloEscogido[2]][1] = p2xt, p2yt, p3xt, p3yt
            

def trasladar():
    if modoElegido == "traslación":
        global points
        if keys[pygame.K_RIGHT]:
            points[TrianguloEscogido[0]][0] += 1
            points[TrianguloEscogido[1]][0] += 1
            points[TrianguloEscogido[2]][0] += 1
        if keys[pygame.K_LEFT]:
            points[TrianguloEscogido[0]][0] -= 1
            points[TrianguloEscogido[1]][0] -= 1
            points[TrianguloEscogido[2]][0] -= 1
        if keys[pygame.K_UP]:
            points[TrianguloEscogido[0]][1] += 1
            points[TrianguloEscogido[1]][1] += 1
            points[TrianguloEscogido[2]][1] += 1
        if keys[pygame.K_DOWN]:
            points[TrianguloEscogido[0]][1] -= 1
            points[TrianguloEscogido[1]][1] -= 1
            points[TrianguloEscogido[2]][1] -= 1


def puntoRotacion(p1, p2, p3):
    puntoRotacion = []
    if (p1[0] > 0 and p2[0] < 0) or (p2[0] > 0 and p1[0] < 0):
        v1x = abs(p1[0]) + abs(p2[0])     
    elif (p1[0] >= 0 and p2[0] >= 0) or (p1[0] <= 0 and p2[0] <= 0):
        v1x = max(p1[0], p2[0]) - min(p1[0],p2[0])
    if (p1[1] > 0 and p2[1] < 0) or (p2[1] > 0 and p1[1] < 0):
        v1y = abs(p1[1]) + abs(p2[1])
    elif (p1[1] >= 0 and p2[1] >= 0) or (p1[1] <= 0 and p2[1] <= 0):
        v1y = max(p1[1], p2[1]) - min(p1[1], p2[1])
    if (p1[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p1[0] < 0):
        v2x = abs(p1[0]) + abs(p3[0])
    elif (p1[0] >= 0 and p3[0] >= 0) or (p1[0] <= 0 and p3[0] <= 0):
        v2x = max(p1[0], p3[0]) - min(p1[0], p3[0])
    if (p1[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p1[1] < 0):
        v2y = abs(p1[1]) + abs(p3[1])
    elif (p1[1] >= 0 and p3[1] >= 0) or (p1[1] <= 0 and p3[1] <= 0):
        v2y = max(p1[1], p3[1]) - min(p1[1], p3[1])
    if (p2[0] > 0 and p3[0] < 0) or (p3[0] > 0 and p2[0] < 0):
        v3x = abs(p2[0]) + abs(p3[0])
    elif (p2[0] >= 0 and p3[0] >= 0) or (p2[0] <= 0 and p3[0] <= 0):
        v3x = max(p2[0], p3[0]) - min(p2[0], p3[0])
    if (p2[1] > 0 and p3[1] < 0) or (p3[1] > 0 and p2[1] < 0):
        v3y = abs(p2[1]) + abs(p3[1])
    elif (p2[1] >= 0 and p3[1] >= 0) or (p2[1] <= 0 and p3[1] <= 0):
        v3y = max(p2[1], p3[1]) - min(p2[1], p3[1])
       
    v1, v2, v3 = math.sqrt((v1x)**2 + (v1y)**2), math.sqrt((v2x)**2 + (v2y)**2), math.sqrt((v3x)**2 + (v3y)**2) 
    
    if v1 > v2 and v1 > v3:
        if modoElegido == "rotación":
            puntoRotacion.append((p1[0]+p2[0]) / 2)
            puntoRotacion.append((p1[1]+p2[1]) / 2)
            return puntoRotacion
    elif v2 > v1 and v2 > v3:       
        if modoElegido == "rotación":
            puntoRotacion.append((p1[0]+p3[0]) / 2)
            puntoRotacion.append((p1[1]+p3[1]) / 2)
            return puntoRotacion
    elif v3 > v2 and v3 > v1:
        if modoElegido == "rotación":
            puntoRotacion.append((p2[0]+p3[0]) / 2)
            puntoRotacion.append((p2[1])+p3[1] / 2)
            return puntoRotacion


    #Hay que determinar en qué orden se va hacer todo esto

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = -400
ortho_bottom = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Polygons in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)



TrianguloEscogido = [] #Acá va guardar las coords del triángulo que vamos a transformar
def EyF(keys):
    if len(TrianguloEscogido) < 3:
        return
    else:
        if len(points) >= 3:
            if modoElegido == "rotación":
                pointX = puntoRotacion(points[TrianguloEscogido[0]],points[TrianguloEscogido[1]],points[TrianguloEscogido[2]])[0]
                pointY = puntoRotacion(points[TrianguloEscogido[0]],points[TrianguloEscogido[1]],points[TrianguloEscogido[2]])[1]
                if keys[pygame.K_LEFT]: #Esta notación es interesante
                    for p in range(3):
                        z_rotation2D(p, pointX, pointY, 3)
                if keys[pygame.K_RIGHT]:
                    for p in range(3):
                        z_rotation2D(p, pointX, pointY, -3)
        

def mostrarTexto(text):
    glutInit(sys.argv)
    glMatrixMode(GL_PROJECTION)
    #glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(-400, 400, -400, 400)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.0, 1.0, 0.0) # Green
    glRasterPos2i(300, 380)
    font = GLUT_BITMAP_9_BY_15
    for i in text:
        glutBitmapCharacter(font, ord(i))
    #glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def plot_polygon():
    glColor(0.2, 0.2, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    for p in range(len(points) - 1):
        glVertex2f(points[p][0], points[p][1])
    glEnd()
    for i in np.arange(0, len(points) - 2, 3):
        if i in TrianguloEscogido:
            glColor(0.8, 0.8, 0, 0.1)
            glBegin(GL_LINE_LOOP)
            glVertex2f(points[TrianguloEscogido[0]][0], points[TrianguloEscogido[0]][1])
            glVertex2f(points[TrianguloEscogido[1]][0], points[TrianguloEscogido[1]][1])
            glVertex2f(points[TrianguloEscogido[2]][0], points[TrianguloEscogido[2]][1])
            glEnd()
        else:
            glColor(0.5, 0.5, 0.5, 0.1)
            glBegin(GL_LINE_LOOP)
            glVertex2f(points[i][0], points[i][1])
            glVertex2f(points[i+1][0], points[i+1][1])
            glVertex2f(points[i+2][0], points[i+2][1])
            glEnd()


modo = ["rotación", "traslación", "reescalado"]
modoElegido = modo[0]

def elegirModo(modo):
    global modoElegido
    if keys[pygame.K_LSHIFT]:
        for p in range(len(modo)):
            if modoElegido == modo[p]:
                if p == len(modo) - 1:
                    modoElegido = modo[0]
                    break
                else:
                    modoElegido = modo[p+1]
                    break
            else:
                continue

def elegirTriang(points):
    if len(points) < 3:
        return None
    else:
        if keys[pygame.K_TAB]:
            global TrianguloEscogido
            if len(TrianguloEscogido) == 0:
                TrianguloEscogido = [0, 1, 2]
            elif (TrianguloEscogido[0] / 3) + 1 == math.floor(len(points) / 3):
                TrianguloEscogido = [0, 1, 2]
            else:
                TrianguloEscogido = [TrianguloEscogido[0]+3, TrianguloEscogido[1]+3, TrianguloEscogido[2]+3]



done = False
init_ortho()
points = np.array([[1500,1500]])
while not done:
    p = None
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            if points[0][0] == 1500:
                points[0][0] = mapValue(0, screen_width, ortho_left, ortho_right, p[0])
                points[0][1] = mapValue(0, screen_height, ortho_bottom, ortho_top, p[1])
            else:
                points = np.append(points, [mapValue(0, screen_width, ortho_left, ortho_right, p[0]), mapValue(0, screen_height, ortho_bottom, ortho_top, p[1])])
                points = points.reshape(int(len(points)/2),2)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    elegirModo(modo)
    EyF(keys)
    if len(points) >= 3:
        trasladar()
        reescalar()
    plot_polygon()
    elegirTriang(points)
    mostrarTexto(modoElegido)
    pygame.display.flip()
    pygame.time.wait(150)
pygame.quit()
