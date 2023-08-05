from .base_class import Line

import pandas as pd
import numpy as np
import pandas as pd
import pkg_resources

def import_figure_from_csv(path):
    # Create a stream relative to package location
    stream = pkg_resources.resource_stream(__name__, path)

    data = pd.read_csv(stream)

    columns = data.columns.values.tolist()

    Nlines = int(data.shape[1]/2)

    # Make sure array contains floats
    val = data.values[1:]
    val = np.array(val, dtype=np.float)

   
    lines = []
    for i in range(Nlines):
        lines.append(Line(val[:,2*i],val[:,2*i+1], str(columns[2*i])))  # Each line consists of two columns in the dataframe (X,Y)
    
    return lines