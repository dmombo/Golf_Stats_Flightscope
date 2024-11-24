import pandas as pd
import streamlit as st
import plotly.express as px

# TO RUN THIS, USE TERMINAL
# streamlit run e:\iCloudDrive\Drop\Python_dropbox\Python\2024\Streamlit_Golf_Stats.py
# Turn on 'Always re-run' option on your app (in the web browser), then every time you save code changes, they'll automatically show in the app

# File and folder path
fol = 'C:/Users/dmomb/OneDrive/Documents/Golf/'
fn = 'FS_Golf_DB.xlsx'
df = pd.read_excel(fol+fn)
# Cleaning the column names
df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip().str.replace(' ', '_')
#df.columns = df.columns.str.strip().str.replace('\xa0', ' ', regex=True)    #  Some weird characters in the column names
# Cleaning column names again to remove non-breaking spaces
#df.columns = df.columns.str.replace('\xa0', ' ').str.replace(r'[^\w\s]', '', regex=True).str.strip().str.replace(' ', '_')
df.columns = df.columns.str.replace('\xa0', ' ').str.replace(r'[^\w\s]', '', regex=True).str.strip().str.replace(' ', ' ')

# Function to convert values
# Lateral yards are given as Left or Right of the center line.  We need plus/minus to plot
def convert_lateral(value):
    # Split into numeric and direction
    number, direction = value.split()
    number = float(number)  # Convert to float
    return -number if direction == 'R' else number

# Apply the function to the 'Lateral (yds)' column
df['Lateral yds'] = df['Lateral yds'].apply(convert_lateral)
#-----------------------
# Set the page layout to wide
st.set_page_config(layout="wide")

# sidebar description ------------------------------------------------------------------------------------------
st.sidebar.title("Filter Shots")
st.sidebar.write("Choose Time/Golfer/Club")
def return_filtered_df(df,col,search_term):
        
    if search_term!= "All":
        df = df[df[col] == search_term]
    return df

col = 'Time'
choices = ['All']+df[col].unique().tolist()
search_term =   st.sidebar.selectbox('Select '+ col,choices)
df =  return_filtered_df(df,col,search_term)

col = 'Golfer'
choices = ['All']+df[col].unique().tolist()
search_term =   st.sidebar.selectbox('Select '+ col,choices)
df =  return_filtered_df(df,col,search_term)

col = 'Club'
choices = ['All']+df[col].unique().tolist()
search_term =   st.sidebar.selectbox('Select '+ col,choices)
df =  return_filtered_df(df,col,search_term)

# Dark grey line separator
st.sidebar.markdown("<hr style='border: 1px solid #333333;'>", unsafe_allow_html=True)
# Line break in the sidebar
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Choose what to color on 
choices = ['Time','Golfer','Club']
color_on =   st.sidebar.selectbox('Select ColorOn',choices)

df['Shot Type'] = df['Shot Type'].astype(str)
#----------------------------------------------------------------------------------------------------------------
hov_data = ['Time','Club','Golfer','Shot Type']
###### Golf Analysis and Plots ##########################################################
df['Shot Type'] = df['Shot Type'].astype(str)

##### fig1 #####
fig1 = px.scatter(df, x="Carry yds", y='Lateral yds', color=color_on, title="Golf Cloud",color_discrete_sequence=px.colors.qualitative.Bold,hover_data=hov_data)
# Update x-axis to start at 0.0
fig1.update_xaxes(range=[0, 200])  # Set minimum to 0, maximum is 200  (Use None if you want auto scaling, ie [0, None])
fig1.update_yaxes(range=[-50, 50])  # Set minimum to -50, maximum is 50
fig1.update_layout(
    # Lock the aspect ratio
    yaxis_scaleanchor="x"  # Links the scales of x and y axes
)

##### fig2 #####
fig2 = px.scatter(df, x="Carry yds", y='Height ft', color=color_on, title="Height vs Carry(yds)",color_discrete_sequence=px.colors.qualitative.Bold,hover_data=hov_data)

##### fig3 #####
df['Club mph'] = pd.to_numeric(df['Club mph'], errors='coerce')
df['Ball mph'] = pd.to_numeric(df['Ball mph'], errors='coerce')

fig3 = px.scatter(df, x='Club mph', y='Ball mph', color=color_on, title="Smash Factor by 'Color'",
                  color_discrete_sequence=px.colors.qualitative.Bold,hover_data=hov_data,trendline='ols')

