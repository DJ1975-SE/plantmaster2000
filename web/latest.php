<?php
	include 'header-dark.php';
	// Include the database configuration file
	require_once 'dbConfig.php';
	$cleanid=1000;
	$cleandevicemac="";
	$cleanoperator="down";
	$macpattern="/^[a-fA-F0-9]{8}$/";

	// sanitize user input, we only use devicemac in latest
	if (isset($_GET["id"])) {
		$cleanid = htmlspecialchars($_GET["id"]);
	}
	if (isset($_GET["devicemac"])) {
		$cleandevicemac = htmlspecialchars($_GET["devicemac"]);
	}
	if (isset($_GET["operator"])) {
		$cleanoperator = htmlspecialchars($_GET["operator"]);
	}
	echo "<code><table>";
	date_default_timezone_set($config_timezone);
	$now = new DateTime('now', new DateTimeZone($config_timezone));
	echo "<tr>";

	// We fetch more images than we need because there might be gaps (and we are lazy)
	$imagesql = "SELECT ts,id,b64photo,devicemac FROM snapshot WHERE devicemac = ? ORDER BY ts DESC LIMIT " . strval($latest_no_images + 5);
	$imagestmt = $db->prepare($imagesql);
	$imagestmt->bind_param("s",$cleandevicemac);
	$imagestmt->execute();
	$imageresult = $imagestmt->get_result();


	if($imageresult->num_rows > 0){
		$i = 0;
        	while(($imagerow = $imageresult->fetch_assoc()) && $i < $latest_no_images) {
			// calculate how old this photo is
			$thistime = (new DateTime($imagerow['ts'], new DateTimeZone($config_timezone)));
			$diffts = $thistime->diff($now);

			// prepare the image
			$thumb = imagecreatetruecolor($thumb_width, $thumb_height);
			$source = imagecreatefromstring(base64_decode($imagerow['b64photo']));
			$orig_width  = imagesx($source);
			$orig_height = imagesy($source);
		        // Resize to thumb size
			if ($i < ($latest_no_images - 1)) {
			        imagecopyresized($thumb, $source, 0, 0, 0, 0, $thumb_width, $thumb_height, $orig_width, $orig_height);
			        // Output
				echo "<td><b>" . $diffts->format('%a days %H h %I m %S s') . "</b><br>";
			}
			// create a thumb made of 4 smaller thumbs
			// not sure how much nense this makes but it was interesting to get working.
			else {
				$offsetx=0;
				$offsety=0;
				for ($j=0; $j < 4; $j++) {
					switch($j) {
						case 0:
							$offsetx = 0;
							$offsety = 0;
							break;
						case 1:
							$offsetx = $thumb_width/2;
							$offsety = 0;
							break;
						case 2:
							$offsetx = 0;
							$offsety = $thumb_height/2;
							break;
						case 3:
							$offsetx = $thumb_width/2;
							$offsety = $thumb_height/2;
							break;
					}
					imagecopyresized($thumb, $source, $offsetx, $offsety, 0, 0, $thumb_width/2, $thumb_height/2, $orig_width, $orig_height);
					$imagerow = $imageresult->fetch_assoc();
					$source = imagecreatefromstring(base64_decode($imagerow['b64photo']));
				}
			        // Output
				echo "<td>last 4<br>";
			}

			// output the actual image as a base64 encoded stream directly in the HTML
	        	echo "<img src=\"data:image/jpg;charset=utf8;base64,";
			ob_start();
 			 imagejpeg($thumb);
	 		 $image_data = ob_get_contents();
			ob_end_clean();
			echo base64_encode($image_data);
			echo "\" />\n</a>\n";
			echo "<br><code>" . $imagerow['ts'] . "&nbsp;-&nbsp;" . $imagerow['devicemac'];
			echo "</code></td>";
			$i++;
		}
		echo "</tr>";
		imagedestroy($thumb);
		imagedestroy($source);
	}
	echo "</table>";
	echo "</body></html>";
?>
