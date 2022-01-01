# By Tester.

from gui_library.xlvns_script_tool_gui import XlvnsScriptToolGUI


debug = False


def test(mode):
    # decompile, compile
    from script_library.xlvns_script import XlvnsScriptDeCompiler
    file_base = "SCN095"
    sdt_file = file_base + ".SDT"
    txt_file = file_base + ".txt"
    if mode == "decompile":
        new_script = XlvnsScriptDeCompiler(sdt_file_name=sdt_file, txt_file_name=txt_file,
                                           verbose=True, version=(76, 70))
        new_script.decompile()
        del new_script
    elif mode == "decompile_for_hack":
        new_script = XlvnsScriptDeCompiler(sdt_file_name=sdt_file, txt_file_name=txt_file,
                                           verbose=True, hacker_mode=True)
        new_script.decompile()
        del new_script
    elif mode == "compile":
        new_script = XlvnsScriptDeCompiler(sdt_file_name=sdt_file, txt_file_name=txt_file,
                                           verbose=True, version=(76, 70))
        new_script.compile()
        del new_script
    else:
        print("Incorrect mode!/Некорретный режим!")


def main():
    gui = XlvnsScriptToolGUI()


if __name__ == '__main__':
    if debug:
        test("compile")
    else:
        main()
