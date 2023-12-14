<?php
require 'vendor/autoload.php'; // include Composer's autoloader
 
$client = new MongoDB\Client("mongodb://localhost:27017");

$collection = $client->kuchikomi->post;
$cursor = $collection->find();

foreach ($cursor as $document) {
    var_dump($document);
}
?>