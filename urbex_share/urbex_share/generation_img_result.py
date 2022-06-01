from PIL import Image, ImageDraw, ImageFont

def render(c1,c2):
    x=max([len(c1),len(c2)])*30
    mode="RGB"
    size=(x,135)
    color=(255,33,33)
    img = Image.new(mode,size,color)
    __draw_text(img,c1,int(x/2),30,0,40)
    __draw_text(img,c2,int(x/2),100,0,40)
    img.show()

def __draw_text(img,text,x,y,space,size):
    img1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size)
    d=font.getsize(text)
    img1.text((x+((space-d[0])/2),((y+(space-d[1])/2))),text,align="left",font=font)

#render("49.3527203,6.1532284","49.3527203,6.1532284")