##### fig4 #####
df['AOA'] = pd.to_numeric(df['AOA'], errors='coerce')

fig4 = px.scatter(df, x='AOA', y='Height ft', color=color_on, title="Height of Ball Flight vs Angle of Attack",
                  color_discrete_sequence=px.colors.qualitative.Bold,hover_data=hov_data)

##### fig5 #####
xvar_choice = 'Launch V'
yvar_choice = 'Height ft'
df[xvar_choice] = pd.to_numeric(df[xvar_choice], errors='coerce')

fig5 = px.scatter(df, x=xvar_choice, y=yvar_choice, color=color_on, title="Height vs Launch Angle",
                  color_discrete_sequence=px.colors.qualitative.Bold,hover_data=['Shot Type','Club'])
fig5.update_yaxes(range=[0, None])  # Set minimum to -50, maximum is 50
# Add a box around the plot area
fig5.update_layout(
    xaxis=dict(showline=True, mirror=True, linecolor='black'),
    yaxis=dict(showline=True, mirror=True, linecolor='black')
)


###################################################################################################################

tab1, tab2 = st.tabs(["Tab1", "Tab2"])

with tab1:
    # # sidebar description ------------------------------------------------------------------------------------------

    
    # def return_filtered_df(df,col,search_term):
            
    #     if search_term!= "All":
    #         df = df[df[col] == search_term]
    #     return df
    
    # col = 'Time'
    # choices = ['All']+df[col].unique().tolist()
    # search_term =   st.sidebar.selectbox('Select '+ col,choices)
    # df =  return_filtered_df(df,col,search_term)

    # col = 'Golfer'
    # choices = ['All']+df[col].unique().tolist()
    # search_term =   st.sidebar.selectbox('Select '+ col,choices)
    # df =  return_filtered_df(df,col,search_term)

    # col = 'Club'
    # choices = ['All']+df[col].unique().tolist()
    # search_term =   st.sidebar.selectbox('Select '+ col,choices)
    # df =  return_filtered_df(df,col,search_term)

    # df['Shot Type'] = df['Shot Type'].astype(str)
   
    # --------------------------------------------------------------------------------------------------------------

    # Create a visual template of 2 columns and 2 rows
 
    # Create the first row with two columns
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.write("Title: Col 1, Row 1")  # Placeholder for your visual in Col 1, Row 1
        st.plotly_chart(fig1, use_container_width=False,key="T1C1R1")  # key identifier appears to be necessary if you use the fig4 twice in the same app
    with row1_col2:
        st.write("Title: Col 2, Row 1")  # Placeholder for your visual in Col 2, Row 1
        st.plotly_chart(fig4, use_container_width=True,key="T1C2R1")

    # Create the second row with two columns
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.write("Title: Col 1, Row 2")  # Placeholder for your visual in Col 1, Row 2
        st.plotly_chart(fig5, use_container_width=True,key="T1C1R2")
    with row2_col2:
        st.write("Title: Col 2, Row 2")  # Placeholder for your visual in Col 2, Row 2
        st.plotly_chart(fig3, use_container_width=True,key="T1C2R2")


with tab2:
    # Top large box with title and Plotly chart
    with st.container():
        # Use columns to center the content if desired
        row1 = st.columns([1, 7, 1])  # Middle column wider for alignment

        with row1[1]:  # Center column
            st.markdown("### Col 1, Row 1 - Large Box")  # Large box title
            st.plotly_chart(fig4, use_container_width=True,key="T2C1R1")  # Plotly chart inside the large box

    # Bottom row with three smaller boxes side-by-side
    # Use the [1,1,2] spec to set the relative size of the columns,  ([1,1,1] would be 3 equal columns)
    bottom_row = st.columns([1,1,2])

    # Box 1
    with bottom_row[0]:
        st.write("Bottom Row - Box 1")
        st.metric(label="Sales", value="$1,200", delta="+15%")
    sl_img = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffndomariano.github.io%2Fimages%2F2020-12-23%2Fstreamlit.png&f=1&nofb=1&ipt=00de013865760b41b2bd429b08d5f55eb6965d4d6b801f8728fa8ea94d97938a&ipo=images"
    # Box 2
    with bottom_row[1]:
        st.write("Bottom Row - Box 2")
        st.image(sl_img, caption="Sample Image", use_column_width=True)

    # Box 3
    with bottom_row[2]:
        st.write("Bottom Row - Box 3")
        st.line_chart([1, 2, 3, 4, 5])




