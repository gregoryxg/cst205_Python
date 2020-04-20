#Shaker Funkhouser, Ryan Westerhoff, Greg Gonzalez
#finalProject.py
#April 14, 2016

'''
List of Commands:
Command:    Action:
go north        move north
go south        move south
go east         move east
go west         move west
examine         check item to see if its useful 
use cauldron        put materials in cauldron and stir
look            get details about room's contents
teleport        move to different random room
help            get a list of commands and their descriptions
inventory       get a list of player inventory
quit            exit program
///////////////////////////////////////////
Indices of each Room List:
0    name of room
1    contents of room
2    number of room
3   (coded) direction of first door
4    (coded) direction of second door

Each room's indices are:
0  room name
1  list of items in room
2  room number
3  list containing direction of first door, and number of the room to which it leads
4  list containing direction of second door, and number of the room to which it leads
'''
printNow("Type \"Game()\" to start the game")

def Game():  
  room0 = ["Kitchen", ["toaster",  "alcohol", "muffin"], 0, ["south", 3],  ["east", 1]]
  room1 = ["Living Room", ["cauldron", "xbox"], 1, ["west", 0], ["east", 2]]
  room2 = ["Bedroom", ["wizard-hat", "crocs", "welders-mask"], 2, ["south", 4], ["west", 1]]
  room3 = ["Dining Room", ["cookie-jar", "butter-beer", "crystal-ball"], 3, ["north", 0], ["east", 4]]
  room4 = ["Bathroom", ["books", "plunger"], 4, ["west", 3], ["north", 2]]
  room5 = ["Secret Lair", ["pizza"], 5, ["west", 5], ["east", 5]]
  rooms = [room0, room1, room2, room3, room4, room5]  
  
  #Player selects game directory where sound and image files exist, then dictionary containing the files is returned.
  files = getFiles()  
  #curRN is the number of the current room
  curRN = 2
  #maxMoves is the maximum number of moves one can make in the game
  maxMoves = 12
  #Main loop condition
  condition = true
  #player's list of items
  inventory = []  
  #counter helps keep track of moves
  counter = 0
  
  show(files['title'])
  play(files['intro'])
  name = requestString("Enter your name")
  #This is the main function that handles the game
  printNow(("You awaken in a potion-induced stupor, feeling very ashamed. Your experiment last nigth had... unpredictable results."))
  printNow(("You perceive ravenous hunger, and must consume wizard pizza as soon as possible, or the unthinkable may happen."))
  printNow(("There is only one place to find wizard pizza, and it is only accessible via a secret spell.")) 
  printNow(("However, the wizard's ill-behaved wizard lizard has scattered the reagents of the spell."))
  printNow(("Now you must find them. Quickly!"))
  printNow(("If you don't find the pieces quickly (within "+str(maxMoves)+" exertions), you will perish."))
  help()
  #describes current room (setting up game)
  look(rooms, curRN, files)
  
  #Main loop:    
  while(condition):
    #Check if current room is living room, and provide hint about cauldron:
    if curRN == 1:
      printNow("The cauldron in the middle of the room seems like a great place to put stuff (HINT, HINT).")
    #request user input:
    mainResponse = requestString("What would you like to do? To review the commands available, type help")
    mainResponse = mainResponse.upper()
    #testing lose condition:
    if counter >= maxMoves:
      play(files['gameOver'])
      printNow("The wizard perishes from hunger (lame). You lose.")
      condition = false
      break
    if mainResponse == "HELP":
      help()
      printNow("You are in the " + rooms[curRN][0])
    elif mainResponse == "LOOK":
      printNow("You are in the " + rooms[curRN][0])
      look(rooms, curRN, files)
    elif mainResponse.startswith("EXAMINE"):
      mainResponse = mainResponse.lower()
      response = mainResponse.split(" ")      
      subR = response[1]      
      if rooms[curRN][1].count(subR) > 0:
        examine(inventory, subR, rooms, curRN, files)
      else:
        printNow("You must be seeing things... that item is not in this room.")        
     
    elif mainResponse.startswith("USE"):
      mainResponse = mainResponse.lower()
      response = mainResponse.split(" ")      
      subR = response[1]
      if rooms[curRN][1].count(subR) > 0:
        if subR == "cauldron":
          if(use(inventory, rooms, curRN, files)):
            curRN = 5
            play(files['teleport'])            
        #evaluate win condition
        elif subR == "pizza" and curRN == 5:
          show(files['wizardpizza'])
          play(files['gameWin'])
          printNow("Congratulations, "+str(name)+". You win! (It's about time!)")
          condition = false
          break
        else:
          printNow("Using this item doesn't further your quest for pizza.")        
        counter += 1
        printNow("This wizard is really hungry... moves remaining: " + str(maxMoves - counter))
      else:
        printNow("You must be seeing things... that item is not in this room.")        
     
    elif mainResponse == "TELEPORT":
      play(files['teleport'])
      curRN = teleport(curRN)
      printNow("You are in the " + rooms[curRN][0])
      look(rooms, curRN, files)
      counter += 1
      printNow("This wizard is really hungry... moves remaining: " + str(maxMoves - counter))
      
    elif mainResponse == "INVENTORY" or mainResponse == "I":
      printInventory(inventory)
     
    elif mainResponse.startswith("GO"):
      response = mainResponse.split(" ")      
      subR = response[1]
      curRN = move(rooms, curRN, subR)
      printNow("You are in the " + rooms[curRN][0])
      look(rooms, curRN, files)
      counter += 1
      printNow("This wizard is really hungry... moves remaining: " + str(maxMoves - counter))
      
    elif mainResponse == "QUIT":
      condition == false
      break
      
    else:
      printNow("Invalid command")
      printNow("You are in the " + rooms[curRN][0])
      
    printNow("****************")        

