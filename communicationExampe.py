#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:28:29 2016

@author: elhe
"""
import spade
import time
host = "127.0.0.1"
identification = spade.AID.aid(name="agent@127.0.0.1", addresses=["xmpp://agent@m127.0.0.1"])

class Sender(spade.Agent.Agent):

    def _setup(self):
        self.addBehaviour(self.SendMsgBehav())
        print "Agent started!"

    class SendMsgBehav(spade.Behaviour.Behaviour):
        """
        This behaviour sends a message to this same agent to trigger an EventBehaviour
        """

        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
            msg.setOntology("ururur")
            msg.setContent("Hello World")
            
            
            msg1 = spade.ACLMessage.ACLMessage()
            msg1.setPerformative("inform")
            msg1.addReceiver(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
            msg1.setOntology("qqq")
            msg1.setContent("Hello World")
            
            print "Sending message in 1 . . ."
            time.sleep(1)

            self.myAgent.send(msg)
            
            print "I sent a message"
            
        def _onTick(self):
            print "q"
    
    class RecvMsgBehav(spade.Behaviour.EventBehaviour):
        """
        This EventBehaviour gets launched when a message that matches its template arrives at the agent
        """

        def _process(self): 
            self.msg = None
            self.msg = self._receive(True, None)
            #print self.msg
            print "I got an qqq message!"
            print "This behaviour has been triggered by a message!"
    
    class RecvMsgBehav1(spade.Behaviour.EventBehaviour):
        def _process(self): 
            self.msg = None
            self.msg = self._receive(True, None)
            #print self.msg
            if self.msg:
                print "I got an ururur message!"
            else:
                print "This behaviour has been triggered by a message!"
            
    
    def _setup(self):
    
        template = spade.Behaviour.ACLTemplate()
        #template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        template.setOntology("ururur")
        t = spade.Behaviour.MessageTemplate(template)
        
        template1 = spade.Behaviour.ACLTemplate()
        template1.setOntology("qqq")
        t1 = spade.Behaviour.MessageTemplate(template)
        
        # Add the EventBehaviour with its template
        self.addBehaviour(self.RecvMsgBehav(),t)
        self.addBehaviour(self.RecvMsgBehav1(),t1)
        
        # Add the sender behaviour
        self.addBehaviour(self.SendMsgBehav())

if __name__ == "__main__":
    a = Sender("rece...@127.0.0.1", "secret")
    a.start()