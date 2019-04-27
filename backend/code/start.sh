#!/bin/bash
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

alembic="pipenv run alembic"
uwsgi="pipenv run uwsgi"

echo -e "${YELLOW}Running migrations${NC}"
$alembic upgrade head
if [ "$?" != "0" ] ; then
  exit 1
fi

if [ "$AUTORELOAD" == "true" ] ; then
    echo -e "${YELLOW}Starting dev server${NC}"
    COMMAND="--py-autoreload 1 --honour-stdin"
else
    echo -e "${YELLOW}Starting production server${NC}"
    COMMAND=""
fi
$uwsgi --ini-paste /code/app.ini $COMMAND
