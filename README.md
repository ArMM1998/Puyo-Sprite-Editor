To use, download the sprite_viewer.py and run it via command prompt.

It only works on windows so far because of the pywin32 library.

# Requirements:
	Python 3.0 or above
	pillow
	pygame
	pywin32
	

# Usage: 
	sprite_viewer.py [directory] [animation file] [big endian flag]

	- directory: Directory containing all of the textures converted to png.
	- animation file: Any animation file from 15th anniversary up to 20th anniversary (excluding 20th 3ds).
	- big endian flag: OPTIONAL. has to be "-be" without quotations. Only use this if the animation file is big endian, leave it empty if it's little endian.

# Shortcuts:
	- Left Click:
		While holding LShift:
			Resize sprite
	- Right Click:
		drag the sprite around to adjust it's position.
	
	- Middle Click:
		Move the texture view.
	
	- Mouse Wheel:
		Zoom in / out
	
	- Arrow Keys: 
			Move the sprite around to adjust it's position.
		- While holding CTRL:
			Select next / previous sprite
	- R: 
		Reset sprite position, width, height, and texture.
		
	- E:
		Center texture view.
	
		
	- S:
		Save the currently selected sprite into the animation file.
		
	- CTRL + C: 
		Copy to the clipboard a red square of the currenty selected sprite.
		
	- CTRL + ALT + C: 
		Copy to the clipboard a red square for every sprite on the currenty selected texture.
	
	- Delete:
		Set the current sprite's position, width and height to 0. (useful when you want to clear out unnecessary sprites that are not used.)
		Deleted sprites will appear as red next time you open the file.
