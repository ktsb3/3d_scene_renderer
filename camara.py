from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    def __init__(self):
        # posicion inicial de la camara
        self.camera_pos = Vector3([0.0, 4.0, 3.0])

        # establecer las direcciones de la camara, en que coordenadas se encuentra el frente, arriba y a la derecha
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        # sensibilidad del mouse para el movimiento de la camara
        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0

    # actualizacion de la vista para la camara actual
    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    # capturar y procesar el movimiento del mouse
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        # calculamos el movimiento de xoffset y yoffset multiplicado por el movimiento del mouse denotado por su sensitividad
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        # calculamos el movimiento horizontal y vertical de la camara
        self.jaw += xoffset
        self.pitch += yoffset

        # limitar la rotacion de la camara a solo 45° vertical y horizontalmente
        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    # movimiento de la camara
    def update_camera_vectors(self):
        # vector 3 local para almacenar el movimiento de la camara
        front = Vector3([0.0, 0.0, 0.0])

        # se calcula la nueva ubicacion de la camara haciendo uso de trigonometria
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        # actualizar la nueva ubicacion de la camara
        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    # movimiento WASD para la camara
    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity

        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity

        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
            
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity