"""
Color Square Display
====================
Shows a single colored square with a label beneath it.
"""

import pygame
import sys

# ── Configuration ─────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H = 480, 360
FPS = 10                            # frames per second
BG_COLOR    = (255, 255, 255)
SQUARE_COLOR = (255, 100, 50)       # ← change this to any RGB value
SQUARE_SIZE = 200
LABEL_TEXT  = "RGB(255, 100, 50)"
COLOR_SIZE = 20
# ──────────────────────────────────────────────────────────────────────────────

COLOR_LIST = [
    {"R": 189, "G": 108, "B":  72, "ColorName": "Adobe"               },
    {"R":  84, "G": 172, "B": 104, "ColorName": "Algae"               },
    {"R": 240, "G": 248, "B": 255, "ColorName": "Aliceblue"           },
    {"R": 254, "G": 179, "B":   8, "ColorName": "Amber"               },
    {"R": 250, "G": 235, "B": 215, "ColorName": "Antiquewhite"        },
    {"R": 110, "G": 203, "B":  60, "ColorName": "Apple"               },
    {"R": 255, "G": 177, "B": 109, "ColorName": "Apricot"             },
    {"R":  19, "G": 234, "B": 201, "ColorName": "Aqua"                },
    {"R": 127, "G": 255, "B": 212, "ColorName": "Aquamarine"          },
    {"R": 154, "G":  48, "B":   1, "ColorName": "Auburn"              },
    {"R": 144, "G": 177, "B":  52, "ColorName": "Avocado"             },
    {"R":  29, "G":  93, "B": 236, "ColorName": "Azul"                },
    {"R": 240, "G": 255, "B": 255, "ColorName": "Azure"               },
    {"R": 255, "G": 255, "B": 126, "ColorName": "Banana"              },
    {"R": 172, "G":  29, "B": 184, "ColorName": "Barney"              },
    {"R": 245, "G": 245, "B": 220, "ColorName": "Beige"               },
    {"R": 153, "G":  15, "B":  75, "ColorName": "Berry"               },
    {"R": 255, "G": 228, "B": 196, "ColorName": "Bisque"              },
    {"R":   0, "G":   0, "B":   0, "ColorName": "Black"               },
    {"R": 255, "G": 235, "B": 205, "ColorName": "Blanchedalmond"      },
    {"R": 175, "G": 168, "B": 139, "ColorName": "Bland"               },
    {"R": 119, "G":   0, "B":   1, "ColorName": "Blood"               },
    {"R":   0, "G":   0, "B": 255, "ColorName": "Blue"                },
    {"R": 138, "G":  43, "B": 226, "ColorName": "Blueviolet"          },
    {"R":  41, "G": 118, "B": 187, "ColorName": "Bluish"              },
    {"R":  85, "G":  57, "B": 204, "ColorName": "Blurple"             },
    {"R": 242, "G": 158, "B": 142, "ColorName": "Blush"               },
    {"R": 155, "G": 181, "B":  60, "ColorName": "Booger"              },
    {"R": 160, "G":  54, "B":  35, "ColorName": "Brick"               },
    {"R": 168, "G": 121, "B":   0, "ColorName": "Bronze"              },
    {"R": 165, "G":  42, "B":  42, "ColorName": "Brown"               },
    {"R": 126, "G":  64, "B": 113, "ColorName": "Bruise"              },
    {"R": 254, "G": 246, "B": 158, "ColorName": "Buff"                },
    {"R": 222, "G": 184, "B": 135, "ColorName": "Burlywood"           },
    {"R": 104, "G":  50, "B": 227, "ColorName": "Burple"              },
    {"R": 255, "G": 255, "B": 129, "ColorName": "Butter"              },
    {"R":  95, "G": 158, "B": 160, "ColorName": "Cadetblue"           },
    {"R": 198, "G": 159, "B":  89, "ColorName": "Camel"               },
    {"R": 127, "G": 143, "B":  78, "ColorName": "Camo"                },
    {"R": 253, "G": 255, "B":  99, "ColorName": "Canary"              },
    {"R": 175, "G": 111, "B":   9, "ColorName": "Caramel"             },
    {"R": 157, "G":   2, "B":  22, "ColorName": "Carmine"             },
    {"R": 193, "G": 253, "B": 149, "ColorName": "Celery"              },
    {"R": 165, "G": 163, "B": 145, "ColorName": "Cement"              },
    {"R": 222, "G":  12, "B":  98, "ColorName": "Cerise"              },
    {"R": 127, "G": 255, "B":   0, "ColorName": "Chartreuse"          },
    {"R": 207, "G":   2, "B":  52, "ColorName": "Cherry"              },
    {"R": 210, "G": 105, "B":  30, "ColorName": "Chocolate"           },
    {"R": 104, "G":   0, "B":  24, "ColorName": "Claret"              },
    {"R": 182, "G": 106, "B":  80, "ColorName": "Clay"                },
    {"R":  30, "G":  72, "B": 143, "ColorName": "Cobalt"              },
    {"R": 135, "G":  95, "B":  66, "ColorName": "Cocoa"               },
    {"R": 166, "G": 129, "B":  76, "ColorName": "Coffee"              },
    {"R": 182, "G":  99, "B":  37, "ColorName": "Copper"              },
    {"R": 255, "G": 127, "B":  80, "ColorName": "Coral"               },
    {"R": 100, "G": 149, "B": 237, "ColorName": "Cornflowerblue"      },
    {"R": 255, "G": 248, "B": 220, "ColorName": "Cornsilk"            },
    {"R": 255, "G": 255, "B": 194, "ColorName": "Cream"               },
    {"R": 255, "G": 255, "B": 182, "ColorName": "Creme"               },
    {"R": 220, "G":  20, "B":  60, "ColorName": "Crimson"             },
    {"R":   0, "G": 255, "B": 255, "ColorName": "Cyan"                },
    {"R":  27, "G":  36, "B":  49, "ColorName": "Dark"                },
    {"R":   0, "G":   0, "B": 139, "ColorName": "Darkblue"            },
    {"R":   0, "G": 139, "B": 139, "ColorName": "Darkcyan"            },
    {"R": 184, "G": 134, "B":  11, "ColorName": "Darkgoldenrod"       },
    {"R":   0, "G": 100, "B":   0, "ColorName": "Darkgreen"           },
    {"R": 169, "G": 169, "B": 169, "ColorName": "Darkgrey"            },
    {"R": 189, "G": 183, "B": 107, "ColorName": "Darkkhaki"           },
    {"R": 139, "G":   0, "B": 139, "ColorName": "Darkmagenta"         },
    {"R":  85, "G": 107, "B":  47, "ColorName": "Darkolivegreen"      },
    {"R": 255, "G": 140, "B":   0, "ColorName": "Darkorange"          },
    {"R": 153, "G":  50, "B": 204, "ColorName": "Darkorchid"          },
    {"R": 139, "G":   0, "B":   0, "ColorName": "Darkred"             },
    {"R": 233, "G": 150, "B": 122, "ColorName": "Darksalmon"          },
    {"R": 143, "G": 188, "B": 143, "ColorName": "Darkseagreen"        },
    {"R":  72, "G":  61, "B": 139, "ColorName": "Darkslateblue"       },
    {"R":  47, "G":  79, "B":  79, "ColorName": "Darkslategrey"       },
    {"R":   0, "G": 206, "B": 209, "ColorName": "Darkturquoise"       },
    {"R": 148, "G":   0, "B": 211, "ColorName": "Darkviolet"          },
    {"R": 255, "G":  20, "B": 147, "ColorName": "Deeppink"            },
    {"R":   0, "G": 191, "B": 255, "ColorName": "Deepskyblue"         },
    {"R":  59, "G":  99, "B": 140, "ColorName": "Denim"               },
    {"R": 204, "G": 173, "B":  96, "ColorName": "Desert"              },
    {"R": 105, "G": 105, "B": 105, "ColorName": "Dimgrey"             },
    {"R": 138, "G": 110, "B":  69, "ColorName": "Dirt"                },
    {"R":  30, "G": 144, "B": 255, "ColorName": "Dodgerblue"          },
    {"R": 130, "G": 131, "B":  68, "ColorName": "Drab"                },
    {"R":  78, "G":  84, "B": 129, "ColorName": "Dusk"                },
    {"R": 178, "G": 153, "B": 110, "ColorName": "Dust"                },
    {"R": 162, "G": 101, "B":  62, "ColorName": "Earth"               },
    {"R": 254, "G": 255, "B": 202, "ColorName": "Ecru"                },
    {"R": 207, "G": 175, "B": 123, "ColorName": "Fawn"                },
    {"R":  99, "G": 169, "B":  80, "ColorName": "Fern"                },
    {"R": 178, "G":  34, "B":  34, "ColorName": "Firebrick"           },
    {"R": 255, "G": 250, "B": 240, "ColorName": "Floralwhite"         },
    {"R":  11, "G":  85, "B":   9, "ColorName": "Forest"              },
    {"R":  34, "G": 139, "B":  34, "ColorName": "Forestgreen"         },
    {"R": 220, "G": 220, "B": 220, "ColorName": "Gainsboro"           },
    {"R": 248, "G": 248, "B": 255, "ColorName": "Ghostwhite"          },
    {"R": 255, "G": 215, "B":   0, "ColorName": "Gold"                },
    {"R": 245, "G": 191, "B":   3, "ColorName": "Golden"              },
    {"R": 218, "G": 165, "B":  32, "ColorName": "Goldenrod"           },
    {"R": 108, "G":  52, "B":  97, "ColorName": "Grape"               },
    {"R":  92, "G": 172, "B":  45, "ColorName": "Grass"               },
    {"R":   0, "G": 128, "B":   0, "ColorName": "Green"               },
    {"R": 173, "G": 255, "B":  47, "ColorName": "Greenyellow"         },
    {"R": 128, "G": 128, "B": 128, "ColorName": "Grey"                },
    {"R": 142, "G": 118, "B":  24, "ColorName": "Hazel"               },
    {"R": 240, "G": 255, "B": 240, "ColorName": "Honeydew"            },
    {"R": 255, "G": 105, "B": 180, "ColorName": "Hotpink"             },
    {"R": 214, "G": 255, "B": 250, "ColorName": "Ice"                 },
    {"R": 205, "G":  92, "B":  92, "ColorName": "Indianred"           },
    {"R":  75, "G":   0, "B": 130, "ColorName": "Indigo"              },
    {"R":  98, "G":  88, "B": 196, "ColorName": "Iris"                },
    {"R": 255, "G": 255, "B": 240, "ColorName": "Ivory"               },
    {"R":  31, "G": 167, "B": 116, "ColorName": "Jade"                },
    {"R": 240, "G": 230, "B": 140, "ColorName": "Khaki"               },
    {"R": 156, "G": 239, "B":  67, "ColorName": "Kiwi"                },
    {"R": 230, "G": 230, "B": 250, "ColorName": "Lavender"            },
    {"R": 255, "G": 240, "B": 245, "ColorName": "Lavenderblush"       },
    {"R": 124, "G": 252, "B":   0, "ColorName": "Lawngreen"           },
    {"R": 113, "G": 170, "B":  52, "ColorName": "Leaf"                },
    {"R": 253, "G": 255, "B":  82, "ColorName": "Lemon"               },
    {"R": 255, "G": 250, "B": 205, "ColorName": "Lemonchiffon"        },
    {"R": 143, "G": 182, "B": 123, "ColorName": "Lichen"              },
    {"R": 173, "G": 216, "B": 230, "ColorName": "Lightblue"           },
    {"R": 240, "G": 128, "B": 128, "ColorName": "Lightcoral"          },
    {"R": 224, "G": 255, "B": 255, "ColorName": "Lightcyan"           },
    {"R": 250, "G": 250, "B": 210, "ColorName": "Lightgoldenrodyellow"},
    {"R": 144, "G": 238, "B": 144, "ColorName": "Lightgreen"          },
    {"R": 211, "G": 211, "B": 211, "ColorName": "Lightgrey"           },
    {"R": 255, "G": 182, "B": 193, "ColorName": "Lightpink"           },
    {"R": 255, "G": 160, "B": 122, "ColorName": "Lightsalmon"         },
    {"R":  32, "G": 178, "B": 170, "ColorName": "Lightseagreen"       },
    {"R": 135, "G": 206, "B": 250, "ColorName": "Lightskyblue"        },
    {"R": 119, "G": 136, "B": 153, "ColorName": "Lightslategrey"      },
    {"R": 176, "G": 196, "B": 222, "ColorName": "Lightsteelblue"      },
    {"R": 255, "G": 255, "B": 224, "ColorName": "Lightyellow"         },
    {"R": 206, "G": 162, "B": 253, "ColorName": "Lilac"               },
    {"R": 196, "G": 142, "B": 253, "ColorName": "Liliac"              },
    {"R":   0, "G": 255, "B":   0, "ColorName": "Lime"                },
    {"R":  50, "G": 205, "B":  50, "ColorName": "Limegreen"           },
    {"R": 250, "G": 240, "B": 230, "ColorName": "Linen"               },
    {"R": 255, "G":   0, "B": 255, "ColorName": "Magenta"             },
    {"R": 244, "G": 208, "B":  84, "ColorName": "Maize"               },
    {"R": 255, "G": 166, "B":  43, "ColorName": "Mango"               },
    {"R":   4, "G":  46, "B":  96, "ColorName": "Marine"              },
    {"R": 128, "G":   0, "B":   0, "ColorName": "Maroon"              },
    {"R": 174, "G": 113, "B": 129, "ColorName": "Mauve"               },
    {"R": 102, "G": 205, "B": 170, "ColorName": "Mediumaquamarine"    },
    {"R":   0, "G":   0, "B": 205, "ColorName": "Mediumblue"          },
    {"R": 186, "G":  85, "B": 211, "ColorName": "Mediumorchid"        },
    {"R": 147, "G": 112, "B": 219, "ColorName": "Mediumpurple"        },
    {"R":  60, "G": 179, "B": 113, "ColorName": "Mediumseagreen"      },
    {"R": 123, "G": 104, "B": 238, "ColorName": "Mediumslateblue"     },
    {"R":   0, "G": 250, "B": 154, "ColorName": "Mediumspringgreen"   },
    {"R":  72, "G": 209, "B": 204, "ColorName": "Mediumturquoise"     },
    {"R": 199, "G":  21, "B": 133, "ColorName": "Mediumvioletred"     },
    {"R": 255, "G": 120, "B":  85, "ColorName": "Melon"               },
    {"R": 115, "G":   0, "B":  57, "ColorName": "Merlot"              },
    {"R":  25, "G":  25, "B": 112, "ColorName": "Midnightblue"        },
    {"R": 159, "G": 254, "B": 176, "ColorName": "Mint"                },
    {"R": 245, "G": 255, "B": 250, "ColorName": "Mintcream"           },
    {"R": 255, "G": 228, "B": 225, "ColorName": "Mistyrose"           },
    {"R": 255, "G": 228, "B": 181, "ColorName": "Moccasin"            },
    {"R": 157, "G": 118, "B":  81, "ColorName": "Mocha"               },
    {"R": 118, "G": 153, "B":  88, "ColorName": "Moss"                },
    {"R": 115, "G":  92, "B":  18, "ColorName": "Mud"                 },
    {"R": 255, "G": 222, "B": 173, "ColorName": "Navajowhite"         },
    {"R":   0, "G":   0, "B": 128, "ColorName": "Navy"                },
    {"R":   1, "G": 123, "B": 146, "ColorName": "Ocean"               },
    {"R": 191, "G": 155, "B":  12, "ColorName": "Ocher"               },
    {"R": 191, "G": 144, "B":   5, "ColorName": "Ochre"               },
    {"R": 198, "G": 156, "B":   4, "ColorName": "Ocre"                },
    {"R": 253, "G": 245, "B": 230, "ColorName": "Oldlace"             },
    {"R": 128, "G": 128, "B":   0, "ColorName": "Olive"               },
    {"R": 107, "G": 142, "B":  35, "ColorName": "Olivedrab"           },
    {"R": 255, "G": 165, "B":   0, "ColorName": "Orange"              },
    {"R": 255, "G":  69, "B":   0, "ColorName": "Orangered"           },
    {"R": 218, "G": 112, "B": 214, "ColorName": "Orchid"              },
    {"R": 255, "G": 249, "B": 208, "ColorName": "Pale"                },
    {"R": 238, "G": 232, "B": 170, "ColorName": "Palegoldenrod"       },
    {"R": 152, "G": 251, "B": 152, "ColorName": "Palegreen"           },
    {"R": 175, "G": 238, "B": 238, "ColorName": "Paleturquoise"       },
    {"R": 219, "G": 112, "B": 147, "ColorName": "Palevioletred"       },
    {"R": 255, "G": 239, "B": 213, "ColorName": "Papayawhip"          },
    {"R": 164, "G": 191, "B":  32, "ColorName": "Pea"                 },
    {"R": 255, "G": 176, "B": 124, "ColorName": "Peach"               },
    {"R": 255, "G": 218, "B": 185, "ColorName": "Peachpuff"           },
    {"R": 203, "G": 248, "B":  95, "ColorName": "Pear"                },
    {"R": 205, "G": 133, "B":  63, "ColorName": "Peru"                },
    {"R":   0, "G":  95, "B": 106, "ColorName": "Petrol"              },
    {"R":  43, "G":  93, "B":  52, "ColorName": "Pine"                },
    {"R": 255, "G": 192, "B": 203, "ColorName": "Pink"                },
    {"R": 252, "G": 134, "B": 170, "ColorName": "Pinky"               },
    {"R": 221, "G": 160, "B": 221, "ColorName": "Plum"                },
    {"R": 176, "G": 224, "B": 230, "ColorName": "Powderblue"          },
    {"R": 165, "G": 126, "B":  82, "ColorName": "Puce"                },
    {"R": 128, "G":   0, "B": 128, "ColorName": "Purple"              },
    {"R": 152, "G":  63, "B": 178, "ColorName": "Purply"              },
    {"R": 190, "G": 174, "B": 138, "ColorName": "Putty"               },
    {"R": 102, "G":  51, "B": 153, "ColorName": "Rebeccapurple"       },
    {"R": 255, "G":   0, "B":   0, "ColorName": "Red"                 },
    {"R": 254, "G": 134, "B": 164, "ColorName": "Rosa"                },
    {"R": 207, "G":  98, "B": 117, "ColorName": "Rose"                },
    {"R": 188, "G": 143, "B": 143, "ColorName": "Rosybrown"           },
    {"R": 171, "G":  18, "B":  57, "ColorName": "Rouge"               },
    {"R":  12, "G":  23, "B": 147, "ColorName": "Royal"               },
    {"R":  65, "G": 105, "B": 225, "ColorName": "Royalblue"           },
    {"R": 202, "G":   1, "B":  71, "ColorName": "Ruby"                },
    {"R": 161, "G":  57, "B":   5, "ColorName": "Russet"              },
    {"R": 168, "G":  60, "B":   9, "ColorName": "Rust"                },
    {"R": 139, "G":  69, "B":  19, "ColorName": "Saddlebrown"         },
    {"R": 135, "G": 174, "B": 115, "ColorName": "Sage"                },
    {"R": 250, "G": 128, "B": 114, "ColorName": "Salmon"              },
    {"R": 226, "G": 202, "B": 118, "ColorName": "Sand"                },
    {"R": 241, "G": 218, "B": 122, "ColorName": "Sandy"               },
    {"R": 244, "G": 164, "B":  96, "ColorName": "Sandybrown"          },
    {"R":  60, "G": 153, "B": 146, "ColorName": "Sea"                 },
    {"R":  46, "G": 139, "B":  87, "ColorName": "Seagreen"            },
    {"R": 255, "G": 245, "B": 238, "ColorName": "Seashell"            },
    {"R": 152, "G":  94, "B":  43, "ColorName": "Sepia"               },
    {"R": 160, "G":  82, "B":  45, "ColorName": "Sienna"              },
    {"R": 192, "G": 192, "B": 192, "ColorName": "Silver"              },
    {"R": 130, "G": 202, "B": 252, "ColorName": "Sky"                 },
    {"R": 135, "G": 206, "B": 235, "ColorName": "Skyblue"             },
    {"R":  81, "G": 101, "B": 114, "ColorName": "Slate"               },
    {"R": 106, "G":  90, "B": 205, "ColorName": "Slateblue"           },
    {"R": 112, "G": 128, "B": 144, "ColorName": "Slategrey"           },
    {"R": 255, "G": 250, "B": 250, "ColorName": "Snow"                },
    {"R":   0, "G": 255, "B": 127, "ColorName": "Springgreen"         },
    {"R":  10, "G":  95, "B":  56, "ColorName": "Spruce"              },
    {"R": 242, "G": 171, "B":  21, "ColorName": "Squash"              },
    {"R": 115, "G": 133, "B": 149, "ColorName": "Steel"               },
    {"R":  70, "G": 130, "B": 180, "ColorName": "Steelblue"           },
    {"R": 173, "G": 165, "B": 135, "ColorName": "Stone"               },
    {"R": 252, "G": 246, "B": 121, "ColorName": "Straw"               },
    {"R": 105, "G": 131, "B":  57, "ColorName": "Swamp"               },
    {"R": 210, "G": 180, "B": 140, "ColorName": "Tan"                 },
    {"R": 185, "G": 162, "B": 129, "ColorName": "Taupe"               },
    {"R": 101, "G": 171, "B": 124, "ColorName": "Tea"                 },
    {"R":   0, "G": 128, "B": 128, "ColorName": "Teal"                },
    {"R": 216, "G": 191, "B": 216, "ColorName": "Thistle"             },
    {"R": 255, "G":  99, "B":  71, "ColorName": "Tomato"              },
    {"R":  19, "G": 187, "B": 175, "ColorName": "Topaz"               },
    {"R": 199, "G": 172, "B": 125, "ColorName": "Toupe"               },
    {"R":  64, "G": 224, "B": 208, "ColorName": "Turquoise"           },
    {"R": 178, "G": 100, "B":   0, "ColorName": "Umber"               },
    {"R": 117, "G":   8, "B":  81, "ColorName": "Velvet"              },
    {"R": 238, "G": 130, "B": 238, "ColorName": "Violet"              },
    {"R": 245, "G": 222, "B": 179, "ColorName": "Wheat"               },
    {"R": 255, "G": 255, "B": 255, "ColorName": "White"               },
    {"R": 245, "G": 245, "B": 245, "ColorName": "Whitesmoke"          },
    {"R": 128, "G":   1, "B":  63, "ColorName": "Wine"                },
    {"R": 255, "G": 255, "B":   0, "ColorName": "Yellow"              },
    {"R": 154, "G": 205, "B":  50, "ColorName": "Yellowgreen"         }
]

