.PHONY: clean-inferences clean-plots clean-stan clean-all analysis env docs clean-docs

ENV_MARKER = .venv/.bibat.marker
ACTIVATE_VENV = .venv/bin/activate
SRC = baseball
DOCS_DIR = docs

REPORT_STEM = docs/report
QUARTO_EXTENSIONS_FOLDER = $(DOCS_DIR)/_extensions

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_FLAGS = --compiler
	ACTIVATE_VENV = .venv/Scripts/activate
else
	INSTALL_CMDSTAN_FLAGS =
endif

env: $(ENV_MARKER)

$(ACTIVATE_VENV):
	python -m venv .venv --prompt=baseball

$(QUARTO_EXTENSIONS_FOLDER):
	cd docs && quarto add quarto-ext/include-code-files && cd -

docs: $(ENV_MARKER) $(QUARTO_EXTENSIONS_FOLDER)
	. $(ACTIVATE_VENV) && (\
		quarto render $(REPORT_STEM).qmd; \
	)

$(ENV_MARKER): $(ACTIVATE_VENV) $(CMDSTAN)
	. $(ACTIVATE_VENV) && (\
	  python -m pip install --upgrade pip; \
		python -m pip install -e .; \
	  install_cmdstan $(INSTALL_CMDSTAN_FLAGS); \
		touch $@ ; \
	)

analysis: $(ENV_MARKER)
	. $(ACTIVATE_VENV) && (\
	  python $(SRC)/prepare_data.py || exit 1; \
	  python $(SRC)/sample.py || exit 1; \
	  jupyter execute $(SRC)/investigate.ipynb || exit 1; \
	)

clean-docs:
	$(RM) $(shell find $(DOCS_DIR) -iname "$(REPORT_STEM).*" -type f -not -name "*.qmd")

clean-stan:
	$(RM) $(shell find ./$(SRC)/stan -perm +100 -type f) # remove binary files
	$(RM) $(SRC)/stan/*.hpp

clean-inferences:
	$(RM) $(shell find ./inferences/* -type f -not -name "*.toml")

clean-plots:
	$(RM) -r plots/*.png

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-inferences clean-plots clean-docs
