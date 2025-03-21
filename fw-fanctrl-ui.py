from pystray import MenuItem, Menu
import pystray
from PIL import Image
import subprocess

program_name="Framework Fan Control UI"
currentStrategy = ""

def is_current_strategy(item):
  global currentStrategy
  return item.text == currentStrategy

def set_strategy(icon, item):
  global currentStrategy
  currentStrategy = subprocess.check_output(["fw-fanctrl", "use", item.text]).decode("utf-8").strip()
  icon.notify(f"{currentStrategy}")

def generate_strategy_menu():
  for i in subprocess.check_output(["fw-fanctrl", "print", "list"]).decode("utf-8").splitlines():
    if i.startswith("Strategy list:"): 
      continue
    cleanedName = i.strip()
    cleanedName = i.lstrip(" - ")
    yield MenuItem(cleanedName, set_strategy, checked=is_current_strategy, radio=True)
    
def reload(icon, item):
  result = subprocess.check_output(["fw-fanctrl", "reload"]).decode("utf-8").strip()
  icon.notify(f"Reload: {result}")
    
def pause(icon, item):
  result = subprocess.check_output(["fw-fanctrl", "pause"]).decode("utf-8").strip()
  icon.notify(f"Pause: {result}")
  
def resume(icon, item):
  result = subprocess.check_output(["fw-fanctrl", "resume"]).decode("utf-8").strip()
  icon.notify(f"Resume: {result}")
  
def quit():
  exit(0)

def generate_main_menu():
  global currentStrategy
  try:
    commandOutput = subprocess.check_output(["fw-fanctrl", "print", "current"]).decode("utf-8").strip()
    commandOutput = commandOutput.splitlines()[0]
    commandOutput = commandOutput.replace('Strategy in use:', '');
    commandOutput = commandOutput.strip().strip("'")
    currentStrategy = commandOutput
  except:
    yield MenuItem("fw-fanctrl not installed", action=None, enabled=False)
    return
  
  yield MenuItem(program_name, action=None, enabled=False)
  yield MenuItem(f"Current Strategy: {currentStrategy}", action=None, enabled=False)
  yield MenuItem("Set Strategy", Menu(generate_strategy_menu))
  yield MenuItem("Reload", reload)
  yield MenuItem("Pause", pause)
  yield MenuItem("Resume", resume)
  yield MenuItem("Quit", quit)

image=Image.open("favicon.ico")
icon=pystray.Icon("name", image, program_name, Menu(generate_main_menu))

def setup(icon):
    icon.visible = True

icon.run(setup)

