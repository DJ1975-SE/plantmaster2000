<?php
	// Include the database configuration file
	require_once 'dbConfig.php';

	// get the base64 encoded images for one specific mac, in order of oldest to newest but start now and go back X photos.
	$imagesql = "SELECT * FROM (SELECT ts,id,b64photo FROM snapshot WHERE devicemac = ? ORDER BY ts DESC LIMIT " . strval($batch_files) . ") AS tmp ORDER BY ts ASC";
	$imagestmt = $db->prepare($imagesql);
	$imagestmt->bind_param("s",$batch_mac);
	$imagestmt->execute();
	$imageresult = $imagestmt->get_result();


	// if we got any resulsts, process them (decode, possibly rotate, and write to disk)
	// name of files can be changed here, for timelapses ther current naming works.
	if($imageresult->num_rows > 0){
		$i = 0;
        	while($imagerow = $imageresult->fetch_assoc()) {
			$source = imagerotate(imagecreatefromstring(base64_decode($imagerow['b64photo'])),$batch_rotate,0);
			echo $imagesql . "\n";
			$outfilename = $batch_path . sprintf('%08d', $i) . "-" . $batch_mac . "-id_" . $imagerow['id'] . ".jpg";
			imagejpeg($source,$outfilename);
			$i++;
		 }
	}
?>
