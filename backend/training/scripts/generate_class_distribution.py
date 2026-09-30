import matplotlib.pyplot as plt

classes = ["D00", "D10", "D20", "D40"]
counts = [150, 5, 177, 136]

plt.figure(figsize=(8, 5))

bars = plt.bar(classes, counts)

plt.title("Distribution of Road Damage Classes")
plt.xlabel("Road Damage Class")
plt.ylabel("Number of Instances")

for bar, value in zip(bars, counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 3,
        str(value),
        ha="center"
    )

plt.tight_layout()
plt.savefig("road_damage_class_distribution.png", dpi=300)
plt.show()