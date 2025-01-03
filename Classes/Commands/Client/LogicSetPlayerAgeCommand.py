import json

from Classes.Commands.LogicCommand import LogicCommand
from Classes.Messaging import Messaging
from Database.DatabaseHandler import DatabaseHandler

class LogicSetPlayerAgeCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeDataReference(0)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["Unk1"] = calling_instance.readVInt()
        fields['Unk2'] = calling_instance.readVInt()
        fields["Unk3"] = calling_instance.readVInt()
        fields['Age'] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        if fields['Age'] <= 18:
            player_data['IntValueEntry']['SocialAge'] = 3
            db_instance.updatePlayerData(player_data, calling_instance)
        if fields['Age'] >= 18:
            player_data['IntValueEntry']['SocialAge'] = 2
            db_instance.updatePlayerData(player_data, calling_instance)

    def getCommandType(self):
        return 530