def getFiles():  
  showInformation("Please select the game folder")
  gameDir = pickAFolder()
  
  #Sound files
  intro = makeSound(gameDir +"GameIntro.wav")
  useful = makeSound(gameDir +"UsefulItemDiscovery.wav")
  notUseful = makeSound(gameDir +"OtherItemDiscovery.wav")
  teleport = makeSound(gameDir +"Teleport.wav")
  gameWin = makeSound(gameDir +"GameWin.wav")
  gameOver = makeSound(gameDir +"GameOver.wav")
  
  #JPEG files
  title = makePicture(gameDir +"titlescreen.jpg")
  bedroom = makePicture(gameDir +"bedroom.jpg") 
  bathroom = makePicture(gameDir +"bathroom.jpg")
  diningroom = makePicture(gameDir +"diningroom.jpg")
  kitchen = makePicture(gameDir +"kitchen.jpg")
  livingroom = makePicture(gameDir +"livingroom.jpg")
  wizardpizza = makePicture(gameDir +"wizardpizza.jpg")
  
  files = {'intro':intro, 'useful':useful, 'notUseful':notUseful, 'teleport':teleport, 'gameWin':gameWin, 'gameOver':gameOver,
           'title':title, 'bedroom':bedroom, 'bathroom':bathroom, 'diningroom':diningroom, 'kitchen':kitchen, 'livingroom':livingroom, 'wizardpizza':wizardpizza}
  return files

def help():
  #These are the main commands and their descriptions;
  #The first index of each command is the prompt; the second index is the description.
  mainPrompts = [["quit", "exit game"], ["go", "Move in specified direction: north, south, east, or west"], ["examine","Examine object"], ["use", "Attempt to use object"],["look", "Get details about room"], ["teleport", "Move player to random room"], ["help","get descritptions of commands"], ["inventory", "get list of items in your inventory"]]
  printNow((""))
  printNow(("Here are the commands: "))
  for i in range(0, len(mainPrompts)):
    message = ("" + mainPrompts[i][0] + ": " + mainPrompts[i][1])
    printNow(message)
  
#provide details about the current room
def look(rooms, roomNumber, files):  
  printNow("")
  printNow("There is one door to the " + rooms[roomNumber][3][0])
  printNow("There is a second door to the " + rooms[roomNumber][4][0] + ".")
  printNow("")
  printNow("This room contains: ")
  for i in range(0, len(rooms[roomNumber][1])):
    printNow("     " + rooms[roomNumber][1][i])
  
  if (rooms[roomNumber][0] == "Bedroom"):
    show(files['bedroom'])
  elif (rooms[roomNumber][0] == "Bathroom"):
   show(files['bathroom'])
  elif (rooms[roomNumber][0] == "Dining Room"):
   show(files['diningroom'])
  elif (rooms[roomNumber][0] == "Kitchen"):
   show(files['kitchen'])
  elif (rooms[roomNumber][0] == "Living Room"):
     show(files['livingroom'])

#moves player to adjacent room, if there is a door in specified direction    
def move(rooms, roomNumber, direction):
  direction = direction.lower()
  if direction == rooms[roomNumber][3][0]:
    roomNumber = rooms[roomNumber][3][1]
  elif direction == rooms[roomNumber][4][0]:
    roomNumber = rooms[roomNumber][4][1]
  else:
    printNow("There's a wall in that direction.")
  
  return roomNumber
  
#used for teleport function
def randGen(x): # Generated a random number from 0 to x
 import random 
 return random.randint(0,x)
 
#move player to random room
def teleport(roomNumber):
  rand = randGen(4)
  while(roomNumber == rand):
    rand = randGen(4)
  return rand

def printInventory(inventory):
  printNow("These are the items in your inventory: ")
  if len(inventory) > 0:
    for i in inventory:
      printNow(i)
  else:
    printNow("You've got nothing. NOTHING!")

#look at specified object, provide details if relevant
def examine(inventory, itemName, rooms, roomNumber, files):
  itemName = itemName.lower()
  if itemName == "pizza" and roomNumber == 5:
    printNow("Stop looking at it and eat (use) it!")
  elif itemName == "plunger" or itemName == "cookie-jar" or itemName == "wizard-hat" or itemName == "toaster":
    indexOfItem = rooms[roomNumber][1].index(itemName)
    rooms[roomNumber][1].pop(indexOfItem)
    printNow("You have a tingling sensation... this must be useful.")
    play(files['useful'])   
    if itemName == "plunger":      
      inventory.append("wand")
      printNow("The plunger... it's turned into a wand!")
    elif itemName == "toaster":
      inventory.append("recipe")
      printNow("A recipe popped out of the toaster, and the toaster vanished!")
    elif itemName == "cookie-jar":
      inventory.append("stardust")
      printNow("There's nothing but crumbs... Oh wait... that's stardust!")
    elif itemName == "wizard-hat":      
      inventory.append("soap")
      printNow("You find soap in the wizard-hat... better not to ask questions.")    
  else:
    printNow("This does not appear to have any magical application.")
    play(files['notUseful'])

#test object for usefulness  
def use(inventory, rooms, roomNumber, files):
  if len(inventory) == 4 and roomNumber == 1:
    printNow("You have all four items necessary to achieve teleportation to the wizard pizza repository.")
    printNow("You place them ever so delicately in the cauldron, wave the wand, and... voila...")
    roomNumber = 5
    printNow("You are in the secret room!")
    look(rooms, 5, files)
    return true
  else:
    printNow("You have a lack of mojo with the present materials (YOU NEED MORE STUFF).")
    return false
    
