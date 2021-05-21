# This folder contains the code to compile and upload a view that does the analysis to CouchDB

- Run `npm install` to install dependencies
- Run `npm run build` to build the view
- Run `npm run upload` to upload the view to couchDB
  - Set environment variable `backendUrl` to the url of webservices before running
  - Or use `backendUrl=URL npm run upload`