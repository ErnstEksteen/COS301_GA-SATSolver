from BitVector import BitVector
import random
import timing
bv = BitVector(intVal=0)
print("Start Initialisation Tests")

timing.start()
for i in range(51):
    bv = bv.gen_random_bits(50)
timing.log("Random Initialisation with n = 50", 50.0)

timing.start()
for i in range(51):
    bv = bv.gen_random_bits(10000)
timing.log("Random Initialisation with n = 10,000", 50.0)

timing.start()
for i in range(51):
    bv = bv.gen_random_bits(250000)
timing.log("Random Initialisation with n = 250,000", 50.0)

timing.start()
for i in range(51):
    bv = bv.gen_random_bits(1000000)
timing.log("Random Initialisation with n = 1,000,000", 50.0)

print("Start Random Access Tests")

bv = bv.gen_random_bits(50)
timing.start()
for i in range(51):
    bv[random.randrange(50)]
timing.log("Random Access with n = 50", 50.0)

bv = bv.gen_random_bits(10000)
timing.start()
for i in range(51):
    bv[random.randrange(10000)]
timing.log("Random Access with n = 10,000", 50.0)

bv = bv.gen_random_bits(250000)
timing.start()
for i in range(51):
    bv[random.randrange(250000)]
timing.log("Random Access with n = 250,000", 50.0)

bv = bv.gen_random_bits(1000000)
timing.start()
for i in range(51):
    bv[random.randrange(1000000)]
timing.log("Random Access with n = 1,000,000", 50.0)
