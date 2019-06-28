#!/bin/bash
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

alembic="pipenv run alembic"
gunicorn="pipenv run gunicorn"

echo -e "${YELLOW}Running migrations${NC}"
$alembic upgrade head
if [ "$?" != "0" ] ; then
  exit 1
fi

if [ "$AUTORELOAD" == "true" ] ; then
    echo -e "${YELLOW}Starting dev server${NC}"
    COMMAND="--reload 1 --reload-engine poll"
else
    echo -e "${YELLOW}Starting production server${NC}"
    COMMAND=""
fi
$gunicorn --paste /code/app.ini $COMMAND --log-level debug
