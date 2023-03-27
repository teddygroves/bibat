.PHONY: qa

## Apply code quality assurance tools.
qa:
	black .
	isort .


