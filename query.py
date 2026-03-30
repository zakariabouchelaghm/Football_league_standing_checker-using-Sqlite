import sqlite3

class league:
    def __init__(self):
        self.connect=sqlite3.connect('database.sqlite')
        self.cur=self.connect.cursor()
        self.leagues={1:"England Premier League",2:"Spain LIGA BBVA",3:"Italy Serie A",4:"France Ligue 1",5:"Germany 1. Bundesliga"}
        self.seasons={1:"2008/2009",2:"2009/2010",3:"2010/2011",4:"2011/2012",5:"2012/2013",6:"2013/2014",7:"2014/2015",8:"2015/2016"}
    def list_leagues(self):
        return self.leagues
    def list_seasons(self):
        return self.seasons
    def get_teams(self,league,season):
        try:
            query = """
             WITH team_ids AS(
              SELECT Distinct home_team_api_id as id from match WHERE league_id=(SELECT id FROM
             League WHERE name=? AND season=?) 
             UNION
             SELECT Distinct away_team_api_id as id from match WHERE league_id=(SELECT id FROM
             League WHERE name=? AND season=?))
             SELECT t.team_long_name,ti.id from team t join team_ids ti ON t.team_api_id=ti.id;
             """
            params=(league,season,league,season)
            with self.connect:
                  self.cur.execute(query,params)
                  teams={value: key for key, value in self.cur.fetchall()}
            return teams
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_points(self,team,season):
        try:
            query="""
               WITH utd_points AS (SELECT date,CASE
               WHEN is_tie=0 AND Match_winner=? THEN 3
               WHEN is_tie=1 THEN 1
               ELSE 0
               END AS points FROM Match WHERE (home_team_api_id =?
                OR away_team_api_id =?) AND season=?)
               SELECT COALESCE(SUM(points), 0) AS points FROM utd_points; 
              """
            params=(team,team,team,season)
            with self.connect:
                  self.cur.execute(query,params)
                  row=self.cur.fetchone()
            return row[0]
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_goals(self,team,season):
        try:
            query="""
              WITH goals as (SELECT SUM(home_team_goal) as goals FROM Match m JOIN Team t ON m.home_team_api_id=
              t.team_api_id WHERE t.team_api_id=? and m.season=?
              UNION
              SELECT SUM(away_team_goal) as goals FROM Match m JOIN Team t ON m.away_team_api_id=
              t.team_api_id WHERE t.team_api_id=? and m.season=?)
              SELECT SUM(goals) FROM goals;
              """
            params=(team,season,team,season)
            with self.connect:
                  self.cur.execute(query,params)
                  row=self.cur.fetchone()
            return row[0]
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_goals_against(self,team,season):
        try:
            query="""
             WITH goals as (SELECT SUM(home_team_goal) as goals FROM Match m JOIN Team t ON m.away_team_api_id=
             t.team_api_id WHERE t.team_api_id=? and m.season=?
             UNION
             SELECT SUM(away_team_goal) as goals FROM Match m JOIN Team t ON m.home_team_api_id=
             t.team_api_id WHERE t.team_api_id=? and m.season=?)
             SELECT SUM(goals) FROM goals;
             """
            params=(team,season,team,season)
            with self.connect:
                  self.cur.execute(query,params)
                  row=self.cur.fetchone()
            return row[0]
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_goals_diff(self,team,season):
        try:
            return self.get_goals(team,season)-self.get_goals_against(team,season)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_league_standing(self,league,season):
        try:
            teams=self.get_teams(league,season)
            stats={}
            for team in teams:
                points=self.get_points(team,season)
                goals_for=self.get_goals(team,season)
                goals_against=self.get_goals_against(team,season)
                goals_diff=self.get_goals_diff(team,season)
                stats[teams[team]]=[points,goals_for,goals_against,goals_diff]
            sorted_data = dict(sorted(stats.items(), key=lambda item: (item[1][0],item[1][3]),reverse=True))    
            return sorted_data
        except Exception as e:
            print(f"An error occurred: {e}")
    
l=league()
print("Welcome to our champions checker!!")
print("We have statictics about:")
leagues=l.list_leagues()

for ligue in leagues:
    print(f"{ligue}-{leagues[ligue]}")

print("We have the followng seasons:")
seasons=l.list_seasons()
for saison in seasons:
    print(f"{saison}-{seasons[saison]}")
while True:
  checked_ligue=False
  while not checked_ligue: 
   ligue=input("Select the league you want (1 or 2 or 3 or 4 or 5): ")
   if ligue.isdigit():
    if int(ligue) in [1,2,3,4,5]:
     checked_ligue=True
    else:
     print("Enter a valid number from 1 to 5.")
   else:
     print("Enter a number.")

  checked_season=False
  while not checked_season: 
   season=input("Select the season you want (from 1 to 8): ")
   if season.isdigit():
    if int(season) in [1,2,3,4,5,6,7,8]:
     checked_season=True
    else:
     print("Enter a valid number from 1 to 8.")
   else:
     print("Enter a number.")
  print(f"{leagues[int(ligue)]}-{seasons[int(season)]}")
  standing=l.get_league_standing(leagues[int(ligue)],seasons[int(season)])
  i=1
  for t in standing:
     print(f"{i}- {t}: GF:{standing[t][1]} | GA:{standing[t][2]} | GD:{standing[t][3]} | P:{standing[t][0]}")
     i+=1
  print("Done!")


  



