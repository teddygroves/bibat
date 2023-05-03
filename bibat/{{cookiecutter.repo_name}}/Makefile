.PHONY: clean-inferences clean-plots clean-stan clean-all analysis env {% if cookiecutter.docs_format != 'No docs' %}docs clean-docs{% endif %}

ENV_MARKER = .venv/.bibat.marker
ACTIVATE_VENV = .venv/bin/activate
REQUIREMENTS_FILE = requirements.txt
SRC = {{cookiecutter.repo_name}}
{% if cookiecutter.docs_format != 'No docs' %}DOCS_DIR = docs{% endif %}
{% if cookiecutter.docs_format == 'SPHINX' %}DOCS_BUILDDIR = docs/build{% endif %}
{% if cookiecutter.docs_format == 'Quarto' %}REPORT_STEM = docs/report{% endif %}

ifeq ($(OS),Windows_NT)
	INSTALL_CMDSTAN_FLAGS = --compiler
	ACTIVATE_VENV = .venv/Scripts/activate
else
	INSTALL_CMDSTAN_FLAGS =
endif

$(ACTIVATE_VENV):
	python -m venv .venv --prompt={{cookiecutter.repo_name}}

{% if cookiecutter.docs_format != 'No docs' %}docs: $(ENV_MARKER)
	. $(ACTIVATE_VENV) && (\{% endif %}
		{% if cookiecutter.docs_format == 'Sphinx' %}sphinx-build "$(DOCS_SOURCE)" "$(DOCS_BUILDDIR)" -b html; \
    {%- elif cookiecutter.docs_format == 'Quarto' -%}quarto render $(REPORT_STEM).qmd; \
		{%- endif %}
{% if cookiecutter.docs_format != 'No docs' %}	){% endif %}

$(ENV_MARKER): $(ACTIVATE_VENV) $(REQUIREMENTS_FILE) $(CMDSTAN)
	. $(ACTIVATE_VENV) && (\
	  python -m pip install --upgrade pip; \
		python -m pip install -e .; \
	  install_cmdstan $(INSTALL_CMDSTAN_FLAGS); \
		touch $@ ; \
	)

analysis: $(ENV_MARKER)
	. $(ACTIVATE_VENV) && (\
	  {% if cookiecutter.create_tests_directory %}python -m pytest || exit 1; \{% endif %}
	  python $(SRC)/prepare_data.py || exit 1; \
	  python $(SRC)/sample.py || exit 1; \
	  jupyter execute $(SRC)/investigate.ipynb || exit 1; \
	)

{% if cookiecutter.docs_format != 'No docs' %}clean-docs:{% endif -%}
	{% if cookiecutter.docs_format == 'Sphinx' -%}$(RM) -r $(DOCS_BUILDDIR)
	{%- elif cookiecutter.docs_format == 'Quarto' %}
	$(RM) $(shell find $(DOCS_DIR) -iname "$(REPORT_STEM).*" -type f -not -name "*.qmd")
	{%- endif %}

clean-stan:
	$(RM) $(shell find ./$(SRC)/stan -perm +100 -type f) # remove binary files
	$(RM) $(SRC)/stan/*.hpp

clean-inferences:
	$(RM) $(shell find ./inferences/* -type f -not -name "*.toml")

clean-plots:
	$(RM) -r plots/*.png

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-inferences clean-plots {% if cookiecutter.docs_format != 'No docs' %}clean-docs{% endif %}
