#!/bin/bash
#SBATCH --job-name=trainFEL
#SBATCH --time=01:30:00
#SBATCH -p aaiken
#SBATCH --gres gpu:1
#SBATCH --nodes=1

source ${HOME}/setup.bash
module load py-keras
module load py-tensorflow
cd ${HOME}/SLAC_FEL_data/training
python forward_keras.py

