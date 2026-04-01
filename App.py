import threading
from PIL import Image
from query import league
import customtkinter as ctk
from CTkTable import *

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.l=league()
        #window configuration
        self.title("European Football League Standings Checker")
        self.geometry("800x600")
        

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #home_page
        self.home_frame=ctk.CTkFrame(self,fg_color="transparent")
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.home_frame.grid_columnconfigure(0, weight=1)

        
        
        
        #Welcome label
        self.welcome_label=ctk.CTkLabel(self.home_frame,text="Welcome to European Football Leagues stats app",font=("Arial", 24),fg_color="transparent", 
        bg_color="transparent")
        self.welcome_label.grid(row=0, column=0, padx=10, pady=10)

        #description label
        self.desc_label=ctk.CTkLabel(self.home_frame,text="This App contains statistiques about the top 5 leagues in europe from 2008 to 2016",font=("Arial", 16),fg_color="transparent")
        self.desc_label.grid(row=1, column=0, padx=10, pady=10)
       
        self.line = ctk.CTkFrame(self.home_frame, height=2, fg_color="gray50")
        self.line.grid(row=2, column=0, padx=100, pady=20, sticky="ew")
        #final_league_standing_description_label
        self.desc_label=ctk.CTkLabel(self.home_frame,text="1-Get the final standings for any league and season",font=("Arial", 14),fg_color="transparent")
        self.desc_label.grid(row=3, column=0, padx=10, pady=10)
        #Add a query button
        self.query_button=ctk.CTkButton(self.home_frame,text="Open Standing Checker",command=lambda:self.show_page(self.league_standing),fg_color="#1f538d",hover_color="#14375e")
        self.query_button.grid(row=4, column=0, padx=10, pady=10)
        
        #final_pathway_description_label
        self.desc_label=ctk.CTkLabel(self.home_frame,text="2-Get the pathway for any team and season",font=("Arial", 14),fg_color="transparent")
        self.desc_label.grid(row=5, column=0, padx=10, pady=10)

        self.pathway_button=ctk.CTkButton(self.home_frame,text="Open team pathway",command=lambda:self.show_page(self.team_pathway),fg_color="#1f538d",hover_color="#14375e")
        self.pathway_button.grid(row=6, column=0, padx=10, pady=10)

        #initialize league standing frame
        self.league_standing=league_standing(self)
        self.league_standing.grid(row=0, column=0, sticky="nsew")

        self.team_pathway=team_pathway(self)
        self.team_pathway.grid(row=0, column=0, sticky="nsew")
        

        # Initialize pages immediately
        self.league_standing = league_standing(self)
        self.team_pathway = team_pathway(self)
        
        for frame in (self.home_frame, self.league_standing, self.team_pathway):
            frame.grid(row=0, column=0, sticky="nsew")


        self.home_frame.tkraise()
        self.home_frame.focus_set()
    def show_page(self,frame):
        frame.tkraise()


class league_standing(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.l=master.l

        #Define the header frame
        self.header_frame=ctk.CTkFrame(self,fg_color="transparent")
        self.header_frame.pack(padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=0)
        self.header_frame.grid_columnconfigure(3, weight=0)
        self.header_frame.grid_columnconfigure(4, minsize=170)
        

        self.stop_thread=False


        #Define a go back to main button
        self.back_button=ctk.CTkButton(self.header_frame,text="Back",command=lambda: master.show_page(master.home_frame),fg_color="#1f538d",hover_color="#14375e",width=100)
        self.back_button.grid(row=0, column=0, padx=10, pady=10)

        #Define the league button
        self.leagues=self.l.list_leagues()
        self.league_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.leagues.values()),width=200)
        self.league_menu.grid(row=0, column=1, padx=10, pady=10)
        
        #Define the season button
        self.seasons=self.l.list_seasons()
        self.season_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.seasons.values()))
        self.season_menu.grid(row=0, column=2, padx=10, pady=10)

        #Add a query button
        self.query_button=ctk.CTkButton(self.header_frame,text="Query Standing",command=self.query_league,fg_color="#1f538d",hover_color="#14375e")
        self.query_button.grid(row=0, column=3, padx=10, pady=10)

        #define a by default table
        self.table_data=[["Position", "Team", "W", "D", "L", "GF", "GA", "GD", "P"]]
        for i in range(1,21):
         self.table_data.append([i," "," "," " ," " ," "," " ," " ," " ])
        self.table=CTkTable(master=self,row=21,column=9,values=self.table_data,font=("Arial", 12))
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

   
    def query_league(self):
       # 1. Start loading animation
        self.query_button.configure(state="disabled") # Prevent double clicks

        # 2. Start the database query in a separate thread
        threading.Thread(target=self.run_query_task, daemon=True).start()
    def run_query_task(self):
        # --- This runs in the background ---
        season = self.season_menu.get()
        league = self.league_menu.get()
        
        # This is the slow part:
        standing = self.l.get_league_standing(league, season)
        i=1
        # Prepare the data
        new_table_data = [["Position", "Team", "W", "D", "L", "GF", "GA", "GD", "P"]]
        for t in standing:
            new_table_data.append([i, t[0], t[2], t[3], t[4], t[5], t[6],t[7], t[1]])
            i+=1
        # 3. Update the UI back on the main thread
        self.after(0, self.update_table, new_table_data)
    
    def update_table(self, data):
        self.table.update_values(data)
        self.query_button.configure(state="normal")

        
    def back_button(self):
        self.l.is_cancelled = True
        try:
            self.l.connection.interrupt()
        except:
            pass
        self.master.show_page(self.master.home_frame)
            
