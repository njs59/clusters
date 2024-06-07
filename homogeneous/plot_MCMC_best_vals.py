import matplotlib.pyplot as plt

x = [2,3,4,5,6]

y1 = [2.66e-04,2.55e-04,2.48e-04,2.47e-04,2.47e-04]
y2 = [909,1259,1471,1497,1492]
y3 = [54,79,122,156,196]

# Create two subplots and unpack the output array immediately
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.scatter(x, y1)
# ax1.set_title('Sharing Y axis')
ax2.scatter(x, y2)
plt.show()

# Create two subplots and unpack the output array immediately
f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.scatter(x, y1)
# ax1.set_title('Sharing Y axis')
ax2.scatter(x, y2)
ax3.scatter(x, y3)
plt.show()