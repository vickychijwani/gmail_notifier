GMAIL NOTIFIER
==============

Notifies the user of unread email as soon as it arrives, using Ubuntu's default notification bubbles. Also integrates with the messaging menu. HTTP proxy supported.


Installation
------------
1. Open the script 'gmail_notifier' in a text editor. Enter your Gmail username and password at the top of the script in the 'User Configuration Options' section. Also configure other options to your liking (all options are documented in the script itself). Save and exit.
2. Run the following commands (this will also install all dependencies automatically):

```sh
$ make configure
$ sudo make install
```
3. To uninstall, run:

```sh
$ sudo make uninstall
```


Dependencies
------------
- curl
- python-indicate (installed by default in Ubuntu 10.10 Maverick Meerkat; I'm not sure about other versions of Ubuntu.)
- feedparser (available at http://code.google.com/p/feedparser/)


Supported Platforms
-------------------
Tested on Ubuntu 10.10, 11.04


Features
--------
1. Notifications are sent through the native notification system (notify-osd)
2. Notifications also display the subject and sender's name for all unread mail
3. Integrates well with Ubuntu's messaging menu
4. Network errors and authentication errors are handled gracefully, and the user is optionally notified of them too


To-do
-----
2. Currently the username and password are hard-coded into the script. This vulnerability should be eliminated either by storing the password in encrypted form or under the control of another password (say, the user's login password).
3. Currently, to check for new unread email, the script checks if the count of unread email has increased. This is not necessarily true (e.g. if the user reads an unread email and another new email arrives in the time between two checks).
4. Provide GUI for configuration options (time between 2 consecutive checks, expiry time of notifications, what things to display in the notification, etc).
