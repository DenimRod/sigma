import { Component, ViewChild } from '@angular/core';
import { NavController } from 'ionic-angular';
import { SignaturePad } from 'angular2-signaturepad/signature-pad';
import { ToastController } from 'ionic-angular';
import { Platform } from 'ionic-angular';

function getFileFromServer(url, doneCallback) {
    var xhr;

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleStateChange;
    xhr.open("GET", url, true);
      // Set headers to force the form to be reloaded every time
    xhr.setRequestHeader('Cache-control', 'no-cache');
    xhr.setRequestHeader('Cache-control', 'no-store');
    xhr.setRequestHeader('Expires', '0');
    xhr.setRequestHeader('Pragma', 'no-cache');

    xhr.send();

    function handleStateChange() {
        if (xhr.readyState === 4) {
            doneCallback(xhr.status == 200 ? xhr.responseText : null);
        }
    }
}

function putFileOnServer(url, data, doneCallback) {
    var xhr;
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleStateChange;
    xhr.open("POST", url, true);
    xhr.send(data);

    function handleStateChange() {
        if (xhr.readyState === 4) {
            doneCallback(xhr.status == 200 ? xhr.responseText : null);
        }
    }
}

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
  testFlag = true;
  version = 'v1.6';
  signature = '';
  formLoaded = false;
  isDrawing = false;
  signStarted = false;
  formAsImg = null;
  height = 0;
  width = 0;
  config = {
    'serverPathLocal' : '/sigma/testOrdi',
    'serverPath' : 'https://www.ordination-kutschera.at/sigma/testOrdi'
  }
  formURL = '';
  sigURL = '';

  @ViewChild(SignaturePad) signaturePad: SignaturePad;
  public signaturePadOptions: Object = { // Check out https://github.com/szimek/signature_pad
    'minWidth': 1,
    //'maxWidth': 2,
    'minDistance': 0,
    'canvasWidth': 800,
    'canvasHeight': 1120,
    'backgroundColor': '#f6fbff',
    'penColor': '#666a73'
  };

  constructor(public navController: NavController, public toastCtrl: ToastController, public plt: Platform) {}

  ionViewDidEnter() {
    this.formLoaded = false;
    this.signaturePad.clear()
    //---check device size---
    this.width = this.plt.width();
    this.height = this.plt.height();
      //--check, whether width or height is "longest side"--
    if (this.width * 1120 / 800 > this.height) {
      this.width = this.height * 800 / 1120
    }
    else {
      this.height = this.width * 1120 / 800
    }

    this.signaturePad.set("canvasWidth",this.width);
    this.signaturePad.set("canvasHeight",this.height);

    //---check for local development---
    this.formURL = (this.testFlag ? this.config.serverPathLocal : this.config.serverPath) + "/form.txt";
    this.sigURL = (this.testFlag ? this.config.serverPathLocal : this.config.serverPath) + "/saveImg.php";
}

  drawComplete() {
    this.isDrawing = false;

    //--- if no form loaded, drawing serves as reload---
    if(!this.formLoaded) {
      getFileFromServer(this.formURL, (text) => {
          if (text === null) {
              // alert("Error");
          }
          else {
            this.formAsImg = "data:image/png;base64," + text;
            this.signaturePad.fromDataURL(this.formAsImg, {width: this.width, height: this.height});
            this.formLoaded = true;
          }
      });
    }
    //---if form was loaded, drawing activates the buttons for sending/reloading---
    else if (!this.signStarted) {
      this.signStarted = true;
    }
  }

  drawStart() {
    this.isDrawing = true;
  }

  savePad() {
    //--- save signature and clear form ---
    this.signature = this.signaturePad.toDataURL();
      // this.storage.set('savedSignature', this.signature);
    this.signaturePad.clear();
    this.formLoaded = false;
    this.signStarted = false;
    this.formAsImg = null;

    //--- upload on server ---
    let data = new FormData();
    data.append('type', 'signature');
    data.append('image', this.signature);

    putFileOnServer(this.sigURL,data, (text) => {
      //alert(text)
    });

    let toast = this.toastCtrl.create({
      message: 'Neue Signatur gespeichert',
      duration: 3000
    });
    toast.present();
  }

  clearPad() {
    this.signaturePad.clear();
    this.signStarted = false;

    getFileFromServer(this.formURL, (text) => {
        if (text === null) {
            // alert("Error");
        }
        else {
          this.formAsImg = "data:image/png;base64," + text;
          this.signaturePad.fromDataURL(this.formAsImg, {width: this.width, height: this.height});
          this.formLoaded = true;
        }
    });

    // this.signStarted = false;
    // //--- if form has been downloaded, draw it again --
    // if(this.formAsImg) {
    //   this.signaturePad.fromDataURL(this.formAsImg, {width: 800, height: 1120});
    // }
  }
}
