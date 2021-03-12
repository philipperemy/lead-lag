all:
	make install

install:
	python setup.py build_ext --inplace
	pip install -e .

uninstall:
	pip uninstall -y lead-lag

clean:
	rm -rf *.out lead_lag/*.c *.bin *.exe *.o *.a lead_lag/*.so build *.html __pycache__ lead_lag/__pycache__ notebooks/.ipynb_checkpoints/


deploy:
	python setup.py sdist bdist_wheel
	pip install twine
	twine upload dist/*

jupyter:
	pip install jupyter
	cd notebooks && jupyter notebook lead_lag_example_1.ipynb
