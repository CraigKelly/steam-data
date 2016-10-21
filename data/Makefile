PY=python3

SETUP=$(CURDIR)/setup
PYTOOL=$(CURDIR)/pytool
VENV=$(CURDIR)/venv
IDLIST=idlist.csv
GAMEJSON=games.json
TARBALL=steam-data.tar.gz

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

tarball: $(TARBALL)
$(TARBALL): $(IDLIST) $(GAMEJSON)
	rm -f $(TARBALL)
	tar -zvcf $(TARBALL) $(IDLIST) $(GAMEJSON)
	@echo "Tarball created - you should put it somewhere"

.PHONY: clean setup idlist games
