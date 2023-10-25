import pygame
import serial
import time


class Controller:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.DELTA = 5
        self.angle_y = 500
        self.angle_x = 3000
        self.controller.init()
        self.ser = serial.Serial('COM5', baudrate=9600, timeout=0.01)
        time.sleep(1)

    def listen(self):
        while True:
            pygame.event.get()
            if self.controller.get_button(3):
                self.angle_y += self.DELTA if self.angle_y <= 1500 else 0
                self.ser.write((str(self.angle_y) + '\n').encode('utf-8'))
                print(self.angle_y)
            elif self.controller.get_button(0):
                self.angle_y -= self.DELTA if self.angle_y >= 500 else 0
                self.ser.write((str(self.angle_y) + '\n').encode('utf-8'))
                print(self.angle_y)
            elif self.controller.get_button(1):
                self.angle_x -= self.DELTA if self.angle_x >= 3000 else 0
                self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
                print(self.angle_x)
            elif self.controller.get_button(2):
                self.angle_x += self.DELTA if self.angle_x <= 5000 else 0
                self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
                print(self.angle_x)
            elif round(self.controller.get_axis(5), 2) != -1.0:
                axis_data = round(self.controller.get_axis(5), 2)
                new_value = int(self.map_data(axis_data, -1.0, 1.0, 7500, 7750))
                self.ser.write((str(new_value) + '\n').encode('utf-8'))
            elif round(self.controller.get_axis(4), 2) != -1.0:
                axis_data = round(self.controller.get_axis(4), 2)
                new_value = int(self.map_data(axis_data, -1.0, 1.0, 7500, 7280))
                self.ser.write((str(new_value) + '\n').encode('utf-8'))

    def close_port(self):
        self.ser.close()

    def map_data(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == "__main__":
    try:
        ps4 = Controller()
        ps4.listen()
    except KeyboardInterrupt:
        ps4.close_port()
