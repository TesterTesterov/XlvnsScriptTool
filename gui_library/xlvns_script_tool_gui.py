import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror
from .silky_mes_gui import SilkyMesGUI
from script_library.xlvns_script import XlvnsScriptDeCompiler
from script_library.version_lib import XvlnsScriptBase


class XlvnsScriptToolGUI(SilkyMesGUI):
    ver_sep = ":   "

    _strings_lib = {
        "eng": (
            "XlvnsScriptTool by Tester",  # 0
            "Single file",
            "Directory",
            "Enter a name of the .SDT file:",
            "Enter a name of the directory with .SDT files:",
            "Enter a title of the .txt file:",  # 5
            "Enter a name of the directory with .txt files:",
            "All files",
            "Xlvns SDT scripts",
            "Choice of SDT script",
            "Choice of directory with SDT scripts",  # 10
            "Text files",
            "Choice of directory with txt files",
            "Choice of text file",
            "Commands:",
            "Status:",  # 15
            "Help:",
            "Common help",
            "Usage help",
            "Breaks help",
            "Decompile",  # 20
            "Compile",
            "Warning",
            "File SDT or a directory of them is not chosen.",
            "File txt or a directory of them is not chosen.",
            "Managing files...",  # 25
            "Error",
            "Decompilation failed. ",
            "Decompilation succeed. ",
            "Compilation failed. ",
            "Compilation succeed. ",  # 30
            "Choose the script version:",
        ),
        "rus": (
            "XlvnsScriptTool от Tester-а",  # 0
            "По файлами",
            "По папкам",
            "Введите название файла .SDT:",
            "Введите название директории с файлами .SDT:",
            "Введите название файла .txt:",  # 5
            "Введите название директории с файлами .txt:",
            "Все файлы",
            "Скрипты SDT xlvns",
            "Выбор скрипта SDT",
            "Выбор директории со скриптами SDT",  # 10
            "Текстовые файлы",
            "Выбор директории с файлами txt",
            "Выбор текстового файла",
            "Команды:",
            "Статус:",  # 15
            "Справка:",
            "Общая справка",
            "Справка о использовании",
            "Справка о переносах",
            "Декомпилировать",  # 20
            "Компилировать",
            "Предупреждение",
            "Файл SDT или их директория не выбраны",
            "Файл txt или их директория не выбраны",
            "Обрабатываем файлы...",  # 25
            "Ошибка",
            "Декомпиляция не удалась. ",
            "Декомпиляция удалась. ",
            "Компиляция не удалась. ",
            "Компиляция удалась. ",  # 30
            "Выберите версию скриптов:",
        )
    }

    common_help = {
        'eng': """
 Dual languaged (rus+eng) tool for decompiling and compiling (actually, this tool is more than just (dis)assenbler, but less than (de)compiler) scripts .SDT from the visual novel's engine xlvns. It mostly used in [Leaf](https://vndb.org/p21) and [Aquaplus](https://vndb.org/p87) games, albeit not all. With it thou can fully edit all the code, not just strings. Thou can add message breaks and change scenarios without restrictions!

Definations: "#0-" are "free bytes", "#1-" are commands (and "\[...]" are arguments below), "#2-" are labels.
    """,
        'rus': """
 Двуязычное (рус+англ) средство для декомпиляции и компиляции (на самом деле, сие средство имеет больше функционала, чем у простых дизассемблеров, но при это меньше, чем у декомпиляторов) скриптов .mes движка визуальных новелл xlvns. В основном он используется в играх [Leaf](https://vndb.org/p21) и [Aquaplus](https://vndb.org/p87), хоть и не всех. С ним вы можете полностью редактирвоать код, а не только строки; по вашему повелению добавлять разрывы между сообщений и даже менять сценарии по своему замыслу!
  
 Определения: "#0-" есть "вольные байты", "#1-" есть команды (и под ними "\[...]" аргументы), "#2-" есть метки.
    """
    }
    usage_help = {
        'eng': """
1. Choose the mode, file or directory. In first mode you will work with one .mes - .txt pair, in second -- with all files in a pair of directories.
2. Enter a name of the .mes file in the top entry (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
3. Enter a name of the .txt file (do see, with extension) or the directory name. Thou can also enter relative or absolute path. You can also click on "..." to choose.
4. Choose the script version.
5. To decompile push the button "Decompile".
6. To compile push the button "Compile".
7. Status will be displayed on the text area below.
    """,
        'rus': """
1. Выберите режим: файл или директорию. В первом вы будете работать с парой .mes - .txt, во втором -- со всеми файлами в паре директорий.
2. Введите название файла .mes в верхней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
3. Введите название файла .txt в нижней форме (заметьте, с расширением) или имя директории. Также можно вводить относительный или абсолютный до него путь. Также вы можете нажать на кнопку "...", чтобы выбрать.
4. Выберите версию скрипта.
5. Для декомпиляции нажмите на кнопку "Декомпилировать".
6. Для компиляции нажмите на кнопку "Компилировать".
7. Статус сих операций будет отображаться на текстовом поле ниже.
    """,
    }
    breaks_help = {
        'eng': """
For line break add "\\n" special symbol in the string, to message break -- "\\k".
If by any chance message break did not work, append new message command, as showed below. (Insert your string instead of \<Somestring\>).

#1-MESSAGE
[
    "<Somestring>",
    2,
    "*MESSAGE_NUM*"
]

    """,
        'rus': """

Для переноса по строкам добавьте в строку спецсимвол "\\n", для переноса по сообщениям -- "\\k".
Если перенос по сообещниям почему-то не сработал, просто добавьте новую команду сообщения, как показано ниже. (Вместо \<Какая-то строка\> введите вашу строку).

#1-MESSAGE
[
    "<Какая-то строка>",
    2,
    "*MESSAGE_NUM*"
]

    """
    }

    def __init__(self, **kwargs):
        self._flag_block = True
        super().__init__(**kwargs)
        self._flag_block = False

        self._version_lbl = tk.Label(master=self._root,
                                     bg='white',
                                     font=('Helvetica', 12))
        self._version_lbl.lang_index = 31

        self._version = tk.StringVar()

        possible_versions = [self.ver_sep.join(map(str, i)) for i in XvlnsScriptBase.supported_versions]
        self._version_cmb = ttk.Combobox(
            master=self._root,
            font=('Helvetica', 12),
            textvariable=self._version,
            values=possible_versions,
            state="readonly",
        )
        if possible_versions:
            self._version.set(possible_versions[0])

        self._init_strings()
        self.place_widgets()
        self.start_gui()

    def place_widgets(self) -> None:
        """Place widgets of the GUI."""
        if self._flag_block:
            return
        # Top buttons.
        self._rus_btn.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=0.05)
        self._eng_btn.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.05)

        # Input/output files/dirs choosers widgets.

        for num, widget in enumerate(self._mode_rdb):
            widget.place(relx=0.5 * num, rely=0.05, relwidth=0.5, relheight=0.05)
        self._mes_point_lbl.place(relx=0.0, rely=0.1, relwidth=1.0, relheight=0.05)
        self._mes_name_ent.place(relx=0.0, rely=0.15, relwidth=0.9, relheight=0.05)
        self._mes_find_btn.place(relx=0.9, rely=0.15, relwidth=0.1, relheight=0.05)
        self._txt_point_lbl.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.05)
        self._txt_name_ent.place(relx=0.0, rely=0.25, relwidth=0.9, relheight=0.05)
        self._txt_find_btn.place(relx=0.9, rely=0.25, relwidth=0.1, relheight=0.05)

        self._version_lbl.place(relx=0.0, rely=0.3, relwidth=1.0, relheight=0.05)
        self._version_cmb.place(relx=0.0, rely=0.35, relwidth=1.0, relheight=0.05)

        # Commands.

        for widget in self._action_btn:
            widget.pack(fill=tk.X)

        # Text area.

        self._status_txt.pack()

        # Help buttons.

        self._common_help_btn.pack(fill=tk.X)
        self._usage_help_btn.pack(fill=tk.X)
        self._breaks_help_btn.pack(fill=tk.X)

        # And finally label frames.

        self._commands_lfr.place(relx=0.0, rely=0.4, relwidth=1.0, relheight=0.2)
        self._status_lfr.place(relx=0.0, rely=0.6, relwidth=1.0, relheight=0.15)
        self._help_lfr.place(relx=0.0, rely=0.75, relwidth=1.0, relheight=0.25)

    def start_gui(self) -> None:
        """Start the GUI."""
        if self._flag_block:
            return
        # To make more space for patching.
        self._root.mainloop()

    #  Compiling and decompiling methods.

    def _disassemble(self) -> bool:
        """Decompile a script or a group of them to a text file or a group of them"""
        script_file, txt_file, status = self._get_mes_and_txt()
        if not status:
            return False

        self._lock_activity()
        if self._input_mode.get() == 0:  # File mode.
            self._unlocker_count = 1
            new_thread = threading.Thread(daemon=False, target=self._disassemble_this_script,
                                          args=(script_file, txt_file))
            new_thread.start()
        else:  # Dir mode.
            files_to_manage = []
            os.makedirs(txt_file, exist_ok=True)
            for root, dirs, files in os.walk(script_file):
                for file_name in files:
                    new_file_array = []  # script_file, txt_file

                    basic_path = os.sep.join(os.path.join(root, file_name).split(os.sep)[1:])
                    rel_script_name = os.path.normpath(os.path.join(script_file, basic_path))
                    rel_txt_name = os.path.normpath(os.path.join(txt_file, os.path.splitext(basic_path)[0] + ".txt"))

                    new_file_array.append(rel_script_name)
                    new_file_array.append(rel_txt_name)
                    files_to_manage.append(new_file_array)

            self._unlocker_count = len(files_to_manage)
            for file_mes, file_txt in files_to_manage:
                new_thread = threading.Thread(daemon=False, target=self._disassemble_this_script,
                                              args=(file_mes, file_txt))
                new_thread.start()

        return True

    def _disassemble_this_script(self, script_file: str, txt_file: str) -> None:
        """Decompile this script."""
        try:
            self._thread_semaphore.acquire()
            script_mes = XlvnsScriptDeCompiler(sdt_file_name=script_file,
                                               txt_file_name=txt_file)
            script_mes.decompile()
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, script_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][28])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
            self._print_lock.acquire()
            print("Disassembling of {0} succeed./Дизассемблирование {0} прошло успешно.".format(script_file))
            self._print_lock.release()
        except Exception as ex:
            self._print_lock.acquire()
            print("Disassembling of {0} error./Дизассемблирование {0} не удалось.".format(script_file))
            self._print_lock.release()
            showerror(title=self._strings_lib[self._language][26], message=str(ex))
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, script_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][27])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
        finally:
            self._count_lock.acquire()
            self._unlocker_count -= 1
            self._count_lock.release()
            if self._unlocker_count == 0:
                self._unlock_activity()
            self._thread_semaphore.release()

    def _assemble(self) -> bool:
        """Compile a script or a group of them from the text file or a group of them"""
        script_file, txt_file, status = self._get_mes_and_txt()
        if not status:
            return False

        self._lock_activity()
        if self._input_mode.get() == 0:  # File mode.
            self._unlocker_count = 1
            new_thread = threading.Thread(daemon=False, target=self._assemble_this_script,
                                          args=(script_file, txt_file))
            new_thread.start()
        else:  # Dir mode.
            files_to_manage = []
            os.makedirs(txt_file, exist_ok=True)
            for root, dirs, files in os.walk(txt_file):
                for file_name in files:
                    new_file_array = []  # mes_file, txt_file

                    basic_path = os.sep.join(os.path.join(root, file_name).split(os.sep)[1:])
                    rel_script_name = os.path.normpath(os.path.join(script_file, os.path.splitext(basic_path)[0]
                                                                    + ".SDT"))
                    rel_txt_name = os.path.normpath(os.path.join(txt_file, basic_path))

                    new_file_array.append(rel_script_name)
                    new_file_array.append(rel_txt_name)
                    files_to_manage.append(new_file_array)

                    # Why did I not initiate file management right away, thou ask?

            self._unlocker_count = len(files_to_manage)  # ...That is the answer.
            for file_mes, file_txt in files_to_manage:
                new_thread = threading.Thread(daemon=False, target=self._assemble_this_script,
                                              args=(file_mes, file_txt))
                new_thread.start()

        return True

    def _assemble_this_script(self, mes_file: str, txt_file: str) -> None:
        """Compile this script."""
        try:
            version_tuple = eval(self._version.get().split(self.ver_sep)[0])
            self._thread_semaphore.acquire()
            script_mes = XlvnsScriptDeCompiler(mes_file, txt_file, version=version_tuple)
            script_mes.compile()
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][30])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
            self._print_lock.acquire()
            print("Assembling of {0} succeed./Ассемблирование {0} прошло успешно.".format(mes_file))
            self._print_lock.release()
        except Exception as ex:
            self._print_lock.acquire()
            print("Assembling of {0} error./Ассемблирование {0} не удалось.".format(mes_file))
            self._print_lock.release()
            showerror(title=self._strings_lib[self._language][26], message=str(ex))
            self._status_lock.acquire()
            self._status_txt["state"] = tk.NORMAL
            self._status_txt.delete(1.0, tk.END)
            self._status_txt.insert(1.0, mes_file + ": ")
            self._status_txt.insert(2.0, self._strings_lib[self._language][29])
            self._status_txt["state"] = tk.DISABLED
            self._status_lock.release()
        finally:
            self._count_lock.acquire()
            self._unlocker_count -= 1
            self._count_lock.release()
            if self._unlocker_count == 0:
                self._unlock_activity()
            self._thread_semaphore.release()

    # Choose input/output files/dirs.

    def _change_input_mode(self) -> None:
        """Change of mode of the input: text or directory."""
        indexer = self._input_mode.get()
        self._mes_point_lbl.lang_index = 3 + indexer
        self._txt_point_lbl.lang_index = 5 + indexer
        if indexer == 0 and indexer != self._last_indexer:  # Filenames now.
            self._mes_file.set("")
            self._txt_file.set("")
        else:
            self._mes_file.set(os.path.splitext(self._mes_file.get())[0])
            self._txt_file.set(os.path.splitext(self._txt_file.get())[0])
        self._last_indexer = indexer
        self._init_strings()

    # File file.

    def _find_mes(self) -> None:
        """Find mes file or a directory with them."""
        if self._input_mode.get() == 0:  # File mode.
            file_types = [(self._strings_lib[self._language][8], '*.SDT'),
                          (self._strings_lib[self._language][7], '*')]
            file_name = askopenfilename(filetypes=file_types, initialdir=os.getcwd(),
                                        title=self._strings_lib[self._language][9])
            if file_name:
                file_name = os.path.normpath(file_name)
                relpath = os.path.relpath(file_name, os.getcwd())
                end_arc = file_name
                if relpath.count(os.sep) < file_name.count(os.sep):
                    end_arc = relpath
                self._mes_file.set(end_arc)
                if self._txt_file.get() == "":
                    self._txt_file.set(os.path.splitext(end_arc)[0] + ".txt")
        else:  # Dir mode.
            dir_name = askdirectory(initialdir=os.getcwd(), title=self._strings_lib[self._language][10])
            if dir_name:
                dir_name = os.path.normpath(dir_name)
                relpath = os.path.relpath(dir_name, os.getcwd())
                end_dir = dir_name
                if relpath.count(os.sep) < dir_name.count(os.sep):
                    end_dir = relpath
                self._mes_file.set(end_dir)

    def _find_txt(self) -> None:
        """Find txt file or a directory with them."""
        if self._input_mode.get() == 0:  # File mode.
            file_types = [(self._strings_lib[self._language][1], '*.txt'),
                          (self._strings_lib[self._language][7], '*')]
            file_name = askopenfilename(filetypes=file_types, initialdir=os.getcwd(),
                                        title=self._strings_lib[self._language][13])
            if file_name:
                file_name = os.path.normpath(file_name)
                relpath = os.path.relpath(file_name, os.getcwd())
                end_arc = file_name
                if relpath.count(os.sep) < file_name.count(os.sep):
                    end_arc = relpath
                self._txt_file.set(end_arc)
                if self._mes_file.get() == "":
                    self._mes_file.set(os.path.splitext(end_arc)[0] + ".SDT")
        else:  # Dir mode.
            dir_name = askdirectory(initialdir=os.getcwd(), title=self._strings_lib[self._language][12])
            if dir_name:
                dir_name = os.path.normpath(dir_name)
                relpath = os.path.relpath(dir_name, os.getcwd())
                end_dir = dir_name
                if relpath.count(os.sep) < dir_name.count(os.sep):
                    end_dir = relpath
                self._txt_file.set(end_dir)
