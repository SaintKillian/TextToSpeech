import pyttsx3
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# REMEMBER TO TURN ON VPN
def main():
    # Variables    
    startChapter = 185
    endChapter = 190
    playbackSpeed = 300
    folder = "Nightfall"
    baseURL = "https://www.lightnovelspot.com/novel/nightfall-312/chapter-"
    voiceId = 0
    sleeper = 5    

    createFolder(folder)    
    engine = pyttsx3.init()

    options = Options()
    # Stops chrome from opening up everytime
    options.add_argument("--headless")
    # Removes Errors
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dr = webdriver.Chrome(options=options)

    for i in range(startChapter, endChapter+1):    
        URL = baseURL+str(i)
        soup = getSoup(URL, dr)
        name = convertSoupToFile(soup, str(i),folder)
        text = getText(folder + "/" + name)
        convertToSound(text, name, engine, voiceId, playbackSpeed,folder)
        print(f"Completed {name}")
        time.sleep(sleeper)
    dr.close()

# Gets a soup from a URL
def getSoup(URL, dr):
    dr.get(URL)
    page = dr.page_source
    return BeautifulSoup(page, 'html.parser')

# Creates folder if doesn't exist
def createFolder(folder):
    # Check whether the specified path exists or not
    if not os.path.exists(folder):
        os.makedirs(folder)

# Converts a soup to a file
def convertSoupToFile(soup, name, folder="."):
    if soup.find('title') == "Page Not Found":
        print("Error Page Not Found, Stopping" + name)
        exit(0)
    temp = []
    for index, element in enumerate(soup.find_all('p')):
        if index == 1:
            continue
        temp.append(element.text) 
    
    with open(folder+"/"+name, 'w') as f:
        f.write("\n".join(temp))
    return name

# Returns file as a string
def getText(file):
    with open(file) as f:
        l = f.read()
    return l

# Converts text to mp3 'outputFile' 
def convertToSound(text, outputFile, engine, voiceId=0, playbackSpeed=250, folder="."):
    voices = engine.getProperty("voices")
    engine.setProperty("rate", playbackSpeed)
    engine.setProperty("voice", voices[voiceId].id)
    engine.save_to_file(text, folder+"/"+outputFile+".mp3")
    engine.runAndWait()

if  __name__ == '__main__':
    main()
