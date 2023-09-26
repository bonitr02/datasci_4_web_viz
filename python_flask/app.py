from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg') # required for local development and g-shell
import matplotlib.pyplot as plt
import io
import base64

import warnings
warnings.simplefilter("ignore", UserWarning)

app = Flask(__name__)

# Load the dataset
url = "https://raw.githubusercontent.com/bonitr02/datasci_4_web_viz_1/main/datasets/HEALTHYPLACES__Local_Data_for_Better_Health__County_Data_2023_release.csv"
df = pd.read_csv(url)
df_teeth = df[(df['MeasureId'] == 'TEETHLOST') & (df['Data_Value_Type'] == 'Age-adjusted prevalence')]

@app.route('/', methods=['GET', 'POST'])
def index():
    states = sorted(df_teeth['StateDesc'].unique())
    selected_state = request.form.get('state') or states[0]
    
    img = create_plot(selected_state)
    
    return render_template("index.html", states=states, selected_state=selected_state, img=img)

def create_plot(state):
    overall_avg = df_teeth['Data_Value'].mean()
    selected_state_avg = df_teeth[df_teeth['StateDesc'] == state]['Data_Value'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(['Selected State', 'Overall Average'], [selected_state_avg, overall_avg], color=['cyan', 'aquamarine'])
    ax.axhline(selected_state_avg, color='gray', linestyle='dashed', alpha=0.7)
    ax.set_ylabel('Data Value (Age-adjusted prevalence) - Percent')
    ax.set_ylim(0, 30)
    ax.set_title('All Teeth Lost in NY, CA and FL by Age-adjusted PrevalenceComparison')
    
    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)
