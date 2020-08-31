import sys, os
import pymol

from PIL import Image
from os import listdir
from datetime import datetime

numbers = [0,1,2,3,4,5,6,7,8,9]

def load(raysize,overwrite):

	codes = []
	path = os.getcwd()
	
	for dirName in os.walk(path):
	
		os.chdir(dirName[0])
		possibleCode = dirName[0][len(dirName[0]) - 4:len(dirName[0])]

		if('structure_sequence_alignment.txt' in dirName[2]):
			file = open(dirName[0] + "\\structure_sequence_alignment.txt", 'r')
			lines = file.readlines() 
			
			tempDummy = 'noneYet'
			bestDummy = 'noneYet'
			bestScore = -9999999.99
			
			for line in lines:
				if(line.startswith('>>>')):
					tempDummy = line[3:7]
				
					for line in lines:
						if(line.startswith('Score: ')):
							line = line.replace('Score: ', '')
							score = float(line)
							
							if(score > bestScore):
								bestScore = score
								bestDummy = tempDummy
								
							break
	
			print(dirName[0] + " BestDummy: " + bestDummy)
		else:
			if('human_interaction_partners' in dirName[0]):
				tempDummy = 'noneYet'
				bestDummy = 'noneYet'
				bestScore = -9999999.99
			
			
		for num in numbers:
			if(possibleCode.startswith(str(num))):
				if(overwrite == "True" or overwrite == "true"):
					makemove(possibleCode,raysize,bestDummy)
					codes.append(possibleCode)
				else:
					if(not os.path.exists(possibleCode + "_structure.jpg")):
						makemove(possibleCode,raysize,bestDummy)
						codes.append(possibleCode)
					else:
						print(possibleCode + "_structure.png existiert bereits")
						break
					

	print(codes)

def makemove(code,raysize,dummy):	
	try:
		print(code + " --> " + dummy)
		pymol.cmd.fetch(code, "structure_model type=cif")
		pymol.cmd.create

		settings()
		colors()
		
		if(not dummy == "noneYet"):
			pymol.cmd.fetch(dummy, "dummy")
			pymol.cmd.create
			pymol.cmd.align("structure_model", "dummy")
			pymol.cmd.remove("dummy")
			os.remove(dummy + ".cif")

		export(code, raysize)

		img = Image.open(code + "_structure.png")
		rgb_im = img.convert('RGB')
		rgb_im.save(code + "_structure.jpg")
		os.remove(code + "_structure.png")
		os.remove(code + ".cif")
		print("Successfully finished on " + code + "!")
	except:
		print("Skipped " + code)
	
def settings():
	#Settings
	pymol.cmd.set("ray_opaque_background", "on") #off for opaque background
	pymol.cmd.set("depth_cue", 1)
	pymol.cmd.set("ray_shadows", 0)
	pymol.cmd.set("ray_shadows", 1)
	pymol.cmd.set("antialias", 1)
	pymol.cmd.set("ray_trace_fog", 1)
	pymol.cmd.set("line_smooth", 0.25)
	pymol.cmd.set("surface_quality", 4)
	pymol.cmd.set("cartoon_ring_mode", 3)
	pymol.cmd.set("cartoon_ring_finder", 3)
	pymol.cmd.set("cartoon_ladder_mode", 1)
	pymol.cmd.set("cartoon_nucleic_acid_mode", 0)
	pymol.cmd.set("cartoon_ring_transparency", 0.9)
	pymol.cmd.set("cartoon_tube_radius", 0.3) #0.5
	pymol.cmd.set("cartoon_fancy_helices", 1)
	pymol.cmd.set("cartoon_fancy_sheets", 1)
	pymol.cmd.set("cartoon_loop_quality", 10)
	pymol.cmd.set("cartoon_loop_radius", 0.5)#1.25, ribbon width
	pymol.cmd.set("cartoon_refine", 1)
	pymol.cmd.set("cartoon_sampling", 50)
	pymol.cmd.remove("solvent")
	
def colors():
	#Colors
	pymol.cmd.color("grey")
	pymol.cmd.color("tv_red", "ss h")
	pymol.cmd.color("skyblue", "ss s")
	pymol.cmd.color("orange", "resn A+T+G+C+U+dA+dT+dG+dC+dU")
	pymol.cmd.set("cartoon_ring_color", "brightorange")
	pymol.cmd.set("cartoon_nucleic_acid_color", "orange")
	
def export(id, raysize):
	#Render
	pymol.cmd.orient
	pymol.cmd.zoom("structure_model")
	
	print("Working on: " + id + "_structure.jpg...")
	pymol.cmd.ray(raysize,raysize)
	pymol.cmd.png(id + "_structure.png")

	pymol.cmd.delete("all")
	
load(sys.argv[len(sys.argv) - 2],sys.argv[len(sys.argv) - 1])