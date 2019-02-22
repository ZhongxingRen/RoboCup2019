#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
from time import sleep
from threading import Thread
import time


class pepper_follow:

    def __init__(self, session):
        self.follow_enable = False
        self.Motion = session.service("ALMotion")
        self.Tracker = session.service("ALTracker")
        self.RobotPos = session.service("ALRobotPosture")
        self.PeoplePer = session.service("ALPeoplePerception")
        self.TextToSpe = session.service("ALTextToSpeech")
        self.PeopPer = session.service("ALPeoplePerception")
        self.Memory = session.service("ALMemory")
        self.People_Dete = self.Memory.subscriber("PeoplePerception/PeopleDetected")
        self.People_Dete.signal.connect(self.callback_people_dete)
        # 设置成true时，所有其他可选的检测（比如脸、运动等）都将停用
        self.PeoplePer.setFastModeEnabled(True)
        # Set Stiffness
        name = "Body"
        stiffness = 1.0
        time = 1.0
        self.Motion.stiffnessInterpolation(name, stiffness, time)
        # Go to posture stand
        speed = 1.0
        self.people_id = 0
        self.RobotPos.goToPosture("Standing", speed)
        # 设置追踪模式
        mode = "Move"
        self.Tracker.setMode(mode)
        # 设置追踪目标
        self.target = "People"
        self.Tracker.trackEvent(self.target)
        # 调小安全距离
        self.Motion.setTangentialSecurityDistance(.05)
        self.Motion.setOrthogonalSecurityDistance(.1)
        # 设置追踪时的距离
        self.Tracker.setRelativePosition([-.5, 0.0, 0.0, 0.1, 0.1, 0.3])
        print("                        ↓                            ")
        print('\033[0;32m [Kamerider I] follow function initialized \033[0m')

    def callback_people_dete(self, msg):
        self.people_id = msg[1][0][0]

    def follow(self):
        time.sleep(1)
        while self.follow_enable:
            if self.people_id == 0:
                print("\033[0;32;40m\t[Kamerider W] : There is nobody in front of me\033[0m")
                self.TextToSpe.say("I can't see you, please adjust the distance between us  ")
                continue
            else:
                self.Tracker.registerTarget(self.target, self.people_id)
                print "registe Target successfully!!"
                break
        while self.follow_enable:
            # 获得机器人躯干坐标系下距离目标的距离
            target_position = self.Tracker.getTargetPosition(0)
            if not target_position:
                continue
            # 距离大于1.7m
            if target_position[0] > 1.7:
                self.TextToSpe.say("Please slow down, I can not follow you")
        self.Tracker.stopTracker()
        self.Tracker.unregisterAllTargets()

    def __del__(self):
        self.Tracker.stopTracker()
        self.Tracker.unregisterAllTargets()