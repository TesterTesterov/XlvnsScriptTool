import json
from .version_lib import XvlnsScriptBase


class XlvnsScriptDeCompiler:
    default_sdt_encoding = "cp932"
    default_txt_encoding = "cp932"
    default_extension = "PDT"
    default_version = (0, 0)

    free_bytes_def = "#0"
    command_def = "#1"
    label_def = "#2"
    split_def = "-"
    comment_def = "$"

    def __init__(self, sdt_file_name: str, txt_file_name: str, version: tuple = (0, 0),
                 sdt_encoding: str = "", txt_encoding: str = "", verbose: bool = False,
                 hacker_mode: bool = False):
        self.sdt_file_name = sdt_file_name
        self.txt_file_name = txt_file_name
        self.version = version
        if sdt_encoding == "":
            self.sdt_encoding = self.default_sdt_encoding  # Sdt file encoding.
        else:
            self.sdt_encoding = sdt_encoding
        if txt_encoding == "":
            self.txt_encoding = self.default_txt_encoding  # Txt file encoding.
        else:
            self.txt_encoding = txt_encoding

        self._script_lib = XvlnsScriptBase.get_script_from_version(self.version)
        self._verbose = verbose
        self._hacker_mode = hacker_mode

    # User methods.

    def decompile(self) -> None:
        """Decompile this PDT script."""
        with open(self.sdt_file_name, "rb") as sdt_file, open(self.txt_file_name, "w",
                                                              encoding=self.txt_encoding) as txt_file:
            if not self._script_lib:
                ver = XvlnsScriptBase.get_version(sdt_file)
                self._script_lib = XvlnsScriptBase.get_script_from_version(ver)
            else:
                self._script_lib.prepare()
            ver, prm = self._script_lib.decompile_header(sdt_file)
            if self._verbose:
                print("Version/Версия:", ver)
                print("Parameters/Параметры:", prm)
            sdt_file.seek(self._script_lib.to_true_offset(0), 0)
            if not self._hacker_mode or True:
                self._decompile_offsets(sdt_file)
            if self._verbose:
                print("Offsets/Смещения:", self._script_lib.found_offsets)
            sdt_file.seek(self._script_lib.to_true_offset(0), 0)
            self._decompile_commands(sdt_file, txt_file)

    def compile(self) -> None:
        """Compile this PDT script."""
        self._script_lib.prepare()
        with open(self.sdt_file_name, "wb") as sdt_file, open(self.txt_file_name, "r",
                                                              encoding=self.txt_encoding) as txt_file:
            txt_file.seek(0, 0)
            self._compile_parameters(sdt_file, txt_file)
            if self._verbose:
                print("Offsets:", self._script_lib.found_offsets)
                print("Offsets indexes:", self._script_lib.offsets_indexes)
            txt_file.seek(0, 0)
            self._compile_commands(sdt_file, txt_file)

    # Compilation methods.

    def _compile_commands(self, sdt_file, txt_file) -> None:
        while True:
            new_line = txt_file.readline()
            if not new_line:
                break
            this_line_def = new_line.split(self.split_def)
            if this_line_def[0] == self.comment_def:
                continue
            elif this_line_def[0] == self.free_bytes_def:
                new_bytes = bytes.fromhex(this_line_def[1])
                sdt_file.write(new_bytes)
            elif this_line_def[0] == self.command_def:
                this_command = this_line_def[1].rstrip()
                this_entry = self._script_lib.get_command_entry(this_command)
                sdt_file.write(bytes.fromhex(this_entry[0]))

                these_args = json.loads(self.read_args_string(txt_file))
                these_args = self._script_lib.pack_offsets(this_entry[0], these_args)
                these_args = self._script_lib.ass_counter_manage(this_entry[0], these_args)
                new_args = self._script_lib.pack_args(these_args, this_entry[1], self.sdt_encoding)
                sdt_file.write(new_args)

    def _compile_parameters(self, sdt_file, txt_file) -> None:
        """Compile the game parameters."""

        pointer = self._script_lib.to_true_offset(0)
        while True:
            new_line = txt_file.readline()
            if not new_line:
                break
            this_line_def = new_line.split(self.split_def)
            if this_line_def[0] == self.comment_def:
                continue
            elif this_line_def[0] == self.free_bytes_def:
                new_bytes = bytes.fromhex(this_line_def[1])
                pointer += len(new_bytes)
            elif this_line_def[0] == self.command_def:
                this_command = this_line_def[1].rstrip()
                pointer += 2

                this_entry = self._script_lib.get_command_entry(this_command)
                these_args = json.loads(self.read_args_string(txt_file))
                these_args = self._script_lib.counter_safe(this_entry[0], these_args)
                new_args = self._script_lib.pack_args(these_args, this_entry[1], self.sdt_encoding)
                pointer += len(new_args)
            elif this_line_def[0] == self.label_def:
                this_offset_index = int(this_line_def[1])
                self._script_lib.append_offsets_with_index(pointer, this_offset_index)

        sdt_file.write(self._script_lib.get_header_bytes(self.version, pointer))

    # Decompilation methods.

    def _decompile_commands(self, sdt_file, txt_file) -> None:
        """Decompile SDT script commands."""

        new_bytes_flag = False

        while True:
            pointer = sdt_file.tell()

            # Offsets management.

            offset_index = self._script_lib.find_offset_index(pointer)
            if offset_index != -1:
                if new_bytes_flag:
                    txt_file.write("\n")
                    new_bytes_flag = False
                txt_file.write("{0}{1}{2}".format(self.label_def, self.split_def, str(offset_index)))
                if self._verbose:
                    txt_file.write("{0}{1}".format(self.split_def, str(pointer)))
                txt_file.write("\n")

            # Commands management.

            new_word = sdt_file.read(2)
            if new_word == b'':
                break
            new_word = new_word.hex(' ')
            this_entry = self._script_lib.get_command_entry(new_word)

            if this_entry:
                if new_bytes_flag:
                    txt_file.write("\n")
                    new_bytes_flag = False

                if this_entry[2]:
                    new_word = this_entry[2]
                txt_file.write("{0}{1}{2}".format(self.command_def, self.split_def, new_word))
                if self._hacker_mode:
                    txt_file.write("{0}{1}".format(self.split_def, str(pointer)))
                txt_file.write("\n")

                arguments = self._script_lib.extract_args(sdt_file, this_entry[1], self.sdt_encoding)
                arguments = self._script_lib.diss_counter_manage(this_entry[0], arguments)
                arguments = self._script_lib.extract_offsets(this_entry[0], arguments)
                json.dump(arguments, txt_file, ensure_ascii=False, indent=4)
                txt_file.write("\n")

            else:
                if not new_bytes_flag:
                    new_bytes_flag = True
                    txt_file.write(self.free_bytes_def)
                txt_file.write(self.split_def)
                if " " not in new_word:
                    txt_file.write(new_word)
                else:
                    txt_file.write(new_word.split(' ')[0])
                    sdt_file.seek(-1, 1)

    def _decompile_offsets(self, sdt_file):
        """Decompile offsets from scripts."""
        while True:
            new_word = sdt_file.read(2)
            if new_word == b'':
                break
            new_word = new_word.hex(' ')
            this_entry = self._script_lib.get_command_entry(new_word)
            if this_entry:
                arguments = self._script_lib.extract_args(sdt_file, this_entry[1], self.sdt_encoding)
                self._script_lib.extract_offsets(new_word, arguments)
            else:
                if " " in new_word:
                    sdt_file.seek(-1, 1)

    # Some extra technical methods.

    def read_args_string(self, input_file) -> str:
        """Read string of the arguments."""
        out_string = ''
        while True:
            new_string = input_file.readline()
            out_string += new_string
            stripper_string = new_string.rstrip()
            if len(new_string) == 0:
                break
            if new_string[0] == self.comment_def:
                continue
            if stripper_string == ']' or stripper_string == '[]':
                break
        return out_string
