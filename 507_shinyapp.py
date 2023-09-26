# Import necessary libraries
from shiny import App, render, ui
import matplotlib.pyplot as plt
import pandas as pd

 # Load the dataset
def load_data():
    url = "https://raw.githubusercontent.com/bonitr02/datasci_4_web_viz/main/HEALTHYPLACES__Local_Data_for_Better_Health__County_Data_2023_release.csv"
    return pd.read_csv(url)
  
df = load_data()
df_teeth = df[(df['MeasureId'] == 'TEETHLOST') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

# Available states for selection
states = df_teeth['StateDesc'].unique()

app_ui = ui.page_fluid(
    ui.input_select("state", "Select State", {state: state for state in states}),
    ui.output_text_verbatim("avg_data_value"),
    ui.output_plot("bar_chart")
)


def server(input, output, session):

    @output
    @render.text
    def avg_data_value():
        selected_state = input.state()
        avg_value = df_teeth[df_teeth['StateDesc'] == selected_state]['Data_Value'].mean()
        return f"All Teeth Lost in NY, CA and FL by Age-adjusted Prevalence for {selected_state}: {avg_value:.2f}%"

    @output
    @render.plot(alt="All Teeth Lost in NY, CA and FL by Age-adjusted Prevalence Bar Chart")
    def bar_chart():
        overall_avg = df_teeth['Data_Value'].mean()
        selected_state_avg = df_teeth[df_teeth['StateDesc'] == input.state()]['Data_Value'].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(['Selected State', 'Overall Average'], [selected_state_avg, overall_avg], color=['cyan', 'aquamarine'])
        
        ax.set_ylabel('Data Value (Age-adjusted prevalence) - Percent')
        ax.set_ylim(0, 30)
        ax.set_title('All Teeth Lost in NY, CA and FL by Age-adjusted Prevalence')
        
        return fig


app = App(app_ui, server)


