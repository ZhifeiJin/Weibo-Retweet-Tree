import csv


def saveCSV(l, new):
    if new:
        print("new")
        with open('test.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for i in l:
                writer.writerow(i)
    else:
        print("not new")
        with open('test.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for i in l:
                writer.writerow(i)


def main():
    print("Input a bool: ")
    x = bool(int(input()))
    print(x)
    l1 = [[1, 2, 3, 4]]
    l2 = [[5, 6, 7, 8], [1, 2, 3, 4]]
    #saveCSV(l1, True)
    saveCSV(l2, x)


if __name__ == '__main__':
    main()
