.phony = clean_all clean_stan clean_plots clean_pdf clean_data

BIBLIOGRAPHY = bibliography.bib
CMDSTAN_LOGS = $(shell find results/samples -type f -name "*.txt")
STAN_FILES = $(shell find stan -type f \( -not -name "*.stan" -not -name "*.md" \))
SAMPLES = $(shell find results/samples -name "*.csv")
FAKE_DATA = $(shell find data/fake -name "*.csv")
PREPARED_DATA = $(shell find data/prepared -name "*.csv")
INFDS = $(shell find results/infd -type f -not -name "*.md")
LOOS = $(shell find results/loo -type f -not -name "*.md")
JSONS = $(shell find results/input_data_json -type f -not -name "*.md")
PLOTS = $(shell find results/plots -type f -name "*.png")
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
	$(RM) $(CMDSTAN_LOGS) $(STAN_FILES)

clean_results:
	$(RM) $(SAMPLES) $(INFDS) $(LOOS) $(PLOTS) $(JSONS)

clean_pdf:
	$(RM) $(PDF_FILE)
