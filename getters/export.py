import subprocess
from xml.dom import minidom
import json
import numpy as np
import sys
import os
sys.dont_write_bytecode=True


def highcharts_export(modified_data):

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filename = os.path.join(SITE_ROOT,'infile.json')
    
    with open(filename) as f:
        a = json.load(f)  
        a['series'][0]['data'] = modified_data

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    updated = os.path.join(SITE_ROOT,'updated.json')
    with open(updated, 'w') as w:
        w.write(json.dumps(a))

    #infile = "/home/marreddy/testing/myapp/back_end/updated.json"
    #outfile = "/home/marreddy/testing/myapp/back_end/outfile.svg"
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

    infile = os.path.join(SITE_ROOT,'updated.json')

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    outfile = os.path.join(SITE_ROOT,'outfile.svg')

    subprocess.check_call("highcharts-export-server --type svg  -infile "+infile+" -outfile "+outfile, shell = True) 
   
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    outfile = os.path.join(SITE_ROOT,'outfile.svg')


    xmldoc = minidom.parse(outfile)

    itemlist = xmldoc.getElementsByTagName('svg')

    for path in xmldoc.getElementsByTagName('path'):
        
        if path.getAttribute("class") == "highcharts-graph":

            svg_path = path.getAttribute('d')

            ar = svg_path.split(" "); 
                #br STORES COORDINATE POINT 
            br = []
            for x in range(0,len(ar)):
                if(ar[x]=="M" or ar[x]=="L"):
                    continue
                else:
                    br.append(ar[x])
            
                #TAKING THE LAST FOUR POINTS AND CALCULATING THE ANGLES
            if(len(br) >= 4):
                x1 = br[len(br)-4]
                y1 = br[len(br)-3]
                x2 = br[len(br)-2]
                y2 = br[len(br)-1]
                y = float(y1)-float(y2)
                x = float(x2)-float(x1)
                an = np.arctan2(y, x)
                angle = np.rad2deg(an)
                return angle
            else:
                return 'angle calculation is not possible'