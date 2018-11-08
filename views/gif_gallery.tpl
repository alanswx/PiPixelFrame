<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>LCD Gallery</title>
  <style>
img { 
  image-rendering: pixelated;
}
  </style>
  </head>

  <body>
    <h1>Gallery</h1>

% for anim in animations:
  <a href="/showgif/{{anim['name']}}">[show]</a>
  {{anim['name']}}: <img src="{{anim['name']}}" height=64><br>
% end

  </body>
</html>
