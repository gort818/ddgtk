#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte, GLib

from subprocess import call
import os
def get_data():
    drives="""lsblk -l -o name,size,model,hotplug  | tr -s "\n "| tr -s " " | grep -v MODEL | grep '1$' | grep -v 'sd.[0-9]' | sed 's/^/\/dev\//' | sed 's/.$//'"""
    info=os.popen(drives)

    now=info.read()

    now =now.split('\n')
    now.remove('')
    #print(now)
    #new=dict(zip(now[::2],now[1::2]))
    new_list=[]
    for i in range(len(now)):
        new_list.append(i)
    my_dict=dict(zip(new_list,now))
    
    return my_dict

class launcher:
    def __init__(self):
        
        self.terminal = Vte.Terminal()

        self.builder = Gtk.Builder()
        #GObject.type_register(Vte.Terminal)

        self.builder.add_from_file("ddgtk.glade")

        self.builder.connect_signals(self)
        
        self.window = self.builder.get_object('window')
        self.window.connect('destroy', lambda w: Gtk.main_quit())
        icontheme = Gtk.IconTheme.get_default()
        self.icon = icontheme.load_icon(Gtk.STOCK_FLOPPY, 128, 0)
        self.combo=self.builder.get_object('combo')
        self.box=self.builder.get_object('box')
        self.expander=self.builder.get_object('expander')
        self.s_window=self.builder.get_object('s_window')
        self.term=self.builder.get_object('term')
        self.s_window.add(self.terminal)
        self.file = self.builder.get_object('file')
        self.refresh=self.builder.get_object('refresh')
        self.done_button=self.builder.get_object('done_button')
        self.create_disk_message=self.builder.get_object('create_disk_message')
        self.confirm=self.builder.get_object('confirm')
        self.confirm_ok=self.builder.get_object('confirm_ok')
        a=0
        self.confirm_cancel=self.builder.get_object("confirm_cancel")
        self.terminal.connect('child-exited',self.done)
        self.filter=Gtk.FileFilter()
        self.filter.set_name("ISO files")
        self.filter.add_pattern("*.iso")
        self.file.add_filter(self.filter)
        self.no_file_message=self.builder.get_object('no_file_message')
        self.ok_no_file_button=self.builder.get_object('ok_no_file_button')
        self.warning_label=self.builder.get_object('warning_label')
        self.create_disk_label=self.builder.get_object('create_disk_label')
        self.window.show()
        self.pop_combo()
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ['/bin/sh'],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
        #self.terminal.show()
    def on_file_set(self,widget):
        print(self.file.get_filename())
        self.filename=self.file.get_filename()
    def pop_combo(self):
        my_dict=get_data()
        #self.combo.insert_text(now[0],now[1])
        for key,values in my_dict.items():
            self.combo.insert_text(int(key),values)
        return my_dict
    def on_combo_changed(self,widget):
        self.device=(self.combo.get_active_text())
        self.device=self.device.split(' ')[0]
        call(["lsblk",self.device])
    def on_start_clicked(self,widget):
        
        if (self.file.get_filename()) == None:
            print("No file selected")
            self.no_file_message.show()
        elif (self.combo.get_active_text()) == None:
            self.warning_label.set_text("Warning: No Device Selected")
            self.no_file_message.show()
            print("No device selected")
        else:
            print("let's go")
            self.confirm.show()
        #self.terminal.show()
        #self.command = "pkexec cat /etc/shadow \n"
        #self.terminal.feed_child(self.command,-1)
        #call([, 'ls'])
    def dd(self):
        self.create_disk_message.show()
        clear="stty -echo ;clear \n"
        wait="echo 'Writing to disk please wait!'\n"
        self.umount= "umount " + self.device+"*" + " &>/dev/null \n"
        self.command = "pkexec dd if="+self.filename+" of="+self.device+" status=progress && sync;exit \n"
        self.terminal.feed_child(clear,-1)
        self.terminal.feed_child(wait,-1)
        self.terminal.feed_child(self.umount,-1)
        #self.terminal.feed_child(cmd,-1)
        self.terminal.feed_child(self.command,-1)
        
        #self.terminal.set_input_enabled(False)
        
    def on_expander_activate(self,widget):
        self.terminal.set_rewrap_on_resize(True)
        self.terminal.show()
        
    def on_no_file_button_clicked(self,widget):
        self.no_file_message.hide()
    def on_done_button_clicked(self,widget):
        self.create_disk_message.hide()
        self.terminal.hide()
    def on_refresh_clicked(self,widget):
        self.window.destroy()
        main()
    def on_confirm_ok_clicked(self,widget):
        self.confirm.hide()
        self.dd()
    def on_confirm_cancel_clicked(self,widget):
        self.confirm.hide()
        return
        
    def done (self,terminal,a):
        print("All done")
        self.done_button.set_visible(True)
        self.create_disk_label.set_text("Finshed!\n Click the done Button :)")
        
        
def main():

    launcher()
    Gtk.main()


if __name__ == '__main__':
    main()
