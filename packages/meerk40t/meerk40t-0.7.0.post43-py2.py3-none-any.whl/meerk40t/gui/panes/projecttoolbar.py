import wx

ID_MAIN_TOOLBAR = wx.NewId()
ID_ADD_FILE = wx.NewId()
ID_OPEN = wx.NewId()

ID_SAVE = wx.NewId()
ID_NAV = wx.NewId()
ID_USB = wx.NewId()
ID_CONTROLLER = wx.NewId()
ID_CONFIGURATION = wx.NewId()
ID_DEVICES = wx.NewId()
ID_CAMERA = wx.NewId()
ID_CAMERA1 = wx.NewId()
ID_CAMERA2 = wx.NewId()
ID_CAMERA3 = wx.NewId()
ID_CAMERA4 = wx.NewId()
ID_CAMERA5 = wx.NewId()
ID_JOB = wx.NewId()
ID_SIM = wx.NewId()
ID_PAUSE = wx.NewId()
ID_STOP = wx.NewId()

ID_SPOOLER = wx.NewId()
ID_KEYMAP = wx.NewId()
ID_SETTING = wx.NewId()
ID_NOTES = wx.NewId()
ID_OPERATIONS = wx.NewId()
ID_CONSOLE = wx.NewId()
ID_ROTARY = wx.NewId()
ID_RASTER = wx.NewId()

from ..icons import (
    icon_meerk40t,
    icons8_administrative_tools_50,
    icons8_camera_50,
    icons8_comments_50,
    icons8_computer_support_50,
    icons8_connected_50,
    icons8_console_50,
    icons8_direction_20,
    icons8_emergency_stop_button_50,
    icons8_fantasy_50,
    icons8_file_20,
    icons8_group_objects_20,
    icons8_home_filled_50,
    icons8_keyboard_50,
    icons8_laser_beam_20,
    icons8_laser_beam_52,
    icons8_laser_beam_hazard2_50,
    icons8_lock_50,
    icons8_manager_50,
    icons8_move_50,
    icons8_opened_folder_50,
    icons8_padlock_50,
    icons8_pause_50,
    icons8_play_50,
    icons8_roll_50,
    icons8_route_50,
    icons8_save_50,
    icons8_scatter_plot_20,
    icons8_system_task_20,
    icons8_vector_20,
)

_ = wx.GetTranslation


class ProjectToolBar(wx.ToolBar):
    def __init__(self, *args, context, gui, **kwds):
        # begin wxGlade: wxToolBar.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.ToolBar.__init__(self, *args, **kwds)
        self.context = context
        self.gui = gui

        self.AddTool(
            ID_OPEN,
            _("Open"),
            icons8_opened_folder_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Opens new project",
        )
        self.AddTool(
            ID_SAVE,
            _("Save"),
            icons8_save_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Saves a project to disk",
            "",
        )
        self.AddSeparator()
        self.Bind(wx.EVT_TOOL, gui.on_click_open, id=ID_OPEN)
        self.Bind(wx.EVT_TOOL, gui.on_click_save, id=ID_SAVE)

        self.AddTool(
            ID_JOB,
            _("Execute Job"),
            icons8_laser_beam_52.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Execute the current laser project",
            "",
        )
        self.Bind(
            wx.EVT_TOOL,
            lambda v: self.context("window toggle ExecuteJob 0\n"),
            id=ID_JOB,
        )
        self.AddTool(
            ID_SIM,
            _("Simulate"),
            icons8_laser_beam_hazard2_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Simulate the current laser job",
            "",
        )
        self.AddTool(
            ID_RASTER,
            _("RasterWizard"),
            icons8_fantasy_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Run RasterWizard ",
            "",
        )
        self.Bind(
            wx.EVT_TOOL,
            lambda v: self.context("window toggle RasterWizard\n"),
            id=ID_RASTER,
        )
        self.AddSeparator()
        self.AddTool(
            ID_NOTES,
            _("Notes"),
            icons8_comments_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Open Notes Window",
            "",
        )
        self.Bind(
            wx.EVT_TOOL,
            lambda v: self.context("window toggle Notes\n"),
            id=ID_NOTES,
        )
        self.AddTool(
            ID_CONSOLE,
            _("Console"),
            icons8_console_50.GetBitmap(),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Open Console Window",
            "",
        )
        self.Bind(
            wx.EVT_TOOL,
            lambda v: self.context("window toggle Console\n"),
            id=ID_CONSOLE,
        )

        def open_simulator(v=None):
            with wx.BusyInfo(_("Preparing simulation...")):
                self.context(
                    "plan0 copy preprocess validate blob preopt optimize\nwindow toggle Simulation 0\n"
                ),

        self.Bind(
            wx.EVT_TOOL,
            open_simulator,
            id=ID_SIM,
        )
        self.SetBackgroundColour((200, 225, 250, 255))

        self.__set_properties()
        self.__do_layout()
        # Tool Bar end

    def __set_properties(self):
        # begin wxGlade: wxToolBar.__set_properties
        self.Realize()
        self.SetLabel("Project")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxToolBar.__do_layout
        pass
        # end wxGlade
