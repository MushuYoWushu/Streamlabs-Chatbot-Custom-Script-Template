# modMehen, a moderation suite for StreamLabs ChatBot
# Copyright (C) 2019  MushuYoWushu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# NOTE: This program is only intended for use with Python 2.7.13 and Streamlabs Chatbot
# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json

# If you have files with the same name pointed to by this it will find the FIRST one in the path and not the
# one in the project directory
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references

import clr

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
# The settings file CANNOT have the same name as other settings files that the bot uses. Conform to the convention
# (project_name)_Settings, to minimize this risk
from modMehen_Settings import MySettings

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "Mod Mehen"
Website = "https://github.com/MushuYoWushu"
Description = "Provides some mod tools to manage users"
Creator = "MushuYoWushu"
Version = "1.0.0"


# ---------------------------
#   Define Utility Classes
# ---------------------------
#  Initialize the SettingTable with default values
# Tuples are in "Command: Command, Permission, Info, Cooldown, Cost"
class SearchTable(object):
    def __init__(self, init_settings):
        # Here we define default parameters for commands and such
        self.__dict__ = {
            init_settings.Command0: {'COMMAND': 'True', 'PERMISSION': init_settings.Permission0,
                                     'INFO': init_settings.Info0, 'COOLDOWN': init_settings.Cooldown0,
                                     'COST': init_settings.Cost0},
            init_settings.Command1: {'COMMAND': 'True', 'PERMISSION': init_settings.Permission1,
                                     'INFO': init_settings.Info1, 'COOLDOWN': init_settings.Cooldown1,
                                     'COST': init_settings.Cost1},
            init_settings.Command2: {'COMMAND': 'True', 'PERMISSION': init_settings.Permission2,
                                     'INFO': init_settings.Info2, 'COOLDOWN': init_settings.Cooldown2,
                                     'COST': init_settings.Cost2}
        }

    def update(self, mysettings):
        self.__dict__ = {
            mysettings.Command0: {'COMMAND': 'True', 'PERMISSION': mysettings.Permission0, 'INFO': mysettings.Info0,
                                  'COOLDOWN': mysettings.Cooldown0, 'COST': mysettings.Cost0},
            mysettings.Command1: {'COMMAND': 'True', 'PERMISSION': mysettings.Permission1, 'INFO': mysettings.Info1,
                                  'COOLDOWN': mysettings.Cooldown1, 'COST': mysettings.Cost1},
            mysettings.Command2: {'COMMAND': 'True', 'PERMISSION': mysettings.Permission2, 'INFO': mysettings.Info2,
                                  'COOLDOWN': mysettings.Cooldown2, 'COST': mysettings.Cost2}
        }


# ---------------------------
#   Define Global Variables
# ---------------------------
global SettingsFile
SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
global ScriptSettings
ScriptSettings = MySettings()
global SettingTable
SettingTable = SearchTable(ScriptSettings)


# ---------------------------
#   [Required] Initialize Data (Only called on load/reload)
# ---------------------------

def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings.Load(SettingsFile)
    #  Parent.SendStreamMessage("Load Triggered")
    SettingTable.update(ScriptSettings)

    return


# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------


