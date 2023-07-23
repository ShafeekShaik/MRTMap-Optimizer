from flask import render_template, flash
from app import app
from app.forms import PathForm
from flask import request
from app.algorithm import short_path_finder
from config import basedir
import csv
import os

mrt_names= []
csv_file= os.path.join(basedir,'app','mrt.csv')
# basedir"S:/SIT Tri 3/DSAG/Projec/hub/Project_input/Attendance/MRTMap-Optimizer/app/mrt.csv"
with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mrt_names.append(row['Source'])
mrt_names = list(dict.fromkeys(mrt_names))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PathForm()
    searched=False
    if request.method == 'POST':
        startpoint = request.values.get('startpoint')  # Your form's
        endpoint = request.values.get('endpoint')  # input names
        print(startpoint)
        print(endpoint)
        if startpoint not in mrt_names:
            flash("Startpoint is not an MRT station")
            path = ""
            timing = ""
        elif  endpoint not in mrt_names:
            flash("Endpoint is not an MRT station")
            path = ""
            timing = ""

            
        else:
            searched=True
            timing, path = short_path_finder(startpoint, endpoint)
    else:
        path = ""
        timing = ""
    return render_template('index.html', title='Home', form=form, timing=timing, path=path, mrt_names=mrt_names,searched=searched)


@app.route('/short_path')
def short_path():
    return render_template('shortest_path_map.html')

if __name__ == "__main__":
    app.run(debug=True)
