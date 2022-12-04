import json
import os
import shutil
# first digit: to count which review we are in, 
# second digit: to count all the reviews in file, 
# third digit: number of words in all the reviews. 
# fourth digit: count how many times the word has been in a single review
whichReview = [-1, 0, 0, 0]    
nestedList = [['??????', 1, [0, [['????????', 0]]]]]
tempId = []
listOfReviewsId = []
reviewId = 'id'



class IndexWriter:

    def __init__(self, inputFile, dir):
        """Given product review data, creates an on disk
        index
        inputFile is the path to the file containing the
        review data => its 100.txt or 1000.txt
        dir is the path of the directory in which all index
        files will be created
        if the directory does not exist, it should be
        created"""
        self.inputFile = inputFile
        self.dir = dir
    
        # Path
        path = os.path.join(self.dir, "Dir")     
        # make directory
        os.mkdir(path)

        textDicFile = os.path.join(path, "text.dic")
        textListFile = os.path.join(path, 'text.lst')
        collectionDataFile = os.path.join(path, "collection.data")
        reviewTableFile = os.path.join(path, 'reviews.tbl')
        productsDicFile = os.path.join(path, 'products.dic')
        productsListFile = os.path.join(path, "products.lst")

        with open(self.inputFile,'r+') as readFile:
            with open(textDicFile, 'w') as writeFile:
                with open(textListFile, 'w') as listFile:

                    self.recursion(readFile, writeFile, listFile)

                    # write the dictionary and the pointer list to there files.
                    for list in nestedList:
                        writeFile.write("%s\n" % list) 
                    for list in listOfReviewsId:
                        listFile.write("%s\n" % list)
                    
                    with open(collectionDataFile, 'w') as collectionFile:
                        data = [whichReview[1], whichReview[2]]
                        collectionFile.write("%s\n" % data)

            readFile.seek(0)
            with open(reviewTableFile, 'w') as reviewsTableFile:
                self.buildReviewsTable( readFile, reviewsTableFile)

            readFile.seek(0)
            with open(productsDicFile, 'w') as productDicFile:
                self.buildProductDictionary(readFile, productDicFile, productsListFile)

    def removed (self, dir):
        """Delete all index files by removing the given
        directory
        dir is the path of the directory to be deleted"""
        path = os.path.join(self.dir, 'Dir')
        shutil.rmtree(path)	
        return 5


    # modify the list and write it to the file. 
    # @param file to write to "text.dic"
    # @param the splitted list that i wanna write to the file 
    def WriteToTheFileFunc(self, splittedList):

        checkerList = []
        
        for item in splittedList:
        
            whichReview[2] = whichReview[2] + 1

            # this will move all non alphabatcal letters from the word.
            item = item.lower()
            if item.isalpha() == False:
                for char in item:
                    if char.isalnum() == False:
                        item = item.replace(char, "")
            
            # fill the checker list to check if the word is already exist
            for existWord in nestedList:
                checkerList.append(existWord[0]) 
        
            # if the word is not exist it will be added to dictionary
            if item not in checkerList:
                nestedList.append([item, 1, whichReview[2]])         
                listItem = [whichReview[2], reviewId, 1]
                listOfReviewsId.append(listItem)
    
            # if the word is already exist in the dictionary
            else:     
                for smallList in nestedList:
                    if smallList[0] == item:  
                        smallList[1] = smallList[1] + 1
                        for list in listOfReviewsId:
                            if smallList[2] == list[0]:
                                # if the word has been reapted in the same review id
                                if reviewId == list[1]:
                                    list[2] += 1
                                    break
                                # if the word has been reapted in different review id that has been before
                                else:
                                    toAddList = [list[0], reviewId, 0]
                                    toAddList[2] += 1
                                    listOfReviewsId.append(toAddList)
                                    break
                        break

    # in this function i take every line in the file and check if "review/text" apears
    # in the line and split this line to a list (every word in this list is an item) to write it after that to the text.dic file
    # @param readfile is the file to read from "100.txt",
    # @param writefile is the file to write to "text.dic"
    def recursion(self, readfile, writefile, listFile):

        tempLine = readfile.readline()
        if len(tempLine) == 0:
            return
    
        word = "review/text"
        id = "review/userId"
        global tempId
        global reviewId

        if id in tempLine:
            tempId = tempLine.split()     # it will get the review id 
            tempId.pop(0)
            reviewId = tempId[0]

        if word in tempLine:   

            whichReview[0] = whichReview[0] + 1
            whichReview[1] = whichReview[1] + 1
            splittedList = tempLine.split() 
            splittedList.pop(0)                         # all the text seperated and put in a list
            
            self.WriteToTheFileFunc(splittedList)

            if whichReview[0] == 0:             
                nestedList.pop(0)

            self.recursion(readfile, writefile, listFile)

        else:
            self.recursion(readfile, writefile, listFile)


    def buildReviewsTable(self, readFile, reviewsTableFile):

        proId = "product/productId"
        id = "review/userId"
        profileName = "review/profileName"
        helpFulness = "review/helpfulness"
        score = "review/score"
        time = "review/time"
        summary = "review/summary"
        text = "review/text"
        counter = 1        # this counter defines th id of the dictionary
        DictionaryForAllReviews = {}
        dicId = 'Dict' + str(counter)
        DictionaryForAllReviews[dicId] = {}

        for line in readFile:
    
            if line == '\n':            # when the review ends create another dictionary for the next review
                counter += 1
                dicId = 'Dict' + str(counter)
                DictionaryForAllReviews[dicId] = {}

            if line != '\n':
                checkLine = line.split()
                checkLine.pop(0)
                checkLine2 = checkLine[0]

            if proId in line:  
                DictionaryForAllReviews[dicId][proId] = checkLine2

            if id in line:
                DictionaryForAllReviews[dicId][id] = checkLine2

            if profileName in line:
                DictionaryForAllReviews[dicId][profileName] = checkLine2

            if helpFulness in line:
                DictionaryForAllReviews[dicId][helpFulness] = checkLine2

            if score in line:
                DictionaryForAllReviews[dicId][score] = checkLine2

            if time in line:
                DictionaryForAllReviews[dicId][time] = checkLine2

            if summary in line:
                tempString = ''
                for letter in checkLine:                 # joins all the letters to create the text
                    tempString = " ".join([tempString, letter]) 
                DictionaryForAllReviews[dicId][summary] = tempString[1:]

            if text in line:
                tempString = ''
                for letter in checkLine:               # joins all the letters to create the text
                    tempString = " ".join([tempString, letter]) 
                DictionaryForAllReviews[dicId][text] = tempString[1:]
    
        reviewsTableFile.write(json.dumps(DictionaryForAllReviews, indent=4))                  # add the dictionary to the file in json format



    def buildProductDictionary(self, readFile, productDicFile, productsListFile):

        proId = "product/productId"
        id = "review/userId"
        pointerToList = 1
        numberOfRepetition = 0
        firstMove = 0
        DictionaryForProductsId = {}
        DictionaryProductList = {}
        whichReviewId = 0
    
        reviewsList = []
        for line in readFile:               # add all the reviews in a list called reviewsList
            if id in line:
                tempReviewId = line.split()
                tempReviewId.pop(0)
                tempReviewId = tempReviewId[0]
                reviewsList.append(tempReviewId)

        readFile.seek(0)

        for line in readFile:
            if line == '\n':               # to know which review we are in
                whichReviewId += 1

            if proId in line:
                checkLine = line.split()
                checkLine.pop(0)
                checkLine = checkLine[0]

                if firstMove == 0:
                    DictionaryForProductsId[checkLine] = {}                    # build a dic for the spesific product id
                    DictionaryForProductsId[checkLine][proId] = checkLine
                    DictionaryForProductsId[checkLine]["pointer_To_List"] = pointerToList
                    DictionaryForProductsId[checkLine]["number_of_repetition"] = 1
                    DictionaryProductList[pointerToList] = {}
                    DictionaryProductList[pointerToList]["Review_Id"] = [reviewsList[whichReviewId]]
                        
                keysList = DictionaryForProductsId.keys()

                if firstMove != 0:

                    if checkLine not in keysList:
                        pointerToList += 1
                        DictionaryForProductsId[checkLine] = {}              # build a dic for the spesific product id
                        DictionaryForProductsId[checkLine][proId] = checkLine
                        DictionaryForProductsId[checkLine]["pointer_To_List"] = pointerToList
                        DictionaryForProductsId[checkLine]["number_of_repetition"] = 1
                        DictionaryProductList[pointerToList] = {}
                        DictionaryProductList[pointerToList]["Review_Id"] = [reviewsList[whichReviewId]]

                    else:
                        DictionaryForProductsId[checkLine]["number_of_repetition"] += 1
                        with open(productsListFile, "w") as productListFile:
                            DictionaryProductList[pointerToList]["Review_Id"].append(reviewsList[whichReviewId])          # add the review id to to the list that contains the repeated product
                            productListFile.write(json.dumps(DictionaryProductList, indent=4))
                    
                firstMove += 1

        productDicFile.write(json.dumps(DictionaryForProductsId, indent=4))

