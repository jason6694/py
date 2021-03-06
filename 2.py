from linepy import *
import timeit
from time import strftime
import time


client = LINE('booooob456@gmail.com', 'Sonyxp456')
#or client = LINE()
#or client.log("Auth Token : " + str(client.authToken))

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid =["u2d18b195540f5484316912e588829dda", "u234bcf9156e7a0a24ead24451a5f47c1"]


blackListedMid = ["mid1", "mid2"]


#mymid : ""


def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if op.param1 not in JoinedGroups:
            if op.param2 in whiteListedMid:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
            else:
                client.acceptGroupInvitation(op.param1)
                JoinedGroups.append(op.param1)
                client.leaveGroup(op.param1)
                JoinedGroups.remove(op.param1)
        else:
            # blacklist
            group = client.getGroup(op.param1)
            if op.param2 not in whiteListedMid:
                if op.param3 in blackListedMid:
                    group = client.getGroup(op.param1)
                    if group.invitee is not None:
                        client.cancelGroupInvitation(op.param1, [op.param3])
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
        return


def NOTIFIED_UPDATE_GROUP(op):
    group = client.getGroup(op.param1)
    if op.param2 not in whiteListedMid:
        if op.param3 == "4":
            if group.preventedJoinByTicket == True:
                try:
                    client.reissueGroupTicket(op.param1)
                    group.preventedJoinByTicket = True
                    client.updateGroup(group)
                    client.kickoutFromGroup(op.param1, [op.param2])
                except Exception as e:
                    print(e)


