
PYTHON = python
VENV = venv/bin/activate



setup:
	python -m venv venv
	. $(VENV) && pip install -U pip && pip install -r requirements.txt


quick:
	. $(VENV) && $(PYTHON) main_quick.py


run:
	. $(VENV) && $(PYTHON) main.py


plots:
	. $(VENV) && $(PYTHON) main.py


clean:
	rm -f *.csv *.png
	rm -rf __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -r {} +


test:
	. $(VENV) && pytest -v tests/


all: setup run plots
