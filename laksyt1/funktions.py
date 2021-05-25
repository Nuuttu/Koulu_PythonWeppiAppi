import sys

if len(sys.argv)<2:
    sys.exit("Kerro nimesi")

nimi = sys.argv[1]

def moi(nimi):
    return f"moi { nimi }"

def main():
    print(moi(nimi))

if __name__ == "__main__":
    main()