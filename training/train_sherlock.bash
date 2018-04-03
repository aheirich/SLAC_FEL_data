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

NUM_HIDDEN_LAYERS=2
NUM_HIDDEN_UNITS_PER_LAYER=2048
LEARNING_RATE=0.00001
EPOCHS=25000
DIRECTION=forward
ROOT=$SCRATCH/checkpoint/${DIRECTION}_${NUM_HIDDEN_LAYERS}_${NUM_HIDDEN_UNITS_PER_LAYER}

python train_keras.py ${NUM_HIDDEN_LAYERS} ${NUM_HIDDEN_UNITS_PER_LAYER} ${LEARNING_RATE} ${EPOCHS} ${DIRECTION} ${ROOT}


