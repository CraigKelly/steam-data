PY=python3

SETUP=$(CURDIR)/setup
PYTOOL=$(CURDIR)/pytool
VENV=$(CURDIR)/venv

IDCMD=idlist.py
GAMESCMD=games.py
FEATURESCMD=games-features.py

IDLIST=idlist.csv
GAMEJSON=games.json
STEAMSPY=steamspy.json
FEATURECSV=games-features.csv
TARBALL=steam-data.tar.gz

csv: $(FEATURECSV)
$(FEATURECSV): $(IDLIST) $(GAMEJSON) $(FEATURESCMD) $(STEAMSPY)
	@echo "Creating CSV - run 'make games' to update games.json from idlist"
	$(PYTOOL) games-features.py

steamspy: $(STEAMSPY)
$(STEAMSPY): $(VENV)
	wget 'http://steamspy.com/api.php?request=all' -O $(STEAMSPY)

games: $(VENV) $(IDLIST) $(GAMESCMD)
	@echo "Getting ID's not in games.json"
	$(PYTOOL) games.py

idlist: $(IDLIST) $(IDCMD)
$(IDLIST): $(VENV)
	$(PYTOOL) idlist.py

setup: $(VENV)
$(VENV):
	$(CURDIR)/setup

clean:
	rm -fr $(VENV) $(IDLIST) $(FEATURECSV) $(STEAMSPY)
	@echo "games.json skipped because of restart logic. Manually delete if you"
	@echo "must. BUT ONLY IF YOU KNOW WHAT YOU'RE DOING"

tarball: $(TARBALL)
$(TARBALL): $(IDLIST) $(GAMEJSON) $(FEATURECSV) $(STEAMSPY)
	rm -f $(TARBALL)
	tar -zvcf $(TARBALL) $(IDLIST) $(GAMEJSON) $(FEATURECSV) $(STEAMSPY) columns.md
	@echo "Tarball created - you should put it somewhere"

.PHONY: clean setup idlist games csv steamspy tarball
