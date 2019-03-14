* <https://developer.gnome.org/gnome-devel-demos/stable/menubar.py.html.en>
* <https://stackoverflow.com/questions/22578346/python-gtk3-toolbar-accelerator-doesnt-work>
* <https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Application.html*Gtk.Application.add_accelerator>
* <https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Widget.html*Gtk.Widget.set_tooltip_text>
* <https://gitlab.gnome.org/GNOME/pygobject/blob/master/gi/overrides/Gio.py*L137>
* <warning: https://gitlab.gnome.org/GNOME/pygobject/issues/29>
* <https://lazka.github.io/pgi-docs/Gio-2.0/classes/ActionMap.html*Gio.ActionMap.add_action_entries>
* <https://lazka.github.io/pgi-docs/index.html*Gtk-3.0/classes/Application.html*Gtk.Application.set_accels_for_action>

```python
print(Gio.Action.print_detailed_name(self.impl.window.lookup_action("rotate").get_name(), GLib.Variant.new_int32(90)))
Gtk.accelerator_name(Gdk.KEY_Delete, 0)=='Delete'
```

## GMenu migration

* <https://gitlab.gnome.org/GNOME/gtk/blob/master/demos/gtk-demo/shortcuts-builder.ui>
* <https://lazka.github.io/pgi-docs/Gtk-3.0/classes/ShortcutsWindow.html>

## `cx_Freeze`

* <https://stackoverflow.com/questions/24195311/how-to-set-shortcut-working-directory-in-cx-freeze-msi-bundle>
* <https://github.com/marcelotduarte/cx_Freeze/issues/48>
