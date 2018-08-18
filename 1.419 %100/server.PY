#coding: utf-8
import os, sys, json, time, random, sqlite3, traceback, ConfigParser

# Others
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

# Imports Components
from utils import *
from moduller import *

# Library
from datetime import datetime
from twisted.internet import reactor, protocol
from datetime import timedelta

class Client:
    def __init__(this):

        # String
        this.chatColor = ""
        this.langue = "TR"
        this.packages = ""
        this.roomName = ""
        this.marriage = ""
        this.shopItems = ""
        this.tribeName = ""
        this.nameColor = ""
        this.tradeName = ""
        this.playerName = ""
        this.shamanItems = ""
        this.lastMessage = ""
        this.tribeMessage = ""
        this.tempMouseColor = ""
        this.silenceMessage = ""
        this.currentCaptcha = ""
        this.mouseColor = "78583a"
        this.shamanColor = "95d9d6"
        this.modoPwetLangue = "ALL"
        this.playerLook = "1;0,0,0,0,0,0,0,0,0"
        this.shamanLook = "0,0,0,0,0,0,0,0,0,0"
        this.botVillage = ""
        
        # Integer
        this.pet = 0
        this.posX = 0
        this.posY = 0
        this.velX = 0
        this.velY = 0
        this.gender = 0
        this.petEnd = 0
        this.viewMessage = 0
        this.priceDoneVisu = 0
        this.lastOn = 0
        this.regDate = 0
        this.langueID = 0
        this.playerID = 0
        this.banHours = 0
        this.iceCount = 2
        this.privLevel = 0
        this.nowTokens = 0
        this.nowCoins = 0
        this.shamanExp = 0
        this.tribeCode = 0
        this.tribeRank = 0
        this.tribeChat = 0
        this.titleStars = 0
        this.firstCount = 0
        this.playerCode = 0
        this.shamanType = 0
        this.tribeHouse = 0
        this.tribeJoined = 0
        this.silenceType = 0
        this.playerScore = 0
        this.titleNumber = 0
        this.cheeseCount = 0
        this.shopFraises = 10000
        this.shamanSaves = 0
        this.shamanLevel = 15
        this.lastGameMode = 0
        this.bubblesCount = 0
        this.currentPlace = 0
        this.shamanCheeses = 0
        this.hardModeSaves = 0
        this.bootcampCount = 0
        this.shopCheeses = 10000
        this.shamanExpNext = 32
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.divineModeSaves = 0
        this.lastDivorceTimer = 0
        this.TimeGiro = 0
        this.equipedShamanBadge = 0
        this.playerStartTimeMillis = 0
        this.racingRounds = 0
        this.bootcampRounds = 0
        this.survivorDeath = 0
        this.countTime = 1
        this.countP = 0
        this.cannonX = 2
        this.cannonY = 8
        this.cXpos = 189
        this.cYpos = 133
        this.cnCustom = 0
        this.page = 1
        this.lastPacketID = random.randint(0, 99)
        this.authKey = random.randint(0, 2147483647)
        this.TFMUtils = Utils
        this.tribulleID = 0
        this.artefactID = 0

        # Bool
        this.isAfk = False
        this.isDead = False
        this.isMute = False
        this.isCafe = False
        this.isGuest = False
        this.isVoted = False
        this.isTrade = False
        this.useTotem = False
        this.isHidden = False
        this.isClosed = False
        this.isShaman = False
        this.hasEnter = False
        this.isSuspect = False
        this.isVampire = False
        this.isLuaAdmin = False
        this.hasCheese = False
        this.isJumping = False
        this.resetTotem = False
        this.isModoPwet = False
        this.canRespawn = False
        this.enabledLua = False
        this.isNewPlayer = False
        this.isEnterRoom = False
        this.tradeConfirm = False
        this.canSkipMusic = False
        this.isReloadCafe = False
        this.isMovingLeft = False
        this.isMovingRight = False
        this.isOpportunist = False
        this.qualifiedVoted = False
        this.desintegration = False
        this.canShamanRespawn = False
        this.validatingVersion = False
        this.canRedistributeSkills = False
        this.libCn = False
        this.canCN = False
        this.isFly = False
        this.isSpeed = False
        this.isFFA = False
        this.canSpawnCN = True
        this.isTeleport = False
        this.chatdisabled = False
        this.canKiss = True
        this.openingFriendList = False
        this.isTribeOpen = False
        this.hasArtefact = False

        this.showButtons = True

        # Others
        this.Cursor = Cursor
        this.CMDTime = time.time()
        this.CAPTime = time.time()
        this.CTBTime = time.time()

        # Nonetype
        this.room = None
        this.awakeTimer = None
        this.skipMusicTimer = None
        this.resSkillsTimer = None

        # List
        this.totem = [0, ""]
        this.PInfo = [0, 0, 400]
        this.tempTotem = [0, ""]
        this.racingStats = [0] * 4
        this.survivorStats = [0] * 4
        
        this.chats = []
        this.voteBan = []
        this.clothes = []
        this.titleList = []
        this.shopBadges = []
        this.friendsList = []
        this.tribeInvite = []
        this.shamanBadges = []
        this.ignoredsList = []
        this.mulodromePos = []
        this.shopTitleList = []
        this.marriageInvite = []
        this.firstTitleList = []
        this.cheeseTitleList = []
        this.shamanTitleList = []
        this.specialTitleList = []
        this.bootcampTitleList = []
        this.hardModeTitleList = []
        this.equipedConsumables = []
        this.ignoredTribeInvites = []
        this.divineModeTitleList = []
        this.ignoredMarriageInvites = []
        this.custom = []
        this.visuDone = []

        # Dict
        this.tribeRanks = ""
        this.playerSkills = {}
        this.tradeConsumables = {}
        this.playerConsumables = {}
        this.itensBots = {"Papaille": [(1, 184, 1, 4, 2103, 50), (1, 181, 1, 4, 2103, 50), (1, 69, 1, 4, 2103, 50), (1, 71, 1, 4, 2103, 50), (1, 73, 1, 4, 2103, 50), (1, 129, 1, 4, 2103, 50), (1, 130, 1, 4, 2103, 50), (1, 131, 1, 4, 2103, 50), (1, 132, 1, 4, 2103, 50), (1, 133, 1, 4, 2103, 50), (1, 134, 1, 4, 2103, 50), (1, 139, 1, 4, 2103, 50), (1, 142, 1, 4, 2103, 50), (1, 144, 1, 4, 2103, 50), (1, 158, 1, 4, 2103, 50), (1, 161, 1, 4, 2103, 50), (1, 162, 1, 4, 2103, 50), (1, 169, 1, 4, 2103, 50), (1, 170, 1, 4, 2103, 50), (1, 174, 1, 4, 2103, 50), (1, 46, 1, 4, 2103, 50), (1, 47, 1, 4, 2103, 50), (1, 50, 1, 4, 2103, 50), (1, 51, 1, 4, 2103, 50), (1, 57, 1, 4, 2103, 50), (1, 58, 1, 4, 2103, 50), (1, 59, 1, 4, 2103, 50), (1, 64, 1, 4, 2103, 50), (1, 65, 1, 4, 2103, 50), (1, 0, 1, 4, 2103, 50), (1, 1, 1, 4, 2103, 50), (1, 6, 1, 4, 2103, 50), (1, 7, 1, 4, 2103, 50), (1, 16, 1, 4, 2103, 50), (1, 17, 1, 4, 2103, 50), (1, 18, 1, 4, 2103, 50), (1, 28, 1, 4, 2103, 50), (1, 29, 1, 4, 2103, 50), (1, 30, 1, 4, 2254, 50), (1, 33, 1, 4, 2103, 50), (1, 34, 1, 4, 2103, 50), (1, 35, 1, 4, 2103, 50), (1, 9, 1, 4, 2103, 50), (1, 42, 1, 4, 2103, 50), (1, 54, 1, 4, 2103, 50), (1, 55, 1, 4, 2103, 50)], "Buffy": [(1, 147, 1, 4, 2103, 200), (3, 398, 1, 4, 2103, 150), (3, 392, 1, 4, 2103, 50)], "Indiana Mouse": [(2, 1, 1, 4, 2103, 150), (2, 2, 1, 4, 2103, 150), (2, 3, 1, 4, 2103, 150), (2, 4, 1, 4, 2103, 150), (2, 5, 1, 4, 2103, 150), (2, 6, 1, 4, 2103, 150), (2, 7, 1, 4, 2103, 150), (2, 8, 1, 4, 2103, 150), (2, 9, 1, 4, 2103, 150), (2, 10, 1, 4, 2103, 150), (2, 11, 1, 4, 2103, 150), (2, 12, 1, 4, 2103, 150), (2, 13, 1, 4, 2103, 150), (2, 14, 1, 4, 2103, 150), (2, 15, 1, 4, 2103, 150), (2, 16, 1, 4, 2103, 150), (2, 17, 1, 4, 2103, 150), (2, 18, 1, 4, 2103, 150), (2, 19, 1, 4, 2103, 150), (2, 20, 1, 4, 2103, 150), (2, 21, 1, 4, 2103, 150), (2, 22, 1, 4, 2103, 150), (2, 23, 1, 4, 2103, 150), (2, 24, 1, 4, 2103, 150), (2, 25, 1, 4, 2103, 150), (2, 26, 1, 4, 2103, 150), (2, 27, 1, 4, 2103, 150), (2, 28, 1, 4, 2103, 150)], "Elise": [(3, 255, 1, 4, 2103, 50), (3, 394, 1, 4, 2103, 50), (3, 395, 1, 4, 2103, 50), (3, 320, 1, 4, 2103, 50), (3, 393, 1, 4, 2103, 50), (3, 402, 1, 4, 2103, 50), (3, 397, 1, 4, 2103, 50), (3, 341, 1, 4, 2103, 50), (3, 335, 1, 4, 2103, 25), (3, 403, 1, 4, 2103, 50)], "Oracle": [(1, 145, 1, 4, 2253, 200), (3, 390, 1, 4, 2253, 50), (3, 391, 1, 4, 2253, 200), (3, 399, 1, 4, 2253, 150)], "Prof": [(4, 2247, 5, 4, 2103, 5), (4, 2262, 5, 4, 2103, 5), (4, 31, 5, 4, 2103, 5), (4, 1, 20, 4, 2103, 10), (4, 5, 20, 4, 2103, 10), (4, 6, 20, 4, 2103, 10), (4, 8, 20, 4, 2103, 10), (4, 25, 20, 4, 2103, 10), (4, 26, 20, 4, 2103, 10), (4, 10, 20, 4, 2103, 10), (4, 11, 20, 4, 2103, 10), (4, 15, 20, 4, 2103, 10), (4, 24, 20, 4, 2103, 10), (4, 28, 20, 4, 2103, 10), (4, 29, 20, 4, 2103, 10), (4, 30, 20, 4, 2103, 10), (4, 2241, 20, 4, 2103, 10), (4, 2330, 20, 4, 2103, 10), (4, 33, 20, 4, 2103, 10), (4, 2234, 20, 4, 2103, 10), (4, 2246, 20, 4, 2103, 10), (4, 2232, 20, 4, 2103, 10), (4, 14, 20, 4, 2103, 10)], "Cassidy": [(1, 154, 1, 4, 2261, 200), (3, 400, 1, 4, 2261, 100)], "Von Drekkemouse": [(1, 153, 1, 4, 2260, 200), (3, 401, 1, 4, 2260, 100)], "Tod": [(4, 2259, 10, 4, 2103, 1), (4, 2258, 10, 4, 2103, 230), (3, 401, 1, 4, 2260, 100)], "Fishing 2017": [(1, 184, 1, 4, 2254, 200), (2, 24, 1, 4, 2254, 150), (3, 422, 1, 4, 2103, 200)], "Loading": [(1, 131, 130, 000, 147, 1, 4, 2103, 200), (3, 422, 1, 4, 2103, 200)], "Jeenklynn": [(1, 181, 1, 4, 2254, 200), (3, 374, 1, 4, 2254, 200)]}
        this.aventureCounts = {}
        this.aventurePoints = {}
        this.visusRemove = []

    def dataReceived(this, packet):
        if packet.startswith("<policy-file-request/>"):
            this.transport.write("<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>")
            this.transport.loseConnection()
        else:
            this.packages += packet
            while this.packages.strip(chr(0)):
                if len(this.packages) >= 5:
                    sizeBytes, package, length = 0, "", 0
                    p = ByteArray(this.packages)
                    sizeBytes = p.readByte()
                    if sizeBytes == 1:
                        length = p.readUnsignedByte()
                    elif sizeBytes == 2:
                        length = p.readUnsignedShort()
                    elif sizeBytes == 3:
                        length = ((p.readUnsignedByte() & 0xFF) << 16) | ((p.readUnsignedByte() & 0xFF) << 8) | (p.readUnsignedByte() & 0xFF) 
                    else:
                        this.packages = ""
                    if (length >= 1 and p.getLength() >= 3):
                        length += 1
                        if length == p.getLength():
                            package = p.toByteArray()
                            this.packages = ""
                        elif length > p.getLength():
                            break
                        else:
                            package = p.toByteArray()[:length]
                            this.packages = p.toByteArray()[length:]
                    else:
                        this.packages = ""
                    if package:
                        if len(package) >= 3:
                            this.parseString(ByteArray(package))
                    p
                else:
                    this.packages = ""

    def sendAddPopupText(this, id, x, y, l, a, fur1, fur2, opcit, Message):
        bg = int(fur1, 16)
        bd = int(fur2, 16)
        data = struct.pack("!i", id)
        data = data + struct.pack("!h", len(Message))
        data = data + Message + struct.pack("!hhhhiibb", int(x), int(y), int(l), int(a), int(bg), int(bd), int(opcit), 0)
        this.sendPacket([29, 20], data)

    def makeConnection(this, transport):
        this.transport = transport
        this.server = this.factory
        this.ipAddress = this.transport.getPeer().host

        this.cafe = Cafe(this, this.server)
        this.modoPwet = ModoPwet(this, this.server)
        this.tribulle = Tribulle(this, this.server)
        this.parseShop = ParseShop(this, this.server)
        this.parseSkill = ParseSkill(this, this.server)
        this.parsePackets = ParsePackets(this, this.server)
        this.parseCommands = ParseCommands(this, this.server)
        this.ranking = ranking(this, this.server)
        this.roleta = roleta(this, this.server)
        this.equipe = equipe(this, this.server)
        this.shop = shop(this, this.server)
        this.consumablesShop = consumablesShop(this, this.server)
        this.Utility = Utility(this, this.server)
        
        if this.server.connectedCounts.has_key(this.ipAddress):
            this.server.connectedCounts[this.ipAddress] += 1
        else:
            this.server.connectedCounts[this.ipAddress] = 1

        if this.server.connectedCounts[this.ipAddress] >= 5 or this.ipAddress in this.server.IPPermaBanCache or this.ipAddress in this.server.IPTempBanCache:
            this.transport.loseConnection()

    def connectionLost(this, args):
        this.isClosed = True
        if this.server.connectedCounts.has_key(this.ipAddress):
            count = this.server.connectedCounts[this.ipAddress] - 1
            if count <= 0:
                del this.server.connectedCounts[this.ipAddress]
            else:
                this.server.connectedCounts[this.ipAddress] = count

        if this.server.players.has_key(this.playerName):
            del this.server.players[this.playerName]
                
            if this.isTrade:
                this.cancelTrade(this.tradeName)

            if this.playerName in this.server.reports["names"]:
                if not this.server.reports[this.playerName]["status"] == "banned":
                    this.server.reports[this.playerName]["status"] = "disconnected"
                    this.modoPwet.updateModoPwet()

            if this.server.chatMessages.has_key(this.playerName):
                this.server.chatMessages[this.playerName] = {}
                del this.server.chatMessages[this.playerName]

            for player in this.server.players.values():
                if this.playerName and player.playerName in this.friendsList and player.friendsList:
                    player.tribulle.sendFriendDisconnected(this.playerName)

            if this.tribeCode != 0:
                this.tribulle.sendTribeMemberDisconnected()

				
            this.updateDatabase()

        if this.room != None:
            this.room.removeClient(this)

    def sendPacket(this, identifiers, packet=""):
        if this.isClosed:
            return

        p = ByteArray().writeBytes(("".join(map(chr, identifiers)) + chr(packet)) if type(packet) == int else "".join(map(chr, identifiers)) + packet) if type(packet) != list else ByteArray().writeBytes(chr(1) + chr(1)).writeUTF(chr(1).join(map(str, ["".join(map(chr, identifiers))] + packet)))
        this.transport.write((ByteArray().writeByte(1).writeUnsignedByte(p.getLength()) if p.getLength() <= 0xFF else ByteArray().writeByte(2).writeUnsignedShort(p.getLength()) if p.getLength() <= 0xFFFF else ByteArray().writeByte(3).writeUnsignedByte((p.getLength() >> 16) & 0xFF).writeUnsignedByte((p.getLength() >> 8) & 0xFF).writeUnsignedByte(p.getLength() & 0xFF) if p.getLength() <= 0xFFFFFF else 0).writeBytes(p.toByteArray()).toByteArray())
        this.transport.setTcpKeepAlive(1)
        this.transport.setTcpNoDelay(True)

    def parseString(this, packet):
        if this.isClosed:
            return

        if packet in ["", " ", "\x00", "\x01"]:
            this.server.IPTempBanCache.append(this.ipAddress)
            this.transport.loseConnection()
            this.breakLoop()
             
        packetID, C, CC = packet.readByte(), packet.readByte(), packet.readByte()        
        if not this.validatingVersion:
            if (C == Identifiers.recv.Informations.C and CC == Identifiers.recv.Informations.Correct_Version) and not (this.isClosed):
                version = packet.readShort()
                ckey = packet.readUTF()

                if not ckey == this.server.CKEY and version != this.server.Version:
                    print "[%s] [WARN] Invalid version or CKey (%s, %s)" %(time.strftime("%H:%M:%S"), version, ckey)
                    this.transport.loseConnection()
                else:
                    this.validatingVersion = True
                    this.sendCorrectVersion()
            else:
                this.transport.loseConnection()
        else:
            try:
                this.lastPacketID = (this.lastPacketID + 1) % 100
                this.lastPacketID = packetID
                this.parsePackets.parsePacket(packetID, C, CC, packet)
            except:
                with open("./moduller/config/SErros.log", "a") as f:
                    traceback.print_exc(file=f)
                    f.write("\n")

    def loginPlayer(this, playerName, password, startRoom):
        playerName = "Souris" if playerName == "" else playerName
        if password == "":
            playerName = this.server.checkAlreadyExistingGuest("*" + (playerName[0].isdigit() or len(playerName) > 12 or len(playerName) < 3 or "Souris" if "+" in playerName else playerName))
            startRoom = "\x03[Tutorial] %s" %(playerName)
            this.isGuest = True

        if not this.isGuest and playerName in this.server.userPermaBanCache:
            this.sendPacket(Identifiers.old.send.Player_Ban_Login, [this.server.getPermBanInfo(playerName)])
            this.transport.loseConnection()
            return

        if not this.isGuest:
            banInfo = this.server.getTempBanInfo(playerName)
            timeCalc = Utils.getHoursDiff(banInfo[1])
            if timeCalc <= 0:
                this.server.removeTempBan(playerName)
            else:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [timeCalc, banInfo[0]])
                this.transport.loseConnection()
                return

        if this.server.checkConnectedAccount(playerName):
            this.sendPacket(Identifiers.send.Login_Result, 1)
        else:
            gifts, messages = "", ""
            if not this.isGuest and not playerName == "":
                Cursor.execute("select * from Users where Username = ? and Password = ?", [playerName, password])
                rs = Cursor.fetchone()
                if rs:
                    this.playerID = rs["PlayerID"]
                    this.privLevel = rs["PrivLevel"]
                    this.titleNumber = rs["TitleNumber"]
                    this.firstCount = rs["FirstCount"]
                    this.cheeseCount = rs["CheeseCount"]
                    this.shamanCheeses = rs["ShamanCheeses"]
                    this.shopCheeses = rs["ShopCheeses"]
                    this.shopFraises = rs["ShopFraises"]
                    this.shamanSaves = rs["ShamanSaves"]
                    this.hardModeSaves = rs["HardModeSaves"]
                    this.divineModeSaves = rs["DivineModeSaves"]
                    this.bootcampCount = rs["BootcampCount"]
                    this.shamanType = rs["ShamanType"]
                    this.shopItems = rs["ShopItems"]
                    this.shamanItems = rs["ShamanItems"]
                    this.clothes = map(str, filter(None, rs["Clothes"].split("|")))
                    this.playerLook = rs["Look"]
                    this.shamanLook = rs["ShamanLook"]
                    this.mouseColor = rs["MouseColor"]
                    this.shamanColor = rs["ShamanColor"]
                    this.regDate = rs["RegDate"]
                    this.shopBadges = map(str, filter(None, rs["Badges"].split(",")))
                    this.cheeseTitleList = map(float, filter(None, rs["CheeseTitleList"].split(",")))
                    this.firstTitleList = map(float, filter(None, rs["FirstTitleList"].split(",")))
                    this.shamanTitleList = map(float, filter(None, rs["ShamanTitleList"].split(",")))
                    this.shopTitleList = map(float, filter(None, rs["ShopTitleList"].split(",")))
                    this.bootcampTitleList = map(float, filter(None, rs["BootcampTitleList"].split(",")))
                    this.hardModeTitleList = map(float, filter(None, rs["HardModeTitleList"].split(",")))
                    this.divineModeTitleList = map(float, filter(None, rs["DivineModeTitleList"].split(",")))
                    this.specialTitleList = map(float, filter(None, rs["SpecialTitleList"].split(",")))
                    this.banHours = rs["BanHours"]
                    this.shamanLevel = rs["ShamanLevel"]
                    this.shamanExp = rs["ShamanExp"]
                    this.shamanExpNext = rs["ShamanExpNext"]

                    for skill in map(str, filter(None, rs["Skills"].split(";"))):
                        values = skill.split(":")
                        this.playerSkills[int(values[0])] = int(values[1])

                    this.lastOn = rs["LastOn"]
                    this.friendsList = rs["FriendsList"].split(",")
                    this.ignoredsList = rs["IgnoredsList"].split(",")
                    this.gender = rs["Gender"]
                    this.lastDivorceTimer = rs["LastDivorceTimer"]
                    this.marriage = rs["Marriage"]
                    this.tribeCode = rs["TribeCode"]
                    this.tribeRank = rs["TribeRank"]
                    this.tribeJoined = rs["TribeJoined"]
                    gifts = rs["Gifts"]
                    message = rs["Messages"]
                    this.visuDone = rs["VisuDone"].split("|")
                    this.custom = map(str, filter(None, rs["CustomItems"].split(",")))
                    this.survivorStats = map(int, rs["SurvivorStats"].split(","))
                    this.racingStats = map(int, rs["RacingStats"].split(","))
                    
                    for consumable in map(str, filter(None, rs["Consumables"].split(";"))):
                        values = consumable.split(":")
                        this.playerConsumables[int(values[0])] = int(values[1])

                    this.equipedConsumables = []
                    this.pet = rs["Pet"]
                    this.petEnd = 0 if this.pet == 0 else Utils.getTime() + rs["PetEnd"]
                    this.shamanBadges = map(int, filter(None, rs["ShamanBadges"].split(",")))
                    this.equipedShamanBadge = rs["EquipedShamanBadge"]
                    this.totem = [rs["TotemItemCount"], rs["Totem"].replace("%"[0], chr(1))]
                    this.nowCoins = rs["Coins"]
                    this.nowTokens = rs["Tokens"]
                    this.deathStats = map(int, rs["DeathStats"].split(","))
                    vipTime = rs["VipTime"]
                    this.langueStaff = rs["Langue"]
                    this.votemayor, this.candidatar, this.isMayor, this.isPresidente, this.votepresidente, this.addpresidente=map(int, rs["Mayor"].split("#"))
                    for counts in map(str, filter(None, rs["AventureCounts"].split(";"))):
                        values = counts.split(":")
                        f = []
                        aux = 0
                        for i in xrange(len(values[1])):
                            try:
                                aux = aux * 10 + int(values[1][i])
                            except:
                                if aux > 0:
                                    f.append(aux)
                                aux = 0
                                pass
                        this.aventureCounts[int(values[0])] = int(f[0]), int(f[1])
                    #this.aventureCounts = eval(rs["AventureCounts"])
                    for points in map(str, filter(None, rs["AventurePoints"].split(";"))):
                        values = points.split(":")
                        this.aventurePoints[int(values[0])] = int(values[1])
                    this.aventureSaves = rs["SavesAventure"]
                else:
                    reactor.callLater(5, lambda: this.sendPacket(Identifiers.send.Login_Result, 2))
                    return

            if this.privLevel == -1:
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, ["Blocked account."])
                this.transport.loseConnection()
                return

            this.server.lastPlayerCode += 1
            this.playerName = playerName
            this.playerCode = this.server.lastPlayerCode

            Cursor.execute("insert into loginlog (Username, IP) select ?, ? where not exists (select 1 from loginlog where Username = ? and IP = ?)", [playerName, this.ipAddress, playerName, this.ipAddress])

            for name in ["cheese", "first", "shaman", "shop", "bootcamp", "hardmode", "divinemode"]:
                this.checkAndRebuildTitleList(name)

            this.sendCompleteTitleList()
            this.parseShop.checkAndRebuildBadges()
            
            for title in this.titleList:
                if str(title).split(".")[0] == str(this.titleNumber):
                    this.titleStars = int(str(title).split(".")[1])
                    break

            this.isMute = playerName in this.server.userMuteCache
            this.server.players[this.playerName] = this

            this.sendLogin()
            this.parseShop.sendShamanItems()
            this.sendPacket([60, 4], chr(1))
            this.parseSkill.sendShamanSkills(False)
            this.parseSkill.sendExp(this.shamanLevel, this.shamanExp, this.shamanExpNext)
            if this.shamanSaves >= 0:
                this.sendShamanType(this.shamanType, (this.shamanSaves >= 0 and this.hardModeSaves >= 0))

            this.server.checkPromotionsEnd()
            this.sendTimeStamp()
            this.sendPromotions()


            if this.privLevel >= 1:
                this.sendLogMessage
            if this.privLevel >= 7:
                this.sendMessage("<font color='#3DBAFF'> /yardım yazarak özel komutlarınızı görebilirsiniz Sürüm 1.419</font>""", True)

            if this.tribeCode != 0:
                tribeInfo = this.tribulle.getTribeInfo(this.tribeCode)
                this.tribeName = tribeInfo[0]
                this.tribeMessage = tribeInfo[1]
                this.tribeHouse = tribeInfo[2]
                this.tribeRanks = tribeInfo[3]
                this.tribeChat = tribeInfo[4]

            if this.privLevel in [2,3,4]:
                this.checkVip(vipTime)

            #this.tribulle.sendTribe(False)
            #this.tribulle.sendPlayerInfo()
            #this.tribulle.sendIgnoredsList()
            this.tribulle.sendFriendsList(None)

            for player in this.server.players.values():
                if this.playerName and player.playerName in this.friendsList and player.friendsList:
                    player.tribulle.sendFriendConnected(this.playerName)

            if this.tribeCode != 0:
                this.tribulle.sendTribeMemberConnected()
				

            this.sendInventoryConsumables()
            this.parseShop.checkGiftsAndMessages(gifts, messages)
            this.resSkillsTimer = reactor.callLater(600, setattr, this, "canRedistributeSkills", True)
            this.startBulle(this.server.checkRoom(startRoom, this.langue) if not startRoom == "" and not startRoom == "1" else this.server.recommendRoom(this.langue))
            this.langueStaff = this.langue
    		
    def checkAndRebuildTitleList(this, type):
        titlesLists = [this.cheeseTitleList, this.firstTitleList, this.shamanTitleList, this.shopTitleList, this.bootcampTitleList, this.hardModeTitleList, this.divineModeTitleList]
        titles = [this.server.cheeseTitleList, this.server.firstTitleList, this.server.shamanTitleList, this.server.shopTitleList, this.server.bootcampTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
        typeID = 0 if type == "cheese" else 1 if type == "first" else 2 if type == "shaman" else 3 if type == "shop" else 4 if type == "bootcamp" else 5 if type == "hardmode" else 6 if type == "divinemode" else 0
        count = this.cheeseCount if type == "cheese" else this.firstCount if type == "first" else this.shamanSaves if type == "shaman" else this.parseShop.getShopLength() if type == "shop" else this.bootcampCount if type == "bootcamp" else this.hardModeSaves if type == "hardmode" else this.divineModeSaves if type == "divinemode" else 0
        tempCount = count
        rebuild = False
        while tempCount > 0:
            if titles[typeID].has_key(tempCount):
                if not titles[typeID][tempCount] in titlesLists[typeID]:
                    rebuild = True
                    break
            tempCount -= 1

        if rebuild:
            titlesLists[typeID] = []
            x = 0
            while x <= count:
                if titles[typeID].has_key(x):
                    title = titles[typeID][x]                    
                    i = 0
                    while i < len(titlesLists[typeID]):
                        if str(titlesLists[typeID][i]).startswith(str(title).split(".")[0]):
                            del titlesLists[typeID][i]
                        i += 1                        
                    titlesLists[typeID].append(title)
                x += 1
                
        this.cheeseTitleList = titlesLists[0]
        this.firstTitleList = titlesLists[1]
        this.shamanTitleList = titlesLists[2]
        this.shopTitleList = titlesLists[3]
        this.bootcampTitleList = titlesLists[4]
        this.hardModeTitleList = titlesLists[5]
        this.divineModeTitleList = titlesLists[6]

    def getConnectedPlayerCount(this):
        return len(this.server.players)

    def updateDatabase(this):
        if not this.isGuest:
            Cursor.execute("select VipInfos from users where Username = ?", [this.playerName])
            rrf = Cursor.fetchone()[0]
            if not rrf == '':
                vipInfos = eval(rrf)
                vipPriv = vipInfos[0]
                vipShopCheese = vipInfos[1]
                vipFraises = vipInfos[1]
                vipCoins = vipInfos[2]
                vipTokens = vipInfos[3]
                vipCheeses = vipInfos[4]
                vipFirst = vipInfos[4]

                this.privLevel = vipPriv
                this.shopCheeses += vipShopCheese
                this.shopFraises += vipFraises
                this.nowCoins += vipCoins
                this.nowTokens += vipTokens
                this.cheeseCount += vipCheeses
                this.firstCount += vipFirst

                Cursor.execute("update users set VipInfos = ? where Username", ['', this.playerName])
                
            Cursor.execute("update Users set PrivLevel = ?, TitleNumber = ?, FirstCount = ?, CheeseCount = ?, ShamanCheeses = ?, ShopCheeses = ?, ShopFraises = ?, ShamanSaves = ?, HardModeSaves = ?, DivineModeSaves = ?, BootcampCount = ?, ShamanType = ?, ShopItems = ?, ShamanItems = ?, Clothes = ?, Look = ?, ShamanLook = ?, MouseColor = ?, ShamanColor = ?, RegDate = ?, Badges = ?, CheeseTitleList = ?, FirstTitleList = ?, ShamanTitleList = ?, ShopTitleList = ?, BootcampTitleList = ?, HardModeTitleList = ?, DivineModeTitleList = ?, SpecialTitleList = ?, BanHours = ?, ShamanLevel = ?, ShamanExp = ?, ShamanExpNext = ?, Skills = ?, LastOn = ?, FriendsList = ?, IgnoredsList = ?, Gender = ?, LastDivorceTimer = ?, Marriage = ?, TribeCode = ?, TribeRank = ?, TribeJoined = ?, SurvivorStats = ?, RacingStats = ?, Consumables = ?, EquipedConsumables = ?, Pet = ?, PetEnd = ?, ShamanBadges = ?, EquipedShamanBadge = ?, VisuDone = ?, CustomItems = ?, Coins = ?, Tokens = ?, DeathStats = ?, Langue = ?, Mayor = ?, AventureCounts = ?, AventurePoints = ?, SavesAventure = ? where Username = ?", [this.privLevel, this.titleNumber, this.firstCount, this.cheeseCount, this.shamanCheeses, this.shopCheeses, this.shopFraises, this.shamanSaves, this.hardModeSaves, this.divineModeSaves, this.bootcampCount, this.shamanType, this.shopItems, this.shamanItems, "|".join(map(str, this.clothes)), this.playerLook, this.shamanLook, this.mouseColor, this.shamanColor, this.regDate, ",".join(map(str, this.shopBadges)), ",".join(map(str, this.cheeseTitleList)), ",".join(map(str, this.firstTitleList)), ",".join(map(str, this.shamanTitleList)), ",".join(map(str, this.shopTitleList)), ",".join(map(str, this.bootcampTitleList)), ",".join(map(str, this.hardModeTitleList)), ",".join(map(str, this.divineModeTitleList)), ",".join(map(str, this.specialTitleList)), this.banHours, this.shamanLevel, this.shamanExp, this.shamanExpNext, ";".join(map(lambda skill: "%s:%s" %(skill[0], skill[1]), this.playerSkills.items())), this.tribulle.getTime(), ",".join(map(str, filter(None, this.friendsList))), ",".join(map(str, filter(None, this.ignoredsList))), this.gender, this.lastDivorceTimer, this.marriage, this.tribeCode, this.tribeRank, this.tribeJoined, ",".join(map(str, this.survivorStats)), ",".join(map(str, this.racingStats)), ";".join(map(lambda consumable: "%s:%s" %(consumable[0], 250 if consumable[1] > 250 else consumable[1]), this.playerConsumables.items())), ",".join(map(str, this.equipedConsumables)), this.pet, abs(Utils.getSecondsDiff(this.petEnd)), ",".join(map(str, this.shamanBadges)), this.equipedShamanBadge, "|".join(map(str, this.visuDone)), ",".join(map(str, this.custom)), this.nowCoins, this.nowTokens, ",".join(map(str, this.deathStats)), this.langueStaff, "#".join([str(this.votemayor), str(this.candidatar), str(this.isMayor), str(this.isPresidente), str(this.votepresidente), str(this.addpresidente)]), ";".join(map(lambda aventure: "%s:%s" %(aventure[0], aventure[1]), this.aventureCounts.items())), ";".join(map(lambda points: "%s:%s" %(points[0], points[1]), this.aventurePoints.items())), this.aventureSaves, this.playerName])

    def startBulle(this, roomName):
        if not this.isEnterRoom:
            this.isEnterRoom = True
            reactor.callLater(0.4, this.sendBulle)
            reactor.callLater(0.8, lambda: this.enterRoom(roomName))
            reactor.callLater(6, setattr, this, "isEnterRoom", False)

    def enterRoom(this, roomName):
        this.updateDatabase()
        
        if this.isTrade:
            this.cancelTrade(this.tradeName)

        roomName = roomName.replace("<", "&lt;")
        if not roomName.startswith("*") and not (len(roomName) > 3 and roomName[2] == "-" and this.privLevel >= 7):
            roomName = "%s-%s" %(this.langue, roomName)
            
        for rooms in ["\x03[Editeur] ", "\x03[Totem] ", "\x03[Tutorial] "]:
            if roomName.startswith(rooms) and not this.playerName == roomName.split(" ")[1]:
                roomName = "%s-%s" %(this.langue, this.playerName)

        nomSalon = ["#utility0%s" % (this.playerName or this.tribeName), "#utility00%s" % (this.playerName or this.tribeName)]
        if roomName == nomSalon[0] or nomSalon[1]:
            if re.search(this.playerName, roomName):
                reactor.callLater(0.1, this.Utility.moreSettings, "giveAdmin")
            else:
                try:
                    if not this.tribeName == '':
                        if re.search(this.tribeName, roomName):
                            reactor.callLater(0.1, this.Utility.moreSettings, "giveAdmin")
                except:
                    pass

        if re.search("#utility", roomName):
            reactor.callLater(0.1, this.Utility.moreSettings, "join")
            reactor.callLater(1.5, this.Utility.moreSettings, "removePopups")

        if this.room != None:
            this.room.removeClient(this)

        this.roomName = roomName
        this.sendGameType(11 if "music" in roomName else 4, 0)
        this.sendEnterRoom(roomName)
        this.server.addClientToRoom(this, roomName)
        this.sendPacket(Identifiers.old.send.Anchors, this.room.anchors)
        this.sendPacket([29, 1], "")

        for player in this.server.players.values():
            if this.playerName and player.playerName in this.friendsList and player.friendsList:
                player.tribulle.sendFriendChangedRoom(this.playerName, this.langueID)

        if this.tribeCode != 0:
            this.tribulle.sendTribeMemberChangeRoom()

        if this.room.isMusic and this.room.isPlayingMusic:
            this.sendMusicVideo(False)

        #if not this.room.isTotemEditor and not this.room.isEditor and not this.room.isRacing and not this.room.isBootcamp and not this.room.isSurvivor and not this.room.isVillage and not this.room.isDefilante:

        if roomName.startswith(this.langue + "-" + "music") or roomName.startswith(this.langue + "-" + "*music"):
            this.canSkipMusic = False
            if this.skipMusicTimer != None:
                this.skipMusicTimer.cancel()
            this.skipMusicTimer = reactor.callLater(15, setattr, this, "canSkipMusic", True)

        if this.room.isDeathmatch:
            this.room.bindKeyBoard(this.playerName, 3, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 32, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 79, False, this.room.isDeathmatch)
            this.room.bindKeyBoard(this.playerName, 80, False, this.room.isDeathmatch)
            this.sendMessage("<CH><ROSE>#deathmatch <CH>modülüne hoşgeldin.", True)
            this.sendMessage("<V><ROSE>AŞAĞI OK <V>veya <ROSE>BOŞLUK <V>tuşuna basarak gülle atabilirsin.", True)
            this.sendMessage("<V><ROSE>P<V> tuşuna basarak profiline, <ROSE>O <V>tuşuna basarak envanterine bakabilirsin.", True)


    def resetPlay(this):
        this.iceCount = 2
        this.bubblesCount = 0
        this.currentPlace = 0
        this.ambulanceCount = 0
        this.defilantePoints = 0
        this.bootcampRounds = 0
        this.artefactID = 0
        
        this.isAfk = True
        this.isDead = False
        this.useTotem = False
        this.hasEnter = False
        this.isShaman = False
        this.isVampire = False
        this.hasCheese = False
        this.isSuspect = False
        this.canRespawn = False
        this.isNewPlayer = False
        this.isOpportunist = False
        this.desintegration = False
        this.canShamanRespawn = False
        this.canKiss = True
        this.hasArtefact = False

        this.a = []
        this.i = []
        this.s = []
        
    def sendAccountTime(this):
        eventTime = 1
        date = datetime.now() + timedelta(hours=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        this.Cursor.execute('select IP from Account where IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
           this.Cursor.execute('insert into Account values (?, ?)', [this.ipAddress, eventTime_])
        else:
           this.Cursor.execute('update Account set Time = ? where IP = ?', [eventTime_, this.ipAddress])
        
    def checkTimeAccount(this):
        this.Cursor.execute('SELECT Time FROM Account WHERE IP = ?', [this.ipAddress])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            return True
        else:
            if (int(str(thetime.time()).split(".")[0]) >= int(rrf[0])):
                return True
            else:
                return False

    def startFrogEvent(this):
        this.sendPacket([5, 51], "\t\x00,\x07\x00i\x07\xb2")
        this.sendPacket([5, 51], "\t\x00-\x07\x00\xc3\x07\xb2")
        this.sendPacket([5, 51], "\t\x00.\x07\x00\xcd\x07\xb2")
        this.sendPacket([5, 51], "\t\x00/\x08\x011\x07\xb2")
        this.sendPacket([5, 51], "\t\x000\x08\x01\x8b\x07\xb2")
        this.sendPacket([5, 51], "\t\x001\x08\x01\x90\x07\xc1")
        this.sendPacket([5, 51], "\t\x002\x08\x01\x95\x07\xb2")
        this.sendPacket([5, 51], "\t\x003\x08\x01\xf9\x07\xb2")
        this.sendPacket([5, 51], "\t\x004\x07\x02S\x07\xb2")
        this.sendPacket([5, 51], "\t\x005\x07\x02]\x07\xb2")
        this.sendPacket([5, 51], "\t\x006\x07\x02\xc1\x07\xb2")
        reactor.callLater(13, this.travarRatos)

    def travarRatos(this):
        this.room.sendAll([100, 66], "\x01")

    def sendTimeEvent(this):
        #times = 1
        time = range(40, 61)
        eventTime = random.choice(time)
        date = datetime.now() + timedelta(minutes=int(eventTime))
        timetuple = date.timetuple()
        eventTime_ = int(str(thetime.mktime(timetuple)).split(".")[0])
        this.server.timeEvent = eventTime_
        this.server.updateConfig()

    def StartEvent(this):
        if (int(str(thetime.time()).split(".")[0]) >= this.server.timeEvent):
            for room in this.server.rooms.values():
                if not room.isDefilante and not room.isSurvivor and not room.isTutorial and not room.isTotemEditor and not room.isTribeHouse and not room.isMulodrome and not room.isMusic and not room.isEditor and not room.isBootcamp and not room.isDeathmatch:
                    for playerCode, client in room.clients.items():
                        d = ["@800"]
                        client.room.forceNextMap = random.choice(d)
                        this.sendTimeEvent()
        else:
            pass

    def startPlay(this):
        #this.StartEvent()
        this.playerStartTimeMillis = this.room.gameStartTimeMillis
        this.isNewPlayer = this.isDead
        this.sendMap(newMapCustom=True) if this.room.mapCode != -1 else this.sendMap() if this.room.isEditor and this.room.EMapCode != 0 else this.sendMap(True)

        shamanCode, shamanCode2 = 0, 0
        if this.room.isDoubleMap:
            shamans = this.room.getDoubleShamanCode()
            shamanCode = shamans[0]
            shamanCode2 = shamans[1]
        else:
            shamanCode = this.room.getShamanCode()

        if this.playerCode == shamanCode or this.playerCode == shamanCode2:
            this.isShaman = True

        if this.isShaman and not this.room.noShamanSkills:
            this.parseSkill.getkills()

        if this.room.currentShamanName != "" and not this.room.noShamanSkills:
            this.parseSkill.getPlayerSkills(this.room.currentShamanSkills)

        if this.room.currentSecondShamanName != "" and not this.room.noShamanSkills:
            this.parseSkill.getPlayerSkills(this.room.currentSecondShamanSkills)

        this.sendPlayerList()
        if this.room.catchTheCheeseMap and not this.room.noShamanSkills:
            this.sendPacket(Identifiers.old.send.Catch_The_Cheese_Map, [shamanCode])
            this.sendPacket(Identifiers.old.send.Player_Get_Cheese, [shamanCode])
            if not this.room.currentMap in [108, 109]:
                this.sendShamanCode(shamanCode, shamanCode2)
        else:
            this.sendShamanCode(shamanCode, shamanCode2)

        this.sendSync(this.room.getSyncCode())
        this.sendRoundTime(this.room.roundTime + (this.room.gameStartTime - Utils.getTime()) + this.room.addTime)
        this.sendMapStartTimer(False) if this.isDead or this.room.isTutorial or this.room.isTotemEditor or this.room.isBootcamp or this.room.isDefilante or this.room.getPlayerCountUnique() < 2 else this.sendMapStartTimer(True)

        if this.room.isTotemEditor:
            this.initTotemEditor()

        if this.room.isMulodrome:
            if not this.playerName in this.room.redTeam and not this.playerName in this.room.blueTeam:
                if not this.isDead:
                    this.isDead = True
                    this.sendPlayerDied()

        if this.room.isSurvivor and this.isShaman:
            this.sendPacket(Identifiers.send.Can_Meep, 1)

        if this.room.currentMap in range(200, 211) and not this.isShaman:
            this.sendPacket(Identifiers.send.Can_Transformation, 1)

        if this.room.isVillage:
            this.sendBotsVillage()

    def sendBotsVillage(this):
        this.sendPacket([8, 30], '\xff\xff\xff\xff\x00\x06Oracle\x01+\x00*61;0,0,0,0,0,19_3d100f+1fa896+ffe15b,0,0,0\x08\x8b\x01}\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfe\x00\x08Papaille\x01*\x00\x134;2,0,2,2,0,0,0,0,1\tZ\x00\xd1\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfd\x00\x05Elise\x01]\x00\x143;10,0,1,0,1,0,0,1,0\t\x19\x00\xd1\x01\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfc\x00\x05Buffy\x01[\x00\x06$Buffy\x07t\x01\xf3\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfb\x00\rIndiana Mouse\x01(\x00\x1445;0,0,0,0,0,0,0,0,0\x00\xae\x02\xca\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xfa\x00\x04Prof\x01G\x00\n$Proviseur\x01!\x02\xcb\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xf9\x00\x07Cassidy\x01\x18\x00\x07$Barman\n\xd2\x02%\x00\x0b\x00\x00')
        this.sendPacket([8, 30], '\xff\xff\xff\xf8\x00\x0fVon Drekkemouse\x01\x1f\x00\n$Halloween\x06\x88\x01z\x00\x0b\x00\x00')
        this.sendNPC(1, 1, "Cakmamadara", 336, "00/17;96_FFFFFF+000000,0,0,0,0,0,0,0,0/78583a/95d9d6", 2010, 767, 11, 0)
	#this.sendNPC(1, 2, "Taha", 336, "84;132,0,0,0,0,0,0,0,0", 2964, 700, 11, 0)
        #this.sendNPC(1, 3, "Xgoku_pr0zao", 336, "84;132,0,0,0,0,0,0,0,0", 2010, 767, 11, 0)
        #this.sendNPC(1, 4, "Stricker", 336, "85;132,0,0,0,0,0,0,1,0", 1910, 767, 11, 0)
        this.sendNPC(1, 5, "JeenklynN ", 452, "00/77;78_000000+FFFFFF+000000,0,0,0,18_FFFFFF+000000+000000,4_EAEAEA,21,0,0/78583a/95d9d6", 1810, 767, 11, 0)
        #this.sendNPC(1, 4, "Tugce", 336, "85;132,0,0,0,0,0,0,1,0", 1910, 767, 11, 0)
        #this.sendNPC(1, 7, "Fishing 2017", 422, "87;93,6,0,0,30,0,16,0,0", 1649, 580, 11, 0)
        
    def sendNPC(this, id, id2, name, title, look, px, py, mode, end):
        this.sendPacket([8, 30], ByteArray().writeShort(id).writeShort(id2).writeUTF(name).writeShort(title).writeUTF(look).writeShort(px).writeShort(py).writeShort(mode).writeShort(end).toByteArray()) 


    


    def getPlayerData(this):
        return "#".join(map(str, [this.playerName, this.playerCode, 1, 1 if this.isDead else 0, this.playerScore, 1 if this.hasCheese else 0, "%s,%s,%s" %(this.titleNumber, this.titleStars, this.gender), 0, this.playerLook if not this.room.isBootcamp else "1;0,0,0,0,0,0,0,0,0", 0, this.tempMouseColor if not this.tempMouseColor == "" else this.mouseColor, this.shamanColor, 0]))

    def sendShamanCode(this, shamanCode, shamanCode2):
        this.sendShaman(shamanCode, shamanCode2, this.server.getShamanType(shamanCode), this.server.getShamanType(shamanCode2), this.server.getShamanLevel(shamanCode), this.server.getShamanLevel(shamanCode2), this.server.getShamanBadge(shamanCode), this.server.getShamanBadge(shamanCode2))

    def sendCorrectVersion(this):
        this.sendPacket(Identifiers.send.Correct_Version, ByteArray().writeInt(len(this.server.players)).writeByte(this.lastPacketID).writeUTF("").writeUTF("").writeInt(this.authKey).toByteArray())
        this.sendPacket(Identifiers.send.Banner_Login, ByteArray().writeByte(1).writeByte(this.server.adventureID).writeByte(1).writeBoolean(False).toByteArray())
        this.sendPacket(Identifiers.send.Image_Login, ByteArray().writeUTF(this.server.adventureIMG).toByteArray())
        this.awakeTimer = reactor.callLater(120, this.transport.loseConnection)

    def sendLogin(this):
       this.sendPacket([26, 2], ByteArray().writeInt(this.playerID).writeUTF(this.playerName).writeInt(6000000).writeByte(this.langueID).writeInt(this.playerCode).writeBoolean(True).writeByte(5).writeByte(5).writeBoolean(False).writeByte(10).writeByte(-1).writeByte(-1).writeByte(-1).toByteArray())
          
       if this.isGuest:
          this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(1).writeByte(10).toByteArray())
          this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(2).writeByte(5).toByteArray())
          this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(3).writeByte(15).toByteArray())
          this.sendPacket(Identifiers.send.Login_Souris, ByteArray().writeByte(4).writeUnsignedByte(200).toByteArray())

    def sendTimeStamp(this):
        this.sendPacket(Identifiers.send.Time_Stamp, ByteArray().writeInt(Utils.getTime()).toByteArray())

    def enableSpawnCN(this):
        this.canSpawnCN = True

    def fireworksUtility(this):
        if this.room.isUtility and this.Utility.isFireworks == True:
            this.Utility.newCoordsConj()
            reactor.callLater(0.2, this.Utility.buildConj)
            reactor.callLater(1, this.Utility.removeConj)
            reactor.callLater(1.5, this.fireworksUtility)
    
    def discoUtility(this):
        if this.room.isUtility == True:
            colors = ["000000", "FF0000", "17B700", "F2FF00", "FFB900", "00C0D9", "F600A8", "850000", "62532B", "EFEAE1", "201E1C"]
            sColor = random.choice(colors)                
            data = struct.pack("!i", this.playerCode)
            data += struct.pack("!i", int(sColor, 16))
            this.room.sendAll([29, 4], data)
            if this.room.discoRoom == True:
                this.reactorDisco()

    def reactorDisco(this):
        if this.room.isUtility == True:
            if this.room.discoRoom == True:
                reactor.callLater(0.7, this.discoUtility)

    def sendPromotions(this):
        for promotion in this.server.shopPromotions:
            this.sendPacket(Identifiers.send.Promotion, ByteArray().writeInt(promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)).writeInt(promotion[3]).writeByte(promotion[2]).toByteArray())
        
        if len(this.server.shopPromotions) > 0:
            promotion = this.server.shopPromotions[0]
            item = promotion[0] * (10000 if promotion[1] > 99 else 100) + promotion[1] + (10000 if promotion[1] > 99 else 0)
            this.sendPacket(Identifiers.send.Promotion_Popup, ByteArray().writeByte(promotion[0]).writeByte(promotion[1]).writeByte(promotion[2]).writeShort(this.server.shopBadges.get(item, 0)).toByteArray())

    def sendGameType(this, gameType, serverType):
        this.sendPacket(Identifiers.send.Room_Type, gameType)
        this.sendPacket(Identifiers.send.Room_Server, serverType)

    def sendEnterRoom(this, roomName):
        this.sendPacket(Identifiers.send.Enter_Room, ByteArray().writeBoolean(roomName.startswith("")).writeUTF(roomName).toByteArray())

    def sendMap(this, newMap=False, newMapCustom=False):
        this.sendPacket(Identifiers.send.New_Map, ByteArray().writeInt(this.room.currentMap if newMap else this.room.mapCode if newMapCustom else -1).writeShort(this.room.getPlayerCount()).writeByte(this.room.lastRoundCode).writeShort(0).writeUTF("" if newMap else this.room.mapXML.encode("zlib") if newMapCustom else this.room.EMapXML.encode("zlib")).writeUTF("" if newMap else this.room.mapName if newMapCustom else "-").writeByte(0 if newMap else this.room.mapPerma if newMapCustom else 100).writeBoolean(this.room.mapInverted if newMapCustom else False).toByteArray())

    def sendPlayerList(this):
        this.sendPacket(Identifiers.old.send.Player_List, this.room.getPlayerList())

    def sendSync(this, playerCode):
        this.sendPacket(Identifiers.old.send.Sync, [playerCode, ""] if (this.room.mapCode != 1 or this.room.EMapCode != 0) else [playerCode])

    def sendRoundTime(this, time):
        this.sendPacket(Identifiers.send.Round_Time, ByteArray().writeShort(0 if time < 0 or time > 32767 else time).toByteArray())

    def sendMapStartTimer(this, startMap):
        this.sendPacket(Identifiers.send.Map_Start_Timer, ByteArray().writeBoolean(startMap).toByteArray())

    def sendPlayerDisconnect(this):
        this.room.sendAll(Identifiers.old.send.Player_Disconnect, [this.playerCode])

    def sendChangeMap(this, time):
       this.room.sendAll([5, 22], ByteArray().writeShort(time).toByteArray())
       if this.room.changeMapTimer:
               try:
                       this.room.changeMapTimer.cancel()
               except:
                       this.room.changeMapTimer=None
       this.room.changeMapTimer = reactor.callLater(time, this.room.mapChange)

    def sendPlayerDied(this):
        this.room.sendAll(Identifiers.old.send.Player_Died, [this.playerCode, this.playerScore])
        this.hasCheese = False

        if this.room.getAliveCount() < 1 or this.room.catchTheCheeseMap or this.isAfk:
            this.canShamanRespawn = False

        if ((this.room.checkIfTooFewRemaining() and not this.canShamanRespawn) or (this.room.checkIfShamanIsDead() and not this.canShamanRespawn) or (this.room.checkIfDoubleShamansAreDead())):
            this.room.send20SecRemainingTimer()

        if this.room.isDeathmatch:
           if this.room.checkIfDeathMouse():
              if this.room.getPlayerCount() >= 2:
                 this.sendChangeMap(5)
              for client in this.room.clients.values():
                 if not client.isDead:
                     client.sendMessage("<J>Bu roundu kazanmak için, bir sonraki bekleyin.")

        if this.room.isRacing:
            this.racingRounds = 0

        if this.canShamanRespawn:
            this.isDead = False
            this.isAfk = False
            this.hasCheese = False
            this.hasEnter = False
            this.canShamanRespawn = False
            this.playerStartTimeMillis = time.time()
            this.room.sendAll(Identifiers.old.send.Player_Respawn, [this.getPlayerData(), 1])
            for player in this.room.clients.values():
                player.sendShamanCode(this.playerCode, 0)

    def sendShaman(this, shamanCode, shamanCode2, shamanType, shamanType2, shamanLevel, shamanLevel2, shamanBadge, shamanBadge2):
        this.sendPacket(Identifiers.send.Shaman_Info, ByteArray().writeInt(shamanCode).writeInt(shamanCode2).writeByte(shamanType).writeByte(shamanType2).writeShort(shamanLevel).writeShort(shamanLevel2).writeShort(shamanBadge).writeShort(shamanBadge2).toByteArray())

    def sendConjurationDestroy(this, x, y):
        this.room.sendAll(Identifiers.old.send.Conjuration_Destroy, [x, y])

    def sendGiveCheese(this, distance=-1):
        if distance != -1 and distance != 1000 and not this.room.catchTheCheeseMap and this.room.countStats:
            if distance >= 30:
                this.isSuspect = True

        this.room.canChangeMap = False
        if not this.hasCheese:
            this.room.sendAll(Identifiers.old.send.Player_Get_Cheese, [this.playerCode])
            this.hasCheese = True
            
            this.room.numGetCheese += 1 
            if this.room.currentMap in range(108, 114):
                if this.room.numGetCheese >= 10:
                    this.room.killShaman()

            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, 1)
        this.room.canChangeMap = True

    def playerWin(this, holeType, distance=-1):
        if distance != -1 and distance != 1000 and this.isSuspect and this.room.countStats:
            if distance >= 30:
                this.server.sendStaffMessage(7, "[<V>ANTI-HACK</V>][<J>%s</J>][<V>%s</V>] Instant win detected." %(this.ipAddress, this.playerName))
                this.sendPacket(Identifiers.old.send.Player_Ban_Login, [0, "Instant win detected."])
                this.transport.loseConnection()
                return

        timeTaken = int((time.time() - (this.playerStartTimeMillis if this.room.autoRespawn else this.room.gameStartTimeMillis)) * 100)
        if timeTaken > 5:
            this.room.canChangeMap = False
            canGo = this.room.checkIfShamanCanGoIn() if this.isShaman else True
            if not canGo:
                this.sendSaveRemainingMiceMessage()

            if this.isDead or not this.hasCheese and not this.isOpportunist:
                canGo = False

            if this.room.isTutorial:
                this.sendPacket(Identifiers.send.Tutorial, 2)
                this.hasCheese = False
                reactor.callLater(10, lambda: this.startBulle(this.server.recommendRoom(this.langue)))
                this.sendRoundTime(10)
                return

            if this.room.isEditor:
                if not this.room.EMapValidated and this.room.EMapCode != 0:
                    this.room.EMapValidated = True
                    this.sendPacket(Identifiers.old.send.Map_Validated, [""])

            if canGo:
                this.isDead = True
                this.hasCheese = False
                this.hasEnter = True
                this.room.numCompleted += 1
                place = this.room.numCompleted
                if this.room.isDoubleMap:
                    if holeType == 1:
                        this.room.FSnumCompleted += 1
                    elif holeType == 2:
                        this.room.SSnumCompleted += 1
                    else:
                        this.room.FSnumCompleted += 1
                        this.room.SSnumCompleted += 1

                this.currentPlace = place

                if place == 1:
                    this.playerScore += (4 if this.room.isRacing else 16) if not this.room.noAutoScore else 0
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.firstCount += 200
                        this.cheeseCount += 200
                        
                        ntimeTaken = str(timeTaken)
                        if len(ntimeTaken) == 3:
                                ntimeTaken = ntimeTaken[:1] + "." + ntimeTaken[1:]
                        elif len(ntimeTaken) == 4:
                                ntimeTaken = ntimeTaken[:2] + "." + ntimeTaken[2:]
                        elif len(timeTaken) == 5:
                                ntimeTaken = ntimeTaken[:3] + "." + ntimeTaken[3:]
                        #this.sendMessage(str(ntimeTaken), True)
                        if not this.room.mapPerma == -1:
                            CursorMaps.execute("select Time from maps where Code = ?", [this.room.mapCode])
                            rrf = eval(CursorMaps.fetchone()[0])
                            namePlayer = rrf.keys()[0]
                            timePlayer = rrf[rrf.keys()[0]]
                            if not timePlayer == 0:
                                if float(ntimeTaken) < float(timePlayer):
                                    recordista = {this.playerName: ntimeTaken}
                                    strRecordista = str(recordista)
                                    CursorMaps.execute("update maps set Time = ? where Code = ?", [strRecordista, this.room.mapCode])
                                    this.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<font color='#00C0FF'>%s</font>, haritayı <J>%s</J> saniyede tamamlayarak rekor kırdı." % (this.playerName, ntimeTaken)).toByteArray())
                            else:
                                recordista = {this.playerName: ntimeTaken}
                                strRecordista = str(recordista)
                                CursorMaps.execute("update maps set Time = ? where Code = ?", [strRecordista, this.room.mapCode])
                                this.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<J>%s</J> haritayı <J>%s</J> tamamlayarak haritanın ilk rekorunu kırdı." % (this.playerName, ntimeTaken)).toByteArray())
 
                elif place == 2:
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.cheeseCount += 150
                    this.playerScore += (3 if this.room.isRacing else 14) if not this.room.noAutoScore else 0
                            
                elif place == 3:
                    if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.isShaman and not this.canShamanRespawn:
                        this.cheeseCount += 100
                    this.playerScore += (2 if this.room.isRacing else 12) if not this.room.noAutoScore else 0

                else:
                    this.playerScore += (1 if this.room.isRacing else 10) if not this.room.noAutoScore else 0

                if this.room.isMulodrome:
                    if this.playerName in this.room.redTeam:
                        this.room.redCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    elif this.playerName in this.room.blueTeam:
                        this.room.blueCount += 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                    this.room.sendMulodromeRound()

                if this.room.isDefilante:
                    if not this.room.noAutoScore: this.playerScore += this.defilantePoints

                if this.room.getPlayerCountUnique() >= this.server.needToFirst:
                   if this.room.isRacing:
                       id = 2103
                       this.racingRounds += 1
                       if this.racingRounds >= 1:
                           if not id in this.playerConsumables:
                               this.playerConsumables[id] = 1
                           else:
                               count = this.playerConsumables[id] + 1
                               this.playerConsumables[id] = count
                           this.sendAnimZeldaInventory(4, id, 1)
                           this.racingRounds = 0

                   if this.room.isBootcamp:
                       id = 2261
                       this.bootcampRounds += 1
                       if this.bootcampRounds == 1:
                           if not id in this.playerConsumables:
                               this.playerConsumables[id] = 1
                           else:
                               count = this.playerConsumables[id] + 1
                               this.playerConsumables[id] = count
                           this.sendAnimZeldaInventory(4, id, 1)

                if this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.countStats and not this.room.isBootcamp:
                    if this.playerCode == this.room.currentShamanCode or this.playerCode == this.room.currentSecondShamanCode:
                        this.shamanCheeses += 1
                        this.sendAnimZeldaInventory(4, 2253, 1)
                        if this.playerConsumables.has_key(2253):
                            this.playerConsumables[2253] += 1
                        else:
                            this.playerConsumables[2253] = 1
                    else:
                        this.cheeseCount += 1

                        count = 4 if place == 1 else 3 if place == 2 else 2 if place == 2 else 1
                        this.shopCheeses += count
                        this.shopFraises += count

                        this.sendGiveCurrency(0, count)
                        this.parseSkill.earnExp(False, 20)

                        if not this.isGuest:
                            if place == 1 and this.server.firstTitleList.has_key(this.firstCount):
                                title = this.server.firstTitleList[this.firstCount]
                                this.checkAndRebuildTitleList("first")
                                this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                                this.sendCompleteTitleList()
                                this.sendTitleList()

                            if this.server.cheeseTitleList.has_key(this.cheeseCount):
                                title = this.server.cheeseTitleList[this.cheeseCount]
                                this.checkAndRebuildTitleList("cheese")
                                this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                                this.sendCompleteTitleList()
                                this.sendTitleList()

                elif this.room.getPlayerCountUnique() >= this.server.needToFirst and this.room.isBootcamp:
                    this.bootcampCount += 1

                    if this.server.bootcampTitleList.has_key(this.bootcampCount):
                        title = this.server.bootcampTitleList[this.bootcampCount]
                        this.checkAndRebuildTitleList("bootcamp")
                        this.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                        this.sendCompleteTitleList()
                        this.sendTitleList()

                this.room.giveShamanSave(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName, 0)
                if this.room.currentShamanType != 0:
                    this.room.giveShamanSave(this.room.currentShamanName, this.room.currentShamanType)

                if this.room.currentSecondShamanType != 0:
                    this.room.giveShamanSave(this.room.currentSecondShamanName, this.room.currentSecondShamanType)

                player = this.server.players.get(this.room.currentSecondShamanName if holeType == 2 and this.room.isDoubleMap else this.room.currentShamanName)
                if player != None:
                    if this.hasArtefact:
                        player.aventureSaves += 1

                if this.hasArtefact:
                    if not this.artefactID == 0:
                        imageID = this.artefactID
                        if not imageID in this.aventureCounts:
                            this.aventureCounts[imageID] = (3, 1)
                        else:
                            count = this.aventureCounts[imageID][1] + 1
                            this.aventureCounts[imageID] = (3, count)

                        if this.aventureCounts[imageID][1] == 30:
                            count = this.aventurePoints[24] + 15
                            this.aventurePoints[24] = count

                        if this.aventurePoints[24] == 30:
                            titles = ["420.1"]
                            title = random.choice(titles)
                            while title in this.titleList:
                                try:
                                    titles.remove(title)
                                    title = random.choice(titles)
                                except:
                                    break
                            if not title in this.titleList:
                                stitle = title.split(".")
                                this.specialTitleList = this.specialTitleList + [float(title)]
                                this.sendUnlockedTitle(stitle[0], stitle[1])

                                this.sendCompleteTitleList()
                                this.sendTitleList()

                        if this.aventurePoints[24] == 60:
                            medal = 181
                            if not int(medal) in this.shopBadges:
                                this.parseShop.sendUnlockedBadge(medal)
                                this.shopBadges.append(str(medal))

                        if this.aventurePoints[24] == 90:
                            titles = ["421.1"]
                            title = random.choice(titles)
                            while title in this.titleList:
                                try:
                                    titles.remove(title)
                                    title = random.choice(titles)
                                except:
                                    break
                            if not title in this.titleList:
                                stitle = title.split(".")
                                this.specialTitleList = this.specialTitleList + [float(title)]
                                this.sendUnlockedTitle(stitle[0], stitle[1])

                                this.sendCompleteTitleList()
                                this.sendTitleList()

                this.sendPlayerWin(place, timeTaken)

                if this.room.getPlayerCount() >= 2 and this.room.checkIfTooFewRemaining() and not this.room.isDoubleMap:
                    enterHole = False
                    for player in this.room.clients.values():
                        if player.isShaman and player.isOpportunist:
                            player.isOpportunist = True
                            player.playerWin(0)
                            enterHole = True
                            break
                    this.room.checkChangeMap()
                else:
                    this.room.checkChangeMap()

            this.room.canChangeMap = True
        else:
            this.isDead = True
            this.sendPlayerDied()

    def sendSaveRemainingMiceMessage(this):
        this.sendPacket(Identifiers.old.send.Save_Remaining, [])

    def sendGiveCurrency(this, type, count):
        this.sendPacket(Identifiers.send.Give_Currency, ByteArray().writeByte(type).writeByte(count).toByteArray())

    def sendPlayerWin(this, place, timeTaken):
        this.room.sendAll(Identifiers.send.Player_Win, ByteArray().writeByte(1 if this.room.isDefilante else (2 if this.playerName in this.room.blueTeam else 3 if this.playerName in this.room.blueTeam else 0)).writeInt(this.playerCode).writeShort(this.playerScore).writeUnsignedByte(255 if place >= 255 else place).writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken).toByteArray())
        this.hasCheese = False

    def sendCompleteTitleList(this):
        this.titleList = []
        this.titleList.append(0.1)
        this.titleList.extend(this.shopTitleList)
        this.titleList.extend(this.firstTitleList)
        this.titleList.extend(this.cheeseTitleList)
        this.titleList.extend(this.shamanTitleList)
        this.titleList.extend(this.bootcampTitleList)
        this.titleList.extend(this.hardModeTitleList)
        this.titleList.extend(this.divineModeTitleList)
        this.titleList.extend(this.specialTitleList)

        if this.privLevel == 12:
            this.titleList.extend([201.9, 456.9, 443.9, 441.9, 439.9, 440.9, 442.9, 444.9, 445.9, 446.9, 447.9, 448.9, 449.9, 450.9, 451.9, 452.9, 453.9, 454.9, 455.9, 456.9, 457.9]) #Owner
		
        if this.privLevel == 11:
            this.titleList.extend([201.9]) #Baş Admin
			
        if this.privLevel == 10:
            this.titleList.extend([201.9]) #Genel Sorumlu

        elif this.privLevel == 9:
            this.titleList.extend([201.9]) #Admin

        elif this.privLevel == 8:
            this.titleList.extend([201.9]) #Smod

        elif this.privLevel == 7:
            this.titleList.extend([201.9]) #Mod

        elif this.privLevel == 6:
            this.titleList.extend([201.9]) #Mapcrew

        elif this.privLevel == 5:
            this.titleList.extend([201.9]) #Helper

        elif this.privLevel == 2:
            this.titleList.extend([201.9]) #Vip
            
    def sendTitleList(this):
        this.sendPacket(Identifiers.old.send.Titles_List, [this.titleList])

    def sendUnlockedTitle(this, title, stars):
        this.room.sendAll(Identifiers.old.send.Unlocked_Title, [this.playerCode, title, stars])

    def sendMessage(this, message, tab=False):
        this.sendPacket(Identifiers.send.Recv_Message, ByteArray().writeBoolean(tab).writeUTF(message).writeByte(0).writeUTF("").toByteArray())

    def sendProfile(this, playerName):
        player = this.server.players.get(playerName.lower().capitalize())
        if player == None or player.isGuest:
            pass
        else:
            p = ByteArray()
            p.writeUTF(player.playerName)
            p.writeInt(player.playerID)
            p.writeInt(str(player.regDate)[:10])
            if player.privLevel == 1:
                yetki_renk = 1
            if player.privLevel == 2 or player.privLevel == 3 or player.privLevel == 4 or player.privLevel == 5:
                yetki_renk = 11
            if player.privLevel >= 6:
                yetki_renk = 5
            if player.privLevel == 9:
                yetki_renk = 11    
            if player.privLevel == 10:
                yetki_renk = 13
            if player.privLevel == 11:
                yetki_renk = 13 
            if player.privLevel == 12:
                yetki_renk = 10

            p.writeByte(yetki_renk)#yetki renk
            p.writeByte(player.gender)# cinsiyet
            p.writeUTF(player.tribeName) #kabile
            p.writeUTF(player.marriage + "\n<font color='#c0c0d8'>Yetki:</font> " + ("<font color='#B44848'><font size='14' face='soopafresh'>☪ Game Master ☪</font></font>" if player.privLevel == 12 else "<font color='#B44848'><font size='14' face='soopafresh'>Genel Sorumlu</font></font>" if player.privLevel == 10 else "<font color='#AB53CC'><font size='14' face='soopafresh'>GenelSorumlu</font></font>" if player.privLevel == 9 else "<font color='#B1E856'><font size='14' face='soopafresh'>Super Moderator</font></font>" if player.privLevel == 8 else "<font color='#C9C067'><font size='14' face='soopafresh'>Moderator</font></font>" if player.privLevel == 7 else "<font color='#45A0BC'><font size='14' face='soopafresh'>MapCrew</font></font>" if player.privLevel == 6 else "<font color='#BB8848'><font size='14' face='soopafresh'>Helper</font></font>" if player.privLevel == 5 else "Oyuncu"))
            for stat in [player.shamanSaves, player.shamanCheeses, player.firstCount, player.cheeseCount, player.hardModeSaves, player.bootcampCount, player.divineModeSaves]:
                p.writeInt(stat)
            p.writeShort(player.titleNumber) # unvan
            p.writeShort(len(player.titleList))
            for title in player.titleList:
                p.writeShort(int(title - (title % 1)))
                p.writeByte(int(round((title % 1) * 10)))
            try:
                fullLook = player.playerLook + ';' + player.mouseColor
            except:
                packet.writeInt(int("", 16))
                fullLook = player.playerLook + ';78583A'
            p.writeUTF(fullLook)
            p.writeShort(player.shamanLevel)
            badges = []
            for bid in player.shopBadges:
                if 0 <= int(bid) <= 255:
                    badges.append(bid)

            p.writeShort(len(badges)*2)
            for badge in badges:
                p.writeUnsignedByte(int(badge))
                p.writeByte(int(badges.count(badge)))

            stats = [[30, player.racingStats[0], 1500, 124], [31, player.racingStats[1], 10000, 125], [33, player.racingStats[2], 10000, 127], [32, player.racingStats[3], 10000, 126], [26, player.survivorStats[0], 1000, 120], [27, player.survivorStats[1], 800, 121], [28, player.survivorStats[2], 20000, 122], [29, player.survivorStats[3], 10000, 123]]
            p.writeByte(len(stats))
            for stat in stats:
                p.writeByte(stat[0]).writeInt(stat[1]).writeInt(stat[2]).writeByte(stat[3])

            p.writeUnsignedByte(len(player.shamanBadges))
            stats2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30]
            p.writeByte(len(stats2))
            for stat2 in stats2:
                p.writeByte(stat2)
 
            count = 100
            for c in player.aventurePoints.values():
                count += c
            p.writeByte(1).writeInt(count)

            this.sendPacket(Identifiers.send.Profile, p.toByteArray())

    def sendPlayerBan(this, hours, reason, silent):
        this.sendPacket(Identifiers.old.send.Player_Ban, [hours * 3600000, reason])
        if not silent and this.room != None:
            for player in this.room.clients.values():
                player.sendLangueMessage("", "<ROSE>• [Moderasyon] $Message_Ban", this.playerName, str(hours), reason)
        this.server.disconnectIPAddress(this.ipAddress)

    def sendPlayerEmote(this, emoteID, flag, others, lua):
        packet = ByteArray().writeInt(this.playerCode).writeByte(emoteID)
        if not flag == "": packet.writeUTF(flag)
        this.room.sendAllOthers(this, Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray()) if others else this.room.sendAll(Identifiers.send.Player_Emote, packet.writeBoolean(lua).toByteArray())

    def sendEmotion(this, emotion):
        this.room.sendAllOthers(this, Identifiers.send.Emotion, ByteArray().writeInt(this.playerCode).writeByte(emotion).toByteArray())

    def sendPlaceObject(this, objectID, code, px, py, angle, vx, vy, dur, sendAll):
        packet = ByteArray().writeInt(objectID).writeShort(code).writeShort(px).writeShort(py).writeShort(angle).writeByte(vx).writeByte(vy).writeBoolean(dur)
        if this.isGuest or sendAll:
            packet.writeByte(0)
        else:
            packet.writeBytes(this.parseShop.getShamanItemCustom(code))

        if not sendAll:
            this.room.sendAllOthers(this, Identifiers.send.Spawn_Object, packet.toByteArray())
            this.room.objectID = objectID
        else:
            this.room.sendAll(Identifiers.send.Spawn_Object, packet.toByteArray())
       
    def sendTotem(this, totem, x, y, playerCode):
        this.sendPacket(Identifiers.old.send.Totem, ["%s#%s#%s%s" %(playerCode, x, y, totem)])

    def sendTotemItemCount(this, number):
        if this.room.isTotemEditor:
            this.sendPacket(Identifiers.send.Totem_Item_Count, ByteArray().writeShort(number * 2).toByteArray())

    def initTotemEditor(this):
        if this.resetTotem:
            this.sendTotemItemCount(0)
            this.resetTotem = False
        else:
            if not this.totem[1] == "":
                this.tempTotem[0] = this.totem[0]
                this.tempTotem[1] = this.totem[1]
                this.sendTotemItemCount(this.tempTotem[0])
                this.sendTotem(this.tempTotem[1], 400, 204, this.playerCode)
            else:
                this.sendTotemItemCount(0)

    def sendShamanType(this, mode, canDivine):
        this.sendPacket(Identifiers.send.Shaman_Type, ByteArray().writeByte(mode).writeBoolean(canDivine).writeInt(int(this.shamanColor, 16)).toByteArray())

    def sendBanConsideration(this):
        this.sendPacket(Identifiers.old.send.Ban_Consideration, ["0"])
        
    def sendShamanPosition(this, direction):
        this.room.sendAll(Identifiers.send.Shaman_Position, ByteArray().writeInt(this.playerCode).writeBoolean(direction).toByteArray())

    def sendLangueMessage(this, community, message, *args):
        packet = ByteArray().writeUTF(community).writeUTF(message).writeByte(len(args))
        for arg in args:
            packet.writeUTF(arg)
        this.sendPacket(Identifiers.send.Message_Langue, packet.toByteArray())

    def sendModMute(this, playerName, hours, reason, only):
        if not only:
            this.room.sendMessage("", "<ROSE>• [Moderasyon] $MuteInfo2", playerName, playerName, hours, reason)
        else:
            player = this.server.players.get(playerName)
            if player:
                player.sendLangueMessage("", "<ROSE>• [Moderasyon] $MuteInfo1", hours, reason)

    def sendVampireMode(this, others):
        this.isVampire = True
        if others:
            this.room.sendAllOthers(this, Identifiers.send.Vampire_Mode, ByteArray().writeInt(this.playerCode).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Vampire_Mode, ByteArray().writeInt(this.playerCode).toByteArray())

    def sendRemoveCheese(this):
        this.room.sendAll(Identifiers.send.Remove_Cheese, ByteArray().writeInt(this.playerCode).toByteArray())

    def sendLuaMessage(this, message):
        this.sendPacket(Identifiers.send.Lua_Message, ByteArray().writeUTF(message).toByteArray())

    def sendGameMode(this, mode):
        mode = 1 if mode == 0 else mode
        types = [1, 3, 8, 9, 11, 2, 10, 18, 16]
        packet = ByteArray().writeByte(len(types))
        for roomType in types:
            packet.writeByte(roomType)

        packet.writeByte(mode)
        modeInfo = this.server.getPlayersCountMode(mode, this.langue)
        if not modeInfo[0] == "":
            packet.writeByte(1).writeByte(this.langueID).writeUTF(str(modeInfo[0])).writeUTF(str(modeInfo[1])).writeUTF("mjj").writeUTF("1")
            roomsCount = 0
            for checkRoom in this.server.rooms.values():
                if ({1:checkRoom.isNormRoom, 3:checkRoom.isVanilla, 8:checkRoom.isSurvivor, 9:checkRoom.isRacing, 11:checkRoom.isMusic, 2:checkRoom.isBootcamp, 10:checkRoom.isDefilante, 18:0, 16:checkRoom.isVillage}[mode]) and checkRoom.community == this.langue.lower():
                    roomsCount += 1
                    packet.writeByte(0).writeByte(this.langueID).writeUTF(checkRoom.roomName).writeShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(False)

            if roomsCount == 0:
                packet.writeByte(0).writeByte(this.langueID).writeUTF(("" if mode == 1 else str(modeInfo[0].split(" ")[1])) + "1").writeShort(0).writeUnsignedByte(200).writeBoolean(False)

        if mode == 18:
            minigameList = ["#deathmatch", "#utility"]
            moduleCount = {"#deathmatch": 0, "#utility": 0}
            moduleMjj = {"#deathmatch": "#deathmatch", "#utility": "#utility0%s" % (this.playerName)}
            for checkRoom in this.server.rooms.values():
                if checkRoom.isUtility:
                    moduleCount["#utility"] += checkRoom.getPlayerCount()
                elif checkRoom.isDeathmatch:
                    moduleCount["#deathmatch"] += checkRoom.getPlayerCount()
            for minigame in minigameList:                
                packet.writeUnsignedByte(1).writeUnsignedByte(this.langueID).writeUTF(str(minigame)).writeUTF(str(moduleCount[minigame])).writeUTF("mjj").writeUTF(str(moduleMjj[minigame]))
            for checkRoom in this.server.rooms.values():
                if checkRoom.isUtility or checkRoom.isDeathmatch:
                    packet.writeUnsignedByte(0).writeUnsignedByte(this.langueID).writeUTF(checkRoom.roomName).writeUnsignedShort(checkRoom.getPlayerCount()).writeUnsignedByte(checkRoom.maxPlayers).writeBoolean(False)
        this.sendPacket(Identifiers.send.Game_Mode, packet.toByteArray())

    def sendMusicVideo(this, sendAll):
        music = this.room.musicVideos[0]
        packet = ByteArray().writeUTF(str(music["VideoID"].encode("UTF-8"))).writeUTF(str(music["Title"].encode("UTF-8"))).writeShort(this.room.musicTime).writeUTF(str(music["By"].encode("UTF-8")))
        if sendAll:
            this.room.sendAll(Identifiers.send.Music_Video, packet.toByteArray())
        else:
            this.sendPacket(Identifiers.send.Music_Video, packet.toByteArray())

    def checkMusicSkip(this):
        if this.room.isMusic and this.room.isPlayingMusic:
            count = this.room.getPlayerCount()
            count = count if count % 2 == 0 else count + 1
            if this.room.musicSkipVotes >= (count / 2):
                del this.room.musicVideos[0]
                this.room.musicTime = 0
                this.sendMusicVideo(True)
                this.room.musicSkipVotes = 0

    def sendStaffMessage(this, message, othersLangues, tab=False):
        for player in this.server.players.values():
            if othersLangues or player.langue == this.langue:
                player.sendMessage(message, tab)

    def sendBulle(this):
        this.sendPacket(Identifiers.send.Bulle, ByteArray().writeInt(0).writeUTF("x").toByteArray())

    def checkVip(this, vipTime):
        days = Utils.getDiffDays(vipTime)
        if (days <= int(str(thetime.time()).split(".")[0])):
            this.privLevel = 1
            if this.titleNumber == 1100:
                this.titleNumber = 0

            this.sendMessage("O seu VIP se estogou.")
            this.Cursor.execute("update users set VipTime = 0 where Username = ?", [this.playerName])
        else:
            d = datetime.fromtimestamp(int(days)) - datetime.now()
            hours = str(timedelta(seconds=d.seconds)).split(":")
            if not d.days <= 0:
               this.sendMessage("Você ainda tem <V>"+str(d.days)+"</V> dias e <V>"+hours[0]+"</V> horas de VIP!")
            else:
               if not hours[0] == "0":
                  this.sendMessage("Você ainda tem <V>"+hours[0]+"</V> horas de VIP!")
               else:
                  this.sendMessage("Você ainda tem <V>"+hours[1]+"</V> minutos de VIP!")
                  
    def sendLogMessage(this, message):
        this.sendPacket(Identifiers.send.Log_Message, ByteArray().writeByte(0).writeUTF("").writeUnsignedByte((len(message) >> 16) & 0xFF).writeUnsignedByte((len(message) >> 8) & 0xFF).writeUnsignedByte(len(message) & 0xFF).writeBytes(message).toByteArray())

    def runLuaAdminScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            startTime = int(time.time())
            endTime = int(time.time())
            totalTime = endTime - startTime
            message = "<V>["+this.room.roomName+"]<BL> ["+this.playerName+"] Lua script loaded in "+str(totalTime)+" ms (4000 max)"
            this.sendLuaMessage(message)
        except Exception as error:
            this.server.sendStaffMessage(7, "<V>["+this.room.roomName+"]<BL> [Bot: "+this.playerName+"][Exception]: "+str(error))

    def runLuaScript(this, script):
        try:
            pythonScript = compile(str(script), "<string>", "exec")
            exec pythonScript
            totalTime = int(time.time() - time.time())
            this.sendLuaMessage("<V>[%s]<BL> [%s] %s" %(this.room.roomName, this.playerName, "Lua script not loaded. (%s ms - 4000 max)" %(totalTime) if totalTime > 4000 else "Lua script loaded in %s ms (4000 max)" %(totalTime)))
        except Exception as error:
            this.sendLuaMessage("<V>[%s]<BL> [%s][<R>Exception</R>]: %s" %(this.room.roomName, this.playerName, error))
        else:
            this.server.sendStaffMessage(5, "[<V>Lua<BL>][<J>%s<BL>][<R>%s<BL>][<J>%s-%s</J>] Tentou usar algum script no Lua." %(this.ipAddress, this.playerName, this.langue.upper(), this.room.roomName))

    def cnTrueOrFalse(this):
        this.canCN = False

    def sendImg(this, id, image, x, y, sla=1000, minigame=0):
       packet = ByteArray()
       packet.writeInt(id)
       packet.writeUTF(image)
       packet.writeByte(7)
       packet.writeInt(sla)
       packet.writeShort(x)
       packet.writeShort(y)
       this.sendPacket([29, 19], packet.toByteArray())
       if minigame == 1:
          reactor.callLater(0.9, this.removeImage, (id))

    def removeImage(this, id):
       packet = ByteArray()
       packet.writeInt(id)
       this.sendPacket([29, 18], packet.toByteArray())

    def sendContagem(this):
       image = "149af14e1ba.png" if this.countP == 0 else "149af0f217c.png" if this.countP == 1 else "149af14bccc.png" if this.countP == 2 else "149aeabbb5e.png"
       this.sendImg(this.countP, image, 300, 240, 1000, 1)
       this.countP += 1
       if this.countP <= 3:
          reactor.callLater(1, this.sendContagem)
       else:
          this.room.canCannon = True
          this.countP = 0

    def sendDeathInventory(this, page=1):
       ids = 504, 505, 506, 507
       for id in ids:
          this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       message1 = ""
       message2 = '<font color="#9ab7c6"><a href="event:prev">Previous</a></font>'
       message3 = ""
       message4 = ""
       message5 = '<font color="#9ab7c6"><a href="event:next">Next</a></font>'
       message6 = ""
       message7 = ""
       message8 = '<p align="center"><font size="28" face="Soopafresh,Verdana,Arial,sans-serif" color="#9ab7c6">Inventory</font></p>'
       message9 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       if page == 1:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Happy Halloween</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Use !f to choose your cannon. This is only temporary and will be removed in the future.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 15 else '<a href="event:inventory#use#15"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Golden Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was forged with the purest gold found in land. It is meant only for the best of all the mice.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 16 else '<a href="event:inventory#use#16"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Silver Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">These cannons might work really well on weremice!</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 17 else '<a href="event:inventory#use#17"><p align="center">Equip</p>'
          this.sendImg(504, "149aeaa271c.png", 233, 145, 300)
          this.sendImg(505, "149af112d8f.png", 391, 145, 301)
          this.sendImg(506, "149af12c2d6.png", 549, 145, 302)

       if page == 2:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Bronze Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Never before was a cannon so hard and durable.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 18 else '<a href="event:inventory#use#18"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Balanced Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">It might be time for a diet, you should eat more cheese.</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 19 else '<a href="event:inventory#use#19"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Plate-Spike Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was re-inforced with metal plating and spikes. It must not have been deadly enough yet.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 20 else '<a href="event:inventory#use#20"><p align="center">Equip</p>'
          this.sendImg(504, "149af130a30.png", 233, 145, 300)
          this.sendImg(505, "149af0fdbf7.png", 391, 145, 301)
          this.sendImg(506, "149af0ef041.png", 549, 145, 302)

       if page == 3:
          message10 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Death Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon was forged by death himself.</font>\n\n<font color="#c2c2da">'
          message11 = ""
          message12 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 21 else '<a href="event:inventory#use#21"><p align="center">Equip</p>'
          message13 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Diamond Ore Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">Why is there diamond in my cannon?</font>\n\n<font color="#c2c2da">'
          message14 = ""
          message15 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 22 else '<a href="event:inventory#use#22"><p align="center">Equip</p>'
          message16 = '<p align="center"><p align="center"><font size="15" face="Soopafresh,Verdana,Arial,sans-serif" color="#C2C2DA">Lightning Cannon</font></p></p>\n\n\n\n\n<p align="justify"><font size="10"><font color="#93ADBA">This cannon is lightning fast and hits as thunder.</font>\n\n<font color="#c2c2da">'
          message17 = ""
          message18 = '<a href="event:inventory#remove"><p align="center">Unequip</p></a>' if this.deathStats[4] == 23 else '<a href="event:inventory#use#23"><p align="center">Equip</p>'
          this.sendImg(504, "149af13e210.png", 233, 145, 300)
          this.sendImg(505, "149af129a4c.png", 391, 145, 301)
          this.sendImg(506, "149aeaa06d1.png", 549, 145, 302)

          
       this.sendMBox(message1, 95, 99, 70, 16, "100%", "698358", "698358", 131458)#message, x, y, bg, border, alpha, color, color, id, fixed
       this.sendMBox(message2, 95, 100, 70, 16, "100%", "324650", "324650", 123479)
       this.sendMBox(message3, 95, 131, 70, 16, "100%", "000001", "000001", 130449)
       this.sendMBox(message4, 95, 129, 70, 16, "100%", "698358", "698358", 131459)
       this.sendMBox(message5, 95, 130, 70, 16, "100%", "324650", "324650", 123480)
       this.sendMBox(message6, 165, 61, 485, 300, "100%", "000001", "000001", 6992)
       this.sendMBox(message7, 165, 59, 485, 300, "100%", "698358", "698358", 8002)
       this.sendMBox(message8, 165, 60, 485, 300, "100%", "324650", "324650", 23)
       this.sendMBox(message9, 623, 60, 30, 30, "0%", "000000", "000000", 9012)
       this.sendMBox(message10, 179, 110, 140, 245, "100%", "204318", "988183", 9013)
       this.sendMBox(message11, 229, 141, 40, 40, "100%", "697666", "988183", 9893)
       this.sendMBox(message12, 179, 325, 140, 30, "30%", "791275", "000000", 8983)
       this.sendMBox(message13, 337, 110, 140, 245, "100%", "204318", "988183", 9014)
       this.sendMBox(message14, 387, 141, 40, 40, "100%", "697666", "988183", 9894)
       this.sendMBox(message15, 337, 325, 140, 30, "30%", "791275", "000000", 8984)
       this.sendMBox(message16, 495, 110, 140, 245, "100%", "204318", "988183", 9015)
       this.sendMBox(message17, 545, 141, 40, 40, "100%", "697666", "988183", 9895)
       this.sendMBox(message18, 495, 325, 140, 30, "30%", "791275", "000000", 8985)
       this.sendImg(507, "149af1e58d7.png", 601, 124, 300)

    def sendDeathProfile(this):
       ids = 39, 40, 41
       for id in ids:
          this.sendPacket([29, 18], ByteArray().writeInt(id).toByteArray())
       yn = "Yes" if this.deathStats[3] == 0 else "No"
       message1 = ""
       message2 = "<p align=\"center\"><font size=\"28\" face=\"Soopafresh,Verdana,Arial,sans-serif\" color=\"#9ab7c6\">"+this.playerName+"</font></p><p><font color=\"#c0c0d8\"> Settings</font>\n<font color=\"#6b76bf\">\t• Offset X : </font><font color=\"#009b9b\">"+str(this.deathStats[0])+"</font><J> <a href=\"event:offset#offsetX#1\">[+]</a> <a href=\"event:offset#offsetX#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Offset Y : </font><font color=\"#009b9b\">"+str(this.deathStats[1])+"</font><J> <a href=\"event:offset#offsetY#1\">[+]</a> <a href=\"event:offset#offsetY#-1\">[−]</a>\n<font color=\"#6b76bf\">\t• Warn status : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Special Cannon Display : </font><font color=\"#009b9b\"><J><a href=\"event:show\">"+yn+"</a></font></p><p><font color=\"#c0c0d8\"> Season</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><font color=\"#6b76bf\">\t• Rank : </font><font color=\"#009b9b\">1</font> \n<p><font color=\"#c0c0d8\"> Global</font>\n<font color=\"#6b76bf\">\t• Survived : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">2</font></p><p><font color=\"#c0c0d8\"> Team</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p><p><font color=\"#c0c0d8\"> Honour Battle</font>\n<font color=\"#6b76bf\">\t• Wins : </font><font color=\"#009b9b\">0</font>\n<font color=\"#6b76bf\">\t• Rounds : </font><font color=\"#009b9b\">0</font></p>"
       message3 = '<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>'
       message4 = ""
       message5 = ""
       message6 = ""
       #this.sendPacket([29, 20], '\x00\x00#1\x00X<p align="center"><font color="#9ab7c6" size="16"><a href="event:close">X</a></font></p>\x02\x06\x00<\x00\x1e\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
       this.sendImg(39, "149af12df23.png", 427, 180, 201)
       this.sendImg(40, "149af10434e.png", this.deathStats[5], this.deathStats[6], 202)
       this.sendImg(41, "149af10637b.png", 152, 90, 203)
       this.sendMBox(message1, 267, 59, 278, 290, "100%", "698358", "698358", 7999, False)
       this.sendMBox(message2, 267, 60, 278, 280, "100%", "324650", "324650", 20)
       this.sendMBox(message3, 518, 59, 30, 30, "0%", "000000", "000000", 9009)
       this.sendMBox(message4, 152, 91, 101, 101, "100%", "000001", "000001", 7239)
       this.sendMBox(message5, 152, 89, 101, 101, "100%", "698358", "698358", 8249)
       this.sendMBox(message6, 152, 90, 101, 101, "100%", "324650", "324650", 270, False)

    def reloadRanking(this):
        Userlist = []
        this.Cursor.execute('select Username, ShamanSaves, CheeseCount, FirstCount from users where PrivLevel <=2')
        rrfRows = this.Cursor.fetchall()
        if len(rrfRows) >= 15:
            if rrfRows is None:
                    pass
            else:
                    for rrf in rrfRows:
                            Userlist.append(rrf)
            #Saves
            SavesList={}
            SavesListDisp=[]
            for user in Userlist:
                    SavesList[user[0]] = user[1]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([1, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([2, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([3, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([4, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([5, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([6, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([7, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([8, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([9, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([10, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([11, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([12, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([13, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([14, mSL, SavesList[mSL]])
            del SavesList[mSL]
            mSL=max(SavesList.iterkeys(), key=lambda k: SavesList[k])
            SavesListDisp.append([15, mSL, SavesList[mSL]])
            del SavesList[mSL]
            #Cheese
            CheeseList={}
            CheeseListDisp=[]
            for user in Userlist:
                CheeseList[user[0]] = user[2]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([1, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([2, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([3, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([4, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([5, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([6, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([7, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([8, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([9, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([10, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([11, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([12, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([13, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([14, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            mSL=max(CheeseList.iterkeys(), key=lambda k: CheeseList[k])
            CheeseListDisp.append([15, mSL, CheeseList[mSL]])
            del CheeseList[mSL]
            #Firsts
            FirstList={}
            FirstListDisp=[]
            for user in Userlist:
                FirstList[user[0]] = user[3]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([1, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([2, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([3, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([4, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([5, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([6, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([7, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([8, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([9, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([10, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([11, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([12, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([13, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([14, mSL, FirstList[mSL]])
            del FirstList[mSL]
            mSL=max(FirstList.iterkeys(), key=lambda k: FirstList[k])
            FirstListDisp.append([15, mSL, FirstList[mSL]])
            del FirstList[mSL]
            
            fundo = "<p align='center'><B><font color='#009D9D' size='17'>EpicMice Ranking</font></B></p>\n\n<font size='17'>       Save                                   Cheese                                    First</font>"
            saves = ("<p align='left'><font size='13'><J>1 - "+str(SavesListDisp[0][1])+"</font> - <CH>"+str(SavesListDisp[0][2])+""
            +"<br><p align='left'><J>2 - "+str(SavesListDisp[1][1])+" - <CH>"+str(SavesListDisp[1][2])+""
            +"<br><p align='left'><J>3 - "+str(SavesListDisp[2][1])+" - <CH>"+str(SavesListDisp[2][2])+""
            +"<br><p align='left'><BL>4 - "+str(SavesListDisp[3][1])+" - <CH>"+str(SavesListDisp[3][2])+""
            +"<br><p align='left'><BL>5 - "+str(SavesListDisp[4][1])+" - <CH>"+str(SavesListDisp[4][2])+""
            +"<br><p align='left'><BL>6 - "+str(SavesListDisp[5][1])+" - <CH>"+str(SavesListDisp[5][2])+""
            +"<br><p align='left'><BL>7 - "+str(SavesListDisp[6][1])+" - <CH>"+str(SavesListDisp[6][2])+""
            +"<br><p align='left'><BL>8 - "+str(SavesListDisp[7][1])+" - <CH>"+str(SavesListDisp[7][2])+""
            +"<br><p align='left'><BL>9 - "+str(SavesListDisp[8][1])+" - <CH>"+str(SavesListDisp[8][2])+""
            +"<br><p align='left'><BL>10- "+str(SavesListDisp[9][1])+" - <CH>"+str(SavesListDisp[9][2])+""
            +"<br><p align='left'><BL>11- "+str(SavesListDisp[10][1])+" - <CH>"+str(SavesListDisp[10][2])+""
            +"<br><p align='left'><BL>12- "+str(SavesListDisp[11][1])+" - <CH>"+str(SavesListDisp[11][2])+""
            +"<br><p align='left'><BL>13- "+str(SavesListDisp[12][1])+" - <CH>"+str(SavesListDisp[12][2])+""
            +"<br><p align='left'><BL>14- "+str(SavesListDisp[13][1])+" - <CH>"+str(SavesListDisp[13][2])+""
            +"<br><p align='left'><BL>15- "+str(SavesListDisp[14][1])+" - <CH>"+str(SavesListDisp[14][2]))

            cheese = ("<p align='left'><font size='13'><J>1 - "+str(CheeseListDisp[0][1])+" - <CH>"+str(CheeseListDisp[0][2])+"</font>"
            +"<br><p align='left'><J>2 - "+str(CheeseListDisp[1][1])+" - <CH>"+str(CheeseListDisp[1][2])+""
            +"<br><p align='left'><J>3 - "+str(CheeseListDisp[2][1])+" - <CH>"+str(CheeseListDisp[2][2])+""
            +"<br><p align='left'><BL>4 - "+str(CheeseListDisp[3][1])+" - <CH>"+str(CheeseListDisp[3][2])+""
            +"<br><p align='left'><BL>5 - "+str(CheeseListDisp[4][1])+" - <CH>"+str(CheeseListDisp[4][2])+""
            +"<br><p align='left'><BL>6 - "+str(CheeseListDisp[5][1])+" - <CH>"+str(CheeseListDisp[5][2])+""
            +"<br><p align='left'><BL>7 - "+str(CheeseListDisp[6][1])+" - <CH>"+str(CheeseListDisp[6][2])+""
            +"<br><p align='left'><BL>8 - "+str(CheeseListDisp[7][1])+" - <CH>"+str(CheeseListDisp[7][2])+""
            +"<br><p align='left'><BL>9 - "+str(CheeseListDisp[8][1])+" - <CH>"+str(CheeseListDisp[8][2])+""
            +"<br><p align='left'><BL>10- "+str(CheeseListDisp[9][1])+" - <CH>"+str(CheeseListDisp[9][2])+""
            +"<br><p align='left'><BL>11- "+str(CheeseListDisp[10][1])+" - <CH>"+str(CheeseListDisp[10][2])+""
            +"<br><p align='left'><BL>12- "+str(CheeseListDisp[11][1])+" - <CH>"+str(CheeseListDisp[11][2])+""
            +"<br><p align='left'><BL>13- "+str(CheeseListDisp[12][1])+" - <CH>"+str(CheeseListDisp[12][2])+""
            +"<br><p align='left'><BL>14- "+str(CheeseListDisp[13][1])+" - <CH>"+str(CheeseListDisp[13][2])+""
            +"<br><p align='left'><BL>15- "+str(CheeseListDisp[14][1])+" - <CH>"+str(CheeseListDisp[14][2]))

            first = ("<p align='left'><font size='13'><J>1 - "+str(FirstListDisp[0][1])+" - <CH>"+str(FirstListDisp[0][2])+"</font>"
            +"<br><p align='left'><J>2 - "+str(FirstListDisp[1][1])+" - <CH>"+str(FirstListDisp[1][2])+""
            +"<br><p align='left'><J>3 - "+str(FirstListDisp[2][1])+" - <CH>"+str(FirstListDisp[2][2])+""
            +"<br><p align='left'><BL>4 - "+str(FirstListDisp[3][1])+" - <CH>"+str(FirstListDisp[3][2])+""
            +"<br><p align='left'><BL>5 - "+str(FirstListDisp[4][1])+" - <CH>"+str(FirstListDisp[4][2])+""
            +"<br><p align='left'><BL>6 - "+str(FirstListDisp[5][1])+" - <CH>"+str(FirstListDisp[5][2])+""
            +"<br><p align='left'><BL>7 - "+str(FirstListDisp[6][1])+" - <CH>"+str(FirstListDisp[6][2])+""
            +"<br><p align='left'><BL>8 - "+str(FirstListDisp[7][1])+" - <CH>"+str(FirstListDisp[7][2])+""
            +"<br><p align='left'><BL>9 - "+str(FirstListDisp[8][1])+" - <CH>"+str(FirstListDisp[8][2])+""
            +"<br><p align='left'><BL>10- "+str(FirstListDisp[9][1])+" - <CH>"+str(FirstListDisp[9][2])+""
            +"<br><p align='left'><BL>11- "+str(FirstListDisp[10][1])+" - <CH>"+str(FirstListDisp[10][2])+""
            +"<br><p align='left'><BL>12- "+str(FirstListDisp[11][1])+" - <CH>"+str(FirstListDisp[11][2])+""
            +"<br><p align='left'><BL>13- "+str(FirstListDisp[12][1])+" - <CH>"+str(FirstListDisp[12][2])+""
            +"<br><p align='left'><BL>14- "+str(FirstListDisp[13][1])+" - <CH>"+str(FirstListDisp[13][2])+""
            +"<br><p align='left'><BL>15- "+str(FirstListDisp[14][1])+" - <CH>"+str(FirstListDisp[14][2]))

            fechar = "<a href='event:fechadin'>[<R>X<N>]</a>"

            this.sendMBox(fundo, 13, 32, 775, 353, "100%", "324650", "000001", 1)
            this.sendMBox(saves, 30, 113, 200, 250, "100%", "324650", "324650", 2)
            this.sendMBox(cheese, 300, 113, 200, 250, "100%", "324650", "324650", 3)
            this.sendMBox(first, 570, 113, 200, 250, "100%", "324650", "324650", 4)
            this.sendMBox(fechar, 700, 34, 52, 20, "100%", "324650", "324650", 5)
        else:
            this.sendMessage("<J>Sunucuda 15 hesap yok.")
       
    def sendMBox(this, text, x, y, width, height, alpha, bgcolor, bordercolor, boxid, fixed=True):
       p = ByteArray()
       text = str(text)
       x, y, width, height = int(x), int(y), int(width), int(height)

       alpha = str(alpha).split("%")[0]
       alpha = int(alpha)
       
       if "#" in str(bgcolor):
               bgcolor = str(bgcolor[1:])
       else:
               pass
       if "#" in str(bordercolor):
               bordercolor = str(bordercolor[1:])
       else:
               pass
       bgcolor, bordercolor = int(bgcolor, 16), int(bordercolor, 16)
       p.writeInt(int(boxid))
       p.writeUTF(text)
       p.writeShort(x)
       p.writeShort(y)
       p.writeShort(width)
       p.writeShort(height)
       p.writeInt(bgcolor)
       p.writeInt(bordercolor)
       p.writeByte(alpha)
       p.writeShort(fixed)
       
       this.sendPacket([29, 20], p.toByteArray())

    def chatEnable(this):
        this.chatdisabled = False

    def sendAnimZelda(this, type, item=0, case="", id=0):
        packet = ByteArray().writeInt(this.playerCode).writeByte(type)
        if type == 7:
            packet.writeUTF(case).writeUnsignedByte(id)
        elif type == 5:
            packet.writeUTF(case)
        else:
            packet.writeInt(item)
        this.room.sendAll(Identifiers.send.Anim_Zelda, packet.toByteArray())

    def sendAnimZeldaInventory(this, id1, id2, count):
        if id1 == 4:
            this.sendPacket([100, 67], ByteArray().writeByte(0).writeShort(id2).writeShort(count).toByteArray())
            #this.sendData("\x64C", this.put("bhh", 0, id2, count))
        this.room.sendAll([8, 44], ByteArray().writeInt(this.playerCode).writeByte(id1).writeInt(id2).toByteArray())

    def premioVillage(this, coisa):
        if coisa[0] == 1:
            medal = coisa[1]
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                if not int(medal) in this.shopBadges:
                    this.parseShop.sendUnlockedBadge(medal)
                    this.shopBadges.append(str(medal))
                    this.playerConsumables[coisa[4]] -= coisa[5]
        elif coisa[0] == 2:
            symbol = str(coisa[1])
            if not symbol in this.shamanBadges:
                if this.shamanBadges == '':
                    this.shamanBadges = [symbol]
                else:
                    test = [symbol]
                    this.shamanBadges = this.shamanBadges + test
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(6, coisa[1], 1)
        elif coisa[0] == 3:
            titles = [str(coisa[1]) + ".1"]
            title = random.choice(titles)
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                while title in this.titleList:
                    try:
                        titles.remove(title)
                        title = random.choice(titles)
                    except:
                        break
                if not title in this.titleList:
                    stitle = title.split(".")
                    this.specialTitleList = this.specialTitleList + [float(title)]
                    this.sendUnlockedTitle(stitle[0], stitle[1])

                    this.sendCompleteTitleList()
                    this.sendTitleList()
                    this.playerConsumables[coisa[4]] -= coisa[5]

        elif coisa[0] == 4:
            if this.playerConsumables[coisa[4]] >= coisa[5]:
                id = coisa[1]
                if not id in this.playerConsumables:
                    this.playerConsumables[id] = coisa[2]
                else:
                    count = this.playerConsumables[id] + coisa[2]
                    this.playerConsumables[id] = count
                this.playerConsumables[coisa[4]] -= coisa[5]
                this.sendAnimZeldaInventory(4, id, coisa[2])
        this.BotsVillage(this.botVillage)

    def BotsVillage(this, bot):
        itens = list()
        for item in this.itensBots[bot]:
            if item[0] == 1 and str(item[1]) in this.shopBadges:
                itens.append(item)
            elif item[0] == 2 and str(item[1]) in this.shamanBadges:
                itens.append(item)
            elif item[0] == 3 and float(str(item[1])+".1") in this.titleList:
                itens.append(item)
        for item in itens:
            this.itensBots[bot].remove(item)
        p = ByteArray()
        for items in this.itensBots[bot]:
            count = items[5]
            if items[4] in this.playerConsumables:
                one = 0 if this.playerConsumables[items[4]] >= count else 1
            else:
                one = 1
            #data += this.put("bbhhbhh", one, *items)
            p.writeByte(one).writeByte(items[0]).writeShort(items[1]).writeShort(items[2]).writeByte(items[3]).writeShort(items[4]).writeShort(items[5])
        this.sendPacket([26, 38], ByteArray().writeUTF(bot).writeByte(len(this.itensBots[bot])).toByteArray() + p.toByteArray())

    def checkElection(this, fur):
        this.Cursor.execute('SELECT fur from election WHERE name = ?', [this.playerName])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            pass
        else:
            if this.server.election == 0:
                this.Cursor.execute('UPDATE election SET fur = ? WHERE name = ?', [fur, this.playerName])

    def sendSelectPresidente(this):
        this.Cursor.execute('SELECT name FROM election WHERE rank = ? ORDER BY votes DESC LIMIT 1', [1])
        rrf = this.Cursor.fetchone()
        if rrf is None:
            pass
        else:
            name = rrf[0]
            this.Cursor.execute('SELECT Mayor FROM users WHERE Username = ?', [name])
            rrf2 = this.Cursor.fetchone()[0]
            votemayor, candidatar, mayor, presidente, votepresidente, addpresidente = rrf2.split("#")
            presidente = "1"
            a = "#".join([votemayor, candidatar, mayor, presidente, votepresidente, addpresidente])
            this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', [a, name])
            this.Cursor.execute('UPDATE election SET presidente = ? WHERE name = ?', [1, name])
            this.server.presidente = 1
        this.sendMessage("<J>Presidente escolhido", True)
        
    def sendSelectMayors(this):
        shop = this.server.shopList
        furs = [1]
        for item in shop:
                classes = item.split(",")
                if int(classes[0]) == 22:
                        furs.append(int(classes[1]))
        for fur in furs:
                this.Cursor.execute('SELECT name FROM election WHERE fur = ? AND rank = ? ORDER BY votes DESC LIMIT 1', [fur, 0])
                rrf = this.Cursor.fetchone()
                if rrf is None:
                    pass
                else:
                    name = rrf[0]
                    this.Cursor.execute('SELECT mayor FROM users WHERE Username = ?', [name])
                    rrf2 = this.Cursor.fetchone()[0]
                    votemayor, candidatar, mayor, presidente, votepresidente, addpresidente = rrf2.split("#")
                    mayor = "1"
                    a = "#".join([votemayor, candidatar, mayor, presidente, votepresidente, addpresidente])
                    this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', [a, name])
                    this.Cursor.execute('UPDATE election SET mayor = ? WHERE name = ?', [1, name])
                    fur = this.getLookUser(name).split(";")[0]
                    this.Cursor.execute('INSERT INTO election (name, fur, text1, text2, votes, rank, mayor, presidente) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [name, fur, "", "", 0, 1, 0, 0])
        this.server.election = 2
        this.sendMessage("<J>Prefeitos escolhidos", True)
        
    def sendResetarElection(this):
        this.Cursor.execute('DELETE FROM election WHERE rank = ?', [0])
        this.Cursor.execute('SELECT name FROM election where presidente = ?', [1])
        presidente = this.Cursor.fetchone()[0]
        this.Cursor.execute('DELETE from election WHERE name != ?', [presidente])
        this.Cursor.execute('UPDATE users SET Mayor = ? where Username != ?', ['0#0#0#0#0#0', presidente])
        this.Cursor.execute('UPDATE users SET Mayor = ? WHERE Username = ?', ['0#0#0#1#0#0', presidente])
        this.server.election = 0
        this.server.presidente = 0
        this.sendMessage("<J>Eleição resetada", True)
        
    def sendResetarPresidente(this):
        this.Cursor.execute('SELECT name FROM election where presidente = ?', [1])
        presidente = this.Cursor.fetchone()[0]
        this.Cursor.execute('DELETE FROM election where rank = ?', [1])
        this.Cursor.execute('UPDATE users SET Mayor = ? where Username = ?', ['0#0#0#0#0#0', presidente])
        this.sendMessage("<J>Presidente resetado", True)

    def sendMayor(this):
        p = ByteArray().writeByte(this.server.election)
        fur = this.playerLook.split(";")[0]
        if this.server.election == 0:
            if this.votemayor == 0:
                p.writeByte(1)
            else:
                p.writeByte(0)
                
            if this.candidatar == 0:
                p.writeByte(1)
            else:
                p.writeByte(0)
            time = "1-1"
            p.writeUTF(time)
            this.Cursor.execute('SELECT * FROM election WHERE rank = ? AND presidente = ?', [1, 1])
            rrf = this.Cursor.fetchone()
            if rrf is None:
                p.writeByte(0)
            else:
                name = rrf[0]
                text1 = rrf[2]
                text2 = rrf[3]
                votes = rrf[4]
                look = this.getLookUser(name)
                furlook = look.split(";")[0]
                p.writeByte(1)
                p.writeUTF(name)
                p.writeByte(2)
                p.writeInt(furlook)
                p.writeInt(votes)
                p.writeByte(0)
                p.writeUTF(look)
                p.writeUTF(text1)
                p.writeUTF(text2)

            this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ?', [fur, 0])
            rrfs = this.Cursor.fetchall()
            if len(rrfs) == 0:
                pass
            else:
                for rrf in rrfs:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(";")[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)
                    
            this.sendPacket([100, 80], p.toByteArray())
        elif this.server.election == 2:
            if this.isMayor == 1 and this.server.presidente == 0:
                this.sendPresidente()
            else:
                p.writeShort(0)
                time = "you like-my dick for"
                p.writeUTF(time)
                this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ? AND mayor = ?', [fur, 0, 1])
                rrf = this.Cursor.fetchone()
                nonemayor = False
                if rrf is None:
                    p.writeByte(0)
                    nonemayor = True
                else:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(";")[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)
                this.Cursor.execute('SELECT * FROM election WHERE rank = ? AND presidente = ?', [1, 1])
                rrf = this.Cursor.fetchone()
                if rrf is None:
                    p.writeByte(0)
                else:
                    name = rrf[0]
                    text1 = rrf[2]
                    text2 = rrf[3]
                    votes = rrf[4]
                    look = this.getLookUser(name)
                    furlook = look.split(";")[0]
                    p.writeByte(1)
                    p.writeUTF(name)
                    p.writeByte(1)
                    p.writeInt(furlook)
                    p.writeInt(votes)
                    p.writeByte(0)
                    p.writeUTF(look)
                    p.writeUTF(text1)
                    p.writeUTF(text2)
                
                this.sendPacket([100, 80], p.toByteArray())

    def sendPresidente(this):
        p = ByteArray().writeByte(1)        
        fur = this.playerLook.split(";")[0]
        if this.votepresidente == 0:
            p.writeByte(1)
        else:
            p.writeByte(0)
        p.writeByte(0)
        time = "you like-my dick for"
        p.writeUTF(time)
        this.Cursor.execute('SELECT * FROM election WHERE fur = ? AND rank = ? AND mayor = ?', [fur, 0, 1])
        rrf = this.Cursor.fetchone()
        nonemayor = False
        if rrf is None:
            p.writeByte(0)
            nonemayor = True
        else:
            name = rrf[0]
            text1 = rrf[2]
            text2 = rrf[3]
            votes = rrf[4]
            look = this.getLookUser(name)
            furlook = look.split(";")[0]
            p.writeByte(1)
            p.writeUTF(name)
            p.writeByte(1)
            p.writeInt(furlook)
            p.writeInt(votes)
            p.writeByte(0)
            p.writeUTF(look)
            p.writeUTF(text1)
            p.writeUTF(text2)
        this.Cursor.execute('SELECT * FROM election WHERE rank = ?', [1])
        rrfs = this.Cursor.fetchall()
        if len(rrfs) == 0:
            pass
        else:
            for rrf in rrfs:
                name = rrf[0]
                text1 = rrf[2]
                text2 = rrf[3]
                votes = rrf[4]
                look = this.getLookUser(name)
                furlook = look.split(";")[0]
                p.writeByte(1)
                p.writeUTF(name)
                p.writeByte(1)
                p.writeInt(furlook)
                p.writeInt(votes)
                p.writeByte(0)
                p.writeUTF(look)
                p.writeUTF(text1)
                p.writeUTF(text2)
                
        this.sendPacket([100, 80], p.toByteArray())

    def getLookUser(this, name):
        for room in this.server.rooms.values():
            for client in room.clients.values():
                if client.playerName == name:
                    return client.playerLook             
        this.Cursor.execute('SELECT Look FROM users WHERE Username = ?', [name])
        return this.Cursor.fetchone()[0]

    def sendInventoryConsumables(this):
        packet = ByteArray().writeShort(len(this.playerConsumables))
        for id in this.playerConsumables.items():
            packet.writeShort(id[0]).writeUnsignedByte(250 if id[1] > 250 else id[1]).writeByte(0).writeBoolean(True).writeBoolean(False if id[0] in this.server.inventory or id[0] in range(2111, 2200) else True).writeBoolean(True).writeBoolean(True).writeBoolean(True).writeBoolean(False).writeBoolean(False).writeByte(this.equipedConsumables.index(id[0]) + 1 if id[0] in this.equipedConsumables else 0)
        this.sendPacket(Identifiers.send.Inventory, packet.toByteArray())

    def updateInventoryConsumable(this, id, count):
        this.sendPacket(Identifiers.send.Update_Inventory_Consumable, ByteArray().writeShort(id).writeUnsignedByte(250 if count > 250 else count).toByteArray())

    def useInventoryConsumable(this, id):
        if id in [29, 30, 2241, 2330]:
            this.sendPacket(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())
        else:
            this.room.sendAll(Identifiers.send.Use_Inventory_Consumable, ByteArray().writeInt(this.playerCode).writeShort(id).toByteArray())

    def sendTradeResult(this, playerName, result):
        this.sendPacket(Identifiers.send.Trade_Result, ByteArray().writeUTF(playerName).writeByte(result).toByteArray())

    def sendTradeInvite(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Invite, ByteArray().writeInt(playerCode).toByteArray())

    def sendTradeStart(this, playerCode):
        this.sendPacket(Identifiers.send.Trade_Start, ByteArray().writeInt(playerCode).toByteArray())

    def tradeInvite(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None and (not this.ipAddress == player.ipAddress or this.privLevel == 10 or player.privLevel == 10) and this.privLevel != 0 and player.privLevel != 0:
            if not player.isTrade:
                if not player.room.name == this.room.name:
                    this.sendTradeResult(playerName, 3)
                elif player.isTrade:
                    this.sendTradeResult(playerName, 0)
                else:
                    this.sendLangueMessage("", "$Demande_Envoyée")
                    player.sendTradeInvite(this.playerCode)

                this.tradeName = playerName
                this.isTrade = True
            else:
                this.tradeName = playerName
                this.isTrade = True
                this.sendTradeStart(player.playerCode)
                player.sendTradeStart(this.playerCode)

    def cancelTrade(this, playerName):
        player = this.room.clients.get(playerName)
        if player != None:
            this.tradeName = ""
            this.isTrade = False
            this.tradeConsumables = {}
            this.tradeConfirm = False
            player.tradeName = ""
            player.isTrade = False
            player.tradeConsumables = {}
            player.tradeConfirm = False
            player.sendTradeResult(this.playerName, 2)

    def tradeAddConsumable(this, id, isAdd):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.playerName:
            if isAdd:
                if this.tradeConsumables.has_key(id):
                    this.tradeConsumables[id] += 1
                else:
                    this.tradeConsumables[id] = 1
            else:
                count = this.tradeConsumables[id] - 1
                if count > 0:
                    this.tradeConsumables[id] = count
                else:
                    del this.tradeConsumables[id]

            player.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(False).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Add_Consumable, ByteArray().writeBoolean(True).writeShort(id).writeBoolean(isAdd).writeByte(1).writeBoolean(False).toByteArray())

    def tradeResult(this, isAccept):
        player = this.room.clients.get(this.tradeName)
        if player != None and player.isTrade and player.tradeName == this.playerName:
            this.tradeConfirm = isAccept
            player.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(False).writeBoolean(isAccept).toByteArray())
            this.sendPacket(Identifiers.send.Trade_Confirm, ByteArray().writeBoolean(True).writeBoolean(isAccept).toByteArray())
            if this.tradeConfirm and player.tradeConfirm:
                for consumable in player.tradeConsumables.items():
                    if this.playerConsumables.has_key(consumable[0]):
                        this.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        this.playerConsumables[consumable[0]] = consumable[1]

                    count = player.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del player.playerConsumables[consumable[0]]
                        if consumable[0] in player.equipedConsumables:
                            player.equipedConsumables.remove(consumable[0])
                    else:
                        player.playerConsumables[consumable[0]] = count

                for consumable in this.tradeConsumables.items():
                    if player.playerConsumables.has_key(consumable[0]):
                        player.playerConsumables[consumable[0]] += consumable[1]
                    else:
                        player.playerConsumables[consumable[0]] = consumable[1]

                    count = this.playerConsumables[consumable[0]] - consumable[1]
                    if count <= 0:
                        del this.playerConsumables[consumable[0]]
                        if consumable[0] in this.equipedConsumables:
                            this.equipedConsumables.remove(consumable[0])
                    else:
                        this.playerConsumables[consumable[0]] = count

                player.tradeName = ""
                player.isTrade = False
                player.tradeConsumables = {}
                player.tradeConfirm = False
                player.sendPacket(Identifiers.send.Trade_Close)
                player.sendInventoryConsumables()
                this.tradeName = ""
                this.isTrade = False
                this.tradeConsumables = {}
                this.tradeConfirm = False
                this.sendPacket(Identifiers.send.Trade_Close)
                this.sendInventoryConsumables()

    def sendGiveConsumables(this, id, amount=80, limit=80):
        this.sendAnimZelda(4, id)
        this.sendNewConsumable(id, amount)
        sum = (this.playerConsumables[id] if this.playerConsumables.has_key(id) else 0) + amount
        if limit != -1 and sum > limit: sum = limit
        if this.playerConsumables.has_key(id):
            this.playerConsumables[id] = sum
            this.updateInventoryConsumable(id, sum)
        else:
            this.playerConsumables[id] = sum
            this.updateInventoryConsumable(id, sum)

    def sendNewConsumable(this, consumable, count):
        this.sendPacket(Identifiers.send.New_Consumable, ByteArray().writeByte(0).writeShort(consumable).writeShort(count).toByteArray())

    def getFullItemID(this, category, itemID):
        return itemID + 10000 + 1000 * category if (itemID >= 100) else itemID + 100 * category

    def getSimpleItemID(this, category, itemID):
        return itemID - 10000 - 1000 * category if (itemID >= 10000) else itemID - 100 * category

    def getItemInfo(this, category, itemID):
        shop = map(lambda x: map(int, x.split(",")), this.server.shopList)

        return filter(lambda x: x[0] == category and x[1] == itemID, shop)[0] + ([20] if (category != 22) else [0])

class Server(protocol.ServerFactory):
    protocol = Client
    def __init__(this):

        # Settings
        this.miceName = str(this.config("game.miceName"))
        this.isDebug = bool(int(this.config("game.debug")))
        this.adventureIMG = this.config("game.adventureIMG")
        this.lastChatID = int(this.config("ids.lastChatID"))
        this.serverURL = this.config("server.url").split(", ")
        this.adventureID = int(this.config("game.adventureID"))
        this.needToFirst = int(this.config("game.needToFirst"))
        this.lastPlayerID = int(this.config("ids.lastPlayerID"))
        this.initialCheeses = int(this.config("game.initialCheeses"))
        this.initialFraises = int(this.config("game.initialFraises"))
        this.timeEvent = int(this.config("game.timeevent"))
        this.calendarioSystem = eval(this.config("game.calendario"))
        this.calendarioCount = eval(this.config("game.calendarioCount"))
        
        this.shopList = this.configShop("shop.shopList").split(";")
        this.shamanShopList = this.configShop("shop.shamanShopList").split(";")
        this.newVisuList = eval(this.configShop("shop.visuDone"))

        this.election = int(this.config("election.election"))
        this.presidente = int(this.config("election.presidente"))
        this.electionTime = int(this.config("election.time"))

        # Integer
        this.lastGiftID = 0
        this.lastPlayerCode = 0
        this.startServer = datetime.today()

        # Nonetype
        this.rebootTimer = None
        this.rankingTimer = None

        # List
        this.loginKeys = []
        this.packetKeys = []
        this.userMuteCache = []
        this.shopPromotions = []
        this.IPTempBanCache = []
        this.IPPermaBanCache = []
        this.userTempBanCache = []
        this.userPermaBanCache = []
        this.inventory = [2224, 2236]
        this.ranking = [{}, {}, {}, {}]

        # Dict
        this.rooms = {}
        this.players = {}
        this.shopGifts = {}
        this.vanillaMaps = {}
        this.chatMessages = {}
        this.shopListCheck = {}
        this.connectedCounts = {}
        this.reports = {"names": []}
        this.shamanShopListCheck = {}
        this.statsPlayer = {"racingCount":[1500,10000,10000,10000], "survivorCount":[1000,800,20000,10000], "racingBadges":[124,125,126,127], "survivorBadges":[120,121,122,123]}
        this.hardModeTitleList = {500:213.1, 2000:214.1, 4000:215.1, 7000:216.1, 10000:217.1, 14000:218.1, 18000:219.1, 22000:220.1, 26000:221.1, 30000:222.1, 40000:223.1}
        this.divineModeTitleList = {500:324.1, 2000:325.1, 4000:326.1, 7000:327.1, 10000:328.1, 14000:329.1, 18000:330.1, 22000:331.1, 26000:332.1, 30000:333.1, 40000:334.1}
        this.shamanTitleList = {10:1.1, 100:2.1, 1000:3.1, 2000:4.1, 3000:13.1, 4000:14.1, 5000:15.1, 6000:16.1, 7000:17.1, 8000:18.1, 9000:19.1, 10000:20.1, 11000:21.1, 12000:22.1, 13000:23.1, 14000:24.1, 15000:25.1, 16000:94.1, 18000:95.1, 20000:96.1, 22000:97.1, 24000:98.1, 26000:99.1, 28000:100.1, 30000:101.1, 35000:102.1, 40000:103.1, 45000:104.1, 50000:105.1, 55000:106.1, 60000:107.1, 65000:108.1, 70000:109.1, 75000:110.1, 80000:111.1, 85000:112.1, 90000:113.1, 100000:114.1, 140000:115.1}
        this.firstTitleList = {1:9.1, 10:10.1, 100:11.1, 200:12.1, 300:42.1, 400:43.1, 500:44.1, 600:45.1, 700:46.1, 800:47.1, 900:48.1, 1000:49.1, 1100:50.1, 1200:51.1, 1400:52.1, 1600:53.1, 1800:54.1, 2000:55.1, 2200:56.1, 2400:57.1, 2600:58.1, 2800:59.1, 3000:60.1, 3200:61.1, 3400:62.1, 3600:63.1, 3800:64.1, 4000:65.1, 4500:66.1, 5000:67.1, 5500:68.1, 6000:69.1, 7000:231.1, 8000:232.1, 9000:233.1, 10000:70.1, 12000:224.1, 14000:225.1, 16000:226.1, 18000:227.1, 20000:202.1, 25000:228.1, 30000:229.1, 35000:230.1, 40000:71.1}
        this.cheeseTitleList = {5:5.1, 20:6.1, 100:7.1, 200:8.1, 300:35.1, 400:36.1, 500:37.1, 600:26.1, 700:27.1, 800:28.1, 900:29.1, 1000:30.1, 1100:31.1, 1200:32.1, 1300:33.1, 1400:34.1, 1500:38.1, 1600:39.1, 1700:40.1, 1800:41.1, 2000:72.1, 2300:73.1, 2700:74.1, 3200:75.1, 3800:76.1, 4600:77.1, 6000:78.1, 7000:79.1, 8000:80.1, 9001:81.1, 10000:82.1, 14000:83.1, 18000:84.1, 22000:85.1, 26000:86.1, 30000:87.1, 34000:88.1, 38000:89.1, 42000:90.1, 46000:91.1, 50000:92.1, 55000:234.1, 60000:235.1, 65000:236.1, 70000:237.1, 75000:238.1, 80000:93.1}
        this.shopBadges = {2227:2, 2208:3, 2202:4, 2209:5, 2228:8, 2218:10, 2206:11, 2219:12, 2229:13, 2230:14, 2231:15, 2211:19, 2232:20, 2224:21, 2217:22, 2214:23, 2212:24, 2220:25, 2223:26, 2234:27, 2203:31, 2220:32, 2236:36, 2204:40, 2239:43, 2241:44, 2243:45, 2244:48, 2207:49, 2246:52, 2247:53, 210:54, 2225:56, 2213:60, 2248:61, 2226:62, 2249:63, 2250:66, 2252:67, 2253:68, 2254:70, 2255:72, 2256:128, 2257:135, 2258:136, 2259:137, 2260:138, 2261:140, 2262:141, 2263:143, 2264:146, 2265:148, 2267:149, 2268:150, 2269:151, 2270:152, 2271:155, 2272:156, 2273:157, 2274:160, 2275:164, 2276:165, 2277:167, 2278:171, 2279:173, 2280:175, 2281:176, 2282:177, 2283:178, 2284:179, 2285:180, 2286:183, 2287:185, 2288:186, 2289:187}
        this.shopTitleList = {1:115.1, 2:116.1, 4:117.1, 6:118.1, 8:119.1, 10:120.1, 12:121.1, 14:122.1, 16:123.1, 18:124.1, 20:125.1, 22:126.1, 23:115.2, 24:116.2, 26:117.2, 28:118.2, 30:119.2, 32:120.2, 34:121.2, 36:122.2, 38:123.2, 40:124.2, 42:125.2, 44:126.2, 45:115.3, 46:116.3, 48:117.3, 50:118.3, 52:119.3, 54:120.3, 56:121.3, 58:122.3, 60:123.3, 62:124.3, 64:125.3, 66:126.3, 67:115.4, 68:116.4, 70:117.4, 72:118.4, 74:119.4, 76:120.4, 78:121.4, 80:122.4, 82:123.4, 84:124.4, 86:125.4, 88:126.4, 89:115.5, 90:116.5, 92:117.5, 94:118.5, 96:119.5, 98:120.5, 100:121.5, 102:122.5, 104:123.5, 106:124.5, 108:125.5, 110:126.5, 111:115.6, 112:116.6, 114:117.6, 116:118.6, 118:119.6, 120:120.6, 122:121.6, 124:122.6, 126:123.6, 128:124.6, 130:125.6, 132:126.6, 133:115.7, 134:116.7, 136:117.7, 138:118.7, 140:119.7, 142:120.7, 144:121.7, 146:122.7, 148:123.7, 150:124.7, 152:125.7, 154:126.7, 155:115.8, 156:116.8, 158:117.8, 160:118.8, 162:119.8, 164:120.8, 166:121.8, 168:122.8, 170:123.8, 172:124.8, 174:125.8, 176:126.8, 177:115.9, 178:116.9, 180:117.9, 182:118.9, 184:119.9, 186:120.9, 188:121.9, 190:122.9, 192:123.9, 194:124.9, 196:125.9, 198:126.9}
        this.bootcampTitleList = {1:256.1, 3:257.1, 5:258.1, 7:259.1, 10:260.1, 15:261.1, 20:262.1, 25:263.1, 30:264.1, 40:265.1, 50:266.1, 60:267.1, 70:268.1, 80:269.1, 90:270.1, 100:271.1, 120:272.1, 140:273.1, 160:274.1, 180:275.1, 200:276.1, 250:277.1, 300:278.1, 350:279.1, 400:280.1, 500:281.1, 600:282.1, 700:283.1, 800:284.1, 900:285.1, 1000:286.1, 1001:256.2, 1003:257.2, 1005:258.2, 1007:259.2, 1010:260.2, 1015:261.2, 1020:262.2, 1025:263.2, 1030:264.2, 1040:265.2, 1050:266.2, 1060:267.2, 1070:268.2, 1080:269.2, 1090:270.2, 1100:271.2, 1120:272.2, 1140:273.2, 1160:274.2, 1180:275.2, 1200:276.2, 1250:277.2, 1300:278.2, 1350:279.2, 1400:280.2, 1500:281.2, 1600:282.2, 1700:283.2, 1800:284.2, 1900:285.2, 2000:286.2, 2001:256.3, 2003:257.3, 2005:258.3, 2007:259.3, 2010:260.3, 2015:261.3, 2020:262.3, 2025:263.3, 2030:264.3, 2040:265.3, 2050:266.3, 2060:267.3, 2070:268.3, 2080:269.3, 2090:270.3, 2100:271.3, 2120:272.3, 2140:273.3, 2160:274.3, 2180:275.3, 2200:276.3, 2250:277.3, 2300:278.3, 2350:279.3, 2400:280.3, 2500:281.3, 2600:282.3, 2700:283.3, 2800:284.3, 2900:285.3, 3000:286.3, 3001:256.4, 3003:257.4, 3005:258.4, 3007:259.4, 3010:260.4, 3015:261.4, 3020:262.4, 3025:263.4, 3030:264.4, 3040:265.4, 3050:266.4, 3060:267.4, 3070:268.4, 3080:269.4, 3090:270.4, 3100:271.4, 3120:272.4, 3140:273.4, 3160:274.4, 3180:275.4, 3200:276.4, 3250:277.4, 3300:278.4, 3350:279.4, 3400:280.4, 3500:281.4, 3600:282.4, 3700:283.4, 3800:284.4, 3900:285.4, 4000:286.4, 4001:256.5, 4003:257.5, 4005:258.5, 4007:259.5, 4010:260.5, 4015:261.5, 4020:262.5, 4025:263.5, 4030:264.5, 4040:265.5, 4050:266.5, 4060:267.5, 4070:268.5, 4080:269.5, 4090:270.5, 4100:271.5, 4120:272.5, 4140:273.5, 4160:274.5, 4180:275.5, 4200:276.5, 4250:277.5, 4300:278.5, 4350:279.5, 4400:280.5, 4500:281.5, 4600:282.5, 4700:283.5, 4800:284.5, 4900:285.5, 5000:286.5, 5001:256.6, 5003:257.6, 5005:258.6, 5007:259.6, 5010:260.6, 5015:261.6, 5020:262.6, 5025:263.6, 5030:264.6, 5040:265.6, 5050:266.6, 5060:267.6, 5070:268.6, 5080:269.6, 5090:270.6, 5100:271.6, 5120:272.6, 5140:273.6, 5160:274.6, 5180:275.6, 5200:276.6, 5250:277.6, 5300:278.6, 5350:279.6, 5400:280.6, 5500:281.6, 5600:282.6, 5700:283.6, 5800:284.6, 5900:285.6, 6000:286.6, 6001:256.7, 6003:257.7, 6005:258.7, 6007:259.7, 6010:260.7, 6015:261.7, 6020:262.7, 6025:263.7, 6030:264.7, 6040:265.7, 6050:266.7, 6060:267.7, 6070:268.7, 6080:269.7, 6090:270.7, 6100:271.7, 6120:272.7, 6140:273.7, 6160:274.7, 6180:275.7, 6200:276.7, 6250:277.7, 6300:278.7, 6350:279.7, 6400:280.7, 6500:281.7, 6600:282.7, 6700:283.7, 6800:284.7, 6900:285.7, 7000:286.7, 7001:256.8, 7003:257.8, 7005:258.8, 7007:259.8, 7010:260.8, 7015:261.8, 7020:262.8, 7025:263.8, 7030:264.8, 7040:265.8, 7050:266.8, 7060:267.8, 7070:268.8, 7080:269.8, 7090:270.8, 7100:271.8, 7120:272.8, 7140:273.8, 7160:274.8, 7180:275.8, 7200:276.8, 7250:277.8, 7300:278.8, 7350:279.8, 7400:280.8, 7500:281.8, 7600:282.8, 7700:283.8, 7800:284.8, 7900:285.8, 8000:286.8, 8001:256.9, 8003:257.9, 8005:258.9, 8007:259.9, 8010:260.9, 8015:261.9, 8020:262.9, 8025:263.9, 8030:264.9, 8040:265.9, 8050:266.9, 8060:267.9, 8070:268.9, 8080:269.9, 8090:270.9, 8100:271.9, 8120:272.9, 8140:273.9, 8160:274.9, 8180:275.9, 8200:276.9, 8250:277.9, 8300:278.9, 8350:279.9, 8400:280.9, 8500:281.9, 8600:282.9, 8700:283.9, 8800:284.9, 8900:285.9, 9000:286.9}

        # Files
        this.parseSWF = this.parseFile("./moduller/config/files/infoSWF.json")
        this.captchaList = this.parseFile("./moduller/config/files/captchas.json")
        this.promotions = this.parseFile("./moduller/config/files/promotions.json")
        this.serverList = this.parseFile("./moduller/config/files/serverList.json")


        # Others
        this.CursorCafe = CursorCafe
        this.parseFunctions()
        this.getVanillaMaps()
        this.parsePromotions()
        this.rankingTimer = reactor.callLater(1, this.getRanking)

    def updateConfig(this):
        this.configs("ids.lastPlayerID", str(this.lastPlayerID))
        this.configs("ids.lastChatID", str(this.lastChatID))
        this.configs("game.timeevent", str(this.timeEvent))
        this.configs("election.election", str(this.election))
        this.configs("election.presidente", str(this.presidente))
        this.configs("election.time", str(this.electionTime))

    def getPointsColor(this, playerName, aventure, itemID, itemType, itemNeeded):
        for client in this.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    if client.aventureCounts[int(itemID)][1] >= int(itemNeeded):
                        return 1
        return 0

    def getAventureCounts(this, playerName, aventure, itemID, itemType):
        for client in this.players.values():
            if client.playerName == playerName:
                if int(itemID) in client.aventureCounts.keys():
                    return client.aventureCounts[int(itemID)][1]
        return 0

    def getAventureItems(this, playerName, aventure, itemType, itemID):
        c = 0
        for client in this.players.values():
            if client.playerName == playerName:
                if aventure == 24:
                    if itemType == 0 and itemID == 1:
                        return client.aventureSaves
                    elif itemType == 0 and itemID == 2:
                        for item in client.aventureCounts.keys():
                            if item in range(38, 44):
                                c += client.aventureCounts[item][1]
                        return c
        return 0
        
    def parseFunctions(this):
        # SWF
        data = this.parseSWF
        this.CKEY = data["key"]
        this.Version = data["version"]

        keys = data["packetKeys"]
        i = 0
        while i < len(keys):
            this.packetKeys.append(keys[i])
            i += 1

        login = data["loginKeys"]
        i = 0
        while i < len(login):
            this.loginKeys.append(login[i])
            i += 1

        # Shop
        for item in this.shopList:
            values = item.split(",")
            this.shopListCheck[values[0] + "|" + values[1]] = [int(values[5]), int(values[6])]

        for item in this.shamanShopList:
            values = item.split(",")
            this.shamanShopListCheck[values[0]] = [int(values[3]), int(values[4])]

        # DB
        Cursor.execute("select ip from IPPermaBan")
        rs = Cursor.fetchone()
        if rs:
            this.IPPermaBanCache.append(rs["ip"])

        Cursor.execute("select Username from UserPermaBan")
        rs = Cursor.fetchone()
        if rs:
            this.userPermaBanCache.append(rs["Username"])

        Cursor.execute("select Username from UserTempBan")
        rs = Cursor.fetchone()
        if rs:
            this.userTempBanCache.append(rs["Username"])

        Cursor.execute("select Username from UserTempMute")
        rs = Cursor.fetchone()
        if rs:
            this.userMuteCache.append(rs["Username"])

    def config(this, setting):
        return config.get("configGame", setting, 0)

    def configShop(this, setting):
        return config.get("configShop", setting, 0)

    def configs(this, setting, value):
        config.set("configGame", setting, value)
        with open("./moduller/config/configs.properties", "w") as f:
            config.write(f)

    def parseFile(this, directory):
        with open(directory, "r") as f:
            return eval(f.read())

    def updateBlackList(this):
        with open("./moduller/config/files/serverList.json", "w") as f:
            json.dump(this.serverList, f)

    def getVanillaMaps(this):
        for fileName in os.listdir("./moduller/config/maps/vanilla"):
            with open("./moduller/config/maps/vanilla/"+fileName) as f:
                this.vanillaMaps[int(fileName[:-4])] = f.read()

    def closeServer(this):
        this.updateConfig()
        for client in this.players.values():
            client.updateDatabase()
            client.transport.loseConnection()
            del this.players[client.playerName]

        os._exit(0)

    def sendServerRestart(this, no, sec):
        if sec > 0 or no != 5:
            this.sendServerRestartSEC(120 if no == 0 else 60 if no == 1 else 30 if no == 2 else 20 if no == 3 else 10 if no == 4 else sec)
            if this.rebootTimer != None: this.rebootTimer.cancel()
            this.rebootTimer = reactor.callLater(60 if no == 0 else 30 if no == 1 else 10 if no == 2 or no == 3 else 1, lambda: this.sendServerRestart(no if no == 5 else no + 1, 9 if no == 4 else sec - 1 if no == 5 else 0))

    def sendServerRestartSEC(this, seconds):
        this.sendPanelRestartMessage(seconds)
        this.sendWholeServer(Identifiers.send.Server_Restart, ByteArray().writeInt(seconds * 1000).toByteArray())

    def sendPanelRestartMessage(this, seconds):
        if seconds == 120:
            print "[%s] [SERVER] The server will restart in 2 minutes." %(time.strftime("%H:%M:%S"))
        elif seconds < 120 and seconds > 1:
            print "[%s] [SERVER] The server will restart in %s seconds." %(time.strftime("%H:%M:%S"), seconds)
        else:
            print "[%s] [SERVER] The server will restart in 1 second." %(time.strftime("%H:%M:%S"))
            this.updateConfig()
            for player in this.players.values():
                player.updateDatabase()
            os._exit(0)

    def buildCaptchaCode(this):
        CC = "".join([random.choice(this.captchaList.keys()) for x in range(4)])
        words, px, py, lines = list(CC), 0, 1, []
        for count in range(1, 17):
            wc, values = 1, []
            for word in words:
                ws = this.captchaList[word]
                if count > len(ws):
                    count = len(ws)
                ws = ws[str(count)]
                values += ws.split(",")[(1 if wc > 1 else 0):]
                wc += 1
            lines += [",".join(map(str, values))]
            if px < len(values):
                px = len(values)
            py += 1
        return [CC, (px + 2), 17, lines]

    def checkAlreadyExistingGuest(this, playerName):
        if not playerName: playerName = "Souris"
        if this.checkConnectedAccount(playerName):
            playerName += "_%s" %("".join([random.choice(string.ascii_lowercase) for x in range(4)]))
        return playerName

    def checkConnectedAccount(this, playerName):
        return this.players.has_key(playerName)

    def disconnectIPAddress(this, ip):
        for player in this.players.values():
            if player.ipAddress == ip:
                player.transport.loseConnection()

    def checkExistingUser(this, playerName):
        Cursor.execute("select 1 from Users where Username = ?", [playerName])
        return Cursor.fetchone() != None

    def recommendRoom(this, langue, prefix=""):
        count = 0
        result = ""
        while result == "":
            count += 1
            if this.rooms.has_key("%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)):
                if this.rooms["%s-%s" %(langue, count) if prefix == "" else "%s-%s%s" %(langue, prefix, count)].getPlayerCount() < 25:
                    result = str(count)
            else:
                result = str(count)
        return result

    def checkRoom(this, roomName, langue):
        found = False
        x = 0
        result = roomName
        if this.rooms.has_key(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName):
            room = this.rooms.get(("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName)
            if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                found = True
        else:
            found = True

        while not found:
            x += 1
            if this.rooms.has_key((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x)):
                room = this.rooms.get((("%s-%s" %(langue, roomName)) if not roomName.startswith("*") and roomName[0] != chr(3) else roomName) + str(x))
                if room.getPlayerCount() < room.maxPlayers if room.maxPlayers != -1 else True:
                    found = True
                    result += str(x)
            else:
                found = True
                result += str(x)
        return result

    def addClientToRoom(this, player, roomName):
        if this.rooms.has_key(roomName):
            this.rooms[roomName].addClient(player)
        else:
            room = Room(this, roomName)
            this.rooms[roomName] = room
            room.addClient(player, True)
            room.mapChange()

    def banPlayer(this, playerName, bantime, reason, modName, silent):        
        found = False

        player = this.players.get(playerName)
        if player != None:
            found = True
            if not modName == "Server":
                player.banHours += bantime
                Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Online', ?)", [playerName, modName, bantime, reason, int(time.time() / 10), player.ipAddress])
            else:
                this.sendStaffMessage(5, "<V>Servidor <BL>baniu o jogador <V>%s<BL> por <V>1 <BL> hora. Motivo: <V>Vote Populaire<BL>." %(playerName))

            Cursor.execute("update Users set BanHours = ?, UnRanked = 1 where Username = ?", [bantime, playerName])

            if bantime >= 361 or player.banHours >= 361:
                this.userPermaBanCache.append(playerName)
                Cursor.execute("insert into UserPermaBan values (?, ?, ?)", [playerName, reason, modName])

            if player.banHours >= 361:
                this.IPPermaBanCache.append(player.ipAddress)
                Cursor.execute("insert into IPPermaBan values (?, ?, ?)", [player.ipAddress, modName, reason])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)
                this.tempBanIP(player.ipAddress, bantime)

            if playerName in this.reports["names"]:
                this.reports[playerName]["status"] = "banned"
                this.reports[playerName]["status"] = "modname"
                this.reports[playerName]["status"] = str(bantime)
                this.reports[playerName]["banreason"] = "hack"

            player.sendPlayerBan(bantime, reason, silent)

        if not found and this.checkExistingUser(playerName) and not modName == "Server" and bantime >= 1:
            found = True
            totalBanTime = this.getTotalBanHours(playerName) + bantime
            if (totalBanTime >= 361 and bantime <= 360) or bantime >= 361:
                this.userPermaBanCache.append(playerName)
                Cursor.execute("insert into UserPermaBan values (?, ?, ?)", [playerName, reason, modName])

            if bantime >= 1 and bantime <= 360:
                this.tempBanUser(playerName, bantime, reason)

            Cursor.execute("update Users set BanHours = ?, UnRanked = 1 where Username = ?", [bantime, playerName])
            Cursor.execute("insert into BanLog values (?, ?, ?, ?, ?, 'Offline', 'Offline')", [playerName, modName, str(bantime), reason, int(time.time() / 10)])
        return found

    def checkTempBan(this, playerName):
        Cursor.execute("select 1 from UserTempBan where Username = ?", [playerName])
        return Cursor.fetchone() != None

    def removeTempBan(this, playerName):
        if playerName in this.userTempBanCache:
            this.userTempBanCache.remove(playerName)
        Cursor.execute("delete from UserTempBan where Username = ?", [playerName])

    def tempBanUser(this, playerName, bantime, reason):
        if this.checkTempBan(playerName):
            this.removeTempBan(playerName)

        this.userTempBanCache.append(playerName)
        Cursor.execute("insert into UserTempBan values (?, ?, ?)", [playerName, reason, str(Utils.getTime() + (bantime * 60 * 60))])

    def getTempBanInfo(this, playerName):
        Cursor.execute("select Reason, Time from UserTempBan where Username = ?", [playerName])
        for rs in Cursor.fetchall():
            return [rs["Reason"], rs["Time"]]
        else:
            return ["Without a reason", 0]

    def getPermBanInfo(this, playerName):
        Cursor.execute("select Reason from UserPermaBan where Username = ?", [playerName])
        for rs in Cursor.fetchall():
            return rs["Reason"]
        else:
            return "Without a reason"

    def checkPermaBan(this, playerName):
        Cursor.execute("select 1 from UserPermaBan where Username = ?", [playerName])
        return Cursor.fetchone() != None

    def removePermaBan(this, playerName):
        if playerName in this.userPermaBanCache:
            this.userPermaBanCache.remove(playerName)
        Cursor.execute("delete from UserPermaBan where Username = ?", [playerName])
        Cursor.execute("update Users set UnRanked = 0 where Username = ?", [playerName])

    def tempBanIP(this, ip, time):
        if not ip in this.IPTempBanCache:
            this.IPTempBanCache.append(ip)
            if ip in this.IPTempBanCache:
                reactor.callLater(time, lambda: this.IPTempBanCache.remove(ip))

    def getTotalBanHours(this, playerName):
        Cursor.execute("select BanHours from Users where Username = ?", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return rs["BanHours"]
        else:
            return 0

    def voteBanPopulaire(this, playerName, playerVoted, ip):
        player = this.players.get(playerName)
        if player != None and player.privLevel == 1 and not ip in player.voteBan:
            player.voteBan.append(ip)
            if len(player.voteBan) == 10:
                this.banPlayer(playerName, 1, "Vote Populaire", "Server", False)
            this.sendStaffMessage(7, "O jogador <V>%s</V> está votando contra <V>%s</V> [<R>%s</R>/10]" %(playerVoted, playerName, len(player.voteBan)))

    def muteUser(this, playerName, mutetime, reason):
        this.userMuteCache.append(playerName)
        Cursor.execute("insert into UserTempMute values (?, ?, ?)", [playerName, str(Utils.getTime() + (mutetime * 60 * 60)), reason])

    def removeModMute(this, playerName):
        if playerName in this.userMuteCache:
            this.userMuteCache.remove(playerName)
        Cursor.execute("delete from UserTempMute where Username = ?", [playerName])

    def getModMuteInfo(this, playerName):
        Cursor.execute("select Reason, Time from UserTempMute where Username = ?", [playerName])
        rs = Cursor.fetchone()
        if rs:
            return [rs["Reason"], rs["Time"]]
        else:
            return ["Without a reason", 0]

    def mutePlayer(this, playerName, hours, reason, modName):
        player = this.players.get(playerName)
        if player != None:
            this.sendStaffMessage(5, "<V>%s</V> deixou <V>%s</V> sem falar por <V>%s</V> %s pelo seguinte motivo: <V>%s</V>" %(modName, playerName, hours, "hora" if hours == 1 else "horas", reason))
            if playerName in this.userMuteCache:
                this.removeModMute(playerName)

            player.isMute = True
            player.sendModMute(playerName, hours, reason, False)
            player.sendModMute(playerName, hours, reason, True)
            this.muteUser(playerName, hours, reason)

    def desmutePlayer(this, playerName, modName):
        player = this.players.get(playerName)
        if player != None:
            this.sendStaffMessage(5, "<V>%s</V> desmutou <V>%s</V>." %(modName, playerName))
            this.removeModMute(playerName)
            player.isMute = False
				
    def getShamanType(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanType
        return 0

    def getShamanLevel(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.shamanLevel
        return 0

    def getShamanBadge(this, playerCode):
        for player in this.players.values():
            if player.playerCode == playerCode:
                return player.parseSkill.getShamanBadge()
        return 0

    def getTribeHouse(this, tribeName):
        Cursor.execute("select House from Tribe where Name = ?", [tribeName])
        rs = Cursor.fetchone()
        if rs:
            return rs["House"]
        else:
            return -1

    def getPlayerID(this, playerName):
        if playerName.startswith("*"):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].playerID
        else:
            Cursor.execute("select PlayerID from Users where Username = ?", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs["PlayerID"]
            else:
                return 0

    def getPlayerPrivlevel(this, playerName):
        if playerName.startswith("*"):
            return 0
        elif this.players.has_key(playerName):
            return this.players[playerName].privLevel
        else:
            Cursor.execute("select PrivLevel from Users where Username = ?", [playerName])
            rs = Cursor.fetchone()
            if rs:
                return rs["PrivLevel"]
            else:
                return 0

    def getPlayerName(this, playerID):
        Cursor.execute("select Username from Users where PlayerID = ?", [playerID])
        rs = Cursor.fetchone()
        if rs:
            return rs["Username"]
        else:
            return ""

    def getPlayerRoomName(this, playerName):
        if this.players.has_key(playerName):
            return this.players[playerName].roomName
        else:
            return ""

    def getPlayersCountMode(this, mode, langue):
        modeName = {1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 18: "", 16: "village"}[mode]
        playerCount = 0
        for room in this.rooms.values():
            if ((room.isNormRoom if mode == 1 else room.isVanilla if mode == 3 else room.isSurvivor if mode == 8 else room.isRacing if mode == 9 else room.isMusic if mode == 11 else room.isBootcamp if mode == 2 else room.isDefilante if mode == 10 else room.isVillage if mode == 16 else True) and room.community == langue.lower()):
                playerCount += room.getPlayerCount()
        return ["%s %s" %(this.miceName, modeName), playerCount]

    def parsePromotions(this):
        needUpdate = False
        i = 0
        while i < len(this.promotions):
            item = this.promotions[i]                
            if item[3] < 1000:
                item[3] = Utils.getTime() + item[3] * 86400 + 30
                needUpdate = True
            
            this.shopPromotions.append([item[0], item[1], item[2], item[3]])
            i += 1

        if needUpdate:
            with open("./moduller/config/files/promotions.json", "w") as f:
                json.dump(this.promotions, f)
        
        this.checkPromotionsEnd()

    def checkPromotionsEnd(this):
        needUpdate = False
        for promotion in this.shopPromotions:
            if Utils.getHoursDiff(promotion[3]) <= 0:
                this.shopPromotions.remove(promotion)
                needUpdate = True
                i = 0
                while i < len(this.promotions):
                    if this.promotions[i][0] == promotion[0] and this.promotions[i][1] == promotion[1]:
                        del this.promotions[i]
                    i += 1

        if needUpdate:
            with open("./moduller/config/files/promotions.json", "w") as f:
                json.dump(this.promotions, f)

    def sendWholeServer(this, identifiers, result):
        for player in this.players.values():
            player.sendPacket(identifiers, result)

    def checkMessage(this, message):
        message = message.lower()
        for word in this.serverList:
            if re.search("[^a-zA-Z]*".join(list(word)), message):
                return 1
        return 0

    def setVip(this, playerName, days):
        player = this.players.get(playerName)
        if ((player != None and player.privLevel == 1) or this.getPlayerPrivlevel(playerName) == 1):
            Cursor.execute("update users set VipTime = ? where Username = ?" if player != None else "update users SET VipTime = ?, PrivLevel = 2 where Username = ?", [Utils.getTime() + (days * 24 * 3600), playerName])
            if player != None:
                player.privLevel = 2

            this.sendStaffMessage(7, "<V>"+playerName+"</V> <V>"+str(days)+"</V> günlüğüne VIP oldu.")
            return True
        
        return False

    def getPlayerCode(this, playerName):
        player = this.players.get(Utils.parsePlayerName(playerName))
        return player.playerCode if player != None else 0

    def sendStaffMessage(this, minLevel, message, tab=False):
        for player in this.players.values():
            if player.privLevel >= minLevel:
                player.sendMessage(message, tab)

    def getRanking(this):
        this.rankingTimer = reactor.callLater(300, this.getRanking)
        this.rankingsList = [{}, {}, {}, {}, {}]

        Cursor.execute("select Username, FirstCount from Users where PrivLevel < 3 order by FirstCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs["Username"]
            this.rankingsList[0][count] = [playerName, this.players[playerName].firstCount if this.checkConnectedAccount(playerName) else rs["FirstCount"]]
            count += 1
        
        Cursor.execute("select Username, CheeseCount from Users where PrivLevel < 3 order by CheeseCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs["Username"]
            this.rankingsList[1][count] = [playerName, this.players[playerName].cheeseCount if this.checkConnectedAccount(playerName) else rs["CheeseCount"]]
            count += 1

        Cursor.execute("select Username, ShamanSaves from Users where PrivLevel < 3 order by ShamanSaves desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs["Username"]
            this.rankingsList[2][count] = [playerName, this.players[playerName].shamanSaves if this.checkConnectedAccount(playerName) else rs["ShamanSaves"]]
            count += 1

        Cursor.execute("select Username, BootcampCount from Users where PrivLevel < 3 order by BootcampCount desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs["Username"]
            this.rankingsList[3][count] = [playerName, this.players[playerName].bootcampCount if this.checkConnectedAccount(playerName) else rs["BootcampCount"]]
            count += 1

        Cursor.execute("select Username, Coins from Users where PrivLevel < 3 order by Coins desc limit 0, 13")
        count = 1
        for rs in Cursor.fetchall():
            playerName = rs["Username"]
            this.rankingsList[4][count] = [playerName, this.players[playerName].nowCoins if this.checkConnectedAccount(playerName) else rs["Coins"]]
            count += 1

class Room:
    def __init__(this, server, name):

        # String
        this.mapXML = ""
        this.mapName = ""
        this.EMapXML = ""
        this.roomPassword = ""
        this.forceNextMap = "-1"
        this.currentSyncName = ""
        this.currentShamanName = ""
        this.currentSecondShamanName = ""

        # Integer
        this.addTime = 0
        this.mapCode = -1
        this.cloudID = -1
        this.EMapCode = 0
        this.objectID = 0
        this.redCount = 0
        this.mapPerma = -1
        this.blueCount = 0
        this.musicTime = 0
        this.mapStatus = -1
        this.mapNoVotes = 0
        this.currentMap = 0
        this.receivedNo = 0
        this.EMapLoaded = 0
        this.roundTime = 120
        this.mapYesVotes = 0
        this.receivedYes = 0
        this.roundsCount = -1
        this.maxPlayers = 200
        this.numCompleted = 0
        this.numGetCheese = 0
        this.companionBox = -1
        this.gameStartTime = 0
        this.lastRoundCode = 0
        this.FSnumCompleted = 0
        this.SSnumCompleted = 0
        this.musicSkipVotes = 0
        this.forceNextShaman = -1
        this.currentSyncCode = -1
        this.changeMapAttemps = 0
        this.currentShamanCode = -1
        this.currentShamanType = -1
        this.mulodromeRoundCount = 0
        this.gameStartTimeMillis = 0
        this.currentSecondShamanCode = -1
        this.currentSecondShamanType = -1

        # Bool
        this.isMusic = False
        this.isClosed = False
        this.noShaman = False
        this.isEditor = False
        this.isRacing = False
        this.isSnowing = False
        this.isVillage = False
        this.isVanilla = False
        this.is801Room = False
        this.countStats = True
        this.isFixedMap = False
        this.isNormRoom = False
        this.isTutorial = False
        this.isBootcamp = False
        this.isSurvivor = False
        this.isVotingBox = False
        this.autoRespawn = False
        this.noAutoScore = False
        this.isDoubleMap = False
        this.specificMap = False
        this.mapInverted = False
        this.isDefilante = False
        this.isMulodrome = False
        this.canChangeMap = True
        this.isVotingMode = False
        this.isTribeHouse = False
        this.isNoShamanMap = False
        this.EMapValidated = False
        this.isTotemEditor = False
        this.canChangeMusic = True
        this.initVotingMode = True
        this.disableAfkKill = False
        this.isPlayingMusic = False
        this.noShamanSkills = False
        this.isSurvivorVamp = False
        this.never20secTimer = False
        this.isTribeHouseMap = False
        this.changed20secTimer = False
        this.catchTheCheeseMap = False
        this.isDeathmatch = False
        this.canCannon = False
        this.isUtility = False
        this.discoRoom = False

        # Bool
        this.killAfkTimer = None
        this.endSnowTimer = None
        this.changeMapTimer = None
        this.voteCloseTimer = None
        this.startTimerLeft = None
        this.autoRespawnTimer = None
        this.contagemDeath = None

        # List Arguments
        this.anchors = []
        this.redTeam = []
        this.blueTeam = []
        this.roomTimers = []
        this.musicVideos = []
        this.lastHandymouse = [-1, -1]
        this.noShamanMaps = [7, 8, 14, 22, 23, 28, 29, 54, 55, 57, 58, 59, 60, 61, 70, 77, 78, 87, 88, 92, 122, 123, 124, 125, 126, 1007, 888, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.mapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
        this.adminsRoom = []
        this.playersBan = []
        
        # Dict
        this.clients = {}
        this.currentTimers = {}
        this.currentShamanSkills = {}
        this.currentSecondShamanSkills = {}

        # Others
        this.name = name
        this.server = server
        this.CursorMaps = CursorMaps

        if this.name.startswith("*"):
            this.community = "xx"
            this.roomName = this.name
        else:
            this.community = this.name.split("-")[0].lower()
            this.roomName = this.name.split("-")[1]

        roomNameCheck = this.roomName[1:] if this.roomName.startswith("*") else this.roomName
        if this.roomName.startswith("\x03[Editeur] "):
            this.countStats = False
            this.isEditor = True
            this.never20secTimer = True

        elif this.roomName.startswith("\x03[Tutorial] "):
            this.countStats = False
            this.currentMap = 900
            this.specificMap = True
            this.noShaman = True
            this.never20secTimer = True
            this.isTutorial = True

        elif this.roomName.startswith("\x03[Totem] "):
            this.countStats = False
            this.specificMap = True
            this.currentMap = 444
            this.isTotemEditor = True
            this.never20secTimer = True

        elif this.roomName.startswith("*\x03"):
            this.countStats = False
            this.isTribeHouse = True
            this.autoRespawn = True
            this.never20secTimer = True
            this.noShaman = True
            this.disableAfkKill = True
            this.isFixedMap = True
            this.roundTime = 0

        elif roomNameCheck.startswith("music"):
            this.isMusic = True

        elif roomNameCheck.startswith("racing"):
            this.isRacing = True
            this.noShaman = True
            this.noAutoScore = False
            this.roundTime = 63

        elif roomNameCheck.startswith("bootcamp"):
            this.isBootcamp = True
            this.countStats = False
            this.roundTime = 360
            this.never20secTimer = True
            this.autoRespawn = True
            this.noShaman = True

        elif roomNameCheck.startswith("vanilla"):
            this.isVanilla = True

        elif roomNameCheck.startswith("survivor"):
            this.isSurvivor = True
            this.roundTime = 90

        elif this.roomName.startswith("#deathmatch"):
            this.isDeathmatch = True
            this.roundTime = 90
            this.noShaman = True

        elif this.roomName.startswith("#utility"):
            this.isUtility = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True

        elif roomNameCheck.startswith("defilante"):
            this.isDefilante = True
            this.noShaman = True
            this.countStats = False
            this.noAutoScore = False

        elif roomNameCheck.startswith("801") or roomNameCheck.startswith("village"):
            if roomNameCheck.startswith("village"):
                this.isVillage = True
            else:
                this.is801Room = True
            this.roundTime = 0
            this.never20secTimer = True
            this.autoRespawn = True
            this.countStats = False
            this.noShaman = True
            this.isFixedMap = True
            this.disableAfkKill = True
        else:
            this.isNormRoom = True
        this.mapChange()

    def addTextPopUpStaff(this, id, type, text, targetPlayer, x, y, width):
        p = ByteArray().writeInt(id).writeByte(type).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeByte(4)
        if targetPlayer == '':
            this.sendAll([29, 23], p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket([29, 23], p.toByteArray())
        return


    def startTimer(this):
        for player in this.clients.values():
            player.sendMapStartTimer(False)

    def mapChange(this):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()

        for room in this.server.rooms.values():
            for playerCode, client in room.clients.items():
                if this.isDeathmatch:
                    if not this.contagemDeath is None:
                        this.contagemDeath.cancel()
        
        if not this.canChangeMap:
            this.changeMapAttemps += 1
            if this.changeMapAttemps < 5:
                this.changeMapTimer = reactor.callLater(1, this.mapChange)
                return

        for timer in this.roomTimers:
            timer.cancel()

        this.roomTimers = []

        for timer in [this.voteCloseTimer, this.killAfkTimer, this.autoRespawnTimer, this.startTimerLeft]:
            if timer != None:
                timer.cancel()

        if this.initVotingMode:
            if not this.isVotingBox and (this.mapPerma == 0 and this.mapCode != -1) and this.getPlayerCount() >= 2:
                this.isVotingMode = True
                this.isVotingBox = True
                this.voteCloseTimer = reactor.callLater(8, this.closeVoting)
                for player in this.clients.values():
                    player.sendPacket(Identifiers.old.send.Vote_Box, [this.mapName, this.mapYesVotes, this.mapNoVotes])
            else:
                this.votingMode = False
                this.closeVoting()

        elif this.isTribeHouse and this.isTribeHouseMap:
            pass
        else:
            if this.isVotingMode:
                TotalYes = this.mapYesVotes + this.receivedYes
                TotalNo = this.mapNoVotes + this.receivedNo
                isDel = False

                if TotalYes + TotalNo >= 100:
                    TotalVotes = TotalYes + TotalNo
                    Rating = (1.0 * TotalYes / TotalNo) * 100
                    rate = str(Rating).split(".")
                    if int(rate[0]) < 50:
                        isDel = True
                CursorMaps.execute("update Maps set YesVotes = ?, NoVotes = ?, Perma = 44 where Code = ?" if isDel else "update Maps set YesVotes = ?, NoVotes = ? where Code = ?", [TotalYes, TotalNo, this.mapCode])
                this.isVotingMode = False
                this.receivedNo = 0
                this.receivedYes = 0
                for player in this.clients.values():
                    player.qualifiedVoted = False
                    player.isVoted = False

            this.initVotingMode = True
            this.lastRoundCode = (this.lastRoundCode + 1) % 127

            if this.isSurvivor:
                for player in this.clients.values():
                    if not player.isDead and (not player.isVampire if this.mapStatus == 0 else not player.isShaman):
                        if not this.noAutoScore: player.playerScore += 10

            if this.catchTheCheeseMap:
                this.catchTheCheeseMap = False
            else:
                numCom = this.FSnumCompleted - 1 if this.isDoubleMap else this.numCompleted - 1
                numCom2 = this.SSnumCompleted - 1 if this.isDoubleMap else 0
                if numCom < 0: numCom = 0
                if numCom2 < 0: numCom2 = 0

                player = this.clients.get(this.currentShamanName)
                if player != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentShamanName, numCom])
                    if not this.noAutoScore: player.playerScore = numCom
                    if numCom > 0:
                        player.parseSkill.earnExp(True, numCom)

                player2 = this.clients.get(this.currentSecondShamanName)
                if player2 != None:
                    this.sendAll(Identifiers.old.send.Shaman_Perfomance, [this.currentSecondShamanName, numCom2])
                    if not this.noAutoScore: player2.playerScore = numCom2
                    if numCom2 > 0:
                        player2.parseSkill.earnExp(True, numCom2)

            if this.getPlayerCount() >= this.server.needToFirst:
                this.giveSurvivorStats() if this.isSurvivor else this.giveRacingStats() if this.isRacing else None

            this.currentSyncCode = -1
            this.currentShamanCode = -1
            this.currentShamanType = -1
            this.currentSecondShamanCode = -1
            this.currentSecondShamanType = -1

            this.currentSyncName = ""
            this.currentShamanName = ""
            this.currentSecondShamanName = ""
            
            this.currentShamanSkills = {}
            this.currentSecondShamanSkills = {}
            
            this.changed20secTimer = False
            this.isDoubleMap = False
            this.isNoShamanMap = False
            this.FSnumCompleted = 0
            this.SSnumCompleted = 0
            this.objectID = 0
            this.numGetCheese = 0
            this.addTime = 0
            this.cloudID = -1
            this.companionBox = -1
            this.lastHandymouse = [-1, -1]
            this.isTribeHouseMap = False
            this.canChangeMusic = True
            this.canChangeMap = True
            this.changeMapAttemps = 0
            
            this.getSyncCode()
            this.anchors = []
            this.mapStatus = (this.mapStatus + 1) % 10

            this.numCompleted = 0
                
            this.currentMap = this.selectMap()
            this.checkMapXML()

            if this.currentMap in [range(44, 54), range(138, 144)] or this.mapPerma == 8 and this.getPlayerCount() >= 3:
                this.isDoubleMap = True

            if this.mapPerma in [7, 17, 42] or (this.isSurvivor and this.mapStatus == 0):
                this.isNoShamanMap = True

            if this.currentMap in range(108, 114):
                this.catchTheCheeseMap = True

            this.gameStartTime = Utils.getTime()
            this.gameStartTimeMillis = time.time()

            for player in this.clients.values():
                player.resetPlay()

            for player in this.clients.values():
                player.startPlay()

                if player.isHidden:
                    player.sendPlayerDisconnect()
					
            if not this.mapPerma == -1 and not this.mapPerma == 41 and not this.mapPerma == 45 and not this.isVillage and not this.is801Room and not this.mapCode == -1 and not this.isTribeHouse:
                CursorMaps.execute("select Time from maps where Code = ?", [this.mapCode])
                rrf = eval(CursorMaps.fetchone()[0])
                namePlayer = rrf.keys()[0]
                timePlayer = rrf[rrf.keys()[0]]
                if not this.mapPerma == -1:
                    if timePlayer == 0:
                        for player in this.clients.values():
                            player.sendMessage("<ROSE>Bu haritanın rekoru henüz kırılmamış.", True)
                    else:
                        for player in this.clients.values():
                            player.sendMessage("<FC>%s</FC> <font color='#00C0FF'>saniye'de kırılan rekor sahibi</font> <FC>%s</FC> <font color='#00C0FF'>isimli oyuncu sahiptir.</font>" % (timePlayer, namePlayer), True)
                    
            if this.getPlayerCount() >= 9999999999:
                if not this.isDefilante and not this.isSurvivor and not this.isTutorial and not this.isTotemEditor and not this.isTribeHouse and not this.isMulodrome and not this.isMusic and not this.isEditor:
                    anyone = random.choice([0, 1])
                    itemID = random.choice([7462, 7463, 7464, 7465, 7466, 7467])
                    positionY = random.randint(0, 30)
                    if itemID == 7462:
                        idI = 1
                    elif itemID == 7463:
                        idI = 2
                    elif itemID == 7464:
                        idI = 3
                    elif itemID == 7465:
                        idI = 4
                    elif itemID == 7466:
                        idI = 5
                    elif itemID == 7467:
                        idI = 6
                    for player in this.clients.values():
                        if anyone == 1:
                            p = ByteArray()
                            p.writeByte(24)
                            p.writeByte(idI)
                            p.writeShort(itemID)
                            p.writeShort(positionY)
                            p.writeShort(-100)
                            player.sendPacket([5, 51], p.toByteArray())
                        player.sendPacket([100, 101], "\x01\x01")  

            for player in this.clients.values():
                if player.pet != 0:
                    if Utils.getSecondsDiff(player.petEnd) >= 0:
                        player.pet = 0
                        player.petEnd = 0
                    else:
                        this.sendAll(Identifiers.send.Pet, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.pet).toByteArray())

            if this.isSurvivor and this.mapStatus == 0:
                reactor.callLater(5, this.sendVampireMode)

            if this.isMulodrome:
                this.mulodromeRoundCount += 1
                this.sendMulodromeRound()

                if this.mulodromeRoundCount <= 10:
                    for player in this.clients.values():
                        if player.playerName in this.blueTeam:
                            this.setNameColor(player.playerName, 0x979EFF)
                        elif player.playerName in this.redTeam:
                            this.setNameColor(player.playerName, 0xFF9396)
                else:
                    this.sendAll(Identifiers.send.Mulodrome_End)

            if this.isDeathmatch:
               this.canCannon = False
               for client in this.clients.values():
                  reactor.callLater(3, client.sendContagem)

            if this.isRacing or this.isDefilante:
                this.roundsCount = (this.roundsCount + 1) % 10
                player = this.clients.get(this.getHighestScore())
                this.sendAll(Identifiers.send.Rounds_Count, ByteArray().writeByte(this.roundsCount).writeInt(player.playerCode if player != None else 0).toByteArray())
                if this.roundsCount == 9:
                    for client in this.clients.values():
                        client.playerScore = 0
                        
            this.startTimerLeft = reactor.callLater(3, this.startTimer)
            if not this.isFixedMap and not this.isTribeHouse and not this.isTribeHouseMap:
                this.changeMapTimer = reactor.callLater(this.roundTime + this.addTime, this.mapChange)
            
            this.killAfkTimer = reactor.callLater(30, this.killAfk)
            if this.autoRespawn or this.isTribeHouseMap:
                this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def getPlayerCount(this):
        return len(filter(lambda player: not player.isHidden, this.clients.values()))

    def getPlayerCountUnique(this):
        ipList = []
        for player in this.clients.values():
            if not player.ipAddress in ipList:
                ipList.append(player.ipAddress)
        return len(ipList)

    def getPlayerList(this):
        result = []
        for player in this.clients.values():
            if not player.isHidden:
                result.append(player.getPlayerData())
        return result

    def addClient(this, player, newRoom=False):
        this.clients[player.playerName] = player

        player.room = this
        if not newRoom:
            player.isDead = True
            this.sendAllOthers(player, Identifiers.old.send.Player_Respawn, [player.getPlayerData()])
            player.startPlay()

    def removeClient(this, player):
        if player.playerName in this.clients:
            del this.clients[player.playerName]
            player.resetPlay()
            player.isDead = True
            player.playerScore = 0
            player.sendPlayerDisconnect()

            if this.isMulodrome:
                if player.playerName in this.redTeam: this.redTeam.remove(player.playerName)
                if player.playerName in this.blueTeam: this.blueTeam.remove(player.playerName)

                if len(this.redTeam) == 0 and len(this.blueTeam) == 0:
                    this.mulodromeRoundCount = 10
                    this.sendMulodromeRound()

            if len(this.clients) == 0:
                for timer in [this.autoRespawnTimer, this.changeMapTimer, this.endSnowTimer, this.killAfkTimer, this.voteCloseTimer]:
                    if timer != None:
                        timer.cancel()
                        
                del this.server.rooms[this.name]
            else:
                if player.playerCode == this.currentSyncCode:
                    this.currentSyncCode = -1
                    this.currentSyncName = ""
                    this.getSyncCode()
                this.checkChangeMap()

    def checkChangeMap(this):
        if (not (this.isBootcamp or this.autoRespawn or this.isTribeHouse and this.isTribeHouseMap or this.isFixedMap)):
            alivePeople = filter(lambda player: not player.isDead, this.clients.values())
            if not alivePeople:
                this.mapChange()

    def sendMessage(this, message1, message2, AP, *args):
        for player in this.clients.values():
            if player.playerName != AP:
                player.sendLangueMessage(message1, message2, *args)

    def sendAll(this, identifiers, packet=""):
        for player in this.clients.values():
            player.sendPacket(identifiers, packet)

    def sendAllOthers(this, senderClient, identifiers, packet=""):
        for player in this.clients.values():
            if not player == senderClient:
                player.sendPacket(identifiers, packet)

    def sendAllChat(this, playerCode, playerName, message, langueID, isOnly, renk):
        if renk:
            message = '<font color="%s">%s</font>' % (renk, message)
        packet = ByteArray().writeInt(playerCode).writeUTF(playerName).writeByte(langueID).writeUTF(message)
        if not isOnly:
            for player in this.clients.values():
                if not playerName in player.ignoredsList:
                    player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
        else:
            player = this.clients.get(playerName)
            if player != None:
                player.sendPacket(Identifiers.send.Chat_Message, packet.toByteArray())
            this.server.sendStaffMessage(7, "<V>%s</R> karalisteden bir kelime yazdı: [<R>%s</R>]." %(playerName, message))

    def getSyncCode(this):
        if this.getPlayerCount() > 0:
            if this.currentSyncCode == -1:
                player = random.choice(this.clients.values())
                this.currentSyncCode = player.playerCode
                this.currentSyncName = player.playerName
        else:
            if this.currentSyncCode == -1:
                this.currentSyncCode = 0
                this.currentSyncName = ""
        return this.currentSyncCode

    def selectMap(this):
        if not this.forceNextMap == "-1":
            force = this.forceNextMap
            this.forceNextMap = "-1"
            this.mapCode = -1

            if force.isdigit():
                return this.selectMapSpecificic(force, "Vanilla")
            elif force.startswith("@"):
                return this.selectMapSpecificic(force[1:], "Custom")
            elif force.startswith("#"):
                return this.selectMapSpecificic(force[1:], "Perm")
            elif force.startswith("<"):
                return this.selectMapSpecificic(force, "Xml")
            else:
                return 0

        elif this.specificMap:
            this.mapCode = -1
            return this.currentMap
        else:
            if this.isEditor:
                return this.EMapCode

            elif this.isTribeHouse:
                tribeName = this.roomName[2:]
                runMap = this.server.getTribeHouse(tribeName)

                if runMap == 0:
                    this.mapCode = 0
                    this.mapName = "Scrain"
                    this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                    this.mapYesVotes = 0
                    this.mapNoVotes = 0
                    this.mapPerma = 22
                    this.mapInverted = False
                else:
                    run = this.selectMapSpecificic(runMap, "Custom")
                    if run != -1:
                        this.mapCode = 0
                        this.mapName = "Scrain"
                        this.mapXML = "<C><P /><Z><S><S Y=\"360\" T=\"0\" P=\"0,0,0.3,0.2,0,0,0,0\" L=\"800\" H=\"80\" X=\"400\" /></S><D><P Y=\"0\" T=\"34\" P=\"0,0\" X=\"0\" C=\"719b9f\" /><T Y=\"320\" X=\"49\" /><P Y=\"320\" T=\"16\" X=\"224\" P=\"0,0\" /><P Y=\"319\" T=\"17\" X=\"311\" P=\"0,0\" /><P Y=\"284\" T=\"18\" P=\"1,0\" X=\"337\" C=\"57703e,e7c3d6\" /><P Y=\"284\" T=\"21\" X=\"294\" P=\"0,0\" /><P Y=\"134\" T=\"23\" X=\"135\" P=\"0,0\" /><P Y=\"320\" T=\"24\" P=\"0,1\" X=\"677\" C=\"46788e\" /><P Y=\"320\" T=\"26\" X=\"588\" P=\"1,0\" /><P Y=\"193\" T=\"14\" P=\"0,0\" X=\"562\" C=\"95311e,bde8f3,faf1b3\" /></D><O /></Z></C>"
                        this.mapYesVotes = 0
                        this.mapNoVotes = 0
                        this.mapPerma = 22
                        this.mapInverted = False

            elif this.is801Room or this.isVillage:
                return 801

            elif this.isVanilla:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                map = random.choice(this.mapList)
                while map == this.currentMap:
                    map = random.choice(this.mapList)
                return map
                
            else:
                this.mapCode = -1
                this.mapName = "Invalid";
                this.mapXML = "<C><P /><Z><S /><D /><O /></Z></C>"
                this.mapYesVotes = 0
                this.mapNoVotes = 0
                this.mapPerma = -1
                this.mapInverted = False
                return this.selectMapStatus()
        return -1

    def selectMapStatus(this):
        maps = [0, -1, 4, 9, 5, 0, -1, 8, 6, 7]
        selectPerma = (17 if this.mapStatus % 2 == 0 else 7) if this.isRacing else (13 if this.mapStatus % 2 == 0 else 3) if this.isBootcamp else 18 if this.isDefilante else (11 if this.mapStatus == 0 else 10) if this.isSurvivor else 19 if this.isMusic and this.mapStatus % 2 == 0 else 41 if this.isDeathmatch else 45 if this.isUtility else 0
        isMultiple = False

        if this.isNormRoom:
            if this.mapStatus < len(maps) and maps[this.mapStatus] != -1:
                isMultiple = maps[this.mapStatus] == 0
                selectPerma = maps[this.mapStatus]
            else:
                map = random.choice(this.mapList)
                while map == this.currentMap:
                    map = random.choice(this.mapList)
                return map

        elif this.isVanilla or (this.isMusic and this.mapStatus % 2 != 0):
            map = random.choice(this.mapList)
            while map == this.currentMap:
                map = random.choice(this.mapList)
            return map

        CursorMaps.execute("select * from Maps where Code != "+ str(this.currentMap) +" and Perma = 0 or Perma = 1 order by random() limit 1" if isMultiple else "select * from Maps where Code != "+ str(this.currentMap) + " and Perma = "+ str(selectPerma) +" order by random() limit 1")
        rs = CursorMaps.fetchone()
        if rs:
           this.mapCode = rs["Code"]
           this.mapName = rs["Name"]
           this.mapXML = rs["XML"]
           this.mapYesVotes = rs["YesVotes"]
           this.mapNoVotes = rs["NoVotes"]
           this.mapPerma = rs["Perma"]
           this.mapInverted = random.randint(0, 100) > 85
        else:
           map = random.choice(this.mapList)
           while map == this.currentMap:
               map = random.choice(this.mapList)
           return map
            
        return -1
        
    def selectMapSpecificic(this, code, type):
        if type == "Vanilla":
            return int(code)

        elif type == "Custom":
            mapInfo = this.getMapInfo(int(code))
            if mapInfo[0] == None:
                return 0
            else:
                this.mapCode = int(code)
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Perm":
            mapList = []
            CursorMaps.execute("select Code from Maps where Perma = ?", [int(str(code))])
            for rs in CursorMaps.fetchall():
                mapList.append(rs["Code"])

            if len(mapList) >= 1:
                runMap = random.choice(mapList)
            else:
                runMap = 0

            if len(mapList) >= 2:
                while runMap == this.currentMap:
                    runMap = random.choice(mapList)

            if runMap == 0:
                map = random.choice(this.MapList)
                while map == this.currentMap:
                    map = random.choice(this.MapList)
                return map
            else:
                mapInfo = this.getMapInfo(runMap)
                this.mapCode = runMap
                this.mapName = str(mapInfo[0])
                this.mapXML = str(mapInfo[1])
                this.mapYesVotes = int(mapInfo[2])
                this.mapNoVotes = int(mapInfo[3])
                this.mapPerma = int(mapInfo[4])
                this.mapInverted = False
                return -1

        elif type == "Xml":
            this.mapCode = 0
            this.mapName = "#Module"
            this.mapXML = str(code)
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 22
            this.mapInverted = False
            return -1

    def getMapInfo(this, mapCode):
        mapInfo = ["", "", 0, 0, 0]
        CursorMaps.execute("select Name, XML, YesVotes, NoVotes, Perma from Maps where Code = ?", [mapCode])
        rs = CursorMaps.fetchone()
        if rs:
            mapInfo = rs["Name"], rs["XML"], rs["YesVotes"], rs["NoVotes"], rs["Perma"]
        return mapInfo

    def checkIfDeathMouse(this):
        return len(filter(lambda player: not player.isDead, this.clients.values())) <= 1

    def checkIfTooFewRemaining(this):
        return len(filter(lambda player: not player.isDead, this.clients.values())) <= 2

    def getAliveCount(this):
        return len(filter(lambda player: not player.isDead, this.clients.values()))

    def getDeathCountNoShaman(this):
        return len(filter(lambda player: not player.isShaman and not player.isDead and not player.isNewPlayer, this.clients.values()))

    def getHighestScore(this):
        playerScores = []
        playerID = 0
        for player in this.clients.values():
            playerScores.append(player.playerScore)
                    
        for player in this.clients.values():
            if player.playerScore == max(playerScores):
                playerID = player.playerCode
        return playerID

    def getSecondHighestScore(this):
        playerScores = []
        playerID = 0
        for player in this.clients.values():
            playerScores.append(player.playerScore)
        playerScores.remove(max(playerScores))

        if len(playerScores) >= 1:
            for player in this.clients.values():
                if player.playerScore == max(playerScores):
                    playerID = player.playerCode
        return playerID

    def getShamanCode(this):
        if this.currentShamanCode == -1:
            if this.currentMap in this.noShamanMaps or this.isNoShamanMap or this.noShaman:
                pass
            else:
                if this.forceNextShaman > 0:
                    this.currentShamanCode = this.forceNextShaman
                    this.forceNextShaman = 0
                else:
                    this.currentShamanCode = this.getHighestScore()

            if this.currentShamanCode == -1:
                this.currentShamanName = ""
            else:
                for player in this.clients.values():
                    if player.playerCode == this.currentShamanCode:
                        this.currentShamanName = player.playerName
                        this.currentShamanType = player.shamanType
                        this.currentShamanSkills = player.playerSkills
                        break
        return this.currentShamanCode

    def getDoubleShamanCode(this):
        if this.currentShamanCode == -1 and this.currentSecondShamanCode == -1:
            if this.forceNextShaman > 0:
                this.currentShamanCode = this.forceNextShaman
                this.forceNextShaman = 0
            else:
                this.currentShamanCode = this.getHighestScore()

            if this.currentSecondShamanCode == -1:
                this.currentSecondShamanCode = this.getSecondHighestScore()

            if this.currentSecondShamanCode == this.currentShamanCode:
                tempClient = random.choice(this.clients.values())
                this.currentSecondShamanCode = tempClient.playerCode

            for player in this.clients.values():
                if player.playerCode == this.currentShamanCode:
                    this.currentShamanName = player.playerName
                    this.currentShamanType = player.shamanType
                    this.currentShamanSkills = player.playerSkills
                    break

                if player.playerCode == this.currentSecondShamanCode:
                    this.currentSecondShamanName = player.playerName
                    this.currentSecondShamanType = player.shamanType
                    this.currentSecondShamanSkills = player.playerSkills
                    break

        return [this.currentShamanCode, this.currentSecondShamanCode]

    def closeVoting(this):
        this.initVotingMode = False
        this.isVotingBox = False
        if this.voteCloseTimer != None: this.voteCloseTimer.cancel()
        this.mapChange()

    def killShaman(this):
        for player in this.clients.values():
            if player.playerCode == this.currentShamanCode:
                player.isDead = True
                player.sendPlayerDied()
        this.checkChangeMap()

    def killAfk(this):
        if this.isEditor or this.isTotemEditor or this.isBootcamp or this.isTribeHouseMap or this.disableAfkKill:
            return
            
        if ((Utils.getTime() - this.gameStartTime) < 32 and (Utils.getTime() - this.gameStartTime) > 28):
            for player in this.clients.values():
                if not player.isDead and player.isAfk:
                    player.isDead = True
                    if not this.noAutoScore: player.playerScore += 1
                    player.sendPlayerDied()
            this.checkChangeMap()

    def checkIfDoubleShamansAreDead(this):
        player1 = this.clients.get(this.currentShamanName)
        player2 = this.clients.get(this.currentSecondShamanName)
        return (False if player1 == None else player1.isDead) and (False if player2 == None else player2.isDead)

    def checkIfShamanIsDead(this):
        player = this.clients.get(this.currentShamanName)
        return False if player == None else player.isDead

    def checkIfShamanCanGoIn(this):
        for player in this.clients.values():
            if player.playerCode != this.currentShamanCode and player.playerCode != this.currentSecondShamanCode and not player.isDead:
                return False
        return True

    def giveShamanSave(this, shamanName, type):
        if not this.countStats:
            return

        player = this.clients.get(shamanName)
        if player != None:
            if type == 0:
                player.shamanSaves += 1
            elif type == 1:
                player.hardModeSaves += 1
            elif type == 2:
                player.divineModeSaves += 1
            if player.privLevel != 0:
                counts = [player.shamanSaves, player.hardModeSaves, player.divineModeSaves]
                titles = [this.server.shamanTitleList, this.server.hardModeTitleList, this.server.divineModeTitleList]
                rebuilds = ["shaman", "hardmode", "divinemode"]
                if titles[type].has_key(counts[type]):
                    title = titles[type][counts[type]]
                    player.checkAndRebuildTitleList(rebuilds[type])
                    player.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
                    player.sendCompleteTitleList()
                    player.sendTitleList()

    def respawnMice(this):
        for player in this.clients.values():
            if player.isDead:
                player.isDead = False
                player.playerStartTimeMillis = time.time()
                this.sendAll(Identifiers.old.send.Player_Respawn, [player.getPlayerData(), 0 if this.isBootcamp and this.isUtility else 1])

        if this.autoRespawn or this.isTribeHouseMap:
            this.autoRespawnTimer = reactor.callLater(2, this.respawnMice)

    def respawnSpecific(this, playerName):
        player = this.clients.get(playerName)
        if player != None and player.isDead:
            player.resetPlay()
            player.isAfk = False
            player.playerStartTimeMillis = time.time()
            this.sendAll(Identifiers.old.send.Player_Respawn, [player.getPlayerData(), 0 if this.isBootcamp else 1])

    def sendMulodromeRound(this):
        this.sendAll(Identifiers.send.Mulodrome_Result, ByteArray().writeByte(this.mulodromeRoundCount).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
        if this.mulodromeRoundCount > 10:
            this.sendAll(Identifiers.send.Mulodrome_End)
            this.sendAll(Identifiers.send.Mulodrome_Winner, ByteArray().writeByte(2 if this.blueCount == this.redCount else (1 if this.blueCount < this.redCount else 0)).writeShort(this.blueCount).writeShort(this.redCount).toByteArray())
            this.isMulodrome = False
            this.mulodromeRoundCount = 0
            this.redCount = 0
            this.blueCount = 0
            this.redTeam = []
            this.blueTeam = []
            this.isRacing = False
            this.never20secTimer = False
            this.noShaman = False

    def checkMapXML(this):
        if int(this.currentMap) in this.server.vanillaMaps:
            this.mapCode = int(this.currentMap)
            this.mapName = "_Village" if this.mapCode == 801 else "EpicMice" 
            this.mapXML = str(this.server.vanillaMaps[int(this.currentMap)])
            this.mapYesVotes = 0
            this.mapNoVotes = 0
            this.mapPerma = 41
            this.currentMap = -1
            this.mapInverted = False

    def sendVampireMode(this):
        player = this.clients.get(this.currentSyncName)
        if player != None:
            player.sendVampireMode(False)

    def bindKeyBoard(this, playerName, key, down, yes):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Key_Board, ByteArray().writeShort(key).writeBoolean(down).writeBoolean(yes).toByteArray())

    def addPhysicObject(this, id, x, y, bodyDef):
        this.sendAll(Identifiers.send.Add_Physic_Object, ByteArray().writeShort(id).writeBoolean(bool(bodyDef["dynamic"]) if bodyDef.has_key("dynamic") else False).writeByte(int(bodyDef["type"]) if bodyDef.has_key("type") else 0).writeShort(x).writeShort(y).writeShort(int(bodyDef["width"]) if bodyDef.has_key("width") else 0).writeShort(int(bodyDef["height"]) if bodyDef.has_key("height") else 0).writeBoolean(bool(bodyDef["foreground"]) if bodyDef.has_key("foreground") else False).writeShort(int(bodyDef["friction"]) if bodyDef.has_key("friction") else 0).writeShort(int(bodyDef["restitution"]) if bodyDef.has_key("restitution") else 0).writeShort(int(bodyDef["angle"]) if bodyDef.has_key("angle") else 0).writeBoolean(bodyDef.has_key("color")).writeInt(int(bodyDef["color"]) if bodyDef.has_key("color") else 0).writeBoolean(bool(bodyDef["miceCollision"]) if bodyDef.has_key("miceCollision") else True).writeBoolean(bool(bodyDef["groundCollision"]) if bodyDef.has_key("groundCollision") else True).writeBoolean(bool(bodyDef["fixedRotation"]) if bodyDef.has_key("fixedRotation") else False).writeShort(int(bodyDef["mass"]) if bodyDef.has_key("mass") else 0).writeShort(int(bodyDef["linearDamping"]) if bodyDef.has_key("linearDamping") else 0).writeShort(int(bodyDef["angularDamping"]) if bodyDef.has_key("angularDamping") else 0).writeBoolean(False).writeUTF("").toByteArray())

    def removeObject(this, objectId):
        this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(objectId).writeBoolean(True).toByteArray())

    def movePlayer(this, playerName, xPosition, yPosition, pOffSet, xSpeed, ySpeed, sOffSet):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Move_Player, ByteArray().writeShort(xPosition).writeShort(yPosition).writeBoolean(pOffSet).writeShort(xSpeed).writeShort(ySpeed).writeBoolean(sOffSet).toByteArray())

    def setNameColor(this, playerName, color):
        if this.clients.has_key(playerName):
            this.sendAll(Identifiers.send.Set_Name_Color, ByteArray().writeInt(this.clients.get(playerName).playerCode).writeInt(color).toByteArray())

    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBoolean(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def bindMouse(this, playerName, yes):
        player = this.clients.get(playerName)
        if player != None:
            player.sendPacket(Identifiers.send.Bind_Mouse, ByteArray().writeBoolean(yes).toByteArray())
			
    def addTextArea(this, id, text, targetPlayer, x, y, width, height, backgroundColor, borderColor, backgroundAlpha, fixedPos):
        p = ByteArray().writeInt(id).writeUTF(text).writeShort(x).writeShort(y).writeShort(width).writeShort(height).writeInt(backgroundColor).writeInt(borderColor).writeByte(100 if backgroundAlpha > 100 else backgroundAlpha).writeBool(fixedPos)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Add_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Add_Text_Area, p.toByteArray())

    def removeTextArea(this, id, targetPlayer):
        p = ByteArray().writeInt(id)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Remove_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Remove_Text_Area, p.toByteArray())

    def updateTextArea(this, id, text, targetPlayer):
        p = ByteArray().writeInt(id).writeUTF(text)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Update_Text_Area, p.toByteArray())
        else:
            client = this.clients.get(targetPlayer)
            if client != None:
                client.sendPacket(Identifiers.send.Update_Text_Area, p.toByteArray())

    def showColorPicker(this, id, targetPlayer, defaultColor, title):
        packet = ByteArray().writeInt(id).writeInt(defaultColor).writeUTF(title)
        if targetPlayer == "":
            this.sendAll(Identifiers.send.Show_Color_Picker, packet.toByteArray())
        else:
            player = this.clients.get(targetPlayer)
            if player != None:
                player.sendPacket(Identifiers.send.Show_Color_Picker, packet.toByteArray())

    def startSnowSchedule(this, power):
        if this.isSnowing:
            this.startSnow(0, power, False)

    def startSnow(this, millis, power, enabled):
        this.isSnowing = enabled
        this.sendAll(Identifiers.send.Snow, ByteArray().writeBoolean(enabled).writeShort(power).toByteArray())
        if enabled:
            this.endSnowTimer = reactor.callLater(millis, lambda: this.startSnowSchedule(power))

    def giveSurvivorStats(this):
        for player in this.clients.values():
            if not player.isNewPlayer:
                player.survivorStats[0] += 1
                if player.isShaman:
                    player.survivorStats[1] += 1
                    player.survivorStats[2] += this.getDeathCountNoShaman()
                elif not player.isDead:
                    player.survivorStats[3] += 1

                i = 0
                while i < 3:
                    if player.survivorStats[i] >= this.server.statsPlayer["survivorCount"][i] and not this.server.statsPlayer["survivorBadges"][i] in player.shopBadges:
                        player.parseShop.sendUnlockedBadge(this.server.statsPlayer["survivorBadges"][i])
                        player.shopBadges.append(this.server.statsPlayer["survivorBadges"][i])
                        player.parseShop.checkAndRebuildBadges()
                    i += 1

    def giveRacingStats(this):
        for player in this.clients.values():
            if not player.isNewPlayer:
                player.racingStats[0] += 1
                if player.hasCheese or player.hasEnter:
                    player.racingStats[1] += 1
                if player.hasEnter:
                    if player.currentPlace <= 3:
                        player.racingStats[2] += 1
                    if player.currentPlace == 1:
                        player.racingStats[3] += 1

                i = 0
                while i < 3:
                    if player.racingStats[i] >= this.server.statsPlayer["racingCount"][i] and not this.server.statsPlayer["racingBadges"][i] in player.shopBadges:
                        player.parseShop.sendUnlockedBadge(this.server.statsPlayer["racingBadges"][i])
                        player.shopBadges.append(this.server.statsPlayer["racingBadges"][i])
                        player.parseShop.checkAndRebuildBadges()
                    i += 1

    def send20SecRemainingTimer(this):
        if not this.changed20secTimer:
            if not this.never20secTimer and this.roundTime + (this.gameStartTime - Utils.getTime()) > 21:
                this.changed20secTimer = True
                this.changeMapTimers(20)
                for player in this.clients.values():
                    player.sendRoundTime(20)

    def changeMapTimers(this, seconds):
        if this.changeMapTimer != None: this.changeMapTimer.cancel()
        this.changeMapTimer = reactor.callLater(seconds, this.mapChange)

    def newConsumableTimer(this, code):
        this.roomTimers.append(reactor.callLater(10, lambda: this.sendAll(Identifiers.send.Remove_Object, ByteArray().writeInt(code).writeBoolean(False).toByteArray())))

if __name__ == "__main__":
    # Connection Settings
    config = ConfigParser.ConfigParser()
    config.read("./moduller/config/configs.properties")

    # Connection SQLite Players Database
    Database, Cursor = None, None
    Database = sqlite3.connect("./moduller/config/database/Transformice.db", check_same_thread = False)
    Database.text_factory = str
    Database.isolation_level = None
    Database.row_factory = sqlite3.Row
    Cursor = Database.cursor()

    # Connection SQLite Cafe Database
    DatabaseCafe, CursorCafe = None, None
    DatabaseCafe = sqlite3.connect("./moduller/config/database/Cafe.db", check_same_thread = False)
    DatabaseCafe.text_factory = str
    DatabaseCafe.isolation_level = None
    DatabaseCafe.row_factory = sqlite3.Row
    CursorCafe = DatabaseCafe.cursor()

    # Connection SQLite Maps Database
    DatabaseMaps, CursorMaps = None, None
    DatabaseMaps = sqlite3.connect("./moduller/config/database/Maps.db", check_same_thread = False)
    DatabaseMaps.text_factory = str
    DatabaseMaps.isolation_level = None
    DatabaseMaps.row_factory = sqlite3.Row
    CursorMaps = DatabaseMaps.cursor()
    
    # Connection Server
    S = Server()
    for port in [443, 44440, 44444, 5555, 3724, 6112]:
        try:
            reactor.listenTCP(port, S)
        except:
            pass
    print "[%s] %s server baslatildi." %(time.strftime("%H:%M:%S"), config.get("configGame", "game.miceName"))
    reactor.run()
