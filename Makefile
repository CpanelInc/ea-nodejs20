OBS_PROJECT := EA4
OBS_PACKAGE := ea-nodejs20
DISABLE_BUILD := arch=i586 repository=CentOS_6.5_standard
include $(EATOOLS_BUILD_DIR)obs.mk
