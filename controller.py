# index of each button
sqaure = 0
X = 1
O = 2
delta = 3

L1 = 4
R1 = 5
L2 = 6
R2 = 7

LStickButton = 10
RStickButton = 11

# index of joyhat(上下左右按键)
Hat_Right = (1, 0)
Hat_Left = (-1,0)
Hat_Up = (0,1)
Hat_Down = (0,-1)

# index of stick axis
'''
LeftStick_LR = 0
LeftStick_UD = 1
LeftStick_LR = 2
LeftStick_UD = 3
'''
LStick_Right = 0
LStick_Left = 1
LStick_Down = 2
LStick_Up = 3
RStick_Right = 4
RStick_Left = 5
RStick_Down = 6
RStick_Up = 7

import numpy as np
import os
import pprint
import pygame
import time
import threading
from recorder import Recorder
import sys
import os
from Speech_to_TextAPI import translate
from MyThread import MyThread
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def clear_folder(path):
    ls = os.listdir(path)
    for tmp in ls:
        c_path = os.path.join(path, tmp)
        if os.path.isdir(c_path):
            clear_folder(c_path)
        else:
            os.remove(c_path)

def write_data(book):
    output = open('data.txt','w',encoding='UTF-8')
    output.write('id\ttime\temotion_id\temotion\tspeech\n')
    for i in range(len(book)):
        for j in range(len(book[i])):
            output.write(str(book[i][j]))
            output.write('\t')   #相当于Tab一下，换一个单元格
        output.write('\n')       #写完一行立马换行
    output.close()

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    eps = 0.8
    n_button = 12 # button number
    n_axis = 6
    controller = None   # controller object

    # data of controller
    axis_data_last = None
    axis_data_current = None
    button_data_last = None # last status of button
    button_data_current = None # current status of button
    button_data_pushdown = None # if last==false && current==true, then pushdown = true
    hat_data = None

    # whether we turned a stick to one direction
    stick_move = None
    stick_move_time = None
    

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        n_button = self.controller.get_numbuttons()
        
        if not self.axis_data_last:
            self.axis_data_last = {}
            for i in range(self.n_axis):
                self.axis_data_last[i] = 0
                
        if not self.axis_data_current:
            self.axis_data_current = {}
            for i in range(self.n_axis):
                self.axis_data_current[i] = 0

        # initial status of each button = false (not pushdown)
        if not self.button_data_last:
            self.button_data_last = {}
            for i in range(self.n_button):
                self.button_data_last[i] = False

        if not self.button_data_current:
            self.button_data_current = {}
            for i in range(self.n_button):
                self.button_data_current[i] = False

        if not self.button_data_pushdown:
            self.button_data_pushdown = {}
            for i in range(self.n_button):
                self.button_data_pushdown[i] = False
        
        if not self.stick_move:
            self.stick_move = {}
            for i in range(8):
                self.stick_move[i] = False

        if not self.stick_move_time:
            self.stick_move_time = {}
            for i in range(8):
                self.stick_move_time[i] = 0

        # inital status of 上下左右按键
        if not self.hat_data:
            self.hat_data = (0, 0)

    def get_status(self):
        # get the status of each button
        for event in pygame.event.get(): 
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data_current[event.axis] = event.value
                
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data_current[event.button] = True
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data = event.value
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data_current[event.button] = False

        # figure out whether the player has push the stick to one of the direction
        if(self.axis_data_current[0] > self.eps and self.axis_data_last[0] < self.eps):
            # self.LStick_Right = True
            self.stick_move_time[LStick_Right] = time.time()
            self.stick_move[LStick_Right] = True
        if(self.axis_data_current[0] < -self.eps and self.axis_data_last[0] > -self.eps):
            # self.LStick_Left = True
            self.stick_move_time[LStick_Left] = time.time()
            self.stick_move[LStick_Left] = True
        if(self.axis_data_current[1] > self.eps and self.axis_data_last[1] < self.eps):
            # self.LStick_Down = True
            self.stick_move_time[LStick_Down] = time.time()
            self.stick_move[LStick_Down] = True
        if(self.axis_data_current[1] < -self.eps and self.axis_data_last[1] > -self.eps):
            # self.LStick_Up = True
            self.stick_move_time[LStick_Up] = time.time()
            self.stick_move[LStick_Up] = True
        if(self.axis_data_current[2] > self.eps and self.axis_data_last[2] < self.eps):
            # self.RStick_Right = True
            self.stick_move_time[RStick_Right] = time.time()
            self.stick_move[RStick_Right] = True
        if(self.axis_data_current[2] < -self.eps and self.axis_data_last[2] > -self.eps):
            # self.RStick_Left = True
            self.stick_move_time[RStick_Left] = time.time()
            self.stick_move[RStick_Left] = True
        if(self.axis_data_current[3] > self.eps and self.axis_data_last[3] < self.eps):
            # self.RStick_Down = True
            self.stick_move_time[RStick_Down] = time.time()
            self.stick_move[RStick_Down] = True
        if(self.axis_data_current[3] < -self.eps and self.axis_data_last[3] > -self.eps):
            # self.RStick_Up = True
            self.stick_move_time[RStick_Up] = time.time()
            self.stick_move[RStick_Up] = True

        for i in range(self.n_axis):
            self.axis_data_last[i] = self.axis_data_current[i]

        # figure out whether each button has been pushed down
        for i in range(self.n_button):
            if(self.button_data_current[i]==True and self.button_data_last[i]==False):
                self.button_data_pushdown[i] = True
            self.button_data_last[i] = self.button_data_current[i]
        
        if(self.button_data_pushdown[LStickButton]):
            if(abs(self.axis_data_current[0])<self.eps and abs(self.axis_data_current[1])<self.eps):
                self.button_data_pushdown[LStickButton] = False

        if(self.button_data_pushdown[RStickButton]):
            if(abs(self.axis_data_current[2])<self.eps and abs(self.axis_data_current[3])<self.eps):
                self.button_data_pushdown[RStickButton] = False
            
        '''
        pprint.pprint(self.button_data_current)
        pprint.pprint(self.axis_data)
        pprint.pprint(self.hat_data)
        print('\n\n')
        '''


