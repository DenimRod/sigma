<?php
$imgString = $_POST['image'];

if ($_POST['type'] == "form"){
  $myfile = fopen("form.txt", "w");
  fwrite($myfile, $imgString);
  fclose($myfile);
}

else if ($_POST['type'] == "signature"){
  $myfile = fopen("signature.txt", "w");
  fwrite($myfile, $imgString);
  fclose($myfile);
}
?>
