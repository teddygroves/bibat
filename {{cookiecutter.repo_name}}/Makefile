.phony = clean_all clean_stan clean_results clean_pdf clean_data

QUOTE_LINES = sed "s/^/'/;s/$$/'/"  # pipe this to make sure filenames are quoted
BIBLIOGRAPHY = bibliography.bib
CMDSTAN_LOGS = $(shell find results/samples -type f -name "*.txt" | $(QUOTE_LINES))
STAN_OBJECT_CODE = \
  $(shell find src/stan -type f \( -not -name "*.stan" -not -name "*.md" \) \
  | $(QUOTE_LINES))
SAMPLES = $(shell find results/samples -name "*.csv" | $(QUOTE_LINES))
FAKE_DATA = $(shell find data/fake -type f -name "*.csv" | $(QUOTE_LINES))
PREPARED_DATA = $(shell find data/prepared -name "*.csv" | $(QUOTE_LINES))
INFDS = $(shell find results/infd -type f -not -name "*.md" | $(QUOTE_LINES))
LOOS = $(shell find results/loo -type f -not -name "*.md" | $(QUOTE_LINES))
JSONS = $(shell find results/input_data_json -type f -not -name "*.md" | $(QUOTE_LINES))
MARKDOWN_FILE = report.md
PDF_FILE = report.pdf
PANDOCFLAGS =                         \
  --from=markdown                     \
  --highlight-style=pygments          \
  --pdf-engine=xelatex                \
  --bibliography=$(BIBLIOGRAPHY)      

$(PDF_FILE): $(MARKDOWN_FILE) $(BIBLIOGRAPHY)
	pandoc $< -o $@ $(PANDOCFLAGS)

clean_all: clean_stan clean_results clean_pdf clean_data

clean_data:
	$(RM) $(FAKE_DATA) $(PREPARED_DATA)

clean_stan:
	$(RM) $(CMDSTAN_LOGS) $(STAN_OBJECT_CODE)

clean_results:
	$(RM) $(SAMPLES) $(INFDS) $(LOOS) $(PLOTS) $(JSONS) $(CMDSTAN_LOGS)

clean_pdf:
	$(RM) $(PDF_FILE)
