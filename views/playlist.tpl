<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>Playlists</title>
  <style>
img { 
  image-rendering: pixelated;
}
  </style>
  </head>

  <body>
    <h1>Playlists</h1>

  {{line['number']}},{{line['name']}}
% for line in playlist :
  {{line['number']}},{{line['name']}}
% end

  </body>
</html>
