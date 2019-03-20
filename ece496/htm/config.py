#*** CONSTANTS
DATA_FOLDER = './out' #this is relative to the working directory of start_prediction.py
MODEL_PARAMS_PATH = "model_params/model_params.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PROM_USER = "admin"
PROM_PASS = "admin"


#*** GETTER FUNCTIONS
def getCsvFile(mode,container,part):
    #container: ue (default) or base
    #part: cpu (default) or mem
	if mode == 'prom':
	    return "{0}/{1}_{2}_prediction.csv".format(folder,container,part)
	else:
		return "./out/realtime_prediction.csv"
