import os
import re

dorms_only = 'dorms_only'
pngs = 'pngs'

os.mkdir(pngs)

dirs = [ name for name in os.listdir(dorms_only) if os.path.isdir(os.path.join(dorms_only, name)) ]

for d in dirs:
	if ' ' in d:
		dorm_strings = d.split(' ')
		if '\'' in d:
			dorm_strings[0] = "O\'neil"
	
		d = dorm_strings[0] + " " +  dorm_strings[1]
		
	dorm_path = dorms_only + '/' + d
	new_path = pngs + '/' + d
	os.mkdir(new_path)


	if (os.path.exists(dorm_path)):
		print  dorm_path + " Exists!  "
		for filename in os.listdir(dorm_path):
			if "BSMT" not in filename:
				pdf_path = dorm_path + '/' + filename
				base = filename.split('.')[0]
				png_path = new_path + '/' + base + '.png'
				command = 'sips -s format png ' + pdf_path +  ' --out ' +  png_path
				print command
				os.system(command)

	
