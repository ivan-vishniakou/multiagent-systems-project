import pygame
from multiagent_factory.factory import Factory
from multiagent_factory.agents import *
from pygame.locals import *

class FactoryVisualizer(object):
    
    FLOOR_COLOR = (220,220,220)
    MACHINE_COLOR = (250, 100, 100)
    TRANSPORTER_COLOR = (100, 150, 250)
    MACHINE_FONT_COLOR = (100,100,100)
    MACHINE_FONT_SCALE = 0.5
    
    def __init__(self, factory):
        pygame.init()
        self.factory = factory
        self.scale = 25
        
    def xy_to_screen(self, x, y):
        return int(x*self.scale), int(y*self.scale)
    
    def redraw_factory(self):
        pass
      
    def draw_static(self):
        surf = pygame.Surface((self.xy_to_screen(*self.factory.size)))
        surf.fill(FactoryVisualizer.FLOOR_COLOR)
        for a in self.factory.agents:
            if not isinstance(a, Machine):
                continue
            rect = pygame.Rect(self.xy_to_screen(0,0), (self.xy_to_screen(1,1)))
            rect.center = self.xy_to_screen(*a.pos)
            pygame.draw.rect(surf, FactoryVisualizer.MACHINE_COLOR, rect, 3)
            rect.size = self.xy_to_screen(a._progress, 1)
            pygame.draw.rect(surf, FactoryVisualizer.MACHINE_COLOR, rect, 0)
            
            #PRINT NAME
            font = pygame.font.SysFont(None, int(self.scale))
            text = font.render(str(a), 1, FactoryVisualizer.MACHINE_FONT_COLOR)
            textpos = text.get_rect()
            textpos.bottomleft = (rect.bottomleft[0]+self.scale*0.2, 
                                  rect.bottomleft[1]-self.scale*0.1)
            surf.blit(text, textpos)
            
            #PRINT INPUT/OUTPUT
            to_print = 'I:{} O:{}'.format(len(a.input), len(a.output))
            font = pygame.font.SysFont(None, int(self.scale*0.7))
            text = font.render(to_print, 1, FactoryVisualizer.MACHINE_FONT_COLOR)
            textpos = text.get_rect()
            textpos.topleft = (rect.bottomleft[0], 
                                  rect.bottomleft[1]+self.scale*0.1)
            surf.blit(text, textpos)

        return surf
    
    def draw_dynamic(self, background):
        surf = pygame.Surface((self.xy_to_screen(*self.factory.size)))
        surf.blit(background, background.get_rect())
        for a in self.factory.agents:
            if not isinstance(a, Transporter):
                continue
            rect = pygame.Rect(self.xy_to_screen(0,0), (self.xy_to_screen(1,1)))
            rect.center = self.xy_to_screen(*a.pos)
            pygame.draw.ellipse(surf, FactoryVisualizer.TRANSPORTER_COLOR, rect, 0)
            
            #PRINT NAME
            font = pygame.font.SysFont(None, int(self.scale))
            text = font.render(str(a), 1, FactoryVisualizer.MACHINE_FONT_COLOR)
            textpos = text.get_rect()
            textpos.bottomleft = (rect.bottomleft[0]+self.scale*0.2, 
                                  rect.bottomleft[1]-self.scale*0.1)
            surf.blit(text, textpos)
            
            if not a._carried_piece is None:
                font = pygame.font.SysFont(None, int(self.scale*0.7))
                text = font.render(str(a._carried_piece), 1, FactoryVisualizer.MACHINE_FONT_COLOR)
                textpos = text.get_rect()
                textpos.topleft = (rect.bottomright[0]+self.scale*0.1, 
                                      rect.bottomright[1]-self.scale*0.1)
                surf.blit(text, textpos)
        return surf
    
    def run(self):
        screen = pygame.display.set_mode((800, 600))
        screen.fill((255, 255, 255))
        background = self.draw_static()
        background = background.convert()
        center = screen.get_rect().center
        clock = pygame.time.Clock()
        done = False
        paused = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    elif event.key == pygame.K_d:
                        self.factory.debug_print()
                    elif event.key == pygame.K_p:
                        paused = not paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    dx, dy = mouse_pos[0]-center[0], mouse_pos[1]-center[1]
                    if event.button == 4 and self.scale<500: self.scale *= 1.1
                    if event.button == 5 and self.scale>0.1: self.scale /= 1.1
                    ''' TODO: nicer zoom in/out
                    mouse_pos = pygame.mouse.get_pos()
                    prev_rect = background.get_rect()
                    background = self.draw_static()
                    new_rect = background.get_rect()
                    center = (
                        mouse_pos
                              )
                    p = pygame.Rect()
                    '''
            background = self.draw_static()
                    #print dx, dy
            overlay = self.draw_dynamic(background)
            screen.fill((255, 255, 255))
            rect = background.get_rect()
            rect.center = center
            screen.blit(overlay, rect)
            pygame.display.flip()
            clock.tick(200)
            if not paused:
                self.factory.tick()
        pygame.quit()