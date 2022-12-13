import json
import os
import shutil


class CompressedIndexWriter:
    def __init__(self, in_dir, out_dir):
        """Given uncompressed product review data, creates
        an on disk compressed index
        in_dir is the path of the directory where the
        uncompressed files are
        out_dir is the path of the directory in which the
        compressed files will be created
        if the out directory does not exist, it should be
        created"""
        self.in_dir = in_dir
        self.out_dir = out_dir

        # self.inputFile = inputFile
        # self.dir = dir

        # Path
        compFilesPath = os.path.join(self.out_dir, "compressed_files")
        unCompFilesPath = os.path.join(self.in_dir, "unCompressed_files")
        # make directory
        if not os.path.exists(compFilesPath):
            os.mkdir(compFilesPath)

        ComptextDicStrFile = os.path.join(compFilesPath, "text.dic.str")
        ComptextDicTableFile = os.path.join(compFilesPath, "text.dic.tbl")
        ComptextListFile = os.path.join(compFilesPath, 'text.lst.lpu')
        CompproductsDicFile = os.path.join(compFilesPath, 'products.dic.fxd')
        CompproductsListFile = os.path.join(compFilesPath, "products.lst.vrnt")
        CompcollectionDataFile = os.path.join(compFilesPath, "collection.data")
        CompreviewTableFile = os.path.join(compFilesPath, 'reviews.tbl')


        unCompTextDicFile = os.path.join(unCompFilesPath, "text.dic")
        unComptextListFile = os.path.join(unCompFilesPath, 'text.lst')
        unCompcollectionDataFile = os.path.join(unCompFilesPath, "collection.data")
        unCompreviewTableFile = os.path.join(unCompFilesPath, 'reviews.tbl')
        unCompproductsDicFile = os.path.join(unCompFilesPath, 'products.dic')
        unCompproductsListFile = os.path.join(unCompFilesPath, "products.lst")

        with open(unCompTextDicFile, "r") as unComp_TextDic_File:
            with open(ComptextDicStrFile, "w") as Comp_textDic_Str_File:
                self.buildTextDicStr(unComp_TextDic_File, Comp_textDic_Str_File)

        self.copyFile(unCompcollectionDataFile, CompcollectionDataFile)
        self.copyFile(unCompreviewTableFile, CompreviewTableFile)
                


    def remove(self, dir):
        """Delete all index files by removing the given
        directory
        dir is the path of the directory to be deleted"""
        path = os.path.join(self.out_dir, 'Dir')
        shutil.rmtree(path)
        return 5

    def buildTextDicStr(self, unComp_TextDic_File, Comp_textDic_Str_File):
        list = []
        templine = unComp_TextDic_File.read()
        unComp_TextDic_File = json.loads(templine)
        for key in unComp_TextDic_File:
            list.append(key)
        stringToAdd = "".join(list)
        Comp_textDic_Str_File.write(stringToAdd)
    

    def copyFile(self, original, target):
        shutil.copyfile(original, target)


def main():
    CompressedIndexWriter(os.getcwd(), os.getcwd())


if __name__ == "__main__":
    main()
