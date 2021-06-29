import datetime
from PIL import Image


def isEmpacher(imgPath):
    rAvg = 214
    gAvg = 205
    bAvg = 125

    thresh = .002
    leeway = 25
    #25 -- 0.0026373519414204637
    #40 -- 0.010268639283628577
    empPix = 0

    img = Image.open(imgPath)
    pixels = img.load()

    imgX = img.size[0]
    imgY = img.size[1]

    examp = pixels[0 , 0]
    r = examp[0]
    print(examp)
    print(abs(r - rAvg))

    # print(examp)
    # print(examp[0])
    
    for x in range(0 , imgX):
        for y in range(0 , imgY):
            curPix = pixels[x , y]
            r = curPix[0]
            g = curPix[1]
            b = curPix[2]

            if(abs(r - rAvg) < leeway and abs(g - gAvg) < leeway and abs(b - bAvg) < leeway):
                empPix += 1
                pixels[x , y] = (245, 75, 66, 255)

    # print(empPix)
    # print(imgX * imgY)
    print(empPix / (imgX * imgY))
    print((empPix / (imgX * imgY) > thresh))

    time = datetime.datetime.now()
    stringTime = time.strftime("%m-%d %H:%M")
    
    img.save("EmpacherTestImagesResults/test5--" + stringTime + ".png")
    
    return (empPix / (imgX * imgY) > thresh)
            

output = isEmpacher("EmpacherTestImages/test5.png")

print(output)
