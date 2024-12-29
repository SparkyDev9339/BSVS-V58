from Classes.ByteStreamHelper import ByteStreamHelper
from Classes.Packets.PiranhaMessage import PiranhaMessage
from Classes.Logic.LogicStarrDropData import starrDropOpening
from datetime import datetime
from Database.DatabaseHandler import DatabaseHandler

import json
import time
import random

class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        Shop = json.loads(open("shop.json", 'r').read())
        Events = json.loads(open("Events.json", 'r').read())

        nowTime = time.time() + 3600 * 4
        EventIndex = 0
        showDownMap = 0
        for EventData in Events['Events']:
            if int(EventData['TimeToEnd']) <= int(nowTime):
                with open('Events.json') as f:
                    data = json.load(f)
                if data['Events'][EventIndex]['Slot'] == 1:
                    data['Events'][EventIndex]['TimeToEnd'] = time.time() + 3600 * 4 + 86400
                    data['Events'][EventIndex]['MapID'] = random.choice([739, 762, 763, 808])
                if data['Events'][EventIndex]['Slot'] == 2:
                    data['Events'][EventIndex]['TimeToEnd'] = time.time() + 3600 * 4 + 43200
                    data['Events'][EventIndex]['MapID'] = random.choice([731, 774, 776, 814])
                    showDownMap = data['Events'][EventIndex]['MapID']
                if data['Events'][EventIndex]['Slot'] == 4:
                    data['Events'][EventIndex]['TimeToEnd'] = time.time() + 3600 * 4 + 14400
                    data['Events'][EventIndex]['MapID'] = random.choice([637, 638, 677, 678])
                if data['Events'][EventIndex]['Slot'] == 5:
                    data['Events'][EventIndex]['TimeToEnd'] = time.time() + 3600 * 4 + 86400
                    data['Events'][EventIndex]['MapID'] = showDownMap + 1
                if data['Events'][EventIndex]['Slot'] == 4:
                    data['Events'][EventIndex]['TimeToEnd'] = time.time() + 3600 * 4 + 86400
                    data['Events'][EventIndex]['MapID'] = random.choice([638, 639, 640, 719])
                with open('Events.json', 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            EventIndex += 1

        db_instance = DatabaseHandler()
        playerData = db_instance.getPlayer(player.ID)

        self.writeVInt(1688816070)
        self.writeVInt(1191532375)
        self.writeVInt(2023189)
        self.writeVInt(73530)

        self.writeVInt(player.Trophies + 5000)
        self.writeVInt(player.HighestTrophies + 5000)
        self.writeVInt(player.HighestTrophies + 5000) 
        self.writeVInt(player.TrophyRoadTier + 200)
        self.writeVInt(player.Experience)
        self.writeDataReference(28, player.Thumbnail)
        self.writeDataReference(43, player.Namecolor)

        self.writeVInt(26)
        for x in range(26):
            self.writeVInt(x)

        self.writeVInt(len(player.SelectedSkins))
        for brawlerID in player.SelectedSkins:
            self.writeDataReference(29, player.SelectedSkins[str(brawlerID)])

        self.writeVInt(0)

        self.writeVInt(0)
        
        self.writeVInt(len(player.OwnedSkins))
        for x in player.OwnedSkins:
            self.writeDataReference(29, x)

        self.writeVInt(0)

        self.writeVInt(0)

        self.writeVInt(0)
        self.writeVInt(player.HighestTrophies)
        self.writeVInt(0)
        self.writeVInt(2)
        self.writeBoolean(True)
        self.writeVInt(115)
        self.writeVInt(335442)
        self.writeVInt(1001442)
        self.writeVInt(5778642) 
        self.writeVInt(0)

        self.writeVInt(120)
        self.writeVInt(200)
        self.writeVInt(0)

        self.writeBoolean(True)
        self.writeVInt(2)
        self.writeVInt(2)
        self.writeVInt(2)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeVInt(0) # Shop Offers

        for shopData in range(0):
            self.writeVInt(len(shopData['Rewards'])) # RewardCount
            for rewardData in shopData['Rewards']:
                self.writeVInt(rewardData['ItemType'])  # ItemType
                self.writeVInt(rewardData['Amount']) # Amount
                self.writeDataReference(rewardData['CsvID'][0], rewardData['CsvID'][1])  # CsvID
                self.writeVInt(rewardData['SkinID']) # SkinID

            self.writeVInt(shopData['Currency']) # Currency(0-Gems, 1-Gold, 3-StarpoInts)
            self.writeVInt(shopData['Cost']) # Cost
            self.writeVInt(0) # Time
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False) # Daily Offer
            self.writeVInt(0) # Old price
            self.writeString(shopData['Text']) # Text
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeString("offer_bgr_sushi") # Background
            self.writeVInt(0)
            self.writeBoolean(False) # This purchase is already being processed
            self.writeVInt(0) # Type Benefit
            self.writeVInt(0) # Benefit
            self.writeString()
            self.writeBoolean(False) # One time offer
            self.writeBoolean(False) # Claimed
            self.writeDataReference(0)
            self.writeDataReference(0)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeBoolean(False)
        
        self.writeVInt(20)
        self.writeVInt(1428)

        self.writeVInt(0)

        self.writeVInt(1)
        self.writeVInt(30)

        self.writeByte(1) # count brawlers selected
        self.writeDataReference(16, player.SelectedBrawlers[0]) # selected brawler

        self.writeString(player.Region) # location
        self.writeString(player.ContentCreator) # supported creator

        self.writeVInt(21)
        self.writeDataReference(2, 1)  # Unknown
        self.writeDataReference(3, player.IntValueEntry['TokensGained'])  # Tokens Gained
        self.writeDataReference(4, player.IntValueEntry['TrophiesGained'])  # Trophies Gained
        self.writeDataReference(6, player.IntValueEntry['DemoAccount'])  # Demo Account
        self.writeDataReference(7, player.IntValueEntry['InvitesBlock'])  # Invites Blocked
        self.writeDataReference(8, player.IntValueEntry['StarPointsGained'])  # Star Points Gained
        self.writeDataReference(9, 1)  # Show Star Points
        self.writeDataReference(10, 0)  # Power Play Trophies Gained
        self.writeDataReference(12, 1)  # Unknown
        self.writeDataReference(14, 0)  # Coins Gained
        self.writeDataReference(15, player.IntValueEntry['SocialAge'])  # AgeScreen | 3 = underage (disable social media) | 1 = age popup
        self.writeDataReference(16, 1)
        self.writeDataReference(17, 0)  # Team Chat Muted
        self.writeDataReference(18, 1)  # Esport Button
        self.writeDataReference(19, 0)  # Champion Ship Lives Buy Popup
        self.writeDataReference(20, player.IntValueEntry['GemsGained'])  # Gems Gained
        self.writeDataReference(21, 1)  # Looking For Team State
        self.writeDataReference(22, 1)
        self.writeDataReference(23, 0)  # Club Trophies Gained
        self.writeDataReference(24, 1)  # Have already watched club league stupid animation
        self.writeDataReference(32447, 28)

        self.writeVInt(0)

        Free32LVL = 0
        Free64LVL = 0
        Free96LVL = 0

        Pass32LVL = 0
        Pass64LVL = 0
        Pass96LVL = 0

        for LVL in player.BrawlPassFreeLevel:
            if LVL < 30:
                Free32LVL += (2**(LVL + 2))
            if LVL > 30:
                Free64LVL += (2**(LVL-30))
            if LVL > 61:
                Free96LVL += (1**(LVL-61))
        
        for LVL in player.BrawlPassLevel:
            if LVL < 30:
                Pass32LVL += (2**(LVL + 2))
            if LVL > 29:
                Pass64LVL += (2**(LVL-30))
            if LVL > 60:
                Pass96LVL += (1**(LVL-61))
        
        if player.BrawlPassBuy == 0:
            BrawlPassActive = False
            BrawlPassPlusActive = False
        if player.BrawlPassBuy == 1:
            BrawlPassActive = True
            BrawlPassPlusActive = False
        if player.BrawlPassBuy == 2:
            BrawlPassActive = True
            BrawlPassPlusActive = True

        # BrawlPassSeasonData::encode
        self.writeVInt(1)
        for season in range(1):
            self.writeVInt(32)
            self.writeVInt(player.BPTokens)
            self.writeBoolean(BrawlPassActive) # BrawlPass buy
            self.writeVInt(0)
            self.writeBoolean(False)

            self.writeBoolean(True)
            self.writeInt(Pass32LVL)
            self.writeInt(Pass64LVL)
            self.writeInt(Pass96LVL)
            self.writeInt(0)

            self.writeBoolean(True)
            self.writeInt(Free32LVL)
            self.writeInt(Free64LVL)
            self.writeInt(Free96LVL)
            self.writeInt(0)

            self.writeBoolean(BrawlPassPlusActive) # BrawlPass + Buy
            self.writeBoolean(True)
            self.writeInt(0)
            self.writeInt(0)
            self.writeInt(0)
            self.writeInt(0)
        # BrawlPassSeasonData::encode

        self.writeBoolean(True)
        self.writeVInt(0)
        self.writeVInt(1)
        self.writeVInt(2)
        self.writeVInt(0) 

        self.writeBoolean(True) # Vanity items
        self.writeVInt(len(player.OwnedThumbnails) + len(player.OwnedPins) + 1)
        for ThumbnailID in player.OwnedThumbnails:
            self.writeDataReference(28, ThumbnailID)
            self.writeVInt(0)
        for PinID in player.OwnedPins:
            self.writeDataReference(52, PinID)
            self.writeVInt(0)
        for i in range(1):
            self.writeDataReference(28, 186) # IconCreator
            self.writeVInt(0)


        self.writeBoolean(False) # Power league season data

        self.writeInt(0)
        self.writeVInt(0)
        self.writeDataReference(16, player.favoriteBrawler) # favoriteBrawler
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeVInt(2023189)

        self.writeVInt(38) # event slot id
        for EventID in range(38):
            self.writeVInt(EventID)
        Events = json.loads(open("Events.json", 'r').read())
        EventIndex = 0

        self.writeVInt(len(Events['Events'])) # Events
        for EventData in Events['Events']:
            self.writeVInt(-1)
            self.writeVInt(EventData['Slot']) # EventSlot
            self.writeVInt(EventData['Slot']) # EventSlot
            self.writeVInt(0)
            self.writeVInt(int(EventData['TimeToEnd']) - int(nowTime))
            self.writeVInt(10) 
            self.writeDataReference(15, EventData['MapID']) # map id
            self.writeVInt(-1)
            self.writeVInt(2) # MapStatus
            self.writeString("")
            self.writeVInt(0)
            self.writeVInt(0)
            if EventData['Slot'] in [20, 21, 22, 23, 24]:
                self.writeVInt(EventData['ChampionShipInfo']['MaxWins']) # Max Wins
            else:
                self.writeVInt(0) # Max Wins
            self.writeVInt(0) # Modifers
            self.writeVInt(0) # Wins
            self.writeVInt(7)
            self.writeBoolean(False) # MapMaker map structure array
            self.writeVInt(0)
            self.writeBoolean(False) # Power League array entry
            self.writeVInt(0)
            self.writeVInt(0)
            if EventData['Slot'] in [20, 21, 22, 23, 24]:
                self.writeBoolean(True) # ChoronosTextEntry::encode
                for ChoronosTextEntry in range(1):
                    self.writeString(EventData['ChampionShipInfo']['ChoronosTextEntry'])
                    self.writeVInt(0)
            else:
                self.writeBoolean(False) # ChoronosTextEntry::encode
            self.writeBoolean(False)
            self.writeBoolean(False)
            if EventData['Slot'] in [20, 21, 22, 23, 24]:
                self.writeBoolean(True)
                for LogicGemOffer in range(1):
                    self.writeVInt(EventData['ChampionShipInfo']['LogicGemOffer']['ID'])
                    self.writeVInt(EventData['ChampionShipInfo']['LogicGemOffer']['Ammount'])
                    self.writeDataReference(EventData['ChampionShipInfo']['LogicGemOffer']['CsvID'][0], EventData['ChampionShipInfo']['LogicGemOffer']['CsvID'][1])
                    self.writeVInt(EventData['ChampionShipInfo']['LogicGemOffer']['SkinID'])
            else:
                self.writeBoolean(False) # LogicGemOffer::encode
            self.writeVInt(-1)
            if EventData['Slot'] in [20, 21, 22, 23, 24]:
                self.writeBoolean(True) # ChronosFileEntry::encode
                for ChronosFileEntry in range(1):
                    self.writeString(EventData['ChampionShipInfo']['ChronosFileEntry']['scName'])
                    self.writeString(EventData['ChampionShipInfo']['ChronosFileEntry']['scFile'])
            self.writeBoolean(False) # ChoronosFileEntry::encode
            self.writeBoolean(False)
            self.writeVInt(-1)
            self.writeVInt(0) 
            self.writeVInt(0) 
            self.writeVInt(0) 
            self.writeBoolean(False) 
            self.writeBoolean(False) 
            self.writeBoolean(False)
            self.writeBoolean(False)
            EventIndex += 1

        self.writeVInt(0)
       
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeLong(0, 1) # Player ID

        player.NotificationFactory = playerData['NotificationFactory']

        self.writeVInt(0) # Notification factory
        
        self.writeVInt(1)
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0) 
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(0)

        self.writeBoolean(True) # Starr Road
        
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        if player.UnlockingBrawler != 0:
            self.writeVInt(1) # Unlocking Brawler

            all_brawlers = []
            rare = [1, 2, 3, 6, 8, 10, 13, 24]
            super_rare = [7, 9, 18, 19, 22, 25, 27, 34, 61, 4]
            epic = [14, 15, 16, 20, 26, 29, 30, 36, 39, 43, 44, 45, 46, 49, 48, 50, 51, 53, 58, 65, 68, 69, 77, 79, 82]
            mythic = [11, 17, 21, 35, 31, 32, 37, 41, 42, 47, 54, 55, 57, 59, 60, 62, 64, 66, 67, 71, 72, 73, 74, 75, 78, 81, 83, 84]
            legendary = [5, 12, 23, 28, 38, 40, 52, 63, 70, 76, 80, 85]
            for brawlerID in rare:
                if player.UnlockingBrawler != brawlerID:
                    all_brawlers.append(brawlerID)
            for brawlerID in super_rare:
                if player.UnlockingBrawler != brawlerID:
                    all_brawlers.append(brawlerID)

            x = player.UnlockingBrawler

            if x in rare:
                CreditsNeeded = 160
                GemsNeeded = 29
            if x in super_rare:
                CreditsNeeded = 430
                GemsNeeded = 79
            if x in epic:
                CreditsNeeded = 925
                GemsNeeded = 169
            if x in mythic:
                CreditsNeeded = 1900
                GemsNeeded = 349
            if x in legendary:
                CreditsNeeded = 3800
                GemsNeeded = 699
        
            self.writeDataReference(16, x)
            self.writeVInt(CreditsNeeded) # CreditsNeeded
            self.writeVInt(GemsNeeded) # GemsNeeded
            self.writeVInt(0)
            self.writeVInt(player.RareTokens) # CollectedCredits
            self.writeVInt(0)
            self.writeVInt(0)
        else:
            self.writeVInt(0)

        self.writeVInt(0)
        for i in range(0):  
            self.writeDataReference(16, 80 + i)
            self.writeVInt(1488 + i) # CreditsNeeded
            self.writeVInt(1488 + i) # GemsNeeded
            self.writeVInt(0)
            self.writeVInt(1 + i) # CollectedCredits
            self.writeVInt(0)
            self.writeVInt(0)

        self.writeVInt(0)
        self.writeVInt(0)

        self.writeVInt(len(player.OwnedBrawlers)) # Mastery
        for brawlerID,brawlerData in player.OwnedBrawlers.items():
            self.writeVInt(brawlerData["MasteryPoints"]) #Mastery Points
            self.writeVInt(brawlerData["MasteryClaimed"]) #Claimed Rewards
            self.writeDataReference(16, brawlerID) #brawlers
        #BattleCard
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeVInt(0) #Brawler's BattleCards

        starrDropOpening.encode(self) # StarDrops

        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False) 
        self.writeVInt(0)
        self.writeBoolean(False) 

        # end LogicClientHome

        self.writeVLong(player.ID[0], player.ID[1])
        self.writeVLong(player.ID[0], player.ID[1])
        self.writeVLong(player.ID[0], player.ID[1])
        self.writeStringReference(player.Name)
        self.writeBoolean(player.Registered)
        self.writeInt(-1)

        self.writeVInt(23)
        unlocked_brawler = [i['CardID'] for x,i in player.OwnedBrawlers.items()]
        self.writeVInt(len(unlocked_brawler) + 3)
        for x in unlocked_brawler:
            self.writeDataReference(23, x)
            self.writeVInt(-1)
            self.writeVInt(1)

        self.writeDataReference(5, 8)
        self.writeVInt(-1)
        self.writeVInt(player.Coins)

        self.writeDataReference(5, 21)
        self.writeVInt(-1)
        if player.UnlockingBrawler == 0:
            self.writeVInt(player.RareTokens)
        else:
            self.writeVInt(0)

        self.writeDataReference(5, 23)
        self.writeVInt(-1)
        self.writeVInt(player.Blings)

        self.writeVInt(len(player.OwnedBrawlers)) # HeroScore
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["Trophies"])

        self.writeVInt(len(player.OwnedBrawlers)) # HeroHighScore
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["HighestTrophies"] + 1250)

        self.writeVInt(0) # Array

        self.writeVInt(0) # HeroPower
        
        self.writeVInt(len(player.OwnedBrawlers)) # HeroLevel
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["PowerLevel"]-1)

        self.writeVInt(0) # hero star power gadget and hypercharge

        self.writeVInt(len(player.OwnedBrawlers)) # HeroSeenState
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(2)

        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeVInt(player.Gems) # Diamonds
        self.writeVInt(player.Gems) # Free Diamonds
        self.writeVInt(10) # Player Level
        self.writeVInt(100)
        self.writeVInt(0) # CumulativePurchasedDiamonds or Avatar User Level Tier | 10000 < Level Tier = 3 | 1000 < Level Tier = 2 | 0 < Level Tier = 1
        self.writeVInt(100) # Battle Count
        self.writeVInt(10) # WinCount
        self.writeVInt(80) # LoseCount
        self.writeVInt(50) # WinLooseStreak
        self.writeVInt(20) # NpcWinCount
        self.writeVInt(0) # NpcLoseCount
        self.writeVInt(2) # TutorialState | shouldGoToFirstTutorialBattle = State == 0
        self.writeVInt(12)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeString()
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(1)

    def decode(self):
        fields = {}
        return fields

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24101

    def getMessageVersion(self):
        return self.messageVersion
