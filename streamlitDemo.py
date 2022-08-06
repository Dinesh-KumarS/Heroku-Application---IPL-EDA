import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

matches_df = pd.read_csv('C:/Users/Dinesh/Desktop/ML Projects/IPL Dataset Assignment/matches.csv')
deliveries_df = pd.read_csv('C:/Users/Dinesh/Desktop/ML Projects/IPL Dataset Assignment/deliveries.csv')
batsmen = matches_df[['id','season']].merge(deliveries_df, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
seasons = batsmen.groupby(['season'])['total_runs'].sum().reset_index()

st.title("IPL Dataset - EDA")

st.header("""
Let's Explore the dataset and visualize the answers for below questions

1.  Highest Score recorded across each seasons?
2.  Players with maximum man of the match awards?
3.  Which team has highest winning portfolio?
4.  Percentage of Batting and Fielding chosen by toss winnners?
5.  Top 5 Batsman's Performance over the year?
6.  Batsman scored maximum sixes in their ipl career?
7.  Batsman scored maximum boundaries in their ipl career?
8.  Batsman faced many dot balls in their ipl career?
9.  Bowlers delived most dotball in their ipl career?
10. Bowlers consumed most sixs in their ipl career?
11. Bowlers consumed most fours in their ipl career?

""")

st.header("Scroll down for answers!!")
def maxScoreinSeasons_barChart():
    st.subheader("1) High score in each season")
    fig = plt.figure(figsize=(10,7))
    plt.title('Highest runs across season',fontsize=20,color='royalblue')
    ax = sns.barplot(x=seasons['season'],y=seasons['total_runs'])
    ax.set_xlabel("Seasons", fontsize = 15)
    ax.set_ylabel("Highest runs", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)

def maxScoreinSeasons_Graph():
    fig = plt.figure(figsize=(10,7))
    plt.xlabel('season',fontsize=15)
    plt.ylabel('runs scores',fontsize=15)
    plt.title('Overall runs scored in a calender year',fontsize=20)
    plt.plot(seasons['season'],seasons['total_runs'],marker='o')
    st.pyplot(fig)

    st.write("Highest scored was recorded is Season 6 in 2013")

def manOfMatch_Seasons():
    st.subheader("2) Man of the Match Awards")
    mom = matches_df['player_of_match'].value_counts().reset_index()
    mom.rename(columns={'index':'player_name','player_of_match':'count'},inplace=True)
    fig = plt.figure(figsize=(14,8))
    plt.title('Maximum man of the match awards',fontsize=25)
    ax = sns.barplot(x=mom['player_name'][:10],y=mom['count'][:10],color='grey')
    ax.set_xlabel('player_name',fontsize=20)
    ax.set_ylabel('count of man of match awards',fontsize=20)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Chris Gayle won most MOM Awards!!!...")

def maxMatches_Won():
    st.subheader("3) Most Winning Team in IPL")
    most_wins = matches_df['winner'].value_counts().reset_index()
    most_wins.rename(columns={'index':'Team','winner':'count'},inplace=True)
    fig = plt.figure(figsize=(23,10))
    plt.title('Maximum matches won by each team',fontsize=35)
    ax = sns.barplot(x=most_wins['Team'][:10],y=most_wins['count'][:10])
    ax.set_xlabel('Team names',fontsize=30)
    ax.set_ylabel('Most wins',fontsize=30)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Mumbai India is the most successful team in IPL.")

def tossFactor():
    st.subheader("4) Ratio of selecting Bat/Field after toss")
    tossFactor = matches_df.toss_decision.value_counts()
    labels = (np.array(tossFactor.index))
    sizes = (np.array((tossFactor / tossFactor.sum())*100))
    colors = ['skyblue', 'lightgreen']
    fig = plt.figure(figsize=(6,4))
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Toss decision percentage")
    st.pyplot(fig)
    st.write("Interesting, most captains perfered chasing after winning the toss.")

def batsman_highScore():
    st.subheader("5) Performance of Top 5 Batter's")
    highest_runscorers = batsmen.groupby(['season','batsman'])['batsman_runs'].sum().unstack().T
    highest_runscorers['Total'] = highest_runscorers.sum(axis=1)
    highest_runscorers = highest_runscorers.sort_values(by='Total',ascending = False).drop('Total',axis=1)
    fig = plt.figure(figsize=(10,8))
    plt.plot(highest_runscorers[:5].T,label=highest_runscorers.index[:5])
    plt.title('Graphical Represenetation of Top 5 Batsman in IPL',fontsize=20)
    plt.xlabel('Seasons',fontsize=15)
    plt.ylabel('Runs',fontsize=15)
    plt.legend()
    st.pyplot(fig)
    st.write("Virat Kohli's batting performance had been improved in each season expect the last one, unLuckly!")
    st.write("Suresh rains looks a conisistent player you can bet on.")

def mostSixes_Scored():
    st.subheader("6) Most sixes scored by batsman")
    most_sixes = deliveries_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='batsman_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(12,8))
    plt.title('Batsman with most number of sixes',fontsize=20)
    ax =sns.barplot(x=most_sixes['batsman'][:10],y=most_sixes['batsman_runs'][:10],color='red')
    ax.set_xlabel("Batsman", fontsize = 15)
    ax.set_ylabel("Number of sixes", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Again, Chris Gayle who won most MOM has hit maximum sixes in IPL.")

def mostBoundaries_Scored():
    st.subheader("7) Most boundaries scored by batsman")
    most_boundaries = deliveries_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='batsman_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(12,8))
    plt.title('Batsman with most number of boundaries',fontsize=20)
    ax = sns.barplot(x=most_boundaries['batsman'][:10],y=most_boundaries['batsman_runs'][:10],color='lightgreen')
    ax.set_xlabel("Batsman", fontsize = 15)
    ax.set_ylabel("Number of boundaries", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Gambhir has scored most boundaries in IPL.")

def mostDotBall_Faced():
    st.subheader("8) Most dotball faced")
    mostDotBalls_faced = deliveries_df.groupby('batsman')['batsman_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='batsman_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(14,8))
    plt.title('Batsman with most dot falls faced',fontsize=20)
    ax = sns.barplot(x=mostDotBalls_faced['batsman'][:10],y=mostDotBalls_faced['batsman_runs'][:10],color='cyan')
    ax.set_xlabel("Batsman", fontsize = 15)
    ax.set_ylabel("Number of dotballs", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Gambhir faced most dot balls and takes time to settle in the Crease.")

def mostDotBalls_Bowled():
    st.subheader("9) Most dotball bowled")
    mostDotBalls_bowled = deliveries_df.groupby('bowler')['total_runs'].agg(lambda x: (x==0).sum()).reset_index().sort_values(by='total_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(14,8))
    plt.title('Most dot balls bowled',fontsize=20)
    ax = sns.barplot(x=mostDotBalls_bowled['bowler'][:10],y=mostDotBalls_bowled['total_runs'][:10],color='chocolate')
    ax.set_xlabel("Bowler", fontsize = 15)
    ax.set_ylabel("Number of dotballs", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Pravin Kumar is the one you need to defend the score who can bowl most dot balls and make batsman nervous in the batting field.")   

def mostSix_Bowled():
    st.subheader("10) Most sixes bowled")
    mostsixes_consumed = deliveries_df.groupby('bowler')['total_runs'].agg(lambda x: (x==6).sum()).reset_index().sort_values(by='total_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(14,8))
    plt.title('Most six consumed by bowlers',fontsize=20)
    ax = sns.barplot(x=mostsixes_consumed['bowler'][:10],y=mostsixes_consumed['total_runs'][:10],color='deepskyblue')
    ax.set_xlabel("Bowler", fontsize = 15)
    ax.set_ylabel("Number of sixes", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Amit Mishra has given out lot of sixes in the history of IPL.")

def mostFour_Bowled():
    st.subheader("11) Most fours bowled")
    mostfours_consumed = deliveries_df.groupby('bowler')['total_runs'].agg(lambda x: (x==4).sum()).reset_index().sort_values(by='total_runs',ascending=False).reset_index(drop=True)
    fig = plt.figure(figsize=(14,8))
    plt.title('Most fours consumed by bowlers',fontsize=20)
    ax = sns.barplot(x=mostfours_consumed['bowler'][:10],y=mostfours_consumed['total_runs'][:10],color='lightsalmon')
    ax.set_xlabel("Bowler", fontsize = 15)
    ax.set_ylabel("Number of fours", fontsize = 15)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)
    st.write("Ohh, there should be correlation with P.Kumar bowling most dot ball and giving most fours.")
    
maxScoreinSeasons_barChart()
maxScoreinSeasons_Graph()
manOfMatch_Seasons()
maxMatches_Won()
tossFactor()
batsman_highScore()
mostSixes_Scored()
mostBoundaries_Scored()
mostDotBall_Faced()
mostDotBalls_Bowled()
mostSix_Bowled()
mostFour_Bowled()

st.header("This is not the end, can go futher with the analysis")
st.subheader("The results derived from the analysis with a possible dream winning team with bat/bowl")
st.write("""
Mumbai Indians - Most wins
1.  Chris Gayle
2.  Virat Kolhi
3.  David Warner
4.  Suresh Raina
5.  RG Sharma
6.  Gambhir
7.  Pravin Kumar
8.  Harbajan singh
9.  Dw Steyn
10. Malinga
11. BKumar
""")


