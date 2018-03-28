#!/bin/bash
#SBATCH --job-name=trainFEL
#SBATCH --time=01:30:00
#SBATCH -p aaiken
#SBATCH -p gres 1
#SBATCH --nodes=1

module load py-keras
module load py-tensorflow
cd ${HOME}/SLAC_FEL_data/training
python forward-keras.py

