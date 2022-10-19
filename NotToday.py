# width is set to 1280x720. PLEASE dont change it might affect the game
# source for OnImage https://pixabay.com/vectors/hook-check-mark-check-completed-1727484/ and offImage https://pixabay.com/vectors/false-error-is-missing-absent-x-2061132/
# source for student https://pixabay.com/vectors/cap-school-graduation-1266204/, source for deadlin https://pixabay.com/illustrations/deadline-rubber-stamp-red-due-date-481452/
from tkinter import Tk, Canvas, Frame, PhotoImage, Button, Entry, Label
import time
import random
import os


def mouse_move(event):  # based on mouse_stuff.py from lectures
    global reset
    x = event.x
    y = event.y
    blocked = False # becomes true if path is blocked by other object
    if light: # needed when cheatcode is thereisanother, when light is red resets
        if canvas.itemcget(lightsOval, "fill") == "#FF2E2E":
            reset = True
    global moved
    if(not bossButtonStatus and not pauseButtonStatus and not end):#does not allow to move when game ended, pause, or boss button was pressed
        for i in range(objects):  # checks above which box cursor is and moves it
            boxPos = canvas.coords(boxes[i]) # saves coordinates rectangle
            if x < boxPos[2] and x > boxPos[0] and y < boxPos[3] and y > boxPos[1]:#checks if any box collides with cursor

                if types[i] == "s":  # checks type of box, and makes it move in specific direction
                    for j in range(objects):#checks if other rectangles block it
                        collPos = canvas.coords(boxes[j])
                        if (j != i) and (collPos[0] < (x + ((height / 6) * lengths[i]) / 2) - 30 and collPos[2] > (x-((height / 6) * lengths[i]) / 2) + 30 and collPos[1] < boxPos[3] and collPos[3] > boxPos[1]):
                            blocked = True
                            break
                    # checks if box left left corner of screen
                    if (x-((height / 6) * lengths[i]) / 2) + 30 < 0:
                        blocked = True

                    # checks if left right border
                    elif (x + ((height / 6) * lengths[i]) / 2) - 30 > border1Pos[0] and boxPos[1] < border1Pos[3] and boxPos[3] > border1Pos[1]:
                        blocked = True

                    # checks if left right border
                    elif (x + ((height / 6) * lengths[i]) / 2) - 30 > border2Pos[0] and boxPos[1] < border2Pos[3] and boxPos[3] > border2Pos[1]:
                        blocked = True
                    if not blocked:
                        previousPosition[i] = boxPos
                        moved = i
                        canvas.coords(boxes[i], x-((height / 6) * lengths[i]) / 2,
                                      boxPos[1], x + ((height / 6) * lengths[i]) / 2, boxPos[3])
                        boxPos = canvas.coords(boxes[i])
                        if i == 0:# needed for UNLIMITEDPOWER cheatcode
                            canvas.coords(images[0], boxPos[0], boxPos[1])
                        elif not blind:
                            canvas.coords(images[i], boxPos[0], boxPos[1])

                else:
                    for j in range(objects):#checks if other rectangles block it
                        collPos = canvas.coords(boxes[j])
                        if (j != i) and (collPos[0] < boxPos[2] and collPos[2] > boxPos[0] and collPos[1] < (y + ((height / 6) * lengths[i]) / 2) - 30 and collPos[3] > (y-((height / 6) * lengths[i]) / 2) + 30):
                            blocked = True
                            break
                    # checks if left bottom corner of screen
                    if (y + ((height / 6) * lengths[i]) / 2) - 30 > height:
                        blocked = True

                    # checks if border left toop corner of screen
                    elif (y-((height / 6) * lengths[i]) / 2) + 30 < 0:
                        blocked = True

                    if not blocked:#moves only if it isnt blocked
                        previousPosition[i] = boxPos
                        moved = i
                        canvas.coords(boxes[i], boxPos[0], y-((height / 6) * lengths[i]
                                                              ) / 2, boxPos[2], y + ((height / 6) * lengths[i]) / 2)
                        boxPos = canvas.coords(boxes[i])
                        if i == 0:# needed for UNLIMITEDPOWER cheatcode
                            canvas.coords(images[0], boxPos[0], boxPos[1])
                        elif not blind:
                            canvas.coords(images[i], boxPos[0], boxPos[1])


