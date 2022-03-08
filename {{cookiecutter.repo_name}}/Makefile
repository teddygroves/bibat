.PHONY: clean-results clean-stan clean-all results 

analysis:
	python prepare_data.py
	python sample.py
	python analyse.py

clean-stan:
	$(RM) $(shell find ./src/stan -perm +100 -type f) # remove binary files
	$(RM) ./src/stan/*.hpp

clean-results:
	$(RM) -r results/runs/*/

clean-prepared-data:
	$(RM) -r data/prepared/*/

clean-all: clean-prepared-data clean-stan clean-results
