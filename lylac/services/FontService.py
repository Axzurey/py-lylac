import os;
import pathlib
from typing import Optional

import pygame;

FreeColorTuple = tuple[int, int, int, Optional[int]]

class FreeFont:

    def render(
        self, text: str, fgcolor: FreeColorTuple = (255, 255, 255, 255), bgColor: FreeColorTuple = (0, 0, 0, 0),
        rotation: int = 0, size: int = 16
    ) -> tuple[pygame.Surface, pygame.Rect]: ...

class FontService:

    fonts: dict[str, FreeFont] = {}
    _subFontsForTextEffects: dict[str, dict[int, pygame.font.Font]] = {}; #{name, {fontsize, Font Object}}
    _fontPaths: dict[str, str] = {};

    @staticmethod
    def get_width_and_height_for_string(font: str, string: str, fontSize: int):

        if not font in FontService._subFontsForTextEffects:
            FontService._subFontsForTextEffects[font] = {fontSize: pygame.font.Font(FontService._fontPaths[font], fontSize)};
        if not fontSize in FontService._subFontsForTextEffects[font]:
            FontService._subFontsForTextEffects[font][fontSize] = pygame.font.Font(FontService._fontPaths[font], fontSize);

        return FontService._subFontsForTextEffects[font][fontSize].size(string);

    @staticmethod
    def loadFont(fontAlias: str, fontPath: str, defaultFontSize: int = 20):
        """
        parameter [fontAlias] is automatically made lowercase
        parameter [fontPath] should be the absolute path to the font file
        """
        try:
            if os.path.isfile(fontPath) and fontPath.split('.')[len(fontPath.split('.')) - 1] == 'ttf':
                font: freeFont = pygame.freetype.Font(fontPath, defaultFontSize) #type: ignore
                FontService._fontPaths[fontAlias.lower()] = fontPath;
                FontService.fonts[fontAlias.lower()] = font
            else:
                print(f'[nyle]: Unable to load font "{fontAlias.lower()}" from path {fontPath} as it is not .ttf file')
        except Exception:
            print(f'[nyle]: (Unexpected) Unable to load font "{fontAlias.lower()}" from path {fontPath}')
    
    @staticmethod
    def loadDefaultFonts():
        searchDir = os.path.join(str(pathlib.Path(__file__).parent.parent.resolve()), 'fonts')
        if os.path.isdir(searchDir):
            for p in os.listdir(searchDir):
                FontService.loadFont(os.path.basename(p.split('.')[0]), os.path.join(searchDir, p))
        else:
            print(f'[nyle]: Unable to load default fonts from {searchDir} as it is not a folder')