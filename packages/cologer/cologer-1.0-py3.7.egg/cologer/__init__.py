from cologer.main import Cologer
from cologer.field import Fore, Back, Style


loger = Cologer()
loger.set_field_fore(time=Fore.CYAN)
# coloring debug
loger.debug.fields.level.set_fore(Fore.BLACK).set_back(Back.MAGENTA)
# coloring info
loger.info.fields.level.set_fore(Fore.BLACK).set_back(Back.BLUE)
# coloring success
loger.success.fields.level.set_fore(Fore.BLACK).set_back(Back.GREEN)
# coloring warning
loger.warning.fields.level.set_fore(Fore.BLACK).set_back(Back.YELLOW)
# coloring error
loger.error.fields.level.set_fore(Fore.BLACK).set_back(Back.RED)