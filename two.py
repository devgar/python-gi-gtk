from gi.repository import Gtk, GLib, GObject
from gi.repository import AppIndicator3 as appindicator
import os
import signal

class Gui():
    def __init__(self):
        self.window = Gtk.Window(title="Signal example")
        self.window.set_size_request(250,150)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

    def cleanup(self):
        print("... Cleaning up variables, etc.")

    def quit(self, widget):
        print("... Exiting main gtk loop")
        Gtk.main_quit()

def InitSignal(gui):
    def signal_action(signal):
        if signal is 1:
            print("Caught signal SIGHUP(1)")
        elif signal is 2:
            print("Caught signal SIGINT(2)")
        elif signal is 15:
            print("Caught signal SIGTERM(15)")
        gui.cleanup()
        gui.quit(None)

    def idle_handler(*args):
        print("Python signal handler activated.")
        GLib.idle_add(signal_action, priority=GLib.PRIORITY_HIGH)

    def handler(*args):
        print("GLib signal handler activated.")
        signal_action(args[0])

    def install_glib_handler(sig):
        unix_signal_add = None

        if hasattr(GLib, "unix_signal_add"):
            unix_signal_add = GLib.unix_signal_add
        elif hasattr(GLib, "unix_signal_add_full"):
            unix_signal_add = GLib.unix_signal_add_full

        if unix_signal_add:
            print("Register GLib signal handler: %r" % sig)
            unix_signal_add(GLib.PRIORITY_HIGH, sig, handler, sig)
        else:
            print("Can't install GLib signal handler, too old gi.")

    SIGS = [getattr(signal, s, None) for s in "SIGINT SIGTERM SIGHUP".split()]
    for sig in filter(None, SIGS):
        print("Register Python signal handler: %r" % sig)
        signal.signal(sig, idle_handler)
        GLib.idle_add(install_glib_handler, sig, priority=GLib.PRIORITY_HIGH)

if __name__ == "__main__":
    gui = Gui()
    InitSignal(gui)
    Gtk.main()
