import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = Adw.Leaflet(
            fold_threshold_policy=Adw.FoldThresholdPolicy.NATURAL,
            can_navigate_back=True,
            can_navigate_forward=True,
        )
        self.set_titlebar(Gtk.Box())

        # Left Box
        self.l = Gtk.Box(hexpand=True)
        self.b = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.lp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.lh = Adw.HeaderBar()
        self.lp.append(self.lh)
        self.l.append(self.lp)
        self.l.append(self.b)

        # Right Box
        self.r = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.rh = Adw.HeaderBar()
        self.r.append(self.rh)

        # Append Children to Leaflet (append ist in Python-Bindungen noch gültig)
        self.set_child(self.a)
        self.a.append(self.l)  # Verwende append() in Python-Bindungen
        self.a.append(self.r)  # Verwende append() in Python-Bindungen

        # Connect Signal
        self.a.connect("notify::folded", self.e)
        self.e()

    def e(self, *data):
        if self.a.props.folded:  # Korrekt: props.folded
            self.lh.set_show_end_title_buttons(True)
            self.rh.set_show_start_title_buttons(True)
            self.b.set_visible(False)
        else:
            self.lh.set_show_end_title_buttons(False)
            self.rh.set_show_start_title_buttons(False)
            self.b.set_visible(True)

class Main(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, application_id="com.example.LeafletDemo")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def main(version):
    app = Main()
    return app.run(sys.argv)

if __name__ == "__main__":
    sys.exit(main(None))