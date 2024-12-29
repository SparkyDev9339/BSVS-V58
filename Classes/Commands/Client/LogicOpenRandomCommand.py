from Classes.Commands.LogicCommand import LogicCommand
from Classes.Messaging import Messaging

from Database.DatabaseHandler import DatabaseHandler
import json
import time

class LogicOpenRandomCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeVInt(0)
        self.writeDataReference(0)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["Unk1"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        fields["Socket"] = calling_instance.client
        fields["PlayerID"] = calling_instance.player.ID
        for i in range(1):
            player_data['BrawlPassSeason'] = 0
            player_data['RewardForRank'] = 0
            db_instance.updatePlayerData(player_data, calling_instance)
            player_data['RewardForRank'] =  0
            db_instance.updatePlayerData(player_data, calling_instance)
            
            player_data["delivery_items"] = {
            'Boxes': []
            }
            box = {
            'Type': 0,
            'Items': []
            }
            item = {'Amount': 1, 'DataRef': [0, 0], 'RewardID': 8}
            box['Items'].append(item)
            box['Type'] = 100
            player_data["delivery_items"]['Boxes'].append(box)
            
            db_instance.updatePlayerData(player_data, calling_instance)

            fields["Command"] = {"ID": 203}
            time.sleep(5)
            Messaging.sendMessage(24111, fields)

        fields["Command"] = {"ID": 228}
        Messaging.sendMessage(24111, fields)

    def getCommandType(self):
        return 571