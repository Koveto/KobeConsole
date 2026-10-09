import pygame

pygame.init()
pygame.joystick.init()

print("-" * 50)
print("CONTROLLER TEST")
print("-" * 50)

controller_count = pygame.joystick.get_count()

print(f"Controllers Found: {controller_count}")

if controller_count == 0:

    print("\nNo controller detected.")
    print("Connect a controller and restart.")
    input("\nPress ENTER to exit...")
    quit()

controller = pygame.joystick.Joystick(0)
controller.init()

print(f"\nController Name: {controller.get_name()}")
print(f"Axes: {controller.get_numaxes()}")
print(f"Buttons: {controller.get_numbuttons()}")
print(f"Hats: {controller.get_numhats()}")

print("\nMove sticks, press buttons, and use the D-Pad.")
print("Close the window to exit.\n")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Controller Test")

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.JOYBUTTONDOWN:

            print(
                f"BUTTON DOWN: "
                f"{event.button}"
            )

        elif event.type == pygame.JOYBUTTONUP:

            print(
                f"BUTTON UP: "
                f"{event.button}"
            )

        elif event.type == pygame.JOYHATMOTION:

            print(
                f"HAT: "
                f"{event.value}"
            )

        elif event.type == pygame.JOYAXISMOTION:

            if abs(event.value) > 0.5:

                print(
                    f"AXIS {event.axis}: "
                    f"{event.value:.2f}"
                )

    screen.fill((20, 20, 40))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()