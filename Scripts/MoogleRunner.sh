# Below is an example script that will be written and ran by AudioMogGUI
# This file will rewritten everytime Unpack button/functionality is called

#!/bin/bash

cd ${0%/*}
cd ../Binaries/AudioMog/
wine start AudioMog.exe Input/SWAV_fld_UN10701_jump.uexp
