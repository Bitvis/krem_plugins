set -x

PYTHON_VERSION=$1
OUTPUT_DIR=./output_$PYTHON_VERSION

set -e

rm -rf ./output_$PYTHON_VERSION 
mkdir ./output_$PYTHON_VERSION

cp krem_plugins/tests/library/scripts/Dockerfile_$PYTHON_VERSION ./Dockerfile

rm -rf krem
cp $(dirname $(which krem)) ./krem -r
docker build -t test_krem_plugins .
rm -rf krem

set +e
docker run --name test_krem_plugins test_krem_plugins
test_rc=$?

docker cp test_krem_plugins:/usr/src/app/krem_plugins/tests/output $OUTPUT_DIR
output_rc=$?

docker rm -f test_krem_plugins
clean_img_rc=$?

docker rmi -f test_krem_plugins
clean_cont_rc=$?

if [ $test_rc -eq 1 ] || [ $output_rc -eq 1 ] || [ $clean_img_rc -eq 1 ] || [ $clean_cont_rc -eq 1 ]
then
	exit 1
else
	exit 0
fi
