.PHONY: clean-runs clean-plots clean-stan clean-all analysis

ACTIVATE_VENV = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt
RAW_DATA = data/raw/2006.csv \
	data/raw/bdb-main.csv \
	data/raw/bdb-post.csv \
	data/raw/bdb-apps.csv

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_FLAGS = --compiler
	ACTIVATE_VENV = .venv/Scripts/activate
else
	INSTALL_CMDSTAN_FLAGS =
endif

$(ACTIVATE_VENV):
	python -m venv .venv --prompt=baseball

env: $(ACTIVATE_VENV) $(REQUIREMENTS_FILE) $(CMDSTAN)
	. $(ACTIVATE_VENV) && (\
	  python -m pip install --upgrade pip; \
	  python -m pip install -r $(REQUIREMENTS_FILE) --quiet; \
	  install_cmdstan $(INSTALL_CMDSTAN_FLAGS); \
	)

$(RAW_DATA):
	. $(ACTIVATE_VENV) && python fetch_data.py

analysis: env $(RAW_DATA)
	. $(ACTIVATE_VENV) && (\
	  python prepare_data.py || exit 1; \
	  python sample.py || exit 1; \
	  jupyter execute investigate.ipynb || exit 1; \
	)

clean-stan:
	$(RM) $(shell find ./src/stan -perm +100 -type f) # remove binary files
	$(RM) ./src/stan/*.hpp

clean-runs:
	$(RM) -r results/runs/*/

clean-plots:
	$(RM) -r results/plots/*.png

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-runs clean-plots
