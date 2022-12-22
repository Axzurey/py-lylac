from typing import TypedDict
import pygame
from enum import Enum, unique

@unique
class KeyCode(Enum):
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
    KeyCode.TILDE,
    KeyCode.AT,
    KeyCode.HASH,
    KeyCode.DOLLAR,
    KeyCode.PERCENT,
    KeyCode.CARET,
    KeyCode.AMPERSAND,
    KeyCode.ASTERISK,
    KeyCode.LEFT_PARENTHESIS,
    KeyCode.RIGHT_PARENTHESIS,
    KeyCode.MINUS,
    KeyCode.PLUS,
    KeyCode.LEFT_PARENTHESIS,
    KeyCode.RIGHT_PARENTHESIS,
    KeyCode.UNDERSCORE,
    KeyCode.PLUS,
    KeyCode.LEFT_BRACE,
    KeyCode.RIGHT_BRACE,
    KeyCode.PIPE,
    KeyCode.COLON,
    KeyCode.GREATER_THAN,
    KeyCode.LESS_THAN,
    KeyCode.QUESTION_MARK
]

keyConvert = {
    pygame.K_BACKSPACE: KeyCode.BACKSPACE,
    pygame.K_TAB: KeyCode.TAB,
    pygame.K_CLEAR: KeyCode.CLEAR,
    pygame.K_RETURN: KeyCode.ENTER,
    pygame.K_ESCAPE: KeyCode.ESCAPE,
    pygame.K_SPACE: KeyCode.SPACE,
    pygame.K_EXCLAIM: KeyCode.BANG,
    pygame.K_QUOTEDBL: KeyCode.DOUBLE_QUOTE,
    pygame.K_HASH: KeyCode.HASH,
    pygame.K_DOLLAR: KeyCode.DOLLAR,
    pygame.K_AMPERSAND: KeyCode.AMPERSAND,
    pygame.K_QUOTE: KeyCode.SINGLE_QUOTE,
    pygame.K_LEFTPAREN: KeyCode.LEFT_PARENTHESIS,
    pygame.K_RIGHTPAREN: KeyCode.RIGHT_PARENTHESIS,
    pygame.K_ASTERISK: KeyCode.ASTERISK,
    pygame.K_PLUS: KeyCode.PLUS,
    pygame.K_COMMA: KeyCode.COMMA,
    pygame.K_MINUS: KeyCode.MINUS,
    pygame.K_PERIOD: KeyCode.PERIOD,
    pygame.K_SLASH: KeyCode.SLASH,
    pygame.K_0: KeyCode.ZERO,
    pygame.K_1: KeyCode.ONE,
    pygame.K_2: KeyCode.TWO,
    pygame.K_3: KeyCode.THREE,
    pygame.K_4: KeyCode.FOUR,
    pygame.K_5: KeyCode.FIVE,
    pygame.K_6: KeyCode.SIX,
    pygame.K_7: KeyCode.SEVEN,
    pygame.K_8: KeyCode.EIGHT,
    pygame.K_9: KeyCode.NINE,
    pygame.K_COLON: KeyCode.COLON,
    pygame.K_SEMICOLON: KeyCode.SEMICOLON,
    pygame.K_LESS: KeyCode.LESS_THAN,
    pygame.K_EQUALS: KeyCode.EQUALS,
    pygame.K_GREATER: KeyCode.GREATER_THAN,
    pygame.K_QUESTION: KeyCode.QUESTION_MARK,
    pygame.K_AT: KeyCode.AT,
    pygame.K_LEFTBRACKET: KeyCode.LEFT_BRACKET,
    pygame.K_BACKSLASH: KeyCode.BACKSLASH,
    pygame.K_RIGHTBRACKET: KeyCode.RIGHT_BRACKET,
    pygame.K_CARET: KeyCode.CARET,
    pygame.K_UNDERSCORE: KeyCode.UNDERSCORE,
    pygame.K_BACKQUOTE: KeyCode.TILDE,
    pygame.K_a: KeyCode.A,
    pygame.K_b: KeyCode.B,
    pygame.K_c: KeyCode.C,
    pygame.K_d: KeyCode.D,
    pygame.K_e: KeyCode.E,
    pygame.K_f: KeyCode.F,
    pygame.K_g: KeyCode.G,
    pygame.K_h: KeyCode.H,
    pygame.K_i: KeyCode.I,
    pygame.K_j: KeyCode.J,
    pygame.K_k: KeyCode.K,
    pygame.K_l: KeyCode.L,
    pygame.K_m: KeyCode.M,
    pygame.K_n: KeyCode.N,
    pygame.K_o: KeyCode.O,
    pygame.K_p: KeyCode.P,
    pygame.K_q: KeyCode.Q,
    pygame.K_r: KeyCode.R,
    pygame.K_s: KeyCode.S,
    pygame.K_t: KeyCode.T,
    pygame.K_u: KeyCode.U,
    pygame.K_v: KeyCode.V,
    pygame.K_w: KeyCode.W,
    pygame.K_x: KeyCode.X,
    pygame.K_y: KeyCode.Y,
    pygame.K_z: KeyCode.Z,
    pygame.K_DELETE: KeyCode.DELETE,
    pygame.K_KP0: KeyCode.KEYPAD_ZERO,
    pygame.K_KP1: KeyCode.KEYPAD_ONE,
    pygame.K_KP2: KeyCode.KEYPAD_ZERO,
    pygame.K_KP3: KeyCode.KEYPAD_THREE,
    pygame.K_KP4: KeyCode.KEYPAD_FOUR,
    pygame.K_KP5: KeyCode.KEYPAD_FIVE,
    pygame.K_KP6: KeyCode.KEYPAD_SIX,
    pygame.K_KP7: KeyCode.KEYPAD_SEVEN,
    pygame.K_KP8: KeyCode.KEYPAD_EIGHT,
    pygame.K_KP9: KeyCode.KEYPAD_NINE,
    pygame.K_KP_PERIOD: KeyCode.KEYPAD_PERIOD,
    pygame.K_KP_DIVIDE: KeyCode.KEYPAD_SLASH,
    pygame.K_KP_MULTIPLY: KeyCode.KEYPAD_ASTERISK,
    pygame.K_KP_MINUS: KeyCode.KEYPAD_MINUS,
    pygame.K_KP_PLUS: KeyCode.KEYPAD_PLUS,
    pygame.K_KP_ENTER: KeyCode.KEYPAD_ENTER,
    pygame.K_KP_EQUALS: KeyCode.KEYPAD_EQUALS,
    pygame.K_UP: KeyCode.UP,
    pygame.K_DOWN: KeyCode.DOWN,
    pygame.K_RIGHT: KeyCode.RIGHT,
    pygame.K_LEFT: KeyCode.LEFT,
    pygame.K_INSERT: KeyCode.INSERT,
    pygame.K_HOME: KeyCode.HOME,
    pygame.K_END: KeyCode.END,
    pygame.K_PAGEUP: KeyCode.PAGE_UP,
    pygame.K_PAGEDOWN: KeyCode.PAGE_DOWN,
    pygame.K_F1: KeyCode.F1,
    pygame.K_F2: KeyCode.F2,
    pygame.K_F3: KeyCode.F3,
    pygame.K_F4: KeyCode.F4,
    pygame.K_F5: KeyCode.F5,
    pygame.K_F6: KeyCode.F6,
    pygame.K_F7: KeyCode.F7,
    pygame.K_F8: KeyCode.F8,
    pygame.K_F9: KeyCode.F9,
    pygame.K_F10: KeyCode.F10,
    pygame.K_F11: KeyCode.F11,
    pygame.K_F12: KeyCode.F12,
    pygame.K_F13: KeyCode.F13,
    pygame.K_F14: KeyCode.F14,
    pygame.K_F15: KeyCode.F15,
    pygame.K_NUMLOCK: KeyCode.NUMLOCK,
    pygame.K_CAPSLOCK: KeyCode.CAPS_LOCK,
    pygame.K_SCROLLOCK: KeyCode.SCROLL_LOCK,
    pygame.K_RSHIFT: KeyCode.RIGHT_SHIFT,
    pygame.K_LSHIFT: KeyCode.LEFT_SHIFT,
    pygame.K_RCTRL: KeyCode.RIGHT_CONTROL,
    pygame.K_LCTRL: KeyCode.LEFT_CONTROL,
    pygame.K_RALT: KeyCode.LEFT_ALT,
    pygame.K_LALT: KeyCode.RIGHT_ALT,
    pygame.K_RMETA: KeyCode.RIGHT_META,
    pygame.K_LMETA: KeyCode.LEFT_META,
    pygame.K_LSUPER: KeyCode.LEFT_SUPER,
    pygame.K_RSUPER: KeyCode.RIGHT_SUPER,
    pygame.K_MODE: KeyCode.MODE,
    pygame.K_HELP: KeyCode.HELP,
    pygame.K_PRINT: KeyCode.PRINT,
    pygame.K_SYSREQ: KeyCode.SYSREQ,
    pygame.K_BREAK: KeyCode.BREAK,
    pygame.K_MENU: KeyCode.MENU,
    pygame.K_POWER: KeyCode.POWER,
    pygame.K_EURO: KeyCode.EURO,
    pygame.K_AC_BACK: KeyCode.ANDROID_BACK
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
    keys: list[KeyCode]
    modifiers: list[LylacModifiers]

def purifyRawKeyBuffer(keyBuffer: RawKeyBuffer) -> KeyBuffer:
    pureKeys: list[KeyCode] = []
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