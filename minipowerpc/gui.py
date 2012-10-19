import sys, os
try:
    import gi

    gi.require_version("Gtk", "3.0")
    # from gi.repository import Gtk,GdkPixbuf,GObject,Pango,Gdk
    from gi.repository import Gtk
except:
    pass

from minipowerpc import MiniPC

class GUI(object):

    def __init__(self):
        self.pc = MiniPC()
        #GObject.threads_init()
        self.gladefile = "minipowerpc.glade"
        self.gladefile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "res", self.gladefile)
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile_path)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("mppc_gui")
        #prog view
        self.progview = self.builder.get_object("treeview_prog")

        self.cell_prog_num = Gtk.CellRendererText()
        self.col_prog_num = Gtk.TreeViewColumn("pos", self.cell_prog_num, text=0)
        self.progview.append_column(self.col_prog_num)

        self.cell_prog_bin = Gtk.CellRendererText()
        self.col_prog_bin = Gtk.TreeViewColumn("bin", self.cell_prog_bin, text=1)
        self.progview.append_column(self.col_prog_bin)

        self.cell_prog_code = Gtk.CellRendererText()
        self.col_prog_code = Gtk.TreeViewColumn("decompiled", self.cell_prog_code, text=2)
        self.progview.append_column(self.col_prog_code)

        self.cell_prog_int = Gtk.CellRendererText()
        self.col_prog_int = Gtk.TreeViewColumn("int value", self.cell_prog_int, text=3)
        self.progview.append_column(self.col_prog_int)

        self.cell_prog_hex = Gtk.CellRendererText()
        self.col_prog_hex = Gtk.TreeViewColumn("hex value", self.cell_prog_hex, text=4)
        self.progview.append_column(self.col_prog_hex)


        #mem view
        self.memview = self.builder.get_object("treeview_mem")

        self.cell_mem_num = Gtk.CellRendererText()
        self.col_mem_num = Gtk.TreeViewColumn("pos", self.cell_mem_num, text=0)
        self.memview.append_column(self.col_mem_num)

        self.cell_mem_bin = Gtk.CellRendererText()
        self.col_mem_bin = Gtk.TreeViewColumn("bin", self.cell_mem_bin, text=1)
        self.memview.append_column(self.col_mem_bin)

        self.cell_mem_int = Gtk.CellRendererText()
        self.col_mem_int = Gtk.TreeViewColumn("int value", self.cell_mem_int, text=2)
        self.memview.append_column(self.col_mem_int)

        self.cell_mem_hex = Gtk.CellRendererText()
        self.col_mem_hex = Gtk.TreeViewColumn("hex value", self.cell_mem_hex, text=3)
        self.memview.append_column(self.col_mem_hex)

        self.txt_steps = self.builder.get_object("txt_steps")
        self.txt_mempos = self.builder.get_object("txt_mempos")
        self.txt_jumps = self.builder.get_object("txt_jumps")
        self.txt_runtime_real = self.builder.get_object("txt_runtime_real")

        self.img_accu_curry = self.builder.get_object("img_accu_curry")
        self.txt_accu_bin = self.builder.get_object("txt_accu_bin")
        self.txt_accu_int = self.builder.get_object("txt_accu_int")
        self.txt_accu_hex = self.builder.get_object("txt_accu_hex")

        self.txt_reg1_bin = self.builder.get_object("txt_reg1_bin")
        self.txt_reg1_int = self.builder.get_object("txt_reg1_int")
        self.txt_reg1_hex = self.builder.get_object("txt_reg1_hex")

        self.txt_reg2_bin = self.builder.get_object("txt_reg2_bin")
        self.txt_reg2_int = self.builder.get_object("txt_reg2_int")
        self.txt_reg2_hex = self.builder.get_object("txt_reg2_hex")

        self.txt_reg3_bin = self.builder.get_object("txt_reg3_bin")
        self.txt_reg3_int = self.builder.get_object("txt_reg3_int")
        self.txt_reg3_hex = self.builder.get_object("txt_reg3_hex")

        self.init_gui()

        self.window.show()

        Gtk.main()

        self.loaded = False

    #helper methods
    def load(self, file):
        print "loading file: ".format(file)
        self.pc.cpu.mem.load(file)
        self.pc.cpu.init()
        self.init_gui()

    def init_gui(self):
        #setup models

        self.memstore = Gtk.ListStore(int, str, int, str)
        self.memview.set_model(self.memstore)
        self.progstore = Gtk.ListStore(int, str, str, int, str)
        self.progview.set_model(self.progstore)

        i = 100
        while True:
            opcode = self.pc.cpu.mem.get(i)
            line = i
            as_bin = opcode.bin
            op = self.pc.cpu.get_operation(opcode)
            if op:
                decom = op.decompile(opcode)
            else:
                decom = "END"
            as_int = opcode.int
            as_hex = opcode.hex
            self.progstore.append([line, as_bin, decom, as_int, as_hex])
            if opcode == self.pc.cpu.END:
                break
            i += 2

        i = 500
        while True:
            opcode = self.pc.cpu.mem.get(i)
            line = i
            as_bin = opcode.bin
            as_int = opcode.int
            as_hex = opcode.hex
            self.memstore.append([line, as_bin, as_int, as_hex])
            if opcode == self.pc.cpu.END:
                break
            i += 2

        self.selection = self.progview.get_selection()

        self.update_gui()

    def update_gui(self):
        self.txt_steps.set_text(str(self.pc.cpu.steps))
        self.txt_mempos.set_text(str(self.pc.cpu.mem.real.bytepos))
        self.txt_jumps.set_text(str(self.pc.cpu.mem.jumps))
        self.txt_runtime_real.set_text(str(self.pc.cpu.exec_time_real))

        if self.pc.cpu.accu.curry:
            self.img_accu_curry.set_from_stock(Gtk.STOCK_YES, Gtk.IconSize.BUTTON)
        else:
            self.img_accu_curry.set_from_stock(Gtk.STOCK_NO, Gtk.IconSize.BUTTON)
        self.txt_accu_bin.set_text(self.pc.cpu.accu.val.bin)
        self.txt_accu_int.set_text("%i"%self.pc.cpu.accu.val.int)
        self.txt_accu_hex.set_text(self.pc.cpu.accu.val.hex)

        self.txt_reg1_bin.set_text(self.pc.cpu.registers['01'].val.bin)
        self.txt_reg1_int.set_text("%i"%self.pc.cpu.registers['01'].val.int)
        self.txt_reg1_hex.set_text(self.pc.cpu.registers['01'].val.hex)

        self.txt_reg2_bin.set_text(self.pc.cpu.registers['10'].val.bin)
        self.txt_reg2_int.set_text("%i"%self.pc.cpu.registers['10'].val.int)
        self.txt_reg2_hex.set_text(self.pc.cpu.registers['10'].val.hex)

        self.txt_reg3_bin.set_text(self.pc.cpu.registers['11'].val.bin)
        self.txt_reg3_int.set_text("%i"%self.pc.cpu.registers['11'].val.int)
        self.txt_reg3_hex.set_text(self.pc.cpu.registers['11'].val.hex)

        self.selection.select_path("{}".format((self.pc.cpu.mem.pos-100)/2))

    # event handlers
    def delete_event(self, event, data=None):
        Gtk.main_quit()
        return False

    def on_compile_event(self, event, data=None):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
          Gtk.FileChooserAction.OPEN,
          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
           Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        #self.add_filters(dialog)
        response = dialog.run()
        filename = False
        if response == Gtk.ResponseType.OK:
            print "Open clicked"
            print "File selected: " + dialog.get_filename()
            filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print "Cancel clicked"

        dialog.destroy()
        if filename:
            compiled_file = self.pc.compiler.compile(filename)
            self.load(compiled_file)

    def on_open_event(self, event, data=None):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        #self.add_filters(dialog)

        response = dialog.run()
        filename = False
        if response == Gtk.ResponseType.OK:
            print "Open clicked"
            print "File selected: " + dialog.get_filename()
            filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print "Cancel clicked"

        dialog.destroy()

        if filename:
            self.load(filename)

    def on_run_event(self, event, data=None):
        pass

    def on_slow_event(self, event, data=None):
        pass

    def on_step_event(self, event, data=None):
        self.pc.cpu.step()
        self.update_gui()
