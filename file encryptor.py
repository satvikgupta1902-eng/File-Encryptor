from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
import keyboard as key
import os
import shutil
from tkinter import *
from tkinter import filedialog
import numpy as np

def clean():
    
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS and Linux
        os.system('clear')

def keycheck (x):# check which key is pressed 
    z=0
    while z == 0 :
        y = key.read_event(suppress=True)
        if y.event_type == key.KEY_DOWN and y.name in x :
            z=1
            return y.name
            
def symbcheck (x) : #remove "" from path
    if x[0] == '''"''' and x[len(x)-1] == '''"''':
        x = x[1:len(x)-1]
    return x
    

def manage (x,s): # x = file path s = to check string
    c=0
    z={}
    for y in range (len(x)):
        if x[y] == s  :
            z[c] = y
            c=c+1
    
    y = len(z)-1
    return z[y]

def pathgen (x,y,z): #x = file path y = output file name z = extension
    c = manage(x,"\\")
    otp =  x [0:c+1] +y+z
    return otp

def convt_to_zip (x,co):

    if co == "up":  #for file
        c = manage(x,".")
        zppath = x[0:c+1]+"zip"

        with ZipFile (zppath,'w',ZIP_DEFLATED) as zip:
            zip.write (x)
        

    elif co == "down":  #for folder
        c= manage(x,"\\")
        zppath = x[0:c+1]+"1.zip"

        with ZipFile (zppath,'w',ZIP_DEFLATED) as zip:
            for file in pathlib.Path(x).iterdir():
                zip.write(file,arcname=file.name)
            
    return zppath

def convt_to_original (x): #any zip file to original
    c= manage(x,"\\")
    zppath = x[0:c+1]
    with ZipFile (x,'r') as zip :
        zip.extractall(zppath)

def encrypt (x): #convert 0 to 1 and 1 to 0
    z={}
    a = ""
    for y in range (len(x)):
        if x[y] == "0":
            z[y] = "1"
        else :
            z[y] = "0"
        a = a + z[y]
    return a 



# def encrypt_the_file (filepath, output_filepath=None):
    
   
    
    
    #first converts a file into binary and then change it digits and convert back to file
    
    # with open(filepath, 'rb') as file:  # Open the file in binary read mode
    #     binary_data = file.read()        

    # binary_string = ''.join(format(byte, '08b') for byte in binary_data)  # Convert bytes to binary string
        
    #     # encrypted_binary_string = encrypt (binary_string)  #change 0 to 1 and 1 to 0

    # encrypted_binary_string = ''.join('1' if bit == '0' else '0' for bit in binary_string) #change 0 to 1 and 1 to 0

    # byte_list = []  #convert binary strings to bytes
    # for i in range(0, len(encrypted_binary_string), 8):
    #      # Convert the 8-bit binary string to an integer
    #     byte_string = encrypted_binary_string[i:i + 8]
    #     if len(byte_string) == 8: #prevent issues with trailing incomplete bytes.
    #         byte_list.append(int(byte_string, 2))

    # # Create a bytes object from the list of byte values.
    # byte_array = bytes(byte_list)
        
    # # Open the output file in binary write mode ('wb').
    # with open(output_filepath, 'wb') as output_file:
    #     # Write the byte array to the output file.
    #     output_file.write(byte_array)

    # print(f"File successfully encrypted to '{output_filepath}'.")

    # # except FileNotFoundError:
    # #     print(f"Error: File not found at {filepath}")
    # #     return None
    # # except Exception as e:
    # #      print(f"An error occurred: {e}")
    # #      return None
   
def encrypt_the_file(input_filepath, output_filepath):
    # 1. Read the input file as a memory-mapped NumPy array
    input_data = np.fromfile(input_filepath, dtype=np.uint8)

    # 2. Perform the bit-flip (NOT operation)
    flipped_data = ~input_data
    
    ulen= (len(flipped_data)//64)*64
    udata= flipped_data[:ulen]
    udata=udata.reshape(-1,4,4,4)
    
    udata[:,[0,1,2,3],[0,1,2,3],[0,1,2,3]]=udata[:,[1,0,3,2],[1,0,3,2],[1,0,3,2]]
    flipped_data[:ulen]=udata.flatten()
    
    # 3. Save the result directly to the output file
    flipped_data.tofile(output_filepath)

    print(f"Success! {input_filepath} flipped and saved to {output_filepath}")

# To get the array for your "few things":
# data_array = np.fromfile(input_filepath, dtype=np.uint8)
# flipped_array = ~data_array

rept = 0

while rept == 0 :

    print ("Press '▷' key to encrypt or '◁' this key to de-encrypt and press 'esc' to exit.")
    keypress = keycheck(['left','right','esc','c'])
    print()

    if keypress == 'right' :

        print ("Type '△' to encrypt a file and '▽' to encrypt a folder : ")
        x = keycheck(['up','down'])
        print()
        infp = input ("Enter Input File/Folder path : ") 
        infp = symbcheck (infp)
        foldbackup = infp
        otf = input ("Enter Output File name : ") 
        print()

        infp = convt_to_zip(infp,x)

        # change anyother extension to .txt
        y  = manage (infp,".")
        if infp [y+1:len(infp)] != "txt":
            backup = infp
            infp = infp [0:y+1]+"txt"
            os.replace (backup,infp)

        # generates the path of output file
        otfp =  pathgen (infp,otf,".txt")

        encrypt_the_file(infp,otfp) #encrypt the file



        if infp != otfp and os.path.exists(infp):
            os.remove(infp)
        if os.path.exists(foldbackup):           
            if os.path.isdir(foldbackup):
                shutil.rmtree(foldbackup)
            else :
                os.remove(foldbackup)

    elif keypress == 'left':
        infp = input ("Enter Input File/Folder path : ") 
        infp = symbcheck (infp)
        otf = input ("Enter Output File name : ") 
        print()

        # generates the path of output file
        otfp =  pathgen (infp,otf,".txt")

        encrypt_the_file(infp,otfp) #de-encrypt the file
        
        #change anyother extension to .zip
        y  = manage (otfp,".")
        backup = otfp
        otfp = otfp [0:y+1]+"zip"
        os.replace (backup,otfp)
            
        convt_to_original (otfp)
        if os.path.exists(otfp):
            os.remove (otfp)
    
    elif keypress == 'esc' :
        rept = 1

    elif keypress == 'c':
        clean()
