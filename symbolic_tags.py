from gi.repository import Nautilus, Gtk, GObject

class SymbolicTags(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass
   
    def get_file_items(self, window, files):
        self.window = window
        item = Nautilus.MenuItem(name='SymbolicTags::Tags',
                                         label='Tags',
                                         tip='',
                                         icon='')
        item.connect('activate', self.manage_file_tags, files)
        return item,

    def get_background_items(self, window, file):
        self.window = window
        item = Nautilus.MenuItem(name='SymbolicTags::Filter',
                                         label='Filter by Tags',
                                         tip='',
                                         icon='')
        item.connect('activate', self.filter_by_tags, file)
        return item,

    def filter_by_tags(self, menuItem, file):
        panedWindow = Gtk.HPaned()
        dialogBox = Gtk.Dialog("Filter by Tags", self.window, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,))
        dialogBox.set_size_request(600, 400)
        dialogBox.vbox.pack_start(panedWindow, expand=True, fill=True, padding=0)
        dialogBox.run()  
        dialogBox.destroy()

    def manage_file_tags (self, menuItem, files):
        panedWindow = Gtk.HPaned()
        dialogBox = Gtk.Dialog("Manage File Tags", self.window, Gtk.DialogFlags.MODAL, (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,))
        dialogBox.set_size_request(600, 400)
        dialogBox.vbox.pack_start(panedWindow, expand=True, fill=True, padding=0)
        dialogBox.run()  
        dialogBox.destroy()
