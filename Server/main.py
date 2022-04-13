from Server import Server


def main():
    Server('localhost', 8080).run()


if __name__ == '__main__':
    main()