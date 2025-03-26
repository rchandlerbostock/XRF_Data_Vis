import os
import struct
import datetime
import numpy as np

ABIF_TYPES = {
    1: 'byte', 2: 'char', 3: 'word', 4: 'short', 5: 'long',
    7: 'float', 8: 'double', 10: 'date', 11: 'time', 12: 'thumb',
    13: 'bool', 18: 'pString', 19: 'cString'
}

class ABIFReader:
    def __init__(self, fn):
        self.filename = fn
        self.file = open(fn, 'rb')
        self.type = self.readNextString(4)
        if self.type != 'ABIF':
            self.close()
            raise ValueError(f"Error: No ABIF file '{fn}'")
        self.version = self.readNextShort()
        dir_entry = DirEntry(self)
        self.seek(dir_entry.dataoffset)
        self.entries = [DirEntry(self) for _ in range(dir_entry.numelements)]

    def getData(self, name, num=1):
        entry = self.getEntry(name, num)
        if not entry:
            raise ValueError(f"Error: Entry '{name} ({num})' not found in '{self.filename}'")
        self.seek(entry.mydataoffset())
        data = self.readData(entry.elementtype, entry.numelements)
        return data[0] if len(data) == 1 else data

    def showEntries(self):
        for entry in self.entries:
            print(entry)

    def getEntry(self, name, num):
        for entry in self.entries:
            if entry.name == name and entry.number == num:
                return entry
        return None

    def readData(self, type, num):
        if type == 1:
            return [self.readNextByte() for _ in range(num)]
        elif type == 2:
            return self.readNextString(num)
        elif type == 3:
            return [self.readNextUnsignedInt() for _ in range(num)]
        elif type == 4:
            return [self.readNextShort() for _ in range(num)]
        elif type == 5:
            return [self.readNextLong() for _ in range(num)]
        elif type == 7:
            return [self.readNextFloat() for _ in range(num)]
        elif type == 8:
            return [self.readNextDouble() for _ in range(num)]
        elif type == 10:
            return [self.readNextDate() for _ in range(num)]
        elif type == 11:
            return [self.readNextTime() for _ in range(num)]
        elif type == 12:
            return [self.readNextThumb() for _ in range(num)]
        elif type == 13:
            return [self.readNextBool() for _ in range(num)]
        elif type == 18:
            return self.readNextpString()
        elif type == 19:
            return self.readNextcString()
        elif type >= 1024:
            return self.readNextUserData(type, num)
        else:
            return NotImplemented

    def readNextBool(self):
        return self.readNextByte() == 1

    def readNextByte(self):
        return self.primUnpack('B', 1)

    def readNextChar(self):
        return self.primUnpack('c', 1)

    def readNextcString(self):
        chars = []
        while True:
            c = self.readNextChar()
            if ord(c) == 0:
                return ''.join(chars)
            else:
                chars.append(c.decode('utf-8'))

    def readNextDate(self):
        return datetime.date(self.readNextShort(), self.readNextByte(), self.readNextByte())

    def readNextDouble(self):
        return self.primUnpack('>d', 8)

    def readNextInt(self):
        return self.primUnpack('>i', 4)

    def readNextFloat(self):
        return self.primUnpack('>f', 4)

    def readNextLong(self):
        return self.primUnpack('>l', 4)

    def readNextpString(self):
        nb = self.readNextByte()
        chars = [self.readNextChar().decode('utf-8') for _ in range(nb)]
        return ''.join(chars)

    def readNextShort(self):
        return self.primUnpack('>h', 2)

    def readNextString(self, size):
        chars = [self.readNextChar().decode('utf-8') for _ in range(size)]
        return ''.join(chars)

    def readNextThumb(self):
        return (self.readNextLong(), self.readNextLong(), self.readNextByte(), self.readNextByte())

    def readNextTime(self):
        return datetime.time(self.readNextByte(), self.readNextByte(), self.readNextByte(), self.readNextByte())

    def readNextUnsignedInt(self):
        return self.primUnpack('>I', 4)

    def readNextUserData(self, type, num):
        return NotImplemented

    def primUnpack(self, format, nb):
        val = self.file.read(nb)
        x = struct.unpack(format, val)
        return x[0]

    def close(self):
        self.file.close()

    def seek(self, pos):
        self.file.seek(pos)

    def tell(self):
        return self.file.tell()

class DirEntry:
    def __init__(self, reader):
        self.name = reader.readNextString(4)
        self.number = reader.readNextInt()
        self.elementtype = reader.readNextShort()
        self.elementsize = reader.readNextShort()
        self.numelements = reader.readNextInt()
        self.datasize = reader.readNextInt()
        self.dataoffsetpos = reader.tell()
        self.dataoffset = reader.readNextInt()
        self.datahandle = reader.readNextInt()

    def __str__(self):
        return f"{self.name} ({self.number}) / {self.mytype()} ({self.numelements})"

    def mydataoffset(self):
        return self.dataoffsetpos if self.datasize <= 4 else self.dataoffset

    def mytype(self):
        return ABIF_TYPES.get(self.elementtype, 'unknown') if self.elementtype < 1024 else 'user'

def write_out_raw_csv(data, data_file, directory):
    """
    Writes out the CSV data from the raw FSA file.
    """
    output_file = os.path.join(directory, f"{os.path.basename(data_file).replace('.fsa', '_raw.csv')}")
    with open(output_file, 'w') as f:
        f.write('Position,Footprinted Sample,ddA Ladder,ddC Ladder,Space Measure\n')
        for position in range(len(data)):
            f.write(f"{position + 1},{data[position][0]},{data[position][1]},{data[position][2]},{data[position][3]}\n")

def readABI(fname):
    reader = ABIFReader(fname)
    col0 = reader.getData('DATA', 1)
    col1 = reader.getData('DATA', 2)
    col2 = reader.getData('DATA', 3)
    col3 = reader.getData('DATA', 4)
    
    data = np.zeros([len(col0), 4], dtype='f4')
    data[:, 0] = np.array(col0)
    data[:, 1] = np.array(col1)
    data[:, 2] = np.array(col2)
    data[:, 3] = np.array(col3)
    return data

if __name__ == '__main__':
    directory = os.getcwd()  # Use current working directory
    print(f"Looking for .fsa files in: {directory}")
    found_files = False  # Track if any .fsa files are found
    
    for fsa_file in os.listdir(directory):
        if fsa_file.endswith('.fsa'):
            found_files = True  # Set to True if at least one file is found
            full_path = os.path.join(directory, fsa_file)
            print(f"Processing file: {full_path}")
            reference_data = readABI(full_path)
            write_out_raw_csv(reference_data, full_path, directory)
            print(f"Converted {fsa_file} to {fsa_file.replace('.fsa', '_raw.csv')}")
    
    if not found_files:
        print("No .fsa files found in the directory.")
