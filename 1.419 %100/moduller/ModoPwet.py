#coding: utf-8
# Modules
from utils import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

class ModoPwet:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server

    def checkReport(this, array, playerName):
        return playerName in array    

    def makeReport(this, playerName, type, comments):
        playerName = Utils.parsePlayerName(playerName)
        this.server.sendStaffMessage(7, "<V>%s</V> oyuncuyu rapor ediyor <R>%s</R> tarafından <J>%s</J> bu sebeple: <J>%s</J>" %(this.client.playerName, playerName, {0:"Hack", 1:"Spam / Flood", 2:"Insultos", 3:"Pishing", 4:"Outro"}[type], "-" if comments == "" else comments))

        if playerName in this.server.reports["names"]:
            this.server.reports[playerName]["types"].append(str(type))
            this.server.reports[playerName]["reporters"].append(this.client.playerName)
            this.server.reports[playerName]["comments"].append(comments)
            this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
        else:
            this.server.reports["names"].append(playerName)
            this.server.reports[playerName] = {}
            this.server.reports[playerName]["types"] = [str(type)]
            this.server.reports[playerName]["reporters"] = [this.client.playerName]
            this.server.reports[playerName]["comments"] = [comments]
            this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
            this.server.reports[playerName]["langue"] = this.getModopwetLangue(playerName)

        this.updateModoPwet()
        this.client.sendBanConsideration()

    def getModopwetLangue(this, playerName):
        player = this.server.players.get(playerName)
        return player.langue if player != None else "tr"

    def updateModoPwet(this):
        for player in this.server.players.values():
            if player.isModoPwet and player.privLevel >= 7:
                player.modoPwet.openModoPwet()

    def getPlayerRoomName(this, playerName):
        player = this.server.players.get(playerName)
        return player.roomName if player != None else "0"

    def getProfileCheeseCount(this, playerName):
        player = this.server.players.get(playerName)
        return player.cheeseCount if player != None else 0

    def openModoPwet(this):
        if len(this.server.reports["names"]) <= 0:
            this.client.sendPacket(Identifiers.send.Open_Modopwet, chr(0))
        else:
            reports = 0
            totalReports = len(this.server.reports["names"])
            count = 0

            bannedList = {}
            deletedList = {}
            disconnectList = []

            p = ByteArray()

            while reports < totalReports:
                playerName = this.server.reports["names"][reports]
                reports += 1
                if this.client.modoPwetLangue == "ALL" or this.server.reports[playerName]["langue"] == this.client.modoPwetLangue.upper():
                    count += 1
                    if count >= 255:
                        break

                    p.writeByte(count).writeUTF(this.server.reports[playerName]["langue"].upper()).writeUTF(playerName).writeUTF(this.getPlayerRoomName(playerName)).writeInt(this.getProfileCheeseCount(playerName))

                    reporters = 0
                    totalReporters = len(this.server.reports[playerName]["types"])
                    p.writeByte(totalReporters)

                    while reporters < totalReporters:
                        p.writeUTF(this.server.reports[playerName]["reporters"][reporters]).writeShort(this.getProfileCheeseCount(this.server.reports[playerName]["reporters"][reporters])).writeUTF(this.server.reports[playerName]["comments"][reporters]).writeByte(this.server.reports[playerName]["types"][reporters]).writeShort(reporters)
                        reporters += 1

                    if this.server.reports[playerName]["status"] == "banned":
                        x = {}
                        x["banhours"] = this.server.reports[playerName]["banhours"]
                        x["banreason"] = this.server.reports[playerName]["banreason"]
                        x["bannedby"] = this.server.reports[playerName]["bannedby"]
                        bannedList[playerName] = x

                    if this.server.reports[playerName]["status"] == "deleted":
                        x = {}
                        x["deletedby"] = this.server.reports[playerName]["deletedby"]
                        deletedList[playerName] = x

                    if this.server.reports[playerName]["status"] == "disconnected":
                        disconnectList.append(playerName)

            this.client.sendPacket(Identifiers.send.Open_Modopwet, ByteArray().writeByte(count).writeBytes(p.toByteArray()).toByteArray())

            for user in disconnectList:
                this.changeReportStatusDisconnect(user)

            for user in deletedList.keys():
                this.changeReportStatusDeleted(user, deletedList[user]["deletedby"])

            for user in bannedList.keys():
                this.changeReportStatusBanned(user, bannedList[user]["banhours"], bannedList[user]["banreason"], bannedList[user]["bannedby"])

    def changeReportStatusDisconnect(this, playerName):
        this.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())

    def changeReportStatusDeleted(this, playerName, deletedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

    def changeReportStatusBanned(this, playerName, banhours, banreason, bannedby):
        this.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

    def openChatLog(this, playerName):
        packet = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]) * 2 if this.server.chatMessages.has_key(playerName) else 0)
        if this.server.chatMessages.has_key(playerName):
            for message in this.server.chatMessages[playerName]:
                packet.writeUTF(message[0]).writeUTF(message[1])                        
        this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
