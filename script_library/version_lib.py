import struct


class XvlnsScriptBase:
    stop_def = "*STOP*"
    continue_def = "*CONTINUE*"
    struct_def = "*STRUCT*"
    f_struct_def = "*F_STRUCT*"

    supported_versions = (
        ((76, 70), "Shizuku: Renewal etc."),
    )

    script_padding = 1032
    default_prms = (1, 0)

    script_library = tuple()
    struct_library = (
        ("00", "I", "UINT"),
        ("01", "i", "INT"),
        ("02", "s", "STR"),
    )
    # Command, struct, name.
    offsets_library = tuple()
    # Command, index.
    counter_library = (
        ("c4 00", 2, "MESSAGE_NUM", 1),
    )
    # Command, index, name, starts.

    command_instances = {
        'I': ('I', 'i'),
        'H': ('H', 'h'),
        'B': ('B', 'b'),
        'S': ('S', 's'),
        'C': ('C'),
        'K': ('K'),
        'F': ('F'),
    }

    def __init__(self):
        self.found_offsets = []
        self.offsets_indexes = []
        self.counters = []
        self.prepare()

    # Preparation methods.

    def prepare(self) -> None:
        """Get it ready."""
        self.clear_offsets()
        self.counters_initialize()

    # Counter methods.

    def counters_initialize(self) -> None:
        """Initialize counters."""
        for count_entry in self.counter_library:
            self.counters.append(count_entry[3])

    def counter_safe(self, command: str, args: list) -> list:
        """Manage counters while decompiling."""
        for num, counter_entry in enumerate(self.counter_library):
            if command == counter_entry[0]:
                args[counter_entry[1]] = 0
                break
        return args

    def diss_counter_manage(self, command: str, args: list) -> list:
        """Manage counters while decompiling."""
        for num, counter_entry in enumerate(self.counter_library):
            if command == counter_entry[0]:
                args[counter_entry[1]] = "*{}*".format(counter_entry[2])
                break
        return args

    def ass_counter_manage(self, command: str, args: list) -> list:
        """Manage counters while compiling."""
        for num, counter_entry in enumerate(self.counter_library):
            if command == counter_entry[0]:
                args[counter_entry[1]] = self.counters[num]
                self.counters[num] += 1
                break
        return args

    # Offsets methods.

    def append_offsets_with_index(self, offset: int, index: int) -> None:
        self.found_offsets.append(offset)
        self.offsets_indexes.append(index)

    def extract_offsets(self, command: str, args: list) -> list:
        """Extract offset from the commands."""
        for offseter in self.offsets_library:
            if command == offseter[0]:
                for zlo in offseter[1]:
                    new_offset = self.to_true_offset(args[zlo])
                    if new_offset in self.found_offsets:
                        args[zlo] = self.found_offsets.index(new_offset)
                    else:
                        args[zlo] = len(self.found_offsets)
                        self.found_offsets.append(new_offset)
                break
        return args

    def pack_offsets(self, command: str, args: list) -> list:
        """Extract offset from the commands."""
        for offseter in self.offsets_library:
            if command == offseter[0]:
                for zlo in offseter[1]:
                    new_offset_index = args[zlo]
                    new_offset = self.to_script_offset(self.found_offsets[self.offsets_indexes.index(new_offset_index)])
                    args[zlo] = new_offset
                break
        return args

    def clear_offsets(self) -> None:
        """Clear found offsets."""
        self.found_offsets.clear()
        self.offsets_indexes.clear()

    def to_script_offset(self, offset) -> int:
        """Convert true offset to script offset."""
        return offset - self.script_padding

    def to_true_offset(self, offset) -> int:
        """Convert script offset to true offset."""
        return offset + self.script_padding

    def find_offset_index(self, offset) -> int:
        """Get an index of the offset or -1."""
        for offset_number, possible_offset in enumerate(self.found_offsets):
            if offset == possible_offset:
                return offset_number
        return -1

    # Common command methods.

    @classmethod
    def get_command_entry(cls, command: str) -> tuple:
        """Get the entry of the current command."""
        for entry in cls.script_library:
            if (entry[0] == command) or (entry[2] == command):
                return entry
        return None

    @classmethod
    def get_struct_entry(cls, structure: str) -> tuple:
        """Get the entry of the current struct."""
        for entry in cls.struct_library:
            if (entry[0] == structure) or (entry[2] == structure):
                return entry
        return None

    # Arguments packing methods.

    def pack_args(self, argument_list: list, args: str, encoding: str) -> bytes:
        args_bytes = b''

        for val, arg in zip(argument_list, args):
            if arg in self.command_instances['I']:
                args_bytes += self.set_I(val, arg)
            elif arg in self.command_instances['H']:
                args_bytes += self.set_H(val, arg)
            elif arg in self.command_instances['B']:
                args_bytes += self.set_B(val, arg)
            elif arg in self.command_instances['S']:
                args_bytes += self.set_S(val, arg, encoding)
            elif arg in self.command_instances['C']:
                args_bytes += self.set_C(val, encoding)
            elif arg in self.command_instances['K']:
                if val == self.stop_def:
                    break

        return args_bytes

    def set_C(self, arguments: list, encoding: str) -> bytes:
        """Pack a code structure."""
        arguments.pop(0)  # STRUCT.

        new_struct = arguments[0]
        new_entry = self.get_struct_entry(new_struct)
        if new_entry is None:
            raise XlvnsScriptError("Incorrect struct: {}!".format(new_struct))

        arg_bytes = bytes.fromhex(new_entry[0])
        arg_bytes += self.pack_args(arguments[1], new_entry[1], encoding)

        return arg_bytes

    @staticmethod
    def set_B(arguments: int, command: str) -> bytes:
        """Pack B-struct."""
        return struct.pack(command, arguments)

    @staticmethod
    def set_H(arguments: int, command: str) -> bytes:
        """Pack H-structs."""
        return struct.pack(command, arguments)

    @staticmethod
    def set_I(arguments: int, command: str) -> bytes:
        """Pack I-structs."""
        return struct.pack(command, arguments)

    @staticmethod
    def set_S(arguments: str, command: str, encoding: str) -> bytes:
        """Pack string structs."""
        arg_bytes = arguments.encode(encoding)
        lenner = b''
        if command == "s":
            lenner = struct.pack("B", len(arg_bytes))
        elif command == "S":
            lenner = struct.pack("H", len(arg_bytes))
        arg_bytes = lenner + arg_bytes
        return arg_bytes

    # Arguments extraction methods.

    def extract_args(self, in_file, args: str, encoding: str) -> list:
        """Extract arguments from the file."""
        arg_list = []
        for arg in args:
            if arg in self.command_instances['I']:
                arg_list.append(self.get_I(in_file, arg))
            elif arg in self.command_instances['H']:
                arg_list.append(self.get_H(in_file, arg))
            elif arg in self.command_instances['B']:
                arg_list.append(self.get_B(in_file, arg))
            elif arg in self.command_instances['S']:
                result = self.get_S(arg, in_file, encoding)
                arg_list.append(result)
            elif arg in self.command_instances['C']:
                result = self.get_C(in_file, encoding)
                arg_list.append(result)
            elif arg in self.command_instances['K']:
                result = self.get_K(in_file)
                arg_list.append(result)
                if result == self.stop_def:
                    break
        return arg_list

    def get_K(self, file_in):
        """Get a crutchy structure."""
        new_struct = file_in.read(1)[0]
        file_in.seek(-1, 1)
        if new_struct > 2:
            return self.stop_def
        else:
            return self.continue_def

    def get_C(self, file_in, encoding):
        """Get a code structure from the file."""
        result_list = [self.struct_def]

        new_struct = file_in.read(1).hex(' ')
        new_entry = self.get_struct_entry(new_struct)
        if new_entry is None:
            raise XlvnsScriptError("Incorrect struct: {}!".format(new_struct))
        if new_entry[2]:
            new_struct = new_entry[2]
        result_list.append(new_struct)
        result_list.append(
            self.extract_args(file_in, new_entry[1], encoding)
        )
            
        return result_list

    @staticmethod
    def get_B(file_in, definer: str) -> int:
        """Extract B/b structure."""
        dummy = struct.unpack(definer, file_in.read(1))[0]
        return dummy

    @staticmethod
    def get_H(file_in, definer: str) -> int:
        """Extract H/h structure."""
        dummy = struct.unpack(definer, file_in.read(2))[0]
        return dummy

    @staticmethod
    def get_I(file_in, definer: str) -> int:
        """Extract I/i structure."""
        dummy = struct.unpack(definer, file_in.read(4))[0]
        return dummy

    @staticmethod
    def get_S(definer: str, in_file, encoding: str) -> str:
        """Get string from the mode and input file (pointer at the start of stirng)."""
        if definer == "S":
            size = struct.unpack("H", in_file.read(2))[0]
        elif definer == "s":
            size = struct.unpack("B", in_file.read(1))[0]
        string = in_file.read(size)
        return string.decode(encoding)

    # Version methods.

    def get_header_bytes(self, version: tuple, size: int, **kwargs) -> bytes:
        """Get header bytes from version, size and default_prms."""
        default_prms = kwargs.get("default_prms", self.default_prms)
        out_bytes = b''
        out_bytes += struct.pack("HH", *version)
        out_bytes += struct.pack("I", size)
        out_bytes += struct.pack("II", *default_prms)
        out_bytes += bytes(self.script_padding - len(out_bytes))
        return out_bytes


    @staticmethod
    def get_version(sdt_file):
        """Get script version."""
        sdt_file.seek(0, 0)
        return tuple(struct.unpack("HH", sdt_file.read(4)))

    @staticmethod
    def get_script_from_version(version: tuple):
        """Get script library from version."""
        if version == (0, 0):
            return None
        elif version == (76, 70):
            return XlvnsScript76_70()
        else:
            raise XlvnsScriptError("Incorrect version!")


