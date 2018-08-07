import { Component, ViewChild } from '@angular/core';
import { NavController } from 'ionic-angular';
import { SignaturePad } from 'angular2-signaturepad/signature-pad';
import { Storage } from '@ionic/storage';
import { ToastController } from 'ionic-angular';
import { File } from '@ionic-native/file';

// function download(dataURL, filename) {
// function getDataUri(url, callback) {
//     var image = new Image();
//
//     image.onload = function () {
//         var canvas = document.createElement('canvas');
//         canvas.width = image.naturalWidth; // or 'width' if you want a special/scaled size
//         canvas.height = image.naturalHeight; // or 'height' if you want a special/scaled size
//
//         canvas.getContext('2d').drawImage(image, 0, 0);
//         alert("!");
//         //or get as Data URI
//         callback(canvas.toDataURL('image/jpeg'));
//     };
//     image.crossOrigin = 'anonymous';
//     image.src = "http://ordination-kutschera.at/sigma/Test_Unterschrift.jpg";
//
// }


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
  signature = '';
  formLoaded = false;
  isDrawing = false;
  testFlag = true;
  formAsImg = null;
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

  constructor(public navController: NavController, public storage: Storage, public toastCtrl: ToastController, public file: File) {}

  ionViewDidEnter() {
    this.signaturePad.clear()
    this.storage.get('savedSignature').then((data) => {
      this.signature = data;
    });
    //---check for local development---
    this.formURL = (this.testFlag ? "/sigma/form.txt"  : "https://ordination-kutschera.at/sigma/form.txt");
    this.sigURL = (this.testFlag ? "/sigma/saveImg.php"  : "https://ordination-kutschera.at/sigma/saveImg.php");
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
  }

  drawStart() {
    this.isDrawing = true;
  }

  savePad() {
    //--- save signature locally and clear form ---
    this.signature = this.signaturePad.toDataURL();
    this.storage.set('savedSignature', this.signature);
    this.signaturePad.clear();
    this.formLoaded = false;
    this.formAsImg = null;

    //--- save on server ---
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
    //--- if form has been downloaded, draw it again --
    if(this.formAsImg) {
      this.signaturePad.fromDataURL(this.formAsImg, {width: 992, height: 1403});
    }
  }
}
