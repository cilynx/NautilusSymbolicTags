from gi.repository import Nautilus, Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf

import os
import urllib

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

    def select_tag(self, widget, event, data=None):
        icon = Gtk.IconTheme.get_default().load_icon('gtk-file', 48, 0)
        (treeModel, selectedPaths) =  widget.get_selection().get_selected_rows()
        self.fileList.clear()

        taggedFiles = {}
        selectedTags = []

        for treePath in selectedPaths:
            tag = treeModel.get_value(treeModel.get_iter(treePath), 0)
            tagDir = os.path.join(self.tagsDir, tag)
            for fileName in os.listdir(tagDir):
                if os.path.isfile(os.path.join(tagDir, fileName)):
                    if fileName in taggedFiles:
			taggedFiles[fileName] += [tag]
                    else:
                        taggedFiles[fileName] = [tag]
            selectedTags += [tag]

        for fileName, tagList in taggedFiles.iteritems():
            if len(tagList) == len(selectedTags):
                self.fileList.append([icon, fileName, fileName])

    def filter_by_tags(self, menuItem, file):

        self.tagsDir = os.path.join(urllib.unquote(file.get_uri()[7:]), '.symtags')

        try:
            os.makedirs(self.tagsDir)
        except OSError:
            if not os.path.isdir(self.tagsDir):
                raise

        tags = [tag for tag in os.listdir(self.tagsDir) if os.path.isdir(os.path.join(self.tagsDir, tag))]
        tags.sort()

        treeTags = Gtk.ListStore(str)
        for tag in tags:
            treeTags.append([tag])

        cell = Gtk.CellRendererText()

        treeView = Gtk.TreeView(treeTags)
        treeView.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        treeView.connect("button_release_event", self.select_tag, None)
        treeView.append_column(Gtk.TreeViewColumn("Tags", cell, text=0))

        self.fileList = Gtk.ListStore(Pixbuf, str, str)
        iconView = Gtk.IconView.new()
        iconView.set_model(self.fileList)
        iconView.set_pixbuf_column(0)
        iconView.set_text_column(1)

        treeWindow = Gtk.ScrolledWindow()
        treeWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        treeWindow.add_with_viewport(treeView)

        iconWindow = Gtk.ScrolledWindow()
        iconWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        iconWindow.add_with_viewport(iconView)

        panedWindow = Gtk.HPaned()
        panedWindow.add1(treeWindow)
        panedWindow.add2(iconWindow)
        panedWindow.set_position(150)
        panedWindow.show_all()

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
