"""
lab 4
"""

class Node:

    def __init__(self,frequency):
        self.left = None
        self.right = None
        self.top = None
        self.frequency = frequency

    def is_left(self):
        return self.top.left == self
        


def create_nodes(freqs):
    return [Node(freq) for freq in freqs]


def create_huffman_tree(nodes):
    q = nodes[:]
    while len(q) > 1:
        q.sort(key=lambda item:item.frequency)
        node_left = q.pop(0)
        node_right = q.pop(0)
        node_top = Node(node_left.frequency + node_right.frequency)
        node_top.left = node_left
        node_top.right = node_right
        node_left.top = node_top
        node_right.top = node_top
        q.append(node_top)
    q[0].top = None
    return q[0]
    
    

def frequency_table(codes):
    frequencies_file=open('freq.txt','w')
    for i in range(256):
        frequencies_file.write(str(codes[i])+'\n')
    frequencies_file.close()  


def huffman_encoding(nodes,root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.is_left():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.top
    return codes


def compression(filename):
    count=[0 for i in range(256)]
    file_with_secret_msg=open(filename,"rb")
    compressed_file=open("archive.txt","wb")
    text=file_with_secret_msg.read()
    for i in text:
        count[i]+=1

    nodes = create_nodes([item for item in count])
    root = create_huffman_tree(nodes)
    codes = huffman_encoding(nodes,root)
    for i in range(256):
        codes[i]='1'+codes[i]
    frequency_table(codes)
    
    encoder=""
    for i in text:
        encoder+=codes[i]
    if len(encoder)%8 !=0:
        num=(8-len(encoder)%8)
        encoder+='0'*num
    
    lst=[int(encoder[i:i + 8],2) for i in range(0, len(encoder), 8)]
    compressed_file.write(bytearray(lst))

    file_with_secret_msg.close()
    compressed_file.close()

def decompression(filename):
    fs_binary=[]
    compressed_file=open("archive.txt","rb")
    frequencies_file=open('freq.txt','r')
    new_file_with_secret_msg=open(filename,"wb")
    
    for line in frequencies_file.readlines():
        fs_binary.append(line[:-1])
    text=""    
    for i in compressed_file.read():
        text+='0'*(8-len(bin(i)[2:]))+bin(i)[2:]
    tmp=""
    for i in text:
        if tmp+i in fs_binary:
            lst=[int(fs_binary.index(tmp+i))]
            new_file_with_secret_msg.write(bytes(lst))
            tmp=""
        else:
            tmp+=i
    
    compressed_file.close()
    frequencies_file.close()
    new_file_with_secret_msg.close()



compression("message.txt")
decompression("message_2.txt")
print("DONE!")
    