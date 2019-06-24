"""
do/undo/redo code for all pdfarranger actions
"""
from gi.repository import Gtk
from gi.repository import GObject


class Manager(object):
    """
    Stack of actions
    """

    def __init__(self):
        self.actions = []
        # the one which can be undone
        self.current = -1
        self.undoaction = None
        self.redoaction = None

    def push(self, action):
        self.actions = self.actions[:self.current + 1]
        self.actions.append(action)
        self.current += 1
        self.__refresh()

    def undo(self, action, param, unused):
        a = self.actions[self.current]
        a.undo()
        self.current -= 1
        self.__refresh()

    def redo(self, action, param, unused):
        a = self.actions[self.current + 1]
        a.redo()
        self.current += 1
        self.__refresh()

    def set_actions(self, undo, redo):
        self.undoaction = undo
        self.redoaction = redo
        self.__refresh()

    def __refresh(self):
        if self.undoaction:
            self.undoaction.set_enabled(self.current >= 0)
        if self.redoaction:
            self.redoaction.set_enabled(self.current + 1 < len(self.actions))
        # TODO: refresh undo/redo action labels


class Crop(object):
    """ Undo/redo the crop action """

    def __init__(self, app, oldcrop):
        self.app = app
        self.oldcrop = oldcrop
        self.selection = self.app.iconview.get_selected_items()
        self.is_unsaved = app.is_unsaved

    def redo(self):
        self.oldcrop = self.app.crop(self.selection, self.oldcrop)
        self.app.set_unsaved(True)

    def undo(self):
        self.oldcrop = self.app.crop(self.selection, self.oldcrop)
        self.app.set_unsaved(self.is_unsaved)


class Rotate(object):
    """ Undo/redo the rotate action """

    def __init__(self, app, angle):
        self.app = app
        self.angle = angle
        self.selection = self.app.iconview.get_selected_items()
        self.is_unsaved = app.is_unsaved

    def redo(self):
        self.app.rotate_page(self.selection, self.angle)
        self.app.set_unsaved(True)

    def undo(self):
        self.app.rotate_page(self.selection, -self.angle)
        self.app.set_unsaved(self.is_unsaved)


class Add(object):
    """ Undo/redo actions which add pages """
    def __init__(self, app, pages, insert_ref, before):
        #: A PdfArranger instance
        self.app = app
        #: List of tuples to add to the model
        self.pages = pages
        #: Gtk.TreeRowReference pointing to insertion location
        self.insert_ref = insert_ref
        #: True to insert before insert_ref, False to insert after
        self.before = before
        self.is_unsaved = app.is_unsaved
        #: Gtk.TreeRowReference list to be removed by undo
        self.toremove = []

    def redo(self):
        m = self.app.model
        for p in self.pages:
            it = m.append(p)
            self.toremove.append(Gtk.TreeRowReference.new(m, m.get_path(it)))
            if self.insert_ref:
                iter_to = m.get_iter(self.insert_ref.get_path())
                if self.before:
                    m.move_before(it, iter_to)
                else:
                    m.move_after(it, iter_to)
            self.app.update_geometry(it)
        GObject.idle_add(self.app.render)
        self.app.set_unsaved(True)

    def undo(self):
        m = self.app.model
        for p in self.toremove:
            m.remove(m.get_iter(p.get_path()))
        self.app.set_unsaved(self.is_unsaved)
        self.toremove = []


# TODO: Copy and Add classes looks very similar. Try to factorize.
class Copy(object):
    """ Undo/redo copy of existing pages in the document """
    def __init__(self, app, ref_from_list, ref_to, before):
        #: A PdfArranger instance
        self.app = app
        #: List of Gtk.TreeRowReference to copy from
        self.ref_from_list = ref_from_list
        #: Gtk.TreeRowReference to copy to
        self.ref_to = ref_to
        #: True to insert before insert_ref, False to insert after
        self.before = before
        #: Gtk.TreeRowReference list to be removed by undo
        self.toremove = []
        self.is_unsaved = app.is_unsaved

    def redo(self):
        m = self.app.model
        for ref_from in self.ref_from_list:
            it_to = m.get_iter(self.ref_to.get_path())
            it_from = m.get_iter(ref_from.get_path())
            row = m[it_from][:]
            if self.before:
                new_it = m.insert_before(it_to, row)
            else:
                new_it = m.insert_after(it_to, row)
            self.toremove.append(Gtk.TreeRowReference.new(m, m.get_path(new_it)))

    def undo(self):
        m = self.app.model
        for p in self.toremove:
            m.remove(m.get_iter(p.get_path()))
        self.app.set_unsaved(self.is_unsaved)
        self.toremove = []


class Move(object):
    """ Undo/redo move of pages in the document """
    def __init__(self, app, ref_from_list, ref_to, before):
        #: A PdfArranger instance
        self.app = app
        #: List of Gtk.TreeRowReference to copy from
        self.ref_from_list = ref_from_list
        #: Gtk.TreeRowReference to copy to
        self.ref_to = ref_to
        #: True to insert before insert_ref, False to insert after
        self.before = before
        self.is_unsaved = app.is_unsaved
        #: Positions of tiles before moving
        self.orig=[]

    def redo(self):
        m = self.app.model
        for ref_from in self.ref_from_list:
            iter_to = m.get_iter(self.ref_to.get_path())
            orig_path = ref_from.get_path()
            orig_before = not orig_path.prev()
            if orig_before:
                orig_path.next()
            self.orig.append((Gtk.TreeRowReference.new(m, orig_path), orig_before, ))
            it_from = m.get_iter(ref_from.get_path())
            if self.before:
                m.move_before(it_from, iter_to)
            else:
                m.move_after(it_from, iter_to)

    def undo(self):
        m = self.app.model
        n = len(self.ref_from_list)
        for i in range(n-1, -1, -1):
            ref_from = self.ref_from_list[i]
            orig_ref, orig_before = self.orig[i]
            iter_to = m.get_iter(orig_ref.get_path())
            it_from = m.get_iter(ref_from.get_path())
            if orig_before:
                m.move_before(it_from, iter_to)
            else:
                m.move_after(it_from, iter_to)
        self.app.set_unsaved(self.is_unsaved)
        self.orig=[]
