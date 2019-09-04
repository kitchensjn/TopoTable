"""
Pixelate and Scale Map

James Kitchens - 08/31/2019

Backend of the map conversion. This code communicates with the GUI used to take maps downloaded from 'terrain.party'
and produce a .csv file with associated heights of each pillar to display map to scale. In doing so, the program takes
the higher resolution map and pixelates it to the resolution expected by the table. Grayscale values (elevation values)
rescaled to the pillar heights based on the footprints of the original map and tables. File is saved in the directory
of original maps.
"""

from PIL import Image                                                                                                                                                       # Python module to work with images

def mean(numbers):                                                                                                                                                          # General arithmetic mean function, takes in a list of numbers
    return float(sum(numbers)) / len(numbers)                                                                                                                               # Return the arithmetic mean

def minMax(list):                                                                                                                                                           # Determines the minimum and maximum values in a list of numbers
    minimum = min(list)                                                                                                                                                     # Stores minimum value
    maximum = max(list)                                                                                                                                                     # Stores maximum value
    return [minimum, maximum]                                                                                                                                               # Returns the two stored values as a list

def elevationDataStrip(README):                                                                                                                                             # Determines the maximum and minimum elevation of the chosen map from the README file in the directory
    for line in README:                                                                                                                                                     # Loops over the lines in the README
        if " through " in line:                                                                                                                                             # Identifies the line containing the desired elevation data (ex. '0 through 108 meters.')
            elevationData = line                                                                                                                                            # Stores this string of text
            break                                                                                                                                                           # Breaks the loop as this is the only important line
    elevationData = elevationData.replace(' meters.\n', '').split(' through ')                                                                                              # Strips the string of unnecessary information and splits into list
    elevationData = [int(x) for x in elevationData]                                                                                                                         # Converts the elevation values as strings into integers
    return elevationData                                                                                                                                                    # Returns the elevation values as integers in a list

def pixelDataLossIndex(original, new):                                                                                                                                      # Determines how well the pixelated map represents the original
    sumOfDifferences = 0                                                                                                                                                    # Creates a integer variable that will represent the sum of the elevation differences
    for pixel in original:                                                                                                                                                  # Loops over each pixel in the original
        sumOfDifferences += abs(pixel - new)                                                                                                                                # Sums the absolute value difference between the original elevation and the pixelated elevation representing that region
    return sumOfDifferences                                                                                                                                                 # Returns this value, representing the error of the pixelated version (certain maps are more accurately represented with fewer pillars than others)

