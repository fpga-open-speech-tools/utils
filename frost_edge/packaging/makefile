build:
	mkdir -p src/armhf/lib/modules/frost/;
	cp ../lkms/* src/armhf/lib/modules/frost/;

	mkdir -p src/armhf/var/lib/frost/web_app/;
	cp -r ../publish src/armhf/var/lib/frost/web_app/;
	
	cp -r ../utils/runtime_config/ src/armhf/var/lib/frost/;

	mkdir -p src/armhf/usr/bin/;
	cp scripts/frost_edge.sh src/armhf/usr/bin/;

	mkdir -p src/armhf/etc/systemd/system/;
	cp scripts/frost_edge.service src/armhf/etc/systemd/system/;

install:
	cp -av src/`dpkg --print-architecture`/* ${DESTDIR}

clean:
	@echo "Cleaning not required. Binary package."