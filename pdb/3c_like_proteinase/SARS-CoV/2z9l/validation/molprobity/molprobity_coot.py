# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', '  43 ', 'ILE', 0.08274497807812291, (29.31499999999999, -17.39099999999999, -8.724)), ('A', '  51 ', 'ASN', 0.06757319657560867, (22.92800000000001, -23.595, 0.648)), ('B', '  47 ', 'GLU', 0.028435152433393472, (53.917, -62.925999999999995, -50.398)), ('B', '  48 ', 'ASP', 0.010262827196282147, (56.85499999999999, -60.612, -49.726)), ('B', '  49 ', 'MET', 0.0485900730946157, (56.266000000000005, -60.86199999999999, -45.95499999999999)), ('B', '  51 ', 'ASN', 0.0, (60.993999999999986, -62.60099999999999, -45.883999999999986)), ('B', ' 191 ', 'ALA', 0.040781077657622664, (57.53999999999999, -68.21099999999997, -35.822)), ('B', ' 216 ', 'ASP', 0.010510385848638802, (42.275, -48.23399999999999, 0.801))]
data['omega'] = []
data['rota'] = [('A', '   4 ', 'ARG', 0.022439603094659734, (40.774000000000015, -52.54, -24.088)), ('A', '   5 ', 'LYS', 0.0, (38.67600000000001, -50.173, -22.042)), ('A', '  60 ', 'ARG', 0.005422759366572195, (25.58299999999999, -8.879, -7.476)), ('A', '  75 ', 'LEU', 0.0033411421655560637, (36.786, -13.908999999999999, -24.231)), ('A', '  86 ', 'LEU', 0.014447017006209659, (24.344000000000012, -24.335000000000008, -15.188)), ('A', '  87 ', 'LEU', 0.019842427902197486, (25.6, -20.85, -16.173)), ('A', ' 153 ', 'ASP', 0.18398475587302018, (28.599999999999994, -40.777, -33.074)), ('A', ' 222 ', 'ARG', 0.22442749645040783, (24.786000000000005, -76.12, -23.307999999999993)), ('A', ' 227 ', 'LEU', 0.00036746888214492923, (14.89, -64.661, -16.978)), ('A', ' 253 ', 'LEU', 0.0, (25.483, -59.30400000000001, -30.268)), ('B', '  56 ', 'ASP', 0.1310456734543209, (64.964, -54.323, -53.101)), ('B', '  75 ', 'LEU', 0.07225819617681828, (48.88, -35.166999999999994, -50.547)), ('B', '  77 ', 'VAL', 0.12379801195879395, (54.671, -37.032999999999994, -52.176)), ('B', '  87 ', 'LEU', 0.0510260164529506, (59.188, -45.095, -44.464)), ('B', ' 168 ', 'PRO', 0.1067800770056678, (51.16400000000001, -65.334, -31.93799999999999)), ('B', ' 216 ', 'ASP', 0.21038514230648908, (42.275, -48.23399999999999, 0.801)), ('B', ' 228 ', 'ASN', 0.07174938469090703, (67.42199999999997, -57.788999999999994, -0.632)), ('B', ' 253 ', 'LEU', 0.06977680636415323, (55.21600000000001, -40.64, -2.9)), ('B', ' 268 ', 'LEU', 0.07287765083493462, (53.515000000000015, -56.17399999999999, -1.099)), ('B', ' 288 ', 'GLU', 0.06370282548696188, (47.985000000000014, -53.596, -11.317))]
data['cbeta'] = []
data['probe'] = [(' B  44  CYS  HB3', ' B  57  LEU HD13', -1.005, (57.928, -55.25, -50.593)), (' B 107  GLN  H  ', ' B 110  GLN HE21', -0.901, (61.755, -46.129, -21.706)), (' B 226  THR HG23', ' B 229  ASP  H  ', -0.842, (66.356, -57.246, 1.649)), (' B 198  THR HG21', ' B 883  HOH  O  ', -0.834, (61.002, -57.75, -15.911)), (' B 280  THR HG22', ' B 285  THR HG22', -0.809, (38.781, -57.701, -6.358)), (' A 294  PHE  HB2', ' A 920  HOH  O  ', -0.804, (24.931, -49.91, -28.759)), (' B  49  MET  HB3', ' B 189  GLN  HG2', -0.804, (54.689, -61.632, -44.224)), (' B 226  THR  CG2', ' B 229  ASP  H  ', -0.787, (65.842, -57.419, 2.112)), (' A   4  ARG  HB2', ' B 139  SER  HB2', -0.782, (42.182, -52.378, -26.873)), (' A   6  MET  HE3', ' A 299  GLN  HG3', -0.772, (38.442, -51.089, -29.503)), (' A 106  ILE  HB ', ' A 110  GLN HE21', -0.758, (23.766, -42.994, -21.432)), (' A  27  LEU HD22', ' A  39  PRO  HG2', -0.73, (32.369, -24.641, -12.731)), (' A 276  MET  HE1', ' A 280  THR  HA ', -0.706, (39.02, -65.113, -16.415)), (' A  51  ASN  HA ', ' A 188  ARG  HG3', -0.702, (22.755, -24.59, -0.54)), (' B  44  CYS  HB3', ' B  57  LEU  CD1', -0.701, (58.334, -56.256, -50.259)), (' B  87  LEU HD22', ' B  89  LEU HD21', -0.695, (56.921, -43.982, -48.54)), (' A 102  LYS  HE3', ' A 156  CYS  SG ', -0.687, (24.658, -35.141, -33.088)), (' B 190  THR  OG1', ' B 192  GLN  HG3', -0.68, (58.743, -64.027, -36.523)), (' A 137  LYS  NZ ', ' A 756  HOH  O  ', -0.676, (29.942, -47.661, -7.531)), (' B 107  GLN  N  ', ' B 110  GLN HE21', -0.675, (61.534, -46.065, -21.893)), (' B 107  GLN  O  ', ' B 110  GLN  HG3', -0.634, (60.294, -47.534, -20.62)), (' A 236  LYS  HE3', ' A 841  HOH  O  ', -0.632, (18.015, -63.789, -4.691)), (' B 277  ASN  HA ', ' B 878  HOH  O  ', -0.63, (42.02, -65.171, -0.485)), (' A 188  ARG  HG2', ' A 189  GLN  N  ', -0.629, (25.184, -27.153, -0.232)), (' A   6  MET  CE ', ' A 299  GLN  HG3', -0.622, (38.924, -50.725, -29.505)), (' B 226  THR HG22', ' B 229  ASP  HB2', -0.618, (65.168, -57.846, 2.916)), (' A   4  ARG  HG3', ' A   4  ARG HH11', -0.617, (43.852, -51.192, -22.554)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.613, (50.549, -32.501, -42.829)), (' B 132  PRO  HG2', ' B 198  THR HG22', -0.608, (58.471, -58.057, -17.133)), (' B  44  CYS  HB2', ' B  48  ASP  CB ', -0.603, (56.205, -57.485, -49.757)), (' A  81  SER  O  ', ' A  87  LEU HD13', -0.602, (24.21, -18.194, -16.838)), (' B  22  CYS  SG ', ' B  61  LYS  HE3', -0.595, (54.41, -48.715, -52.113)), (' A 286  ILE  O  ', ' A 286  ILE HD12', -0.593, (36.468, -58.23, -14.877)), (' B  44  CYS  SG ', ' B  54  TYR  CE2', -0.593, (57.615, -54.761, -46.94)), (' B 132  PRO  CB ', ' B 198  THR HG22', -0.593, (58.996, -57.878, -17.797)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.589, (25.759, -48.972, -16.45)), (' B 102  LYS  HD3', ' B 925  HOH  O  ', -0.587, (62.066, -32.061, -27.742)), (' B 200  ILE HG21', ' B 203  ASN  ND2', -0.584, (55.37, -50.777, -14.888)), (' A 286  ILE HD11', ' A 288  GLU  OE2', -0.583, (37.478, -56.184, -15.089)), (' A 605  DMS  H23', ' A 753  HOH  O  ', -0.581, (34.882, -50.025, -27.252)), (' B  87  LEU HD22', ' B  89  LEU  CD2', -0.573, (57.414, -43.413, -48.516)), (' B 288  GLU  HG3', ' B 850  HOH  O  ', -0.568, (44.634, -51.79, -13.732)), (' A 297  VAL  O  ', ' A 301  SER  HB3', -0.568, (32.275, -53.2, -33.724)), (' B 210  ALA  HB2', ' B 296  VAL HG13', -0.559, (48.803, -43.208, -7.405)), (' B 226  THR HG22', ' B 229  ASP  CB ', -0.559, (65.409, -58.679, 2.661)), (' A 286  ILE  C  ', ' A 286  ILE HD12', -0.557, (36.085, -58.356, -14.154)), (' B  31  TRP  CD2', ' B  95  ASN  HB2', -0.553, (50.608, -32.714, -42.668)), (' A 107  GLN  H  ', ' A 110  GLN  NE2', -0.551, (21.585, -43.251, -20.831)), (' A 106  ILE  HB ', ' A 110  GLN  NE2', -0.549, (23.212, -42.667, -21.588)), (' B 107  GLN  H  ', ' B 110  GLN  NE2', -0.546, (61.565, -45.24, -21.378)), (' A 111  THR HG22', ' A 129  ALA  HB2', -0.544, (30.449, -47.361, -17.957)), (' B 153  ASP  O  ', ' B 154  TYR  HB2', -0.54, (54.904, -29.843, -22.569)), (' A 154  TYR  HB2', ' A 889  HOH  O  ', -0.54, (27.421, -38.438, -36.976)), (' B 132  PRO  HG2', ' B 198  THR  CG2', -0.538, (58.023, -57.646, -16.577)), (' B 221  ASN HD22', ' B 270  GLU  CD ', -0.538, (52.058, -58.127, 5.566)), (' B  86  LEU HD13', ' B 179  GLY  HA2', -0.537, (60.569, -47.803, -37.581)), (' A 227  LEU HD12', ' A 244  GLN HE21', -0.534, (12.704, -61.509, -19.521)), (' A 140  PHE  HB3', ' A 144  SER  OG ', -0.533, (37.339, -32.986, -10.82)), (' A  62  SER  O  ', ' A  65  SER  HB2', -0.532, (30.498, -10.209, -13.702)), (' B 175  THR HG22', ' B 181  PHE  HA ', -0.532, (60.859, -51.63, -33.928)), (' A   5  LYS  HE2', ' A 752  HOH  O  ', -0.53, (35.695, -48.407, -17.608)), (' A 165  MET  HA ', ' A 604  DMS  H12', -0.529, (33.069, -31.221, -7.178)), (' A  51  ASN  N  ', ' A  52  PRO  CD ', -0.527, (24.645, -23.532, -0.053)), (' B 108  PRO  HD3', ' B 853  HOH  O  ', -0.524, (62.968, -50.388, -23.447)), (' A  74  GLN  HG2', ' A 922  HOH  O  ', -0.524, (43.642, -12.815, -21.342)), (' B 132  PRO  CG ', ' B 198  THR HG22', -0.523, (58.539, -57.444, -17.273)), (' B 233  VAL  O  ', ' B 236  LYS  HB3', -0.52, (59.402, -65.086, -4.959)), (' A 294  PHE  CD2', ' A 298  ARG  NH1', -0.515, (28.52, -46.881, -29.523)), (' A  78  ILE HG13', ' A  90  LYS  HD3', -0.513, (26.354, -11.903, -25.893)), (' A 295  ASP  OD1', ' A 298  ARG  NH2', -0.511, (31.016, -47.285, -26.673)), (' B  48  ASP  HB3', ' B  52  PRO  HB3', -0.51, (58.477, -58.924, -49.059)), (' A  60  ARG  HG2', ' A  60  ARG HH11', -0.509, (23.541, -8.903, -5.11)), (' B 276  MET  CE ', ' B 281  ILE HG13', -0.508, (43.804, -55.64, -3.44)), (' A  40  ARG  HD2', ' A  82  MET  SD ', -0.508, (21.799, -20.997, -11.11)), (' B 236  LYS  HG2', ' B 236  LYS  O  ', -0.508, (58.26, -67.752, -6.449)), (' B 230  PHE  CD1', ' B 265  CYS  HB3', -0.504, (59.115, -54.939, -0.977)), (' A  50  LEU  O  ', ' A  51  ASN  HB3', -0.498, (23.24, -23.062, 2.436)), (' A 153  ASP  O  ', ' A 154  TYR  HB2', -0.496, (28.477, -39.028, -36.177)), (' B 218  TRP  CD2', ' B 279  ARG  HD3', -0.489, (41.824, -56.199, 1.812)), (' B 276  MET  HE3', ' B 281  ILE HG13', -0.488, (44.177, -55.237, -3.005)), (' B 276  MET  O  ', ' B 279  ARG  HB2', -0.488, (41.309, -59.384, -0.016)), (' B  52  PRO  HB2', ' B  57  LEU HD11', -0.485, (59.583, -57.312, -49.556)), (' A 276  MET  CE ', ' A 280  THR  HA ', -0.483, (39.075, -65.372, -16.171)), (' B  48  ASP  HA ', ' B 886  HOH  O  ', -0.481, (58.496, -60.654, -51.015)), (' A  53  ASN  O  ', ' A  54  TYR  C  ', -0.48, (21.212, -17.196, -6.218)), (' B 215  GLY  O  ', ' B 216  ASP  C  ', -0.48, (43.642, -47.303, 1.503)), (' A  67  LEU  N  ', ' A  67  LEU HD22', -0.478, (36.061, -12.998, -15.313)), (' A 276  MET  HE2', ' A 279  ARG  O  ', -0.476, (39.455, -66.272, -15.001)), (' B  50  LEU  O  ', ' B  51  ASN  HB2', -0.474, (61.136, -64.641, -45.408)), (' A 167  LEU  HB3', ' A 168  PRO  HD2', -0.474, (28.789, -37.954, -1.361)), (' A 154  TYR  CD1', ' A 154  TYR  N  ', -0.472, (28.571, -41.018, -35.638)), (' B 297  VAL  O  ', ' B 301  SER  HB2', -0.471, (49.747, -35.484, -8.425)), (' B  46  ALA  O  ', ' B  47  GLU  C  ', -0.47, (54.272, -61.761, -49.089)), (' B  44  CYS  HB2', ' B  48  ASP  HB2', -0.468, (55.926, -58.029, -49.493)), (' A  22  CYS  SG ', ' A  61  LYS  NZ ', -0.467, (30.778, -13.946, -9.983)), (' A  40  ARG  NE ', ' A  54  TYR  CD1', -0.466, (22.81, -22.758, -8.464)), (' A  60  ARG  HG2', ' A  60  ARG  NH1', -0.465, (23.289, -9.426, -4.9)), (' B  22  CYS  SG ', ' B  61  LYS  NZ ', -0.465, (53.499, -48.993, -52.738)), (' B  19  GLN  OE1', ' B  26  THR HG21', -0.464, (43.066, -46.313, -46.619)), (' A  43  ILE  O  ', ' A  43  ILE HG13', -0.464, (27.64, -17.294, -7.215)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.463, (52.257, -49.411, -44.748)), (' B 226  THR HG22', ' B 229  ASP  CG ', -0.462, (65.821, -58.496, 3.425)), (' B  22  CYS  SG ', ' B  61  LYS  CE ', -0.461, (54.269, -48.707, -52.338)), (' A 142  ASN HD22', ' A 604  DMS  H21', -0.46, (37.862, -30.855, -5.862)), (' A 298  ARG  HE ', ' A 605  DMS  H22', -0.459, (33.17, -47.639, -28.869)), (' A 235  MET  HE3', ' A 241  PRO  HG3', -0.454, (17.007, -57.021, -8.985)), (' B 100  LYS  HB3', ' B 100  LYS  HE2', -0.453, (57.136, -29.029, -28.801)), (' B 225  THR  OG1', ' B 269  LYS  NZ ', -0.453, (60.971, -58.017, 3.299)), (' B  44  CYS  SG ', ' B  54  TYR  HE2', -0.452, (57.41, -54.772, -46.648)), (' B 218  TRP  CE2', ' B 279  ARG  HD3', -0.451, (41.69, -56.171, 1.444)), (' B  53  ASN  O  ', ' B  57  LEU  HG ', -0.45, (62.219, -55.886, -50.776)), (' A  57  LEU  H  ', ' A  57  LEU HD12', -0.448, (22.934, -15.448, -4.538)), (' A 153  ASP  C  ', ' A 154  TYR  HD1', -0.447, (27.904, -41.205, -35.234)), (' A 256  GLN  HG3', ' A 872  HOH  O  ', -0.447, (29.206, -60.129, -36.499)), (' B 121  SER  HA ', ' B 122  PRO  HD3', -0.445, (41.747, -40.476, -38.502)), (' A 163  HIS  CE1', ' A 172  HIS  HB3', -0.444, (32.321, -36.118, -10.028)), (' A   5  LYS  HA ', ' A 291  PHE  CE2', -0.444, (36.855, -51.16, -22.614)), (' B  50  LEU  O  ', ' B  51  ASN  CB ', -0.443, (60.964, -64.399, -45.652)), (' A   1  SER  HA ', ' B 166  GLU  OE2', -0.442, (45.529, -58.55, -31.574)), (' B 239  TYR  CE1', ' B 272  LEU HD21', -0.441, (53.542, -60.163, -7.553)), (' A 121  SER  HA ', ' A 122  PRO  HD3', -0.441, (42.97, -27.048, -21.635)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.44, (32.935, -37.211, -21.175)), (' B 140  PHE  HB3', ' B 144  SER  OG ', -0.44, (45.921, -52.882, -34.462)), (' A   5  LYS  CE ', ' A 752  HOH  O  ', -0.439, (35.415, -48.497, -17.762)), (' B 231  ASN  O  ', ' B 235  MET  HG3', -0.437, (63.258, -61.369, -5.904)), (' A  57  LEU  N  ', ' A  57  LEU HD12', -0.436, (22.988, -15.07, -4.42)), (' B  49  MET  HB3', ' B 189  GLN  CG ', -0.434, (54.514, -61.934, -43.788)), (' A 163  HIS  HE1', ' A 172  HIS  HB3', -0.434, (32.259, -36.073, -9.88)), (' A   5  LYS  HA ', ' A 291  PHE  CZ ', -0.432, (37.32, -51.081, -22.026)), (' A  51  ASN  CG ', ' A  51  ASN  O  ', -0.432, (21.078, -22.587, 1.01)), (' A 189  GLN  O  ', ' A 190  THR HG23', -0.432, (23.828, -28.812, 1.544)), (' B  56  ASP  O  ', ' B  60  ARG  HG3', -0.431, (63.12, -53.067, -55.537)), (' A 243  THR  H  ', ' A 246  HIS  CD2', -0.43, (17.324, -55.643, -17.906)), (' B 210  ALA  HB2', ' B 296  VAL  CG1', -0.423, (49.207, -43.53, -7.419)), (' A 189  GLN  O  ', ' A 190  THR  CG2', -0.422, (23.597, -28.785, 1.928)), (' B 294  PHE  CD2', ' B 298  ARG  NH2', -0.42, (53.975, -38.391, -15.853)), (' A  50  LEU  N  ', ' A 941  HOH  O  ', -0.417, (28.088, -21.234, 1.364)), (' A 252  PRO  HD2', ' A 711  HOH  O  ', -0.417, (22.799, -56.046, -29.453)), (' A 153  ASP  N  ', ' A 153  ASP  OD1', -0.416, (28.59, -39.976, -31.342)), (' B 243  THR  H  ', ' B 246  HIS  CD2', -0.416, (64.345, -51.473, -9.11)), (' A 276  MET  HE2', ' A 279  ARG  C  ', -0.412, (39.765, -66.662, -15.127)), (' B  45  THR  N  ', ' B  48  ASP  OD1', -0.41, (54.872, -57.308, -50.846)), (' B 294  PHE  HB2', ' B 766  HOH  O  ', -0.41, (57.421, -41.684, -13.238)), (' B 118  TYR  CE1', ' B 144  SER  HB3', -0.407, (43.363, -51.145, -36.473)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.405, (50.308, -43.702, -27.731)), (' A  51  ASN  CA ', ' A 188  ARG  HG3', -0.405, (23.299, -24.728, 0.144)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.404, (39.895, -31.582, -11.935)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.403, (41.388, -32.991, -22.455)), (' B 298  ARG  NH1', ' B 606  DMS  S  ', -0.402, (49.321, -39.331, -17.093)), (' B 217  ARG  HD2', ' B 791  HOH  O  ', -0.4, (44.929, -44.875, 4.04))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
