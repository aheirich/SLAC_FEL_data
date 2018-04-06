all:	mse.log

mse.log:	FEL_INPUT_SCALED.py FEL_OUTPUT_SCALED.py verify_forward_inference.py
	python verify_forward_inference.py > mse.log

clean:
	rm -f mse.log
