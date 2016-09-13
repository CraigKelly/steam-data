PY=python3

BASEDIR=$(CURDIR)
SETUP=$(CURDIR)/setup
PYTOOL=$(CURDIR)/pytool
VENV=$(BASEDIR)/venv
IDLIST=idlist.csv
GAMEJSON=games.json

games: $(VENV) $(IDLIST)
	@echo "Getting ID's not in games.json"
	$(PYTOOL) games.py

idlist: $(IDLIST)
$(IDLIST): $(VENV)
	$(PYTOOL) idlist.py

setup: $(VENV)
$(VENV):
	$(CURDIR)/setup

clean:
	rm -fr $(VENV) $(IDLIST)
	@echo "games.json skipped because of restart logic. Manually delete if you"
	@echo "must. BUT ONLY IF YOU KNOW WHAT YOU'RE DOING"

.PHONY: clean setup idlist games