def Execute(data):
    # Raw data scope
    if data.IsChatMessage():  # Is public message?

        #  Parent.SendStreamMessage(data.UserName + " sent a public message")
        if parse_command(data.GetParam(0).lower(), 'COMMAND') == 'True':  # Is valid command?
            command = data.GetParam(0).lower()
            #  Parent.SendStreamMessage(data.UserName + ", the command is valid.")

            if not Parent.IsOnUserCooldown(ScriptName, command, data.User):  # Is the user NOT on cooldown
                #  Parent.SendStreamMessage(data.UserName + " is not on cooldown.")

                if Parent.HasPermission(data.User, parse_command(command, 'PERMISSION'), parse_command(command, 'INFO')):
                    if Parent.GetPoints(data.User) >= int(parse_command(command, 'COST')):  # The user has enough pts
                        Parent.RemovePoints(data.User, data.UserName, int(parse_command(command, 'COST')))
                        Parent.BroadcastWsEvent("EVENT_MINE", "{'show':false}")

                        #  if-elif chains are ugly but since we can't use 'Parent' outside of Execute() we can't use a
                        #  dictionary lookup like normal because it will execute everything in it when it builds itself
                        #  ********Define Commmand logic here********
                        if command == ScriptSettings.Command0:  # ----------------------------!exile $targetid
                            userid = data.GetParam(1).lower()
                            username = Parent.GetDisplayName(userid)
                            target_pts = Parent.GetPoints(userid)
                            if not target_pts:
                                Parent.SendStreamMessage("This user is not in our ranks")
                            else:
                                Parent.RemovePoints(userid, username, target_pts)
                                Parent.SendStreamMessage(username + " was successfully erased from our ranks.")
                        elif command == ScriptSettings.Command1:  # --------------------------!fine $targetid $value
                            userid, penalty = data.GetParam(1).lower(), int(data.GetParam(2).lower())
                            username, target_pts = Parent.GetDisplayName(userid), int(Parent.GetPoints(userid))
                            if not target_pts:
                                Parent.SendStreamMessage("This user is not in our ranks")
                            else:
                                if penalty > target_pts:  # Don't fine more than they have
                                    penalty = target_pts
                                Parent.RemovePoints(userid, username, penalty)
                                Parent.SendStreamMessage(username + " was fined " + str(penalty) + " Dicecoin.")
                        elif command == ScriptSettings.Command2:  # --------------------------!verify
                            target_pts = int(Parent.GetPoints(data.User))
                            if not target_pts:
                                Parent.AddPoints(data.User, data.UserName, 1)
                                Parent.SendStreamMessage("Thanks for verifying " + data.UserName + "! Welcome to the chat!")
                            else:
                                Parent.SendStreamMessage("You're good with verification " + data.UserName + "!")
                        else:
                            Parent.SendStreamMessage(
                                data.UserName + "ERROR-DNE: Execution could not find command logic.")

                        Parent.AddUserCooldown(ScriptName, command, data.User,
                                               parse_command(command, 'COOLDOWN'))  # Put the command on cooldown
                    else:
                        Parent.SendStreamMessage(data.UserName + " you have " + str(Parent.GetPoints(data.User))
                                                 + " Dicecoin and I require " + str(parse_command(command, 'COST')) +
                                                 " to do that.")  # No cash
                else:
                    Parent.SendStreamMessage(data.UserName + " you are unauthorized to use that tool.")  # No permission
            else:  # They are on cooldown
                Parent.SendStreamMessage(data.UserName + " you are still on cooldown for that, you have " +
                                         str(Parent.GetUserCooldownDuration(ScriptName, command, data.User)) +
                                         " seconds left to wait.")
        #  isChatMessage() Scope
        if not int(Parent.GetPoints(data.User)): #  User has no currency
            Parent.SendStreamMessage("Hey " + data.UserName + "! Could you (re)read the rules and type " + ScriptSettings.Command2 + " to let me know?")

    return


# ---------------------------
#   [Optional] Debits users for calling paid functionality
# ---------------------------


def parse_command(command, elem):  # Checks to see if a command is a valid command
    command = SettingTable.__dict__.get(command)
    if command is None:  # there is no entry for 'command'
        return 'False'
    else:
        return command[elem]


# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return


# ---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
# ---------------------------


def Parse(parseString, userid, username, targetid, targetname, message):
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter", "I am a cat!")

    return parseString


# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------


def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    SettingTable.update(ScriptSettings)
    ScriptSettings.Reload(jsonData)
    #  Parent.SendStreamMessage("Reload Triggered")


    return


# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------


def Unload():
    return


# ---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
# ---------------------------


def ScriptToggled(state):
    return
