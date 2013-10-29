// Get XHR Object
function getXMLHttpRequest() {
    var xhr = null;
    if (window.XMLHttpRequest || window.ActiveXObject) {
        if (window.ActiveXObject) {
            try {
                xhr = new ActiveXObject("Msxml2.XMLHTTP");
            } catch(e) {
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
            }
        } else {
            xhr = new XMLHttpRequest();
        }
    } else {
        alert("Browser not supported (XMLHTTPRequest).");
        return null;
    }
    return xhr;
}

function sendFile(options){
  var form = new FormData();
  form.append('file', options['params']['fileInput']);

  var xhr = getXMLHttpRequest();
  xhr.open("POST", options['url']);

  // Bind 'readystatechange'
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      if (xhr.status == 200 || xhr.status == 0) {
        var data = xhr.responseText;

        // Try parsing to JSON
        try { data = JSON.parse(data); } catch(e) {
          window.location = "";
        };

        if (options['callback'])
          options['callback'](xhr, data);

      } else {
        var data = {success: false, content: {}}
        if (options['callback'])
          options['callback'](xhr, data);
      }
    }
  }
  xhr.send(form);
  return xhr;
}

function ajaxRequest(options){

  if (options == undefined)
    return false;

  var default_options = {
    url: undefined,
    method: "GET",
    params: {},
    callback: undefined,
    headers: {}
  };

  // Merge options
  for (var key in default_options)
    if (! options[key])
      options[key] = default_options[key];

  // Check URL
  if (options['url'] == undefined)
    return false;

  var xhr = getXMLHttpRequest();

  // Bind 'readystatechange'
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4) {
      if (xhr.status == 200 || xhr.status == 0) {
        var data = xhr.responseText;

        // Try parsing to JSON
        try { data = JSON.parse(data); } catch(e) {
          window.location = "";
        };

        if (options['callback'])
          options['callback'](xhr, data);

      } else {
        var data = {success: false, content: {}}
        if (options['callback'])
          options['callback'](xhr, data);
      }
    }
  }

  var params = "";
  for (var key in options['params'])
    params += "&" + key + "=" + options['params'][key]

  // Remove first char
  if (params.length)
    params = params.substr(1-params.length);

  // Add params in URL for GET method
  if (params.length && options['method'] == "GET")
    options['url'] += "?" + params;

  // Open XHR
  xhr.open(options['method'], options['url'], true);

  // Set headers
  if (options['method'] == "POST")
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  for (var key in options['headers'])
    xhr.setRequestHeader(key, options['headers'][key]);

  // Send Request
  if (options['method'] == "GET")
    xhr.send(null);

  else if (options['method'] == "POST")
    xhr.send(params);

  else
    xhr.send(null);

  return xhr;
}
