import random

def prng_service():
    """Generates a random number and writes the number to prng_file"""
    while True:
        prng_file = open('prng-service.txt', 'r+')
        prng_data = prng_file.readline()

        if prng_data == 'run':
            rand_num = str(random.randint(1, 1025))
            prng_file.seek(0)
            prng_file.truncate()
            prng_file.write(rand_num)
        prng_file.close()
        

if __name__ == "__main__":
    prng_service()