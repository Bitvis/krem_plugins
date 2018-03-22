set -x
set -e

ROOT_PATH=$PWD
PLUGIN_PATH=$ROOT_PATH/krem_plugins
PLUGIN_TESTS_PATH=$PLUGIN_PATH/tests
JOB_OUTPUT_PATH=$PLUGIN_TESTS_PATH/output/plugin_testing


cd $PLUGIN_TESTS_PATH
if [ -d "$JOB_OUTPUT_PATH" ]; then
  rm -r $JOB_OUTPUT_PATH/*
fi

python /usr/src/app/krem/install.py
source ~/.bashrc

krem run -j plugin_testing

