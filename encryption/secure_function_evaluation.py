import random

alice = 22
bob = 4
carol = 17

alice_values = [0 for elem in range(3)]
bob_values = [0 for elem in range(3)]
carol_values = [0 for elem in range(3)]

def generate_values(values, base):
    while sum(values) != (base + 100):
        for i in range(len(values)):
            values[i] = random.randint(base, 100)


generate_values(alice_values, alice)
generate_values(bob_values, bob)
generate_values(carol_values, carol)

print("alice values: ", alice_values)
print("bob values: ", bob_values)
print("carol values: ", carol_values)

bob_sum = bob_values[0] + alice_values[1] + carol_values[1]
alice_sum = alice_values[0] + bob_values[1] + carol_values[2]
carol_sum = carol_values[0] + alice_values[2] + bob_values[2]
total_sum = bob_sum + alice_sum + carol_sum

if (alice + bob + carol) == (total_sum % 100):
    print("""Alice, Bob, and Carol all know the total, but not the individual votes.""")
else:
    print("Totals don't match.")
