import sys
from PIL import Image

images = [Image.open(x) for x in ['b_0.01.png', 'b_0.001.png', 'b_0.0001.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('IC_singletons_cst_coag.png')

####################

images = [Image.open(x) for x in ['b_0.01_diffusion_coag.png', 'b_0.001_diffusion_coag.png',
                                  'b_0.0001_diffusion_coag.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('IC_singletons_diffusion_coag.png')

############################

images = [Image.open(x) for x in ['b_0.01_IC_cst.png', 'b_0.001_IC_cst.png', 'b_0.0001_IC_cst.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('IC_cst_cst_coag.png')

#################################

images = [Image.open(x) for x in ['b_0.01_IC_cst_diffusion_coag.png',
                                  'b_0.001_IC_cst_diffusion_coag.png',
                                  'b_0.0001_IC_cst_diffusion_coag.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('IC_cst_diffusion_coag.png')
