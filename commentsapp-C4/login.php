<?php
/**
 * Created by IntelliJ IDEA.
 * User: GaryPC
 * Date: 09/02/2015
 * Time: 20:51
 */
$servername = "localhost";
$username = "root";
$password = "gaz360";
$dbname = "myDB";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$pass = md5($_POST['Password']);



$sql = "SELECT * FROM obdreader.owner WHERE obdreader.owner.email = \"gazlynam@lynam.com\" AND password = \"1a1dc91c907325c69271ddf0c944bc72\";";


$url = "webApp.html";
if ($conn->query($sql) === TRUE) {
    header( "Location: $url" );
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
