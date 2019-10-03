#!bin/bash
WORKING_DIR="AirdropDeploy"
ENVIR="mitnick"
URL="http://localhost"
while getopts ":u:d:e:h" opt; do
      case $opt in
        d ) WORKING_DIR="$OPTARG";;
        h )
            echo "Usage:"
            echo "    deploy.sh -h               Display this help message."
            echo "    deploy.sh -d               Name of the destination Directory"
            exit 0
            ;;
        \?) echo "Invalid option: -"$OPTARG"" >&2
            exit 1;;
        : ) echo "Option -"$OPTARG" requires an argument." >&2
            exit 1;;
      esac
    done

echo "Your working directory is "$WORKING_DIR""
echo "Your url is "$URL""

if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi
if [ -d "$WORKING_DIR.zip" ]; then rm -Rf $WORKING_DIR.zip; fi
mkdir $WORKING_DIR
cp -r ./airdrop-api ./$WORKING_DIR
cp -r ./docker-compose.yml ./$WORKING_DIR
zip -r $WORKING_DIR.zip $WORKING_DIR
rm -Rf $WORKING_DIR




