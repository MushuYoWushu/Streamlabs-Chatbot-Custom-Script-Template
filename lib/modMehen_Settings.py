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

import os
import codecs
import json


class MySettings(object):
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")

        except:  # Here we define default parameters for commands and such
            #  Exile Command
            self.Command0 = "!exile"
            self.Cooldown0 = 10
            self.Permission0 = "Moderator"
            self.Info0 = ""
            self.Cost0 = 1234
            #  Fine Command
            self.Command1 = "!fine"
            self.Cooldown1 = 10
            self.Permission1 = "Moderator"
            self.Info1 = ""
            self.Cost1 = 5
            #  Verify Command
            self.Command2 = "!verify"
            self.Cooldown2 = 10
            self.Permission2 = "Moderator"
            self.Info2 = ""
            self.Cost2 = 0

    def Load(self, settingsfile):
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
            self.__dict__ = json.load(f, encoding="utf-8")

        return

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, settingsfile):
        with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
            json.dump(self.__dict__, f, encoding="utf-8")
        with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))

        return