def windowDimensions(width, height):  # sets up window based on snake game
    window = Tk()
    window.title("Not Today")
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth / 2) - (width/2)
    y = (screenHeight / 2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    return window


def menuShow():  # displays menu
    for index, value in enumerate(menuOptions, start=1):
        print(" " + str(index) + ". " + value)
    while True:
        choice = input("Type in number of your choice: ")
        try:
            choice = int(choice)
            if not choice in range(1, 6):
                print("Chose either 1, 2, 3, 4 or 5")
            else:
                break
        except:
            print("Chose either 1, 2, 3, 4 or 5")
    return choice


def leaderBoard():  # displays leaderboard
    # leaders are saved in a file
    LeaderboardFile = open("leaderboard.txt", "r")
    title_text = canvas.create_text(
        width / 2, 50, text="LEADERBOARD", fill="yellow", font=("Helvetica", 40, 'bold'), anchor="n")
    lines = LeaderboardFile.readlines()
    for i in range(5):  # there are 5 places in leaderboard
        inputs = lines[i].split()
        if inputs[1] == "-1.0":#if leader file is not fool it has -1.0 in it, and for that we have special text
            inputs[1] = "???"
        else:
            if int(int(round(float(inputs[1]), 0)) % 60) < 10:#calculates how many seconds it took, and if amount is lower than 10 adds 0 before, for visual appeal
                secondsText = "0" + \
                    str(int(int(round(float(inputs[1]), 0)) % 60))
            else:
                secondsText = str(int(int(round(float(inputs[1]), 0)) % 60))
            if int(int(round(float(inputs[1]), 0)) / 60) < 10:#calculates how many minutes it took, and if amount is lower than 10 adds 0 before, for visual appeal
                minutesText = "0" + \
                    str(int(int(round(float(inputs[1]), 0)) / 60))
            else:
                minutesText = str(int(int(round(float(inputs[1]), 0)) / 60))
            inputs[1] = minutesText + ":" + secondsText
        number_text = canvas.create_text(
            width / 2 - 300, 200 + 100 * i, text=inputs[0], fill='white', font=("Arial Black", 20, 'bold'))
        time_text = canvas.create_text(
            width / 2, 200 + 100 * i, text=inputs[1], fill='white', font=("Arial Black", 20, 'bold'))
        name_text = canvas.create_text(
            width / 2 + 300, 200 + 100 * i, text=inputs[2], fill='white', font=("Arial Black", 20, 'bold'))
        if (i == 0):  # first place is different
            canvas.itemconfig(number_text, fill="red")
            canvas.itemconfig(time_text, fill="red")
            canvas.itemconfig(name_text, fill="red")
    LeaderboardFile.close()


def settingsLayout():  # sets settings window layout
    title_text = canvas.create_text(
        width / 2, 50, text="SETTINGS", fill="yellow", font=("Helvetica", 40, 'bold'), anchor="n")
    bossButton_text = canvas.create_text(
        width / 2 - 100, 200, text="Boss Key [B]*", fill='white', font=("Arial Black", 20, 'bold'))
    pauseButton_text = canvas.create_text(
        width / 2 - 100, 300, text="Pause Key [P]**", fill='white', font=("Arial Black", 20, 'bold'))
    cheats_text = canvas.create_text(
        width / 2 - 100, 400, text="Cheats***", fill='white', font=("Arial Black", 20, 'bold'))
    for i in range(3):  # sets required image, which displays current settings
        if(status[i]):
            image[i] = on_image
        else:
            image[i] = off_image
    button[0] = Button(canvas, image=image[0], width=50, height=50,
                       bg="black", command=lambda: settings_handle_click(0))
    button[1] = Button(canvas, image=image[1], width=50, height=50,
                       bg="black", command=lambda: settings_handle_click(1))
    button[2] = Button(canvas, image=image[2], width=50, height=50,
                       bg="black", command=lambda: settings_handle_click(2))
    button[0].place(x=width/2 + 100, y=175)
    button[1].place(x=width/2 + 100, y=275)
    button[2].place(x=width/2 + 100, y=375)
    cheats_text = canvas.create_text(
        width / 2, 500, text="TIP: You can press 'Escape' to exit if you are not in game!", fill='white', font=("Arial Black", 20, 'bold'))
    # explanation for all settings:
    bexplenationText = "*Flips to an image that gives the impression that the player is working ;)"
    pexplenationText = "**Pauses the game. You never know when you will need a break!"
    chexplenationText = "***Allows to type in cheat codes (It's a secret that only devs know)"
    bossButton_explain = canvas.create_text(
        width / 2 - 400, height - 90, text=bexplenationText, fill='white', font=("Arial Black", 14), anchor="w")
    pauseButton_explain = canvas.create_text(
        width / 2 - 400, height - 60, text=pexplenationText, fill='white', font=("Arial Black", 14), anchor="w")
    cheats_explain = canvas.create_text(
        width / 2 - 400, height - 30, text=chexplenationText, fill='white', font=("Arial Black", 14), anchor="w")


def settings_handle_click(buttonId):# for buttons in settings
    if(status[buttonId]): # flips to opposite image
        button[buttonId].configure(image=off_image)
    else:
        button[buttonId].configure(image=on_image)
    status[buttonId] = not status[buttonId]

def playGame(): # main function which is active during the game
    global currentLevel, boxes, types, lengths, objects, previousPosition, startTime, timePlayed, reset, end, blind, light, timeLightsStart
    mainPos = canvas.coords(boxes[0])  # position of main box
    if light:
        if canvas.itemcget(lightsOval, "fill") == "#36FEAD" and round(time.time(), 0) - round(timeLightsStart, 0) == 5:
            timeLightsStart = time.time()
            canvas.itemconfig(lightsOval, fill="#FF2E2E")
        elif canvas.itemcget(lightsOval, "fill") == "#FF2E2E" and round(time.time(), 0) - round(timeLightsStart, 0) == 5:
            timeLightsStart = time.time()
            canvas.itemconfig(lightsOval, fill="#36FEAD")
    if not end and not pauseButtonStatus and not bossButtonStatus:
        displayTime = timePlayed + time.time() - startTime
        if int(int(round(displayTime, 0)) % 60) < 10:
            secondsText = "0"+str(int(int(round(displayTime, 0)) % 60))
        else:
            secondsText = str(int(int(round(displayTime, 0)) % 60))
        if int(int(round(displayTime, 0)) / 60) < 10:
            minutesText = "0"+str(int(int(round(displayTime, 0)) / 60))
        else:
            minutesText = str(int(int(round(displayTime, 0)) / 60))
        canvas.itemconfig(time_text, text=minutesText + ":" + secondsText)
    nextLevel = False
    collision = False
    # checks for collisions and leaving borders and moves objects so that they no longer collide
    i = moved
    boxPos = canvas.coords(boxes[i])  # goes through all boxes

    if boxPos[0] < 0:  # checks if box left left corner of screen
        canvas.coords(boxes[i], 0, boxPos[1], 0 +
                      ((height / 6) * lengths[i]), boxPos[3])
        boxPos = canvas.coords(boxes[i])
        if i == 0:
            canvas.coords(images[0], boxPos[0], boxPos[1])
        elif not blind:
            canvas.coords(images[i], boxPos[0], boxPos[1])
    # checks if left right border
    elif boxPos[2] > border1Pos[0] and boxPos[1] < border1Pos[3] and boxPos[3] > border1Pos[1]:
        canvas.coords(boxes[i], border1Pos[0] - ((height / 6)
                                                 * lengths[i]), boxPos[1], border1Pos[0], boxPos[3])
        boxPos = canvas.coords(boxes[i])
        if i == 0:
            canvas.coords(images[0], boxPos[0], boxPos[1])
        elif not blind:
            canvas.coords(images[i], boxPos[0], boxPos[1])
    # checks if left right border
    elif boxPos[2] > border2Pos[0] and boxPos[1] < border2Pos[3] and boxPos[3] > border2Pos[1]:
        canvas.coords(boxes[i], border2Pos[0] - ((height / 6)
                                                 * lengths[i]), boxPos[1], border2Pos[0], boxPos[3])
        boxPos = canvas.coords(boxes[i])
        if i == 0:
            canvas.coords(images[0], boxPos[0], boxPos[1])
        elif not blind:
            canvas.coords(images[i], boxPos[0], boxPos[1])
    elif boxPos[3] > height:  # checks if left bottom corner of screen
        canvas.coords(boxes[i], boxPos[0], height -
                      ((height / 6) * lengths[i]), boxPos[2], height)
        boxPos = canvas.coords(boxes[i])
        if i == 0:
            canvas.coords(images[0], boxPos[0], boxPos[1])
        elif not blind:
            canvas.coords(images[i], boxPos[0], boxPos[1])
    elif boxPos[1] < 0:  # checks if border left toop corner of screen
        canvas.coords(boxes[i], boxPos[0], 0, boxPos[2],
                      0 + ((height / 6) * lengths[i]))
        boxPos = canvas.coords(boxes[i])
        if i == 0:
            canvas.coords(images[0], boxPos[0], boxPos[1])
        elif not blind:
            canvas.coords(images[i], boxPos[0], boxPos[1])
    for j in range(objects):  # checks if collides with other boxes
        collPos = canvas.coords(boxes[j])
        if (i != j and (collPos[0] < boxPos[2] and collPos[2] > boxPos[0] and collPos[1] < boxPos[3] and collPos[3] > boxPos[1])):

            if types[i] == "s":

                if previousPosition[i][0] < collPos[0]:
                    canvas.coords(
                        boxes[i], collPos[0]-((height / 6) * lengths[i]), boxPos[1], collPos[0], boxPos[3])
                    boxPos = canvas.coords(boxes[i])
                    if i == 0:
                        canvas.coords(images[0], boxPos[0], boxPos[1])
                    elif not blind:
                        canvas.coords(images[i], boxPos[0], boxPos[1])
                else:
                    canvas.coords(boxes[i], collPos[2], boxPos[1],
                                  collPos[2] + ((height / 6) * lengths[i]), boxPos[3])
                    boxPos = canvas.coords(boxes[i])
                    if i == 0:
                        canvas.coords(images[0], boxPos[0], boxPos[1])
                    elif not blind:
                        canvas.coords(images[i], boxPos[0], boxPos[1])
            else:
                if previousPosition[i][1] < collPos[1]:
                    canvas.coords(boxes[i], boxPos[0], collPos[1] -
                                  ((height / 6) * lengths[i]), boxPos[2], collPos[1])
                    boxPos = canvas.coords(boxes[i])
                    if i == 0:
                        canvas.coords(images[0], boxPos[0], boxPos[1])
                    elif not blind:
                        canvas.coords(images[i], boxPos[0], boxPos[1])
                else:
                    canvas.coords(boxes[i], boxPos[0], collPos[3],
                                  boxPos[2], collPos[3] + ((height / 6) * lengths[i]))
                    boxPos = canvas.coords(boxes[i])
                    if i == 0:
                        canvas.coords(images[0], boxPos[0], boxPos[1])
                    elif not blind:
                        canvas.coords(images[i], boxPos[0], boxPos[1])
            break

    if mainPos[0] > border1Pos[2]:  # checks if main rectangle left border(win)
        nextLevel = True

    if exitWindow:# exits window if button exit was pressed
        currentLevel = 1
        window.destroy()

    elif (not exitWindow and not nextLevel and not reset) or end: #if nothing changed loops
        try:
            window.after(250, playGame)
        except:
            pass
    elif reset: # if reset was pressed
        blind = False
        reset = False
        for i in range(objects):
            canvas.delete(boxes[i])
            canvas.delete(images[i])
        previousPosition.clear()
        boxes.clear()
        types.clear()
        images.clear()
        lengths.clear()
        objects = 0
        readLevel()
    elif nextLevel: # if completed
        if currentLevel == 5: # if last level
            canvas.create_text(width/2, height/2, fill="lime",
                               font="Times 80 italic bold", text="Victory!")
            currentLevel = 1
            timePlayed += time.time() - startTime
            leaderFile = open("leaderboard.txt", "r")
            lines = leaderFile.readlines()
            leadersNames = []
            leadersTime = []
            end = True
            nextLevel = False
            for i in range(5):
                inputs = lines[i].split()
                leadersTime.append(float(inputs[1]))
                leadersNames.append(inputs[2])
            leadersTime.append(timePlayed)
            leadersNames.append(name)
            leaderFile.close()
            leaderFile = open("leaderboard.txt", "w")
            for i in range(6): # loads data from leader file
                for j in range(i, 6):
                    if(leadersTime[i] == -1 or (leadersTime[i] > leadersTime[j] and leadersTime[j] != -1)):
                        leadersTime[i], leadersTime[j] = leadersTime[j], leadersTime[i]
                        leadersNames[i], leadersNames[j] = leadersNames[j], leadersNames[i]

            for i in range(5): # arranges scores in order
                leaderFile.write(
                    str(i+1) + ". " + str(leadersTime[i]) + " " + str(leadersNames[i]))
                if i != 4:
                    leaderFile.write("\n")
            leaderFile.close()
            try:
                window.after(250, playGame)
            except:
                pass
        else: # if not final level
            for i in range(objects):
                canvas.delete(boxes[i])
                canvas.delete(images[i])
            previousPosition.clear()
            boxes.clear()
            images.clear()
            types.clear()
            lengths.clear()
            blind = False

            objects = 0
            currentLevel += 1
            readLevel()


def readLevel():
    global boxes, types, lengths, objects, previousPosition, level_text
    level = open("Levels/lvl" + str(currentLevel) +
                 ".txt", "r")  # loads a level from file
    for line in level.readlines(): # reads data from level file
        inputs = line.split()
        types.append(inputs[1])
        lengths.append(int(inputs[2]))
        if(str(inputs[1]) == "s"):  # creates boxes
            xy = ((height / 6) * int(inputs[3]), (height / 6) * int(inputs[4]), (height / 6) * int(
                inputs[3]) + (height / 6) * int(inputs[2]), (height / 6) * int(inputs[4]) + height / 6)
        elif(str(inputs[1]) == "t"):
            xy = ((height / 6) * int(inputs[3]), (height / 6) * int(inputs[4]), (height / 6) * int(
                inputs[3]) + height / 6, (height / 6) * int(inputs[4]) + (height / 6) * int(inputs[2]))
        if objects == 0:
            boxes.append(canvas.create_rectangle(
                xy, fill=inputs[0], outline='white', width=5))
        else:
            boxes.append(canvas.create_rectangle(xy, fill=inputs[0]))
        boxPos = canvas.coords(boxes[objects])
        if objects == 0:
            images.append(canvas.create_image(
                boxPos[0], boxPos[1], image=studentImage, anchor="nw"))
        else:
            if(inputs[1] == "s"):
                if(inputs[2] == "3"):
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=LongHorizontal, anchor="nw"))
                else:
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=ShortHorizontal, anchor="nw"))
            else:
                if(inputs[2] == "3"):
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=LongVertical, anchor="nw"))
                else:
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=ShortVertical, anchor="nw"))

        # saves previous postiotion of box for collision
        previousPosition.append(canvas.coords(boxes[objects]))
        objects += 1
    canvas.itemconfig(
        level_text, text="LEVEL" + str(currentLevel))#updates level text box
    level.close()
    playGame() # read levels


