#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class HeaderBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Gister")
        self.set_border_width(4)
        self.set_default_size(540, 360)
        self.set_default_icon_from_file("assets/ico.png")

        self.hb = hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Gist"
        hb.set_subtitle("Noname file")
        self.set_titlebar(hb)

        self.syncbutton = button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        self.syncbutton.connect('clicked', self.on_click_sync)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        self.lbutton = button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        self.rbutton = button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_end(box)

        self.add(Gtk.TextView())
        self.connect('key-press-event', self.on_key_function)
        self.connect("delete-event", Gtk.main_quit)

        self.load_info()

        self.set_position(Gtk.WindowPosition.CENTER)

    def on_click_left(self, widget):
        pass

    def on_click_right(self, widget):
        pass

    def on_click_sync(self, widget):
        icon = "assets/charm.png"
        print "Icon change: '%s'" % icon
        self.set_icon_from_file(icon)

    def load_info(self):
        import json
        with open("info.json") as f:
            ops = json.loads( f.read() )
            self.hb.set_title(ops["title"])
            self.hb.set_subtitle(ops["mainfile"])

    def on_key_function(self, widget, event):
        if Gdk.ModifierType.CONTROL_MASK & event.state:
            if event.keyval == 113:
                Gtk.main_quit()
            print "Event:",event.keyval


win = HeaderBarWindow()
win.show_all()
Gtk.main()
