#!/usr/bin/env python
# vi: sw=4 et
# Copyright 2008 by Kate Scheppke and Wade Brainerd.  
# This file is part of Typing Turtle.
#
# Typing Turtle is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Typing Turtle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Typing Turtle.  If not, see <http://www.gnu.org/licenses/>.

# Import standard Python modules.
import logging, os, math, time, copy, locale, datetime, random, re
from gettext import gettext as _
from port import json
from port import chooser

# Import PyGTK.
import gobject, pygtk, gtk, pango

# Import Sugar UI modules.
import sugar.activity.activity
import sugar.graphics.style
import sugar.mime
import sugar.datastore.datastore

# Import activity modules.
import editlessonscreen

class EditLessonListScreen(gtk.VBox):
    def __init__(self, activity, lessons):
        gtk.VBox.__init__(self)

        self.activity = activity
        self.lessons = lessons

        # Add the header.
        title = gtk.Label()
        title.set_markup("<span size='20000'><b>" + _("Edit Lessons") + "</b></span>")
        title.set_alignment(1.0, 0.0)
        
        stoplabel = gtk.Label(_('Go Back'))
        stopbtn = gtk.Button()
        stopbtn.add(stoplabel)
        stopbtn.connect('clicked', self.stop_clicked_cb)
       
        titlebox = gtk.HBox()
        titlebox.pack_start(stopbtn, False, False, 10)
        titlebox.pack_end(title, False, False, 10)

        # Add the lesson list.
        self.treeview = gtk.TreeView()
        self.treeview.set_rules_hint(True)
        self.treeview.set_enable_search(False)

        self.treeview.connect('cursor-changed', self.lesson_selected_cb)
        self.treeview.connect('row-activated', self.lesson_activated_cb)

        # Note that the only thing we store in our liststore is the lesson id.
        # All the actual data is in the lessons list.
        self.liststore = gtk.ListStore(gobject.TYPE_INT)
        self.treeview.set_model(self.liststore)

        # Construct the columns.
        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(_('Name'), renderer)
        col.set_cell_data_func(renderer, self.name_render_cb) 
        self.treeview.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(_('Description'), renderer)
        col.set_cell_data_func(renderer, self.description_render_cb) 
        col.set_expand(True)
        self.treeview.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(_('Type'), renderer)
        col.set_cell_data_func(renderer, self.type_render_cb) 
        col.set_expand(False)
        self.treeview.append_column(col)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self.treeview)

        importlabel = gtk.Label(_('Import Lessons from Journal'))
        self.importbtn = gtk.Button()
        self.importbtn.add(importlabel)
        self.importbtn.connect('clicked', self.import_clicked_cb)
        
        exportlabel = gtk.Label(_('Export Lessons to Journal'))
        self.exportbtn = gtk.Button()
        self.exportbtn.add(exportlabel)
        self.exportbtn.connect('clicked', self.export_clicked_cb)
        
        self.addbtn = gtk.Button()
        self.addbtn.add(sugar.graphics.icon.Icon(icon_name='list-add'))
        self.addbtn.connect('clicked', self.add_lesson_clicked_cb)
        self.delbtn = gtk.Button()
        self.delbtn.add(sugar.graphics.icon.Icon(icon_name='list-remove'))
        self.delbtn.connect('clicked', self.del_lesson_clicked_cb)
        self.delbtn.set_sensitive(False)
        self.moveupbtn = gtk.Button()
        self.moveupbtn.add(sugar.graphics.icon.Icon(icon_name='go-up'))
        self.moveupbtn.connect('clicked', self.move_lesson_up_clicked_cb)
        self.moveupbtn.set_sensitive(False)
        self.movedownbtn = gtk.Button()
        self.movedownbtn.add(sugar.graphics.icon.Icon(icon_name='go-down'))
        self.movedownbtn.connect('clicked', self.move_lesson_down_clicked_cb)
        self.movedownbtn.set_sensitive(False)

        btnbox = gtk.HBox()
        btnbox.pack_start(self.importbtn, False, False, 10)
        btnbox.pack_start(self.exportbtn, False, False)
        btnbox.pack_end(self.addbtn, False, False)
        btnbox.pack_end(self.delbtn, False, False)
        btnbox.pack_end(self.moveupbtn, False, False)
        btnbox.pack_end(self.movedownbtn, False, False)

        self.pack_start(titlebox, False, False, 10)
        self.pack_start(gtk.HSeparator(), False, False, 0)
        self.pack_start(scroll, True, True, 10)
        self.pack_start(btnbox, False, False, 10)

        self.build()

        self.show_all()
    
    def build(self):
        # Fill the lesson list.
        self.liststore.clear()
        for t in range(0, len(self.lessons)):
            self.liststore.append((0,))
    
    def name_render_cb(self, column, cell_renderer, model, iter):
        id = model.get_path(iter)[0]
        t = self.lessons[id]
        cell_renderer.set_property('text', t['name'])
    
    def description_render_cb(self, column, cell_renderer, model, iter):
        id = model.get_path(iter)[0]
        t = self.lessons[id]
        cell_renderer.set_property('text', t['description'])

    def type_render_cb(self, column, cell_renderer, model, iter):
        id = model.get_path(iter)[0]
        t = self.lessons[id]
        if t['type'] == 'normal':
            cell_renderer.set_property('text', _('Text'))
        if t['type'] == 'balloon':
            cell_renderer.set_property('text', _('Balloon Game'))

    def stop_clicked_cb(self, btn):
        # Assign lesson order.
        num = 0
        for l in self.lessons:
            l['order'] = num
            num = num + 1
        
        # Refresh the main screen given the new lesson data.
        if self.activity.mainscreen.lesson_index >= len(self.lessons):
            self.activity.mainscreen.lesson_index = len(self.lessons) - 1
        self.activity.mainscreen.show_lesson(self.activity.mainscreen.lesson_index)
        
        self.activity.pop_screen()
    
    def add_lesson_clicked_cb(self, btn):
        lesson = {}
        lesson['name'] = ''
        lesson['description'] = ''
        lesson['type'] = 'normal'
        lesson['steps'] = [ { 'instructions':'', 'text':'' } ]
        lesson['medals'] = [ 
            { 'name': 'bronze', 'wpm': 15, 'accuracy': 70, 'score': 3000 },
            { 'name': 'silver', 'wpm': 20, 'accuracy': 80, 'score': 4500 },
            { 'name': 'gold',   'wpm': 25, 'accuracy': 90, 'score': 6000 },
        ]
        self.lessons.append(lesson)
        self.activity.push_screen(editlessonscreen.EditLessonScreen(self.activity, lesson))
        self.liststore.append()

    def del_lesson_clicked_cb(self, btn):
        if len(self.lessons) > 1:
            path = self.treeview.get_cursor()[0]
            if path:
                id = path[0]
                self.lessons.pop(id)
                del self.liststore[id]
                self.treeview.get_selection().select_path(id)
                self.treeview.grab_focus()
                self.update_sensitivity()

    def move_lesson_up_clicked_cb(self, btn):
        path = self.treeview.get_cursor()[0]
        if path:
            id = path[0]
            if id > 0:
                lesson = self.lessons.pop(id)
                self.lessons.insert(id - 1, lesson)
                self.liststore.swap(self.liststore.get_iter(id), self.liststore.get_iter(id - 1))
                self.treeview.get_selection().select_path(id - 1)
                self.treeview.grab_focus()
                self.update_sensitivity()

    def move_lesson_down_clicked_cb(self, btn):
        path = self.treeview.get_cursor()[0]
        if path:
            id = path[0]
            if id < len(self.lessons) - 1:
                lesson = self.lessons.pop(id)
                self.lessons.insert(id + 1, lesson)
                self.liststore.swap(self.liststore.get_iter(id), self.liststore.get_iter(id + 1))
                self.treeview.get_selection().select_path(id + 1)
                self.treeview.grab_focus()
                self.update_sensitivity()

    def lesson_selected_cb(self, treeview):
        self.update_sensitivity()

    def lesson_activated_cb(self, treeview, path, column):
        id = path[0]
        lesson = self.lessons[id]
        self.activity.push_screen(editlessonscreen.EditLessonScreen(self.activity, lesson))

    def enter(self):
        self.update_sensitivity()

    def update_sensitivity(self):
        path = self.treeview.get_cursor()[0]
        
        if path:
            self.delbtn.set_sensitive(True)
            
            if path[0] > 0:
                self.moveupbtn.set_sensitive(True)
            else:
                self.moveupbtn.set_sensitive(False)
                
            if path[0] < len(self.lessons) - 1:
                self.movedownbtn.set_sensitive(True)
            else:
                self.movedownbtn.set_sensitive(False)
                
        else:
            self.delbtn.set_sensitive(False)
            self.moveupbtn.set_sensitive(False)
            self.movedownbtn.set_sensitive(False)
            
        
    def import_clicked_cb(self, btn):
        jobject = chooser.pick(None, None, self, 'text/x-typing-turtle-lessons')
        
        if jobject and jobject.file_path:
            fd = open(jobject.file_path, 'r')
            
            try:
                data = json.loads(fd.read())
                
                # Replace lessons without destroying the object.
                while len(self.lessons):
                    self.lessons.pop()
                for l in data['lessons']:
                    self.lessons.append(l)
                self.build()
            
            finally:
                fd.close()
    
    def export_clicked_cb(self, btn):
        # Create the new journal entry
        fileObject = sugar.datastore.datastore.create()

        meta = self.activity.metadata
        fileObject.metadata['title'] = meta['title'] + _(' (Exported Lessons)')
        fileObject.metadata['title_set_by_user'] = meta['title_set_by_user']
        fileObject.metadata['mime_type'] = 'text/x-typing-turtle-lessons'
        fileObject.metadata['icon-color'] = meta['icon-color']
        fileObject.file_path = os.path.join(self.activity.get_activity_root(), 'instance', '%i' % time.time())
        
        fd = open(fileObject.file_path, 'w')
        
        try:
            data = { 'lessons': self.lessons }
            fd.write(json.dumps(data))
            
        finally:
            fd.close()
        
        sugar.datastore.datastore.write(fileObject, transfer_ownership=True)
        fileObject.destroy()
        del fileObject

     