from PIL import Image, ImageFilter
import os, sys
import math
import streamlit as st
import time

class DiceArt:

    '''
    Author: v5run

    DiceArt()

    a class used to create an image from images of dice

    Attributes:
    ____________

    og_tile = preferred tile size (length, width) on ORIGINAL image (tuple, default to (30, 30))
    new_tile = preferred tile size (length, width) on NEW image (tuple, default to (300, 300))


    Methods:
    ____________

    resizer() = resizes an image.
        Accepts the original image (string), new length and width (tuple), and a name to save the new resized image (string)

    makecanvas() = creates a new canvas with the same aspect ratio as the original image, except bigger (so the resolution of each image isn't lost). 
        Accepts the original image (string)

    greyscaler() = converts an image into greyscale
        Accepts the original image (string)

    dice_paste() = pastes the dice onto the new canvas
        Accepts the original image (string) and a name to save the new artpiece (string)

    tile_brightness() = calculates the brightness of a certain section/"tile" of the original image. This will return a string corresponding to the preferred dice image to replace this section of the image. The dice is then pasted in dice_paste().
        Accepts the top left coordinate on the original image (tuple)

    art() = starting function, used to call the corresponding functions above in order
        Accepts the original image (string) and a name to save the new artpiece (string) 
    '''

    def __init__(self, og_tile: tuple = (30, 30), new_tile: tuple = (300, 300)) -> None: 

        self.og_tile = og_tile
        self.tile = new_tile
        self.canvas = ""

    def resizer(self, image, new_lw: tuple, name):
        '''
        resizes an image
        _____________

        image = image that is needed to be resized -> string

        new_lw = new length and width of resized image -> tuple (length, width)

        name = name of new, resized image -> string
        '''

        im = Image.open(image)
        new_image = im.resize(new_lw)

        new_image.save(name)

    def makecanvas(self, og_image):

        '''
        makes a new canvas to paste images on based on the aspect ratio / dimensions of the original image.

        _______________

        og_image = original image -> string
        '''

        image = Image.open(og_image)
        og_size = image.size

        og_length = self.og_tile[0]
        og_width = self.og_tile[1]

        newL = self.tile[0]
        newW = self.tile[1]
        
        new_length = int((og_size[0]/og_length) * newL)
        new_width = int((og_size[1]/og_width) * newW)

        new_canvas = Image.new("RGBA", (new_length, new_width), color=(255, 255, 255))

        self.canvas = new_canvas
        new_canvas.save("canvas.png")

    def greyscaler(self, image):

        '''
        returns a greyscaled image.
        ___________

        image = string of image to be greyscaled
        '''

        img = Image.open(image).convert('L')
        img.save("gray.png")


    def dice_paste(self, original, name):

        '''
        pastes images of dice onto the new canvas, by looping through the length + width of the new canvas. Returns the finished artpiece (image)
        __________________

        original = a string representing the original image
        name = a name to save the new artpiece (string)
        '''

        original = Image.open(original)
        
        new = self.canvas

        x_length = self.tile[0]
        y_length = self.tile[1]

        # ratio of original image : new canvas
        ratio = self.canvas.size[0] // original.size[0]

        # loop through x and y of new canvas by tile dimensions to avoid unnecessary pasting
        for x in range( 0, self.canvas.size[0] + 1, x_length ):
            for y in range( 0, self.canvas.size[1] + 1, y_length ):

                #print(x, y)

                # the x on the original image are the current X divided by the ratio calculated. Same with the Y
                newx = int(x / ratio)
                newy = int(y / ratio)
                #print(x, y)


                # call upon helper function to calculate the tile brightnesses on the original image. Send the new x and y values calculated (which
                # represent the top left coordinate value). The helper will return a string corresponding to a specific side on the die
                img = self.tile_brightness( (newx, newy) )
                #print(img)


                dice = Image.open(img)

                # paste the returned dice image from tile_brightness() onto the new canvas
                new.paste(dice, (x, y))

        # save the new image under the provided name
        new.save(name)

    
    def tile_brightness(self, coordinate):

        '''
        a function that calculates the average brightness of a "tile" on the original image, and thus returns a string representing a specific side of a die
        ___________

        coordinate = a tuple representing the top left pixel of a "tile" / section of the original image
        '''

        #opens the greyscaled, original image
        img = Image.open("gray.png")
        rgb_im = img.convert('RGB')

        # total brightness counter
        brightness = 0

        #loop through x and y of a tile on greyscaled image, given the top left coordinate of the tile
        for x in range( coordinate[0], coordinate[0] + self.og_tile[0] ):
            for y in range( coordinate[1], coordinate[1] + self.og_tile[1] ):
                
                # conditional to make sure the x and y coordinates are within the boundaries of the image (x is less than the total length, vice versa)
                if x < rgb_im.size[0] and y < rgb_im.size[1]:
                    pix = rgb_im.getpixel((x, y))
                    #print(pix)
                    
                    # find average brightness of pixel through sum of RGB values, then divide by 3 values
                    avg_b = sum(pix) / 3
                    #print(avg_b)

                    # tally brightness from each pixel in tile
                    brightness += avg_b

        # average brightness of tile = total brightness tallied / area of tile
        average = int(brightness / (self.og_tile[0] * self.og_tile[1]))

        
        #returns a string given the possible brightnesses, range(0, 255) -> 255 / 6 sides = about 43
        if average in range(0, 43): #dark image
            return str("1.png")

        elif average in range(43, 86):
            return str("2.png")

        elif average in range(86, 129):
            return str("3.png")

        elif average in range(129, 172):
            return str("4.png")

        elif average in range(172, 215):
            return str("6.png")

        elif average in range(215, 256): #light image
            return str("5.png")


    def art(self, original, name):

        '''
        the starting function, that calls the other functions in order. Returns None
        _______________________

        original = a string representing the original image
        name = a name to save the new artpiece (string)
        '''

        progresstext = "Give us a moment while we get this done for you"
        my_bar = st.progress(0, text=progresstext)
        p_complete = 0
        
        image = Image.open(original)

        #conditional to check if the length and width of the original image are multiples of the original tile dimensions
        if image.size[0] % self.og_tile[0] != 0 or image.size[1] % self.og_tile[1] != 0:

            newlength = ((image.size[0] // self.og_tile[0]) * self.og_tile[0]) + self.og_tile[0]
            newwidth = ((image.size[1] // self.og_tile[1]) * self.og_tile[1]) + self.og_tile[1]

            #print(newlength, newwidth)

            self.resizer(original, (newlength, newwidth), "resized.png")

            original = "resized.png"

        self.makecanvas(original)
        p_complete+=33
        my_bar.progress(p_complete, text=progresstext)
        
        self.greyscaler(original)
        p_complete+=33
        my_bar.progress(p_complete, text=progresstext)
        
        self.dice_paste(original, name)
        p_complete+=34
        my_bar.progress(p_complete, text=progresstext)

        #resize image back to original length and width to maintain proportion
        self.resizer("final.png",(image.size[0], image.size[1]), "final.png")

        return None

d = DiceArt()
#d.resizer("inverted-dice-6.png", (300, 300), "6.png")
#d.greyscaler("barack.png")

try:
    st.write(""" 
            # DiceArt.io
            ### Hey there! How's it going? This is *DiceArt.io*, a surface for "creativists" to drop an image of their choice and watch as it turns into each and every pixel into a form of dice! One-sided? 6-sided? Have 'em all!
            ## Try it for yourself, upload an image! """)

    uploaded_file = st.file_uploader("")
    st.image(uploaded_file, caption="So this is the image, huh?")
    
    time.sleep(1)
    
    d.art(uploaded_file, "final.png")

    st.image("final.png", caption="Now that's a lot of dice ...", output_format="PNG")
    st.balloons()
    
    with open("final.png", "rb") as file:
        st.download_button(
                label="Download the 'Diced' Image (PNG)",
                data=file,
                file_name="diced.png"
            )
    
    st.success("Done! Try Downloading the image above!")
    
except:
    pass