class team_pathway(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #window configuration
        #self.title("European Football League Standings Checker")
        #self.geometry("800x600")
        self.l=master.l
        #Define the header frame
        self.header_frame=ctk.CTkFrame(self,fg_color="transparent")
        self.header_frame.pack(padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=0)
        self.header_frame.grid_columnconfigure(3, weight=0)
        #Define a go back to main button
        

        self.back_button=ctk.CTkButton(self.header_frame,text="Back",command=lambda: master.show_page(master.home_frame),fg_color="#1f538d",hover_color="#14375e",width=100)
        self.back_button.grid(row=0, column=0, padx=10, pady=10)

        #Define the league button
        self.leagues=self.l.list_leagues()
        self.league_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.leagues.values()),width=200)
        self.league_menu.grid(row=0, column=1, padx=10, pady=10)
        
        #Define the season button
        self.seasons=self.l.list_seasons()
        self.season_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.seasons.values()),command=self.update_teams)
        self.season_menu.grid(row=0, column=2, padx=10, pady=10)
        
        #Add a query button
        self.team_menu=ctk.CTkOptionMenu(self.header_frame,values=["Select A team"],command=self.update_teams)
        self.team_menu.grid(row=0, column=3, padx=10, pady=10)

        self.update_teams()
        
        #Add a query button
        self.query_button=ctk.CTkButton(self.header_frame,text="Query Pathway",command=self.query_pathway,fg_color="#1f538d",hover_color="#14375e")
        self.query_button.grid(row=1, column=2, padx=10, pady=10)

        #define a by default table
        self.scrollable_frame=ctk.CTkScrollableFrame(self,height=400,fg_color="transparent")
        self.scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.table_data=[["Date","Home_team","Score","Away_team"]]
        for i in range(1,39):
         self.table_data.append([" "," "," " ," " ," "])
        self.table=CTkTable(master=self.scrollable_frame,row=38,column=4,values=self.table_data,font=("Arial", 12))
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

    
    def query_pathway(self):
       # 1. Start loading animation
        self.query_button.configure(state="disabled") # Prevent double clicks
        # 2. Start the database query in a separate thread
        threading.Thread(target=self.run_query_task, daemon=True).start()
    def run_query_task(self):
        # --- This runs in the background ---
        season = self.season_menu.get()
        league = self.league_menu.get()
        team=self.team_menu.get()
        # This is the slow part:
        pathway = self.l.get_team_pathway(team, season)
        # Prepare the data
        new_table_data = [["Date","Home_team","Score","Away_team"]]
        for t in pathway:
            if t[1]==team:
             new_table_data.append([t[0],f"{t[1]} (H)", f"{t[2]}-{t[4]}", t[3]])
            else:
             new_table_data.append([t[0],f"{t[3]} (A)", f"{t[4]}-{t[2]}", t[1]])
        # 3. Update the UI back on the main thread
        self.after(0, self.update_table, new_table_data)
    
    def update_table(self, data):
        self.table.update_values(data)
        self.query_button.configure(state="normal")


    def update_teams(self,_=None):
        league=self.league_menu.get()
        season=self.season_menu.get()
        teams=self.l.get_teams_by_name(league,season)
        if teams:
            self.team_menu.configure(values=teams)
        else:
            self.team_menu.configure(values=["No Teams"])
    


if __name__=="__main__":
    app=Main()
    app.mainloop()



