import sys

from cologer.field import Fields


class Level:
    def __init__(self, name: str, fmt: str) -> None:
        self.name = name.upper()
        self.visible = True
        self.fields = Fields(fmt, self.name)

    def invisible(self):
        self.visible = False

    def __call__(self, *args, **kwargs):
        if self.visible:
            sys.stdout.write(self.fields._get_final_str(*args, **kwargs)+'\n')