def readSave():# read from save file when load is selected
    global boxes, types, lengths, objects, previousPosition, timePlayed, name, currentLevel, level_text
    saveFile = open("saveFile.txt", "r")# opens save file
    lines = saveFile.readlines()
    for i in range(len(lines) - 1):#reads data from save file input[0] is color, input[1] - type(vertical or horizontal), input[3] length(3 or 2), input[3 to 6] coordinates
        inputs = lines[i].split()
        types.append(inputs[1])
        lengths.append(int(inputs[2]))
        if objects == 0:#sets white outline for first(main) object
            boxes.append(canvas.create_rectangle(
                inputs[3], inputs[4], inputs[5], inputs[6], fill=inputs[0], outline='white', width=5))
        else:
            boxes.append(canvas.create_rectangle(
                inputs[3], inputs[4], inputs[5], inputs[6], fill=str(inputs[0]))) # creates  rectangles
        previousPosition.append(canvas.coords(boxes[objects]))
        boxPos = canvas.coords(boxes[objects]) # saves coordinates of boxes

        if objects == 0: # different image for first rectangle
            images.append(canvas.create_image(
                boxPos[0], boxPos[1], image=studentImage, anchor="nw"))# puts image on top of rectangle
        else:
            if(inputs[1] == "s"):
                if(inputs[2] == "3"):
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=LongHorizontal, anchor="nw")) # puts image on top of rectangle
                else:
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=ShortHorizontal, anchor="nw")) # puts image on top of rectangle
            else:
                if(inputs[2] == "3"):
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=LongVertical, anchor="nw")) # puts image on top of rectangle
                else:
                    images.append(canvas.create_image(
                        boxPos[0], boxPos[1], image=ShortVertical, anchor="nw")) # puts image on top of rectangle
        objects += 1

    inputs = lines[objects].split() # on the last line timeplayed was saved and level on which player finished(saved) and players name
    timePlayed = float(inputs[0])
    currentLevel = int(inputs[1])
    name = inputs[2]
    saveFile.close()
    canvas.itemconfig(
        level_text, text="LEVEL" + str(currentLevel))
    playGame()


