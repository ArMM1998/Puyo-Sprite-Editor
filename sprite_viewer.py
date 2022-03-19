import sys
import os
import pygame
from PIL import Image, ImageDraw
from io import BytesIO
import win32clipboard
import struct 



current_selected = -1
texture_change_flag = True
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                 pygame.RESIZABLE)
pygame.display.set_caption('Sprite Viewer')

COLOR_INACTIVE = (200,200,200)
COLOR_ACTIVE = (255,255,255)

current = (0,0)

multipliersX = []
multipliersY = []

bg_color = (70, 70, 70)
texture_bg_color = (100,100, 100)


own_square_flag = False
pygame.init()
FONT = pygame.font.SysFont("arial", 14)


rect_coords = [-10,-10,0,0]


directory = sys.argv[1:]
texture_list = os.listdir(directory[0])

counter = 120


for fichier in texture_list[:]: # filelist[:] makes a copy of filelist.
    if not(fichier.endswith(".png")):
        texture_list.remove(fichier)


print("textures found: ",texture_list)

pygame.display.set_icon(pygame.image.load(directory[0] + "/" + texture_list[0]))

anim_file = sys.argv[2:][0]
anim_file_data = open(anim_file, "r+b").read()
try:
    big_endian_flag = sys.argv[3:][0]
except:
    big_endian_flag = ""
sprite_list = []

if big_endian_flag == "-be":
    offset = (anim_file_data[71])* 8
    amount_of_sprites = (anim_file_data[79])
    amount_of_sprites += (anim_file_data[78] * 256)
elif big_endian_flag == "-touch":
    counter = 148
    offset = (anim_file_data[68])* 8
    amount_of_sprites = (anim_file_data[72])
    amount_of_sprites += (anim_file_data[63] * 256)
else:
    offset = (anim_file_data[68])* 8
    amount_of_sprites = (anim_file_data[76])
    amount_of_sprites += (anim_file_data[77] * 256)

counter = counter + offset



print(counter)

print("total sprites: ",amount_of_sprites)

for i in range(0,amount_of_sprites):
    
    if big_endian_flag == "-be":
        sprite_list.append([anim_file_data[counter + 3],
                            (anim_file_data[counter + 7], anim_file_data[counter + 6], anim_file_data[counter + 5], anim_file_data[counter + 4]),
                            
                            (anim_file_data[counter + 11], anim_file_data[counter + 10], anim_file_data[counter + 9], anim_file_data[counter + 8]),
                            
                            
                            (anim_file_data[counter + 15], anim_file_data[counter + 14], anim_file_data[counter + 13], anim_file_data[counter + 12]),
                            
                            (anim_file_data[counter + 19], anim_file_data[counter + 18], anim_file_data[counter + 17], anim_file_data[counter + 16]), counter
                            ])
                            
        
    else: 
        sprite_list.append([anim_file_data[counter],
                            (anim_file_data[counter + 4], anim_file_data[counter + 5], anim_file_data[counter + 6], anim_file_data[counter + 7]),
                            
                            (anim_file_data[counter + 8], anim_file_data[counter + 9], anim_file_data[counter + 10], anim_file_data[counter + 11]),
                            
                            
                            (anim_file_data[counter + 12], anim_file_data[counter + 13], anim_file_data[counter + 14], anim_file_data[counter + 15]),
                            
                            (anim_file_data[counter + 16], anim_file_data[counter + 17], anim_file_data[counter + 18], anim_file_data[counter + 19]), counter
                            ])
    counter += 20

backup_sprite_list = sprite_list.copy()


def Export_Image(width, height, sq_x, sq_y, sq_w, sq_h):
    #og_image = Image.open(directory[0] + "/" + texture_list[current_texture], 'r')
    image = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([sq_x,sq_y,sq_w + sq_x,sq_h + sq_y], fill=(0,0,255,128))
    draw.rectangle([sq_x+1,sq_y+1,sq_w + sq_x-1,sq_h + sq_y-1], fill=(255,0,0,128))
    #image.paste(og_image, (0,0), og_image)
    output = BytesIO()
    image.convert("RGBA").save(output, "BMP")
    data = output.getvalue()[14:]
    clipboard(win32clipboard.CF_DIB, data)


img = pygame.image.load(directory[0] + "/" + texture_list[0])

