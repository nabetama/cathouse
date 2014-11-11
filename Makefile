EXCLUDE = --exclude=.git \
					--exclude=Makefile \
					--exclude=.gitignore \
					--exclude=*.pyc \
					--exclude=config.py \
					--exclude=.DS_STORE \
					--exclude=.sass-cache/ \
					--exclude=.test_data/
OPT = -cropgtv --cvs-exclude --delete $(EXCLUDE)
LOCAL_PATH = .

REMOTE_USER=`whoami`
REMOTE_HOST=conoha
REMOTE_PATH=~/git/cathouse


default:
	@echo "Usage:"
	@echo " make install"
	@echo " make install-lite"
	@echo " make dry-install"
	@echo " make bacuum"
	@echo " make dry-bacuum"

install: rsync restart
install-lite: rsync-lite restart
bacuum: take
dry-install: dry-rsync
dry-bacuum: dry-take

rsync:
	rsync $(OPT) $(LOCAL_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_PATH)/

take:
	rsync $(OPT) $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_PATH)/ $(LOCAL_PATH)/

rsync-lite:
	$(MAKE) rsync \
			OPT="$(OPT) --exclude=static"

dry-rsync:
	$(MAKE) rsync \
			OPT="--dry-run $(OPT)"

dry-take:
	$(MAKE) take \
			OPT="--dry-run $(OPT)"

# restart:
# 	ssh $(REMOTE_USER)@$(REMOTE_HOST) 'sudo /etc/init.d/cathouse restart'

test:
	py.test tests/ -v
