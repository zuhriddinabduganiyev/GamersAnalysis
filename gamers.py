import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from streamlit_option_menu import option_menu

df = pd.read_csv("23.csv")
last_df = pd.read_csv("23.csv")
def missing_val_check(data):
    total = data.isnull().sum().sort_values(ascending=False)
    percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat(
        [total, percent * 100], axis=1, keys=["Number of None", "Percentage of None(%)"]
    )
    return missing_data

# Fix sidebar:
st.set_page_config(layout="wide", page_title="GamersData", page_icon="🌟")
with st.sidebar:
    selected = option_menu(
        menu_title=None, 
        options=["About DataFrame", "Statistical analysis", "Graphic analysis", "Summary"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#262731"},
            "icon": {"display": "none"}, 
            "nav-link": {
                "font-size": "20px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#3e4a5e"
            },
            "nav-link-selected": {"background-color": "#3e4a5e"},
        }
    )



# First page:
if selected == "About DataFrame":
    st.write("## About DataFrame:")
    
    # A button to view the DataFrame:
    with st.expander("View DataFrame:"):
        st.write("## DataFrame")
        st.dataframe(df)
        
    # Two columns
    col1, col2 = st.columns(2)
    gameDifficulty = df['GameDifficulty'].unique()
    location = df['Location'].unique()
    
    # GameDifficulty unique values:
    with col1:
        st.subheader("Unique values ​​of the GameDifficulty column:")
        st.table({"GameDifficulty unique": gameDifficulty})
        
    # Location unique values:
    with col2:
        st.subheader("Unique values of the Location column:")
        st.table({"Location unique": location})
        
    # GameGenre unique values:
    col = st.columns(1)
    game_genres = df['GameGenre'].unique()
    with col1:
        st.subheader("Unique values of the GameGenre column:")
        st.table({"GameDifficulty unique": game_genres})
        
    # About DataFrame 
    st.write("### Strategy: Games that emphasize planning, tactics, and decision-making skills.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Starcraft_Gamescom_2017_%2836851382835%29.jpg/440px-Starcraft_Gamescom_2017_%2836851382835%29.jpg", caption="Strategy games", use_column_width=True)
    st.write("### Sports: Games that simulate the practice of sports. This includes team sports such as 'FIFA' (soccer).")
    st.image("""https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1RhEyurtgdbeQ9eel4GwGw0uztE_aT3dhsQ&s""", use_column_width=True, caption="Sport games")
    st.write("### Action: These often include combat, platforming, and other dynamic activities. For example: 'Call of Duty' (shooter).")
    st.image("https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/42700/capsule_616x353.jpg?t=1654809667", use_column_width=True, caption="Action")
    st.write("### Simulation: For example: life simulation games like 'The Sims', business simulation games like 'SimCity'.")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSarIu01D_yHhSYKXUSyOXIU0C07kKIAgqoWA&s", use_column_width=True, caption="Simulation")
    
    # DataFrame's shape
    rows, cols = df.shape
    st.write("## DataFrame's shape:")
    st.write(df.shape)
    st.markdown(f"A 'DataFrame' contains **{rows}** rows and **{cols}** columns.")
    
    # Two columns:
    col1, col2 = st.columns(2)
    # Data Types
    with col1:
        st.subheader("Data Types:")
        st.table({"DataTypes": df.dtypes})
        st.write("General:")
        game_genres = ["int - 1","float - 8 ","object - 5"]
        for genre in game_genres:
            st.write(f"- {genre}")
            
    # Column names
    with col2:
        st.subheader("Columns:")
        st.table({"Columns": df.columns})
        
    # Numeric columns:
    st.write("Columns that are Numeric:")
    st.write(df.select_dtypes("number"))
    
    # Object columns:
    st.write("Columns that are Object:")
    st.write(df.select_dtypes("object"))

 
