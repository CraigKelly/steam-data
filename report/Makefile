REPORT=report.tex
PDF=report.pdf
BIB=report.bib

PNG := $(shell find $(BASEDIR) -name '*.png')
EPS := $(shell find $(BASEDIR) -name '*.eps')

report: $(PDF)
$(PDF): $(REPORT) $(BIB) $(PNG) $(EPS)
	rubber --pdf $(REPORT)

info: $(PDF)
	rubber-info --pdf $(REPORT)

clean:
	rubber --clean --pdf $(REPORT)

.PHONY: clean report
