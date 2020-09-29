# WikiGender

According to the Wikipedia article on [grammatical gender](https://en.wikipedia.org/wiki/Grammatical_gender) ([version at time of writing](https://en.wikipedia.org/w/index.php?title=Grammatical_gender&oldid=980781158)),
> in Spanish, female gender is often attributed to objects that are "used by women, natural, round, or light" and male gender to objects "used by men, artificial, angular, or heavy."

The source is a similar statement in the book [Social Psychology of Culture](https://books.google.com/books?id=8xVdAgAAQBAJ&pg=PA120) by Chi-Yue Chiu and Ying-yi Hong.
No evidence is provided for this claim, as far as I can see.

This project is an attempt to test the above claim by comparing masculine and feminine nouns on the [Spanish Wikipedia](https://es.wikipedia.org/wiki/Wikipedia:Portada), specifically the claims concerning natural and artificial objects.

## Method

* The program `download_wikipedia.py` downloads a specified version of the Spanish Wikipedia from a data dump.
* The master list of masculine and feminine nouns comes from the dictionary FreeLing.
* The program `count_all_pages.py` iterates through all the articles and tallies the masculine and feminine nouns, writing the results to a text file.
* The program `sum_counts.py` sums the masculine and feminine nouns in a given article, and all the articles that it links to.

### Shortcomings

* The word *de* is a preposition and a feminine noun in Spanish.
  Every instance of the preposition *de* would be incorrectly counted as a feminine noun by `count_all_pages.py`.
  There are presumably many other examples of words being incorrectly classed as a noun.
* Certain words occur in Wikipedia articles frequently.
  For example, *Referencias* meaning References occurs in virtually every article.
  These words are not related to the subject matter of the article, but would still be counted.

## Results



## Resources

* I used [this article](https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c) as a basis for downloading and parsing the Wikipedia articles.
* I used the [list of nouns](https://raw.githubusercontent.com/TALP-UPC/FreeLing/master/data/es/dictionary/entries/MM.nom) in the dictionary FreeLing.
This list was extracted from the [Spanish Resource Grammar projects](http://www.upf.edu/pdi/iula/montserrat.marimon/srg.html) and was developed at the [Institut Universitari de Linguistica Aplicada](http://www.iula.upf.edu) of the Universitat Pompeu Fabra.
It is distributed under a "[Lesser General Public License For Linguistic Resources](https://github.com/TALP-UPC/FreeLing/blob/master/LICENSES/LGPLLR.license)" license.

