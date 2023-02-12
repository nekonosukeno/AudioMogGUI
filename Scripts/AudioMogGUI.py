import os
import time
import fileinput
import subprocess
import shutil
import glob
import gi
import re
import binascii
from pathlib import Path
from pathlib import WindowsPath
from sys import platform
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# You'll get over it
pwd = os.getcwd
cd = os.chdir
UserInput = "Default"

ScriptDir = pwd()

"""
I learned about pathlib after as I was finishing the beta version. I will correct stuff later.
In the meantime, please enjoy the ignorant snarky comments from the dev version.
I am the cause of my own problems, yes, but, well, the snark isn't totally unjustified.
"""

# Operating System checks to decide how to write/run scripts
def CheckOpSys():
    global OpSys
    if platform == "linux" or platform == "linux2":
        OpSys = "GNU"
    elif platform == "darwin":
        OpSys = "MacOS"
    elif platform == "win32" or platform == "win64":
        OpSys = "Win10"
    else:
        print("OS Check: Not Compatible; Mobile Device suspected") 
        OpSys = "Bad"

CheckOpSys()

def exitdialog():
    print("Sorry! Your operating system is currently incompatible")
    time.sleep(1)
    print("I'm working hard to fix that for you, please check the Github repo for updates!")
    time.sleep(2)
    print("Now exiting AudioMog GUI...")
    time.sleep(2)
    print("Goodbye!")
    exit()

"""
Automated Scripting Section for launching VLC and AudioMog
"""
"""
AUDIOMOG
"""
"""
Unpack Sounds
"""
# Let's add MoogleRunner_Lx.py as a function here. It calls TheMog on Linux machines.
def MoogleRunner_Lx():
    cwd = pwd()
    Mogger = "/./MoogleRunner.sh"
    TheMog = (cwd + Mogger)
    subprocess.call(TheMog)

# We need a function to write the script everytime MoogleRunner.sh is called.
def WriteLinuxMog():
    bangbinbash = "#!/bin/bash"
    cdCWD = "cd ${0%/*}"
    cdMog = "cd ../Binaries/AudioMog/"
    wine = ("wine start AudioMog.exe Input/" + AssetDotExt)
    with open("MoogleRunner.sh", 'w') as command:
        command.write(bangbinbash + "\n")
        command.write("\n")
        command.write(cdCWD + "\n")
        command.write(cdMog + "\n")
        command.write(wine)

# And f**k it, let's add the Windows version too.
def MoogleRunner_Win10():
    cwd = pwd()
    Mogger = "\\MoogleRunner.bat"
    TheMog = (cwd + Mogger)
    subprocess.call(TheMog)

# Same as the WriteLinuxMog but for Windows
def WriteWin10Mog():
    with open("MoogleRunner.bat", 'w') as command:
        command.write("@echo off" + "\n")
        command.write("title MoogleRunner" + "\n")
        command.write("chdir ..\\Binaries\\AudioMog" + "\n")
        command.write("start AudioMog.exe Input\\" + AssetDotExt + "\n")
        command.write("EXIT")

# This little baby makes this program "Multi-Platform"
# Also, I don't own a Mac and have no idea if this'll work for you.
def SummonMog():
    if OpSys == "GNU" or OpSys == "MacOS":
        WriteLinuxMog()
        MoogleRunner_Lx()
    elif OpSys == "Win10":
        WriteWin10Mog()
        MoogleRunner_Win10()
    else:
        exitdialog()

"""
Repacking new sounds
"""
def WriteLxMogKnight():
    bangbinbash = "#!/bin/bash"
    cdCWD = "cd ${0%/*}"
    cdMog = "cd ../Binaries/AudioMog/"
    wine = ("wine start AudioMog.exe " + ProjectPath + "/RebuildSettings.json" + "\n")
    with open("MoogleRunner.sh", 'w') as command:
        command.write(bangbinbash + "\n")
        command.write("\n")
        command.write(cdCWD + "\n")
        command.write(cdMog + "\n")
        command.write(wine)
        command.write("sleep 2" + "\n")
        command.write("exit")

def MogKnightRunner_Lx():
    cwd = pwd()
    Moogler = "/./MoogleRunner.sh"
    MogKnight = (cwd + Moogler)
    subprocess.call(MogKnight)

