# main.py
#
# Copyright (C) 2017 Alessandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi
import time
gi.require_version('Gtk', '3.0')
#gi.require_version('Vte', '2.91')
from gi.repository import Gtk, GLib,Gio

from subprocess import call,run,PIPE,Popen
import os
def get_data():
    drives="""lsblk -l -o name,size,model,hotplug  | tr -s "\n "| tr -s " " | grep -v MODEL | grep '1$' | grep -v 'sd.[0-9]'| grep sd | sed 's/^/\/dev\//' | sed 's/.$//'"""
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




class Application():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_resource('/org/gnome/Ddgtk/window.ui')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window')
        self.window.connect('destroy', lambda w: Gtk.main_quit())
        #icontheme = Gtk.IconTheme.get_default()
        #self.icon = icontheme.load_icon(drive-removable-media, 128, 0)
        self.combo=self.builder.get_object('combo')
        self.option_box=self.builder.get_object('option_box')
        self.box=self.builder.get_object('box')
        self.expander=self.builder.get_object('expander')
        self.s_window=self.builder.get_object('s_window')
        self.spinner=self.builder.get_object('spinner')
        self.file = self.builder.get_object('file')
        self.refresh=self.builder.get_object('refresh')
        self.done_button=self.builder.get_object('done_button')
        self.create_disk_message=self.builder.get_object('create_disk_message')
        self.confirm=self.builder.get_object('confirm')
        self.confirm_ok=self.builder.get_object('confirm_ok')
        self.confirm_cancel=self.builder.get_object("confirm_cancel")
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

    def on_file_set(self,widget):
        print(self.file.get_filename())
        self.filename=self.file.get_filename()
        file_width=len(os.path.basename(self.filename))
        print(file_width)
        self.file.set_width_chars (file_width)
    def pop_combo(self):
        my_dict=get_data()
        #self.combo.insert_text(now[0],now[1])
        for key,values in my_dict.items():
            self.combo.insert_text(int(key),values)
        return my_dict
    def on_combo_changed(self,widget):
        self.device=(self.combo.get_active_text())
        if self.device is None:
            return
        self.device=self.device.split(' ')[0]
        call(["lsblk",self.device])
    def on_option_box_changed(self,widget):
        print("option changed")
        self.option=(self.option_box.get_active_text())
        print(self.option)

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

    def dd(self):
        self.create_disk_message.show()
        self.option=(self.option_box.get_active_text())
        #self.create_disk_message.show()
        self.umount= self.device+"?*"
        self.command = "if="+self.filename
        self.command2= "of="+self.device
        print(self.command)
        p = call(["umount " + self.umount],shell=True)

        subprocess = Gio.Subprocess.new(['/usr/bin/pkexec','/usr/bin/dd', self.command,self.command2], Gio.SubprocessFlags.STDOUT_PIPE)
        subprocess.wait_check_async(None, self.done)


    def on_no_file_button_clicked(self,widget):
        self.no_file_message.hide()
    def on_done_button_clicked(self,widget):
        self.create_disk_message.hide()
        self.window.destroy()
        main()
    def on_refresh_clicked(self,widget):
        #self.window.destroy()
        #main()
        self.combo.hide()
        self.combo.remove_all()
        self.pop_combo()
        self.combo.show()
    def on_confirm_ok_clicked(self,widget):
        self.confirm.hide()
        self.dd()
    def on_confirm_cancel_clicked(self,widget):
        self.confirm.hide()
        return

    def done (self,subprocess,result):
        subprocess.wait_check_finish(result)
        print("All done")
        self.spinner.hide()
        self.done_button.set_visible(True)
        self.create_disk_label.set_text("Finshed!\n Click the done Button :)")


def main():
    Application()
    Gtk.main()
