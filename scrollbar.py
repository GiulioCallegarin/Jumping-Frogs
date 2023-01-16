import pygame

GRAY = (197, 194, 197)


class ScrollBar(object):
    def __init__(self, PAGE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.y_axis = 0
        self.page_height = PAGE_HEIGHT
        self.change_y = 0

        bar_height = int((SCREEN_HEIGHT - 40) / (PAGE_HEIGHT / (SCREEN_HEIGHT * 1.0)))
        self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20, 20, 20, bar_height)
        self.bar_up = pygame.Rect(SCREEN_WIDTH - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20, 20, 20)

        self.bar_down_image = pygame.image.load("files\down.png")
        self.bar_up_image = pygame.image.load("files\\up.png")

        self.on_bar = False
        self.mouse_diff = 0

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

    def update(self):
        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.page_height) < self.SCREEN_HEIGHT:
            self.y_axis = self.SCREEN_HEIGHT - self.page_height

        height_diff = self.page_height - self.SCREEN_HEIGHT

        scroll_length = self.SCREEN_HEIGHT - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.SCREEN_HEIGHT - 20):
                self.bar_rect.bottom = self.SCREEN_HEIGHT - 20

            self.y_axis = int(
                height_diff
                / (scroll_length * 1.0)
                * (self.bar_rect.centery - bar_half_lenght)
                * -1
            )
        else:
            self.bar_rect.centery = (
                scroll_length / (height_diff * 1.0) * (self.y_axis * -1)
                + bar_half_lenght
            )

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5

        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_y = 5
            elif event.key == pygame.K_DOWN:
                self.change_y = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.change_y = 0
            elif event.key == pygame.K_DOWN:
                self.change_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.bar_rect)

        screen.blit(self.bar_up_image, (self.SCREEN_WIDTH - 20, 0))
        screen.blit(
            self.bar_down_image, (self.SCREEN_WIDTH - 20, self.SCREEN_HEIGHT - 20)
        )
