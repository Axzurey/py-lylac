from typing import TypedDict
import pygame
from enum import Enum, unique

@unique
class LylacEnum(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    O = 'O'
    P = 'P'
    Q = 'Q'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    V = 'V'
    W = 'W'
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    ONE = 'ONE'
    TWO = 'TWO'
    THREE = 'THREE'
    FOUR = 'FOUR'
    FIVE = 'FIVE'
    SIX = 'SIX'
    SEVEN = 'SEVEN'
    EIGHT = 'EIGHT'
    NINE = 'NINE'
    ZERO = 'ZERO'
    PERIOD = 'PERIOD'
    COMMA = 'COMMA'
    SLASH = 'SLASH'
    BACKSPACE = 'BACKSPACE'
    SEMICOLON = 'SEMICOLON'
    BACKSLASH = 'BACKSLASH'
    BACKTICK = 'BACKTICK' # `
    SINGLE_QUOTE = 'SINGLE_QUOTE'
    DOUBLE_QUOTE = 'DOUBLE_QUOTE'
    LEFT_BRACKET = 'LEFT_BRACKET' # [
    RIGHT_BRACKET = 'RIGHT_BRACKET'
    MINUS = 'MINUS'
    EQUALS = 'EQUALS'
    ESCAPE = 'ESCAPE'
    HOME = 'HOME'
    TAB = 'TAB'
    CAPS_LOCK = 'CAPS_LOCK'
    LEFT_SHIFT = 'LEFT_SHIFT'
    RIGHT_SHIFT = 'RIGHT_SHIFT'
    LEFT_CONTROL = 'LEFT_CONTROL'
    RIGHT_CONTROL = 'RIGHT_CONTROL'
    LEFT_ALT = 'LEFT_ALT'
    RIGHT_ALT = 'RIGHT_ALT'
    ENTER = 'ENTER'
    FUNCTION = 'FUNCTION'
    PAGE_UP = 'PAGE_UP'
    PAGE_DOWN = 'PAGE_DOWN'
    KEYPAD_ONE = 'KEYPAD_ONE'
    KEYPAD_TWO = 'KEYPAD_TWO'
    KEYPAD_THREE = 'KEYPAD_THREE'
    KEYPAD_FOUR = 'KEYPAD_FOUR'
    KEYPAD_FIVE = 'KEYPAD_FIVE'
    KEYPAD_SIX = 'KEYPAD_SIX'
    KEYPAD_SEVEN = 'KEYPAD_SEVEN'
    KEYPAD_EIGHT = 'KEYPAD_EIGHT'
    KEYPAD_NINE = 'KEYPAD_NINE'
    KEYPAD_ZERO = 'KEYPAD_ZERO'
    KEYPAD_PERIOD = 'KEYPAD_PERIOD'
    KEYPAD_ENTER = 'KEYPAD_ENTER'
    KEYPAD_PLUS = 'KEYPAD_PLUS'
    KEYPAD_MINUS = 'KEYPAD_MINUS'
    KEYPAD_ASTERISK = 'KEYPAD_ASTERISK'
    KEYPAD_SLASH = 'KEYPAD_SLASH'
    KEYPAD_EQUALS = 'KEYPAD_EQUALS'
    NUMLOCK = 'NUMLOCK'
    F1 = 'F1'
    F2 = 'F2'
    F3 = 'F3'
    F4 = 'F4'
    F5 = 'F5'
    F6 = 'F6'
    F7 = 'F7'
    F8 = 'F8'
    F9 = 'F9'
    F10 = 'F10'
    F11 = 'F11'
    F12 = 'F12'
    F13 = 'F13'
    F14 = 'F14'
    F15 = 'F15'
    INSERT = 'INSERT'
    DELETE = 'DELETE'
    SPACE = 'SPACE'
    END = 'END'
    SCROLL_LOCK = 'SCROLL_LOCK'
    LEFT_META = 'LEFT_META'
    RIGHT_META = 'RIGHT_META'
    LEFT_SUPER = 'LEFT_SUPER'
    RIGHT_SUPER = 'RIGHT_SUPER'
    MODE = 'MODE'
    HELP = 'HELP'
    PRINT = 'PRINT'
    SYSREQ = 'SYSREQ'
    BREAK = 'BREAK'
    MENU = 'MENU'
    POWER = 'POWER'
    EURO = 'EURO'
    ANDROID_BACK = 'ANDROID_BACK'

    #The following require the shift key to be pressed

    TILDE = 'TILDE' # ~
    BANG = 'BANG' # !
    AT = 'AT' # @
    HASH = 'HASH'
    DOLLAR = 'DOLLAR'
    PERCENT = 'PERCENT'
    CARET = 'CARET'
    AMPERSAND = 'AMPERSAND'
    ASTERISK = 'ASTERISK'
    LEFT_PARENTHESIS = 'LEFT_PARENTHESIS' # (
    RIGHT_PARENTHESIS = 'RIGHT_PARENTHESIS' # )
    UNDERSCORE = 'UNDERSCORE'
    PLUS = 'PLUS'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    PIPE = 'PIPE' # |
    COLON = 'COLON'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    QUESTION_MARK = 'QUESTION_MARK'

    #MACOS

    CLEAR = 'CLEAR'


requiresShift = [
    LylacEnum.TILDE,
    LylacEnum.AT,
    LylacEnum.HASH,
    LylacEnum.DOLLAR,
    LylacEnum.PERCENT,
    LylacEnum.CARET,
    LylacEnum.AMPERSAND,
    LylacEnum.ASTERISK,
    LylacEnum.LEFT_PARENTHESIS,
    LylacEnum.RIGHT_PARENTHESIS,
    LylacEnum.MINUS,
    LylacEnum.PLUS,
    LylacEnum.LEFT_PARENTHESIS,
    LylacEnum.RIGHT_PARENTHESIS,
    LylacEnum.UNDERSCORE,
    LylacEnum.PLUS,
    LylacEnum.LEFT_BRACE,
    LylacEnum.RIGHT_BRACE,
    LylacEnum.PIPE,
    LylacEnum.COLON,
    LylacEnum.GREATER_THAN,
    LylacEnum.LESS_THAN,
    LylacEnum.QUESTION_MARK
]

keyConvert = {
    pygame.K_BACKSPACE: LylacEnum.BACKSPACE,
    pygame.K_TAB: LylacEnum.TAB,
    pygame.K_CLEAR: LylacEnum.CLEAR,
    pygame.K_RETURN: LylacEnum.ENTER,
    pygame.K_ESCAPE: LylacEnum.ESCAPE,
    pygame.K_SPACE: LylacEnum.SPACE,
    pygame.K_EXCLAIM: LylacEnum.BANG,
    pygame.K_QUOTEDBL: LylacEnum.DOUBLE_QUOTE,
    pygame.K_HASH: LylacEnum.HASH,
    pygame.K_DOLLAR: LylacEnum.DOLLAR,
    pygame.K_AMPERSAND: LylacEnum.AMPERSAND,
    pygame.K_QUOTE: LylacEnum.SINGLE_QUOTE,
    pygame.K_LEFTPAREN: LylacEnum.LEFT_PARENTHESIS,
    pygame.K_RIGHTPAREN: LylacEnum.RIGHT_PARENTHESIS,
    pygame.K_ASTERISK: LylacEnum.ASTERISK,
    pygame.K_PLUS: LylacEnum.PLUS,
    pygame.K_COMMA: LylacEnum.COMMA,
    pygame.K_MINUS: LylacEnum.MINUS,
    pygame.K_PERIOD: LylacEnum.PERIOD,
    pygame.K_SLASH: LylacEnum.SLASH,
    pygame.K_0: LylacEnum.ZERO,
    pygame.K_1: LylacEnum.ONE,
    pygame.K_2: LylacEnum.TWO,
    pygame.K_3: LylacEnum.THREE,
    pygame.K_4: LylacEnum.FOUR,
    pygame.K_5: LylacEnum.FIVE,
    pygame.K_6: LylacEnum.SIX,
    pygame.K_7: LylacEnum.SEVEN,
    pygame.K_8: LylacEnum.EIGHT,
    pygame.K_9: LylacEnum.NINE,
    pygame.K_COLON: LylacEnum.COLON,
    pygame.K_SEMICOLON: LylacEnum.SEMICOLON,
    pygame.K_LESS: LylacEnum.LESS_THAN,
    pygame.K_EQUALS: LylacEnum.EQUALS,
    pygame.K_GREATER: LylacEnum.GREATER_THAN,
    pygame.K_QUESTION: LylacEnum.QUESTION_MARK,
    pygame.K_AT: LylacEnum.AT,
    pygame.K_LEFTBRACKET: LylacEnum.LEFT_BRACKET,
    pygame.K_BACKSLASH: LylacEnum.BACKSLASH,
    pygame.K_RIGHTBRACKET: LylacEnum.RIGHT_BRACKET,
    pygame.K_CARET: LylacEnum.CARET,
    pygame.K_UNDERSCORE: LylacEnum.UNDERSCORE,
    pygame.K_BACKQUOTE: LylacEnum.TILDE,
    pygame.K_a: LylacEnum.A,
    pygame.K_b: LylacEnum.B,
    pygame.K_c: LylacEnum.C,
    pygame.K_d: LylacEnum.D,
    pygame.K_e: LylacEnum.E,
    pygame.K_f: LylacEnum.F,
    pygame.K_g: LylacEnum.G,
    pygame.K_h: LylacEnum.H,
    pygame.K_i: LylacEnum.I,
    pygame.K_j: LylacEnum.J,
    pygame.K_k: LylacEnum.K,
    pygame.K_l: LylacEnum.L,
    pygame.K_m: LylacEnum.M,
    pygame.K_n: LylacEnum.N,
    pygame.K_o: LylacEnum.O,
    pygame.K_p: LylacEnum.P,
    pygame.K_q: LylacEnum.Q,
    pygame.K_r: LylacEnum.R,
    pygame.K_s: LylacEnum.S,
    pygame.K_t: LylacEnum.T,
    pygame.K_u: LylacEnum.U,
    pygame.K_v: LylacEnum.V,
    pygame.K_w: LylacEnum.W,
    pygame.K_x: LylacEnum.X,
    pygame.K_y: LylacEnum.Y,
    pygame.K_z: LylacEnum.Z,
    pygame.K_DELETE: LylacEnum.DELETE,
    pygame.K_KP0: LylacEnum.KEYPAD_ZERO,
    pygame.K_KP1: LylacEnum.KEYPAD_ONE,
    pygame.K_KP2: LylacEnum.KEYPAD_ZERO,
    pygame.K_KP3: LylacEnum.KEYPAD_THREE,
    pygame.K_KP4: LylacEnum.KEYPAD_FOUR,
    pygame.K_KP5: LylacEnum.KEYPAD_FIVE,
    pygame.K_KP6: LylacEnum.KEYPAD_SIX,
    pygame.K_KP7: LylacEnum.KEYPAD_SEVEN,
    pygame.K_KP8: LylacEnum.KEYPAD_EIGHT,
    pygame.K_KP9: LylacEnum.KEYPAD_NINE,
    pygame.K_KP_PERIOD: LylacEnum.KEYPAD_PERIOD,
    pygame.K_KP_DIVIDE: LylacEnum.KEYPAD_SLASH,
    pygame.K_KP_MULTIPLY: LylacEnum.KEYPAD_ASTERISK,
    pygame.K_KP_MINUS: LylacEnum.KEYPAD_MINUS,
    pygame.K_KP_PLUS: LylacEnum.KEYPAD_PLUS,
    pygame.K_KP_ENTER: LylacEnum.KEYPAD_ENTER,
    pygame.K_KP_EQUALS: LylacEnum.KEYPAD_EQUALS,
    pygame.K_UP: LylacEnum.UP,
    pygame.K_DOWN: LylacEnum.DOWN,
    pygame.K_RIGHT: LylacEnum.RIGHT,
    pygame.K_LEFT: LylacEnum.LEFT,
    pygame.K_INSERT: LylacEnum.INSERT,
    pygame.K_HOME: LylacEnum.HOME,
    pygame.K_END: LylacEnum.END,
    pygame.K_PAGEUP: LylacEnum.PAGE_UP,
    pygame.K_PAGEDOWN: LylacEnum.PAGE_DOWN,
    pygame.K_F1: LylacEnum.F1,
    pygame.K_F2: LylacEnum.F2,
    pygame.K_F3: LylacEnum.F3,
    pygame.K_F4: LylacEnum.F4,
    pygame.K_F5: LylacEnum.F5,
    pygame.K_F6: LylacEnum.F6,
    pygame.K_F7: LylacEnum.F7,
    pygame.K_F8: LylacEnum.F8,
    pygame.K_F9: LylacEnum.F9,
    pygame.K_F10: LylacEnum.F10,
    pygame.K_F11: LylacEnum.F11,
    pygame.K_F12: LylacEnum.F12,
    pygame.K_F13: LylacEnum.F13,
    pygame.K_F14: LylacEnum.F14,
    pygame.K_F15: LylacEnum.F15,
    pygame.K_NUMLOCK: LylacEnum.NUMLOCK,
    pygame.K_CAPSLOCK: LylacEnum.CAPS_LOCK,
    pygame.K_SCROLLOCK: LylacEnum.SCROLL_LOCK,
    pygame.K_RSHIFT: LylacEnum.RIGHT_SHIFT,
    pygame.K_LSHIFT: LylacEnum.LEFT_SHIFT,
    pygame.K_RCTRL: LylacEnum.RIGHT_CONTROL,
    pygame.K_LCTRL: LylacEnum.LEFT_CONTROL,
    pygame.K_RALT: LylacEnum.LEFT_ALT,
    pygame.K_LALT: LylacEnum.RIGHT_ALT,
    pygame.K_RMETA: LylacEnum.RIGHT_META,
    pygame.K_LMETA: LylacEnum.LEFT_META,
    pygame.K_LSUPER: LylacEnum.LEFT_SUPER,
    pygame.K_RSUPER: LylacEnum.RIGHT_SUPER,
    pygame.K_MODE: LylacEnum.MODE,
    pygame.K_HELP: LylacEnum.HELP,
    pygame.K_PRINT: LylacEnum.PRINT,
    pygame.K_SYSREQ: LylacEnum.SYSREQ,
    pygame.K_BREAK: LylacEnum.BREAK,
    pygame.K_MENU: LylacEnum.MENU,
    pygame.K_POWER: LylacEnum.POWER,
    pygame.K_EURO: LylacEnum.EURO,
    pygame.K_AC_BACK: LylacEnum.ANDROID_BACK
}

class LylacModifiers(Enum):
    NONE = 'None'
    LEFT_SHIFT = 'LEFT_SHIFT'
    RIGHT_SHIFT = 'RIGHT_SHIFT'
    SHIFT = 'SHIFT'
    LEFT_CONTROL = 'LEFT_CONTROL'
    RIGHT_CONTROL = 'RIGHT_CONTROL'
    CONTROL = 'CONTROL'
    LEFT_ALT = 'LEFT_ALT'
    RIGHT_ALT = 'RIGHT_ALT'
    ALT = 'ALT'
    LEFT_META = 'LEFT_META'
    RIGHT_META = 'RIGHT_META'
    META = 'META'
    CAPS_LOCK = 'CAPS_LOCK'
    NUM_LOCK = 'NUM_LOCK'
    MODE = 'MODE'

modifierConvert = {
    pygame.KMOD_NONE: LylacModifiers.NONE,
    pygame.KMOD_LSHIFT: LylacModifiers.LEFT_SHIFT,
    pygame.KMOD_RSHIFT: LylacModifiers.RIGHT_SHIFT,
    pygame.KMOD_SHIFT: LylacModifiers.SHIFT,
    pygame.KMOD_LCTRL: LylacModifiers.LEFT_CONTROL,
    pygame.KMOD_RCTRL: LylacModifiers.RIGHT_CONTROL,
    pygame.KMOD_CTRL: LylacModifiers.CONTROL,
    pygame.KMOD_LALT: LylacModifiers.LEFT_ALT,
    pygame.KMOD_RALT: LylacModifiers.RIGHT_ALT,
    pygame.KMOD_ALT: LylacModifiers.ALT,
    pygame.KMOD_LMETA: LylacModifiers.LEFT_META,
    pygame.KMOD_RMETA: LylacModifiers.RIGHT_META,
    pygame.KMOD_META: LylacModifiers.META,
    pygame.KMOD_CAPS: LylacModifiers.CAPS_LOCK,
    pygame.KMOD_NUM: LylacModifiers.NUM_LOCK,
    pygame.KMOD_MODE: LylacModifiers.MODE,
}

class RawKeyBuffer(TypedDict):
    keys: list[int]
    modifiers: list[int]

class KeyBuffer(TypedDict):
    keys: list[LylacEnum]
    modifiers: list[LylacModifiers]

def purifyRawKeyBuffer(keyBuffer: RawKeyBuffer) -> KeyBuffer:
    pureKeys: list[LylacEnum] = []
    pureMods: list[LylacModifiers] = []

    for key in keyBuffer["keys"]:

        v = keyConvert.get(key)

        if v: pureKeys.append(v)
        else: pass #not recognized
    for mod in keyBuffer["modifiers"]:

        v = modifierConvert.get(mod)

        print(keyBuffer)

        if v: pureMods.append(v)
        else: pass #not recognized

    return {
        "modifiers": pureMods,
        "keys": pureKeys
    }