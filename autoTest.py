import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
#Needed: pass.txt which contains email on line1, password on line2
#geckodriver.exe file needs to be in the folder this code is in, and in your PATH environment variable as well
#also you need to have firefox installed (not guaranteed to work on other browsers)
#make sure the bot is running BEFORE launching this program, and once the program
#launches DO NOT TOUCH ANYTHING on your machine until it is finished

def pressKeyRepeatedly(key, num): #does what it says it does, just a shortcut
    for x in range(num):
        time.sleep(.3)
        pyautogui.press(key)
    time.sleep(.5)

def callBotFunct(functerino):
    pyautogui.typewrite(functerino)
    pyautogui.press("enter")
    time.sleep(2.5) #bot can only respond so fast, this is to clarify output

driver = webdriver.Firefox()
driver.get("https://web.groupme.com/chats")#launch firefox and navigate to groupme

time.sleep(5)

f = open("pass.txt", "r") #stores user and pass from pass.txt file
lines = [line.rstrip('\n') for line in f]
user = lines[0]
passw = lines[1]

pressKeyRepeatedly("tab", 3) #tabs to email box
pyautogui.typewrite(user)    #username from pass.txt
pyautogui.press("tab")       #tabs to password box
pyautogui.typewrite(passw)   #pass from pass.txt
pyautogui.press("enter")
time.sleep(2)

pyautogui.hotkey("ctrl", "f")#this block opens the Search Chat bar
pyautogui.typewrite("search")
pyautogui.press("enter")
pyautogui.press("esc")
time.sleep(2)

pyautogui.typewrite("test")#navigates to the group where bot commands can be sent.
pyautogui.press('enter')   #Mine was called test, hence why it types test
pressKeyRepeatedly("tab", 2)
pyautogui.press("enter")#as of right here, the chatbar is open in the test group
time.sleep(2)


callBotFunct("whois")

callBotFunct("weather Detroit") #weather test for a real city
callBotFunct("weather 48127") #weather test for real zipcode
callBotFunct("weather Ditroyte") #weather test for a fake city
callBotFunct("weather 99192") #weather test for fake zipcode

callBotFunct("google crab rave") #google test

callBotFunct("echo ACHOO") #echo test

callBotFunct("string 1001") #string case 1 (should not work)
callBotFunct("string -5") #string case 2 (should not work)
callBotFunct("string 50") #string case 3 (DOES WORK)
callBotFunct("string 50") #string case 3.1 (testing to make sure it's random)

callBotFunct("Restart")
callBotFunct("echo I have restarted!")

callBotFunct("")

# callBotFunct("exit")#self explanatory
