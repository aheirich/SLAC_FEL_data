#!/bin/bash
#SBATCH --job-name=trainFEL
#SBATCH --time=08:00:00
#SBATCH -p aaiken
#SBATCH --gres gpu:1
#SBATCH --nodes=1

source ${HOME}/setup.bash
module load py-keras
module load py-tensorflow
cd ${HOME}/SLAC_FEL_data/training

for NUM_HIDDEN_LAYERS in 2 3 4 
do
  for NUM_HIDDEN_UNITS_PER_LAYER in 1024 2048 4096
  do
    python forward_keras.py ${NUM_HIDDEN_LAYERS} ${NUM_HIDDEN_UNITS_PER_LAYER}
  done
done


