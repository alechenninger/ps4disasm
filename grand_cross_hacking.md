# Grand Cross mod guide

Assumes using Rune to generate ASM.

TODO: This guide is probably out of date

## Bootstrapping maps

Using Rune, maps generate sprites, objects, dialog, and events.

Events (and event pointers) are global, so those should be included globally separately (not per map).

1. After the first `$FFFF` in map data, and after any hard-coded sprites add:

   ```asm
   	include "script/maps/{map id}/sprites.asm"
   ```

   (note if you edit a line like `dc.l $FFFF027F` to just `$FFFF`,
   make sure you change `dc.l` to `dc.w`)
2. Edit `_spriteVramOffsets` to set the right offset for this map (look at the first sprite word normally used),
including room for any hard-coded sprites you left. (Each sprite is 0x48 apart)
3. Under objects (labeled), after any objects you want to keep hard-coded, add
   
   ```asm
   	include "script/maps/{map id}/objects.asm"
   ```
4. If there are any hard-coded objects, edit `_objectIndexOffsets` and `_dialogIdOffsets`
for the number of them.
5. Replace the dialog pointer:
   ```
   	dc.l	Map_{map id}_Dialog
   ```
6. Where dialog pointers are defined, add:
   ```
   	Map_Piata_Dialog:	include "script/maps/{map id}/dialog.asm"
   		even
   ```

## Bootstrapping scenes

See

```asm
Event_PiataChazAlone:
    ; Event code now deals with dialog trees
	include "script/scenes/PiataChazAlone/event.asm"

    ; Use storyEvent for this, or manually	
	move.w	#EventFlag_PiataChazControl, d0
	jmp	(EventFlags_Set).l
    ; remember to rts if not doing this
```

Also, move to `; Event code` section.
