.PHONY: clean-runs clean-plots clean-stan clean-all analysis

ACTIVATE_VENV = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_FLAGS = --compiler
	ACTIVATE_VENV = .venv/Scripts/activate
else
	INSTALL_CMDSTAN_FLAGS =
endif

$(ACTIVATE_VENV):
	python -m venv .venv --prompt={{cookiecutter.repo_name}}

env: $(ACTIVATE_VENV) $(REQUIREMENTS_FILE) $(CMDSTAN)
	. $(ACTIVATE_VENV) && (\
	  python -m pip install --upgrade pip; \
	  python -m pip install -r $(REQUIREMENTS_FILE) --quiet; \
	  install_cmdstan $(INSTALL_CMDSTAN_FLAGS); \
	)

analysis: env
	. $(ACTIVATE_VENV) && (\
	  {% if cookiecutter.create_tests_directory %}python -m pytest || exit 1; \{% endif %}
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
