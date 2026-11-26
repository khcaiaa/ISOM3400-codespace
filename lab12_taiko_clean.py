import streamlit as st
import pandas as pd

st.set_page_config('Taiko No Tatsujin Data', '🥁', layout='wide')
st.title('Taiko no Tatsujin!')

######## Loading the csv data file ########
# Read from csv file and cache data (so the file doesn't need to be re-read every time the page reloads)
@st.cache_data
def read_data_file(filepath):
    return(pd.read_csv(filepath))
########

# We call the read_data_file function here and store the data in the variable df
df = read_data_file("taiko_song_data.csv")

# Some data we can use for the charts...
difficulty_colors = ['#FF2703', '#8CB852', '#435935', '#DB1885', '#7135DB']
category_list = df.groupby('Category').groups.keys()
difficulty_list = ['Easy', 'Normal', 'Hard', 'Extreme', 'Extra Extreme']

# These are placeholder values so the program doesn't crash when you try to run it before it's complete

chosen_category = None
#####

# Let's set up the page as two columns! This time, we will use the dot notation.
# (You can use the with notation from last lab for columns as well.)
col1, col2= st.columns(2)
# col1 will refer to the left column. col2 will refer to the right column.

############################################################################
# TASK 1. Let's display the full dataframe at the top of col1!

col1.dataframe(df,height=400)

#with col1:
#   st.dataframe(df)


############################################################################
# TASK 2. Let's display a bar chart at the top of col2!
#   We would like to see the number of songs per music category.
#   Let's display the bar chart horizontally.

col2.write("Number of songs per category")
col2.bar_chart(df['Category'].value_counts(),horizontal=True,height=356)


############################################################################
# TASK 3. Let's display a bar chart in col1 to see the rating distribution for each difficulty level!

# TASK 3.1:
#   We should add a way for users to choose which difficulty they would like to view.
#   We can try to use the pills widget to let users choose.
#   The pills will return the single chosen option (default).
#   You can get the names of the difficulty levels from the list difficulty_list.

chosen_difficulty = col1.pills("View difficuty distribution for levels:",difficulty_list,default="Easy")

# -----------------------------------

# Task 3.2: Display the rating distribution of the chosen difficulty in the form of a bar chart, i.e. how many songs are of lv 1, how many songs are of lv 2...
#   How to get the data we need? (Hint: Series objects' .value_counts() method can return the frequency of distinct values it contains.)

col1.subheader("Rating distributions of all songs")
if not chosen_difficulty:
    st.error("please choose a difficulty")
else:
    col1.bar_chart(df[chosen_difficulty].value_counts(),x_label=chosen_difficulty+'Rating',\
                y_label='number of songs',\
                color=difficulty_colors[difficulty_list.index(chosen_difficulty)])

    ############################################################################
    # Code for rating distribution according to categories (given)
    # You may need to comment out this block of code to run the program successfully if you haven't completed the previous tasks.

    # The selection mode of this pills set is 'multi'! It will return a *list* of the chosen options instead.
    chosen_category = col2.pills('View difficulty distribution for categories:', category_list, selection_mode = 'multi', default=category_list)
    stacks=col2.checkbox("Stacks bars?",value=True)
    col2.subheader("Rating distribution according to categories")

    # If no category is chosen, no data will be shown.
    # We can display a warning message to ask the user to choose at least one category.
    if not chosen_category:
        col2.warning("Please choose at least one category.")
    else:
        # Grouping by Category, then counting according to difficulty rating.
        difficulty_df = pd.DataFrame(df.groupby(['Category', chosen_difficulty]).count().reset_index())

        # Further filtering: only include selected categories from the chosen_category pills widget
        difficulty_df = difficulty_df.query("Category in @chosen_category")
        
        # Display the bar chart:
        col2.bar_chart(difficulty_df,\
                    x=chosen_difficulty, y='Song Title',\
                    x_label = chosen_difficulty + ' rating', y_label='No. of Songs',\
                    color='Category',stack=stacks)



        # TASK 4.
        #   Notice that if we group or dataframe by categories, we can display the data in a stacked bar.
        #   Each color represents a specific category.
        #   Is it possible for us to display these stacked bar side-by-side instead? (yes)
        #   Is it possible for the user to choose whether they want to show it stacked or side-by-side? (yes)

        #   Let's add a checkbox and modify the bar chart in col2!
        

    ############################################################################
    # TASK 5.
    #   It is possible for the user to deselect all options in the pills widget.
    #   If the user does not choose a difficulty, then the two bar charts cannot be displayed. (There will be an error)
    #   Surround the two displayed tables with an if/else to handle this!
    #   Show an error message with st.error() if no difficulty is chosen.






#############################################################################################################
# If you would like to take a look at what's inside the pill variables, you can check in the expander...
with st.expander("Variables"):
    st.markdown(f"value returned by `chosen_difficulty`: {chosen_difficulty} ({type(chosen_difficulty)})")
    st.markdown(f"value returned by `chosen_category`: {chosen_category} ({type(chosen_category)})")