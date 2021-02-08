#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import rb
from gi.repository import RB, Gtk, Gio, GObject, PeasGtk


class SyncPlaylistConfigureDialog (GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'SyncPlaylistConfigureDialog'
    object = GObject.property(type=GObject.Object)
    '''
    Settings dialog
    '''

    def __init__(self):
        GObject.Object.__init__(self)
        self.config = None
        self.choose_button = None
        self.path_display = None

    def do_create_configure_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file(rb.find_plugin_file(self, "sync_playlist_prefs.ui"))

        self.config = builder.get_object("config")

        self.tracks_choose_button = builder.get_object("tracks_choose_button")
        self.tracks_path_display = builder.get_object("tracks_path_display")

        self.playlists_choose_button = builder.get_object("playlists_choose_button")
        self.playlists_path_display = builder.get_object("playlists_path_display")

        self.tracks_choose_button.connect("clicked", self.tracks_choose_callback)
        self.tracks_path_display.connect("changed", self.tracks_path_changed_callback)

        self.playlists_choose_button.connect("clicked", self.playlists_choose_callback)
        self.playlists_path_display.connect("changed", self.playlists_path_changed_callback)

        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            os.path.expanduser("~/.local/share/rhythmbox/plugins/sync_playlist/schemas"),
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        schema = schema_source.lookup('org.gnome.rhythmbox.plugins.sync_playlist', False)
        settings = Gio.Settings.new_full(schema, None, None)

        #settings = Gio.Settings.new("org.gnome.rhythmbox.plugins.sync_playlist")
        tracks_folder = settings.get_string("tracks-folder")  # get the import-export folder
        playlists_folder = settings.get_string("playlists-folder")  # get the import-export folder

        self.tracks_path_display.set_text(tracks_folder)
        self.playlists_path_display.set_text(playlists_folder)

        return self.config

    def tracks_choose_callback(self, widget):
        def response_handler(widget, response):
            if response == Gtk.ResponseType.OK:
                path = self.chooser.get_filename()
                self.chooser.destroy()
                self.tracks_path_display.set_text(path)

            else:
                self.chooser.destroy()

        buttons = (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,
                   Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.chooser = Gtk.FileChooserDialog(title="Choose folder for import/export...",
                                             parent=None,
                                             action=Gtk.FileChooserAction.SELECT_FOLDER,
                                             buttons=buttons)
        self.chooser.connect("response", response_handler)
        self.chooser.set_modal(True)
        self.chooser.set_transient_for(self.config.get_toplevel())
        self.chooser.present()

    def tracks_path_changed_callback(self, widget):
        path = self.tracks_path_display.get_text()

        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            os.path.expanduser("~/.local/share/rhythmbox/plugins/sync_playlist/schemas"),
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        schema = schema_source.lookup('org.gnome.rhythmbox.plugins.sync_playlist', False)
        settings = Gio.Settings.new_full(schema, None, None)

        #settings = Gio.Settings.new("org.gnome.rhythmbox.plugins.sync_playlist")
        settings.set_string("tracks-folder", path)  # get the import-export folder


    def playlists_choose_callback(self, widget):
        def response_handler(widget, response):
            if response == Gtk.ResponseType.OK:
                path = self.chooser.get_filename()
                self.chooser.destroy()
                self.playlists_path_display.set_text(path)

            else:
                self.chooser.destroy()

        buttons = (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,
                   Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.chooser = Gtk.FileChooserDialog(title="Choose folder for import/export2...",
                                             parent=None,
                                             action=Gtk.FileChooserAction.SELECT_FOLDER,
                                             buttons=buttons)
        self.chooser.connect("response", response_handler)
        self.chooser.set_modal(True)
        self.chooser.set_transient_for(self.config.get_toplevel())
        self.chooser.present()

    def playlists_path_changed_callback(self, widget):
        path = self.playlists_path_display.get_text()

        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            os.path.expanduser("~/.local/share/rhythmbox/plugins/sync_playlist/schemas"),
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        schema = schema_source.lookup('org.gnome.rhythmbox.plugins.sync_playlist', False)
        settings = Gio.Settings.new_full(schema, None, None)
        
        #settings = Gio.Settings.new("org.gnome.rhythmbox.plugins.sync_playlist")
        settings.set_string("playlists-folder", path)  # get the import-export folder

