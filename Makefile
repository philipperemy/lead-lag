all:
	make install

install:
	python -m pip install --upgrade pip
	pip install cython
	python setup.py build_ext --inplace
	pip install -e .

uninstall:
	pip uninstall -y lead-lag

clean:
	rm -rf *.out lead_lag/*.c *.bin *.exe *.o *.a lead_lag/*.so build *.html __pycache__ lead_lag/__pycache__ notebooks/.ipynb_checkpoints/

deploy:
	python setup.py sdist
	pip install twine
	twine upload dist/*

jupyter:
	pip install jupyter
	cd notebooks && jupyter notebook lead_lag_example_2.ipynb

test:
	python -c "import lead_lag; print('success')"
	cd examples && python small.py
	cd examples && python example_synthetic_data.py
