import fire
import main


class ImportLinter(object):
    def check(self, filepath):
        import_linter = main.ImportLinter(filepath)
        import_linter.report()

    def fix(self, filepath):
        import_linter = main.ImportLinter(filepath)
        import_linter.fix()

if __name__ == "__main__":
    fire.Fire(ImportLinter)