def exit_handle_click(): # when exit button in game is pressed
    global exitWindow
    currentLevel = 1
    exitWindow = True


def cheat(event): # for cheat codes when it is activated in settings
    global blind, light, timeLightsStart
    text = cheatEntry.get()
    cheatAnswers = open("Levels/answer" + str(currentLevel) + ".txt", "r")
    lines = cheatAnswers.readlines()
    if(text == "iamtooweak"):# loads answers from asnwer file
        for i in range(objects):
            coordinates = lines[i].split()
            cheatEntry.delete(0, 'end')
            cheatEntry.insert(0, "")
            canvas.coords(boxes[i], int(coordinates[0]) * (height / 6), int(coordinates[2]) * (
                height / 6), int(coordinates[1]) * (height / 6), int(coordinates[3]) * (height / 6)) # puts rectangels into coordinates from previous file
            previousPosition = canvas.coords(boxes[i])
            boxPos = canvas.coords(boxes[i])
            canvas.coords(images[i], boxPos[0], boxPos[1])
    if(text == "UNLIMITEDPOWER"):# activates UNLIMITEDPOWER cheat entry
        for i in range(1, objects): # deletes all images thus all rectangles become black, same color as background as if they are invisble
            canvas.delete(images[i])
        blind = True
        cheatEntry.delete(0, 'end')
        cheatEntry.insert(0, "")
    if (text == "thereisanother"):# activates other cheat code
        canvas.itemconfig(lightsOval, state='normal')
        light = True
        timeLightsStart = time.time()
        cheatEntry.delete(0, 'end')
        cheatEntry.insert(0, "")

    cheatAnswers.close()


