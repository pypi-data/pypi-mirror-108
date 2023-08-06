import os
import sys

sys.path.append(os.path.dirname(__file__))
dirname = os.path.dirname(__file__)

DARK = None
LIGHT = None
with open(os.path.join(dirname, "compiled/dark.qss")) as f:
    DARK = f.read()
with open(os.path.join(dirname, "compiled/light.qss")) as f:
    LIGHT = f.read()


# Return QSS stylesheet for dark theme
def dark(hot_reload=False):
    from compiled import qtstylish_rc
    if hot_reload:
        compile()
    return DARK


# Return QSS stylesheet for light theme
def light(hot_reload=False):
    from compiled import qtstylish_rc
    if hot_reload:
        compile()
    return LIGHT


def compile():
    import qtsass
    # Compile SCSS into QSS
    qtsass.compile_filename(os.path.join(dirname, "stylesheets/dark.scss"),
                            os.path.join(dirname, "compiled/dark.qss"))
    qtsass.compile_filename(os.path.join(dirname, "stylesheets/light.scss"),
                            os.path.join(dirname, "compiled/light.qss"))
    # Compile resources defined by style.qrc into a python module
    os.system("pyrcc5 ./stylesheets/main.qrc -o ./compiled/qtstylish_rc.py")
    # This part is for hot reload
    with open(os.path.join(dirname, "compiled/dark.qss")) as f:
        global DARK
        DARK = f.read()
    with open(os.path.join(dirname, "compiled/light.qss")) as f:
        global LIGHT
        LIGHT = f.read()


if __name__ == "__main__":
    compile()
