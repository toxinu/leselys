#!/bin/bash
STATIC_PATH="leselys/static"

if [ -z $(which npm) ]; then
	echo "!! Need nodejs and npm to minify"
	echo "!! Or use your own script"
	exit 1
fi

if [ -z $(which uglifyjs) ]; then
	echo ":: Installing js minifier"
	sudo npm install -g uglify-js
fi

if [ -z $(which uglifycss) ]; then
	echo ":: Installing css minifier"
	sudo npm install -g uglifycss
fi

echo ":: Minify javascripts"

uglifyjs 	$STATIC_PATH/js/crel.js  \
	 		$STATIC_PATH/js/mousetrap.js \
	 		$STATIC_PATH/js/tinybox.js \
		 	$STATIC_PATH/js/ajax.js \
 			$STATIC_PATH/js/api.js \
 			$STATIC_PATH/js/leselys.js \
 			-o $STATIC_PATH/js/leselys.min.js

echo ":: Minify css"

uglifycss 	$STATIC_PATH/css/font-awesome.css \
			$STATIC_PATH/css/bootstrap-responsive.css \
			$STATIC_PATH/css/leselys.css \
			> $STATIC_PATH/css/leselys.min.css

uglifycss 	$STATIC_PATH/css/bootstrap.css > $STATIC_PATH/css/bootstrap.min.css
uglifycss 	$STATIC_PATH/css/journal.css > $STATIC_PATH/css/journal.min.css
uglifycss 	$STATIC_PATH/css/readable.css > $STATIC_PATH/css/readable.min.css
uglifycss 	$STATIC_PATH/css/flat-ui.css > $STATIC_PATH/css/flat-ui.min.css