def WriteW10MogKnight():
    with open("MoogleRunner.bat", 'w') as command:
        command.write("@echo off" + "\n")
        command.write("title MoogleRunner" + "\n")
        command.write("chdir ..\\Binaries\\AudioMog" + "\n")
        command.write("start AudioMog.exe " + ProjectPath + "\\RebuildSettings.json" + "\n")
        command.write("EXIT")

def MogKnightRunner_W10():
    cwd = pwd()
    RenameLater = Path(cwd)
    Moogler = "MoogleRunner.bat"
    MogKnight = RenameLater / Moogler
    subprocess.call(MogKnight)

def SummonMogKnight():
    if OpSys == "GNU" or OpSys == "MacOS":
        WriteLxMogKnight()
        MogKnightRunner_Lx()
    elif OpSys == "Win10":
        WriteW10MogKnight()
        MogKnightRunner_W10()
    else:
        exitdialog()

"""
VLC and cVLC
"""
# Checks duration of the sound so we can decide to run VLC headless or with the player window
def CheckWavSize():
    with open(SendVLC, 'rb') as Check:
        Check.seek(0x16, 0x00)
        ChannelBytes = Check.read(0x01 - 0x00)
        Channels = int(binascii.hexlify(ChannelBytes), 16)
        #Sample rate
        Check.seek(0x18, 0x00)
        sRateBytes = Check.read(0x02 - 0x00)
        sRate = int.from_bytes(sRateBytes, "little")
        #Bit Rate
        Check.seek(0x22, 0x00)
        bRateBytes = Check.read(0x01 - 0x00)
        bRate = int(binascii.hexlify(bRateBytes), 16)
        #Chunk size, or length in bytes of the actual sound data
        Check.seek(0x28, 0x00)
        ChunkBytes = Check.read(0x04 - 0x00)
        Chunk = int.from_bytes(ChunkBytes, "little")
        #Here's our million dollar algorithm. Returns duration in seconds.
        Samples = Chunk/(bRate/8*Channels)
        global SoundDuration
        SoundDuration = Samples/sRate
# We need scripts to launch VLC from whichever operating system we're running on
def SendVLC_lx():
    cwd = pwd()
    VLClauncher = "/./LaunchVLC.sh"
    LaunchVLC = (cwd + VLClauncher)
    subprocess.call(LaunchVLC)

def WriteSendVLC_lx():
    bangbinbash = "#!/bin/bash"
    if SoundDuration <= 4:
        vlc = ("cvlc " + str(SendVLC) + " vlc://quit")
    else:
        vlc = ("vlc " + str(SendVLC) )
    with open("LaunchVLC.sh", 'w') as command:
        command.write(bangbinbash + "\n")
        command.write("\n")
        command.write(vlc)

def SendVLC_w10():
    cwd = pwd()
    VLClauncher = "\\LaunchVLC.bat"
    LaunchVLC = (cwd + VLClauncher)
    subprocess.call(LaunchVLC)

def WriteSendVLC_w10():
    if SoundDuration <= 4:
        vlc = "start VLC -I dummy --dummy-quiet "
        #...said the Windows terminal
    else:
        vlc = "start VLC "
    with open("LaunchVLC.bat", 'w') as command:
        SendVLCw10 = str(SendVLC).replace("/","\\")
        command.write("@echo off" + "\n")
        command.write("title Launch VLC" + "\n")
        command.write(vlc + str(SendVLCw10) + "\n")
        command.write("EXIT")

# This is the end goal of the previous functions, it calls VLC with the sound file to play
def LaunchVLC():
    CheckWavSize()
    if OpSys == "GNU" or OpSys == "MacOS":
        WriteSendVLC_lx()
        SendVLC_lx()
    elif OpSys == "Win10":
        WriteSendVLC_w10()
        SendVLC_w10()
    else:
        exitdialog()

