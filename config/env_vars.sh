#!/bin/sh

export PROJNAME=wtoa.git
export ENVPATH=$ANACONDA_HOME/envs/$PROJNAME
export PROJPATH=$HOME/Workspace/python/$PROJNAME
export PYTHONPATH=$ENVPATH/bin:$PROJPATH/src
export LOG_CFG=$PROJPATH/config/logging.yaml
