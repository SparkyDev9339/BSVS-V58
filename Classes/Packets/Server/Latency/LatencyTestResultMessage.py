from Classes.ClientsManager import ClientsManager
from Classes.Packets.PiranhaMessage import PiranhaMessage


class LatencyTestResultMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        self.writeVInt(1)
        self.writeVInt(2)
        self.writeVInt(3)
        self.writeVInt(4)
        self.writeVInt(5)
        self.writeVInt(6)
        self.writeVInt(7)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(8)
        self.writeString('sprkdv')
        self.writeInt(0)
        self.writeInt(0)
        
        
    def decode(self):
        fields = {}
        fields["PlayerCount"] = self.readVInt()
        super().decode(fields)
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 49001

    def getMessageVersion(self):
        return self.messageVersion