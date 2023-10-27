import pygame
import serial
import time
import sys


class GUI:
    def __init__(self):
        # screen
        pygame.init()
        self.screen = pygame.display.set_mode((350, 250))
        self.DELTA = 3
        self.wide_value = 7500
        self.angle_y = 3880
        self.angle_x = 1750
        self.ser = serial.Serial('COM6', baudrate=9600, timeout=0.01)
        time.sleep(1)

        # creating buttons
        button_up_surface = pygame.transform.scale(pygame.image.load("up.jpg"), (50, 50))
        ''' button_down_surface = pygame.transform.scale(pygame.image.load("down.jpg"), (50, 50))'''
        button_right_surface = pygame.transform.scale(pygame.image.load("right.png"), (50, 50))
        button_left_surface = pygame.transform.scale(pygame.image.load("left.jpg"), (50, 50))
        button_wide_surface = pygame.transform.scale(pygame.image.load("wide.jpg"), (100, 50))
        button_narrow_surface = pygame.transform.scale(pygame.image.load("narrow.png"), (100, 50))
        self.button_up = Button(button_up_surface, 175, 50)
        '''button_down = Button(button_down_surface, 450, 350)'''
        self.button_right = Button(button_right_surface, 250, 100)
        self.button_left = Button(button_left_surface, 100, 100)
        self.button_wide = Button(button_wide_surface, 175, 125)
        self.button_narrow = Button(button_narrow_surface, 175, 180)

    def listen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    '''down = button_down.checking_input(pygame.mouse.get_pos())'''
                    if self.button_up.checking_input(pygame.mouse.get_pos()):
                        self.angle_y += self.DELTA if self.angle_y <= 4110 else 0
                        self.ser.write((str(self.angle_y) + '\n').encode('utf-8'))
                        print('up')
                    elif self.button_right.checking_input(pygame.mouse.get_pos()):
                        self.angle_x -= self.DELTA if self.angle_x >= 1250 else 0
                        self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
                    elif self.button_left.checking_input(pygame.mouse.get_pos()):
                        self.angle_x += self.DELTA if self.angle_x <= 2250 else 0
                        self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
                    elif self.button_wide.checking_input(pygame.mouse.get_pos()):
                        # wider, from 1500 to 1750
                        self.ser.write((str(7750) + '\n').encode('utf-8'))
                        time.sleep(0.2)
                        self.ser.write((str(7500) + '\n').encode('utf-8'))
                    elif self.button_narrow.checking_input(pygame.mouse.get_pos()):
                        # wider, from 1280 to 1500
                        self.ser.write((str(7300) + '\n').encode('utf-8'))
                        time.sleep(0.2)
                        self.ser.write((str(7500) + '\n').encode('utf-8'))
                    self.screen.fill("white")

            # updating buttons
            self.screen.fill("white")
            self.button_up.update(self.screen)
            '''button_down.update()'''
            self.button_right.update(self.screen)
            self.button_left.update(self.screen)
            self.button_wide.update(self.screen)
            self.button_narrow.update(self.screen)
            pygame.display.update()

    def close_port(self):
        self.ser.close()


class Button:
    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checking_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True


class Controller:
    def __init__(self):
        # controller
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.DELTA = 3
        self.angle_y = 3880
        self.angle_x = 1750
        self.controller.init()
        self.ser = serial.Serial('COM6', baudrate=9600, timeout=0.01)
        time.sleep(1)

    def listen(self):
        while True:
            pygame.event.get()
            if self.controller.get_button(1):
                # right
                self.angle_x -= self.DELTA if self.angle_x >= 1250 else 0
                self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
            elif self.controller.get_button(2):
                # left
                self.angle_x += self.DELTA if self.angle_x <= 2250 else 0
                self.ser.write((str(self.angle_x) + '\n').encode('utf-8'))
            elif self.controller.get_button(3):
                # up
                self.angle_y += self.DELTA if self.angle_y <= 4110 else 0
                self.ser.write((str(self.angle_y) + '\n').encode('utf-8'))
                '''elif self.controller.get_button(0):
                 self.angle_y -= self.DELTA if self.angle_y >= 3880 else 0
                 self.ser.write((str(self.angle_y) +).encode('utf-8'))'''
            elif round(self.controller.get_axis(5), 2) != -1.0:
                # wider
                axis_data = round(self.controller.get_axis(5), 2)
                new_value = int(self.map_data(axis_data, -1.0, 1.0, 7500, 7750))
                self.ser.write((str(new_value) + '\n').encode('utf-8'))
            elif round(self.controller.get_axis(4), 2) != -1.0:
                # narrower
                axis_data = round(self.controller.get_axis(4), 2)
                new_value = int(self.map_data(axis_data, -1.0, 1.0, 7500, 7280))
                self.ser.write((str(new_value) + '\n').encode('utf-8'))

    def close_port(self):
        self.ser.close()

    def map_data(self, x, in_min, in_max, out_min, out_max):
        # converting one interval to another
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == "__main__":
    try:
        try:
            ps4 = Controller()
            ps4.listen()
        except KeyboardInterrupt:
            ps4.close_port()
    except pygame.error:
        try:
            gui = GUI()
            gui.listen()
        except KeyboardInterrupt:
            gui.close_port()
