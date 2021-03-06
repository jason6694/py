from linepy import *
import timeit
from time import strftime
import time


client = LINE('boooooob456@gmail.com', 'Sonyxp456')
#or client = LINE()
#or client.log("Auth Token : " + str(client.authToken))

oepoll = OEPoll(client)

MySelf = client.getProfile()
JoinedGroups = client.getGroupIdsJoined()
print("My MID : " + MySelf.mid)

whiteListedMid = ["u2d18b195540f5484316912e588829dda", "u234bcf9156e7a0a24ead24451a5f47c1"]

blackListedMid = ["mid1", "mid2"]


#mymid : ""


def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    try:
        if op.param2 in blackListedMid:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 == MySelf.mid:
            JoinedGroups.remove(op.param1)
        else:
            if op.param3 in whiteListedMid:
                if op.param2 not in whiteListedMid:
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except Exception as e:
                        print(e)
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
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    if msg._from in whiteListedMid:
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
                else:
                    pass
            except:
                pass
        else:
            pass
    except Exception as error:
        print(error)
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    client.sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg._from}, contentType=13)
                if msg.text == "/you":
                    client.sendMessage(msg.to, text=None, contentMetadata={'mid': msg.to}, contentType=13)
                if msg.text.startswith("/contact"):
                    str1 = find_between_r(msg.text, "/contact ", "")
                    client.sendContact(msg.to, str1)
                if msg.text == "/help":
                    client.sendMessage(msg.to,
                                       "Private Chat Command:\n\n/help\n/contact <MID>\n/mid\n/google\n/wiki\n/github\n/youtube\n/yahoo\n/amazon\n\nGroup Command:\n\n/gid\n/ginfo\n/kick <MID>\n/gurl on\n/gurl off\n/bye")
                if msg.text == "/speed":
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    client.sendMessage(msg.to, str1)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "invite bot":
                    group = client.getGroup(msg.to)
                    try:
                        group.preventedJoinByTicket = False
                        str1 = client.reissueGroupTicket(msg.to)
                        client.updateGroup(group)
                    except Exception as e:
                        print(e)
                    client.sendMessage("u234bcf9156e7a0a24ead24451a5f47c1",
                                "/jgurl gid: " + msg.to + " gid " + "url: http://line.me/R/ti/g/" + str1 + " url")
                if msg.text == "/speed":
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    client.sendMessage(msg.to, str1)
                if msg.text == "mid":
                    client.sendMessage(msg.to, msg._from)
                if msg.text == "/gid":
                    client.sendMessage(msg.to, msg.to)
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
                if msg.text == "/ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventedJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    client.sendMessage(msg.to,md)
                if msg.text == "me":
                    client.sendContact(msg.to, MySelf.mid)
        else:
            pass

    except Exception as e:
        print(e)
        print ("\n\nSEND_MESSAGE\n\n")
        return



# Add function to LinePoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.SEND_MESSAGE: SEND_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION
})

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

while True:
    oepoll.trace()
