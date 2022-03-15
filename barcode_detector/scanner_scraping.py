from scanner import video_capture

from food_scrapping import *

from speech_recog import say
from speech_recog import get_command


## MISSING OVER INFORMATION 
def voice_over_information(info,food_item):
                
        info = info.lower()
        print(info)
        
        if ("ingredients" in info):
            print("INGREDIENTS")
            print(food_item.ingredients)
            say("INGREDIENTS")
            say(food_item.ingredients)
            print()
            
        elif ("allergies" in info):
            print("ALLERGIES")
            print(food_item.allergies)
            say("ALLERGIES")
            say(food_item.allergies)
            print()

        elif ("quantity" in info):
            print("QUANTITY")
            print(food_item.quantity)
            say("QUANTITY")
            say(food_item.quantity)
            print()

        elif ("values" in info):
            print("VALUES")
            print(food_item.nutrition_data.repr())
            say("VALUES")
            say(food_item.nutrition_data.repr())
            print()
            
        elif ("conservation" in info):
            print("CONSERVATION")
            print(food_item.conservation)
            say("CONSERVATION")
            say(food_item.conservation)
            print()

        elif ("exit" in info):
            return
        
        ## Check for number - to print
        else:
            num = ""
            for s in info.split():
                if s.isdigit():
                    num += s

            if (num == food_item.exit_num):
                return
            elif (num in food_item.numbered_values.keys()):
                print (food_item.numbered_values[num])
                say(food_item.numbered_values[num])
            else:
                print("No information about what you are looking was found.")
                print ("Please try again")
                say("No information about what you are looking was found.")
                say ("Please try again")
    
        
        info = None
        while(info == None):
            print()
            print()
            print (food_item.get_titles())
            say (food_item.get_titles())
            info = get_command("Any more information do you want to listen to?")
            if (info != None):
                    voice_over_information(info,food_item)
        
def food_item_titles(food_item):
    if (food_item == None or food_item.name == None):
        print("There is no food item with that barcode.")
        say("There is no food item with that barcode.")
    else:
        print ("We found information about ",food_item.name)
        say ("We found information about " + food_item.name)
        print (food_item.get_titles())
        say (food_item.get_titles())

        info = None
        while(info == None):
            info = get_command("Which information do you want to listen to?")
        
        voice_over_information(info,food_item)
        
def main():

    # scan the barcode - 
    barcodes = video_capture()

    #decode barcode in format that allwos web scrapping 
    barcodes = decode_barcode(barcodes)

    # decode info of barcode by web scrapping 
    food_item = web_scrapping(barcodes)
    #print (food_item.nutrition_data)


    # TALK TO THE USER ABOUT INFORMATION FOUBD 
    food_item_titles(food_item)

        

#PYAUDIO INSTALLATION FOR FOOD ITEM TITLES
main()