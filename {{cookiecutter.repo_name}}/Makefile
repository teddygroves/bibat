.PHONY: clean-runs clean-plots clean-stan clean-all analysis

ACTIVATE_VENV_BINARY = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_FLAGS = --compiler
else
	INSTALL_CMDSTAN_FLAGS =
endif

$(ACTIVATE_VENV_BINARY):
	python -m venv .venv --prompt={{cookiecutter.repo_name}}

$(REQUIREMENTS_FILE): $(ACTIVATE_VENV_BINARY)
	pip install --upgrade pip
	pip install -r $(REQUIREMENTS_FILE)

analysis: $(ACTIVATE_VENV_BINARY) $(REQUIREMENTS_FILE) $(CMDSTAN)
	. $(ACTIVATE_VENV_BINARY) && pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)
	install_cmdstan $(INSTALL_CMDSTAN_FLAGS)
	python prepare_data.py
	python sample.py
	jupyter execute investigate.ipynb

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