def ExportAllSquares():
    image = Image.new('RGBA', img.get_size(), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    Img_size = img.get_size()
    sprite_to_export = [0,0,0,0]
    for sprite in sprite_list:
        x = sprite[1]
        y = sprite[2]
        w = sprite[3]
        h = sprite[4]
        
        if sprite[0] == current_texture:
            
            sprite_to_export = calcu(x, y, w, h)
            sprite_to_export = (Img_size[0] * sprite_to_export[0], Img_size[1] * sprite_to_export[1], Img_size[0] * sprite_to_export[2], Img_size[1] * sprite_to_export[3])

            
            draw.rectangle([sprite_to_export[0],sprite_to_export[1],sprite_to_export[2]-1,sprite_to_export[3]-1], fill=(50,0,0,255))
            draw.rectangle([sprite_to_export[0]+1,sprite_to_export[1]+1,sprite_to_export[2]-2,sprite_to_export[3]-2], fill=(250,50,50,128))
        output = BytesIO()
        image.convert("RGBA").save(output, "BMP")
        data = output.getvalue()[14:]
    clipboard(win32clipboard.CF_DIB, data)
        
        
class InputBox:
    def __init__(self, x, y, w, h, text, index, color):
        self.index = index
        self.rect = pygame.Rect(x, y, w, h)
        self.default_color = pygame.Color(color)
        self.color = pygame.Color(color)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = 0
        self.thickness = 1
        self.xpos = x
        self.ypos = y
        self.width = w 
        self.height = h

    def handle_event(self, event):
        global own_square_flag
        global current_selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # If the user clicked on the input_box rect.
                pos = event.pos[0] - (screen.get_size()[0] -210), event.pos[1]
                if self.rect.collidepoint(pos):
                    current_selected = self.index
                    own_square_flag = False
                    if self.active == 1:
                        SetTexture(sprite_list[self.index][0], (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0))
                        self.active = 0
                        self.thickness = 1
                        self.color = self.default_color
                    else: 
                        for btn in button_list:
                            btn.active = 0
                            btn.thickness = 1
                            btn.color = btn.default_color 
                        # Toggle the active variable.
                        self.active = 1
                        self.thickness = 2 if self.active else 1
                        self.color = pygame.Color("yellow")
                        SetTexture(sprite_list[self.index][0], sprite_list[self.index][1], sprite_list[self.index][2], sprite_list[self.index][3], sprite_list[self.index][4])
    
    def activate_anyway(self):
        global own_square_flag
        global current_selected
        current_selected = self.index
        own_square_flag = False
        for btn in button_list:
            btn.active = 0
            btn.thickness = 1
            btn.color = btn.default_color 
        # Toggle the active variable.
        self.active = 1
        self.thickness = 2 if self.active else 1
        self.color = pygame.Color("yellow")
        SetTexture(sprite_list[self.index][0], sprite_list[self.index][1], sprite_list[self.index][2], sprite_list[self.index][3], sprite_list[self.index][4])

    def draw(self, surface, x_pos):
        # Blit the text.
        self.rect = pygame.Rect(x_pos, self.ypos, self.width, self.height)
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+3))
        # Blit the rect.
        pygame.draw.rect(surface, self.color, self.rect, self.thickness)


def SetTexture(texture, x, y, w, h):
    global texture_pos
    global texture_change_flag
    global img
    global current_texture
    global multipliersX
    global multipliersY
    
    #set image
    img = pygame.image.load(directory[0] + "\\" + texture_list[texture])
    #calculate the coordinates given the values
    Img_size = img.get_size()
    
    square_pos = calcu(x, y, w, h)

    rect_coords[0] = (Img_size[0]) * square_pos[0]
    rect_coords[1] = (Img_size[1]) * square_pos[1]
    rect_coords[2] = (Img_size[0]) * square_pos[2] - rect_coords[0]
    rect_coords[3] = (Img_size[1]) * square_pos[3] - rect_coords[1]
     
    
    
    if texture != current_texture:
        texture_change_flag = True
    current_texture = texture
    
    txt_Xpos.text = str(int(rect_coords[0]))
    txt_Ypos.text = str(int(rect_coords[1]))
    txt_Width.text = str(int(rect_coords[2]))
    txt_Height.text = str(int(rect_coords[3]))
    txt_Xpos.maxm = Img_size[0]
    txt_Ypos.maxm = Img_size[1]
    txt_Width.maxm = Img_size[0]
    txt_Height.maxm = Img_size[1]
    
    
    txt_Xpos.maxm = Img_size[0]
    txt_Ypos.maxm = Img_size[1]
    txt_Width.maxm = Img_size[0]
    txt_Height.maxm = Img_size[1]
    txt_texture.text = str(texture)
    
    txt_texture.update()
    txt_Xpos.update() 
    txt_Ypos.update() 
    txt_Width.update()
    txt_Height.update()
 

