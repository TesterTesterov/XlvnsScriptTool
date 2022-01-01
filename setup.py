import sys
import cx_Freeze

base = None

if (sys.platform == 'win32'):
    base = "Win32GUI"


executables = [cx_Freeze.Executable("main.py",
                                    shortcut_name="XlvnsScriptTool",
                                    shortcut_dir="XlvnsScriptTool")]

cx_Freeze.setup(
        name="XlvnsScriptTool",
        version="1.0",
        description="Dual languaged (rus+eng) tool for compiling and decompiling SDT scripts of xlvns engine.\n"
                    "Двухязычное средство (рус+англ) для компиляции и декомпиляции скриптов SDT движка xlvns.",
        options={"build_exe": {"packages": []}},
        executables=executables
)
