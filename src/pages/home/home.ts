import { Component, ViewChild } from '@angular/core';
import { NavController } from 'ionic-angular';
import { SignaturePad } from 'angular2-signaturepad/signature-pad';
import { ToastController } from 'ionic-angular';

function getFileFromServer(url, doneCallback) {
    var xhr;

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = handleStateChange;
    xhr.open("GET", url, true);
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
  signature = '';
  formLoaded = false;
  isDrawing = false;
  signStarted = false;
  formAsImg = null;
  config = {
    'serverPathLocal' : '/sigma/testOrdi',
    'serverPath' : 'https://ordination-kutschera.at/sigma/testOrdi'
  }
  formURL = '';
  sigURL = '';

  @ViewChild(SignaturePad) signaturePad: SignaturePad;
  private signaturePadOptions: Object = { // Check out https://github.com/szimek/signature_pad
    'minWidth': 1,
    //'maxWidth': 2,
    'minDistance': 0,
    'canvasWidth': 992,
    'canvasHeight': 1403,
    'backgroundColor': '#f6fbff',
    'penColor': '#666a73'
  };

  constructor(public navController: NavController, public toastCtrl: ToastController) {}

  ionViewDidEnter() {
    this.signaturePad.clear()
    //---check for local development---
    this.formURL = (this.testFlag ? this.config.serverPathLocal : this.config.serverPathLocal) + "/form.txt";
    this.sigURL = (this.testFlag ? this.config.serverPathLocal : this.config.serverPathLocal) + "/saveImg.php";
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
            this.formAsImg = "data:image/jpeg;base64, " + text;
            this.signaturePad.fromDataURL(this.formAsImg, {width: 992, height: 1403});
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
    //--- if form has been downloaded, draw it again --
    if(this.formAsImg) {
      this.signaturePad.fromDataURL(this.formAsImg, {width: 992, height: 1403});
    }
  }
}
