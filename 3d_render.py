import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from camara import Camera

# inicializar la camara con sus dimensiones 
cam = Camera()
WIDTH, HEIGHT = 1280, 720 

# establecer las coordenadas de la camara en el centro
lastX, lastY = WIDTH / 2, HEIGHT / 2

# indicar al programa que es la primera inicializacion del movimiento del mouse
first_mouse = True

# bool para detectar si se esta presionando una tecla
left, right, forward, backward = False, False, False, False

# funcion para detectar entradas del teclado
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward

    # cerrar el programa si se presiona escape
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # entradas y accioens de movimiento
    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False

    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False

    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False

    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False


def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.05)

    if right:
        cam.process_keyboard("RIGHT", 0.05)

    if forward:
        cam.process_keyboard("FORWARD", 0.05)

    if backward:
        cam.process_keyboard("BACKWARD", 0.05)

# funcion para que GLFW pueda usar entradas del mouse
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    # establece las coordenadas del mouse en caso de que sea la primera vez que se interactua
    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    # se calculan las nuevas coordenadas
    xoffset = xpos - lastX
    yoffset = lastY - ypos # esta invertido porque las coordenadas de open gl y las coordenadas de la entrada del mosue son opuestas

    # se establecen las nuevas ultimas coordenadas de la camara
    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main(){
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;
out vec4 out_color;

uniform sampler2D s_texture;

void main(){
    out_color = texture(s_texture, v_texture);
}
"""


#funcion para ventana responsiva
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# inicializar glfw y crear la ventana
if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(WIDTH, HEIGHT, "cargar los objetos", None, None)

# verificar si se pudo crear la ventana
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# establecer la posicion del a ventana
glfw.set_window_pos(window, 400, 200)

# establecer la funcion para que la ventana sea responsiva
glfw.set_window_size_callback(window, window_resize_clb)

# establecer funcion para uso del mouse con glfw
glfw.set_cursor_pos_callback(window, mouse_look_clb)

# entrada de teclado
glfw.set_key_callback(window, key_input_clb)

# entrada del mouse
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

glfw.make_context_current(window)

# obtener el archivo obj
chibi_indices, chibi_buffer = ObjLoader.load_model("meshes/chibi.obj")
monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/monkey.obj")
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")
wall_indices, wall_buffer = ObjLoader.load_model("meshes/wall_1.obj")
wall2_indices, wall2_buffer = ObjLoader.load_model("meshes/wall_2.obj")
cube_indices, cube_buffer = ObjLoader.load_model("meshes/cube.obj")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# establecer el arreglo de vertices y el buffer 
VAO = glGenVertexArrays(6)
VBO = glGenBuffers(6)

# arreglo de vertices y buffer para modelo chibi
glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, chibi_buffer.nbytes, chibi_buffer, GL_STATIC_DRAW)

# chibi vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, chibi_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# arreglo de vertices y buffer para la cara de mono
glBindVertexArray(VAO[1])
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)

# cara de mono vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# arreglo de vertices y buffer para el suelo
glBindVertexArray(VAO[2])
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

# suelo vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# arreglo de vertices y buffer para el cubo
glBindVertexArray(VAO[3])
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

# cubo vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# arreglo de vertices y buffer para un muro
glBindVertexArray(VAO[4])
glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, wall_buffer.nbytes, wall_buffer, GL_STATIC_DRAW)

# muro vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, wall_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, wall_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, wall_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# arreglo de vertices y buffer para otro muro
glBindVertexArray(VAO[5])
glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
glBufferData(GL_ARRAY_BUFFER, wall2_buffer.nbytes, wall2_buffer, GL_STATIC_DRAW)

# muro vertices y texturas
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, wall2_buffer.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, wall2_buffer.itemsize * 8, ctypes.c_void_p(12))

glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, wall2_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# obtener la fuente de texturas de las imagenes
textures = glGenTextures(6)
load_texture("meshes/chibi.png", textures[0])
load_texture("meshes/monkey.jpg", textures[1])
load_texture("meshes/floor.jpg", textures[2])
load_texture("meshes/cube.jpg", textures[3])
load_texture("meshes/roof.png", textures[4])
load_texture("meshes/wall.png", textures[5])

# cargar shader
glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# establecer las ubicaciones de los objetos dentro de la vista
projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, -2, 0]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -6, -10]))
cube_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([4, -2, 0]))
roof_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 14, -10]))
wall1_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -6, 15]))
wall2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -6, -35]))
wall3_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([25, -6, -10]))

# punto de vista
#view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

# obtener las ubicaciones relativas de la vista
model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
#glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# aqui inicia el programa
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    # establecer buffer de profundidad y color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # camara actualizada por segundo
    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # rotacion de la figura chibi
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, chibi_pos)

    # renderizar el chibi
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(chibi_indices))

    # rotacion de la cara de mono
    rot_y = pyrr.Matrix44.from_x_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, monkey_pos)

    # renderizar la cara de mono
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))

    # modelo del suelo
    model = floor_pos

    # renderizar suelo
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # modelo del techo
    model = roof_pos

    # renderizar techo
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # modelo del muro 1
    model = wall1_pos

    # renderizar muro 1
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(wall_indices))

    # modelo del muro 2
    model = wall2_pos

    # renderizar muro 2
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(wall_indices))

    # modelo del muro 3
    model = wall3_pos

    # renderizar muro 3
    glBindVertexArray(VAO[5])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(wall2_indices))

    #modelo del cubo
    rot_y = pyrr.Matrix44.from_x_rotation(-0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, cube_pos)

    # renderizar cubo
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

    glfw.swap_buffers(window)

glfw.terminate()