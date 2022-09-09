import XInput
from pynput.keyboard import Key, Controller
import time

print("ZppControllerToChat")

if not XInput.get_connected()[0]:
    print("Manette non détectée :-(")
    quit()

class MyHandler(XInput.EventHandler):
    def __init__(self, *controllers, filter=...):
        super().__init__(*controllers, filter=filter)
        self.upper = False
        self.stop = False
        self.keyboard = Controller()
        self.last_keystroke = time.time()

    def process_button_event(self, event):
        if event.type == XInput.EVENT_BUTTON_PRESSED:
            match event.button_id:
                case XInput.BUTTON_DPAD_UP:
                    self.type_word("haut")
                case XInput.BUTTON_DPAD_DOWN:
                    self.type_word("bas")
                case XInput.BUTTON_DPAD_LEFT:
                    self.type_word("gauche")
                case XInput.BUTTON_DPAD_RIGHT:
                    self.type_word("droite")
                case XInput.BUTTON_A:
                    self.type_word("a")
                case XInput.BUTTON_B:
                    self.type_word("b")
                case XInput.BUTTON_START:
                    self.type_word("start")
                case XInput.BUTTON_LEFT_THUMB:
                    self.stop = True
                case _:
                    print(event)

    def process_trigger_event(self, event):
        return

    def process_stick_event(self, event):
        return

    def process_connection_event(self, event):
        return

    def type_word(self, word):
        now = time.time()

        if (now - self.last_keystroke) > 1.5:
            self.last_keystroke = now

            output = ""
            if self.upper:
                output = word.upper()
            else:
                output = word

            print(output)
            for c in output:
                self.press_key(c)

            self.press_key(Key.enter)

            self.upper = not self.upper

    def press_key(self, character):
        self.keyboard.press(character)
        self.keyboard.release(character)

filter = XInput.BUTTON_DPAD_UP + XInput.BUTTON_DPAD_DOWN + XInput.BUTTON_DPAD_RIGHT + XInput.BUTTON_DPAD_LEFT + XInput.BUTTON_A + XInput.BUTTON_B + XInput.BUTTON_START + XInput.BUTTON_LEFT_THUMB
my_handler = MyHandler(0)
my_handler.set_filter(filter)

print("Lezgo, pour sortir du programme, appuyez sur votre stick gauche.")

my_gamepad_thread = XInput.GamepadThread(my_handler)

while(not my_handler.stop):
    continue

print("Tchao")