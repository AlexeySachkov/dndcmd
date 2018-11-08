import cmd
import enum
from dndcmd.Driver import Driver


class LogLevel(enum.Enum):
    ALL = 0
    DEBUG = 1
    INFO = 2
    ERROR = 3
    FATAL = 4

    def __str__(self):
        if self.value == LogLevel.ALL:
            return 'ALL'
        elif self.value == LogLevel.DEBUG:
            return 'DEBUG'
        elif self.value == LogLevel.INFO:
            return 'INFO'
        elif self.value == LogLevel.ERROR:
            return 'ERROR'
        elif self.value == LogLevel.FATAL:
            return 'FATAL'


class Logger:
    log_level = LogLevel.INFO

    @staticmethod
    def _log(level, msg):
        if level >= Logger.log_level:
            print('[{}] {}'.format(level, msg))

    @staticmethod
    def debug(msg):
        Logger._log(LogLevel.DEBUG, msg)

    @staticmethod
    def info(msg):
        Logger._log(LogLevel.INFO, msg)

    @staticmethod
    def error(msg):
        Logger._log(LogLevel.ERROR, msg)

    @staticmethod
    def fatal(msg):
        Logger._log(LogLevel.FATAL, msg)


class CharacterClass:
    def hp_on_first_level(self):
        Logger.debug(
            'CharacterClass::hp_on_first_level generic method called!')
        pass

    def hp_per_level(self):
        Logger.debug('CharacterClass::hp_per_level generic method called!')
        pass


class Warden(CharacterClass):
    def hp_on_first_level(self):
        return 17

    def hp_per_level(self):
        return 7


class Character:
    def __init__(self, character_class):
        self.character_class = character_class()
        self.max_hp = self.character_class.hp_on_first_level()
        self.level = 1

    def levelup(self):
        self.max_hp += self.character_class.hp_per_level()

    def get_max_hp(self):
        return self.max_hp


class DnDShell(cmd.Cmd):
    intro = 'Hi, it is a D&D shell!'
    prompt = 'D&D > '

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = Driver(self.stdout)

    character = Character(Warden)

    def emit_diags(self, arg, diags):
        for column, msg in diags:
            pointer = '^'.rjust(column + 1, ' ')
            print('Error: {}\n{}\n{}'.format(msg, arg, pointer),
                  file=self.stdout)

    def do_roll(self, arg):
        self.driver.execute_roll_command(arg)

    def do_max_hp(self, arg):
        print('Max HP: {}'.format(self.character.get_max_hp()),
              file=self.stdout)

    def do_levelup(self, arg):
        self.character.levelup()

    def do_exit(self, arg):
        print('Bye!', file=self.stdout)
        return True
