import pygame
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

try:
    while True:
        pygame.event.get()
        x = joystick.get_axis(3)  # X axis
        y = joystick.get_axis(2)  # Y axis
        print(f"X: {x}, Y: {y}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Exiting...')
finally:
    pygame.quit()
