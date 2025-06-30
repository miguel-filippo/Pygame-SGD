import pygame
import sys
from objects import Button, RegressionLine

# Initialize pygame and create the main window
def init_pygame(width=1200, height=800):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Basic Pygame Setup")
    return screen

# Lista global para armazenar os pontos clicados (pygame)
clicked_points_pygame = []
# Lista global para armazenar os pontos em coordenadas cartesianas
clicked_points_cartesian = []

# Inicializa fonte e botões (serão inicializados em main)
button_clear = None
button_method = None
button_start = None
button_font = None
# Método atual de regressão
current_method = "GD"
regression_line = None
regression_active = False

# Handle all events (like quitting the game)
def handle_events():
    global clicked_points_pygame, clicked_points_cartesian, current_method, regression_line, regression_active
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_clear and button_clear.verify_click(event):
                clicked_points_pygame.clear()
                clicked_points_cartesian.clear()
                regression_line = None
                regression_active = False
            elif button_method and button_method.verify_click(event):
                # Alterna o método e atualiza o texto do botão
                current_method = "SGD" if current_method == "GD" else "GD"
                button_method.text = current_method
            elif button_start and button_start.verify_click(event):
                if clicked_points_cartesian:
                    regression_line = RegressionLine()  # Usa o learning rate padrão já ajustado
                    regression_active = True
            else:
                pos = event.pos
                clicked_points_pygame.append(pos)
                # Converte para cartesian usando a tela atual
                cart_pos = pygame_to_cartesian(pos, pygame.display.get_surface())
                clicked_points_cartesian.append(cart_pos)

# Update game state (placeholder for future logic)
def update():
    global regression_line, regression_active
    if regression_active and regression_line and clicked_points_cartesian:
        regression_line.update(clicked_points_cartesian, method=current_method)

# Draw X and Y axes
def draw_axes(screen):
    width, height = screen.get_size()
    center_x = width // 2
    center_y = height // 2

    # Colors
    axis_color = (50, 50, 50)  # Dark gray for axes
    grid_color = (200, 200, 200)  # Light gray for grid lines

    # Draw main axes
    # X-axis (horizontal line through center)
    pygame.draw.line(screen, axis_color, (0, center_y), (width, center_y), 2)
    # Y-axis (vertical line through center)
    pygame.draw.line(screen, axis_color, (center_x, 0), (center_x, height), 2)

    # Draw grid lines
    grid_spacing = 40

    # Vertical grid lines
    for x in range(0, width, grid_spacing):
        if x != center_x:  # Don't draw over the main Y-axis
            pygame.draw.line(screen, grid_color, (x, 0), (x, height), 1)

    # Horizontal grid lines
    for y in range(0, height, grid_spacing):
        if y != center_y:  # Don't draw over the main X-axis
            pygame.draw.line(screen, grid_color, (0, y), (width, y), 1)

    # Draw axis arrows
    arrow_size = 10

    # X-axis arrow (pointing right)
    pygame.draw.polygon(screen, axis_color, [
        (width - 15, center_y),
        (width - 15 - arrow_size, center_y - arrow_size//2),
        (width - 15 - arrow_size, center_y + arrow_size//2)
    ])

    # Y-axis arrow (pointing up)
    pygame.draw.polygon(screen, axis_color, [
        (center_x, 15),
        (center_x - arrow_size//2, 15 + arrow_size),
        (center_x + arrow_size//2, 15 + arrow_size)
    ])

# Função para converter coordenadas do sistema Pygame para o sistema cartesiano
# (origem no centro, eixo Y para cima)
def pygame_to_cartesian(pos, screen):
    width, height = screen.get_size()
    x_pg, y_pg = pos
    x_cart = x_pg - width // 2
    y_cart = (height // 2) - y_pg
    return (x_cart, y_cart)

# Função para converter coordenadas do sistema cartesiano para o sistema Pygame
# (origem no centro, eixo Y para cima)
def cartesian_to_pygame(pos, screen):
    width, height = screen.get_size()
    x_cart, y_cart = pos
    x_pg = x_cart + width // 2
    y_pg = (height // 2) - y_cart
    return (x_pg, y_pg)

# Draw everything on the screen
def draw(screen):
    screen.fill((230, 230, 230))  # Fill the screen with a light gray color
    draw_axes(screen)  # Draw the X and Y axes
    for point in clicked_points_pygame:
        pygame.draw.circle(screen, (255, 0, 0), point, 6)
    if regression_line:
        # Use os coeficientes desnormalizados se existirem
        m = getattr(regression_line, 'm_real', regression_line.m)
        b = getattr(regression_line, 'b_real', regression_line.b)
        width, height = screen.get_size()
        x_left = -width // 2
        x_right = width // 2
        y_top = height // 2
        y_bottom = -height // 2
        points = []
        y_at_left = m * x_left + b
        y_at_right = m * x_right + b
        if y_bottom <= y_at_left <= y_top:
            points.append(cartesian_to_pygame((x_left, y_at_left), screen))
        if y_bottom <= y_at_right <= y_top:
            points.append(cartesian_to_pygame((x_right, y_at_right), screen))
        if m != 0:
            x_at_top = (y_top - b) / m
            x_at_bottom = (y_bottom - b) / m
            if x_left <= x_at_top <= x_right:
                points.append(cartesian_to_pygame((x_at_top, y_top), screen))
            if x_left <= x_at_bottom <= x_right:
                points.append(cartesian_to_pygame((x_at_bottom, y_bottom), screen))
        if len(points) >= 2:
            pygame.draw.line(screen, (0, 0, 255), points[0], points[1], 3)
        else:
            pass  # Menos de 2 pontos visíveis para desenhar a linha.
    # Desenha os botões
    if button_clear:
        button_clear.update()
        button_clear.draw(screen)
    if button_method:
        button_method.update()
        button_method.draw(screen)
    if button_start:
        button_start.update()
        button_start.draw(screen)
    pygame.display.flip()      # Update the display

# Main game loop
def main():
    global button_clear, button_method, button_start, button_font
    screen = init_pygame()
    clock = pygame.time.Clock()
    button_font = pygame.font.SysFont("Consolas", 20)
    button_clear = Button(rect=(30, 30, 160, 40), text="Limpar pontos", font=button_font)
    button_method = Button(rect=(210, 30, 100, 40), text="GD", font=button_font)
    button_start = Button(rect=(330, 30, 120, 40), text="Começar", font=button_font, bg_color=(70, 180, 70))
    while True:
        handle_events()    # Check for quit or other events
        update()           # Update game state
        draw(screen)       # Draw everything

if __name__ == "__main__":
    main()
