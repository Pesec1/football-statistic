
# Football statistic

Web scraped data from https://soccer365.ru/competitions/13/ using  BeautifulSoup and requests libraries.
Convert extracted data to DataFrames and did the following tasks:
- The top three teams by the number of goals scored with their number displayed.
- The first three teams by the number of yellow cards.
- List of players who did not participate in all games of their team. The number of games of a team is determined by the maximum number of matches of its players
- Proportion of penalties in relation to the number of goals for each team.
- Correlation of the number of goals with the number of team points. Take points from the first table on the team rating page.



## Run Locally

Clone the project

```bash
  git clone https://github.com/Pesec1/football-statistic
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install pandas
  pip install requests
  pip install BeautifulSoup
```

Execute

```bash
  python main.py
```




