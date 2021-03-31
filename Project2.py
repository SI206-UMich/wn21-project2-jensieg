from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names. 
    If there is more than one author, only include the first author listed.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    s_directory = os.path.dirname(__file__)
    file_path = os.path.join(s_directory, filename)
    fhand = open(file_path)
    data = fhand.read()
    fhand.close()
    soup = BeautifulSoup(data, 'lxml')
    titles = soup.find_all('a', class_= 'bookTitle')
    authors = soup.find_all('span', itemprop= 'author')
    all_titles = []
    all_authors = [] 
    lst = []
    for t in titles:
        all_titles.append(t.text.strip())
    for a in authors:
        all_authors.append(a.contents[1].text.strip('\n'))
    for i in range(len(all_titles)):
        lst.append((all_titles[i], all_authors[i]))
    return lst
    

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    lst = []
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    books = soup.find('table', {'class' : 'tableList'})
    titles = books.find_all('a', class_ = 'bookTitle')
    for title in titles:
        ending = title.get('href')
        if ending.startswith('/book/show/'):
            lst.append("https://www.goodreads.com" + ending) 
    return lst[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    html_text = requests.get(book_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    book = soup.find('div', {'class' : 'leftContainer'})
    title = book.find('h1', id = 'bookTitle').text.strip('\n')
    t_final = title.lstrip()
    author = book.find('span', itemprop = 'name').text
    pages = book.find('span', itemprop = 'numberOfPages').text.strip(' pages')
    p_final= pages.strip('\n')
    final = (t_final, author, int(p_final))
    return final


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    lst = [] #categories
    lst2 = [] #urls
    lst3 = [] #titles
    final = []
    fhand = open(filepath)
    data = fhand.read()
    fhand.close()
    soup = BeautifulSoup(data, 'lxml')
    categories = soup.find_all('h4', class_ = "category_copy")
    urls = soup.find_all('a')
    titles = soup.find_all('img', class_ = 'category__winnerImage')
    for title in titles:
        lst3.append(title.get('alt'))
    for u in urls:
        url = u.get('href')
        if url.startswith('https://www.goodreads.com/genres/'):
            lst2.append(url)
    for c in categories:
        lst.append(c.text)
    for i in range(len(lst)):
        final.append((lst[i], lst3[i], lst2[i]))
    return final


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    filename = open('funcfile.csv', 'w') #idk about this line 
    filename.write('Book Title,Author Name')
    filename.write('\n')
    for d in data:
        row_string = '{},{}.format(d[0],d[1])'
        filename.write(row_string)
        filename.write('\n')

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    search_urls = get_search_links() 


    def test_get_titles_from_search_results(self):
        titles = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIs(type(titles), list)
        # check that each item in the list is a tuple
        for title in titles:
            self.assertIs(type(title), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIs(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertIs(type(url), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertIn('https://www.goodreads.com/book/show/', url)


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        # check that each item in the list is a tuple
        for s in summaries:
            self.assertIs(type(s), tuple)
        # check that each tuple has 3 elements
        for s in summaries:
            self.assertEqual(len(s), 3)
        # check that the first two elements in the tuple are string
        for s in summaries:
            self.assertIs(type(s[0]), str)
            self.assertIs(type(s[1]), str)
            self.assertIs(type(s[2]), int)
        # check that the third element in the tuple, i.e. pages is an int
        self.assertEqual(summaries[0][2], 337)
        # check that the first book in the search has 337 pages


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable

        # check that we have the right number of best books (20)

            # assert each item in the list of best books is a tuple

            # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        pass

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        full_csv = write_csv(titles, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = full_csv.readlines()
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], 'Book Title,Author Name')
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1],'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')


if __name__ == '__main__':
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



