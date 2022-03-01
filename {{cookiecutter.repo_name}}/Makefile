.PHONY: clean-results clean-stan clean-all results {% if cookiecutter.create_writing_directory == "y" %} report clean-report  {% endif %}
{% if cookiecutter.create_writing_directory == "y" %}
BIBLIOGRAPHY = writing/bibliography.bib
MARKDOWN_FILE = writing/report.md
PDF_FILE = writing/report.pdf
PANDOCFLAGS =                         \
  --from=markdown                     \
  --highlight-style=pygments          \
  --pdf-engine=xelatex                \
  --citeproc                          \
  --bibliography=$(BIBLIOGRAPHY)      
{% endif %}
analysis:
	python prepare_data.py
	python sample.py
	python analyse.py

report: $(PDF_FILE)
{% if cookiecutter.create_writing_directory == "y" %}
$(PDF_FILE): $(MARKDOWN_FILE) $(BIBLIOGRAPHY)
	pandoc $< -o $@ $(PANDOCFLAGS)

clean-report:
	$(RM) $(PDF_FILE)
{% endif %}
clean-stan:
	$(RM) $(shell find ./src/stan -perm +100 -type f) # remove binary files
	$(RM) ./src/stan/*.hpp

clean-results:
	$(RM) -r results/runs/*/

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-results {% if cookiecutter.create_writing_directory == "y" %}clean-report {% endif %}
