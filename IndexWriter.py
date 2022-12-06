import json
import os
import shutil


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
            readFile.seek(0)
            with open(collectionDataFile, 'w') as colleactionFile:
                self.buildCollectionData(readFile, colleactionFile)

            readFile.seek(0)
            with open(reviewTableFile, 'w') as reviewsTableFile:
                self.buildReviewsTable(readFile, reviewsTableFile)

            readFile.seek(0)
            with open(productsDicFile, 'w') as productDicFile:
                self.buildProductDictionary(readFile, productDicFile, productsListFile)

            readFile.seek(0)
            with open(textDicFile, 'w') as textDicFile:
                self.buildTextDictionary(readFile, textDicFile, textListFile)


    def removed (self, dir):
        """Delete all index files by removing the given
        directory
        dir is the path of the directory to be deleted"""
        path = os.path.join(self.dir, 'Dir')
        shutil.rmtree(path)	
        return 5



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



    def buildTextDictionary(self, readFile, textDicFile, textListFile):

        textId = "review/text"
        id = "review/userId"
        pointerToList = 1
        numberOfRepetition = 1
        firstMove = 0
        DictionaryForWords = {}
        DictionaryWordsList = {}
        whichReviewId = 0
        co = 0
        bo = False

        reviewsList = []
        for line in readFile:               # add all the reviews in a list called reviewsList
            if id in line:
                    tempReviewId = line.split()
                    tempReviewId.pop(0)
                    tempReviewId = tempReviewId[0]
                    reviewsList.append(tempReviewId)
                    co += 1

        readFile.seek(0)
        for line in readFile:
            if line == '\n':               # to know which review we are in
                whichReviewId += 1

            if textId in line:
                checkLine = line.split()
                checkLine.pop(0)
                while checkLine:
                    word = checkLine[0].lower()
                    if not word.isalpha():
                        for char in word:
                            if not char.isalnum():
                                liso = word.replace(char, " ")
                                liso = liso.split()
                                if liso:
                                    word = liso[0]
                                    for item in liso[1:]:
                                        checkLine.append(item)
                                else:
                                    bo = True
                    if bo:
                        checkLine.pop(0)
                        bo = False
                        continue

                    if firstMove == 0:
                        DictionaryForWords[word] = {}                    # build a dic for the spesific product id
                        DictionaryForWords[word]["word"] = word
                        DictionaryForWords[word]["pointer_To_List"] = pointerToList
                        DictionaryForWords[word]["number_of_repetition"] = numberOfRepetition
                        DictionaryWordsList[pointerToList] = {}
                        DictionaryWordsList[pointerToList]["Review_Id"] = reviewsList
                        DictionaryWordsList[pointerToList]["iteration_times"] = [0] * co
                        DictionaryWordsList[pointerToList]["iteration_times"][whichReviewId]  += 1

                            
                    keysList = DictionaryForWords.keys()

                    if firstMove != 0:

                        if word not in keysList :
                            pointerToList += 1
                            DictionaryForWords[word] = {}              # build a dic for the spesific product id
                            DictionaryForWords[word]["word"] = word
                            DictionaryForWords[word]["pointer_To_List"] = pointerToList
                            DictionaryForWords[word]["number_of_repetition"] = numberOfRepetition
                            DictionaryWordsList[pointerToList] = {}
                            DictionaryWordsList[pointerToList]["Review_Id"] = reviewsList
                            DictionaryWordsList[pointerToList]["iteration_times"] = [0] * co
                            DictionaryWordsList[pointerToList]["iteration_times"][whichReviewId] += 1

                        else:
                            for key in DictionaryForWords:
                                if key == word:
                                    DictionaryForWords[key]["number_of_repetition"] += 1
                                    tempPoi = DictionaryForWords[key]["pointer_To_List"]
                                    DictionaryWordsList[tempPoi]["iteration_times"][whichReviewId] += 1
                                    break
                                                    
                    firstMove += 1
                    checkLine.pop(0)

        with open(textListFile, "w") as textList0: 
            textList0.write(json.dumps(DictionaryWordsList, indent=4))

        textDicFile.write(json.dumps(DictionaryForWords, indent=4))



    def buildCollectionData(self, readFile, colleactionFile):
        
        textId = "review/text"
        numberOfReviews = 0
        numberOfWords = 0

        for line in readFile:
            if line == '\n':              
                numberOfReviews += 1

            if textId in line:
                checkLine = line.split()
                checkLine.pop(0)
                numberOfWords = numberOfWords + len(checkLine)

        collection = [numberOfReviews, numberOfWords]
        colleactionFile.write(f'{collection}')