def reset_sprite():
    sprite_list[current_selected] = backup_sprite_list[current_selected]
    SetTexture(backup_sprite_list[current_selected][0], backup_sprite_list[current_selected][1], backup_sprite_list[current_selected][2], backup_sprite_list[current_selected][3], 
                backup_sprite_list[current_selected][4])


def Save_Anim():
    offset = (sprite_list[current_selected][5])
    Img_size = img.get_size()
    
    
    with open(anim_file, "r+b") as f:
        if big_endian_flag == "-be":
            
            X1 = struct.pack(">f", rect_coords[0] / Img_size[0])
            Y1 = struct.pack(">f", rect_coords[1] / Img_size[1])
            X2 = struct.pack(">f", rect_coords[2] / Img_size[0] + rect_coords[0] / Img_size[0])
            Y2 = struct.pack(">f", rect_coords[3] / Img_size[1] + rect_coords[1] / Img_size[1])

            
            f.seek(offset)
            f.write(int(txt_texture.text).to_bytes(4, 'big'))
        
            f.seek(offset + 4)
            f.write(X1)
            
            f.seek(offset + 8)
            f.write(Y1)
            
            f.seek(offset + 12)
            f.write(X2)
            
            f.seek(offset + 16)
            f.write(Y2)
            
                        
            sprite_list[current_selected] = (int(txt_texture.text),X1,Y1,X2,Y2, offset)
            
            f.seek(0)
            data = f.read()
        
        
        else:
            X1 = struct.pack("f", rect_coords[0] / Img_size[0])
            Y1 = struct.pack("f", rect_coords[1] / Img_size[1])
            X2 = struct.pack("f", rect_coords[2] / Img_size[0] + rect_coords[0] / Img_size[0])
            Y2 = struct.pack("f", rect_coords[3] / Img_size[1] + rect_coords[1] / Img_size[1])
            
            print(X1, Y1)
            
            f.seek(offset)
            f.write(int(txt_texture.text).to_bytes(4, 'little'))
        
            f.seek(offset + 4)
            f.write(X1)
            
            f.seek(offset + 8)
            f.write(Y1)
            
            f.seek(offset + 12)
            f.write(X2)
            
            f.seek(offset + 16)
            f.write(Y2)
            
                        
            sprite_list[current_selected] = (int(txt_texture.text),X1,Y1,X2,Y2, offset)
            
            f.seek(0)
            data = f.read()
        
    with open(anim_file, "w+b") as f:
        f.write(data)
    
    
    
class Button:
    def __init__(self, x, y, w, h, text, function):
        self.rect = pygame.Rect(x, y, w, h)
        self.function = function
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.function()

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    

class TextBox:
    def __init__(self, x, y, w, h, maxm, text, title):
        self.rect = pygame.Rect(x, y, w, h)
        self.maxm = maxm
        self.title = title
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode == "0" or event.unicode == "1" or event.unicode == "2" or event.unicode == "3" or \
                            event.unicode == "4" or event.unicode == "5" or event.unicode == "6" or \
                            event.unicode == "7" or event.unicode == "8" or event.unicode == "9":
                        self.text += event.unicode
                        if int(self.text) > self.maxm:
                            self.text = str(self.maxm)
                if self == txt_texture:
                    try:
                        SetTexture(int(self.text), sprite_list[current_selected][1], sprite_list[current_selected][2], sprite_list[current_selected][3], sprite_list[current_selected][4])
                    except ValueError:
                        pass
                self.update()            
            

    def update(self):
        global rect_coords
        self.txt_surface = FONT.render(self.text, True, (255, 255, 255, 255))      
        try:
            rect_coords = [float(txt_Xpos.text), float(txt_Ypos.text), float(txt_Width.text), float(txt_Height.text)]
        except:
            pass
        
        
        
    def draw(self, screen):
        
        self.rect = pygame.Rect(self.rect.x, screen.get_size()[1]-30, self.rect.w, self.rect.h)
        txt_surface = FONT.render(str(self.title), True, (255,255,255))
        screen.blit(txt_surface, (self.rect.x,self.rect.y-20))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def clipboard(clip_type, data):
        
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()
    


