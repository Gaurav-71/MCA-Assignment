import os
import time
import multiprocessing 
from PIL import Image
import matplotlib.pyplot as plt 
import numpy as np

imagesPath = os.path.join(os.getcwd(), "Images")

try: 
    os.mkdir(os.path.join(os.getcwd(), "Serial Compressed"))
    os.mkdir(os.path.join(os.getcwd(), "Parallel Compressed")) 
except OSError as error: 
    pass

serialTime = {}
parallelTime = {}

def compressImage(file, type, verbose = False):
    formats = ('.jpg', '.jpeg', '.png')
    if os.path.splitext(file)[1].lower() in formats:
        filepath = os.path.join(imagesPath, file)          
        picture = Image.open(filepath)            
        compressedPath = os.path.join(os.getcwd(),type)                    
        picture.save(os.path.join(compressedPath, file), "JPEG", optimize = True, quality = 10)
    return

def serialProcess():
    print("==== Serial Image Compression ===\n")
    starttime = time.time()
    for index,file in enumerate(os.listdir(imagesPath)):    
        print("\t"+str(index+1)+". Serial Compressing "+file)        
        compressImage(file,"Serial Compressed")
        if(index % 50 == 0 and index!= 0):
            serialTime[index] = time.time() - starttime
    global serialTimeTotal
    serialTimeTotal = time.time() - starttime
    print("\n\tSerial Image Compression Completed.")
    
def parallelProcess():
    print("\n=== Started Parallel Image Compression ===\n")
    starttime = time.time()
    global processes 
    processes = []
    for index,file in enumerate(os.listdir(imagesPath)):  
        print("\t"+str(index+1)+". Parallel Compressing "+file)              
        if(index%50 == 0 and index!= 0):
            parallelTime[index] = time.time() - starttime
        p = multiprocessing.Process(target=compressImage, args=(file,"Parallel Compressed",))
        processes.append(p)
        p.start()
    global parallelTimeTotal
    parallelTimeTotal = time.time() - starttime
    print("\n\tParallel Image Compression Completed.")  

def plotGraph():
    x = list(serialTime.keys())
    y1 = list(serialTime.values())
    y2 = list(parallelTime.values())
    X_axis = np.arange(len(x))
    plt.bar(X_axis - 0.2, y1, 0.4, label = 'Serial Processing')
    plt.bar(X_axis + 0.2, y2, 0.4, label = 'Parallel Processing')
    plt.xticks(X_axis, x)
    plt.xlabel("Images")
    plt.ylabel("Time Taken(s)")
    plt.title("Serial vs Parallel processing for Image Compression")
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    serialProcess()
    parallelProcess()
    print("\n\n === Compression Statistics ===")
    print("\nNo. of images : 268")
    print("\nTotal size of images before compression : 276.5 MB")
    print("Total size of images after compression : 11.4 MB")
    print('\nSerial Compression took {} seconds'.format(serialTimeTotal))
    print('Parallel Compression took {} seconds'.format(parallelTimeTotal))    

    plotGraph()

    print("Terminating all processes, This might take a while ...")

    for process in processes:        
        process.join()