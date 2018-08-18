#coding: utf-8
import re, sys, base64, hashlib, time as _time, random as _random

# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from datetime import datetime

class ParseCommands:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.currentArgsCount = 0

    def requireNoSouris(this, playerName):
        if not playerName.startswith("*"):
            return True

    def requireArgs(this, argsCount):
        if this.currentArgsCount < argsCount:
            this.client.sendMessage("Invalid arguments.")
            return False

        return True
    
    def requireTribe(this, canUse=False, tribePerm=8):
        if (not(not this.client.tribeName == "" and this.client.room.isTribeHouse and tribePerm != -1 and this.client.tribeRanks[this.client.tribeRank].split("|")[2].split(",")[tribePerm] == "1")):
            canUse = True

    def parseCommand(this, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount
        try:
            if command in ["profil", "perfil", "profile"]:
                if this.client.privLevel >= 1:
                    this.client.sendProfile(Utils.parsePlayerName(args[0]) if len(args) >= 1 else this.client.playerName)

            elif command in ["editeur", "editor"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket(Identifiers.send.Room_Type, 1)
                    this.client.enterRoom("\x03[Editeur] %s" %(this.client.playerName))
                    this.client.sendPacket(Identifiers.old.send.Map_Editor, [])

            elif command in ["totem"]:
                if this.client.privLevel >= 1:
                    if this.client.privLevel != 0 and this.client.shamanSaves >= 0:
                        this.client.enterRoom("\x03[Totem] %s" %(this.client.playerName))

            elif command in ["sauvertotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem[0] = this.client.tempTotem[0]
                    this.client.totem[1] = this.client.tempTotem[1]
                    this.client.sendPlayerDied()
                    this.client.enterRoom(this.server.recommendRoom(this.client.langue))

            elif command in ["resettotem"]:
                if this.client.room.isTotemEditor:
                    this.client.totem = [0 , ""]
                    this.client.tempTotem = [0 , ""]
                    this.client.resetTotem = True
                    this.client.isDead = True
                    this.client.sendPlayerDied()
                    this.client.room.checkChangeMap()
       
            elif command in ["ping"]:
                if this.client.privLevel >= 1:
                    this.client.sendMessage(this.client.PInfo[2])      

            elif command in ["mousecolor", "cor"]:
                if this.client.privLevel >= 1:
                    this.client.sendPacket([29, 32], ByteArray().writeByte(0).writeShort(39).writeByte(17).writeShort(57).writeShort(-12).writeUTF("Fareniz için bir renk seçin.").toByteArray())		

            elif command in ["ban", "iban"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    silent = command == "iban"
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 100000 if (hours > 100000) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    if this.server.banPlayer(playerName, hours, reason, this.client.playerName, silent):
                        this.server.sendStaffMessage(5, "<V>%s</V> <V>%s</V> nickli kişiyi <V>%s</V> %s kullanıcıyı uzaklaştırdı. Sebep: <V>%s</V>" %(this.client.playerName, playerName, hours, "saatliğine" if hours == 1 else "saatliğine", reason))
                    else:
                        this.client.sendMessage("[%s] geçersiz kullanıcı." %(playerName))
                else:
                    playerName = Utils.parsePlayerName(args[0])
                    this.server.voteBanPopulaire(playerName, this.client.playerName, this.client.ipAddress)
                    this.client.sendBanConsideration()

            elif command in ["mute"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    time = args[1] if (argsCount >= 2) else "1"
                    reason = argsNotSplited.split(" ", 2)[2] if (argsCount >= 3) else ""
                    hours = int(time) if (time.isdigit()) else 1
                    hours = 500 if (hours > 500) else hours
                    hours = 24 if (this.client.privLevel <= 6 and hours > 24) else hours
                    this.server.mutePlayer(playerName, hours, reason, this.client.playerName)

            elif command in ["unmute"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    this.server.sendStaffMessage(5, "<V>%s</V> <V>%s</V> nickli kişinin susturma cezasını kaldırdı." %(this.client.playerName, playerName))
                    this.server.removeModMute(playerName)
                    this.client.isMute = False

            elif command in ["unban"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    found = False

                    if this.server.checkExistingUser(playerName):
                        if this.server.checkTempBan(playerName):
                            this.server.removeTempBan(playerName)
                            found = True

                        if this.server.checkPermaBan(playerName):
                            this.server.removePermaBan(playerName)
                            found = True

                        if found:
                            import time
                            this.Cursor.execute("insert into BanLog values (?, ?, '', '', ?, 'Unban', '')", [playerName, this.client.playerName, int(str(time.time())[:9])])
                            this.server.sendStaffMessage(5, "<V>%s</V> <V>%s</V> nickli kişinin banını açtı." %(this.client.playerName, playerName))

            elif command in ["playerid"]:
                if this.client.privLevel >= 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    playerID = this.server.getPlayerID(playerName)
                    this.client.sendMessage("Kullanıcının ID'si: %s %s." % (playerName, str(playerID)), True)

            elif command in ["id"]:
                if this.client.privLevel >= 10:
                    playerID = int(args[0])
                    this.requireNoSouris(playerName)
                    playerName = this.server.getPlayerName(playerID)
                    this.client.sendMessage("%s ile ilişkili nick: %s." % (str(playerID), playerName), True)
      

            elif command in ["avatar"]:
                if this.client.privLevel >= 1:
                    avatar = args[0]
                    this.Cursor.execute("update Users set PlayerID = ? where Username = ?", [avatar, this.client.playerName])
                    this.client.sendMessage("<ROSE>Yeni avatar: " + avatar + "\nProfilinizin güncellenmesi için tekrar giriş yapın.") 			

            elif command in ["chatrenk"]:
                if this.client.privLevel >= 7:
                    message = "<p align = \"center\"><font size = \"17\"><font color='#DB7700'>Chat RENK</font></p><p align=\"left\"><font size = \"12\"><br><br>"
                    message += "<font color='#878787'>/gri</font><br>"
                    message += "<font color='#FFFFFF'>/beyaz</font><br>"  
                    message += "<font color='#0000CC'>/mavi</font><br>"
                    message += "<font color='#FF0000'>/kırmızı</font><br>"
                    message += "<font color='#FE8446'>/turuncu</font><br>"
                    message += "<font color='#E3C07E'>/ten</font><br>"
                    message += "<font color='#78583A'>/kahverengi</font><br>"
                    message += "<font color='#00FFFF'>/turkuaz</font><br>"
                    message += "<font color='#735B85'>/mor</font><br>"
                    message += "<font color='#FF00CC'>/pembe</font><br>"
                    message += "<font color='#00FF00'>/yesil</font><br>"
                    message += "<font color='#000001'>/siyah</font><br>"
                    this.client.sendLogMessage(message.replace("&#", "&amp;#").replace("&lt;", "<"))

            elif command in ["beyaz"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#FFFFFF"
                    this.client.sendMessage ("<font color='#FFFFFF'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["kırmızı"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#FF0000"
                    this.client.sendMessage ("<font color='#FF0000'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["mavi"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#0000CC"
                    this.client.sendMessage ("<font color='#0000CC'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["yesil"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#00FF00"
                    this.client.sendMessage ("<font color='#00FF00'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["pembe"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#FF00CC"
                    this.client.sendMessage ("<font color='#FF00CC'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["sarı"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#FFFF00"
                    this.client.sendMessage ("<font color='#FFFF00'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["turkuaz"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#00FFFF"
                    this.client.sendMessage ("<font color='#00FFFF'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["turuncu"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#FE8446"
                    this.client.sendMessage ("<font color='#FE8446'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["ten"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#E3C07E"
                    this.client.sendMessage ("<font color='#E3C07E'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["kahverengi"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#78583A"
                    this.client.sendMessage ("<font color='#78583A'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["gri"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#878787"
                    this.client.sendMessage ("<font color='#878787'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["siyah"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#000001"
                    this.client.sendMessage ("<font color='#000001'>Yönetici Olarak Renginiz Değişti.</font>")
 
            elif command in ["mor"]:
                if this.client.privLevel >= 7:
                    this.client.chatColor = "#735B85"
                    this.client.sendMessage ("<font color='#735B85'>Yönetici Olarak Renginiz Değişti.</font>")

            elif command in ["büyüt"]:
                if this.client.privLevel >= 10:
                        playerName = Utils.parsePlayerName(args[0])
                        this.client.playerSize = 1.0 if args[1] == "off" else (15.0 if float(args[1]) > 15.0 else float(args[1]))
                        if args[1] == "off":
                            this.client.sendMessage("Tüm Oyuncular Normal Boylarına Döndü.")
                            this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(float(1)).writeBoolean(False).toByteArray())

                        elif this.client.playerSize >= float(0.1) or this.client.playerSize <= float(5.0):
                            if playerName == "*":
                                for player in this.client.room.clients.values():
                                    this.client.sendMessage("Tüm Oyuncuların Boyu Şimdi " + str(this.client.playerSize) + ".")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                            else:
                                player = this.server.players.get(playerName)
                                if player != None:
                                    this.client.sendMessage("Bu Oyuncunun Boyu " + str(this.client.playerSize) + ": <BV>" + str(player.playerName) + "</BV>")
                                    this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(player.playerCode).writeUnsignedShort(int(this.client.playerSize * 100)).writeBoolean(False).toByteArray())
                        else:
                            this.client.sendMessage("Geçersiz Boyut.")            

            elif command in ["epicyetki"]:
                if this.client.privLevel == 12:
                    playerName = Utils.parsePlayerName(args[0])
                    rank = args[1].lower()
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s</V>." %(playerName))
                    else:
                        privLevel = 12 if rank.startswith("krc") else 11 if rank.startswith("badm") else 10 if rank.startswith("gs") else 9 if rank.startswith("adm") else 8 if rank.startswith("smod") else 7 if rank.startswith("mod") else 6 if rank.startswith("map") or rank.startswith("mc") else 5 if rank.startswith("cdr") else 4 if rank.startswith("reklamc") else 3 if rank.startswith("fc") or rank.startswith("fnc") else 2 if rank.startswith("vip") else 1
                        rankName = "Kurucu" if rank.startswith("krc") else "Baş Admin" if rank.startswith("badm") else "Genel Sorumlu" if rank.startswith("gs") else "Admin" if rank.startswith("adm") else "Süper Mod" if rank.startswith("smod") else "Moderatör" if rank.startswith("mod") else "Harita Ekibi" if rank.startswith("map") or rank.startswith("mc") else "Coder" if rank.startswith("cdr") else "Reklamcı" if rank.startswith("reklamc") else "FunCorp Ekibi" if rank.startswith("dev") or rank.startswith("lua") else "Vip" if rank.startswith("vip") else "Oyuncu"
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = privLevel
                            player.titleNumber = 0
                            player.sendCompleteTitleList()
                        this.Cursor.execute("update Users set PrivLevel = ?, TitleNumber = 0, UnRanked = ? where Username = ?", [privLevel, 1 if privLevel > 5 else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> artık bir <V>%s</V>." %(playerName, rankName))

            elif command in ["np", "npp"]:
                if this.client.privLevel >= 6:
                    if len(args) == 0:
                        this.client.room.mapChange()
                    else:
                        if not this.client.room.isVotingMode:
                            code = args[0]
                            if code.startswith("@"):
                                mapInfo = this.client.room.getMapInfo(int(code[1:]))
                                if mapInfo[0] == None:
                                    this.client.sendLangueMessage("", "$CarteIntrouvable")
                                else:
                                    this.client.room.forceNextMap = code
                                    if command == "np":
                                        if this.client.room.changeMapTimer != None:
                                            this.client.room.changeMapTimer.cancel()
                                        this.client.room.mapChange()
                                    else:
                                        this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

                            elif code.isdigit():
                                this.client.room.forceNextMap = code
                                if command == "np":
                                    if this.client.room.changeMapTimer != None:
                                        this.client.room.changeMapTimer.cancel()
                                    this.client.room.mapChange()
                                else:
                                    this.client.sendLangueMessage("", "$ProchaineCarte %s" %(code))

            elif command in ["mod", "mapcrews"]:
                if this.client.privLevel >= 1:
                    staff = {}
                    staffList = "$ModoPasEnLigne" if command == "mod" else "$MapcrewPasEnLigne"
                    for player in this.server.players.values():
                        if command == "mod" and player.privLevel >= 4 and not player.privLevel == 6 or command == "mapcrews" and player.privLevel == 6:
                            if staff.has_key(player.langue.lower()):
                                names = staff[player.langue.lower()]
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                            else:
                                names = []
                                names.append(player.playerName)
                                staff[player.langue.lower()] = names
                    if len(staff) >= 1:
                        staffList = "$ModoEnLigne" if command == "mod" else "$MapcrewEnLigne"
                        for list in staff.items():
                            staffList += "<br><BL>[%s]<BV> %s" %(list[0], ("<BL>, <BV>").join(list[1]))
                    this.client.sendLangueMessage("", staffList)

            elif command in ["ls"]:
                if this.client.privLevel >= 4:
                    data = []
                    for room in this.server.rooms.values():
                        if room.name.startswith("*") and not room.name.startswith("*" + chr(3)):
                            data.append(["TOPLAM", room.name, room.getPlayerCount()])
                        elif room.name.startswith(str(chr(3))) or room.name.startswith("*" + chr(3)):
                            if room.name.startswith(("*" + chr(3))):
                                data.append(["KABİLEEVİ", room.name, room.getPlayerCount()])
                            else:
                                data.append(["ÖZEL", room.name, room.getPlayerCount()])
                        else:
                            data.append([room.community.upper(), room.roomName, room.getPlayerCount()])
                    result = "\n"
                    for roomInfo in data:
                        result += "[<J>%s<BL>] <b>%s</b> : %s\n" %(roomInfo[0], roomInfo[1], roomInfo[2])
                    result += "<font color='#00C0FF'>Toplam oyuncular/odalar: </font><J><b>%s</b><font color='#00C0FF'>/</font><J><b>%s</b>" %(len(this.server.players), len(this.server.rooms))
                    this.client.sendMessage(result)

            elif command in ["lsc"]:
                if this.client.privLevel >= 4:
                    result = {}
                    for room in this.server.rooms.values():
                        if result.has_key(room.community):
                            result[room.community] = result[room.community] + room.getPlayerCount()
                        else:
                            result[room.community] = room.getPlayerCount()

                    message = "\n"
                    for community in result.items():
                        message += "<V>%s<BL> : <J>%s\n" %(community[0].upper(), community[1])
                    message += "<V>TOPLAM<BL> : <J>%s" %(sum(result.values()))
                    this.client.sendMessage(message)

            elif command in ["skip"]:
                if this.client.privLevel >= 1 and this.client.canSkipMusic and this.client.room.isMusic and this.client.room.isPlayingMusic:
                    this.client.room.musicSkipVotes += 1
                    this.client.checkMusicSkip()
                    this.client.sendBanConsideration()

            elif command in ["election"]:
                this.client.sendMayor()

            elif command in ["selectmayors"]:
                if this.client.privLevel>=10:
                    this.client.sendSelectMayors()

            elif command in ["selectpresidente"]:
                if this.client.privLevel>=10:
                    this.client.sendSelectPresidente()
                    
            elif command in ["relection"]:
                if this.client.privLevel>=10:
                    this.client.sendResetarElection()
                    
            elif command in ["rpresidente"]:
                if this.client.privLevel>=10:
                    this.client.sendResetarPresidente()

            elif command in ["pw"]:
                if this.client.privLevel >= 1:
                    if this.client.room.roomName.startswith("*" + this.client.playerName) or this.client.room.roomName.startswith(this.client.playerName):
                        if len(args) == 0:
                            this.client.room.roomPassword = ""
                            this.client.sendLangueMessage("", "$MDP_Desactive")
                        else:
                            password = args[0]
                            this.client.room.roomPassword = password
                            this.client.sendLangueMessage("", "$Mot_De_Passe : %s" %(password))
    	

            elif command in ["duyuru", "duyuru2"]:
                if this.client.privLevel >= 12:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("<font color='#FFFF00'>[EpicMice DUYURU]</font> <N>%s" %(argsNotSplited)).toByteArray())
                    
            elif command in ["smn"]:
                if this.client.privLevel >= 9:
                    this.server.sendStaffChat(-1, this.client.langue, this.client.playerName, argsNotSplited, this.client)

            elif command in ["mshtml"]:
                if this.client.privLevel >= 9:
                    this.server.sendStaffChat(0, this.client.langue, "", argsNotSplited.replace("&#", "&amp;#").replace("&lt;", "<"), this.client)

            elif command in ["yardım", "help"]:
                if this.client.privLevel >= 1:
                    this.client.sendLogMessage(this.getCommandsList())        

            elif command in ["hide"]:
                if this.client.privLevel >= 5:
                    this.client.isHidden = True
                    this.client.sendPlayerDisconnect()
                    this.client.sendMessage("Görünmez oldunuz.")

            elif command in ["unhide"]:
                if this.client.privLevel >= 5:
                    if this.client.isHidden:
                        this.client.isHidden = False
                        this.client.enterRoom(this.client.room.name)
                        this.client.sendMessage("Tekrar görünür haldesiniz.")

            elif command in ["pwkaldir"]:
                if this.client.room.roomName.startswith("*" + this.client.Username) or this.client.room.roomName.startswith(this.client.Username):
                    this.client.room.roomPassword = ""
                    this.client.sendClientMessage("Oda Şifresi Kaldırıldı: "+this.client.room.roomName+".")

            elif command in ["reboot"]:
                if this.client.privLevel == 12:
                    this.server.sendServerRestart(0, 0)

            elif command in ["shutdown"]:
                if this.client.privLevel == 12:
                    this.server.closeServer()

            elif command in ["updatesql"]:
                if this.client.privLevel == 12:
                    for player in this.server.players.values():
                        player.updateDatabase()
                    this.server.sendStaffMessage(5, "%s veritabanını güncelledi." %(this.client.playerName))

            elif command in ["kill", "suicide", "mort", "die"]:
                if not this.client.isDead:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()
                    this.client.room.checkChangeMap()

            elif command in ["title", "titulo", "titre"]:
                if this.client.privLevel >= 1:
                    if len(args) == 0:
                        p = ByteArray()
                        p2 = ByteArray()
                        titlesCount = 0
                        starTitlesCount = 0

                        for title in this.client.titleList:
                            titleInfo = str(title).split(".")
                            titleNumber = int(titleInfo[0])
                            titleStars = int(titleInfo[1])
                            if titleStars > 1:
                                p.writeShort(titleNumber).writeByte(titleStars)
                                starTitlesCount += 1
                            else:
                                p2.writeShort(titleNumber)
                                titlesCount += 1
                        this.client.sendPacket(Identifiers.send.Titles_List, ByteArray().writeShort(titlesCount).writeBytes(p2.toByteArray()).writeShort(starTitlesCount).writeBytes(p.toByteArray()).toByteArray())

                    else:
                        titleID = args[0]
                        found = False
                        for title in this.client.titleList:
                            if str(title).split(".")[0] == titleID:
                                found = True

                        if found:
                            this.client.titleNumber = int(titleID)
                            for title in this.client.titleList:
                                if str(title).split(".")[0] == titleID:
                                    this.client.titleStars = int(str(title).split(".")[1])
                            this.client.sendPacket(Identifiers.send.Change_Title, ByteArray().writeByte(this.client.gender).writeShort(titleID).toByteArray())

            elif command in ["sy?"]:
                if this.client.privLevel >= 5:
                    this.client.sendLangueMessage("", "$SyncEnCours : [%s]" %(this.client.room.currentSyncName))

            elif command in ["sy"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.isSync = True
                        this.client.room.currentSyncCode = player.playerCode
                        this.client.room.currentSyncName = player.playerName
                        if this.client.room.mapCode != -1 or this.client.room.EMapCode != 0:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode, ""])
                        else:
                            this.client.sendPacket(Identifiers.old.send.Sync, [player.playerCode])

                        this.client.sendLangueMessage("", "$NouveauSync <V> %s" %(playerName))

            elif command in ["ch"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        if this.client.room.forceNextShaman == player:
                            this.client.sendLangueMessage("", "$PasProchaineChamane", player.playerName)
                            this.client.room.forceNextShaman = -1
                        else:
                            this.client.sendLangueMessage("", "$ProchaineChamane", player.playerName)
                            this.client.room.forceNextShaman = player

            elif re.match("p\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 6:
                    mapCode = this.client.room.mapCode
                    mapName = this.client.room.mapName
                    currentCategory = this.client.room.mapPerma
                    if mapCode != -1:
                        category = int(command[1:])
                        if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44, 45]:
                            this.server.sendStaffMessage(6, "[%s] @%s : %s -> %s" %(this.client.playerName, mapCode, currentCategory, category))
                            this.client.room.CursorMaps.execute("update Maps set Perma = ? where Code = ?", [category, mapCode])

            elif re.match("lsp\\d+(\\.\\d+)?", command):
                if this.client.privLevel >= 6:
                    category = int(command[3:])
                    if category in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 18, 19, 22, 41, 42, 44]:
                        mapList = ""
                        mapCount = 0
                        this.client.room.CursorMaps.execute("select * from Maps where Perma = ?", [category])
                        for rs in this.client.room.CursorMaps.fetchall():
                            mapCount += 1
                            yesVotes = rs["YesVotes"]
                            noVotes = rs["NoVotes"]
                            totalVotes = yesVotes + noVotes
                            if totalVotes < 1: totalVotes = 1
                            rating = (1.0 * yesVotes / totalVotes) * 100
                            mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])
                            
                        try: this.client.sendLogMessage("<font size=\"12\"><N>Há</N> <BV>%s</BV> <N>mapas</N> <V>P%s %s</V></font>" %(mapCount, category, mapList))
                        except: this.client.sendMessage("<R>Há muitos mapas e não será possível abrir.</R>")

            elif command in ["mymaps"]:
                if this.client.privLevel >= (1 if len(args) == 0 else 6):
                    playerName = this.client.playerName if len(args) == 0 else Utils.parsePlayerName(args[0])
                    mapList = ""
                    mapCount = 0

                    this.client.room.CursorMaps.execute("select * from Maps where Name = ?", [playerName])
                    for rs in this.client.room.CursorMaps.fetchall():
                        mapCount += 1
                        yesVotes = rs["YesVotes"]
                        noVotes = rs["NoVotes"]
                        totalVotes = yesVotes + noVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * yesVotes / totalVotes) * 100
                        mapList += "\n<N>%s</N> - @%s - %s - %s%s - P%s" %(rs["Name"], rs["Code"], totalVotes, str(rating).split(".")[0], "%", rs["Perma"])

                    try: this.client.sendLogMessage("<font size= \"12\"><V>%s<N>'s maps: <BV>%s %s</font>" %(playerName, mapCount, mapList))
                    except: this.client.sendMessage("<R>Há muitos mapas e não será possível abrir.</R>")

            elif command in ["info"]:
                if this.client.privLevel >= 1:
                    if this.client.room.mapCode != -1:
                        totalVotes = this.client.room.mapYesVotes + this.client.room.mapNoVotes
                        if totalVotes < 1: totalVotes = 1
                        rating = (1.0 * this.client.room.mapYesVotes / totalVotes) * 100
                        this.client.sendMessage("%s - @%s - %s - %s% - P%s" %(this.client.room.mapName, this.client.room.mapCode, totalVotes, str(rating).split(".")[0], this.client.room.mapPerma))

            elif command in ["re", "respawn"]:
                if len(args) == 0:
                    if this.client.privLevel >= 2:
                        if not this.client.canRespawn:
                            this.client.room.respawnSpecific(this.client.playerName)
                            this.client.canRespawn = True
                else:
                    if this.client.privLevel >= 7:
                        playerName = Utils.parsePlayerName(args[0])
                        if this.client.room.clients.has_key(playerName):
                            this.client.room.respawnSpecific(playerName)

            elif command in ["startsnow", "stopsnow"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    this.client.room.startSnow(1000, 60, not this.client.room.isSnowing)

            elif command in ["music", "musique"]:
                if this.client.privLevel >= 8 or this.requireTribe(True):
                    if len(args) == 0:
                        this.client.room.sendAll(Identifiers.old.send.Music, [])
                    else:
                        this.client.room.sendAll(Identifiers.old.send.Music, [args[0]])

            elif command in ["clearreports"]:
                if this.client.privLevel == 10:
                    this.server.reports = {"names": []}
                    this.server.sendStaffMessage(7, "<V>%s</V> tüm ModoPwet raporlarını sildi." %(this.client.playerName))

            elif command in ["clearcache"]:
                if this.client.privLevel == 10:
                    this.server.IPPermaBanCache = []
                    this.server.sendStaffMessage(7, "<V>%s</V> sunucunun önbelleğini temizledi." %(this.client.playerName))

            elif command in ["cleariptempban"]:
                if this.client.privLevel == 10:
                    this.server.IPTempBanCache = []
                    this.server.sendStaffMessage(7, "<V>%s</V> tüm IP banları kaldırdı." %(this.client.playerName))

            elif command in ["log"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0]) if len(args) > 0 else ""
                    logList = []
                    this.Cursor.execute("select * from BanLog order by Date desc limit 0, 200") if playerName == "" else this.Cursor.execute("select * from BanLog where Username = ? order by Date desc limit 0, 200", [playerName])
                    for rs in this.Cursor.fetchall():
                        if rs["Status"] == "Unban":
                            logList += rs["Username"], "", rs["BannedBy"], "", "", rs["Date"].ljust(13, "0")
                        else:
                            logList += rs["Username"], rs["IP"], rs["BannedBy"], rs["Time"], rs["Reason"], rs["Date"].ljust(13, "0")
                    this.client.sendPacket(Identifiers.old.send.Log, logList)

            elif command in ["move"]:
                if this.client.privLevel >= 8:
                    for player in this.client.room.clients.values():
                        player.enterRoom(argsNotSplited)

            elif command in ["nomip"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    ipList = "Kullanıcının IP geçmişi: " +playerName

                    this.Cursor.execute("select IP from loginlog where Username = ?", [playerName])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        ipList += "<br>" + rs["IP"]

                    this.client.sendMessage(ipList, True)

            elif command in ["ipnom"]:
                if this.client.privLevel >= 7:
                    ip = args[0]
                    nameList = "IP'nin kullanıcı listesi: "+ip
                    historyList = "IP Geçmişi::"
                    for player in this.server.players.values():
                        if player.ipAddress == ip:
                            nameList += "<br>" + player.playerName

                    this.Cursor.execute("select Username from loginlog where IP = ?", [ip])
                    r = this.Cursor.fetchall()
                    for rs in r:
                        historyList += "<br>" + rs["Username"]

                    this.client.sendMessage(nameList)
                    this.client.sendMessage(historyList)							

            elif command in ["settime"]:
                if this.client.privLevel >= 7:
                    time = args[0]
                    if time.isdigit():
                        iTime = int(time)
                        iTime = 5 if iTime < 5 else (32767 if iTime > 32767 else iTime)
                        for player in this.client.room.clients.values():
                            player.sendRoundTime(iTime)
                        this.client.room.changeMapTimers(iTime)

            elif command in ["changepassword"]:
                if this.client.privLevel == 12:
                    this.requireArgs(2)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    password = args[1]
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s</V>." %(playerName))
                    else:
                        this.Cursor.execute("update Users set Password = ? where Username = ?", [base64.b64encode(hashlib.sha256(hashlib.sha256(password).hexdigest() + "\xf7\x1a\xa6\xde\x8f\x17v\xa8\x03\x9d2\xb8\xa1V\xb2\xa9>\xddC\x9d\xc5\xdd\xceV\xd3\xb7\xa4\x05J\r\x08\xb0").digest()), playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> nickli kullanıcının şifresini değiştirdi." %(this.client.playerName, playerName))

                        player = this.server.players.get(playerName)
                        if player != None:
                            player.sendLangueMessage("", "$Changement_MDP_ok")

            elif command in ["playersql"]:
                if this.client.privLevel == 10:
                    playerName = Utils.parsePlayerName(args[0])
                    paramter = args[1]
                    value = args[2]
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.transport.loseConnection()

                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s</V>." %(playerName))
                    else:
                        try:
                            this.Cursor.execute("update Users set %s = ? where Username = ?" %(paramter), [value, playerName])
                            this.server.sendStaffMessage(7, "%s <V>%s</V> nickli kişinin SQL bilgilerini güncelledi. <T>%s</T> -> <T>%s</T>." %(this.client.playerName, playerName, paramter, value))
                        except:
                            this.client.sendMessage("Geçersiz parametre")

            elif command in ["clearban"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.voteBan = []
                        this.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> nickli kullanıcının tüm banlarını sildi." %(this.client.playerName, playerName))

            elif command in ["ip"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.sendMessage("<V>%s</V> : <V>%s</V>." %(playerName, player.ipAddress))

            elif command in ["kick"]:
                if this.client.privLevel >= 6:
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.room.removeClient(player)
                        player.transport.loseConnection()
                        this.server.sendStaffMessage(6, "<V>%s</V> <V>%s</V> nickli kullanıcıyı kickledi."%(this.client.playerName, playerName))
                    else:
                        this.client.sendMessage("<V>%s</V> çevrimiçi değil." %(playerName))

            elif command in ["arat", "find"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    result = ""
                    for player in this.server.players.values():
                        if playerName in player.playerName:
                            result += "\n<V>%s</V> -> <V>%s</V>" %(player.playerName, player.room.name)
                    this.client.sendMessage(result)

            elif command in ["mjoin"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    for player in this.server.players.values():
                        if playerName in player.playerName:
                            room = player.room.name
                            this.client.enterRoom(room)

            elif command in ["clearchat"]:
                if this.client.privLevel >= 5:
                    this.client.room.sendAll(Identifiers.send.Message, ByteArray().writeUTF("\n" * 300).toByteArray())

            elif command in ["sıralama"]:
                Userlist = []
                lists = "<p align='center'><font size='13'><font color='#009d9d'>Sıralama</font> – <N>EpicMice</font></p>"
                lists2 = "<p align='left'><font size='7'>"
                this.Cursor.execute("select Username, CheeseCount, FirstCount, BootcampCount, ShamanSaves, HardModeSaves, DivineModeSaves, TitleNumber from Users where PrivLevel < 13 ORDER By FirstCount DESC LIMIT 10")
                rs = this.Cursor.fetchall()
                pos = 1
                this.client.updateDatabase()
                for rrf in rs:
                    playerName = str(rrf[0])
                    CheeseCount = rrf[1]
                    FirstCount = rrf[2]
                    BootcampCount = rrf[3]
                    ShamanSaves = rrf[4]
                    HardModeSaves = rrf[5]
                    DivineModeSaves = rrf[6]
                    TitleNumber = rrf[7]
                    status= "<N>[<VP>Online - <font color='98FB98'>BR</font><N>]<N>"
                    status= "<N>[<R>Offline<N>]<N>"
                    if pos == 1:
                        lists += "<p align='left'><font color='#FFD700' size='18'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n" 
                    elif pos == 2:
                        lists += "<p align='left'><font color='#FFD700' size='18'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 3:
                        lists += "<p align='left'><font color='#FFD700' size='18'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 4:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 5:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 6:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 7:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 8:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 9:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    elif pos == 10:
                        lists += "<p align='left'><font color='#606090'>"+str(pos)+"º</font> <font color='#3C5064'>-</font> <N>Kullanıcı adı: <font color='#009d9d'>"+str(playerName)+"" + '<N> -' + (' <N>[<VP>Online<N> - <T>TR</font><N>]<N>'if this.server.checkConnectedAccount(playerName) else'<N> [<R>Offline<N>]') + " \n"
                    lists += "   <p align='left'><font color='#00FF7F'>• Birinci olarak topladığı peynir :</font> <font color='#FFFFFF'>"+str(FirstCount)+"</font>"
                    lists += "<br />"
                    lists += "   <font color='#6A7495'>• Şu anki unvanı :</font> <font color='#009d9d'>"+str(TitleNumber)+"</font>"
                    lists += "<br />"
                    lists += "   <p align='left'><font color='#6A7495'>• Peynir yüklü kurtarılan fare sayısı :</font> <font color='#009d9d'>"+str(ShamanSaves)+" / "+"<font color='#FADE55'>"+str(HardModeSaves)+" / "+"<font color='#F52331'>"+str(DivineModeSaves)+"</font>"
                    lists += "<br />"
                    lists += "   <p align='left'><font color='#6A7495'>• Topladığı peynir :</font> <font color='#6C77C1'>"+str(CheeseCount)+"</font>"
                    lists += "<br />"
                    lists += "   <p align='left'><font color='#6A7495'>• Bootcamp :</font> <font color='#6C77C1'>"+str(BootcampCount)+"</font>"
                    lists += "<br /><br />"
                    pos += 1
                this.client.sendLogMessage(lists + "</font></p>")

            elif command in ["staff", "ekip", "equipe"]:
                if this.client.privLevel >= 1:
                    lists = ["<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>", "<p align='center'>"]
                    this.Cursor.execute("select Username, PrivLevel, Langue from Users where PrivLevel > 4")
                    for rs in this.Cursor.fetchall():
                        if rs["Langue"] == this.client.langueStaff:
                            playerName = rs["Username"]
                            privLevel = int(rs["PrivLevel"])
                            player = this.server.players.get(playerName)
                            lists[{12:0, 11:1, 10:2, 9:3, 8:4, 7:5, 6:6, 5:7, 4:8}[privLevel]] += "\n<V>%s</V> <N>-</N> %s <N>- [%s]</N>\n" %(playerName, {12:"<font color='#24B1FF'>☪ Game Master ☪</font>", 11:"<font color='#C724FF'>Baş Admin</font>", 10:"<ROSE>Genel Sorumlu</ROSE>", 9:"<VI>Admin<VI>", 8:"<J>Super Mod</J>", 7:"<CE>Mod</CE0>", 6:"<CEP>MapCrew</CEP>", 5:"<CS>Yardımcı</CS>", 4:"<CH>Reklamcı</CH>"}[privLevel], "<VP>Online</VP> - <R>%s</R>" %(player.langue) if player != None else "<R>Offline</R>")
                    this.client.sendLogMessage("<V><p align='center'><font size = \"15\"><b>   | <font color='#FFFFFF'>EpicMice Yönetim Kadrosu</font> |<font size = \"12\"></b><</p>\n%s</p>" %("".join(lists)))

            elif command in ["vips", "vipers"]:
                lists = ["<p align='center'>"]
                this.Cursor.execute("select Username from Users where PrivLevel >= 2 AND PrivLevel <= 4")
                for rs in this.Cursor.fetchall():
                    playerName = rs["Username"]
                    player = this.server.players.get(playerName)
                    lists += "\n<V>%s</V> <N>-</N> <J>VIP</J> <N>- [%s]</N>\n" %(playerName, "<VP>Online</VP> - <R>%s</R>" %(player.langue) if player != None else "<R>Offline</R>")
                this.client.sendLogMessage("<V><p align='center'><b>Vips</b></p>%s</p>" %("".join(lists)))

            elif command in ["vamp"]:
                if this.client.privLevel >= 4:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendVampireMode(False)
                    else:
                        if this.client.privLevel >= 6:
                            playerName = Utils.parsePlayerName(args[0])
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendVampireMode(False)

            elif command in ["meep"]:
                if this.client.privLevel >= 4:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Meep, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Meep, 1)
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Meep, 1)

            elif command in ["pink"]:
                if this.client.privLevel >= 3:
                    this.client.room.sendAll(Identifiers.send.Player_Damanged, ByteArray().writeInt(this.client.playerCode).toByteArray())

            elif command in ["transformation"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        if this.client.privLevel >= 2:
                            if this.client.room.numCompleted > 1 or this.client.privLevel >= 9:
                                this.client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    else:
                        playerName = Utils.parsePlayerName(args[0])
                        if playerName == "*":
                            for player in this.client.room.clients.values():
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)
                        else:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.sendPacket(Identifiers.send.Can_Transformation, 1)

            elif command in ["shaman"]:
                if this.client.privLevel >= 9:
                    if len(args) == 0:
                        this.client.isShaman = True
                        this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(this.client.playerCode).writeUnsignedByte(this.client.shamanType).writeUnsignedByte(this.client.shamanLevel).writeShort(this.client.server.getShamanBadge(this.client.playerCode)).toByteArray())

                    else:
                        this.requireArgs(1)
                        playerName = Utils.parsePlayerName(args[0])
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.isShaman = True
                            this.client.room.sendAll(Identifiers.send.New_Shaman, ByteArray().writeInt(player.playerCode).writeUnsignedByte(player.shamanType).writeUnsignedByte(player.shamanLevel).writeShort(player.server.getShamanBadge(player.playerCode)).toByteArray())

            elif command in ["lock"]:
                if this.client.privLevel >= 12:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) < 4:
                            player = this.server.players.get(playerName)
                            if player != None:
                                player.room.removeClient(player)
                                player.transport.loseConnection()
                            this.Cursor.execute("update Users set PrivLevel = -1 where Username = ?", [playerName])
                            this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> tarafından engellendi <V>"+this.client.playerName)

            elif command in ["unlock"]:
                if this.client.privLevel >= 12:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>"+playerName+"<BL>.")
                    else:
                        if this.server.getPlayerPrivlevel(playerName) == -1:
                            this.Cursor.execute("update Users set PrivLevel = 1 where Username = ?", [playerName])
                        this.server.sendStaffMessage(7, "<V>"+playerName+"<BL> tarafından engel kaldırıldı <V>"+this.client.playerName)

            elif command in ["namecolor", "isimrenk"]:
                if len(args) == 1:
                    if this.client.privLevel >= 4:
                        hexColor = args[0][1:] if args[0].startswith("#") else args[0]

                        try:
                            this.client.room.setNameColor(this.client.playerName, int(hexColor, 16))
                            this.client.nameColor = hexColor
                            this.client.sendMessage("İsim renginiz değişti!")
                        except:
                            this.client.sendMessage("Renk geçersiz. Lütfen HEX kullanın (#00000).")

                elif len(args) > 1:
                    if this.client.privLevel >= 7:
                        playerName = Utils.parsePlayerName(args[0])
                        hexColor = args[1][1:] if args[1].startswith("#") else args[1]
                        try:
                            if playerName == "*":
                                for player in this.client.room.clients.values():
                                    this.client.room.setNameColor(player.playerName, int(hexColor, 16))
                            else:
                                this.client.room.setNameColor(playerName, int(hexColor, 16))
                        except:
                            this.client.sendMessage("Renk geçersiz. Lütfen HEX kullanın (#00000).")
                else:
                    if this.client.privLevel >= 4:
                        this.client.room.showColorPicker(10000, this.client.playerName, int(this.client.nameColor) if this.client.nameColor == "" else 0xc2c2da, "Selecione uma cor para seu nome.")

            elif command in ["color", "renk"]:
                if this.client.privLevel >= 3:
                    if len(args) == 1:
                        hexColor = args[0][1:] if args[0].startswith("#") else args[0]

                        try:
                            value = int(hexColor, 16)
                            this.client.mouseColor = hexColor
                            this.client.playerLook = "1;" + this.client.playerLook.split(";")[1]
                            this.client.sendMessage("Rennginiz değişti!")
                        except:
                            this.client.sendMessage("Renk geçersiz. Lütfen HEX kullanın (#00000).")
                        
                    elif len(args) > 1:
                        if this.client.privLevel >= 9:
                            playerName = this.client.Utils.parsePlayerName(args[0])
                            hexColor = "" if args[1] == "off" else args[1][1:] if args[1].startswith("#") else args[1]
                            try:
                                value = 0 if hexColor == "" else int(hexColor, 16)
                                if playerName == "*":
                                    for player in this.client.room.clients.values():
                                        player.tempMouseColor = hexColor
                                else:
                                    player = this.server.players.get(playerName)
                                    if player != None:
                                        player.tempMouseColor = hexColor
                            except:
                                this.client.sendMessage("Renk geçersiz. Lütfen HEX kodu kullanın (#00000).")
                    else:
                        try:
                            this.client.room.showColorPicker(10001, this.client.playerName, int(this.client.mouseColor, 16), "Fareniz için bir renk seçin.")
                        except:
                            this.client.room.showColorPicker(10001, this.client.playerName, int("78583A", 16), "Fareniz için bir renk seçin")

            elif command in ["giveforall"]:
                if this.client.privLevel >= 12:
                    this.requireArgs(2)
                    type = args[0].lower()
                    count = int(args[1]) if args[1].isdigit() else 0
                    type = "peynir" if type.startswith("peynir") or type.startswith("cheese") else "çilek" if type.startswith("morango") or type.startswith("çilek") else "bootcamp" if type.startswith("bc") or type.startswith("bootcamp") else "first" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "hediye" if type.startswith("hediye") or type.startswith("hediye") else "fichas" if type.startswith("fichas") else ""
                    if count > 0 and not type == "":
                        this.server.sendStaffMessage(7, "<V>%s</V> sunucuya <V>%s %s</V> dağıttı." %(this.client.playerName, count, type))
                        for player in this.server.players.values():
                            if type in ["peynir", "fraises"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "peynir" else 0).writeInt(count if type == "çilek" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "peynir" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<V>%s %s</V> kazandınız." %(count, type))
                            if type == "peynir":
                                player.shopCheeses += count
                            elif type == "çilek":
                                player.shopFraises += count
                            elif type == "bootcamp":
                                player.bootcampCount += count
                            elif type == "first":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "hediye":
                                player.nowHediye += count
                            elif type == "fichas":
                                player.nowTokens += count

            elif command in ["give"]:
                if this.client.privLevel == 12:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    count = 10000 if count > 10000 else count
                    type = "peynir" if type.startswith("peynir") or type.startswith("cheese") else "çilek" if type.startswith("morango") or type.startswith("çilek") else "bootcamp" if type.startswith("bc") or type.startswith("bootcamp") else "first" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "hediye" if type.startswith("hediye") or type.startswith("hediye") else "fichas" if type.startswith("fichas") else ""
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>%s,</V> %s</V> nickli kişiye <V>%s %s</V> gönderdi." %(this.client.playerName, playerName, count, type))
                            if type in ["peynir", "fraises"]:
                                player.sendPacket(Identifiers.send.Gain_Give, ByteArray().writeInt(count if type == "peynir" else 0).writeInt(count if type == "çilek" else 0).toByteArray())
                                player.sendPacket(Identifiers.send.Anim_Donation, ByteArray().writeByte(0 if type == "peynir" else 1).writeInt(count).toByteArray())
                            else:
                                player.sendMessage("<V>%s %s</V> kazandınız." %(count, type))
                            if type == "peynir":
                                player.shopCheeses += count
                            elif type == "çilek":
                                player.shopFraises += count
                            elif type == "bootcamp":
                                player.bootcampCount += count
                            elif type == "first":
                                player.cheeseCount += count
                                player.firstCount += count
                            elif type == "profile":
                                player.cheeseCount += count
                            elif type == "saves":
                                player.shamanSaves += count
                            elif type == "hardSaves":
                                player.hardModeSaves += count
                            elif type == "divineSaves":
                                player.divineModeSaves += count
                            elif type == "hediye":
                                player.nowHediye += count
                            elif type == "fichas":
                                player.nowTokens += count

            elif command in ["ungive"]:
                if this.client.privLevel >= 12:
                    this.requireArgs(3)
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    type = args[1].lower()
                    count = int(args[2]) if args[2].isdigit() else 0
                    type = "queijos" if type.startswith("queijo") or type.startswith("cheese") else "fraises" if type.startswith("morango") or type.startswith("fraise") else "bootcamps" if type.startswith("bc") or type.startswith("bootcamp") else "firsts" if type.startswith("first") else "profile" if type.startswith("perfilqj") else "saves" if type.startswith("saves") else "hardSaves" if type.startswith("hardsaves") else "divineSaves" if type.startswith("divinesaves") else "hediye" if type.startswith("hediye") or type.startswith("hediye") else "fichas" if type.startswith("fichas") else ""
                    yeah = False
                    if count > 0 and not type == "":
                        player = this.server.players.get(playerName)
                        if player != None:
                            this.server.sendStaffMessage(7, "<V>%s</V> tirou <V>%s %s</V> de <V>%s</V>." %(this.client.playerName, count, type, playerName))
                            if type == "queijos":
                                if not count > player.shopCheeses:
                                    player.shopCheeses -= count
                                    yeah = True
                            if type == "fraises":
                                if not count > player.shopFraises:
                                    player.shopFraises -= count
                                    yeah = True
                            if type == "bootcamps":
                                if not count > player.bootcampCount:
                                    player.bootcampCount -= count
                                    yeah = True
                            if type == "firsts":
                                if not count > player.firstCount:
                                    player.cheeseCount -= count
                                    player.firstCount -= count
                                    yeah = True
                            if type == "profile":
                                if not count > player.cheeseCount:
                                    player.cheeseCount -= count
                                    yeah = True
                            if type == "saves":
                                if not count > player.shamanSaves:
                                    player.shamanSaves -= count
                                    yeah = True
                            if type == "hardSaves":
                                if not count > player.hardModeSaves:
                                    player.hardModeSaves -= count
                                    yeah = True
                            if type == "divineSaves":
                                if not count > player.divineModeSaves:
                                    player.divineModeSaves -= count
                                    yeah = True
                            if type == "hediye":
                                if not count > player.nowHediye:
                                    player.nowHediye -= count
                                    yeah = True
                            if type == "fichas":
                                if not count > player.nowTokens:
                                    player.nowTokens -= count
                                    yeah = True
                            if yeah:
                                player.sendMessage("<V>%s %s</V> kaybettiniz." %(count, type))
                            else:
                                this.sendMessage("Oyuncuda zaten bu kadar miktarda %s yok." %(type))

            elif command in ["unranked", "ranked"]:
                if this.client.privLevel == 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s</V>." %(playerName))
                    else:
                        this.Cursor.execute("update Users set UnRanked = ? where Username = ?", [1 if command == "unranked" else 0, playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> foi %s ranking por <V>%s</V>." %(playerName, "removido do" if command == "unranked" else "colocado novamente no", this.client.playerName))

            elif command in ["resetprofile"]:
                if this.client.privLevel == 10:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s</V>." %(playerName))
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.room.removeClient(player)
                            player.transport.loseConnection()
                        this.Cursor.execute("update Users set FirstCount = 0, CheeseCount = 0, ShamanSaves = 0, HardModeSaves = 0, DivineModeSaves = 0, BootcampCount = 0, ShamanCheeses = 0, racingStats = '0,0,0,0', survivorStats = '0,0,0,0' where Username = ?", [playerName])
                        this.server.sendStaffMessage(7, "<V>%s</V> teve o perfil resetado por <V>%s</V>." %(playerName, this.client.playerName))

            elif command in ["warn"]:
                if this.client.privLevel >= 5:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    message = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)
                    if player == None:
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>%s<BL>." %(playerName))
                    else:
                        rank = {5:"Helper", 6:"MapCrew", 7:"Mod", 8:"Super Mod", 9:"Admin", 10:"Genel Sorumlu", 11:"Baş Admin", 12:"Kurucu"}[this.client.privLevel]
                        player.sendMessage("<ROSE>[<b>UYARI</b>] %s %s size bir uyarı gönderdi. Sebep: %s</ROSE>" %(rank, this.client.playerName, message))
                        this.client.sendMessage("Uyarı Mesajın Başarıyla Gönderildi <V>%s</V>." %(playerName))
                        this.server.sendStaffMessage(7, "<V>%s</V> <V>%s</V> nickli kişiyi uyardı. Sebep: <V>%s</V>" %(this.client.playerName, playerName, message))

            elif command in ["mjj"]:
                roomName = args[0]
                if roomName.startswith("#"):
                    if roomName.startswith("#utility"):
                        this.client.enterRoom(roomName)
                    else:
                        this.client.enterRoom(roomName + "1")
                else:
                    this.client.enterRoom(({0:"", 1:"", 3:"vanilla", 8:"survivor", 9:"racing", 11:"music", 2:"bootcamp", 10:"defilante", 16:"village"}[this.client.lastGameMode]) + roomName)

            elif command in ["mulodrome"]:
                if this.client.privLevel == 10 or this.client.room.roomName.startswith(this.client.playerName) and not this.client.room.isMulodrome:
                    for player in this.client.room.clients.values():
                        player.sendPacket(Identifiers.send.Mulodrome_Start, 1 if player.playerName == this.client.playerName else 0)

            elif command in ["takip"]:
                if this.client.privLevel >= 5:
                    this.requireArgs(1)
                    playerName = Utils.parsePlayerName(args[0])
                    player = this.server.players.get(playerName)
                    if player != None:
                        this.client.enterRoom(player.roomName)

            elif command in ["moveplayer"]:
                if this.client.privLevel >= 7:
                    playerName = Utils.parsePlayerName(args[0])
                    roomName = argsNotSplited.split(" ", 1)[1]
                    player = this.server.players.get(playerName)
                    if player != None:
                        player.enterRoom(roomName)

            elif command in ["setvip"]:
                if this.client.privLevel >= 9:
                    playerName = Utils.parsePlayerName(args[0])
                    days = args[1]
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı:  <V>"+playerName+"<BL>.")
                    else:
                        this.server.setVip(playerName, int(days) if days.isdigit() else 1)

            elif command in ["removevip"]:
                if this.client.privLevel >= 9:
                    playerName = Utils.parsePlayerName(args[0])
                    this.requireNoSouris(playerName)
                    if not this.server.checkExistingUser(playerName):
                        this.client.sendMessage("Kullanıcı bulunamadı: <V>"+playerName+"<BL>.")
                    else:
                        player = this.server.players.get(playerName)
                        if player != None:
                            player.privLevel = 1
                            if player.titleNumber == 1100:
                                player.titleNumber = 0

                            player.sendMessage("<CH>VIP yetkisini kazandınız.")
                            this.Cursor.execute("update Users set VipTime = 0 where Username = ?", [playerName])
                        else:
                            this.Cursor.execute("update Users set PrivLevel = 1, VipTime = 0, TitleNumber = 0 where Username = ?", [playerName])

                        this.server.sendStaffMessage(7, "O jogador <V>"+playerName+"<BL> não é mais VIP.")
                
            elif command in ["mm"]:
                if this.client.privLevel >= 7:
                    this.client.room.sendAll(Identifiers.send.Staff_Chat, ByteArray().writeByte(0).writeUTF("").writeUTF(argsNotSplited).writeShort(0).writeByte(0).toByteArray())
                  		
			
            elif command in ["appendblack", "removeblack"]:
                if this.client.privLevel >= 7:
                    name = args[0].replace("http://www.", "").replace("https://www.", "").replace("http://", "").replace("https://", "").replace("www.", "")
                    if command == "appendblack":
                        if name in this.server.serverList:
                            this.client.sendMessage("[<R>%s</R>] zaten listede." %(name))
                        else:
                            this.server.serverList.append(name)
                            this.server.updateBlackList()
                            this.client.sendMessage("[<J>%s</J>] listeye eklendi" %(name))
                    else:
                        if not name in this.server.serverList:
                            this.client.sendMessage("[<R>%s</R>] listede yok." %(name))
                        else:
                            this.server.serverList.remove(name)
                            this.server.updateBlackList()
                            this.client.sendMessage("[<J>%s</J>] listeden kaldırıldı" %(name))
        except Exception as ERROR:
            pass
			
			
    def getCommandsList(this):
        message = "%s komutlar:\n\n" %({1:"EpicMice Özel", 2:"EpicMice Özel", 3:"EpicMice Özel", 4:"EpicMice Özel", 5:"EpicMice Özel", 6:"EpicMice Özel", 7:"EpicMice Özel", 8:"EpicMice Özel", 9:"EpicMice Özel", 10:"EpicMice Özel", 11:"EpicMice Özel", 12:"EpicMice Özel"}[this.client.privLevel])
        message += "<J>/sıralama</J> <V><BL> : Oyuncu Sıralamasını açar (İlk 10) </BL>\n"
        message += "<J>/ekip</J> <G> <BL> : Oyunun yönetim kadrosunu gösterir </BL>\n"
        message += "<J>/mousecolor</J><BL> : Fare Renginizi Değiştirir </BL>\n"
        message += "<J>/namecolor <G>[#FFFFFF]<BL> : İsim Renginizi Değiştirir</BL>\n"
        message += "<J>/mod</J><BL> : Çevrimiçi yetkilileri gösterir.</BL>\n"
        message += "<J>/ping</J><BL> : İnternetinizin gecikme hızını gösterir</BL>\n"
        message += "<J>/pw</J>[Şifre]<BL> : Özel odanızı şifreler</BL>\n"
        message += "<J>/pwkaldir</J><BL> : Özel odanızın şifresini kaldırır</BL>\n"

        
        message += "</font></p>"
        return message

