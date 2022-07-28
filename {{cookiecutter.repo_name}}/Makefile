.PHONY: clean-runs clean-plots clean-stan clean-all analysis

ACTIVATE_VENV_BINARY = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt

ifndef CMDSTAN
	CMDSTAN = ~/.cmdstan
endif

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_CMD += --compiler
endif

$(ACTIVATE_VENV_BINARY):
	python -m venv .venv --prompt={{cookiecutter.repo_name}}

$(REQUIREMENTS_FILE): $(ACTIVATE_VENV_BINARY)
	pip install --upgrade pip
	pip install -r $(REQUIREMENTS_FILE)

$(CMDSTAN):
	ifeq ($(OS),Windows_NT)
		install_cmdstan --compiler
	else
		install_cmdstan
	endif

analysis: $(ACTIVATE_VENV_BINARY) $(REQUIREMENTS_FILE) $(CMDSTAN)
	. $(ACTIVATE_VENV_BINARY) && pip install --upgrade pip && pip install -r $(REQUIREMENTS_FILE)
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
