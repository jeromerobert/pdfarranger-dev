#! /usr/bin/env python3

import gi
gi.require_version('Atspi', '2.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Atspi
from gi.repository import Gdk
km = Gdk.Keymap.get_for_display(Gdk.Display.get_default())
r, kc = km.get_entries_for_keyval(Gdk.KEY_a)
acode = kc[0].keycode
r, kc = km.get_entries_for_keyval(Gdk.KEY_Control_L)
ctrlcode = kc[0].keycode
print(Gdk.keyval_from_name("é"))
print(ord("é"), hex(Gdk.unicode_to_keyval(ord("é"))))
# Does not work (break keyboard)
# TODO: find why
Atspi.generate_keyboard_event(0, "éèà@ù", Atspi.KeySynthType.STRING)

# Work
#Atspi.generate_keyboard_event(acode, None, Atspi.KeySynthType.PRESSRELEASE)

# Work
#Atspi.generate_keyboard_event(ctrlcode, None, Atspi.KeySynthType.PRESS)
#Atspi.generate_keyboard_event(Gdk.KEY_c, None, Atspi.KeySynthType.PRESSRELEASE | Atspi.KeySynthType.SYM)
#Atspi.generate_keyboard_event(ctrlcode, None, Atspi.KeySynthType.RELEASE)

# Does not work (Is not keyboard layout aware)
#Atspi.generate_keyboard_event(Gdk.KEY_a, None, Atspi.KeySynthType.PRESSRELEASE | Atspi.KeySynthType.SYM)

# TODO: what is the difference between Atspi.KeySynthType.PRESS & Atspi.KeySynthType.LOCKMODIFIERS ?
# /usr/libexec/at-spi-bus-launcher --launch-immediately
# setxkbmap -v fr
# gsettings set org.gnome.desktop.interface toolkit-accessibility true

class Keyboard:
    __instance = None
    def __init__(self, keymap):
        self.keymap = keymap
    @staticmethod
    def get_default():
        if Keyboard.__instance is None:
            Keyboard.__instance = Keyboard(Gdk.Keymap.get_for_display(Gdk.Display.get_default()))
        return Keyboard.__instance

    def __keycode(self,keyname):
        r, kc = self.keymap.get_entries_for_keyval(Gdk.keyval_from_name(keyname))
        return kc[0].keycode

    def press(self, keyname):
        Atspi.generate_keyboard_event(self.__keycode(keyname), None, Atspi.KeySynthType.PRESS)
        
    def release(self, keyname):
        Atspi.generate_keyboard_event(self.__keycode(keyname), None, Atspi.KeySynthType.RELEASE)

    def type(self, keyname):
        Atspi.generate_keyboard_event(self.__keycode(keyname), None, Atspi.KeySynthType.PRESSRELEASE)

    def combo(self, *key):
        for modifier in key[:-1]:
            self.press(modifier)
        self.type(key[-1])
        for modifier in key[:-1]:
            self.release(modifier)

    def string(self, s):
        for c in s:
            r, kc = self.keymap.get_entries_for_keyval(Gdk.unicode_to_keyval(ord(c)))
            Atspi.generate_keyboard_event(kc[0].keycode, None, Atspi.KeySynthType.PRESSRELEASE)
            

#Keyboard.get_default().string('coucou')
#Keyboard.get_default().type('a')
#Keyboard.get_default().combo('Shift_L', 'c')
Keyboard.get_default().string('éç')

