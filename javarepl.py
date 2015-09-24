from os.path import dirname
from os.path import realpath
import os
import sublime_plugin
import sublime
import shutil
import fnmatch


_PACKAGE_PATH = dirname(dirname(dirname(realpath(__file__))))
_OWN_PATH = os.path.join(_PACKAGE_PATH, "Packages/JavaREPL")
_REPL_PATH = os.path.join(_PACKAGE_PATH, "Packages/SublimeREPL/config")
_JINT = os.path.join(_REPL_PATH, "Java")


def is_sublimeREPL_installed():
    return os.path.isdir(os.path.join(_PACKAGE_PATH, "Packages/SublimeREPL"))


def is_javaREPL_installed():
    if os.path.isdir(_JINT):
        for files in os.listdir(_JINT):
            if fnmatch.fnmatch(files, 'bsh*.jar'):
                return True
    return False


def install_javaREPL():
    os.mkdir(_JINT)
    shutil.copytree(_OWN_PATH, _JINT)


class InstallJavaREPLCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not is_sublimeREPL_installed():
            sublime.error_message("Please install SublimeREPL first!")
            return
        if not is_javaREPL_installed():
            install_javaREPL()


class OpenJavaREPLCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        if is_sublimeREPL_installed() and is_javaREPL_installed():
            return True
        return False

    def run(self):
        view = self.window.new_file()
        view.window().run_command("repl_open", {
            "type": "subprocess",
            "encoding": "utf-8",
            "cmd": ["java", "bsh.Interpreter"],
            "cwd": "$file_path",
                   "env": {"CLASSPATH": _JINT},
                   "external_id": "java",

                   "syntax": "Packages/Java/Java.tmLanguage"
            })

