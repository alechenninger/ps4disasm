# notes

# todo

## italics

clean up font files

compile to italics in charset

use markdown or html (gdocs addon can spit out either. alternatively can consider a custom google app script to do more)

## preview output

show where lines will break?

## workflow

scene compiler in dart
compile to gdoc addon

https://medium.com/@florian_32814/google-apps-scripts-with-dart-402c042fa606
https://pub.dev/packages/apps_script_tools

web server to do actual assembly compilation

https://github.com/googleworkspace/apps-script-oauth2
https://developers.google.com/apps-script/reference/script/script-app#getoauthtoken

only thing missing is git commit
it is possible to use github API from app script also
but if its easy to copy from gdocs, not too big of a deal

## dsl

script and events

how to deal with event code we don't want a dsl for without cluttering up the dsl?

Could just add select custom keywords for specific points.

```
Alys: Maybe so...
Movement: Party stops following leader
Event:
  Move: Alys to 592, 592
Event:
  Movement: Y axis first
  Move: Alys to $2A0, $250
  Move: Shay to $280, $250
Event:

Alys: 
```

```