def calcu(x, y, w, h):
    X1_pos = (x[0]).to_bytes(1, "big") + (x[1]).to_bytes(1, "big") + (x[2]).to_bytes(1, "big") + (x[3]).to_bytes(1, "big")
    Y1_pos = (y[0]).to_bytes(1, "big") + (y[1]).to_bytes(1, "big") + (y[2]).to_bytes(1, "big") + (y[3]).to_bytes(1, "big")
    X2_pos = (w[0]).to_bytes(1, "big") + (w[1]).to_bytes(1, "big") + (w[2]).to_bytes(1, "big") + (w[3]).to_bytes(1, "big")
    Y2_pos = (h[0]).to_bytes(1, "big") + (h[1]).to_bytes(1, "big") + (h[2]).to_bytes(1, "big") + (h[3]).to_bytes(1, "big")    
    
    X1_pos = (struct.unpack('f',X1_pos))
    Y1_pos = (struct.unpack('f',Y1_pos))
    X2_pos = (struct.unpack('f',X2_pos))
    Y2_pos = (struct.unpack('f',Y2_pos))
    
    return(X1_pos[0], Y1_pos[0], X2_pos[0], Y2_pos[0])



button_list = []
scale = 1
counter = 0
for sprite in sprite_list:
    color = "white"
    if sprite[1] == (0,0,0,0) and sprite[2] == (0,0,0,0) and sprite[3] == (0,0,0,0) and sprite[4] == (0,0,0,0):
        color = "red"
    button_list.append(InputBox(0, counter * 20, 200, 20, "Sprite " + str(counter) + ", Texture " + str(sprite[0]) + ", Offset: " + str(sprite[5]), counter, color))
    counter += 1


image_surface = pygame.Surface(img.get_size())
image_surface.fill(texture_bg_color)
texture_pos = ((screen.get_size()[0] / 2 - image_surface.get_size()[0] / 2) - 100, screen.get_size()[1] / 2 - image_surface.get_size()[1]/ 2 - 50)

txt_Xpos = TextBox(20, screen.get_size()[1]-30, 50, 22, image_surface.get_size()[0], "0", "X pos")
txt_Ypos = TextBox(20+80, screen.get_size()[1]-30, 50, 22, image_surface.get_size()[0], "0", "Y pos")
txt_Width = TextBox(20+160, screen.get_size()[1]-30, 50, 22, image_surface.get_size()[0], "0", "Width")
txt_Height = TextBox(20+240, screen.get_size()[1]-30, 50, 22, image_surface.get_size()[0], "0", "Height")

txt_texture = TextBox(400, screen.get_size()[1]-40, 50, 22, len(texture_list)-1, "0", "Texture")


input_boxes = [txt_Xpos,txt_Ypos,txt_Width,txt_Height,txt_texture]
    

clickable_buttons_idk = [Button(screen.get_size()[0]-400,screen.get_size()[1]-30,80,22, "Save to File", Save_Anim), Button(screen.get_size()[0]-300,screen.get_size()[1]-30,80,22, "Reset Sprite", reset_sprite)]


zoom_level = 100

# MAIN LOOP
running = True
ypos_counter = 0

current_texture = 0
holding_left_click = False
holding_middle_click = False
holding_right_click = False
holding_shift = False
stop_flag = False
button_list[0].activate_anyway()