def boss_key(event): # when b is pressed and boss key is active in settings
    global bossButtonStatus, startTime, timePlayed

    if not pauseButtonStatus: # doesnt allow for boss button and pause button to be pushed simultaniously
        bossButtonStatus = not bossButtonStatus
        if (bossButtonStatus):
            timePlayed += time.time() - startTime#saves time
            bossImage.pack()
            try:
                cheatEntry.lower()
            except:
                pass
        else:
            try:
                cheatEntry.lift()
            except:
                pass
            startTime = time.time()
            bossImage.pack_forget()


def pause_key(event): # when p is pressed and pause key is active in settings
    global pauseButtonStatus, startTime, timePlayed
    if not bossButtonStatus: # doesnt allow for boss button and pause button to be pushed simultaniously
        pauseButtonStatus = not pauseButtonStatus
        if(pauseButtonStatus):
            timePlayed += time.time() - startTime # saves time
            pauseText.pack()
            try:
                cheatEntry.lower()
            except:
                pass
        else:

            startTime = time.time()
            pauseText.pack_forget()
            try:
                cheatEntry.lift()
            except:
                pass


def save_handle_click():# when save button is pressed while game was active
    saveFile = open("saveFile.txt", "w")
    for i in range(objects):#saves colors coorindates of all rectangles
        boxPos = canvas.coords(boxes[i])
        saveFile.write(str(canvas.itemcget(boxes[i], "fill")) + " " + str(types[i]) + " " + str(lengths[i]) + " " + str(
            boxPos[0]) + " " + str(boxPos[1]) + " " + str(boxPos[2]) + " " + str(boxPos[3]) + "\n")
    global timePlayed, startTime
    timePlayed += time.time() - startTime
    startTime = time.time()
    saveFile.write(str(timePlayed) + " " + str(currentLevel) + " " + str(name))# saves timeplay, current level and name of player
    saveFile.close()


