To use, download the sprite_viewer.py

# Requirements:
	Python 3.0 or above
	pillow
	pygame
	pywin32
	

# Usage: 
	sprite_viewer.py [directory] [animation file] [optional big endian]

	- directory: Directory containing all of the textures converted to png.
	- animation file: Any animation file from 15th anniversary up to 20th anniversary (excluding 20th 3ds).
	- optional big endian: has to be "-be" without quotations. Only use this if the animation file is big endian.

# Shortcuts:
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
		- While holding Shift:
			Move the texture view.
	- R: 
		Reset sprite position, width, height, and texture.
		
	- E:
		Center texture view.
	
		
	- S:
		Save the currently selected sprite into the animation file.
		
	- CTRL + C: 
		Copy to the clipboard a blue square of the currenty selected sprite.
		
	- CTRL + ALT + C: 
		Copy to the clipboard a blue square for every sprite on the currenty selected texture.
	
	- Delete:
		Set the current sprite's position, width and height to 0. (useful when you want to clear out unnecessary sprites that are not used.)
		Deleted sprites will appear as red next time you open the file.
