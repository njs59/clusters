import matplotlib.pyplot as plt
import matplotlib.image as mpimg




img1 = mpimg.imread('plots_to_gif/coag_only/coag_IC_10_num_sims_100_steps_100.jpg')
img2 = mpimg.imread('plots_to_gif/coag_only/coag_IC_50_num_sims_100_steps_200.jpg')
img3 = mpimg.imread('plots_to_gif/coag_only/coag_IC_100_num_sims_100_steps_150.jpg')
img4 = mpimg.imread('plots_to_gif/coag_only/coag_IC_120_num_sims_1000_steps_500.jpg')
img5 = mpimg.imread('plots_to_gif/coag_only/coag_IC_200_num_sims_1000_steps_1000.jpg')
img6 = mpimg.imread('plots_to_gif/coag_only/coag_IC_5000_num_sims_1000_steps_6000.jpg')

rows = ['Average number of clusters']



fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 20))


for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


plt.subplot(3,3,1)
plt.title('IC = 10')
plt.imshow(img1)
plt.axis('off')

plt.subplot(3,3,2)
plt.title('IC = 50')
plt.imshow(img2)
plt.axis('off')

plt.subplot(3,3,3)
plt.title('IC = 100')
plt.imshow(img3)
plt.axis('off')

plt.subplot(3,3,4)
plt.title('IC = 120')
plt.imshow(img4)
plt.axis('off')

plt.subplot(3,3,5)
plt.title('IC = 200')
plt.imshow(img5)
plt.axis('off')

plt.subplot(3,3,6)
plt.title('IC = 5000')
plt.imshow(img6)
plt.axis('off')

plt.savefig("plots_to_gif/IC_sweep_coag_only" + ".jpg")





img1 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_10_num_sims_100_steps_100.jpg')
img2 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_50_num_sims_100_steps_200.jpg')
img3 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_100_num_sims_100_steps_150.jpg')
img4 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_120_num_sims_1000_steps_500.jpg')
img5 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_200_num_sims_1000_steps_1000.jpg')
img6 = mpimg.imread('plots_to_gif/coag_only/norm_coag_IC_5000_num_sims_1000_steps_6000.jpg')

rows = ['Average number of clusters']



fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 20))


for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


plt.subplot(3,3,1)
plt.title('IC = 10')
plt.imshow(img1)
plt.axis('off')

plt.subplot(3,3,2)
plt.title('IC = 50')
plt.imshow(img2)
plt.axis('off')

plt.subplot(3,3,3)
plt.title('IC = 100')
plt.imshow(img3)
plt.axis('off')

plt.subplot(3,3,4)
plt.title('IC = 120')
plt.imshow(img4)
plt.axis('off')

plt.subplot(3,3,5)
plt.title('IC = 200')
plt.imshow(img5)
plt.axis('off')

plt.subplot(3,3,6)
plt.title('IC = 5000')
plt.imshow(img6)
plt.axis('off')

plt.savefig("plots_to_gif/IC_sweep_coag_only_normed" + ".jpg")



img1 = mpimg.imread('plots_to_gif/coag_shed_lam_10_IC_100_num_sims_100_steps_1000.jpg')
img2 = mpimg.imread('plots_to_gif/coag_shed_lam_1_IC_100_num_sims_100_steps_1000.jpg')
img3 = mpimg.imread('plots_to_gif/coag_shed_lam_0.1_IC_100_num_sims_100_steps_1000.jpg')
img4 = mpimg.imread('plots_to_gif/coag_IC_100_num_sims_100_steps_150.jpg')






rows = ['Average number of clusters']



fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 20))


for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


plt.subplot(2,2,1)
plt.title('lambda = 10')
plt.imshow(img1)
plt.axis('off')

plt.subplot(2,2,2)
plt.title('lambda = 1')
plt.imshow(img2)
plt.axis('off')

plt.subplot(2,2,3)
plt.title('lambda = 0.1')
plt.imshow(img3)
plt.axis('off')

plt.subplot(2,2,4)
plt.title('lambda = 0')
plt.imshow(img4)
plt.axis('off')



plt.savefig("plots_to_gif/lambda_sweep_coag_diff" + ".jpg")

plt.show()
