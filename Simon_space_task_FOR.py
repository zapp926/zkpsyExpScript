#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from psychopy import visual, core, event, gui
from numpy import random
import numpy as np
import time, csv, os


def Instruction(displayText):
    textInstruction = visual.TextStim(win, text=u'', height=30, font='Hei', pos=(0.0, 0.0), color='white')
    textInstruction.text = displayText
    textInstruction.draw()
    win.flip()
    core.wait(0)
    keyStart = event.waitKeys()


def IntervalTime(timeDuration):
    textInstruction = visual.TextStim(win, text=u'', height=30, font='Hei', pos=(0.0, 0.0), color='white')
    dtimer = core.CountdownTimer(timeDuration)
    while dtimer.getTime() > 0:
        textInstruction.text = str(int(dtimer.getTime()))
        textInstruction.draw()
        win.flip()


def fixation(fixTime):
    textFixation = visual.TextStim(win, text=u'+', height=72, pos=(0.0, 0.0), color='white',font='Hei')
    textFixation.draw()
    win.flip()
    core.wait(fixTime)

def quitExp():
    for key in event.getKeys():
        if key in ['q']:
            core.quit()
            dataFile.close()


def mainExp(trialNum, fixTime):
    for trial in range(trialNum):
        x1 = random.randint(-500, 200, size=(1,))
        x2 = random.randint(200, 500, size=(1,))
        y1, y2 = random.randint(-400, 400, size=(2,))
        listPos = [(x1, y1), (x2, y2)]
        listRatation = [90, 270]
        random.shuffle(listPos)
        random.shuffle(listRatation)
        # numbers = [i for i in range(-400, 400) if i < -100 or i > 100]
        # n = np.random.choice(numbers, size=(2,))
        # print(n)

        if listRatation[0] == 270:
            Key_answer = 'f'
        else:
            Key_answer = 'j'

        arrowVert = [(-460, 50), (-460, -50), (-200, -50), (-200, -100), (0,0), (-200, 100), (-200, 50)]
        shape_stim_arrow = visual.ShapeStim(win, vertices=arrowVert, fillColor='white', size=0.2, pos=listPos[0])
        shape_stim_arrow.ori = listRatation[0]
        
        fixation(fixTime)
        shape_stim_arrow.draw()
        win.flip()
        core.wait(0)

        clock = core.Clock()
        K_reaction = event.waitKeys(keyList=['f', 'j'], timeStamped=clock)
        result_string = str(K_reaction[0][0]) + ',' + str(K_reaction[0][1]) + ',' + Key_answer + '\n'
        dataFile.write(result_string)

        quitExp()
    dataFile.close()


def experimentEnd(displayEndText):
    Instruction(displayEndText)
    win.close()
    core.quit()


def computeIndex(file_path, file_name):
    list_keypress = []
    list_reaction = []
    list_answer = []
    with open(file_path + '/' + file_name) as f:
        file_csv = csv.reader(f)
        headers = next(file_csv)
        for data_col in file_csv:
            list_keypress.append(data_col[0])
            list_reaction.append(data_col[1])
            list_answer.append(data_col[2])

    count = 0
    for num_stim in range(len(list_keypress)):
        if list_keypress[num_stim] != list_answer[num_stim]:
            count += 1
    accuracy = (len(list_answer) - count) / len(list_answer)

    list_reaction_convert = list(map(float, list_reaction))
    reaction_avg = np.mean(list_reaction_convert)
    reaction_std = np.std(list_reaction_convert)

    for number_detection in list_reaction_convert:
        if number_detection <= reaction_avg - 3*reaction_std or number_detection >= reaction_avg + 3*reaction_std:
            list_reaction_convert.remove(number_detection)
    reaction_avg_dection = np.mean(list_reaction_convert)
    
    return accuracy, reaction_avg_dection


if __name__ == "__main__":
    info = {'name': '', 'gender': '', 'num': '', 'task': ''}
    infoDlg = gui.DlgFromDict(dictionary=info, title=u'基本信息', order=['num', 'name', 'gender', 'task'])
    if not infoDlg.OK:
        core.quit()
    
    pathFile = os.getcwd()
    file_name = '%s.csv'%(info['num'] + '_' + info['name'] + '_' + info['gender'] + '_' + info['task'])
    dataFile = open(pathFile + '/' + file_name, 'a')
    dataFile.write('Key, RT, T&F\n')

    scnWidth, scnHeight = [1920, 1080]
    win = visual.Window((scnWidth, scnHeight), fullscr=True, units='pix', colorSpace='rgb')
    win.mouseVisible = False
    
    disWelcomeText = 'Welcome to the psy experiment.'
    disInstruText = '箭头朝上按「F」键；箭头朝下按「J」键'
    displayEndText = '实验结束，感谢您的参与'
    Instruction(disWelcomeText)
    Instruction(disInstruText)
    IntervalTime(5)
    mainExp(10, 1.2)

    behaviourResult = computeIndex(pathFile, file_name)
    print('ACC: {0}, RT:{1}'.format(round(behaviourResult[0], 2), round(behaviourResult[1], 4)))
 
    experimentEnd(displayEndText)