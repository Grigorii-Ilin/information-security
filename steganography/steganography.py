"""
Lab. 2 
"""

import cv2
import numpy as np



class LSBSteg():
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height
        
        self.MASK_ONE_VALUES = [1+i*10 for i in range(8)]
        self.maskONE = self.MASK_ONE_VALUES.pop(0) #Will be used to do bitwise operations
        
        self.MASK_ZERO_VALUES = [254-i*10 for i in range(8)]
        self.maskZERO = self.MASK_ZERO_VALUES.pop(0)
        
        self.cur_width = 0  # Current width position
        self.cur_height = 0 
        self.cur_channel = 0   

    def put_binary_value(self, bits): #Put the bits in the image
        for c in bits:
            val = list(self.image[self.cur_height,self.cur_width]) #Get the pixel value as a list
            if int(c) == 1:
                val[self.cur_channel] = int(val[self.cur_channel]) | self.maskONE #OR with maskONE
            else:
                val[self.cur_channel] = int(val[self.cur_channel]) & self.maskZERO #AND with maskZERO
                
            self.image[self.cur_height,self.cur_width] = tuple(val)
            self.next_slot() #Move "cursor" to the next space
        
    def next_slot(self):#Move to the next slot were information can be taken or put
        if self.cur_channel == self.nbchannels-1: 
            self.cur_channel = 0
            if self.cur_width == self.width-1: 
                self.cur_width = 0
                if self.cur_height == self.height-1:
                    self.cur_height = 0
                    self.maskONE = self.MASK_ONE_VALUES.pop(0)
                    self.maskZERO = self.MASK_ZERO_VALUES.pop(0)
                else:
                    self.cur_height +=1
            else:
                self.cur_width +=1
        else:
            self.cur_channel +=1

    def read_bit(self): #Read a single bit int the image
        val = self.image[self.cur_height,self.cur_width][self.cur_channel]
        val = int(val) & self.maskONE
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"
    
    def read_byte(self):
        return self.read_bits(8)
    
    def read_bits(self, nb): #Read the given number of bits
        bits = ""
        for i in range(nb):
            bits += self.read_bit()
        return bits

    def byteValue(self, val):
        return self.binary_value(val, 8)
        
    def binary_value(self, val, bitsize): #Return the binary value of an int as a byte
        binval = bin(val)[2:]
        while len(binval) < bitsize:
            binval = "0"+binval
        return binval

    def encode_text(self, txt):
        l = len(txt)
        binl = self.binary_value(l, 16) #Length coded on 2 bytes so the text size can be up to 65536 bytes long
        self.put_binary_value(binl) 
        for char in txt: 
            c = ord(char)
            self.put_binary_value(self.byteValue(c))
        return self.image
       
    def decode_text(self):
        ls = self.read_bits(16) #Read the text size in bytes
        l = int(ls,2)
        i = 0
        unhideTxt = ""
        while i < l: #Read all bytes of the text
            tmp = self.read_byte() #So one byte
            i += 1
            unhideTxt += chr(int(tmp,2)) #Every chars concatenated to str
        return unhideTxt

    def encode_image(self, imtohide):
        w = imtohide.width
        h = imtohide.height
        binw = self.binary_value(w, 16) 
        binh = self.binary_value(h, 16)
        self.put_binary_value(binw) #Put width
        self.put_binary_value(binh)
        for h in range(imtohide.height): #Iterate the hole image to put every pixel values
            for w in range(imtohide.width):
                for chan in range(imtohide.channels):
                    val = imtohide[h,w][chan]
                    self.put_binary_value(self.byteValue(int(val)))
        return self.image

                    
    def decode_image(self):
        width = int(self.read_bits(16),2) #Read 16bits and convert it in int
        height = int(self.read_bits(16),2)
        unhideimg = np.zeros((width,height, 3), np.uint8) #Create an image in which we will put all the pixels read
        for h in range(height):
            for w in range(width):
                for chan in range(unhideimg.channels):
                    val = list(unhideimg[h,w])
                    val[chan] = int(self.read_byte(),2) #Read the value
                    unhideimg[h,w] = tuple(val)
        return unhideimg
    
    def encode_binary(self, data):
        l = len(data)
        self.put_binary_value(self.binary_value(l, 64))
        for byte in data:
            byte = byte if isinstance(byte, int) else ord(byte) 
            self.put_binary_value(self.byteValue(byte))
        return self.image

    def decode_binary(self):
        l = int(self.read_bits(64), 2)
        output = b""
        for i in range(l):
            output += chr(int(self.read_byte(),2)).encode("utf-8")
        return output



in_img = cv2.imread("MARBLES.bmp")
steg = LSBSteg(in_img)

data=open("message.txt", "rb").read()
res = steg.encode_binary(data)
cv2.imwrite("MARBLES_secret.bmp", res)

in_img = cv2.imread("MARBLES_secret.bmp")
steg = LSBSteg(in_img)
raw = steg.decode_binary()
with open("message_2.txt", "wb") as f:
    f.write(raw)

print("Done!")