import pygame, sys
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
            
            font = pygame.font.SysFont(None, int(self.scale))#pygame.font.Font(None, self.scale)
            text = font.render(str(a), 1, FactoryVisualizer.MACHINE_FONT_COLOR)
            textpos = text.get_rect()
            textpos.bottomleft = (rect.bottomleft[0]+self.scale*0.2, 
                                  rect.bottomleft[1]-self.scale*0.1)
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
            
            font = pygame.font.SysFont(None, int(self.scale))#pygame.font.Font(None, self.scale)
            text = font.render(str(a), 1, FactoryVisualizer.MACHINE_FONT_COLOR)
            textpos = text.get_rect()
            textpos.bottomleft = (rect.bottomleft[0]+self.scale*0.2, 
                                  rect.bottomleft[1]-self.scale*0.1)
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
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: self.scale *= 1.1
                    if event.button == 5: self.scale /= 1.1
                    # TODO, smart zooming like in google maps
                    #mouse_pos = pygame.mouse.get_pos()
                    #center = (int(0.5*center[0]+0.5*(mouse_pos[0]-center[0])), 
                    #          int(0.5*center[1]+0.5*(mouse_pos[1]-center[1])))
                    background = self.draw_static()
            overlay = self.draw_dynamic(background)
            screen.fill((255, 255, 255))
            rect = background.get_rect()
            rect.center = center
            #screen.blit(background, rect)
            screen.blit(overlay, rect)
            pygame.display.flip()
            clock.tick(60)
            self.factory.tick()
        pygame.quit()  
        
if __name__=='__main__':
    fv = FactoryVisualizer(Factory())
    fv.run()