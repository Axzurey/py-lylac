import pygame
import numpy
import cv2

def create_neon(surf: pygame.Surface | pygame.surface.Surface):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha) # type: ignore
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1)) # type: ignore
    image = numpy.concatenate((rgb, alpha), 2) # type: ignore
    cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image) # type: ignore
    cv2.blur(image, ksize=(5, 5), dst=image) # type: ignore
    
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA') # type: ignore

    #bloom_surf = pygame.transform.rotate(bloom_surf, 90)
    
    return bloom_surf