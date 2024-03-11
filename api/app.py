from flask import Flask, request, json, jsonify
from printing import APIPrint
import base64
import os
import json
import requests

app = Flask(__name__)

@app.route('/print', methods=["POST"])
def printPdf():

    if request.method == 'POST':
        data = request.json
        if data["url"] is None:
            return jsonify({"status": 500, "message": "url is missing from request"})
        if data["download_path"] is None:
            return jsonify({"status": 500, "message": "download path is missing from request"})
        
        urls = list(data["url"])
        download_path = data["download_path"]
        printAPI = APIPrint(urls, download_path)
        filenames = printAPI.apiCallBack()
        with open(f"{download_path}/{filenames[0]}", "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        os.remove(f"{download_path}/{filenames[0]}")

        return jsonify({"status": 200, "base64": str(encoded_string)})

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    app.run(debug=True, host='0.0.0.0', port=port)