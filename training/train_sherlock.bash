#!/bin/bash
#SBATCH --job-name=FELforward
#SBATCH --time=32:00:00
#SBATCH -p aaiken
#SBATCH --gres gpu:1
#SBATCH --nodes=1

source ${HOME}/setup.bash
module load py-keras
module load py-tensorflow
cd ${HOME}/SLAC_FEL_data/training

NUM_HIDDEN_LAYERS=2
NUM_HIDDEN_UNITS_PER_LAYER=2048
LEARNING_RATE=0.1
EPOCHS=2000
OPTIMIZER=SGD
DIRECTION=forward
ROOT=$SCRATCH/checkpoint/${DIRECTION}_${OPTIMIZER}_${NUM_HIDDEN_LAYERS}_${NUM_HIDDEN_UNITS_PER_LAYER}

python train_keras.py ${NUM_HIDDEN_LAYERS} ${NUM_HIDDEN_UNITS_PER_LAYER} ${LEARNING_RATE} ${EPOCHS} ${OPTIMIZER} ${DIRECTION} ${ROOT}