"""
THE MOOGENING
"""
def MoogOverHere():
    print("Selected file: " + AssetName)
    print("Copying file(s) to input folder...")
    # Breakdown the AssetName to set variables for finding stuff
    # Needs to cleaned up with pathlib
    AssetPath, AssetExt = os.path.splitext(AssetName)
    if OpSys == "GNU" or OpSys == "MacOS":
        AssetPathSplit = AssetPath.split('/')
        AssetBaseName = AssetPathSplit[-1]
    elif OpSys == "Win10":
        AssetPathSplit = AssetPath.split('\\')
        AssetBaseName = AssetPathSplit[-1]
    global AssetDotExt
    AssetDotExt = (AssetBaseName + AssetExt)
    # These are global in case I need them elsewhere
    global PairedUAsset
    PairedUAsset = (AssetPath + ".uasset")
    global PairedUExp
    PairedUExp = AssetName
    UExpFile = (AssetBaseName + ".uexp")
    UAssetFile = (AssetBaseName + ".uasset")
    global ProjectFolder
    ProjectFolder = ("/" + AssetBaseName + "_Project")
    cd("../Binaries/AudioMog/Input")
    global InputDir
    InputDir = pwd()
    cd("../Output")
    global OutputPath
    OutputPath = pwd()
    cd(InputDir)
    # If file selected was a .uexp then find the matching .uasset
    # Otherwise, it will just grab the AssetName file
    if AssetName.endswith(".uexp"):
        shutil.copy(PairedUExp, InputDir)
        shutil.copy(PairedUAsset, InputDir)
    else:
        shutil.copy(AssetName, InputDir)
    cd(ScriptDir)
    global ProjectPath
    ProjectPath = (InputDir + ProjectFolder)
    if OpSys == "Win10":
        ProjectPath = ProjectPath.replace("/", "\\")
        OutputPath = OutputPath.replace("/", "\\")
    global AbsolutePath
    AbsolutePath = Path(ProjectPath)

#Copies the asset(s) to the Input folder and runs AudioMog.exe
def MoogIt():
    MoogOverHere()
    SummonMog()

#Moves the new assets to Output/
def MoogOverThere():
    AssetTypes = ["*.uexp", "*.uasset", "*.sab", "*.sabf", "*.mab", "*.mabf", "*.bytes"]
    asset_list = []
    cwd = pwd()
    cd(ProjectPath)
    for type in AssetTypes:
        ThisType = glob.glob(type)
        for file in ThisType:
            asset_list.append(file)
    if OpSys == "GNU" or OpSys == "MacOS":
        for item in asset_list:
            new_asset = (ProjectPath + "/" + item)
            asset_split = new_asset.split("/")
            asset_name = asset_split[-1]
            print("Copying: " + asset_name + " to Output/")
            shutil.copy(new_asset, OutputPath)
    elif OpSys == "Win10":
        for item in asset_list:
            new_asset = (ProjectPath + "\\" + item)
            asset_split = new_asset.split("\\")
            asset_name = asset_split[-1]
            print("Copying: " + asset_name + " to Output\\")
            shutil.copy(new_asset, OutputPath)
    cd(cwd)

def ChocoCure():
    # Moves par-boiled assets to scripts directory for final baking
    AssetTypes = ["*.uexp", "*.uasset"]
    asset_list = []
    cd(ProjectPath)
    for type in AssetTypes:
        ThisType = glob.glob(type)
        for file in ThisType:
            asset_list.append(file)
    if OpSys == "GNU" or OpSys == "MacOS":
        for item in asset_list:
            new_asset = (ProjectPath + "/" + item)
            asset_split = new_asset.split("/")
            asset_name = asset_split[-1]
            print("Moving: " + asset_name + " to Scripts/")
            shutil.move(new_asset, ScriptDir)
    elif OpSys == "Win10":
        for item in asset_list:
            new_asset = (ProjectPath + "\\" + item)
            asset_split = new_asset.split("\\")
            asset_name = asset_split[-1]
            print("Moving: " + asset_name + " to Scripts\\")
            shutil.move(new_asset, ScriptDir)
    cd(ScriptDir)
    os.system('python3 AudioMog_DQXIS_Fixer.py')

def SlimeOverThere():
    # Moves the fixed files back to the Output folder
    AssetTypes = ["*.uexp", "*.uasset"]
    asset_list = []
    for type in AssetTypes:
        ThisType = glob.glob(type)
        for file in ThisType:
            asset_list.append(file)
    if OpSys == "GNU" or OpSys == "MacOS":
        for item in asset_list:
            fixed_asset = (ScriptDir + "/" + item)
            asset_split = fixed_asset.split("/")
            asset_name = asset_split[-1]
            print("Moving: " + asset_name + " to Output/")
            shutil.move(fixed_asset, OutputPath)
    elif OpSys == "Win10":
        for item in asset_list:
            fixed_asset = (ScriptDir + "\\" + item)
            asset_split = fixed_asset.split("\\")
            asset_name = asset_split[-1]
            print("Moving: " + asset_name + " to Output\\")
            shutil.move(fixed_asset, OutputPath)
    

