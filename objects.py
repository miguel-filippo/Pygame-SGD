import pygame
import random

class Button:
    def __init__(self, rect, text, font, bg_color=(180, 70, 70), text_color=(0, 0, 0), border_color=(50, 50, 50), border_width=2):
        self.rect = pygame.Rect(rect)  # (x, y, w, h)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.hovered = False
        self.clicked = False

    def draw(self, screen):
        # Muda cor se estiver com mouse em cima
        color = tuple(min(255, c+30) for c in self.bg_color) if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        # Renderiza texto centralizado
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def verify_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        return False

    def update(self):
        # Atualiza estado de hover
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def reset(self):
        self.clicked = False

class RegressionLine:
    def __init__(self, m=0.0, b=0.0, learning_rate=1e-2):
        self.m = m  # coeficiente angular
        self.b = b  # coeficiente linear
        self.learning_rate = learning_rate

    def get_coefficients(self):
        """Retorna (m, b)"""
        return self.m, self.b

    def update(self, points, method="GD"):
        """
        Atualiza m e b usando um passo de gradiente descendente.
        points: lista de tuplas (x, y) em coordenadas cartesianas
        method: "GD" (batch) ou "SGD" (estocástico)
        """
        if not points:
            return
        # Normalização dos dados para [-1, 1]
        X = [p[0] for p in points]
        y = [p[1] for p in points]
        max_x = max(abs(x) for x in X) if X else 1
        max_y = max(abs(val) for val in y) if y else 1
        X_norm = [x / max_x for x in X]
        y_norm = [val / max_y for val in y]
        n = len(points)
        if method == "GD":
            # Batch Gradient Descent
            Y_pred = [self.m * xi + self.b for xi in X_norm]
            derivadam = (-2/n) * sum(xi * (yi - ypi) for xi, yi, ypi in zip(X_norm, y_norm, Y_pred))
            derivadab = (-2/n) * sum(yi - ypi for yi, ypi in zip(y_norm, Y_pred))
            self.m -= self.learning_rate * derivadam
            self.b -= self.learning_rate * derivadab
        elif method == "SGD":
            # Stochastic Gradient Descent (um ponto aleatório)
            idx = random.randint(0, n-1)
            xi, yi = X_norm[idx], y_norm[idx]
            Y_pred_i = self.m * xi + self.b
            derivadam = -2 * xi * (yi - Y_pred_i)
            derivadab = -2 * (yi - Y_pred_i)
            self.m -= self.learning_rate * derivadam
            self.b -= self.learning_rate * derivadab
        else:
            raise ValueError("Método deve ser 'GD' ou 'SGD'")
        # Calcular e printar o MSE
        Y_pred_all = [self.m * xi + self.b for xi in X_norm]
        mse = sum((yi - ypi) ** 2 for yi, ypi in zip(y_norm, Y_pred_all)) / n
        print(f"MSE: {mse}")
        # Desnormalizar coeficientes para uso na tela
        self.m_real = self.m * (max_y / max_x)
        self.b_real = self.b * max_y
