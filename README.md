# sigma
is a SIGnature MAker for ganyMED, a medical software suite. It is based on LibreOffice, Basic, python, PHP and the Ionic Framework.

The architecture can be described as following:

1. ganyClient (ganyMED -> LibreOffice + Basic and Python Macros)
2. Server (PHP)
3. ionicClient (Ionic)

## Installation
1. Clone the repository
2. Install the necessary node_modules (npm install)
3. Run the app (ionic serve)

**Server**

Create a new subdirectory sigma/yourName for every instance using sigma individually.

**ionicClient**

Edit the config object im home.ts to point to the correct server URL.
Then package the app and send it to your device.

**ganyClient**

Copy the `sigma_vorlage.odt` file plus the `sigma_files` directory.
Edit the `config.json` to point to the correct server URL.

Now you're ready to go - adapt the .odt file to your demands and import it as a form in ganyMED.
