configure:
	mkdir ~/.gmail_notifier/

install:
	sudo apt-get install curl python-indicate
	cd feedparser/; python setup.py install; cd -
	cp messaging_menu.py ~/.gmail_notifier/
	cp -r sounds/ ~/.gmail_notifier/
	cp gmail_notifier /usr/bin/
	cp gmail_notifier.desktop /usr/share/applications/

uninstall:
	rm -ir ~/.gmail_notifier
	rm -i /usr/bin/gmail_notifier
	rm -i /usr/share/applications/gmail_notifier.desktop
