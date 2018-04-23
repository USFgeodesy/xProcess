# xProcess
code for processing using GipsyX 
## To install it:

cd /dir/with/xProcess/

open the file station.py

edit line 27:

ionfile = '/home/nvoss/goa-var/cddis.gsfc.nasa.gov/gps/products/ionex'
such that it points to the directory where your ionex files are...

python setup.py install

This will create 3 new python modules. 
  1. station
  2. network
  3. timeseries class (does not do anything yet)

## You can call the modules by: 
```python
import station
import network
```

You can then write a python script to run your process or even interactively. 
Example of processing is [here](https://github.com/USFgeodesy/xProcess/blob/master/example_notebooks/GIPSY-X%20with%20xProcess%20example.ipynb)
