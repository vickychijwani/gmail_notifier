import indicate
import time
import feedparser
import os.path

from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

indicators = { }

# handler for clicks on the main "Gmail Notifier" thingy
def serverClick(*args):
  
  os.popen("$(update-alternatives --display x-www-browser|sed 2p -n|sed 's/^.*link currently points to //') http://mail.google.com/")

# handler for clicks on an indicator of Gmail Notifier
def labelClick(*args):
  
  os.popen("$(update-alternatives --display x-www-browser|sed 2p -n|sed 's/^.*link currently points to //') http://mail.google.com/")

# function to set the inbox status, and also draw attention if the unread mail count has increased
def setInboxStatus(new_status):
  """
  Set the inbox status.
  Also draw the user's attention if unread mail count has increased.
  
  @param new_status: The status of the inbox.\n"""
  
  old_status = indicators["Inbox"].get_property("count")
  indicators["Inbox"].set_property("count", new_status)
  
  if new_status.isdigit() and int(new_status) > 0 :
  	indicators["Inbox"].set_property("draw-attention", "true")
  else:
  	indicators["Inbox"].set_property("draw-attention", "false")

# function to monitor the mail.unread file
def pollUnreadMail():
  """
  Monitor the mail.unread file for changes.
  If there are changes, call setUnreadCount.\n"""
  
  if not os.path.isfile(os.path.expanduser("~/.gmail_notifier/mail.error")) and os.path.isfile(os.path.expanduser("~/.gmail_notifier/mail.unread")):
    
    f = open(os.path.expanduser("~/.gmail_notifier/mail.unread"))
    d = feedparser.parse(f.read())
    
    new_count = d.feed.fullcount
    old_count = indicators["Inbox"].get_property("count")
    
    if new_count != old_count:
    	setInboxStatus(new_count)
    
  else:
    
    if os.path.isfile(os.path.expanduser("~/.gmail_notifier/mail.error")):
      error_code = file(os.path.expanduser("~/.gmail_notifier/mail.error")).read().strip()
      print "Error code: "+error_code
      if error_code == "0":
        setInboxStatus("Network error")
      elif error_code == "1":
        setInboxStatus("Auth. error")
      else:
      	setInboxStatus("Error")

# function to add an indicator to the Gmail Notifier server in the messaging menu. ("Inbox" is one such indicator)
def addIndicator(indicator_name):
  """
  Add a new indicator to the application's messaging menu entry.
  
  @param indicator_name: The label for the indicator in the messaging menu.\n"""
  
  indicator = indicate.Indicator()
  indicator.set_property("name", indicator_name)
  indicator.set_property("count", "")
  
  indicator.label = indicator_name
  indicator.connect("user-display", labelClick)
  
  indicators[indicator_name] = indicator
  indicators[indicator_name].show()

# main function
def main():
  server = indicate.indicate_server_ref_default()
  server.set_type("message.mail")
  server.set_desktop_file("/usr/share/applications/gmail_notifier.desktop")
  server.connect("server-display", serverClick)
  
  addIndicator("Inbox")
  setInboxStatus("Connecting...")
  
  lc = LoopingCall(pollUnreadMail)
  lc.start(5,False)
  
  reactor.run()

# call the main() function if this script has been called directly instead of being imported
if __name__ == "__main__":
  main()
