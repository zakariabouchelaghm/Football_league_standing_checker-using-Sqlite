import threading

from query import league
import customtkinter as ctk
from CTkTable import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        #window configuration
        self.title("League Standing Checker")
        self.geometry("800x600")
        self.l=league()
        #Define the header frame
        self.header_frame=ctk.CTkFrame(self,fg_color="transparent")
        self.header_frame.pack(padx=0, pady=0)
        #Define the league button
        self.leagues=self.l.list_leagues()
        self.league_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.leagues.values()),width=200)
        self.league_menu.grid(row=0, column=0, padx=10, pady=10)

        #Define the season button
        self.seasons=self.l.list_seasons()
        self.season_menu=ctk.CTkOptionMenu(self.header_frame,values=list(self.seasons.values()))
        self.season_menu.grid(row=0, column=1, padx=10, pady=10)

        #Add a query button
        self.query_button=ctk.CTkButton(self.header_frame,text="Query Standing",command=self.query_league,fg_color="#1f538d",hover_color="#14375e")
        self.query_button.grid(row=0, column=2, padx=10, pady=10)

        #add a progressif bar
        self.loading_bar = ctk.CTkProgressBar(self.header_frame, orientation="horizontal", width=150, mode="indeterminate") 
        #define a by default table
        self.table_data=[["Position","Team","GF","GA","GD","P"]]
        for i in range(1,21):
         self.table_data.append([i," "," "," " ," " ," " ])
        self.table=CTkTable(master=self,row=21,column=6,values=self.table_data)
        self.table.edit_row(0, font=("Arial", 13, "bold"))
        self.table.pack(expand=True, fill="both", padx=20, pady=20)
       
    def query_league(self):
       # 1. Start loading animation
        self.query_button.configure(state="disabled") # Prevent double clicks
        self.loading_bar.grid(row=0, column=3, padx=10) # Show the bar
        self.loading_bar.start()

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
        new_table_data = [["Position", "Team", "GF", "GA", "GD", "P"]]
        for t in standing:
            new_table_data.append([i, t, standing[t][1], standing[t][2], standing[t][3], standing[t][0]])
            i+=1
        # 3. Update the UI back on the main thread
        self.after(0, self.update_table, new_table_data)
    
    def update_table(self, data):
        # --- This runs back on the main thread ---
        if hasattr(self, "table"):
            self.table.destroy()

        self.table = CTkTable(master=self, values=data)
        self.table.edit_row(0, font=("Arial", 13, "bold"))
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

        # Stop and hide loading bar
        self.loading_bar.stop()
        self.loading_bar.grid_forget()
        self.query_button.configure(state="normal")
    """"
    def query_league(self):
        if hasattr(self, "table") and self.table is not None:
           self.table.destroy()
        season=self.season_menu.get()
        league=self.league_menu.get()
        standing=self.l.get_league_standing(league,season)
        i=1
        self.table_data=[["Position","Team","GF","GA","GD","P"]]
        for t in standing:
         self.table_data.append([i,t,standing[t][1],standing[t][2],standing[t][3],standing[t][0]])
         i+=1
        self.table=CTkTable(master=self,row=len(standing)+1,column=6,values=self.table_data)
        self.table.edit_row(0, font=("Arial", 13, "bold"))
        self.table.pack(expand=True, fill="both", padx=20, pady=20)
    """

if __name__=="__main__":
    app=App()
    app.mainloop()



