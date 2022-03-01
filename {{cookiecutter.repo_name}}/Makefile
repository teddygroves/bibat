.PHONY: clean-results clean-stan clean-all clean-report results report

BIBLIOGRAPHY = writing/bibliography.bib
MARKDOWN_FILE = writing/report.md
PDF_FILE = writing/report.pdf
PANDOCFLAGS =                         \
  --from=markdown                     \
  --highlight-style=pygments          \
  --pdf-engine=xelatex                \
  --citeproc                          \
  --bibliography=$(BIBLIOGRAPHY)      

analysis:
	python prepare_data.py
	python sample.py
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

clean-report:
	$(RM) $(PDF_FILE)


clean-all: clean-prepared-data clean-stan clean-results clean-report
