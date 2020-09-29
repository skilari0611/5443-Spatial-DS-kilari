from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import numpy as np
import folium
from scipy import spatial
from scipy.spatial import KDTree
import json


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/click/')
def click():
    # lat = request.args.get("lat",None)
    # lng = request.args.get("lng",None)
    # lnglat = request.args.get("lnglat",None)
    lat, lng = request.args.get("lngLat", None).split(",")


    f = open('airports.json')
    data = json.load(f)

    latLon = []

    for key, value in data.items():
        latLon.append([data[key]['lat'], data[key]['lon']])


    latLonArray = np.array(latLon)

    tree = KDTree(latLonArray, 2)  # doctest: +SKIP


    tree3 = spatial.KDTree(latLon)
    p1 = [(float(lng), float(lat))]
    v, x = tree.query(p1[0])

    temp3 = latLon[x]

    dist, ind = tree.query(temp3,  k=6)

    tempOutput = []
    for x in ind:
        tempOutput.append(latLonArray[x])
        print(latLonArray[x])

    output = np.array(tempOutput)


    m = folium.Map(location=output[0], zoom_start=12)

    for point in range(0, len(output)):
        folium.Marker(output[point], icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    m

    m.save("output.html")
    return "output.html"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
