# FlexiRPG -- UI for managing the miniature library.
#
# Copyright (C) 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import os

import wx

from orpg.config import Paths
import orpg.lib.ui as ui
from orpg.main import image_library
import orpg.tools.bitmap

IMAGE_DEFAULT = 0
IMAGE_STAR = 1

class MiniatureManager(wx.Dialog):
    def __init__(self, minilib, parent):
        super().__init__(parent, title="Miniatures Library",
                         style=wx.DEFAULT_DIALOG_STYLE)

        self.minilib = minilib

        self.mini_tree = wx.TreeCtrl(self, size=(300, 400), style=wx.TR_HIDE_ROOT)
        self.tree_icons = wx.ImageList(16, 16, False)
        self.tree_icons.Add(orpg.tools.bitmap.create_from_file("tree_default.png"))
        self.tree_icons.Add(orpg.tools.bitmap.create_from_file("tree_star.png"))
        self.mini_tree.SetImageList(self.tree_icons)

        self.root = self.mini_tree.AddRoot("root")
        for mini in self.minilib:
            self._add(mini)

        self.add_btn = wx.Button(self, label="Add")
        self.del_btn = wx.Button(self, label="Delete")

        self.name_text = wx.TextCtrl(self)
        self.preview_image = wx.StaticBitmap(self, size=(200, 200))
        self.preview_image.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.favourite_check = wx.CheckBox(self, label="Favourite")
        self.select_btn = wx.Button(self, id=wx.ID_OK, label="Select")
        self.select_btn.SetDefault()
        self.close_btn = wx.Button(self, id=wx.ID_CANCEL, label="Close")

        self.mini_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_mini_activated)
        self.mini_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_mini_selection_changed)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.del_btn.Bind(wx.EVT_BUTTON, self.on_del)
        self.name_text.Bind(wx.EVT_TEXT, self.on_name_text)
        self.favourite_check.Bind(wx.EVT_CHECKBOX, self.on_favourite)

        col_box = wx.BoxSizer(wx.HORIZONTAL)

        # Left column
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Miniatures"))
        vbox.Add((0, 6))
        vbox.Add(self.mini_tree, 1, wx.EXPAND | wx.LEFT, border=12)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.add_btn)
        hbox.Add(self.del_btn)
        vbox.Add(hbox)
        col_box.Add(vbox, 1, wx.EXPAND)

        col_box.Add((18, 0))

        # Right column
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Name"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.name_text, 1, wx.EXPAND | wx.LEFT, border=12)
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((0, 12))
        vbox.Add(ui.StaticTextHeader(self, label="Preview"))
        vbox.Add((0, 6))
        vbox.Add(self.preview_image, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.LEFT, border=12)
        vbox.Add((0, 12))
        vbox.Add(self.favourite_check)
        col_box.Add(vbox, 0, wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(col_box, 1, wx.EXPAND)
        vbox.Add((0, 12))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.select_btn)
        hbox.Add((6,0))
        hbox.Add(self.close_btn)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT)

        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.box.Add(vbox, 0, wx.ALL, border=12)

        self.SetSizerAndFit(self.box)

    def select(self):
        self._update_controls()
        selected_mini = None
        if self.ShowModal() == wx.ID_OK:
            item = self.mini_tree.GetSelection()
            if item.IsOk():
                selected_mini = self.mini_tree.GetItemData(item)
        self.minilib.save()
        return selected_mini

    def on_mini_activated(self, evt):
        self.EndModal(wx.ID_OK)

    def on_mini_selection_changed(self, evt):
        selection = self.mini_tree.GetSelection()
        self._update_controls()

    def on_add(self, evt):
        d = wx.FileDialog(self.GetParent(), "Add Miniatures to Library",
                          Paths.user(), "",
                          "Images (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                          wx.FD_OPEN | wx.FD_MULTIPLE)
        if d.ShowModal() == wx.ID_OK:
            added = False
            for path in d.GetPaths():
                image = image_library.get_from_file(path)
                if image:
                    name = os.path.splitext(os.path.basename(path))[0].replace("_", " ")
                    mini = self.minilib.add(name, image)
                    self._add(mini)

    def on_del(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        if mini is not None:
            self.minilib.remove(mini)
            self.mini_tree.Delete(item)

    def on_name_text(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        mini.name = self.name_text.Value
        self.mini_tree.SetItemText(item, mini.name)

    def on_favourite(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        if mini.favourite != self.favourite_check.IsChecked():
            mini.favourite = self.favourite_check.IsChecked()
            self.mini_tree.SetItemImage(item, IMAGE_STAR if mini.favourite else IMAGE_DEFAULT)

    def _add(self, mini):
        self.mini_tree.AppendItem(self.root, mini.name,
                                  IMAGE_STAR if mini.favourite else IMAGE_DEFAULT,
                                  data=mini)

    def _update_controls(self):
        item = self.mini_tree.GetSelection()
        if item.IsOk():
            mini = self.mini_tree.GetItemData(item)
        else:
            mini = None
        if mini is not None:
            self.del_btn.Enable(True)
            self.name_text.Enable(True)
            self.name_text.ChangeValue(mini.name)
            self.preview_image.Show()
            self.preview_image.SetBitmap(wx.Bitmap(mini.image()))
            self.favourite_check.Enable(True)
            self.favourite_check.Value = mini.favourite
            self.select_btn.Enable(True)
        else:
            self.del_btn.Enable(False)
            self.name_text.ChangeValue("")
            self.name_text.Enable(False)
            self.preview_image.Hide()
            self.favourite_check.Enable(False)
            self.favourite_check.Value = False
            self.select_btn.Enable(False)
