#!/bin/bash
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

alembic="pipenv run alembic"
uwsgi="pipenv run uwsgi"

# echo "Running migrations"
# $alembic upgrade head
# if [ "$?" != "0" ] ; then
  # exit 1
# fi

if [ "$IS_DEV" == "true" ] ; then
    echo -e "Starting dev server ${YELLOW}(http protocol)${NC}"
    COMMAND="--py-autoreload 1 --honour-stdin"
else
    echo -e "Starting production server ${YELLOW}(wsgi protocol)${NC}"
    COMMAND=""
fi
set -x
$uwsgi --ini-paste /code/app.ini $COMMAND
