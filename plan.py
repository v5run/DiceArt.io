#create a plan based for culminating

# in built variables:

    '''
    #IN dice_paste()
    self.length:
    self.width:
    '''

#FUNCTIONS

    # resizer() - resizes an image
    # makecanvas(original image) = divides original size by og tile size, then multiplies this new num by the new tile size (also use length/width checker here ...)
        #length/width checker - dont make this a function, just check if the length and width of the new image is divisible by section lw

    # greyscaler(original image) = greyscales original image
    # dice_paste(new canvas) = function loops through length and width of new canvas and original image, every loop = paste on new canvas (SAVE FINAL IMAGE ON THIS)
        # must be original image loop: loop through lw of original function, get average brightness of 10x10 square ... LOOP THROUGH TILES?????????




#create a new canvas based on aspect ratio of the original picture

    #   1200 : 1200 -->   (1200/10) : (1200/10)   -->    120:120    ->            120 * 100 : 120 * 100             --> NEW CANVAS DIMENSIONS = 12000px x 12000px
    #  original image   original/original portion    tiles x tiles        multiply # of tiles by new sqaure dimens.

    #divide by 10x10 square die, 

#make a resize function
    #resize dice images to 100x100

#grey scale the entirety of the original image
    #img = Image.open('image.png').convert('L')

#divide image into portions of even sizes based on length and width of total image (probably 10x10 pixel)

#based on the total brightness of each section (sum of r values / num of pixels), it will determine the type of dice that section of the image will replace (in terms of black dice)

    #if sum is between ...
        #(0, 43) -> 1 dot die (majority black)
        #(43, 86) -> 2
        #(86, 129) -> 3
        #(129, 172) -> 4
        #(172, 215) -> 5
        #(215, 257) -> 6 (majority white)

'''
how to cycle through sections of image:

    suppose the image is of size (1000x2000)

    for loop through the image sections?

    for x in range(0, canvas length + 1, square length)
        for y in range(0, canvas width + 1, square width)

        find brightness of section by adding r value of each pixel and dividing by 9 ON ORIGINAL IMAGE
        (use helper function)

        paste appropriate die in section
    
'''

#problems that could occur

    #regions can be too big or small (guess and check the proper region?)
    #