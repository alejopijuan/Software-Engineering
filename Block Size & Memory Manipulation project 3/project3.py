
#Alejo Pijuan
#Michael Gorka

from array import array

import sys

import time

#maximum number of entry for files in the archive  and also for data blocks for the archive
MAX_ENTRY = 32

#maximum number of block for a single file archive entry
#a file cannot splan over multiple archive entry
MAX_BLOCK_PER_FILE = 4

#maximum number of byte per datablock
MAX_BYTE_PER_DATABLOCK = 32

#maxium lenght for a file name
MAX_FILENAME = 8

#maximum number of characters used to store datablocks uses by a file
MAX_DIGIT_FOR_BLOCK = 2

#filesize will use a maximum of 3 digits
MAX_DIGIT_FOR_FILESIZE = 3

ARCHIVE_FILENAME = "archive.dat"

#datablock id starts at 1
class DataBlock:

     def __init__(self, id=0, data="", ):

         self.id    = id
         self.data  = "Z" * MAX_BYTE_PER_DATABLOCK

     def readFromArchive( self, id, line ):
         self.id   = id
         self.data = line

     def writeToArchive( self, file ):
         file.write( self.data.ljust( MAX_BYTE_PER_DATABLOCK ) ) 
         file.write("\n")

#an empty archiveentry has a filename = ""
#the block entries is equal to 0, when it is not in used
class ArchiveEntry:

     def __init__(self, filename="", size=0, ):

         self.filename = filename
         self.size     = size
         
         self.datablocks   = [0] * MAX_BLOCK_PER_FILE

     def readFromArchive( self, line ):

         self.size     = int(line[:MAX_DIGIT_FOR_FILESIZE])
         self.filename = line[MAX_DIGIT_FOR_FILESIZE : MAX_DIGIT_FOR_FILESIZE + MAX_FILENAME]
         
     def writeToArchive( self, file ):
         file.write( str(self.size).zfill( MAX_DIGIT_FOR_FILESIZE ) ) 
         file.write( self.filename.rjust( MAX_FILENAME ) ) 
         for idx in range(0, len( self.datablocks ) ) :
             file.write( str(self.datablocks[ idx ]).zfill( MAX_DIGIT_FOR_BLOCK ) )
         file.write("\n")

     def list( self ):
         print (self.filename.rjust( MAX_FILENAME )), 
         for idx in range(0, len( self.datablocks ) ) :
             print (str(self.datablocks[ idx ]).zfill( MAX_DIGIT_FOR_BLOCK )) 
         print("\n")

     def isEmpty( self ):
         return len(self.filename) == 0

class Archive:

     def __init__( self ):
        self.archiveEntries = []
        self.dataEntries = []

        self.archiveEntries = [ ArchiveEntry()] * MAX_ENTRY
        self.dataEntries    = [ DataBlock()] * MAX_ENTRY
     
     def writeToArchive( self ) :
        archive = open( ARCHIVE_FILENAME, "w")

        for idx in range(0, MAX_ENTRY):
           self.archiveEntries[ idx ].writeToArchive( archive )

        for idx in range(0, MAX_ENTRY):
           self.dataEntries[ idx ].writeToArchive( archive )

        archive.close( )

     def readFromArchive( self ):
        archive = open( ARCHIVE_FILENAME, "r")

        count = 0
        datablockid = 1;
        for line in archive:
            line = line.rstrip('\n')
            if count < MAX_ENTRY: 
               self.archiveEntries[ count ].readFromArchive( line )
            else:
               self.dataEntries[ datablockid - 1 ].readFromArchive( datablockid, line )
               datablockid = datablockid + 1
            count = count + 1


     def list( self ):
        for idx in range(0, MAX_ENTRY):
            print("entry :" + str(idx) )
            if self.archiveEntries[ idx ].isEmpty():
               print(" empty")
            else :
               self.archiveEntries[ idx ].list()
        print("\n")
     
     def create( self ):
        self.writeToArchive();

     def addToArchive( self, filename ):
        # must do validation on 
        # filename
        if len(filename) > 8:
        	return print("Error: Only 8 characters per filename, please rename the file try again")
        else:
            for entry in self.archiveEntries:
                if filename == entry.filename:
                    return print("Error: file name already in use")
            file = open(filename, "r")
            fileContents = file.readline()
            if len(fileContents) > 128:
                return print("Error: file is too large, files should be less than 128B")
            else:
                openblocks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
                for entry in self.archiveEntries:
                    blocksInUse = []
                    entryBlocks = entry.datablocks
                    i = 0
                    while i < 6:
                        blocksInUse.append(entryBlocks[i:i+2])
                        i += 2
                    for num in blocksInUse:
                        openblocks.remove(num)
                neededBlocks = ceil((entry.size)/32)
                if neededBlocks > len(openblocks):
                    return print("Error: not enough space")
                else:
                    for entry in self.archiveEntries:
                        if entry.isEmpty:
                            entry.filename = filename
                            entry.size = len(fileContents)
                            datablocksused = []
                            #for blocks in self.datablocks:
        # filesize vs maximum allowed per file
        # filesize vs free space
        # filename must be unique (case sensitive)
        # the archiveentry allocated for the file must be the 1st available starting at idx = 0
        # the file must used the minimum set of datablock requires to store the file
        # the datablock allocated for the file must be the 1st available starting at idx = 0
 

     def removeFromArchive( self, filename ):
        arch = open(ARCHIVE_FILENAME, "w")
	    archive.writeToArchive
	    arch.remove(filename)
	    arch.close()
	
	    # it must validate the file is or not in the archive and produce an error message
        #
        # remove a file from the archive. It will reset the archiveentry to the free state (filename="", size=0, datablocks=0)
        # and overwrite the data in the datablocks with 'Z's
        #


def createArchive():
     print("Creating Archive")
     Archive().create()

def addToArchive():
     filename = sys.argv[ 2 ];
     print("Adding to Archive:" + filename)
     archive = Archive()
     archive.readFromArchive()
     archive.list()
     archive.addToArchive( filename )
     archive.writeToArchive();

def removeFromArchive():
     filename = sys.argv[ 2 ];
     print("Removing from Archive:" + filename)
     archive = Archive()
     archive.readFromArchive()
     archive.list()
     archive.removeFromArchive( filename )
     archive.writeToArchive();

def listArchive():
     
     print("Listing from Archive")
     archive = Archive()
     archive.readFromArchive()
     archive.list()

'''
def listArchive():
     filename = sys.argv[ 2 ];
     print("Removing from Archive:" + filename)
'''
#
# processing command
#
#
command  = sys.argv[ 1 ] 

print 'Processing command:' + command

if command == 'create' :
   createArchive()
elif command == 'add' :
   addToArchive()
elif command == 'remove' :
   removeFromArchive()
elif command == 'list' :
   listArchive()
else :
   print("Invalid command")


