from flask import Flask, request, json, jsonify
from printing import APIPrint

app = Flask(__name__)

@app.route('/print', methods=["POST"])
def print():

    if request.method == 'POST':
        data = request.json
        if data["url"] is None:
            return jsonify({"status": 500, "message": "url is missing from request"})
        if data["download_path"] is None:
            return jsonify({"status": 500, "message": "download path is missing from request"})
        
        urls = list(data["url"])
        download_path = data["download_path"]
        printAPI = APIPrint(urls, download_path)
        printAPI.apiCallBack()
        return jsonify({"status": 200, "message": "success"})

@app.route('/help', methods=["GET"])
def help():
    data = {
        "url": "/print",
        "method": "POST",
        "body": """
            {
                "url": [],
                "download_path": ""
            }
        """,
        "example": """
            {
                "url": [
                    "https://gis.collaboratoronline.com/search?mapName=Channels&zoomLevel=8&editing=False&print=True&gpsCoordinates=30.092722446611162,-27.730076537015975&geoserverurl=https://geoserver.collaboratoronline.com/geoserver#"
                ],
                "download_path": "/home/voogt/Downloads"
            }
        """
    }
    return jsonify(data)