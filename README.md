**Welcome to AudioMog GUI!**

AudioMog GUI is a graphical interface for the AudioMog binary executeable (.exe). It is designed to be compatible with Windows, Linux, and (hopefully) MacOS. This program has the same functionality as AudioMog (because it requires you to have the .exe file) plus the following features:

Automatic file renaming - no more manually renaming Every_Random_Sound_File_012.wav
Compare sounds by clicking on them and pressing the Play Sound button
Coming Soon: Plugin feature to contain your custom configurations in a drop down menu
High DPI mode available - currently must be done manually, see readme.txt in Icons folder
Pop open the Project's sound files folder at will
All processed files organized to a single Output folder

**Beta Version Note:**  
This program is currently in the beta stage and lacks several features that I intend to implement. These features will be discussed towards the end of this file, please refer to it before reporting any bugs.

Also, I am still new to coding. This is my first "real" program and I basically googled my way through the necessary knowledge. I intend to clean up the code more as I add features. If you have any constructive criticism (other than that I should quit while I'm ahead) then say it with a comment or a commit. Thank you! And if I ever decide to torture myself with another program, I will use tkinter - all I saw was "GTK works on Windows too!" and didn't even think to look for other libraries.

**DEPENDS:**  
*Linux* - GTK 3.0 or higher, Python 3.8 or higher, VLC, Wine, AudioMog.exe

*Windows* -  
    AudioMog.exe  
    VLC (Must be in your PATH as well, usually done automatically when installing)  
    The python and GTK libraries are precompiled and included.  

*MacOS* - Same as Linux I assume. I don't own a Mac so I have not tested it at all. If you run MacOS and have issues using this program, let's work together to fix that.

**INSTALL:**  
*All Operating Systems* - Download the latest AudioMog release and move ONLY THE .EXE FILE to the Binaries/AudioMog/ directory. Beta version: If you have a specific configuration you need to use, copy it to the same directory (replacing the existing TerminalSettings.json) and also replace the same file in Config_Files/Game/Default/

https://github.com/Yoraiz0r/AudioMog/releases

*Linux* - mark Setup.sh as executable and run it. It will create a desktop launcher for you. If you choose to run AudioMogGUI.py from the terminal please remember to mark the additional scripts as executable as well since they are necessary for AMGUI to run.

*Windows* - Double click the precompiled Scripts/AudioMogGUI.exe. You may make a shortcut to it and place the shortcut anywhere. It may take a while to launch the first time since GTK is not a native graphics library to Windows. Please be patient. Don't fear the scary black boxes (command terminals), it just means AudioMog or VLC is being ran. If it's not your first rodeo with terminals, don't think you can run this with with python normally, see the Build section below.

**BUILD:**  
*Windows* - Requires MinGW64 and inside MinGW64 you require Git, Python 3.10, GTK libraries, Pyinstaller. I am currently unaware of how to edit the Glade file on Windows. Theoretically you should be able to install a glade editor inside of MinGW. Please let me know if you succeed in doing so. You may run AudioMogGUI.py directly only from inside the MinGW64 terminal because of the GTK libraries.

*Linux* - You don't need to build this? If you really want to, you will need to install pyinstaller and add it to your PATH. You may want to edit the Glade file though and for that you will need Glade.

Make any edits to AudioMogGUI.py that you would like and from the MinGW64 shell navigate to the Scripts directory then build using the following command:

pyinstaller -F --noconsole AudioMogGUI.py

Of course, you may choose other build flags, see pyinstaller --help for more options. I will not be providing a tutorial on how to set up the MinGW64 environment on Windows, there are plenty of tutorials on google.

**USEAGE:** This video is from a pre-beta demo but the idea is essentially the same. I will make an updated video for the first Stable release.

https://youtu.be/CGQqGqFHD80

**Planned Features:**  
-Files being where they should be!  
-Plugins! You will be able to drop in your custom TerminalSettings.json, name the game, and select it from the drop down.  
-Toolbar for graphic mode and adding plugins  
-Button to delete a sound added to the New Sounds box  
-Option to open Output folder at will (not just after cooking)  
-Support for .HCA conversion (will require another .exe file, I'm not writing what already exists)  
-DQXIS-only fork because DQXIS is special. Both in how annoying it is to cook files for and in terms of it being the game I wrote this program to use on.  
-If any games have fixer scripts or multiple necessary configurations like DQXIS does I can hard code the configuration into AudioMog's configuration drop down menu and have it autorun the script like I do with DQXIS.
