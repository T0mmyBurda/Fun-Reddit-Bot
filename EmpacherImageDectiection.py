from PIL import Image


def isEmpacher(imgPath):
    rAvg = 214
    gAvg = 205
    bAvg = 125

    thresh = .01
    leeway = 25
    empPix = 0

    img = Image.open(imgPath)
    pixels = img.load()

    imgX = img.size[0]
    imgY = img.size[1]

    examp = pixels[0 , 0]
    r = examp[0]
    print("HERE")
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

    print(empPix)
    print(imgX * imgY)
    return (empPix / (imgX * imgY))
            

output = isEmpacher("EmpacherTestImages/test1.png")

#print(output)
