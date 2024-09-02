const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const base64Stream = require('base64-stream');

// Get the directory of server.js
const serverDirectory = __dirname;

class APIPrint {
    constructor(urlList, downloadPath) {
        this.urlList = urlList;
        this.downloadPath = downloadPath;
    }

    waitForTimeout(delay) {
        return new Promise(resolve => setTimeout(resolve, delay));
    }

    async apiCallBack() {
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--window-size=1920,1080'],
        });
        const page = await browser.newPage();
    
        // Set download behavior for Chromium-based browsers
        const client = await page.target().createCDPSession();
        await client.send('Page.setDownloadBehavior', {
            behavior: 'allow',
            downloadPath: this.downloadPath,
        });
    
        const filenames = [];
    
        // Ensure the download directory exists
        if (!fs.existsSync(this.downloadPath)) {
            fs.mkdirSync(this.downloadPath, { mode: 0o777 });
        }
    
        for (const url of this.urlList) {
            try {
                await page.goto(url, { waitUntil: 'domcontentloaded' });
                const originalFiles = new Set(fs.readdirSync(this.downloadPath));
    
                let newFiles = [];
                const maxRetries = 20;
                let retries = 0;
    
                while (retries < maxRetries) {
                    const currentFiles = new Set(fs.readdirSync(this.downloadPath));
                    newFiles = [...currentFiles].filter(x => !originalFiles.has(x));
    
                    if (newFiles.some(name => name.includes('Unconfirmed'))) {
                        console.log('Downloading files...');
                        await this.waitForTimeout(5000); // Call this.waitForTimeout
                    } else if (newFiles.length > 0) {
                        console.log('Download complete:', newFiles);
                        filenames.push(...newFiles);
                        break;
                    } else {
                        retries++;
                        console.log('Waiting for download...', retries);
                        await this.waitForTimeout(2000); // Call this.waitForTimeout
                    }
                }
    
                if (newFiles.length === 0) {
                    console.error('No new files were downloaded after max retries.');
                }
    
            } catch (error) {
                console.error('Error during download:', error);
            }
        }
    
        await browser.close();
        return filenames;
    }
}

const app = express();
app.use(bodyParser.json());

app.post('/print', async (req, res) => {
    const { url, download_path } = req.body;

    // Use the server directory as the base for download path if not provided
    const downloadPath = download_path ? path.resolve(download_path) : path.join(serverDirectory, 'downloads');

    if (!url) {
        return res.status(400).json({ status: 400, message: "URL is missing from request" });
    }

    const urls = Array.isArray(url) ? url : [url];
    const printAPI = new APIPrint(urls, downloadPath);

    try {
        const filenames = await printAPI.apiCallBack();

        if (filenames.length > 0) {
            const firstFilePath = path.join(downloadPath, filenames[0]);

            // Ensure the file exists before attempting to read it
            if (fs.existsSync(firstFilePath)) {
                const fileStream = fs.createReadStream(firstFilePath);
                const base64Encode = new base64Stream.Base64Encode();
                let base64Data = '';

                fileStream.pipe(base64Encode);

                base64Encode.on('data', (chunk) => {
                    base64Data += chunk.toString();
                });

                base64Encode.on('end', () => {
                    // Send the response before deleting the file
                    res.json({ status: 200, base64: base64Data });
                    
                    // Delete the file after sending the response
                    fs.unlinkSync(firstFilePath);
                });

                base64Encode.on('error', (error) => {
                    console.error('Error encoding file:', error);
                    fs.unlinkSync(firstFilePath); // Ensure file is deleted in case of error
                    res.status(500).json({ status: 500, message: 'Error encoding file' });
                });

            } else {
                res.status(404).json({ status: 404, message: 'File not found' });
            }
        } else {
            res.status(500).json({ status: 500, message: 'No files were downloaded' });
        }

    } catch (error) {
        console.error('Error during print process:', error);
        res.status(500).json({ status: 500, message: 'An error occurred during the print process' });
    }
});

app.get('/help', (req, res) => {
    const data = {
        url: "/print",
        method: "POST",
        body: `
            {
                "url": [],
                "download_path": ""
            }
        `,
        example: `
            {
                "url": [
                    "https://gis.collaboratoronline.com/search?mapName=Channels&zoomLevel=8&editing=False&print=True&gpsCoordinates=30.092722446611162,-27.730076537015975&geoserverurl=https://geoserver.collaboratoronline.com/geoserver#"
                ],
                "download_path": "/home/username/Downloads"
            }
        `
    };
    res.json(data);
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