def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    # print op
    try:
        if op.param2 in blackListedMid:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 == MySelf.mid:
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                client.kickoutFromGroup(op.param1, [op.param2])
                group = client.getGroup(op.param1)
                if group.preventedJoinByTicket == True:
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
                else:
                    try:
                        str1 = client.reissueGroupTicket(op.param1)
                        client.updateGroup(group)
                        client.sendMessage(op.param3,
                                           "/jgurlx gid: " + op.param1 + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
        print("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return


def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    print("\n")
                    print("Private Chat Message Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Message : " + msg.text)
                    print("\n")
                    if msg._from in whiteListedMid:
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg._from, str1)
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        elif msg.text.startswith("/jgurl"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                        if msg.text == "/help":
                            client.sendMessage(msg._from,
                                        "Private Chat Command:\n\n/help\n/contact <MID>\n/mid\n/google\n/wiki\n/github\n/youtube\n/yahoo\n/amazon\n/jgurl <gid: GID gid> <url: gurl url>\n/send chat <mid: MID mid> <text: TEXT text>\n/send group <gid: GID gid> <text: TEXT text>\n/send chat contact <mid: MID mid> <cmid: CONTACT MID cmid>\n/send group contact <gid: GID gid> <cmid: CONTACT MID cmid>\n/kick <gid: GID gid> <mid: MID mid>\n\nGroup Command:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\n/bye")
                        if msg.text == "/mid":
                            client.sendMessage(msg._from, "Name : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\nPermission Level : 5")
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg._from, str1)
                        if msg.text == "/google":
                            client.sendMessage(msg._from, "https://www.google.com")
                        if msg.text == "/wiki":
                            client.sendMessage(msg._from, "https://www.wikipedia.com")
                        if msg.text == "/github":
                            client.sendMessage(msg._from, "https://github.com")
                        if msg.text == "/youtube":
                            client.sendMessage(msg._from, "https://www.youtube.com")
                        if msg.text == "/yahoo":
                            client.sendMessage(msg._from, "https://www.yahoo.com")
                        if msg.text == "/amazon":
                            client.sendMessage(msg._from, "https://www.amazon.com")
                        if msg.text.startswith("/send chat"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/send group"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "text: ", " text")
                            client.sendMessage(str1, str2)
                        if msg.text.startswith("/send chat contact"):
                            str1 = find_between_r(msg.text, "mid: ", " mid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/send group contact"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "cmid: ", " cmid")
                            client.sendContact(str1, str2)
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "mid: ", " mid")
                            try:
                                client.kickoutFromGroup(str1, [str2])
                            except Exception as e:
                                print(e)
                    elif msg._from in whiteListedMid:
                        if msg.text.startswith("/jgurlx"):
                            str1 = find_between_r(msg.text, "gid: ", " gid")
                            str2 = find_between_r(msg.text, "url: http://line.me/R/ti/g/", " url")
                            client.acceptGroupInvitationByTicket(str1, str2)
                            JoinedGroups.append(str1)
                            group = client.getGroup(str1)
                            try:
                                client.reissueGroupTicket(str1)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                elif msg.toType == 1:
                    pass
                elif msg.toType == 2:
                    if msg._from in whiteListedMid:
                        if msg.text == "/gid":
                            client.sendMessage(msg.to, msg.to)
                        if msg.text == "/ginfo":
                            group = client.getGroup(msg.to)
                            md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                            if group.preventedJoinByTicket is False:
                                md += "\n\nInvitationURL: Permitted\n"
                            else:
                                md += "\n\nInvitationURL: Refusing\n"
                            if group.invitee is None:
                                md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                            else:
                                md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(
                                    len(group.invitee)) + "People"
                                client.sendMessage(msg.to, md)
                        if msg.text == "/speed":
                            time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                            str1 = str(time0)
                            client.sendMessage(msg.to, str1)
                        if msg.text.startswith("/contact"):
                            str1 = find_between_r(msg.text, "/contact ", "")
                            client.sendContact(msg.to, str1)
                        if msg.text == "/mid":
                            client.sendMessage(msg.to, "Name : " + client.getContact(msg._from).displayName + "\nMID : " + msg._from + "\nPermission Level : 5")
                        if msg.text == "/bye":
                            client.leaveGroup(msg.to)
                            JoinedGroups.remove(msg.to)
                        if msg.text == "/gurl on":
                            group = client.getGroup(msg.to)
                            try:
                                group.preventedJoinByTicket = False
                                str1 = client.reissueGroupTicket(msg.to)
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                            client.sendMessage(msg.to, "http://line.me/R/ti/g/" + str1)
                        if msg.text == "/gurl off":
                            group = client.getGroup(msg.to)
                            try:
                                client.reissueGroupTicket(msg.to)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                            except Exception as e:
                                print(e)
                        if msg.text == "/time":
                            client.sendMessage(msg.to, strftime("現在是 %H 時 %M 分 %S 秒"))
                        if msg.text == "/google":
                            client.sendMessage(msg.to, "https://www.google.com")
                        if msg.text == "/wiki":
                            client.sendMessage(msg.to, "https://www.wikipedia.com")
                        if msg.text == "/github":
                            client.sendMessage(msg.to, "https://github.com")
                        if msg.text == "/youtube":
                            client.sendMessage(msg.to, "https://www.youtube.com")
                        if msg.text == "/yahoo":
                            client.sendMessage(msg.to, "https://www.yahoo.com")
                        if msg.text == "/amazon":
                            client.sendMessage(msg.to, "https://www.amazon.com")
                        if msg.text.startswith("/kick"):
                            str1 = find_between_r(msg.text, "/kick ", "")
                            if str1 not in whiteListedMid:
                                try:
                                    client.kickoutFromGroup(msg.to, [str1])
                                except Exception as e:
                                    print(e)
                                return
                else:
                    pass
            except:
                pass
        elif msg.contentType == 13:
            if msg.toType == 0:
                if msg._from in whiteListedMid:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    else:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
                else:
                    x = op.message.contentMetadata
                    str1 = str(x)
                    str2 = find_between_r(str1, "'mid': '", "'")
                    str3 = find_between_r(str1, "'mid': '", "', '")
                    if "displayName" in str2 and str3 not in whiteListedMid:
                        strx = str(str3)
                        client.sendMessage(msg._from, strx)
                    elif str2 not in whiteListedMid:
                        strx2 = str(str2)
                        client.sendMessage(msg._from, strx2)
                    print("\n")
                    print("Private Chat Contact Received")
                    print("Sender's Name : " + client.getContact(msg._from).displayName)
                    print("Sender's MID : " + msg._from)
                    print("Received Contact MID : " + str2)
                    print("Received Contact Display Name : " + client.getContact(str2).displayName)
                    print("\n")
            elif msg.toType == 1:
                pass
            elif msg.toType == 2:
                x = op.message.contentMetadata
                str1 = str(x)
                str2 = find_between_r(str1, "'mid': '", "'")
                str3 = find_between_r(str1, "'mid': '", "', '")
                if "displayName" in str2 and str3 not in whiteListedMid:
                    strx = str(str3)
                    client.sendMessage(msg.to, strx)
                elif str2 not in whiteListedMid:
                    strx2 = str(str3)
                    client.sendMessage(msg.to, strx2)
                    print("Contact Received, MID : " + str2)
        else:
            pass
    except Exception as error:
        print(error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return


oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


while True:
    oepoll.trace()
