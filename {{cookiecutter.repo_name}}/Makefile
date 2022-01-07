.PHONY: clean-results clean-stan clean-all clean-pdf results report plots

BIBLIOGRAPHY = bibliography.bib
MARKDOWN_FILE = report.md
PDF_FILE = report.pdf
PANDOCFLAGS =                         \
  --from=markdown                     \
  --highlight-style=pygments          \
  --pdf-engine=xelatex                \
  --bibliography=$(BIBLIOGRAPHY)      

results:
	python prepare_data.py
	python sample.py

plots:
	python analyse.py

report: $(PDF_FILE)

$(PDF_FILE): $(MARKDOWN_FILE) $(BIBLIOGRAPHY)
	pandoc $< -o $@ $(PANDOCFLAGS)

clean-stan:
	$(RM) $(shell find ./src/stan -perm +100 -type f) # remove binary files
	$(RM) ./src/stan/*.hpp

clean-results:
	$(RM) -r results/runs/*/

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-plots:
	$(RM) results/plots/*.png
	$(RM) results/plots/*.svg

clean_pdf:
	$(RM) $(PDF_FILE)


clean-all: clean-prepared-data clean-stan clean-results clean-pdf
