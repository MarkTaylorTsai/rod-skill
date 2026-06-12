.PHONY: test validate

test:
	python -m pytest -q

validate:
	python -m rod_skill.cli validate skill.json
	python -m rod_skill.cli validate skills/rod-architecture/skill.json
	python -m rod_skill.cli validate skills/rod-goal-loop/skill.json
