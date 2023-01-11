from lylac.interface.Sprite import get_image;

class PreloadService:

    @staticmethod
    def preloadSprite(path: str, forSize: tuple[int, int]):
        for i in range(360):
            get_image(path, (0, 0), forSize, i);
        return True;