while running:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in button_list:
            button.handle_event(event)
        
        for box in input_boxes:
            box.handle_event(event)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            

            if event.button == 1:
                starting_mouse_pos = event.pos
                holding_left_click = True
                if event.pos[0] in range(0, 40) and event.pos[1] in range(0, 15):
                    scale = 1
            
            if event.button == 2:
                starting_mouse_pos = event.pos
                holding_middle_click = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL )
            
            if event.button == 3:
                starting_mouse_pos = event.pos
                holding_right_click = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
            
            
            if event.button == 4:
                #IF mouse in the range of the texture
                if event.pos[0] < screen.get_size()[0] -210:
                    scale -= 0.1
                    if scale < 0.16:
                        scale += 0.1 
                else:
                    if button_list[0].ypos < 0:
                        for button in button_list:
                            button.ypos = button.ypos + 50
                            
            if event.button == 5:
                if event.pos[0] < screen.get_size()[0] -210:
                    scale += 0.1
                    if scale > 2.1:
                        scale -= 0.1 
                else:
                    if button_list[len(button_list) - 1].ypos > screen.get_size()[1] - 50:
                        for button in button_list:
                            button.ypos = button.ypos - 50
            
            for btn in clickable_buttons_idk:
                btn.handle_event(event)
            
            
            
        if event.type == pygame.MOUSEBUTTONUP:
            holding_left_click = False
            holding_middle_click = False
            holding_right_click = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            txt_Width.text = str(int(rect_coords[2]))
            txt_Height.text = str(int(rect_coords[3]))
            txt_Width.update()
            txt_Height.update()
            txt_Xpos.text = str(int(rect_coords[0]))
            txt_Ypos.text = str(int(rect_coords[1]))
            txt_Xpos.update()
            txt_Ypos.update()
            
        
        if event.type == pygame.KEYUP:
            holding_shift = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if keys[pygame.K_LCTRL]:
                    for txt in input_boxes:
                        txt.active = False
                    if current_selected > 10:
                        current_selected -= 10
                    else:
                        current_selected = 0
                    for btn in button_list:
                        if btn.index == current_selected:
                            btn.activate_anyway()
                            ypos_counter = -current_selected * 20
                    
                else:
                    rect_coords[0] -= 1
                    txt_Xpos.text = str(rect_coords[0])
                    txt_Xpos.update()
              
              
            if event.key == pygame.K_LSHIFT:
                holding_shift = True

                
            if event.key == pygame.K_RIGHT:
                if keys[pygame.K_LCTRL]:
                    for txt in input_boxes:
                        txt.active = False
                    if current_selected < len(sprite_list) - 11:
                        current_selected += 10
                    else:
                        current_selected = len(sprite_list) - 1
                    for btn in button_list:
                        if btn.index == current_selected:
                            btn.activate_anyway()
                            ypos_counter = -current_selected *20
                elif keys[pygame.K_LSHIFT]:
                    texture_pos = ((texture_pos[0] - 20 , texture_pos[1]))

                
                else:
                    rect_coords[0] += 1
                    txt_Xpos.text = str(rect_coords[0])
                    txt_Xpos.update()
                
                
            if event.key == pygame.K_UP:
                if keys[pygame.K_LCTRL]:
                    for txt in input_boxes:
                        txt.active = False
                    if current_selected > 0:
                        current_selected -= 1
                    for btn in button_list:
                        if btn.index == current_selected:
                            btn.activate_anyway()
                            ypos_counter = -current_selected *20
        
                else:
                    rect_coords[1] -= 1
                    txt_Ypos.text = str(rect_coords[1])
                    txt_Ypos.update()
                
                
            if event.key == pygame.K_DOWN:
                if keys[pygame.K_LCTRL]:
                    for txt in input_boxes:
                        txt.active = False
                    if current_selected < len(sprite_list)-1:
                        current_selected += 1
                    for btn in button_list:
                        if btn.index == current_selected:
                            btn.activate_anyway()
                            ypos_counter = -current_selected *20
                elif keys[pygame.K_LSHIFT]:
                    texture_pos = ((texture_pos[0], texture_pos[1]-20))
                
                
                else:
                    rect_coords[1] += 1
                    txt_Ypos.text = str(rect_coords[1])
                    txt_Ypos.update()
            
            if event.key == pygame.K_DELETE:
                txt_Xpos.text = "0"
                txt_Xpos.update()
                txt_Ypos.text = "0"
                txt_Ypos.update()
                txt_Width.text = "0"
                txt_Width.update()
                txt_Height.text = "0"
                txt_Height.update()
                txt_texture.text = "0"
                txt_texture.update()
            
            if event.key == pygame.K_e:
                texture_pos = (screen.get_size()[0]/2 - 100,screen.get_size()[1]/2)
            if event.key == pygame.K_r:
                reset_sprite()
            if event.key == pygame.K_s:
                Save_Anim()
            
            

    if keys[pygame.K_LCTRL] and keys[pygame.K_c]:
        if not stop_flag:
            stop_flag = True
            if keys[pygame.K_LALT]:
                ExportAllSquares()
            else:
                Export_Image(img.get_size()[0], img.get_size()[1], rect_coords[0], rect_coords[1], rect_coords[2], rect_coords[3])
    else:
        stop_flag = False
    zoom_level = int(100 / scale)
    
    mouse_pos = pygame.mouse.get_pos()
    
    print("holding", holding_left_click, holding_shift)
    
    if holding_left_click and holding_shift:
        rect_coords[2] = (rect_coords[2] - (starting_mouse_pos[0] - mouse_pos[0])*scale)
        rect_coords[3] = (rect_coords[3] - (starting_mouse_pos[1] - mouse_pos[1])*scale)
        
        txt_Width.text = str(rect_coords[2])
        txt_Height.text = str(rect_coords[3])
        txt_Width.update()
        txt_Height.update()

        starting_mouse_pos = mouse_pos
    
    clickable_buttons_idk[0].rect = pygame.Rect(screen.get_size()[0]-400,screen.get_size()[1]-30,80,22)
    clickable_buttons_idk[1].rect = pygame.Rect(screen.get_size()[0]-300,screen.get_size()[1]-30,80,22)
    
    #I'm bad at this ┐(￣ヘ￣)┌
    if zoom_level == 49:
        zoom_level = 50
    elif zoom_level == 199:
        zoom_level = 200
    

    if holding_middle_click:
        texture_pos = ((texture_pos[0] - (starting_mouse_pos[0] - mouse_pos[0])), (texture_pos[1] - (starting_mouse_pos[1] - mouse_pos[1])))
        starting_mouse_pos = mouse_pos
    
    if holding_right_click:
        rect_coords[0] = (rect_coords[0] - (starting_mouse_pos[0] - mouse_pos[0])*scale)
        rect_coords[1] = (rect_coords[1] - (starting_mouse_pos[1] - mouse_pos[1])*scale)
        if rect_coords[0] < 0:
            rect_coords[0] = 0
        if rect_coords[1] < 0:
            rect_coords[1] = 0
        
        if rect_coords[0] > img.get_size()[0] - rect_coords[2]:
            rect_coords[0] = img.get_size()[0] - rect_coords[2]
        if rect_coords[1] > img.get_size()[1] - rect_coords[3]:
            rect_coords[1] = img.get_size()[1] - rect_coords[3]
            
            
        txt_Xpos.text = str(rect_coords[0])
        txt_Ypos.text = str(rect_coords[1])
        txt_Xpos.update()
        txt_Ypos.update()
        
        starting_mouse_pos = mouse_pos
    
    pygame.display.flip()
    
    bg = pygame.Surface(screen.get_size())
    bg.fill(bg_color)
    screen.blit(bg, (0,0))
    
    
    
    image_surface = pygame.Surface(img.get_size())
    image_surface.fill(texture_bg_color)
    image_surface.blit(img, (0, 0))
    
    
    square = pygame.Surface((rect_coords[2],rect_coords[3]))
    square.set_alpha(128)               
    square.fill((252, 94, 3)) 
    image_surface.blit(square, (rect_coords[0],rect_coords[1]))
    
    side_bar = pygame.Surface((210,screen.get_size()[1]))
    side_bar.fill((40, 40, 40))
    for button in button_list:
        if button.ypos in range(screen.get_size()[1]):
            button.draw(side_bar, 0)
    
    if texture_change_flag:
        scale = 1
        texture_pos = ((screen.get_size()[0] / 2) - 100, screen.get_size()[1] / 2)
        texture_change_flag = False
    
    image_surface = pygame.transform.scale(image_surface,(image_surface.get_size()[0] / scale , image_surface.get_size()[1] / scale))
    
    screen.blit(image_surface, (texture_pos[0] - image_surface.get_size()[0]/2 ,texture_pos[1] - image_surface.get_size()[1]/2))
    
    bar_bottom = pygame.Surface((screen.get_size()[0], 50))
    bar_bottom.fill(bg_color)
    screen.blit(bg, (0,screen.get_size()[1]-50))
    
    screen.blit(side_bar, (screen.get_size()[0] -210, 0))
    txt_surface = FONT.render(str(zoom_level) + "%", True, (255,255,255))
    screen.blit(txt_surface, (0,0))
    
    for box in input_boxes:
        box.draw(screen)    
    for btn in clickable_buttons_idk:
        btn.draw(screen)
    pass
pygame.quit()
exit()