def reset_handle_click():# when reset button is pressed while game was active
    global reset
    reset = True


# BEGGINING
print("Hello there! Welcome to Not Today!")

print("Description:")
print("Game is very intuitive! Push around deadlines so that you can have a free path to relaxation!")

currentLevel = 1 #Holds number of level that player is currently on
while True:  # loop for menu will run until player selects "Exit"
    # change the game title
    print("This is menu. Please select one of the options:")

    menuOptions = ["Start", "Load", "Leaderboard",
                   "Settings", "Exit"]  # all menu options

    choice = menuShow()
    if(menuOptions[choice - 1] == "Start"):  # starts a game

        name = input("What is your name(up to 10 characters)? ")
        while len(name) < 1 or len(name) > 10:
            name = input("Incorrect input! Please try again: ")
    width = 1280  # window dimensions
    height = 720
    window = windowDimensions(width, height)

    on_image = PhotoImage(file="OnImage.png")
    off_image = PhotoImage(file="OffImage.png")
    boss_Image = PhotoImage(file="boss_Image.png")  # made it myself
    # settings for the game are described in this file
    settingFile = open("settings.txt", "r")
    LongVertical = PhotoImage(file="3vertical.png")
    LongHorizontal = PhotoImage(file="3horizontal.png")
    ShortVertical = PhotoImage(file="2vertical.png")
    ShortHorizontal = PhotoImage(file="2horizontal.png")
    studentImage = PhotoImage(file="student1.png")
    status = [None] * 3  # there are 3 settings
    for i in range(3):#opens setting file
        status[i] = bool(int(settingFile.read(1)))
    settingFile.close()

    canvas = Canvas(window, bg="black", width=width, height=height)
    canvas.pack()
    if(menuOptions[choice - 1] == "Start" or menuOptions[choice - 1] == "Load"):
        # moving objects with mouseclick
        canvas.bind('<B1-Motion>', mouse_move)

        boxes = []  # list of movable objects
        images = [] # list of images, they follow rectangles
        objects = 0 # counts amount of rectangles
        exitWindow = False  # status of button which allows to exit
        bossButtonStatus = False # displays if boss Label is active,
        pauseButtonStatus = False # displays if pause Label is active,
        previousPosition = [] # saves previous position of rectangles
        reset = False # saves result if reset button was set
        end = False # status changes when game ends
        blind = False # status which saves if cheat code UNLIMITEDPOWER was typed in
        light = False# status which saves if cheat code thereisanother was typed in
        timePlayed = 0 # final amount of time played, also needed for pause and save to save for how long it was played
        timeLightsStart = 0 # saves current time, for traffic mode (thereisanother cheat code)
        moved = 0 #saved index of rectangle which was moved
        exitbutton = Button(canvas, text="Exit", font=("Arial Black", 40, 'bold'),
                            bg="black", fg="red", command=exit_handle_click, width=5, height=1)
        exitbutton.place(x=(width + height) / 2 - 100, y=height / 2 + 250)
        savebutton = Button(canvas, text="Save", font=("Arial Black", 40, 'bold'),
                            bg="black", fg="green", command=save_handle_click, width=5, height=1)
        savebutton.place(x=(width + height) / 2 - 100, y=height / 2 + 150)
        resetbutton = Button(canvas, text="Reset", font=("Arial Black", 40, 'bold'),
                             bg="black", fg="yellow", command=reset_handle_click, width=5, height=1)
        resetbutton.place(x=(width + height) / 2 - 100, y=height / 2 + 50)
        time_text = canvas.create_text(
            (width + height) / 2 + 10, 100, text="0:00", fill="white", font=("Helvetica", 60, 'bold'), anchor="n") #timer

        if (status[1]):
            pauseText = Label(canvas, text="PAUSE", fg='yellow', font=(
                "Arial Black", 60, 'bold'), bg="black", width=width, height=height)
            window.bind('<p>', pause_key) # activates pause option when 'p' is pressed if it was selected in settings
        if status[0]:
            bossImage = Label(canvas, image=boss_Image,
                              bg="black", width=width, height=height)
            window.bind('<b>', boss_key) # activates boss key option when 'b' is pressed if it was selected in settings
        if (status[2]):
            cheatEntry = Entry(canvas, bg="black", fg="white")
            canvas.create_window(width - 84, 12, window=cheatEntry)
            window.bind('<Return>', cheat) # activates cheat code console if it was selected in settings

        # borders on the east
        border1 = canvas.create_rectangle(
            height, 0, height + 20, (height / 6) * 2, fill="gray")
        border2 = canvas.create_rectangle(
            height, (height / 6) * 3, height + 20, height, fill="gray")
        border1Pos = canvas.coords((border1))
        border2Pos = canvas.coords((border2))
        lightsOval = canvas.create_oval(
            width - height / 6, (height / 6) * 2, width, (height / 6) * 3, fill="#36FEAD", state='hidden') # oval which describes current light (green or red). it is for(thereisanother cheatcode)
        types = []  # saves type of box (vertical or horizontal)
        lengths = []  # saves lengths of boxes (3 wide or 2 wide)
        startTime = time.time() # saves time of start of the game, needed for timer
        level_text = canvas.create_text(
            (width + height) / 2 + 10, 30, text="LEVEL" + str(currentLevel), fill="cyan", font=("Helvetica", 40, 'bold'), anchor="n")#creates text file which show current level
    if(menuOptions[choice - 1] == "Exit"):
        break  # exits loop and as a result a program
    elif(menuOptions[choice - 1] == "Start"):  # starts a game

        readLevel()

    elif(menuOptions[choice - 1] == "Load"):  # loads data from save file

        readSave()

    elif(menuOptions[choice - 1] == "Leaderboard"):
        leaderBoard()
        window.bind("<Escape>", lambda x: window.destroy())
    elif(menuOptions[choice - 1] == "Settings"):

        button = [None] * 3  # list of buttons in settings menu
        image = [None] * 3
        settingsLayout()

        window.bind("<Escape>", lambda x: window.destroy())

    window.mainloop()
    if(menuOptions[choice - 1] == "Settings"):  # saves settings in settings file
        settingFile = open("settings.txt", "w")
        settingFile.write(
            str(int(status[0])) + str(int(status[1])) + str(int(status[2])))
        settingFile.close()
