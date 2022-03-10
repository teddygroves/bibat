.PHONY: clean-runs clean-plots clean-stan clean-all analysis

analysis:
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
