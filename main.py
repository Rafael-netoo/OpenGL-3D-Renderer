import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

# Variáveis globais
camera_pos = [0, -500, 500]  # Ponto C
camera_n = [0, 1, -1]        # Vetor N
camera_v = [0, -1, -1]       # Vetor V
fovy, aspect, near, far = 45, 1.33, 5, 10000  # Parâmetros de projeção
light_pos = [0, 500, 200]    # Ponto Pl
light_ambient = [0.4, 0.4, 0.4, 1.0]  # Cor ambiental da luz
light_diffuse = [0.5, 0.85, 1.0, 1.0]  # Cor difusa da luz
light_specular = [0.5, 0.85, 1.0, 1.0]  # Cor especular da luz
material_ambient = [0.2, 0.2, 0.2, 1.0]  # Cor ambiental do material
material_diffuse = [0.7, 0.5, 0.8, 1.0]  # Cor difusa do material
material_specular = [0.5, 0.5, 0.5, 1.0]  # Cor especular do material
material_emissive = [0.0, 0.0, 0.0, 1.0]  # Cor emissiva do material
shininess = 100  # Escalar η
byu_file = "objects/calice2.byu"  # Substitua pelo caminho do seu arquivo .byu
vertices = []
triangles = []

# Função para carregar o modelo BYU
def load_byu(filename):
    global vertices, triangles
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        
        # Lê o número de vértices e triângulos
        num_vertices, num_triangles = map(int, lines[0].split())
        
        # Lê os vértices
        vertices = [tuple(map(float, lines[i + 1].split())) for i in range(num_vertices)]
        
        # Lê os triângulos
        triangles = [list(map(int, lines[num_vertices + 1 + i].split())) for i in range(num_triangles)]

        print(f"Modelo carregado: {len(vertices)} vértices, {len(triangles)} triângulos")
        print("Vértices:", vertices)
        print("Triângulos:", triangles)
    except Exception as e:
        print(f"Erro ao carregar o arquivo BYU: {e}")

# Configuração inicial do OpenGL
def init_gl():
    glEnable(GL_DEPTH_TEST)  # Habilita o z-buffer
    glEnable(GL_LIGHTING)    # Habilita a iluminação
    glEnable(GL_LIGHT0)      # Habilita a luz 0
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)  # Habilita o shading de Gouraud
    glDisable(GL_CULL_FACE)  # Desabilita o culling de faces

# Configuração da iluminação
def set_lighting():
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

# Configuração do material
def set_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_EMISSION, material_emissive)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

# Renderização do modelo
def draw_model():
    glScale(0.1, 0.1, 0.1)  # Ajuste a escala conforme necessário
    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        for index in triangle:
            glVertex3fv(vertices[index - 1])  # Índices baseados em 1 no arquivo BYU
    glEnd()

# Renderização da cena
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configura a câmera
    gluPerspective(fovy, aspect, near, far)
    gluLookAt(
        camera_pos[0], camera_pos[1], camera_pos[2],  # Posição da câmera
        camera_pos[0] + camera_n[0], camera_pos[1] + camera_n[1], camera_pos[2] + camera_n[2],  # Ponto de foco
        camera_v[0], camera_v[1], camera_v[2]  # Vetor "up"
    )

    set_lighting()
    set_material()
    draw_model()
    
    pygame.display.flip()

# Movimentação da câmera
def handle_keys():
    global camera_pos, camera_n, camera_v
    keys = pygame.key.get_pressed()
    step = 10  # Passo de movimentação
    if keys[K_w]:  # Move para frente
        camera_pos[0] += step * camera_n[0]
        camera_pos[1] += step * camera_n[1]
        camera_pos[2] += step * camera_n[2]
    if keys[K_s]:  # Move para trás
        camera_pos[0] -= step * camera_n[0]
        camera_pos[1] -= step * camera_n[1]
        camera_pos[2] -= step * camera_n[2]
    if keys[K_a]:  # Move para a esquerda
        right = np.cross(camera_n, camera_v)
        right = right / np.linalg.norm(right)
        camera_pos[0] -= step * right[0]
        camera_pos[1] -= step * right[1]
        camera_pos[2] -= step * right[2]
    if keys[K_d]:  # Move para a direita
        right = np.cross(camera_n, camera_v)
        right = right / np.linalg.norm(right)
        camera_pos[0] += step * right[0]
        camera_pos[1] += step * right[1]
        camera_pos[2] += step * right[2]
    if keys[K_q]:  # Move para cima
        camera_pos[1] += step
    if keys[K_e]:  # Move para baixo
        camera_pos[1] -= step

# Rotação da câmera com o mouse
def handle_mouse_motion(x, y):
    global camera_n, camera_v
    sensitivity = 0.005  # Sensibilidade da rotação
    dx = x - display[0] // 2
    dy = y - display[1] // 2

    # Rotação horizontal (em torno do eixo Y)
    angle_y = -dx * sensitivity
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    camera_n = np.dot(rotation_y, camera_n)
    camera_v = np.dot(rotation_y, camera_v)

    # Rotação vertical (em torno do eixo X)
    angle_x = -dy * sensitivity
    right = np.cross(camera_n, camera_v)
    right = right / np.linalg.norm(right)
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    camera_n = np.dot(rotation_x, camera_n)
    camera_v = np.dot(rotation_x, camera_v)

    # Centraliza o cursor novamente
    pygame.mouse.set_pos(display[0] // 2, display[1] // 2)

# Loop principal
def main():
    global display
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
    aspect = display[0] / display[1]
    load_byu(byu_file)
    init_gl()

    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos(display[0] // 2, display[1] // 2)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEMOTION:
                handle_mouse_motion(event.pos[0], event.pos[1])
        
        handle_keys()
        draw_scene()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()