configure:
	[ -d ~/.gmail_notifier ] || mkdir ~/.gmail_notifier/

install:
	sudo apt-get install curl python-indicate
	cd feedparser/; python setup.py install; cd -
	cp messaging_menu.py ~/.gmail_notifier/
	cp gmail_notifier /usr/local/bin/
	sudo chmod a+x /usr/local/bin/gmail_notifier
	cp gmail_notifier.desktop /usr/share/applications/

uninstall:
	rm -r ~/.gmail_notifier
	rm /usr/local/bin/gmail_notifier
	rm /usr/share/applications/gmail_notifier.desktop
