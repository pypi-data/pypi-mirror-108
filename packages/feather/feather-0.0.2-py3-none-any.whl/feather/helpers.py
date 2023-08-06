#------------------------------------------------------------------------------
# Feather SDK
# Proprietary and confidential
# Unauthorized copying of this file, via any medium is strictly prohibited
# 
# (c) Feather - All rights reserved
#------------------------------------------------------------------------------
import json
from json import JSONEncoder
from enum import Enum

class JsonObject:
    def toJSON(self, pretty=True):
        index = None if pretty == False else 4
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=index)

    def fromJSON(self, str):
        self.__dict__ = json.loads(str)

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def isValidFileType(fileType):
    supported = ["images", "video", "audio", ".csv", ".gif", ".jpg", ".json", ".mp3", ".mp4", ".mpeg", ".png", ".tsv", ".txt"]
    return fileType in supported