class XlvnsScript76_70(XvlnsScriptBase):
    script_library = (
        ("01 00", "", "END"),
        ("02 01", "CCC", "IMAGE_FLASH"),
        ("03 00", "BI", ""),  # Label-related?
        ("05 00", "B", ""),  # Hide next message until the blick? No, probably not...
        ("06 00", "BBBI", ""),
        ("07 00", "HII", "JUMP_IF"),
        ("0b 00", "I", "JUMP"),
        ("0c 00", "B", ""), # BHHIB? # F # Check args!
        ("0d 00", "B", ""),
        ("0d 01", "BC", ""),
        ("0e 01", "BCC", ""),
        ("0f 01", "BCC", ""),

        ("10 00", "H", ""),
        ("11 00", "C", ""),
        ("12 01", "CCC", ""),
        ("13 01", "CC", ""),
        ("14 00", "", ""),
        ("16 00", "H", ""),
        ("19 00", "IB", ""),  # Not offset.
        ("19 01", "", ""),
        ("1b 00", "BHH", ""),  # ?
        ("1b 01", "CCCCCCC", ""),
        ("1c 00", "B", ""),
        ("1c 01", "CCCCCCC", ""),
        ("1d 00", "B", ""),
        ("1e 00", "", ""),
        ("1f 01", "CC", ""),

        ("25 00", "H", ""),  # ""
        ("27 00", "", "START_SCRIPT"),
        ("2d 00", "", ""),

        ("3c 00", "", ""),

        ("40 00", "CCCCCCC", "EFFECT_SCENE"),  # Don't sure about "scene" commands.
        ("41 00", "CCCCCCC", ""),
        ("42 00", "CCCCCC", "BG_SCENE"),
        ("43 00", "CCCCCC", ""),
        ("47 00", "CCCCCCC", ""),
        ("48 00", "CCCCCCC", "CG_SCENE"),
        ("4c 00", "C", ""),
        ("4d 00", "", ""),
        ("4e 00", "C", ""),
        ("4f 00", "CCCC", "BLINK"),

        ("53 00", "CCCCCC", ""),
        ("56 00", "CCCCCCCC", ""),
        ("57 00", "CCC", ""),
        ("5a 00", "", ""),
        ("5d 00", "CCCCCC", ""),
        ("5e 00", "CC", ""),

        ("62 00", "", ""),
        ("63 00", "CCCC", ""),
        ("64 00", "C", ""),
        ("66 00", "CC", ""),
        ("68 00", "CC", ""),  # You may see offset, but it's not.  # Fade?
        ("69 00", "CCCCC", ""),  # You may see offset, but it's not.
        ("6a 00", "CC", ""),
        ("6b 00", "C", ""),
        ("6e 00", "CC", ""),

        ("70 00", "CCCHC", ""),  # [3] is a counter! But I don't know where it starts...
        ("71 00", "CCCCCC", ""),  # No offsets.
        ("78 00", "KCC", ""),  # CC
        ("79 00", "H", ""),
        ("7e 00", "CCC", ""),
        ("7f 00", "", ""),

        ("80 00", "CC", ""),
        ("81 00", "CB", ""),
        ("82 00", "CC", ""),
        ("83 00", "CB", ""),
        ("84 00", "s", "CHANGE_SCRIPT"),
        ("87 00", "CC", "BACKGROUND_IN"),
        ("88 00", "CC", ""),

        ("b7 00", "CCCCC", ""),
        ("b8 00", "", ""),

        ("c4 00", "SBH", "MESSAGE"),  # Message recount [2]!
        ("c8 00", "SB", "DIALOG"),  # Hmmm?
        ("ce 00", "B", ""),
        ("cc 00", "sCCC", ""),

        ("e0 00", "CCCCCCCC", ""),
        ("e2 00", "C", ""),
        ("e3 00", "CCsCCsCCs", "LOAD_BJR"),  # Check.
        ("e4 00", "CCsCCCs", "LOAD_BMP"),
        ("e7 00", "C", ""),
        ("e9 00", "CsCCC", "LOAD_APK"),
        ("ea 00", "C", ""),
        ("eb 00", "C", ""),
        ("ec 00", "", ""),  # H?
        ("ed 00", "CC", ""),

        ("f3 00", "CC", ""),
        ("f5 00", "CCC", ""),
        ("f7 00", "CCCC", ""),
        ("f8 00", "CCC", ""),
        ("fa 00", "CCCCC", ""),
        ("fc 00", "CC", ""),
        ("ff 00", "C", ""),
    )
    offsets_library = (
        ("06 00", (3,)),
        ("07 00", (2,)),
        ("0b 00", (0,)),
        #("0c 00", (3,)), # Sometimes matches, but only sometimes.
    )

    # Technical methods for decompilation.

    @staticmethod
    def decompile_header(in_file) -> tuple:
        in_file.seek(0, 0)
        ver = struct.unpack("HH", in_file.read(4))
        prm = struct.unpack("III", in_file.read(12))
        return ver, prm


class XlvnsScriptError(Exception):
    pass
