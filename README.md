# email_tracker
email_tracker is a program to track when emails have been opened and/or forwarded.
It works by adding a very small image to an email, that is hosted on a server. 
When the image is loaded, the server looks up the images unique identifier and links it to a recipient. 
This program will then notify the user of that email being opened.

# usage
add the client, copy the uuid from 'clients.json', add an image to an email with the image location as http://your.server/images/<uuid>/<anything>, e.g: http://localhost:1337/images/4efa58e6-41db-4ab8-a543-c5e782764524/hackerman.png
