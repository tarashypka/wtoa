### Walmart & Amazon marketplaces products & prices data analysis  


```
$ export PROJNAME=wtoa.git PROJPATH=$(pwd)
$ conda env create --file=$PROJPATH/config/ENVIRONMENT
$ mkdir -p $ANACONDA_HOME/envs/$PROJNAME/etc/conda/{activate.d, deactivate.d}
$ ln -s $PROJPATH/config/env_vars.sh $ANACONDA_HOME/envs/$PROJNAME/etc/conda/activate.d/
$ source activate $PROJNAME
```
