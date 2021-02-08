
import os
import os.path
import rb
import logging
import filecmp

from urllib.parse import unquote, urlparse
from shutil import copy


from gi.repository import Gio, GObject, Peas, PeasGtk, RB, Gtk

from sync_playlist_prefs import SyncPlaylistConfigureDialog




class SyncPlaylistPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'SyncPlaylistPlugin'
    object = GObject.property(type=GObject.Object)
    _menu_names = ['playlist-popup']


    def __init__(self):
        super(SyncPlaylistPlugin, self).__init__()
        self.config = None
        self.choose_button = None
        self.path_display = None
        self.chooser = None
        self.choose_button2 = None
        self.path_display2 = None
        self.chooser2 = None
        self.window = None
        self.action = None
        self.messagedialog = None
        self.plugin_info = "sync_playlist"


    def do_sync_playlist(self, *args):
        print("action...")

        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            os.path.expanduser("~/.local/share/rhythmbox/plugins/sync_playlist/schemas"),
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        schema = schema_source.lookup('org.gnome.rhythmbox.plugins.sync_playlist', False)
        settings = Gio.Settings.new_full(schema, None, None)

        #settings = Gio.Settings.new("org.gnome.rhythmbox.plugins.sync_playlist")
        sync_tracks_folder = settings.get_string("tracks-folder")
        sync_playlists_folder = settings.get_string("playlists-folder")
        
        if (not os.path.isdir(sync_tracks_folder)) or (not os.path.isdir(sync_playlists_folder)):
            print("folders not valid")
            self.display_warning_message("No valid destination folder, please check settings in plugins->sync_playlist")
            return

        
        page = self.object.props.selected_page
        
        print(page.props.name)
        
        file = open(os.path.join(sync_playlists_folder, page.props.name + '.m3u'), 'w')
        file.write("#EXTM3U\n")
                    
        
        for row in page.props.query_model:
            entry = row[0]
            print(entry)
            print(entry.get_playback_uri())
            print(entry.get_string (RB.RhythmDBPropType.ARTIST))
            print(entry.get_string (RB.RhythmDBPropType.LOCATION))
            print(entry.get_ulong (RB.RhythmDBPropType.DURATION))
            print(entry.get_string (RB.RhythmDBPropType.TITLE))
            print("")
            fileuri = entry.get_playback_uri()
            fileparsed = urlparse(fileuri)
            fileunquoted = unquote(fileparsed.path)
            print(fileunquoted)
            print("")
            destination = os.path.join(sync_tracks_folder,fileunquoted[1:])
            print(destination)
            destination_path = os.path.dirname(destination)
            print(destination_path)
            os.makedirs(destination_path,exist_ok=True)
            copy(fileunquoted, destination)
            file.write("#EXTINF:"+str(entry.get_ulong (RB.RhythmDBPropType.DURATION))+","+entry.get_string (RB.RhythmDBPropType.TITLE)+"\n")
            file.write(fileunquoted[1:]+"\n")
            
        file.close()


    def do_activate(self):

        shell = self.object
        app = shell.props.application
        self.window = shell.props.window

        #app = Gio.Application.get_default()
        #self.window = self.object.props.window

        self.action = Gio.SimpleAction.new("action_sync_playlist", None)
        self.action.connect("activate", self.do_sync_playlist)
        app.add_action(self.action)

        # add plugin menu item (note the "app." prefix here)
        item = Gio.MenuItem()
        item.set_label('sync playlist')
        item.set_detailed_action('app.action_sync_playlist')
        app.add_plugin_menu_item('playlist-menu', 'sync-playlist', item)      # display-page-add-playlist




    def do_deactivate(self):
        #del self.string
        app = Gio.Application.get_default()
        app.remove_plugin_menu_item('playlist-menu','sync-playlist')
        app.remove_action("action_sync_playlist")
        self.action = None
        

    def display_warning_message(self, message):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK,
                                   _(message))

        dialog.run()
        dialog.destroy()

