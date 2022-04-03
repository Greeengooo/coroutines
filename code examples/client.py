import random


def main():
    with open("data/sample-2mb-text-file.txt", 'a') as file:
        phrases = ["python", "test", "sample", "afafa", "asfwgewwegg", "l,lbm,opm", "lkmowmg", "dmgwogmw", "lmfmgp[g", "olmowmg"]
        for _ in range(1, 100):
            file.write(phrases[random.randint(0, 9)] + '\n')


if __name__ == '__main__':
    main()
