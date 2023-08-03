![grafana_screenshot](https://github.com/DJ1975-SE/plantmaster2000/blob/main/presentation/latest-example.png)

# plantmaster2000 web interface

Straight PHP with prepared mysql. latest.php presents the last few images, scaled down. The idea is to include latest.php with different MACs as iframes into a grafana dashboard.

A helper script named "batchexport.php" pulls the last X images from the database and writes them to disk. This can be helpful in order to create timelapse movies.

# Using
* adjust values and read the comments in ```dbConfig.php```
* to view the HTML and the last few images, call ```latest.php?devicemac=ccdba75b``` in a browser (assuming you have an ESP32Cam with that MAC)
* bugs likely. Keep an eye on your logfiles.

# Prerequisites
* Tested with apache, php8, and mysql 10.5

# TODO
* which php modules are needed, specific config? probably not
* polishing, remaining web scripts
