build:
	mkdir -p src/armhf/lib/modules/frost/;
	cp ../lkms/* src/armhf/lib/modules/frost/;

	mkdir -p src/armhf/var/lib/frost/web_app/;
	cp -r ../publish src/armhf/var/lib/frost/web_app/;

	mkdir -p src/armhf/var/lib/frost/utils/;
	cp -r ../utils/runtime_config/ src/armhf/var/lib/frost/utils/;

	mkdir -p src/armhf/usr/bin/;
	cp scripts/frost_edge_lkms.sh src/armhf/usr/bin/;

	mkdir -p src/armhf/etc/systemd/system/;
	cp scripts/frost_edge_lkms.service    src/armhf/etc/systemd/system/;
	cp scripts/frost_edge_web_app.service src/armhf/etc/systemd/system/;
	cp scripts/frost_edge_dm.service      src/armhf/etc/systemd/system/;

install:
	cp -av src/`dpkg --print-architecture`/* ${DESTDIR}

clean:
	@echo "Cleaning not required. Binary package."