# Second page:
elif selected=="Statistical analysis":
    st.title("Statistical analysis")

    st.write("### Missing values")
    
    # A button to view the DataFrame:
    with st.expander("'View DataFrame:"):
        st.write("## DataFrame")
        st.dataframe(df)
        
    # What percentage of NaN values ​​are in the DataFrame:
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    st.dataframe(missing_val_check(df))
    
    # PlayerID nan delete
    with st.expander("Delete playerID column NaN values:"):
            code="""
            son = 9000
            lst = []
            for i in range(40034):
                lst.append(son)
                son+=1
            df['PlayerID']=pd.DataFrame(lst).values
            """
            st.code(code, language='python')
    son = 9000
    lst = []
    for i in range(40034):
        lst.append(son)
        son+=1
    df['PlayerID']=pd.DataFrame(lst).values
    
    # Unnamed column dropping
    with st.expander("'Unnamed: 0' ustunini drop qilindi:"):
        st.code("df = df.drop(columns=['Unnamed: 0'])", language='python')
        df = df.drop(columns=['Unnamed: 0'])
    
    # Age column's fillna
    with st.expander("NaN values in the 'Age' column have been replaced by the median:"):
        df['Age']=df['Age'].fillna(df['Age'].median())
        st.code("df['Age']=df['Age'].fillna(df['Age'].median())", language='python')
    
    # The GameGenre column's fillna
    with st.expander("'Instead of NaN values in the 'GameGenre' column, each region has a separate mod:"):
        GameGenre_mode_for_USA = df[df['Location'] == 'USA']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'USA', 'GameGenre'] = df.loc[df['Location'] == 'USA', 'GameGenre'].fillna(GameGenre_mode_for_USA)
        GameGenre_mode_for_Europe = df[df['Location'] == 'Europe']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Europe', 'GameGenre'] = df.loc[df['Location'] == 'Europe', 'GameGenre'].fillna(GameGenre_mode_for_Europe)
        GameGenre_mode_for_Other = df[df['Location'] == 'Other']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Other', 'GameGenre'] = df.loc[df['Location'] == 'Other', 'GameGenre'].fillna(GameGenre_mode_for_Other)
        GameGenre_mode_for_Asia = df[df['Location'] == 'Asia']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Asia', 'GameGenre'] = df.loc[df['Location'] == 'Asia', 'GameGenre'].fillna(GameGenre_mode_for_Asia)
        df['GameGenre']=df['GameGenre'].fillna(df['GameGenre'].mode()[0])
        code = """
        GameGenre_mode_for_USA = df[df['Location'] == 'USA']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'USA', 'GameGenre'] = df.loc[df['Location'] == 'USA', 'GameGenre'].fillna(GameGenre_mode_for_USA)
        GameGenre_mode_for_Europe = df[df['Location'] == 'Europe']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Europe', 'GameGenre'] = df.loc[df['Location'] == 'Europe', 'GameGenre'].fillna(GameGenre_mode_for_Europe)
        GameGenre_mode_for_Other = df[df['Location'] == 'Other']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Other', 'GameGenre'] = df.loc[df['Location'] == 'Other', 'GameGenre'].fillna(GameGenre_mode_for_Other)
        GameGenre_mode_for_Asia = df[df['Location'] == 'Asia']['GameGenre'].mode()[0]
        df.loc[df['Location'] == 'Asia', 'GameGenre'] = df.loc[df['Location'] == 'Asia', 'GameGenre'].fillna(GameGenre_mode_for_Asia)"""
        st.code(code, language='python')
    
    # Gender column's fillna
    with st.expander("Column mode set to NaN values in column 'Gender':"):
        df['Gender']=df['Gender'].fillna(df['Gender'].mode()[0])
        st.code("df['Gender']=df['Gender'].fillna(df['Gender'].mode()[0])", language='python')
    
    # The rest
    with st.expander("The rest of the columns were also filled:"):
        df['Location']=df['Location'].fillna(df['Location'].mode()[0])
        df['PlayTimeHours']=df['PlayTimeHours'].fillna(df['PlayTimeHours'].median())
        df['InGamePurchases']=df['InGamePurchases'].fillna(df['InGamePurchases'].median())
        df['GameDifficulty']=df['GameDifficulty'].fillna(df['GameDifficulty'].mode()[0])
        df['SessionsPerWeek']=df['SessionsPerWeek'].fillna(df['SessionsPerWeek'].median())
        df['AvgSessionDurationMinutes']=df['AvgSessionDurationMinutes'].fillna(df['AvgSessionDurationMinutes'].median())
        df['PlayerLevel']=df['PlayerLevel'].fillna(df['PlayerLevel'].median())
        df['AchievementsUnlocked']=df['AchievementsUnlocked'].fillna(df['AchievementsUnlocked'].median())
        df['EngagementLevel']=df['EngagementLevel'].fillna(df['EngagementLevel'].mode()[0])
        code = """
        df['Location']=df['Location'].fillna(df['Location'].mode()[0])
        df['PlayTimeHours']=df['PlayTimeHours'].fillna(df['PlayTimeHours'].median())
        df['InGamePurchases']=df['InGamePurchases'].fillna(df['InGamePurchases'].median())
        df['GameDifficulty']=df['GameDifficulty'].fillna(df['GameDifficulty'].mode()[0])
        df['SessionsPerWeek']=df['SessionsPerWeek'].fillna(df['SessionsPerWeek'].median())
        df['AvgSessionDurationMinutes']=df['AvgSessionDurationMinutes'].fillna(df['AvgSessionDurationMinutes'].median())
        df['PlayerLevel']=df['PlayerLevel'].fillna(df['PlayerLevel'].median())
        df['AchievementsUnlocked']=df['AchievementsUnlocked'].fillna(df['AchievementsUnlocked'].median())
        df['EngagementLevel']=df['EngagementLevel'].fillna(df['EngagementLevel'].mode()[0])
        """
        st.code(code, language='python')

    # Number of NaN values ​​(after cleaning)
    st.write("The number of NaN values after cleaning:")
    df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    st.dataframe(missing_val_check(df))

    # Missing DataFrame
    with st.expander("Viewing a cleared 'DataFrame':"):
        st.write("## DataFrame")
        st.dataframe(df)


