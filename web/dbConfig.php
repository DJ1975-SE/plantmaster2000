<?php
	// Database configuration
	$dbHost     = "192.168.1.109";
	$dbUsername = "user";
	$dbPassword = "password";
	$dbName     = "plantmaster2k";

	// Create database connection
	$db = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);

	// Check connection
	if ($db->connect_error) {
		die("Connection failed: " . $db->connect_error);
	}

	// example values that works for me, adjust as you see fit
	$thumb_width = 320;
	$thumb_height = 240;
	$orig_width = 1280;
	$orig_height = 1024;
	$thumbview_images = 24;
	$sorted_no_images = 5;
	$latest_no_images = 2;
	$config_timezone = "Europe/Berlin";

	// this is for the mass export script "batchexport.php"
	// if you want to pull out the last NNN images from the database.
	// think timelapse movies, for example

	// in $batch_path, after you ran "php batchexport.php" from a shell, issue
	// ffmpeg -framerate 10 -pattern_type glob -i "*-addrreess-*.jpg" -s:v 1280x1024 -b:v 5000k timelapse.avi
	// do not expect the above to be the best way, but its one way.
	$batch_rotate = 0;
	$batch_files = 400;
        $batch_path = "/mount/htdocs/pm2k-export";
	$batch_mac = "aaddrreess";
?>
