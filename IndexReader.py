import json
import os
import ast


class IndexReader:
    def __init__(self, dir):
        """Creates a FirstIndexReader object which will read
        from the given directory
        dir is the path of the directory that contains the
        index files"""
        self.dir = dir
        
    def getProductId(self, reviewId):
        """Returns the product identifier for the given
        review
        Returns None if there is no review with the given
        identifier"""
        productsListFile = os.path.join(self.dir, "Dir", "products.lst")
        productsDicFile = os.path.join(self.dir, "Dir", "products.dic")

        tempReviewId = 0
        isNone = True
        with open(productsListFile, "r") as listFile:
            tempLine = listFile.read()
            tempDic = json.loads(tempLine)
            count = 1
            while count < len(tempDic):
                whichId = str(count)
                if reviewId in tempDic[whichId]["Review_Id"]:
                    tempReviewId = count
                    isNone = False
                    break
                
                count += 1
            if isNone == True:
                print("None")

        with open(productsDicFile, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                whichId = str(count)
                if tempReviewId == tempDic[key]["pointer_To_List"]:
                    print(key)
                    break


    def getReviewScore(self, reviewId):
        """Returns the score for a given review
        Returns None if there is no review with the given
        identifier"""
        allReviews = os.path.join(self.dir, "Dir", "reviews.tbl")
        isNone = True

        with open(allReviews, "r") as ReviewsFile:
            tempLine = ReviewsFile.read()
            tempDic = json.loads(tempLine)
            
            for key in tempDic:
                if len(tempDic[key]) == 0:
                    break
                if reviewId == tempDic[key]["review/userId"]:
                    print(tempDic[key]["review/score"])
                    isNone = False
                    break
                
            if isNone == True:
                print("None")


    def getReviewHelpfulnessNumerator(self, reviewId):
        """Returns the numerator for the helpfulness of a
        given review
        Returns None if there is no review with the given
        identifier"""

        allReviews = os.path.join(self.dir, "Dir", "reviews.tbl")
        isNone = True

        with open(allReviews, "r") as ReviewsFile:
            tempLine = ReviewsFile.read()
            tempDic = json.loads(tempLine)
            
            for key in tempDic:
                if len(tempDic[key]) == 0:
                    break
                if reviewId == tempDic[key]["review/userId"]:
                    tempList = tempDic[key]["review/helpfulness"]
                    tempList = tempList.replace("/", " ")
                    tempList = tempList.split()
                    tempList.pop(1)
                    num = tempList[0]
                    print(num)
                    isNone = False
                    break
                
            if isNone == True:
                print("None")


    def getReviewHelpfulnessDenominator(self, reviewId):
        """Returns the denominator for the helpfulness of a
        given review
        Returns None if there is no review with the given
        identifier"""
        allReviews = os.path.join(self.dir, "Dir", "reviews.tbl")
        isNone = True

        with open(allReviews, "r") as ReviewsFile:
            tempLine = ReviewsFile.read()
            tempDic = json.loads(tempLine)
            
            for key in tempDic:
                if len(tempDic[key]) == 0:
                    break
                if reviewId == tempDic[key]["review/userId"]:
                    tempList = tempDic[key]["review/helpfulness"]
                    tempList = tempList.replace("/", " ")
                    tempList = tempList.split()
                    tempList.pop(0)
                    num = tempList[0]
                    print(num)
                    isNone = False
                    break
                
            if isNone == True:
                print("None")


    def getReviewLength(self, reviewId):
        """Returns the number of tokens in a given review
        Returns None if there is no review with the given
        identifier"""
        allReviews = os.path.join(self.dir, "Dir", "reviews.tbl")
        isNone = True

        with open(allReviews, "r") as ReviewsFile:
            tempLine = ReviewsFile.read()
            tempDic = json.loads(tempLine)
            
            for key in tempDic:
                if len(tempDic[key]) == 0:
                    break
                if reviewId == tempDic[key]["review/userId"]:
                    tempList = tempDic[key]["review/text"]
                    tempList = tempList.split()
                    length = len(tempList)
                    print(length)
                    isNone = False
                    break
                
            if isNone == True:
                print("None")


    def getTokenFrequency(self, token):
        """Return the number of reviews containing a given
        token (i.e., word)
        Returns 0 if there are no reviews containing this
        token"""
        iterationsArr = []
        pointer = 0
        isThere = False
        reviewsTextDic = os.path.join(self.dir, "Dir", "text.dic")
        with open(reviewsTextDic, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if token == key:
                    pointer = tempDic[key]["pointer_To_List"]
                    break

        reviewsTextList = os.path.join(self.dir, "Dir", "text.lst")
        with open(reviewsTextList, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if pointer == int(key):
                    isThere = True
                    for num in tempDic[key]["iteration_times"]:
                        if num != 0:
                            iterationsArr.append(num)
                        
            if isThere == True:
                print(f'({token}) has been repeated in ({len(iterationsArr)}) reviews')
            else:
                print(0)
       

    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given token
        (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing this
        token"""
        data = os.path.join(self.dir, "Dir", "text.dic")
        with open(data, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if token == key:
                    num = tempDic[key]["number_of_repetition"]
                    print(f'({token}) has appeared ({num}) times.')
                    break
            else:
                print(0)


    def getReviewsWithToken(self, token):
        """Returns a series of integers of the form id-1,
        freq-1, id-2, freq-2, ... such
        that id-n is the n-th review containing the given
        token and freq-n is the
        number of times that the token appears in review idn
        Note that the integers should be sorted by id
        Returns an empty Tuple if there are no reviews
        containing this token"""
        pointer = 0
        myTuple = ()
        lelo = []
        reviewsTextDic = os.path.join(self.dir, "Dir", "text.dic")
        with open(reviewsTextDic, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if token == key:
                    pointer = tempDic[key]["pointer_To_List"]
                    break

        reviewsTextList = os.path.join(self.dir, "Dir", "text.lst")
        with open(reviewsTextList, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if pointer == int(key):
                    for num in tempDic[key]["iteration_times"]:
                        if num != 0:
                            myIndex = tempDic[key]["iteration_times"].index(num)
                            review = tempDic[key]["Review_Id"][myIndex]
                            myTuple = myTuple + (review, num)
                            # lelo.append([review, num])
                            tempDic[key]["iteration_times"][myIndex] = 0
                            # tempList = list(myTuple)
                            # tempList.append((review, num))

            print(f'({token}) has been showed in {myTuple}')


    def getNumberOfReviews(self):
        """Return the number of product reviews available in
        the system"""
        data = os.path.join(self.dir, "Dir", "collection.data")
        with open(data, "r") as dataFile:
            tempLine = dataFile.readline()
            tempLine = ast.literal_eval(tempLine)
            print(tempLine[0])


    def getTokenSizeOfReviews(self):
        """Return the number of tokens in the system
        (Tokens should be counted as many times as they
        appear)"""
        data = os.path.join(self.dir, "Dir", "collection.data")
        with open(data, "r") as dataFile:
            tempLine = dataFile.readline()
            tempLine = ast.literal_eval(tempLine)
            print(tempLine[1])


    def getProductReviews(self, productId):
        """Return the ids of the reviews for a given product
        identifier
        Note that the integers returned should be sorted by
        id
        Returns an empty Tuple if there are no reviews for
        this product"""
        productsListFile = os.path.join(self.dir, "Dir", "products.lst")
        productsDicFile = os.path.join(self.dir, "Dir", "products.dic")

        pointer = 0
        with open(productsDicFile, "r") as dicFile:
            tempLine = dicFile.read()
            tempDic = json.loads(tempLine)
            for key in tempDic:
                if productId == tempDic[key]["product/productId"]:
                    pointer = tempDic[key]["pointer_To_List"]
                    break
        
        with open(productsListFile, "r") as listFile:
            tempLine = listFile.read()
            tempDic = json.loads(tempLine)
            temp = str(pointer)
            count = 1
            for key in tempDic:
                if temp == key:
                    print(tuple(tempDic[key]["Review_Id"]))
                    break
                count += 1