"""
Other Functions
"""
# Open the Project Folder or Output Folder
def OpenProjectDir():
    if OpSys == "GNU":
        subprocess.run(['open', ProjectPath])
    else:
        subprocess.Popen(['explorer', ProjectPath])

def OpenOutputDir():
    if OpSys == "GNU":
        subprocess.run(['open', OutputPath])
    else:
        subprocess.Popen(['explorer', OutputPath])

# These functions work together to populate wavs_list with all .wavs and .hcas
delims = ';|_|\\\\|/|\.'
other_delims = ';|\\\\|/'

def get_wavs_lx():
    cwd = pwd()
    Wavs = (cwd + '/**/*.wav')
    HCAs = (cwd + '/**/*.hca')
    global TheseWavs
    global TheseHCAs
    TheseWavs = glob.glob(Wavs,
                          recursive = True)
    TheseHCAs = glob.glob(HCAs,
                          recursive = True)
    global TheseFiles
    TheseFiles = TheseWavs + TheseHCAs

def get_wavs_w10():
    cwd = pwd()
    Wavs = (cwd + '\\**\\*.wav')
    HCAs = (cwd + '\\**\\*.hca')
    global TheseWavs
    global TheseHCAs
    TheseWavs = glob.glob(Wavs,
                          recursive = True)
    TheseHCAs = glob.glob(HCAs,
                          recursive = True)
    global TheseFiles
    TheseFiles = TheseWavs + TheseHCAs

def get_wavs():
    cd(ProjectPath)
    if OpSys == "GNU":
        get_wavs_lx()
    else:
        get_wavs_w10()
    global wavs_list
    wavs_list = []
    for thing in TheseFiles:
        SlotSplit = re.split(delims,thing)
        NameSplit = re.split(other_delims,thing)
        FileName = NameSplit[-1]
        SlotNO = int(SlotSplit[-2])
        wavs_list.append((FileName, SlotNO))
    wavs_list.sort()
    cd(ScriptDir)

# Preps the list used for the NewSound Tree
# We clear the New Sounds TreeView everytime Add button is clicked,
# so entry_list needs to be defined outside any loops or functions.
entry_list = []
def NewEntry():
    SlotFieldNum = int(SlotFieldTxt)
    entry_list.append((SoundName, SlotFieldNum))

# This is used in summoning MogKnight
# We need to put the right sounds in the right place with the right names.
def ReplaceSounds():
    for OG in wavs_list:
        for new in entry_list:
            # Acts on file pairs whose slot numbers are the same
            if OG[1] == new[1]:
                shutil.copy(new[0], InputDir)
                OGFileName = OG[0]
                global AbsolutePath
                AbsolutePath = Path(ProjectPath)
                OGfile = AbsolutePath / OGFileName
                if OpSys == "GNU" or OpSys == "MacOS":

                    NewPathSplit = new[0].split('/')
                    NewFileName = NewPathSplit[-1]

                    MoveNew = (InputDir + "/" + NewFileName)
                    RenameNew = (ProjectPath + "/" + OGFileName)

                # Our typical bullshit because Windows has to be different
                elif OpSys == "Win10":
                    NewPathSplit = new[0].split('\\')
                    NewPath = Path(InputDir)
                    NewFileName = NewPathSplit[-1]
                    MoveNew = NewPath / NewFileName
                    RenameNew = OGfile
                # Moves new sound to Input/, deletes old sound
                else:
                    exitdialog()
                # Simultaneously moves and renames new sound to old sound name/folder
                shutil.copy(new[0], InputDir)
                os.remove(OGfile)
                os.rename(MoveNew, RenameNew)
            else:
                continue

"""
CONFIG FILE STUFF
"""
DD_List = []
DD_List.append(["Default"])
DD_List.append(["Dragon Quest XI DE"])
def DoTheCook():
    #print(list(wavs_list))
    #print(list(entry_list))
    ReplaceSounds()
    SummonMogKnight()
    entry_list.clear()
    time.sleep(2)

