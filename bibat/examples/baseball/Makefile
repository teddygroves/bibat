.PHONY: clean-runs clean-plots clean-stan clean-all analysis env

ACTIVATE_VENV = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt
SRC = baseball

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
		python -m pip install -e .; \
	  install_cmdstan $(INSTALL_CMDSTAN_FLAGS); \
	)

analysis: env
	. $(ACTIVATE_VENV) && (\
	  python $(SRC)/prepare_data.py || exit 1; \
	  python $(SRC)/sample.py || exit 1; \
	  jupyter execute $(SRC)/investigate.ipynb || exit 1; \
	)

clean-stan:
	$(RM) $(shell find ./$(SRC)/stan -perm +100 -type f) # remove binary files
	$(RM) $(SRC)/stan/*.hpp

clean-inferences:
	$(RM) $(shell find ./inferences/* -type f -not -name "*.toml")

clean-plots:
	$(RM) -r plots/*.png

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-inferences clean-plots
