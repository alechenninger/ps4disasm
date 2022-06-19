# how things work

## events and cutscenes

See EventPtrs for how "event index" (event_index ram addr) is used. Dialog F6 control code hooks up
into this (see `GetEventFromDialogue`). Use when not already within an event. Enables any NPC dialog
to hook into event also. These run `FieldRoutine_Event`, which may in turn run a cutscene instead.

Cutscenes are similar to other events. They use the same event index, but with the 16th bit set (
0x80__). However, they use a different routine `FieldRoutine_Cutscene` and different map load flag 
when done. Probably because cutscenes don't render the field.

Map events are different, they are events which are checked on every move, so they can trigger at 
arbitrary conditions. See RunEventsJmpTbl. RunEvent routines are just what check if an event should
trigger, what's triggered is the usual event kind using event_index per above.
