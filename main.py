import csv
from scipy.spatial import distance
import matplotlib.pyplot as plt
from sklearn import neighbors
training = []
fingerprint = []

with open('trainingData.csv', newline='') as csvfile:
  rows = csv.reader(csvfile)#floor:522 building:523
  for row in rows:
    if row[522] == '1' and row[523] == '1':
      training.append(row)

with open('validationData.csv', newline='') as csvfile:
  rows = csv.reader(csvfile)
  for row in rows:
    if row[522] == '1' and row[523] == '1':
      fingerprint.append(row)

for i in range(len(training)):
  for j in range(len(training[i])-1):
    training[i][j] = float(training[i][j])
for i in range(len(fingerprint)):
  for j in range(len(fingerprint[i])-1):
    fingerprint[i][j] = float(fingerprint[i][j])
#原因是list的浅拷贝问题
#closest = [[0] * 5] * len(fingerprint)
dis = [([100000] * 5) for i in range(len(fingerprint))]
closest = [([0] * 5) for i in range(len(fingerprint))]
tolerance = [0] * len(fingerprint)
avgtol = 0

def eudis():
  global dis,closest,tolerance
  avgtol = 0
  for f in range(len(fingerprint)):
    for i in range(len(training)):
      buf = distance.euclidean(fingerprint[f][0:520], training[i][0:520])
      for j in range(0, 5):
        if buf < dis[f][j]:
          for k in range(4, j, -1):

            dis[f][k] = dis[f][k-1]
            closest[f][k] = closest[f][k - 1]
          dis[f][j] = buf
          closest[f][j] = i
          #print(0,dis[0])
          break
    #lon:520 lat:521
    if len(fingerprint[f]) > 521:
      tolerance[f] = distance.euclidean(fingerprint[f][520:522],training[closest[f][0]][520:522])
    avgtol += tolerance[f]
  avgtol /= len(fingerprint)
  return avgtol

avgtol = eudis()

plt.hist(tolerance, label = ['tolerance'], stacked=True)
plt.legend()
plt.xlabel('tolerance')
plt.ylabel('number')
plt.show()
print("euclidean distance:",avgtol)

def knn(k):
  global dis, closest, tolerance
  tolerance = [0] * len(fingerprint)
  location = []
  avgtol = 0
  lon = [0] * len(fingerprint)
  lat = [0] * len(fingerprint)
  for f in range(len(fingerprint)):
    for i in range(0, k):
      lon[f] += training[closest[f][i]][520]
      lat[f] += training[closest[f][i]][521]
    lon[f] /= k
    lat[f] /= k
    if len(fingerprint[f]) > 521:
      tolerance[f] = distance.euclidean(fingerprint[f][520:522], [lon[f], lat[f]])
    avgtol += tolerance[f]
    location.append([lon[f], lat[f]])
  avgtol /= len(fingerprint)
  if len(fingerprint[0]) < 521:
    return location
  else :
    return avgtol

for k in range(1, 6, 2):
  avgtol = knn(k)
  plt.hist(tolerance, label=['tolerance'], stacked=True)
  plt.legend()
  plt.xlabel('tolerance')
  plt.ylabel('number')
  plt.show()
  print('knn('+str(k)+'):',avgtol)

fingerprint.clear()
with open('plot.csv', newline='') as csvfile:
  rows = csv.reader(csvfile)
  for row in rows:
    fingerprint.append(row)
fingerprint.pop(0)
dis = [([100000] * 5) for i in range(len(fingerprint))]
closest = [([0] * 5) for i in range(len(fingerprint))]
for i in range(len(fingerprint)):
  for j in range(len(fingerprint[i])):
    fingerprint[i][j] = float(fingerprint[i][j])
avgtol = eudis()
location = knn(3)
print(location)
