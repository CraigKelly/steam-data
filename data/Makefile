PY=python3

BASEDIR=$(CURDIR)
SETUP=$(CURDIR)/setup
PYTOOL=$(CURDIR)/pytool
VENV=$(BASEDIR)/venv
IDLIST=idlist.csv
GAMEJSON=games.json

games: $(GAMEJSON)
$(GAMEJSON): $(VENV) $(IDLIST)
	$(PYTOOL) games.py

idlist: $(IDLIST)
$(IDLIST): $(VENV)
	$(PYTOOL) idlist.py

setup: $(VENV)
$(VENV):
	$(CURDIR)/setup

clean:
	rm -fr $(VENV) $(IDLIST) $(GAMEJSON)

.PHONY: clean setup idlist games
