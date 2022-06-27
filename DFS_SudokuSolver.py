"""
SUDOKU SOLVER,
AI used: Depth-First-Search/Backtracking
"""
#-------------------------------
import string
#-------------------------------
class Sudoku:
    variant = "Classic"
    rules = "Fill in the grid with numbers 1 to 9, so that no number repeats in a row, a column or a 3x3 box."
    exampleGrid =  [[0,0,5,0,0,4,7,0,9],
                    [0,3,0,0,9,0,0,6,0],
                    [8,0,0,6,0,0,3,0,5],
                    [0,0,3,0,2,0,0,0,7],
                    [0,8,0,1,0,3,0,9,0],
                    [9,0,0,0,4,0,5,0,0],
                    [5,0,8,0,0,9,0,0,4],
                    [0,7,0,0,6,0,0,2,0],
                    [6,0,1,7,0,0,9,0,0]] 

    def __init__(self, grid):
        self.grid = grid
        self.numOfSol = 0

    def copyExampleGridtoGrid(self):
        """
        Copies example grid into the grid.
        """
        self.grid = self.exampleGrid

    def printRules(self):
        """
        Prints the rules of the sudoku.
        """
        print(self.variant)
        print(self.rules)

    def printGrid(self):
        """
        Prints the current state of the grid.
        """
        i = 0
        for row in self.grid:
            i+=1
            print(row[0:3],"|",row[3:6],"|",row[6:])
            if (i % 3 == 0):
                print("---------------------------------")

    def checkValidGrid(self):
        """
        Checks the entered clue numbers are valid according to the rules of the Variant.
        """
        for posx in range(0,9):
            for posy in range(0,9):
                if (self.grid[posx][posy] != 0):
                    fixedNum = self.grid[posx][posy]
                    self.grid[posx][posy] = 0           #A 0 must be temporarily placed, otherwise the following method will fail because the number will find itself already in the position
                    if not(self.tryGuess(fixedNum, posx, posy)):
                        return False
                    self.grid[posx][posy] = fixedNum    #Returning the number back to its position
    
        return True

    def tryClassic(self, tryNum, posx, posy):
        """
        Checks if the given number can be placed at the given position according to the rules of CLASSIC sudoku.
        """
        for i in range(0,9):
            if (tryNum == self.grid[posx][i]):
                return False

        for j in range(0,9):
            if (tryNum == self.grid[j][posy]):
                return False

        offx = 3 * (posx//3)
        offy = 3 * (posy//3)
        for k in range(0,3):
            for l in range(0,3):
                if (tryNum == self.grid[offx+k][offy+l]):
                    return False

        return True
   
    def tryVariant(self, tryNum, posx, posy):
        """
        This method is a placeholder for derived classes of VARIANT Sudoku.
        """
        return True

    def tryGuess(self, tryNum, posx, posy):
        """
        Checks if the given number can be placed at the given position according to all given rules.
        """
        if not(self.tryClassic(tryNum, posx, posy))or not(self.tryVariant(tryNum, posx, posy)):
            return False

        return True

    def solveGrid(self):
        """
        Solves the grid via the Backtracking algorithm. It finds and prints up to 3 possible solutions of the grid.
        """
        for posx in range(0,9):
            for posy in range(0,9):
                if (self.grid[posx][posy] == 0):
                    for tryNum in range(1,10):
                        if (self.tryGuess(tryNum, posx, posy)):
                            self.grid[posx][posy] = tryNum
                            self.solveGrid()
                            self.grid[posx][posy] = 0
                            if (self.numOfSol == 3):    #To quit looking for solutions after 3 solutions are found.
                                break
                    return
        self.numOfSol += 1
        self.printGrid()
        print("--------------------------------------------")

class Nonconsecutive(Sudoku):
    variant = "Nonconsecutive"
    rules = Sudoku.rules + " Numbers that share an edge cannot have a difference of 1."
    exampleGrid =  [[8,0,7,0,0,2,6,0,5],
                    [0,0,0,0,3,0,0,0,0],
                    [5,0,4,1,0,0,3,0,2],
                    [0,0,9,0,0,0,0,0,8],
                    [0,2,0,0,8,0,0,9,0],
                    [4,0,0,0,0,0,2,0,0],
                    [6,0,8,0,0,3,9,0,7],
                    [0,0,0,0,4,0,0,0,0],
                    [3,0,5,2,0,0,4,0,6]]

    def __init__(self, grid):
       Sudoku.__init__(self, grid)

    def tryVariant(self, tryNum, posx, posy):
        """
        Checks if the given number can be placed at the given position according to the rules of the variant sudoku.
        """
        for offx, offy in [[0,1],[0,-1],[1,0],[-1,0]]:
            positx = posx + offx
            posity = posy + offy
            if (0 <= positx)and(positx <=8):
                if (0 <= posity)and(posity <=8):
                    if self.grid[positx][posity] != 0:      #To avoid errors for the pair 0 and 1
                        if ((tryNum + 1) == self.grid[positx][posity])or((tryNum - 1) == self.grid[positx][posity]):
                            return False

        return True

class Antiknight(Sudoku):
    variant = "Antiknight"
    rules = Sudoku.rules + " Identical numbers cannot be a knight's move apart."
    exampleGrid =  [[0,8,6,0,0,0,4,0,0],
                    [0,0,0,3,0,7,0,0,0],
                    [1,0,7,0,0,0,5,0,8],
                    [2,0,8,6,0,5,3,0,4],
                    [0,0,0,0,0,0,0,0,0],
                    [4,0,9,1,0,2,6,0,5],
                    [7,0,1,0,0,0,8,0,3],
                    [0,0,0,7,0,8,0,0,0],
                    [0,0,2,0,0,0,7,4,0]]

    def __init__(self, grid):
       Sudoku.__init__(self, grid)

    def tryVariant(self, tryNum, posx, posy):
        """
        Checks if the given number can be placed at the given position according to the rules of the variant sudoku.
        """
        for offx, offy in [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]:    #List of all 8 possible Knight's moves
            positx = posx + offx
            posity = posy + offy
            if (0 <= positx)and(positx <=8):
                if (0 <= posity)and(posity <=8):
                    if tryNum == self.grid[positx][posity]:
                        return False

        return True
      
class Quadro(Sudoku):
    variant = "Quadro"
    rules = Sudoku.rules + " Every 2x2 box must contain at least one even and one odd number."
    exampleGrid =  [[6,0,0,0,5,0,0,4,0],
                    [0,9,8,0,0,0,3,0,1],
                    [0,0,1,9,7,0,0,2,0],
                    [7,0,5,0,0,0,0,0,0],
                    [0,4,0,0,0,7,5,0,6],
                    [2,0,0,0,0,0,0,0,0],
                    [0,2,0,0,0,0,0,5,3],
                    [0,0,0,0,9,0,7,1,0],
                    [0,0,7,0,4,0,0,0,8]]

    def __init__(self, grid):
       Sudoku.__init__(self, grid)

    def tryVariant(self, tryNum, posx, posy):
        """
        Checks if the given number can be placed at the given position according to the rules of the variant sudoku.
        """
        for offx, offy in [[-1,-1],[-1,0],[0,-1],[0,0]]:        #the offset from posx, posy to the upper left corner of every 2x2 box
            oddCount = 0
            evenCount = 0
            if (tryNum % 2 == 0):
                evenCount += 1
            else:
                oddCount += 1

            for offBoxx in range(0,2):
                for offBoxy in range(0,2):
                    positx = posx + offx + offBoxx 
                    posity = posy + offy + offBoxy
                    if (0 <= positx)and(positx <=8):
                        if (0 <= posity)and(posity <=8):
                            num = self.grid[positx][posity]
                            if (num == 0):
                                continue
                            elif (num % 2 == 0):
                                evenCount += 1
                            else:
                                oddCount += 1     

            if (evenCount == 4)or(oddCount == 4):
                return False

        return True
#----------------------------------
while True:
    print("Which type of sudoku will be solved? Enter 0 for Classic, 1 for Nonconsecutive, 2 for Quadro or 3 for Antiknight.")
    choiceV = int(input("Choose: "))
    variantList = ["Classic","Nonconsecutive","Quadro","Antiknight"]
    if (0<=choiceV) and (choiceV<len(variantList)):
        sType = variantList[choiceV]
    else:
        continue

    #An empty Grid to be overriden either manually or by an example grid
    sGrid = [[0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0]]

    print("Enter 0 for a random example of the sudoku of your choice. Enter 1 to enter the sudoku manually.")
    choiceE = int(input("Choose: "))
    print(" ")
    if choiceE != 0:
        print("Give me a Sudoku Grid.")
        userGrid = list()
        while len(userGrid) < 9:
            userRow = input("Give me a row of digits in the format 123456789. Use 0 for empty spaces:")
            if not(len(userRow) == 9):
                print("Enter the row again.")
                continue
            newRow = list()
            for num in userRow:
                if not(num.isdigit()):
                    print("Enter the row again.")
                    break
                newRow.append(int(num))
            if len(newRow) == 9:
                userGrid.append(newRow)
        sGrid = userGrid   

    #Initialize the sudoku
    if sType == "Classic":
        sudoku = Sudoku(sGrid)
    elif sType == "Nonconsecutive":
        sudoku = Nonconsecutive(sGrid)
    elif sType == "Quadro":
        sudoku = Quadro(sGrid)
    elif sType == "Antiknight":
        sudoku = Antiknight(sGrid)  
    
    #Must replace the empty grid with an example grid
    if choiceE == 0:
        sudoku.copyExampleGridtoGrid() 

    #Solving the Sudoku
    sudoku.printRules()
    sudoku.printGrid()
    print("---------------------------------------------------------")

    if sudoku.checkValidGrid():
        sudoku.solveGrid()
        print(f"Finished! {sudoku.numOfSol} solutions found!")
    else:
        print("Not a valid grid! It cannot be solved.")

    userChoice = input("Enter 0 to quit. Anything else to continue.")
    if userChoice == "0":
        break