import sys, os
import pymol

from os import listdir
from datetime import datetime

numbers = [0,1,2,3,4,5,6,7,8,9]

def load(amount,raysize,overwrite):

	codes = []
	path = os.getcwd()
	
	if(amount == "all"):
		for dirName in os.walk(path):
		
			os.chdir(dirName[0])
			possibleCode = dirName[0][len(dirName[0]) - 4:len(dirName[0])]
				
			for num in numbers:
				if(possibleCode.startswith(str(num))):
					if(overwrite == "True" or overwrite == "true"):
						makemove(possibleCode,raysize)
						codes.append(possibleCode)
					else:
						if(not os.path.exists(possibleCode + "_anim.mov")):
							makemove(possibleCode,raysize)
							codes.append(possibleCode)
						else:
							print(possibleCode + "_anim.mov existiert bereits")
							break
	else:
		makemove(amount,raysize)
					

	print(codes)

def makemove(code,raysize):	
	pymol.cmd.fetch(code, "structure_model type=cif")
	pymol.cmd.create

	settings()
	colors()

	export(code, raysize)
	
	try:
		os.remove(code + ".cif")
	except:
		print("Nothing to remove here")
		
	print("Successfully finished on " + code + "!")
	
	
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
	
	pymol.cmd.mset("1 x120")
	pymol.cmd.util.mroll("1","120","2")
	pymol.cmd.set("ray_trace_frames", 1)
	pymol.cmd.set("cache_frames", 0)
	
	print("Working on: " + id + "_anim.mov...")
	pymol.cmd.do("movie.produce " + id + "_anim.mov, ray, 1, 120, 0, ffmpeg, 50")

	pymol.cmd.delete("all")
	
load(sys.argv[len(sys.argv) - 3],sys.argv[len(sys.argv) - 2],sys.argv[len(sys.argv) - 1])


#scp /mnt/c/Users/Caipi/Desktop/Taskforce/coronavirus_structural_task_force/pdb/walkani.py konstantinmueller@132.187.172.12:~/animations/pdb/walkani.py 