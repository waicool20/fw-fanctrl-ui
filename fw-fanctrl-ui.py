import re
from threading import Thread
import time
from pystray import MenuItem, Menu
from pystray._base import Icon
import pystray
from PIL import Image
import subprocess

program_name = "Framework Fan Control UI"
currentStrategy = ""


def is_current_strategy(item: MenuItem):
  global currentStrategy
  return item.text == currentStrategy


def set_strategy(icon: Icon, item: MenuItem):
  global currentStrategy
  currentStrategy = subprocess.check_output(["fw-fanctrl", "use", item.text]).decode("utf-8").strip()
  icon.notify(f"{currentStrategy}")


def generate_strategy_menu():
  for i in subprocess.check_output(["fw-fanctrl", "print", "list"]).decode("utf-8").splitlines():
    if not i.startswith("-"):
      continue
    yield MenuItem(i[2:], set_strategy, checked=is_current_strategy, radio=True)


def reload(icon: Icon, item: MenuItem):
  result = subprocess.check_output(["fw-fanctrl", "reload"]).decode("utf-8").strip()
  icon.notify(f"Reload: {result}")


def pause(icon: Icon, item: MenuItem):
  result = subprocess.check_output(["fw-fanctrl", "pause"]).decode("utf-8").strip()
  icon.notify(f"Pause: {result}")


def resume(icon: Icon, item: MenuItem):
  result = subprocess.check_output(["fw-fanctrl", "resume"]).decode("utf-8").strip()
  icon.notify(f"Resume: {result}")


def quit():
  icon.stop()
  exit(0)


def generate_main_menu():
  global currentStrategy
  if currentStrategy == "":
    yield MenuItem("fw-fanctrl daemon not installed or running", action=None, enabled=False)
    yield MenuItem("Quit", quit)
    return

  yield MenuItem(program_name, action=None, enabled=False)
  yield MenuItem(f"Current Strategy: {currentStrategy}", action=None, enabled=False)
  yield MenuItem("Set Strategy", Menu(generate_strategy_menu))
  yield MenuItem("Reload", reload)
  yield MenuItem("Pause", pause)
  yield MenuItem("Resume", resume)
  yield MenuItem("Quit", quit)


def check_alive():
  global icon, currentStrategy
  while True:
    try:
      commandOutput = subprocess.check_output(["fw-fanctrl", "print", "current"],
                                              stderr=subprocess.STDOUT).decode("utf-8").strip()
      _currentStrategy = re.findall(r"Strategy in use: '(.*?)'", commandOutput)[0]
      if currentStrategy != _currentStrategy:
        currentStrategy = _currentStrategy
        icon.update_menu()
    except:
      currentStrategy = ""
      icon.update_menu()
    time.sleep(2)


image = Image.open("favicon.ico")
icon = pystray.Icon("name", image, program_name, Menu(generate_main_menu))
Thread(target=check_alive, name="CheckAliveThread").start()


def setup(icon: Icon):
  icon.visible = True


icon.run(setup)