# Third page:
elif selected=="Graphic analysis":
    df['Location']=df['Location'].fillna(df['Location'].mode()[0])
    df['PlayTimeHours']=df['PlayTimeHours'].fillna(df['PlayTimeHours'].median())
    df['InGamePurchases']=df['InGamePurchases'].fillna(df['InGamePurchases'].median())
    df['GameDifficulty']=df['GameDifficulty'].fillna(df['GameDifficulty'].mode()[0])
    df['SessionsPerWeek']=df['SessionsPerWeek'].fillna(df['SessionsPerWeek'].median())
    df['AvgSessionDurationMinutes']=df['AvgSessionDurationMinutes'].fillna(df['AvgSessionDurationMinutes'].median())
    df['PlayerLevel']=df['PlayerLevel'].fillna(df['PlayerLevel'].median())
    df['AchievementsUnlocked']=df['AchievementsUnlocked'].fillna(df['AchievementsUnlocked'].median())
    df['EngagementLevel']=df['EngagementLevel'].fillna(df['EngagementLevel'].mode()[0])
    df['Gender']=df['Gender'].fillna(df['Gender'].mode()[0])
    df = df.drop(columns=['Unnamed: 0'])
    df['Age']=df['Age'].fillna(df['Age'].median())
    GameGenre_mode_for_USA = df[df['Location'] == 'USA']['GameGenre'].mode()[0]
    df.loc[df['Location'] == 'USA', 'GameGenre'] = df.loc[df['Location'] == 'USA', 'GameGenre'].fillna(GameGenre_mode_for_USA)
    GameGenre_mode_for_Europe = df[df['Location'] == 'Europe']['GameGenre'].mode()[0]
    df.loc[df['Location'] == 'Europe', 'GameGenre'] = df.loc[df['Location'] == 'Europe', 'GameGenre'].fillna(GameGenre_mode_for_Europe)
    GameGenre_mode_for_Other = df[df['Location'] == 'Other']['GameGenre'].mode()[0]
    df.loc[df['Location'] == 'Other', 'GameGenre'] = df.loc[df['Location'] == 'Other', 'GameGenre'].fillna(GameGenre_mode_for_Other)
    GameGenre_mode_for_Asia = df[df['Location'] == 'Asia']['GameGenre'].mode()[0]
    df.loc[df['Location'] == 'Asia', 'GameGenre'] = df.loc[df['Location'] == 'Asia', 'GameGenre'].fillna(GameGenre_mode_for_Asia)
    df['GameGenre']=df['GameGenre'].fillna(df['GameGenre'].mode()[0])
    
    # title
    st.title("Graphic analysis")
    
    # DataFrame
    with st.expander("View DataFrame:"):
        st.write("## DataFrame")
        st.dataframe(df)
        
    # Cuntplot Gender bo'yicha
    with st.expander("Number of players by gender (countplot):"):
        fig, ax = plt.subplots()
        sns.countplot(x="Gender", data=df, palette=sns.color_palette("husl"))
        ax.set_title("Number of players by gender")
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), 
                    textcoords='offset points')
        ax.set_xlabel("Gender", fontsize=14)
        ax.set_ylabel("Count", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        sns.despine()
        st.pyplot(fig)
        
        st.write("In percentages (pie char):")
        fig, ax = plt.subplots()
        gender_counts = df['Gender'].value_counts()
        ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        st.pyplot(fig)
    
    # O'yin vaqti 
    with st.expander("Average playing time of players by gender:"):
        PlayTime_by_Gender = df.groupby('Gender')['PlayTimeHours'].mean()
        total_play_time = PlayTime_by_Gender.sum()
        percent = (PlayTime_by_Gender / total_play_time) * 100
        fig, ax = plt.subplots()
        colors = ['blue' if gender == 'Male' else 'red' for gender in PlayTime_by_Gender.index]
        bars = ax.bar(PlayTime_by_Gender.index, PlayTime_by_Gender.values, color=colors)
        for bar, percentage in zip(bars, percent):
            height = bar.get_height()
            ax.annotate(f'{percentage:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='center')
        ax.set_xlabel('Gender')
        ax.set_ylabel("Game time (hours)")
        ax.set_title("Average playing time by gender")
        sns.despine()
        st.pyplot(fig)



    # O'yinga qiziqish darajasi
    with st.expander("Countplot by level of interest in the game:"):
        fig, ax = plt.subplots()
        sns.countplot(x="EngagementLevel", data=df, palette=sns.color_palette("husl"))
        ax.set_xlabel('The level of interest')
        st.pyplot(fig)
        
        fig, ax = plt.subplots()
        sns.countplot(x="EngagementLevel", data=last_df, palette=sns.color_palette("husl"))
        ax.set_xlabel('The level of interest')
        st.pyplot(fig)
        
        st.write("Total number of gamers by level and gender:")
        fig, ax = plt.subplots()
        sns.countplot(x="EngagementLevel", data=df, palette=sns.color_palette("husl"), hue='Gender')
        ax.set_xlabel('The level of interest')
        st.pyplot(fig)
        
        st.write("By the level of interest in the game (pie char):")
        fig, ax = plt.subplots()
        engagement_counts = df['EngagementLevel'].value_counts()
        ax.pie(engagement_counts, labels=engagement_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') 
        st.pyplot(fig)
        
    # Countplot by Location
    with st.expander("Countplot by location:"):
        fig, ax = plt.subplots()
        sns.countplot(x="Location", data=df, palette=sns.color_palette("husl"))
        st.pyplot(fig)
        
        st.write("By Location and Gender:")
        fig, ax = plt.subplots()
        sns.countplot(x="Location", data=df, palette=sns.color_palette("husl"), hue='Gender')
        st.pyplot(fig)
        
        st.write("By Location (pie char):")
        fig, ax = plt.subplots()
        Location_counts = df['Location'].value_counts()
        ax.pie(Location_counts, labels=Location_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') 
        st.pyplot(fig)

    # Countplot by GameGenre
    with st.expander("Number of players by game genre:"):
        fig, ax = plt.subplots(figsize=(10, 6))
        category_order = ["RPG", "Simulation", "Strategy", "Sports", "Action"]
        sns.countplot(x="GameGenre", data=df, order=category_order, palette=sns.color_palette("husl"), ax=ax)
        ax.set_title("Number of players by game genre:", fontsize=16, fontweight='bold')
        ax.set_xlabel("Game genres", fontsize=14)
        ax.set_ylabel("Count", fontsize=14)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), 
                    textcoords='offset points')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        sns.despine()
        st.pyplot(fig)
        
        st.write("Number of Players by Game Genres and Gender:")
        fig, ax = plt.subplots(figsize=(10, 6))
        category_order = ["RPG", "Simulation", "Strategy", "Sports", "Action"]
        sns.countplot(x="GameGenre", data=df, hue='Gender',order=category_order, palette=sns.color_palette("husl"), ax=ax)
        ax.set_title("Number of Players by Game Genres and Gender", fontsize=16, fontweight='bold')
        ax.set_xlabel("Game genres", fontsize=14)
        ax.set_ylabel("Count", fontsize=14)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), 
                    textcoords='offset points')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        sns.despine()
        st.pyplot(fig)

        st.write("Number of players by game genre and location:")
        fig, ax = plt.subplots(figsize=(10, 6))
        category_order = ["RPG", "Simulation", "Strategy", "Sports", "Action"]
        sns.countplot(x="GameGenre", data=df, hue='Location',order=category_order, palette=sns.color_palette("husl"), ax=ax)
        ax.set_title("Number of players by game genre and location:", fontsize=16, fontweight='bold')
        ax.set_xlabel("Game genres", fontsize=14)
        ax.set_ylabel("Count", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        sns.despine()
        st.pyplot(fig)

    # Bar plot chizish
    with st.expander("Average play time by game genre"):
        plt.figure(figsize=(12, 8))
        sns.barplot(x='GameGenre', y='PlayTimeHours', data=df, estimator=lambda x: sum(x) / len(x))
        plt.title("Average play time by game genre")
        plt.xlabel("Game genre")
        plt.ylabel("Average playing time (in hours)")
        plt.xticks()
        st.pyplot(plt)
        
        st.write("Average play time by game genre and gender:")
        plt.figure(figsize=(12, 8))
        sns.barplot(x='GameGenre', y='PlayTimeHours',hue='Gender',  data=df, estimator=lambda x: sum(x) / len(x))
        plt.title("Average play time by game genre and gender")
        plt.xlabel("Game genre")
        plt.ylabel("Average playing time (in hours)")
        plt.xticks()
        st.pyplot(plt)

    # Histplot binlar tanlash orqali\
    with st.expander("Age distribution of players (histplot):"):
        bin_number = st.select_slider(
            "Select the number of bins:",
            options=list(range(1, 26)),
            value=20
        )
        fig, ax = plt.subplots()
        sns.histplot(df['Age'], bins=bin_number, kde=True, ax=ax)
        st.pyplot(fig)
        
        fig, ax = plt.subplots()
        sns.boxplot(x=df['Age'], ax=ax)
        ax.set_title("Age distribution of players (boxplot)")
        ax.set_xlabel("Age")
        st.pyplot(fig)

    # O'yin qiyinligi bo'yicha o'rtacha sessiya davomiyligi
    with st.expander("Average session length by game difficulty:"):
        fig, ax = plt.subplots()
        sns.boxplot(x='GameDifficulty', y='AvgSessionDurationMinutes', data=df, ax=ax)
        ax.set_xlabel("Game difficulty")
        ax.set_ylabel("Average session duration (in minutes)")
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='GameDifficulty', y='AvgSessionDurationMinutes', data=df, estimator='mean', ax=ax)
        ax.set_xlabel("Game difficulty")
        ax.set_ylabel("Average session duration (in minutes)")
        ax.set_title("Average session length by game difficulty")
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.pointplot(x='GameDifficulty', y='AvgSessionDurationMinutes', data=df, ax=ax)
        ax.set_xlabel("Game difficulty")
        ax.set_ylabel("Average session duration (in minutes)")
        ax.set_title("Average session length by game difficulty")
        st.pyplot(fig)
    
    # Streamlit app title
    with st.expander("Distribution of sessions per week by training level:"):
        fig, ax = plt.subplots(figsize=(12, 6))
        df.boxplot(column='SessionsPerWeek', by='EngagementLevel', grid=False, patch_artist=True, showmeans=True, ax=ax)
        ax.set_title("Weekly sessions based on participation level")
        plt.suptitle('') 
        ax.set_xlabel('Level of participation')
        ax.set_ylabel('Weekly sessions')
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='EngagementLevel', y='SessionsPerWeek', data=df, estimator='mean', ax=ax)
        ax.set_title("Weekly sessions based on participation level")
        ax.set_xlabel('Level of participation')
        ax.set_ylabel('Average weekly sessions')
        st.pyplot(fig)
    
    # Streamlit app title
    with st.expander("Age distribution:"):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df['Age'].dropna(), bins=20, edgecolor='k')
        ax.set_title('Age distribution')
        ax.set_xlabel('Age')
        ax.grid(True)
        st.pyplot(fig)
    
    # Calculate the average play time by game genre
    with st.expander("Average play time by game genre:"):
        avg_play_time = df.groupby('GameGenre')['PlayTimeHours'].mean()
        fig, ax = plt.subplots(figsize=(12, 6))
        avg_play_time.plot(kind='bar', color='skyblue', edgecolor='k', ax=ax)
        ax.set_title("Average play time by game genre")
        ax.set_xlabel("Game genre")
        ax.set_ylabel("Average playing time (in hours)")
        ax.grid(True)
        st.pyplot(fig)
        
    # Plotting
    with st.expander("Distribution of session duration by gender and game genre:"):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.violinplot(x='GameGenre', y='AvgSessionDurationMinutes', hue='Gender', data=df, split=True, ax=ax)
        ax.set_xlabel("Game genre")
        ax.set_ylabel("Session duration (in minutes)")
        st.pyplot(fig)
    
    # Plotting
    with st.expander("The relationship between game level and game difficulty:"):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.stripplot(x='GameDifficulty', y='PlayerLevel', data=df, jitter=True, ax=ax)
        ax.set_xlabel("Game difficulty")
        ax.set_ylabel("Game level")
    
    # Plotting
    with st.expander("Breakdown of winnings by game genre:"):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='GameGenre', y='AchievementsUnlocked', data=df, ax=ax)
        ax.set_xlabel("Game genre")
        ax.set_ylabel("Number of achievements won")
        plt.xticks()
        st.pyplot(fig)
        
    # Pivot table yaratish
    with st.expander("Average game level by game genre and difficulty:"):
        pivot_table = df.pivot_table(values='PlayerLevel', index='GameGenre', columns='GameDifficulty', aggfunc='mean')
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt='.1f')
        plt.title("Average game level by game genre and difficulty")
        plt.xlabel("Game difficulty")
        plt.ylabel("Game genre")
        st.pyplot(plt)

    # heatmap
    with st.expander("Correlation Heatmap:"):
        corr = df.drop(["PlayerID", "Gender", 'Location', 'GameGenre', 'GameDifficulty', 'EngagementLevel'], axis=1).corr()
        plt.figure(figsize=(14, 12))
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlation Heatmap')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        st.pyplot(plt)
        
    with st.expander("Scatter plot:"):
        st.write("Age vs PlayTimeHours")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='Age', y='PlayTimeHours', data=df, ax=ax1, hue='Gender')
        ax1.set_title('Age vs PlayTimeHours')
        ax1.set_xlabel('Age')
        ax1.set_ylabel('PlayTimeHours')
        st.pyplot(fig1)
        
        st.write("PlayerLevel vs AchievementsUnlocked")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='PlayerLevel', y='AchievementsUnlocked', data=df, ax=ax2, hue='EngagementLevel')
        ax2.set_title('PlayerLevel vs AchievementsUnlocked')
        ax2.set_xlabel('PlayerLevel')
        ax2.set_ylabel('AchievementsUnlocked')
        st.pyplot(fig2)

        st.write("PlayTimeHours vs In-Game Purchases")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='PlayTimeHours', y='InGamePurchases', data=df, ax=ax3, hue='GameGenre')
        ax3.set_title("PlayTimeHours vs In-Game Purchases")
        ax3.set_xlabel('PlayTimeHours')
        ax3.set_ylabel("In-game purchases")
        st.pyplot(fig3)


# Fourth page:
elif selected=="Summary":
    st.subheader("General summary of player statistics.")
    st.write("""1. There are more men than women. We can conclude that men participate more in this game. 
    2. Both men and women spend an average of 12 hours playing games.
    3. The number of players with medium interest in the game is twice as many as those with low interest and high interest. In terms of gender, men like the game more.
    4. The largest number of gamers are about 16,000 from America, followed by 12,000 gamers from Europe, so we can guess that these games are popular in these countries.
    5. If we look at the genres of the game, the number of players does not differ much from each other. If we look at gender, there are almost twice as many men in the category of genres.
    6. Game genres do not differ significantly from each other in terms of average playing time. In addition, all game genres are attractive without much difference from each other.
    7. The number of players around the age of 30 is high, which means that people in this age group are more interested and active in games, and we can also know that they like these games. Other age groups are roughly equally distributed. However, there are significant differences between the younger and older age groups.
    8. The higher the game difficulty, the higher the average session duration, we can see that the players are better at challenging games.
    """)