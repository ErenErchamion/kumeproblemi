
import random
import folium
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# 400 km karelik bir bölge belirleme
center_lat = 40.0
center_long = 32.0
radius = 20  # km
north = center_lat + (radius / 111)
south = center_lat - (radius / 111)
east = center_long + (radius / (111 * np.cos(center_lat)))
west = center_long - (radius / (111 * np.cos(center_lat)))

# Rastgele koordinatlar oluşturma
locations = []
for i in range(1200):
    lat = random.uniform(south, north)
    long = random.uniform(west, east)
    locations.append((lat, long))

# Kümeleme yapma
# AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=None, metric='euclidean', linkage='ward', distance_threshold=0.1)
cluster.fit_predict(locations)
num_clusters = len(set(cluster.labels_))

# K means Clustering
"""cluster = KMeans(n_clusters=100)
cluster.fit_predict(locations)
num_clusters = len(set(cluster.labels_))"""

# Sonuçları harita üzerinde görselleştirme

# Harita oluşturma
map = folium.Map(location=[center_lat, center_long], zoom_start=10)

# Renkler tablosu oluşturma
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen',
          'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
print(num_clusters," Küme oluşturuldu")
for i in range(num_clusters):
    cluster_points = []

    # Sepetleri oluşturma
    for j in range(len(cluster.labels_)):
        if cluster.labels_[j] == i:
            cluster_points.append(locations[j])

    # Renkleri atama
    color_index = i % len(colors)

    # Enlem ve boylam ortalamasını alarak dairelerin merkezlerini yerleştirir daha sonra bu merkezden 2km çapa sahip bir çember oluşturma
    folium.Circle(location=[np.mean([p[0] for p in cluster_points]),
                            np.mean([p[1] for p in cluster_points])],
                  radius=2000,
                  color=colors[color_index],
                  fill=False).add_to(map)

    # Noktaları oluşturma
    for point in cluster_points:
        folium.Marker(location=point, icon=folium.Icon(color=colors[color_index])).add_to(map)

# Haritayı kaydetme
map.save('cluster_map.html')
