# sigma
is a SIGnature MAker for ganyMED, a medical software suite. It is based on LibreOffice, Basic, python, PHP and the Ionic Framework.

The Architecture can be described as following:

1. ganyClient (ganyMED -> LibreOffice + Basic and Python Macros)
2. Server (PHP)
3. ionicClient (Ionic)

##Installation
1. Clone the Repository
2. Install the necessary node_modules (npm install)
3. Run the app (ionic serve)

**ionicClient**
Package the App and send it to your Device.

**ganyClient**
Move to the "non_ionic" folder and adapt all the Paths in

* macros.py
* the Basic Scripts inside KD_Sigma_v**.odt

so that they match your desired Location.

Now you can Copy the .odt File and include it as a form in ganyMED.
