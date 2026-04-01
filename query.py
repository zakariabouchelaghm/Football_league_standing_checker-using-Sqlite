import sqlite3
import threading
class league:
    def __init__(self):
        self.connect=sqlite3.connect('database.sqlite', check_same_thread=False)
        self.cur=self.connect.cursor()
        self.is_cancelled = False
        self.lock=threading.Lock()
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
             League WHERE name=?) AND season=?
             UNION
             SELECT Distinct away_team_api_id as id from match WHERE league_id=(SELECT id FROM
             League WHERE name=?) AND season=?)
             SELECT t.team_long_name,ti.id from team t join team_ids ti ON t.team_api_id=ti.id;
             """
            params=(league,season,league,season)
            with self.connect:
                  self.cur.execute(query,params)
                  teams={value: key for key, value in self.cur.fetchall()}
            return teams
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def get_league_standing(self,league,season):
        
            query = """
    SELECT 
        t.team_long_name,
        SUM(CASE WHEN (m.home_team_api_id = t.team_api_id AND m.home_team_goal > m.away_team_goal) OR 
                      (m.away_team_api_id = t.team_api_id AND m.away_team_goal > m.home_team_goal) THEN 3
                 WHEN m.home_team_goal = m.away_team_goal THEN 1 ELSE 0 END) as Points,
        COUNT(CASE WHEN (m.home_team_api_id = t.team_api_id AND m.home_team_goal > m.away_team_goal) OR 
                        (m.away_team_api_id = t.team_api_id AND m.away_team_goal > m.home_team_goal) THEN 1 END) as Wins,
        COUNT(CASE WHEN m.home_team_goal = m.away_team_goal THEN 1 END) as Draws,
        COUNT(CASE WHEN (m.home_team_api_id = t.team_api_id AND m.home_team_goal < m.away_team_goal) OR 
                        (m.away_team_api_id = t.team_api_id AND m.away_team_goal < m.home_team_goal) THEN 1 END) as Losses,
        SUM(CASE WHEN m.home_team_api_id = t.team_api_id THEN m.home_team_goal ELSE m.away_team_goal END) as GF,
        SUM(CASE WHEN m.home_team_api_id = t.team_api_id THEN m.away_team_goal ELSE m.home_team_goal END) as GA,
        (SUM(CASE WHEN m.home_team_api_id = t.team_api_id THEN m.home_team_goal ELSE m.away_team_goal END) -
         SUM(CASE WHEN m.home_team_api_id = t.team_api_id THEN m.away_team_goal ELSE m.home_team_goal END) ) as GD
    FROM Team t
    JOIN Match m ON t.team_api_id = m.home_team_api_id OR t.team_api_id = m.away_team_api_id
    WHERE m.league_id = (SELECT id FROM League WHERE name = ?) AND m.season = ?
    GROUP BY t.team_api_id
    ORDER BY Points DESC, (GF - GA) DESC
    """
            with self.lock:
                self.cur.execute(query,(league,season))
                rows=self.cur.fetchall()
                return rows
            
            
              
    def get_teams_by_name(self,league,season):
        try:
            query="""
            SELECT DISTINCT team_long_name FROM team t join Match m on 
            (t.team_api_id=m.home_team_api_id or t.team_api_id=
            m.away_team_api_id) where m.league_id=(select id from League 
            where name=?)
            and season=?
            """
            params=(league,season)
            self.cur.execute(query,params)
            teams=[row[0] for row in self.cur.fetchall()]
            return sorted(teams)
        except Exception as e:
            print(f"An error occurred: {e}")
    def get_team_pathway(self,team,season):
        try:
            query="""
            SELECT DATE(m.date),t1.team_long_name,m.home_team_goal,t2.team_long_name,
            m.away_team_goal FROM match m JOIN Team t1 ON
            m.home_team_api_id=t1.team_api_id
            join Team t2 on m.away_team_api_id=t2.team_api_id WHERE (
            m.home_team_api_id=(SELECT team_api_id from Team WHERE 
            team_long_name=?) OR
            m.away_team_api_id=(SELECT team_api_id from Team WHERE 
            team_long_name=?))
            AND season=? ORDER BY m.date;
            """
            params=(team,team,season)
            self.cur.execute(query,params)
            pathway=self.cur.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
        return pathway
        