cd(ScriptDir)
# Loads included config files
Win10msg = b'\x5C\x5C\x46\x75\x63\x6B\x5C\x5C\x79\x6F\x75\x5C\x5C\x57\x69\x6E\x64\x6F\x77\x73\x5C\x5C'
if OpSys == "GNU" or OpSys == "MacOS":
    cd("../Config_Files/Game")
    ConfigDir = pwd()
    cd("../../Binaries/AudioMog")
    AMdir = pwd()
    cd(ScriptDir)
    DQXIS_Fixer = ScriptDir + "/AudioMog_DQXIS_Fixer.py"
    CurrentConfig = AMdir + "/TerminalSettings.json"
    DefaultSettings = ConfigDir + "/Default/TerminalSettings.json"
    DQXIS_MS = ConfigDir + "/DQXIS/MS/TerminalSettings.json"
    DQXIS_SB = ConfigDir + "/DQXIS/SB/TerminalSettings.json"
    DQXIS_SS = ConfigDir + "/DQXIS/SS/TerminalSettings.json"
elif OpSys == "Win10":
    #print(codecs.decode(Win10msg, 'u8'))
    cd("..\\Config_Files\\Game")
    ConfigDir = pwd()
    cd("..\\..\\Binaries\\AudioMog")
    AMdir = pwd()
    cd(ScriptDir)
    DQXIS_Fixer = str(WindowsPath(ScriptDir) / "AudioMog_DQXIS_Fixer.py")
    CurrentConfig = str(WindowsPath(AMdir) / "TerminalSettings.json")
    DefaultSettings = str(WindowsPath(ConfigDir) / "Default" / "TerminalSettings.json")
    DQXIS_MS = str(WindowsPath(ConfigDir) / "DQXIS" / "MS" / "TerminalSettings.json")
    DQXIS_SB = str(WindowsPath(ConfigDir) / "DQXIS" / "SB" / "TerminalSettings.json")
    DQXIS_SS = str(WindowsPath(ConfigDir) / "DQXIS" / "SS" / "TerminalSettings.json")
# Loads Default config into memory
with open(DefaultSettings, "r") as StdConfig:
    DefaultConfig = StdConfig.read()
# If it quacks like a dog... or whatever
def RestoreConfig():
    with open(CurrentConfig, "r+") as ResetConfig:
        ResetConfig.write(DefaultConfig)

# For DQXI-S configs
def CheckStreamType():
    # We put this inside this function so non-DQXI-S modders
    # don't have to have the extra configs in memory
    print(DQXIS_MS)
    with open(DQXIS_MS, "r") as MS_Config:
        MultiStream = MS_Config.read()
    with open(DQXIS_SB, "r") as SB_Config:
        SndBank = SB_Config.read()
    with open(DQXIS_SS, "r") as SS_Config:
        SingleStream = SS_Config.read()
    sabf_b = b'\x73\x61\x62\x66'
    sabf = binascii.hexlify(sabf_b)
    with open(AssetName, 'rb') as Open_UExp:
        # Multi Stream
        Open_UExp.seek(0x96, 0x00)
        MSsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        MSsabf = binascii.hexlify(MSsabf_b)
        # Single Stream
        Open_UExp.seek(0x79, 0x00)
        SSsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        SSsabf = binascii.hexlify(SSsabf_b)
        # Sound Bank
        Open_UExp.seek(0x5D, 0x00)
        VOsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        VOsabf = binascii.hexlify(VOsabf_b)
        global DQXIS_Config
        if (MSsabf == sabf):
            DQXIS_Config = MultiStream
        elif (SSsabf == sabf):
            DQXIS_Config = SingleStream
        elif (VOsabf == sabf):
            DQXIS_Config = SndBank
        else:
            print("If you're seeing this message please")
            print("file an issue on the github and include the file in question")
            # I mean really, AudioMog should've crashed before you get that message
            DQXIS_Config = DefaultConfig

def DQXI_Prep():
    CheckStreamType()
    #print(DQXIS_Config)
    with open(CurrentConfig, "r+") as ChangeConfig:
        ChangeConfig.write(DQXIS_Config)
    shutil.rmtree(ProjectPath)

def DQXI_Cook():
    DoTheCook()
    RestoreConfig()
    ChocoCure()
    SlimeOverThere()
    OpenOutputDir()

