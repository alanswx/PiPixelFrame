<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>Playlist Gallery</title>
  <style>
img { 
  image-rendering: pixelated;
}
  </style>
  </head>

  <body>
    <h1>Gallery</h1>

% for anim in playlists:
  <a href="/{{anim['name']}}">[edit]</a>
  <a href="/playshow/{{anim['name']}}">[show]</a>
  {{anim['name']}} <br>
% end

  </body>
</html>
