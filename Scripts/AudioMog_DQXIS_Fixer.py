import os
import fileinput
import glob
import codecs
import binascii
from datetime import datetime

#pwd = os.getcwd
#cd = os.chdir
cwd = os.getcwd()
TheseFiles = (cwd + '/**/*.uexp')
ThisPath = glob.glob(TheseFiles,
                      recursive = True)
"""
Logging Functions
"""
def GetTime():
    TimeString = str(datetime.now())
    global Timestamp
    Timestamp = TimeString[0:-2]

#Presents the data from the buffer to the log, in an HxD-esque format with hex and ascii
def LogData():
            bytes = 0
            line = []
            for RawByte in OG_Bytes:
                bytes = bytes + 1
                line.append(RawByte)
                boofer.write("{0:0{1}X}".format(RawByte,2) + " ")
                if bytes % 16 == 0:
                    boofer.write("#" + "")
                    for Readable in line:
                        if (Readable >= 32) and (Readable != 127) and (Readable <= 255):
                            boofer.write(chr(Readable))
                        else:
                            boofer.write(".")
                    line = []
                    boofer.write("\n")

def hexlog():
    #Writes the header info first
    Boof = "bufffer.log"
    with open(".buffer.tmp", 'rb') as Tmp:
        Tmp.seek(0x00, 0x00)
        global OG_Bytes
        OG_Bytes = Tmp.read(0x40 - 0x00)
        global boofer
        with open(Boof, 'a') as boofer:
            boofer.seek(0, 2)
            boofer.write(Open_UExp.name + "\n")
            GetTime()
            boofer.write("@ " + Timestamp + "\n")
            if (MSorSS == 0x49):
                boofer.write("Single Stream file detected \n")
            elif (MSorSS == 0x66):
                boofer.write("Multi-Stream file detected \n")
            elif (MSorSS == 0x2D):
                boofer.write("Sound Bank file detected \n")
            else:
                boofer.write("If you are seeing this message... \n")
                boofer.write("You have divided by zero and your file is a waffle. \n")
            #Writes the hex and ascii data to the log
            LogData()
        with open(Boof, 'a') as boofer:
            boofer.write("\n")
            boofer.write("\n")

"""
Fixing the Files
"""
def CleanUp():
    with open(".buffer.tmp", 'r+') as Cleanup:
        Cleanup.seek(0x04, 0x00)
        Cleanup.write(chr(0x00))
        Cleanup.write(chr(0x00))
        Cleanup.write(chr(0x00))
        Cleanup.write(chr(0x00))

def Inject_Payload():
    hexlog()
    with open(".buffer.tmp", 'rb') as Fixed:
        Fixed.seek(0x00, 0x00)
        Payload = Fixed.read(0x28 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        Open_UExp.seek(MSorSS, 0x00)
        Open_UExp.write(Payload)

#Call this functino when you need to fix the opened UExp file
def Fix_UExp():
    #Creates a buffer to work from
    if not os.path.exists(".buffer.tmp"):
        with open(".buffer.tmp", 'w') as CreateLog:
            CreateLog.close()
    Open_UExp.seek(MSorSS, 0x00)
    Offset = Open_UExp.read(0x40 - 0x00)
    with open(".buffer.tmp", 'r+b') as Log:
        Log.write(Offset)
    #Log data before the change
    with open(".buffer.tmp", 'rb') as Log:
        Log.seek(0x00, 0x00)
        LogData = Log.read(0x40 - 0x00)
        hexlog()
    #This does the actual hex editing in the buffer
    with open(".buffer.tmp", 'r+b') as Log:
        Log.seek(0x04, 0x00)
        FileSize = Log.read(0x04 - 0x00)
        Log.seek(0x00, 0x00)
        Log.write(FileSize)
        Log.seek(0x20, 0x00)
        Log.write(FileSize)
        Log.seek(0x24, 0x00)
        Log.write(FileSize)
    CleanUp()
    #Now that our data is correct, let's inject it into the original file
    with open(".buffer.tmp", 'rb') as Log:
        Log.seek(0x00, 0x00)
        LogData = Log.read(0x40 - 0x00)
    Inject_Payload()

"""
File Search and Fix - looks for sabf files by type and fixes them
"""
print("Finding files to fix...")

sabf_b = b'\x73\x61\x62\x66'
sabf = binascii.hexlify(sabf_b)

#Multi-Stream fixing
for files in ThisPath:
    with open(files, 'r+b') as Open_UExp:
        Open_UExp.seek(0x66, 0x00)
        mOffset0 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x6A, 0x00)
        mOffset1 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x86, 0x00)
        mOffset2 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x8A, 0x00)
        mOffset3 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x96, 0x00)
        MSsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        MSsabf = binascii.hexlify(MSsabf_b)
        if (MSsabf == sabf) and (mOffset0 == mOffset1) and (mOffset0 == mOffset3):
            MSorSS = 0x66
            Fix_UExp()
            print("Multi-Stream sabf file for fixing has been found...")
            print("Multi-Stream sabf file has been fixed!")
        else:
            continue

#Single Stream fixing
for files in ThisPath:
    with open(files, 'r+b') as Open_UExp:
        Open_UExp.seek(0x49, 0x00)
        sOffset0 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x4D, 0x00)
        sOffset1 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x69, 0x00)
        sOffset2 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x6D, 0x00)
        sOffset3 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x79, 0x00)
        SSsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        SSsabf = binascii.hexlify(SSsabf_b)
        if (SSsabf == sabf) and (sOffset0 != sOffset1) and (sOffset1 == sOffset3):
            MSorSS = 0x49
            Fix_UExp()
            print("Single Stream sabf file for fixing has been found...")
            print("Single Stream sabf file has been fixed!")
        else:
            continue

#Single Stream but, like, different or whatever
#AudioMogGUI will flag this as a multistream but that doesn't really matter
for files in ThisPath:
    with open(files, 'r+b') as Open_UExp:
        Open_UExp.seek(0x66, 0x00)
        mOffset0 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x6A, 0x00)
        mOffset1 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x86, 0x00)
        mOffset2 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x8A, 0x00)
        mOffset3 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x96, 0x00)
        MSsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        MSsabf = binascii.hexlify(MSsabf_b)
        if (MSsabf == sabf) and (mOffset0 != mOffset1) and (mOffset1 == mOffset3):
            MSorSS = 0x66
            Fix_UExp()
            print("Single Stream sabf file for fixing has been found...")
            print("Single Stream sabf file has been fixed!")
        else:
            continue

#Sound Bank/Voice Over fixing
for files in ThisPath:
    with open(files, 'r+b') as Open_UExp:
        Open_UExp.seek(0x2D, 0x00)
        voOffset0 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x31, 0x00)
        voOffset1 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x4D, 0x00)
        voOffset2 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x51, 0x00)
        voOffset3 = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x5D, 0x00)
        VOsabf_b = Open_UExp.read(0x04 - 0x00)
        Open_UExp.seek(0x00, 0x00)
        VOsabf = binascii.hexlify(VOsabf_b)
        if (VOsabf == sabf) and (voOffset1 == voOffset2) and (voOffset1 == voOffset3):
            MSorSS = 0x2D
            Fix_UExp()
            print("Sound Bank sabf file for fixing has been found...")
            print("Sound Bank sabf file has been fixed!")
        else:
            continue

print("No more files found to fix!")
