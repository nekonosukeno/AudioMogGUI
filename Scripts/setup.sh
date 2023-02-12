#!/bin/bash

# The purpose of this script is to perform the following:
#    Verify dependencies of AudioMogGUI are satisfied
#    Create a .desktop launcher for AMGUI
#    Mark permissiosn for the scripts AMGUI uses
#    Launches AMGUI upon completion

cd ${0%/*}
InstallerRoot=$(cd ../; pwd)
VLCer=$InstallerRoot"/Scripts/LaunchVLC.sh"
Moogler=$InstallerRoot"/Scripts/MoogleRunner.sh"
MogGUI=$InstallerRoot"/Scripts/AudioMogGUI.py"
Logo=$InstallerRoot"/Icons/AMlogo.png"
Icon=$InstallerRoot"/Icons/AudioMog_Fixer.png"
Default_Config=$InstallerRoot"/Config_Files/Game/Default/TerminalSettings.json"
Glade=$InstallerRoot"/Config_Files/Window/MogGUI.glade"
AudioMog=$InstallerRoot"/Binaries/AudioMog/AudioMog.exe"
AM_Config=$InstallerRoot"/Binaries/AudioMog/TerminalSettings.json"
Important_Stuff=($VLCer $Moogler $MogGUI $Logo $Icon $Default_Config $Glade $AudioMog $AM_Config)
Scripts=($VLCer $Moogler $MogGUI $AudioMog)

Shortcut="AudioMogGUI.desktop"

Py=$(command -v python)
Py3=$(command -v python3)
HasWine=$(command -v wine)
GTK=$(command -v gtk-launch)
Major=$(gtk-launch --version | cut -d. -f1)

if [[ $Py || $Py3 && $HasWine ]]; then
    echo "Python found"
    echo "wine found"
else echo "Either wine or Python were not found";
    echo "Please make sure both are installed and try again";
    echo "Wine: recommended version - 7.0+"
    echo "Python: required version - 3.8 or higher | Written with 3.10"
    exit
fi

function checkGTK() {
    if [[ GTK ]] && (($Major >= 3 )); then
        echo "GTK found";
        echo "Minimum version required: 3 | Version found: $Major"
    else echo "GTK was not found";
        echo "Minimum version required: GTK 3.0 | Version found: None"
        echo "Please install GTK library through pip or your distro's package manager";
        exit
    fi
}
# If you installed GTK through pip and still have errors running this script, comment this out
checkGTK

# This function prints the directory that the script is located in
function CWD() {
    echo $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
}

# Stuff to make the .desktop shortcut
function MakeFile() {
    touch "$Shortcut";
    chmod u+rwx "$Shortcut"
}

function FileContent() {
    echo "[Desktop Entry]";
    echo "Encoding=UTF-8";
    echo "Version=0.1_beta";
    echo "Type=Application";
    echo "Path=$(CWD)";
    echo "Name=AudioMog GUI";
    echo "Icon="$Icon
    echo "Exec=python3 "$(CWD)"/AudioMogGUI.py";
    echo "Terminal=false";
}

# Write the necessary contents of the .desktop shortcut to the new file
function WriteStuff() {
    FileContent >> AudioMogGUI.desktop
}

# Checks if the shortcut exists and if missing initiates creating it
function MakeShortcut() {
    if [[ ! -f AudioMogGUI.desktop ]]; then
        echo "Creating shortcut now...";
        MakeFile;
        WriteStuff;
        echo "Shortcut created!";
        echo "Launching AudioMog GUI";
        python3 AudioMogGUI.py;
        exit
    else echo "Shortcut already exists!";
        echo "Launching AudioMog GUI";
        python3 AudioMogGUI.py
        exit
    fi
}

# AudioMogGUI uses automated scripting to launch AudioMog.exe and VLC when needed.
# By giving read, write, and execute access before running AMGUI we avoid permissions errors.
function SetPermissions() {
    for script in ${Scripts[@]}; do
        chmod u+rwx "$script";
    done
}

echo "Finding the necessary files..."

n=0
AllFiles=9
newline=$'\n'
Missing=("")
for item in ${Important_Stuff[@]}; do
    if [[ ! -f $item ]]; then
        Missing+=("$item")
    else echo "$item found!";
        n=$(( $n + 1 ))
    fi
done

if [[ ! $n = $AllFiles ]]; then
    echo "The following files were not found:";
    for file in ${Missing[@]}; do
        echo "$file";
    done
    exit
else echo "All files successfully found";
    MakeShortcut;
    SetPermissions
fi