"""
MAIN WINDOW
"""
#The main window of the program. Start by defining the glade file and builder
class MogWindow:
    def __init__(self):
        GladeFile = "../Config_Files/Window/MogGUI.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GladeFile)
        """
        BUTTONS AND OTHER WIDGETS
        """
        """
        Asset Chooser, Unpack, Play Old Sound, Open Sounds
        """
        self.Asset_Finder = self.builder.get_object("Asset_Finder")
        self.Asset_Finder.connect("file-activated", self.AssetSelected)
        #Import the templates for TreeView and ListStore to build to
        self.OldSound_Tree = self.builder.get_object("OldSound_Tree")
        self.OldSound_Store = Gtk.ListStore(str, int)
        #Import Unpack button object and link the function Unpack_clicked() to the clicked event
        Unpack_but = self.builder.get_object("Unpack")
        Unpack_but.connect("clicked", self.Unpack_clicked)
        #Sends the signal that a file was selected in Unpacked Sounds TreeView
        OldSound_Sig = self.builder.get_object("OldSound_Sig")
        OldSound_Sig.connect("changed", self.OldSound_Set)
        #Play sound from Unpacked TreeView
        OldSound_but = self.builder.get_object("OldSoundButton")
        OldSound_but.connect("clicked", self.PlayAssetSound)
        #Open Project Folder button
        OpenSounds_but = self.builder.get_object("OpenSounds")
        OpenSounds_but.connect("clicked", self.OpenProject)
        """
        New Sound Chooser, Slot # Field, Play New Sound
        """
        self.Sound_Finder = self.builder.get_object("Sound_Finder")
        self.Sound_Finder.connect("file-activated", self.NewSoundFile)
        #New Sound TreeView stuff
        self.NewSound_Tree = self.builder.get_object("NewSound_Tree")
        self.NewSound_Store = Gtk.ListStore(str, int)
        #For to add to/update the TreeView
        AddButton = self.builder.get_object("AddButton")
        AddButton.connect("clicked", self.AddNewSound)
        #Delcares the file selected in the New Sound TreeView
        NewSound_Sig = self.builder.get_object("NewSound_Sig")
        NewSound_Sig.connect("changed", self.NewSound_Set)
        #Plays the new sound
        NewSound_but = self.builder.get_object("NewSoundButton")
        NewSound_but.connect("clicked", self.PlayNewSound)
        """
        Cook and Config
        """
        Cooker = self.builder.get_object("CookButton")
        Cooker.connect("clicked", self.CookIt)
        self.ConfigBox = self.builder.get_object("ConfigBox")
        self.ConfigStore = Gtk.ListStore(str)
        self.ConfigBox.set_model(self.ConfigStore)
        self.ConfigBox.connect("changed", self.Config_Set)
        print("Plugins found:")
        print(list(DD_List))
        for item in DD_List:
            self.ConfigStore.append(item)
        """
        Renderings for the TreeViews
        """
        for i, col_title in enumerate(["Sound Name", "Slot #"]):
            renderer = Gtk.CellRendererText()
            os_col = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.OldSound_Tree.append_column(os_col)
            self.OldSound_Tree.set_model(self.OldSound_Store)
        #Renderer for New Sounds TreeView
        for i, col_title in enumerate(["Sound Name", "Slot #"]):
            renderer = Gtk.CellRendererText()
            ns_col = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.NewSound_Tree.append_column(ns_col)
            self.NewSound_Tree.set_model(self.NewSound_Store)
        #Renderer for Drop Down
        renderer = Gtk.CellRendererText()
        self.ConfigBox.pack_start(renderer, True)
        self.ConfigBox.add_attribute(renderer, "text", 0)
        """
        Main Loop
        """
        MogWindow = self.builder.get_object("MogWindow")
        MogWindow.connect("delete-event", Gtk.main_quit)
        self.Asset_Finder.connect("delete-event", Gtk.main_quit)
        MogWindow.show_all()
    """
    FUNCTIONS FOR THE BUTTONS AND WIDGETS
    """
    """
    Unpack Button
    """
    #Sets a variable when an asset file is selected
    def AssetSelected(self):
        global AssetName
        AssetName = self.Asset_Finder.get_filename()
    #Populates the unpacked sounds TreeView when called
    def GetOldSounds(self):
        #Clears out the TreeView indiscriminately when Unpack is clicked
        self.OldSound_Store.clear()
        #Sets up the List to be Stored and stores it in the ListStore
        get_wavs()
        for item in wavs_list:
            self.OldSound_Store.append(list(item))
    #Unpack button copies file to Input, unpacks it, and updates the TreeView
    def Unpack_clicked(self, widget):
        self.AssetSelected()
        #self.SoundSelected()
        MoogIt()
        time.sleep(1)
        self.OldSound_Tree
        self.OldSound_Store
        self.GetOldSounds()
    def OpenProject(self, widget):
        OpenProjectDir()
    """
    Add Sound Button
    """
    #Finds the new sound file
    def NewSoundFile(self):
        global SoundName
        SoundName = self.Sound_Finder.get_filename()
        #print(SoundName)
    #Clears and repopulates the ListStore
    def AddNewSound(self, widget):
        self.NewSound_Store.clear()
        global SlotFieldTxt
        SlotFieldTxt = self.builder.get_object("SlotField").get_text()
        self.NewSoundFile()
        NewEntry()
        for item in entry_list:
            self.NewSound_Store.append(list(item))
            #print(item)
    """
    Cook Button and Config
    """
    # This gets input for config variables
    def Config_Set(self, combo):
        global ConfigItr
        ConfigItr = combo.get_active_iter()
        global UserInput
        if ConfigItr != None:
            self.combo = combo
            UserInput = self.ConfigStore.get_value(ConfigItr, 0)
            print(UserInput)

    def CookIt(self, widget):
        if UserInput == "Default":
            DoTheCook()
            MoogOverThere()
            OpenOutputDir()
            self.NewSound_Store.clear()
            entry_list.clear()
        elif UserInput == "Dragon Quest XI DE":
            DQXI_Prep()
            self.OldSound_Store.clear()
            self.AssetSelected()
            MoogIt()
            time.sleep(1)
            self.OldSound_Tree
            self.OldSound_Store
            self.GetOldSounds()
            DQXI_Cook()
            entry_list.clear()
            self.NewSound_Store.clear()

    """
    TreeView Iter Objects:
    Whenever an item in the TreeView is clicked, this its signal's function.
    Workflow for entering data into a TreeView:
    #   list > ListStore > TreeStore > TreeView
    And to retrieve the data it looks a little like:
    #   TreeView's Signal > TreeView IterObject > value of ItrObj from the ListStore
    I am probably only 20% accurate here but at least this code works, okay?
    """
    def OldSound_Set(self, SelectedOldData):
        global OldSoundSelected
        OldSoundSelected = SelectedOldData.get_selected()[1]
        print(OldSoundSelected)
        if OldSoundSelected != None:
            self.SelectedOldData = SelectedOldData
        global OldSoundItrObj
        OldSoundItrObj = self.OldSound_Store.get_iter_first()

    def NewSound_Set(self, SelectedNewData):
        global NewSoundSelected
        NewSoundSelected = SelectedNewData.get_selected()[1]
        print(NewSoundSelected)
        if NewSoundSelected != None:
            self.SelectedNewData = SelectedNewData
        global NewSoundItrObj
        NewSoundItrObj = self.NewSound_Store.get_iter_first()
    """
    Play Sounds Buttons:
    This is where we actually go through and grab the data from the Iter
    so we can define it globally, and lastly call VLC on it in a script.
    Later, we're going to use this info in the Cooker button
    """
    def PlayAssetSound(self, widget):
        self.OldSound_Set(self.SelectedOldData)
        print(OldSoundItrObj)
        global SendVLC 
        VLCfile = self.OldSound_Store.get_value(OldSoundSelected, 0)
        SendVLC = AbsolutePath / VLCfile
        OldSoundSlot = self.OldSound_Store.get_value(OldSoundSelected, 1)
        global OldSoundItr
        OldSoundItr = ((SendVLC, OldSoundSlot))
        #print(list(OldSoundItr))
        print(SendVLC)
        print(OldSoundSlot)
        LaunchVLC()

    def PlayNewSound(self, widget):
        self.NewSound_Set(self.SelectedNewData)
        print(NewSoundItrObj)
        global SendNewVLC
        SendNewVLC = self.NewSound_Store.get_value(NewSoundSelected, 0)
        NewSoundSlot = self.NewSound_Store.get_value(NewSoundSelected, 1)
        global NewSoundItr
        NewSoundItr = ((SendNewVLC, NewSoundSlot))
        print(list(NewSoundItr))
        print(SendNewVLC)
        global SendVLC
        SendVLC = SendNewVLC
        print(NewSoundSlot)
        LaunchVLC()

if __name__=='__main__':
    main = MogWindow()
    Gtk.main()
