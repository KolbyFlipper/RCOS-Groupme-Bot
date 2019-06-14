
# FILE MANAGEMENT FUNCTIONS
# read, write, change extension
import os


# will create/overwrite fileName
# auto closes the fp
def writeFile(fileName, text):
    with open(fileName, "w+") as fp:
        fp.write(text)


# end of writeFile

# will read a files output to given stream
def readFile(fileName, stream):
    with open(fileName, "r") as fp:
        print(fp.read())


# end of read file


# Edit file extension
def eExt(fileName, ext):
    if(os.path.exists(fileName)):
        fname = os.path.splitext(fileName)[0]
        os.rename(fileName, fname + str(ext))
# end of eExt
