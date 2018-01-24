from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .activity import Activity

"""
This Class creates a formal messaging system between
members and visitors of the hospital.
:atrb: timestamp    Time when message was created.
:atrb: Sender_ID    ID corresponding with the user sending the message.
:atrb: Receiver_ID  ID corresponding with the user receiving the message.
:atrb: Subject      Brief description of what the message is about.
:atrb: Message      Full description of what the message is about.
"""
class Messages( models.Model ):
    timestamp = models.DateTimeField(default=timezone.now)
    Sender_ID = models.CharField(max_length=100, default='')
    Receiver_ID = models.CharField(max_length=100, default='')
    SenderDelete = models.BooleanField(default=False)
    ReceiverDelete = models.BooleanField(default=False)
    Subject = models.CharField(max_length=100, default='')
    Message = models.TextField(max_length=1250, default="")
    def __str__(self):
        return "From "+str(self.Sender_ID) + ", sent at " + str(self.timestamp)
    def sendMsg(message_form,user):
        NewMessage = Messages(
            Sender_ID = user,
            Receiver_ID = message_form['Receiver_ID'],
            timestamp = timezone.now(),
            Subject = message_form['Subject'],
            Message = message_form['Message'],
            SenderDelete = False,
            ReceiverDelete = False
        )
        NewMessage.save()
        Activity.createActivity(timezone.now(),"Sent a message to ", NewMessage.Sender_ID, user, None, "MessageSent")
        return NewMessage
    def deleteMsg(self,user):
        if user == self.Sender_ID:
            self.SenderDelete = True
        if user == self.Receiver_ID:
            self.ReceiverDelete = True
        if self.SenderDelete == True and self.ReceiverDelete == True:
            self.delete()
        self.save()
    def displayMsg(self):
        return "Subject: "+str(self.Subject)+"/n /nDetails: "+str(self.Message)
    def reply(message_form, reply):
        message = Messages(
            Sender_ID = reply.Receiver_ID,
            Receiver_ID = reply.Sender_ID,
            timestamp = timezone.now(),
            Subject = reply.Subject,
            Message = message_form['Message']
        )
        message.save()
        Activity.createActivity(timezone.now(), "New message sent by", message.Sender_ID,message.Receiver_ID , None, "MessageSent")

