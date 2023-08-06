from psychonautcrawler.crawler import Crawler

def main():
    url = 'https://psychonautwiki.org/wiki/LSD'
    c = Crawler(url)
    c.print_doses()

if __name__ == '__main__':
    main()
