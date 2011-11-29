import indicate
import time
import feedparser
import os.path

from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

indicators = {}

def serverClick(*args):
  os.popen("$(update-alternatives --display x-www-browser|sed 2p -n|sed 's/^.*link currently points to //') http://mail.google.com/")


def inboxHandler(*args):
  os.popen("$(update-alternatives --display x-www-browser|sed 2p -n|sed 's/^.*link currently points to //') http://mail.google.com/")


def quitHandler(*args):
  os.popen("pgrep -l gmail_notifier | cut -d' ' -f1 | xargs kill")
  os.popen("pgrep -lf 'python messaging_menu.py' | cut -d' ' -f1 | xargs kill")


def setInboxStatus(new_status):
  """
  Set the inbox status.
  Also draw the user's attention if unread mail count has increased.
  @param new_status: The status of the inbox."""

  inbox = indicators["Inbox"]
  inbox.set_property("count", new_status)
  if new_status.isdigit() and int(new_status) > 0:
  	inbox.set_property("draw-attention", "true")
  else:
  	inbox.set_property("draw-attention", "false")


def pollUnreadMail():
  """
  Monitor the mail.unread file for changes.
  If there are changes, call setUnreadCount."""

  inbox = indicators["Inbox"]
  if not os.path.isfile(os.path.expanduser("~/.gmail_notifier/mail.error")) and os.path.isfile(os.path.expanduser("~/.gmail_notifier/mail.unread")):
    f = open(os.path.expanduser("~/.gmail_notifier/mail.unread"))
    d = feedparser.parse(f.read())

    new_count = d.feed.fullcount
    old_count = inbox.get_property("count")

    if new_count != old_count:
    	setInboxStatus(new_count)
        inbox.show()

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


def addIndicator(indicator_name, handler):
  """
  Add a new indicator to the application's messaging menu entry (the "server").
  @param indicator_name: The label for the indicator in the messaging menu."""

  indicator = indicate.Indicator()
  indicator.set_property("name", indicator_name)
  indicator.set_property("subtype", "mail")

  indicator.label = indicator_name
  indicator.connect("user-display", handler)

  indicators[indicator_name] = indicator
  indicator.show()


if __name__ == "__main__":
  server = indicate.indicate_server_ref_default()
  server.set_type("message.mail")
  server.set_desktop_file("/usr/share/applications/gmail_notifier.desktop")
  server.connect("server-display", serverClick)
  server.show();

  addIndicator("Quit", quitHandler)
  indicators["Quit"].set_property("count", "")

  addIndicator("Inbox", inboxHandler)
  setInboxStatus("Connecting...")

  lc = LoopingCall(pollUnreadMail)
  lc.start(5,False)

  reactor.run()