def main():
    pygame.init()                                                   # initialize pygame
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))          # set display resolution
    pygame.display.set_caption("Color Square")                      # set window caption
    font = pygame.font.SysFont("monospace", 18)                     # set font
    clock = pygame.time.Clock()                                     # create a clock object to set FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)

        # Custom Draw
        colorIndex = 0
        for row in range(12):
            for col in range(19):
                colorEntry = getColor("Red")
                drawPaletteEntry(screen,    
                                 colorEntry["R"], 
                                 colorEntry["G"],
                                 colorEntry["B"],
                                 colorEntry["ColorName"],
                                 col * (COLOR_SIZE + 5), 
                                 row * (COLOR_SIZE + 5))
                colorIndex += 1

        pygame.display.flip()
        clock.tick(FPS)

def getColor(getThisColor):
    for color in COLOR_LIST:
        if color["ColorName"] == getThisColor:
            return color
    return None

def drawPaletteEntry(screen, redValue, greenValue, blueValue, colorName, coordinate_X, coordinate_Y):
    square_rect = pygame.Rect(coordinate_X, coordinate_Y, COLOR_SIZE, COLOR_SIZE)
    pygame.draw.rect(screen, (redValue, greenValue, blueValue), square_rect)


if __name__ == "__main__":
    main()