if __name__ == "__main__":
    # Instantiates a client
    client = speech.SpeechClient()
    rnd = 0
    book = []
    rowdat = []
    step = 0
    recording = False
    #emotions = {0:'Tranquil',1:'Contented',2:'Joyful',3:'Excited',4:'Fatigued',5:'Upset',6:'Anxious',7:'Angry'}
    emotions = {0:'Angry',1:'Anxious',2:'Upset',3:'Fatigued',4:'Tranquil',5:'Contented',6:'Joyful',7:'Excited'}
    new_emotion = ''
    emotion_id = -1
    
    init_time = time.time()
    ps4 = PS4Controller()
    rec = Recorder()
    ps4.init()
    t0 = time.time()
    T = 0.2    # get controller status every T seconds

    clear_folder('audios')

    while True:
        if(time.time()-t0 > T):
            t0 = time.time()
            ps4.get_status()
            if ps4.button_data_current[X]:
                ''' write translation result into list'''
                print('Start to translate, please wait...')
                config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code='en-US')
                for idx in range(rnd):
                    # Loads the audio into memory
                    fname = 'audios\\{}.mp3'.format(idx)
                    with io.open(fname, 'rb') as audio_file:
                        content = audio_file.read()
                        audio = types.RecognitionAudio(content=content)
                    # Detects speech in the audio file
                    response = client.recognize(config, audio)

                    for result in response.results:
                        Transcript = result.alternatives[0].transcript
                    book[idx].append(Transcript)

                '''write list into txt file'''
                write_data(book)
                sys.exit()


        current_time = time.time()
        current_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(current_time))
        
        if step == 0:
            rowdat = [rnd,current_time_str]
            # get emotion
            if ps4.button_data_pushdown[LStickButton]:
                emotion_id = -1
                tmp = [current_time,current_time,current_time,current_time]
                for i in range(4):
                    if ps4.stick_move[i]:
                        tmp[i] = ps4.stick_move_time[i]
                if min(tmp) < current_time:
                    ttt = 0
                    for j in range(4):
                        if tmp[j] < current_time and tmp[j] > ttt:
                            emotion_id = j
                            ttt = tmp[j]
                        
                if emotion_id >= 0:
                    rowdat.append(emotion_id)
                    rowdat.append(emotions[emotion_id])
                    for i in range(4):
                        ps4.stick_move[i] = False
                    ps4.button_data_pushdown[LStickButton] = False
                    print(rowdat)
                    step += 1
            
            elif ps4.button_data_pushdown[RStickButton]:
                emotion_id = -1
                tmp = [current_time,current_time,current_time,current_time]
                for i in range(4):
                    if ps4.stick_move[i+4]:
                        tmp[i] = ps4.stick_move_time[i+4]
                if min(tmp) < current_time:
                    ttt = 0
                    for j in range(4):
                        if tmp[j] < current_time and tmp[j] > ttt:
                            emotion_id = j+4
                            ttt = tmp[j]
                        
                if emotion_id >= 0:
                    rowdat.append(emotion_id)
                    rowdat.append(emotions[emotion_id])
                    for i in range(4):
                        ps4.stick_move[i+4] = False
                    ps4.button_data_pushdown[RStickButton] = False
                    print(rowdat)
                    step += 1
                
        if step == 1:
            if ps4.button_data_current[O]:
                thread_num = len(threading.enumerate())
                print("Start Recording...")
                # Start recording
                recording = True
                rec.start()
                begin = time.time()
                while recording:
                    if(time.time()-t0 > T):
                        t0 = time.time()
                        ps4.get_status()
                    if ps4.button_data_current[O] == False:
                        rec.stop()
                        fina = time.time()
                        t = fina - begin
                        print('录音时间为%ds'%t)
                        file_name = "audios\\{}.mp3".format(rnd)
                        rec.save(file_name)
                        # threading._start_new_thread(translate,(file_name,))
                        # trans_task = MyThread(translate,(file_name,))
                        # trans_task.start()
                        # print(trans_task.get_result())
                        # rowdat.append('record length: {:.2f}s'.format(t))
                        step += 1
                        recording = False
                        ps4.button_data_pushdown[LStickButton] = False
        
        if step > 1:
            book.append(rowdat)
            rnd += 1
            step = 0

                    
                        
                    


        '''
        if ps4.LStick_Right:
            print("At time {}, Left Stick has been moved to right!".format(current_time))
            ps4.LStick_Right = False
        if ps4.LStick_Left:
            print("At time {}, Left Stick has been moved to left!".format(current_time))
            ps4.LStick_Left = False
        if ps4.LStick_Up:
            print("At time {}, Left Stick has been moved to up!".format(current_time))
            ps4.LStick_Up = False
        if ps4.LStick_Down:
            print("At time {}, Left Stick has been moved to down!".format(current_time))
            ps4.LStick_Down = False
        if ps4.RStick_Right:
            print("At time {}, Right Stick has been moved to right!".format(current_time))
            ps4.RStick_Right = False
        if ps4.RStick_Left:
            print("At time {}, Right Stick has been moved to left!".format(current_time))
            ps4.RStick_Left = False
        if ps4.RStick_Up:
            print("At time {}, Right Stick has been moved to up!".format(current_time))
            ps4.RStick_Up = False
        if ps4.RStick_Down:
            print("At time {}, Right Stick has been moved to down!".format(current_time))
            ps4.RStick_Down = False

        for i in range(ps4.n_button):
            if ps4.button_data_pushdown[i]:
                print("Button{} has been pushed down!".format(i))
                ps4.button_data_pushdown[i] = False
        '''
        
        
            
  