def pixelateMap(pwd, fileName, n_pillars):                                                                                                                                  # Reduces the resolution of the map to fit the dimensions of the table
    img = Image.open(pwd + '/' + fileName + ' Height Map (Merged).png', 'r')                                                                                                # Opens the original map file
    WIDTH, HEIGHT = img.size                                                                                                                                                # Determines the sizes of the original map
    rawData = list(img.getdata())                                                                                                                                           # Pulls the grayscale data for each pixel as a list
    pixelData = minMax(list=rawData)                                                                                                                                        # Determines the minimum and maximum pixel data from the raw data
    reorganizedData = []                                                                                                                                                    # Creates empty list that will contain the pixel data arranged as a list of lists
    for offset in range(0, WIDTH*HEIGHT, WIDTH):                                                                                                                            # Loops over each row
        reorganizedData.append(rawData[offset:offset + WIDTH])                                                                                                              # Creates a list of pixel data within the row and appends it to empty list
    if n_pillars > HEIGHT:                                                                                                                                                  # Checks that the dimensions of the table are not bigger than the original original map size
        n_pillars = HEIGHT                                                                                                                                                  # If they are, then resets the dimensions to equal the map size
    outMap = Image.new(mode='I', size=(n_pillars, n_pillars))                                                                                                               # Opens a new image file for the pixelated map
    allPixelData = [[[] for i in range(n_pillars)] for j in range(n_pillars)]                                                                                               # Each individual list will contain all pixels associated with pillar
    heightData = []                                                                                                                                                         # Empty list that will contain height info for each pillar
    imageDataLossIndex = 0                                                                                                                                                  # Variable associated with how accurate the new map is to the original [currently unused: imageDataLossIndex += pixelDataLossIndex(original=pillar, new=averageHeight)]
    for workingRow in range(n_pillars):                                                                                                                                     # Loops over rows of pillars
        for workingColumn in range(n_pillars):                                                                                                                              # Loops over columns of pillars
            for highResRow in range(workingRow * (HEIGHT // n_pillars),(workingRow + 1) * (HEIGHT // n_pillars)):                                                           # Loops over rows of pixels
                for highResColumn in range(workingColumn * (HEIGHT // n_pillars), (workingColumn + 1) * (HEIGHT // n_pillars)):                                             # Loops over columns of pillars
                    allPixelData[workingRow][workingColumn].append(reorganizedData[highResRow][highResColumn])                                                              # Adds all pixels associated with a pillar to list
            averageHeight = mean(allPixelData[workingRow][workingColumn])                                                                                                   # Takes mean of grayscale value of all pixels
            heightData.append([workingColumn, workingRow, averageHeight])                                                                                                   # Appends pillar data to list
            outMap.putpixel(xy=(workingColumn, workingRow), value=int(averageHeight))                                                                                       # Adds pixel info to new pixelated map
    outMap.save(pwd + '/' + fileName + ' Height Map (Merged) ' + str(n_pillars) + '.png')                                                                                   # Saves pixelated map
    return heightData, pixelData, imageDataLossIndex                                                                                                                        # Returns the pillar height information list, minimum and maximum pixel list, and data loss index value

def translateMap(heightData, pixelData):                                                                                                                                    # Translates map so that lowest elevation occurs at lowest pillar height
    translatedData = []                                                                                                                                                     # Creates an empty list which will store the translated heights
    for pixel in heightData:                                                                                                                                                # Loops over all pixels
        translatedData.append([pixel[0],pixel[1],pixel[2]-pixelData[0]])                                                                                                    # Subtracts the mininum pixel datum from each pillar datum and stores new datum in list
    return translatedData                                                                                                                                                   # Returns list of new pillar data

def determineScaleFactor(footprint, s_pillars, n_pillars, elevationData, pixelData):                                                                                        # Scales the pixel datas to the elevation data
    factor = ((s_pillars * n_pillars)/footprint)/((pixelData[1]-pixelData[0])/(elevationData[1]-elevationData[0]))                                                          # Uses a function similar to 'map' function in p5.js to rescale using the map's and display's footprints
    return factor                                                                                                                                                           # Returns the scale factor to be multiplied to the pixel data

def scaleMap(heightData, scaleFactor):                                                                                                                                      # Rescales the map using scale factor
    scaledData = []                                                                                                                                                         # Creates an empty list which will store the scaled heights
    for pixel in heightData:                                                                                                                                                # Loops over all of the unscaled pillar heights
        scaledData.append([pixel[0],pixel[1],float(pixel[2])*scaleFactor])                                                                                                  # Scales them and stores in the list
    return scaledData                                                                                                                                                       # Returns the list of scaled pillar heights

def sendToOutFile(pwd, fileName, heightData, s_pillars, n_pillars):                                                                                                         # Writes the pillar height data to a .csv
    outFileName = pwd + '/' + fileName + ' ' + s_pillars + '_' + n_pillars + '.csv'
    outFile = open(outFileName, 'w')                                                                                  # Creates the empty .csv within the directory containing the original maps
    for pixel in heightData:                                                                                                                                                # Loops over all of the pillars
        outFile.write(str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2]) + '\n')                                                                                     # Writes one pillar per line with info for three dimensions
    outFile.close()                                                                                                                                                         # Closes the file
    return outFileName

def fromGUI(folder, footprint, n_pillars, s_pillars):                                                                                                                       # Function to communicate with GUI
    pwd = folder                                                                                                                                                            # Sets present working directory to be map directory
    fileName = pwd.split('/')[-1].replace(' terrain', '')                                                                                                                   # Identifies file naming pattern
    README = open(pwd + '/' + fileName + ' README.txt', 'r')                                                                                                                # Opens README file
    elevationData = elevationDataStrip(README=README)                                                                                                                       # Determines elevation minimum and maximum from README file
    README.close()                                                                                                                                                          # Closes README file
    heightData, pixelData, imageDataLossIndex = pixelateMap(pwd=pwd, fileName=fileName, n_pillars=int(n_pillars))                                                           # Pixelates the original height maps to requested number of pillars
    #print(imageDataLossIndex)                                                                                                                                              # Prints the value pertaining to how well the map is represented [Commented out because not fully implemented]
    heightData = translateMap(heightData=heightData,pixelData=pixelData)                                                                                                    # Translates the pixel data
    scaleFactor = determineScaleFactor(footprint=int(footprint), s_pillars=float(s_pillars), n_pillars=int(n_pillars), elevationData=elevationData, pixelData=pixelData)    # Determines the scale factor
    heightData = scaleMap(heightData=heightData, scaleFactor=scaleFactor)                                                                                                   # Scales the pixel data to the correct height
    outFileName = sendToOutFile(pwd=pwd, fileName=fileName, heightData=heightData, s_pillars=s_pillars, n_pillars=n_pillars)                                                              # Sends this information to a .csv file
    return outFileName