import difflib
import re
from termcolor import colored


star_import = re.compile("(^from \*|import \*$)")
normal_import = re.compile("(^from .*|^import .*)")


class SortImports:
    """Given a list of imports, return a sorted list of them

    Get all the lines match them to normal_import and then sort
    them with the sorted method using the item at index 1"""
    def __init__(self, lines: list):
        self.lines = lines
        self.import_lines = self.get_import_lines()
        self.sorted_lines = self.alphabet_lines()

    def get_import_lines(self):
        """Get all the imports that match normal_import"""
        return [line for line in self.lines if normal_import.match(line)]

    def named_item(self, item):
        """Get the first item that is named"""
        line = item.split(" ")
        return line[1]

    def alphabet_lines(self):
        """Sort the imports using the item given by named_item"""
        return sorted(self.import_lines, key=self.named_item)


class CheckImports:
    """Check the imports for warnings like using *"""
    def __init__(self, lines):
        self.lines = lines

    def check_bad_practice(self, line):
        if star_import.search(line):
            print(f"Don't do this -> {line.strip()}")

    def check_lines(self):
        for line in self.lines:
            self.check_bad_practice(line)


class ImportLinter:
    """Open the file, reconstruct with oprdered imports, then write to it

    Using the filepath, get the lines and parse out the imports.
    Find the import block (place where the imports are).
    Reconstruct the file with before the import block then the imports
    and after the imports.
    Then write the new file"""
    def __init__(self, input_filepath: str):
        self.input_filepath = input_filepath
        self.lines = self.read_file_lines()

        self.sort_imports = SortImports(self.lines)
        self.import_lines = self.sort_imports.import_lines
        self.sorted_lines = self.sort_imports.sorted_lines

        self.get_import_block()

    def read_file_lines(self):
        file = open(self.input_filepath, "r")
        return file.readlines()

    def get_import_block(self):
        """Get the first import and the last import

        From the lines, get all the ones that are imports
        then set start to the first one and end to the last one"""
        import_line_indexs = []
        for num, line in enumerate(self.lines):
            if normal_import.match(line):
                import_line_indexs.append(num)
        self.start = import_line_indexs[0]
        self.end = import_line_indexs[-1]

    def reconstruct_file(self):
        """Reconstruct the file with all the parts

        Add the starting lines to the sorted imports to the
        lines at the end"""
        before = self.lines[:self.start]
        after = self.lines[self.end+1:]
        final_file_lines = before + self.sorted_lines + after
        return final_file_lines

    def write_file(self):
        """Write file with reconstructed file as lines"""
        file = open(self.input_filepath, "w")
        for line in self.reconstructed_file:
            file.write(line)

    def show_diff(self):
        d = difflib.Differ()
        diffs = d.compare(self.import_lines, self.sorted_lines)
        for diff in diffs:
            diff_type = diff.split()[0]
            if diff_type == "+":
                print(colored(diff.strip(), "green"))
            elif diff_type == "-":
                print(colored(diff.strip(), "red"))

    def fix(self):
        self.reconstructed_file = self.reconstruct_file()
        self.write_file()
        self.show_diff()

    def report(self):
        check_imports = CheckImports(self.lines)
        check_imports.check_lines()
        self.show_diff()
