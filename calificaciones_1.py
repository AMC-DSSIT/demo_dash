# Import required libraries
#import matplotlib as mpl
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# initialize variables
df_raw = pd.DataFrame()
new_df = pd.DataFrame()
tipo = "Empresa Bancaria"
entidad = "Banco Agropecuario"
D01k = "Insatisfactorio"
D03f = "Insatisfactorio"
D06g = "Insatisfactorio"
D06h = "Insatisfactorio"
D06i = "Insatisfactorio"
D06j = "Insatisfactorio"
D06k = "Insatisfactorio"
D06l = "Insatisfactorio"
año = 2020
list_dropdown_año = []
list_dropdown_entidad = []
list_temporal_entidad = []
dict_list_entidad={}

name_data_xlsx = "Data estructurada.xlsx"
name_distribucion_xlsx = "Distribucion_DSSIT.xlsx"

def rename(value):
	lista = value.split()
	del lista[0]
	tipo = " ".join(lista)
	return tipo

#Add row to new_df
def add_row(new_df, entidad, tipo, D01k, D03f, D06g, D06h, D06i, D06j, D06k, D06l, año):
	new_dict={}
	new_dict["Tipo de entidad"]=tipo
	new_dict["01.k"]=D01k
	new_dict["03.f"]=D03f
	new_dict["06.g"]=D06g
	new_dict["06.h"]=D06h
	new_dict["06.i"]=D06i
	new_dict["06.j"]=D06j
	new_dict["06.k"]=D06k
	new_dict["06.l"]=D06l
	new_dict["Año"]=año
	new_df = new_df.append(pd.Series(new_dict, name=entidad), ignore_index=False)
	return new_df

def set_puntaje(value):
	puntaje = 0
	if value == "No se conoce":
		puntaje = 0
	elif value == "Insatisfactorio":
		puntaje = 1
	elif value == "Necesita mejora":
		puntaje = 2
	elif value == "Adecuado":
		puntaje = 3
	elif value == "Cerca mejor práctica":
		puntaje = 4
	return puntaje

# read excel
#df_raw = pd.read_excel('2020.xlsx')
#df_raw = pd.read_excel(r'C:\Documentos-SBS\DSSIT\Capacitaciones\Python\Python Basics for Data Science\Kanban.xlsx', header=None)

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".xlsx") and (file != name_data_xlsx) and (file!=name_distribucion_xlsx):

    	# read excel
    	df_raw = pd.read_excel(file)

    	# get año
    	df_raw = pd.read_excel(file)
    	lista_nombre = file.split(".")
    	año = lista_nombre[0]
    	list_temporal_entidad = []

		# read each row
    	for i, value in enumerate(df_raw["Título"]):
       		if ("->" in value) and ("--" not in value):
       			tipo = rename(value)
       		elif ("-->" in value) and ("---" not in value):
       			entidad = rename(value)
       		elif ("---->  01.k." in value):
       			D01k = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  03.f." in value):
       			D03f = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.g." in value):
       			D06g = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.h." in value):
       			D06h = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.i." in value):
       			D06i = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.j." in value):
       			D06j = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.k." in value):
       			D06k = set_puntaje(df_raw.loc[i,"Calidad"])
       		elif ("---->  06.l." in value):
       			D06l = set_puntaje(df_raw.loc[i,"Calidad"])
       			new_df = add_row(new_df, entidad, tipo, D01k, D03f, D06g, D06h, D06i, D06j, D06k, D06l, año)
       			list_temporal_entidad.append({'label': entidad,'value': entidad})
		
	
		# add lista de entidades a dict de listas por año
    	dict_list_entidad[año] = list_temporal_entidad

    	# show succesfull message
    	#print(file + " leído correctamente")

    	# add año to list_dropdown_año
    	list_dropdown_año.append({'label': año,'value': año})


# remove duplicated elements for list_dropdown_entidad 
#list_temporal_entidad = set(list_temporal_entidad)
#for value in list_temporal_entidad:
#	list_dropdown_entidad.append({'label': value,'value': value})

'''
# create excel writer object
writer = pd.ExcelWriter(name_data_xlsx)

# write dataframe to excel
new_df.to_excel(writer,'Data')

# save the excel
writer.save()

# show succesfull message
print ("Data guardada correctamente como: " + name_data_xlsx)
'''


'''
new_df_dash =  new_df[new_df['Año']=="2020"]
new_df_dash = new_df_dash.loc["Banco Agropecuario","01.k":"06.l"].reset_index()
new_df_dash.columns=["Dominio","Calidad"]
print(new_df_dash)

new_df_dash =  new_df[new_df['Año']=="2021"]
new_df_dash = new_df_dash.loc["Banco Agropecuario","01.k":"06.l"].reset_index()
new_df_dash.columns=["Dominio","Calidad"]
print(new_df_dash)

#print(np.array(new_df.loc["Banco Agropecuario","01.k":"06.l"]).astype('int32'))
'''

# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Dashboard de Calificaciones', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
								html.Div([
									"Año",
									dcc.Dropdown(
							            id='my_dropdown_año',
							            options=list_dropdown_año,
							            value='2020',
							            multi=False,
							            searchable=True,                    #allow user-searching of dropdown values
							            placeholder='Please select...',     #gray, default text shown when no option is selected
							            clearable=True,						#allow user to removes the selected value
							            style={"width": "50%"}
							        ),
									],),
								html.Br(),								
								html.Div([
									"Entidad",
									dcc.Dropdown(
							            id='my_dropdown_entidad',
							            #options=dict_list_entidad["2020"],
							            #value='Banco Agropecuario',
							            multi=False,
							            searchable=True,                    #allow user-searching of dropdown values
							            placeholder='Please select...',     #gray, default text shown when no option is selected
							            clearable=True,						#allow user to removes the selected value
							            style={"width": "50%"}
							        ),
									],),
									#style={'font-size': 30}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-plot')),
                                ])

# add callback decorator: update my_dropdown_entidad
@app.callback( Output(component_id='my_dropdown_entidad', component_property='options'),
			   Input(component_id='my_dropdown_año', component_property='value'))

def update_dropdown(entered_año):
    return dict_list_entidad[entered_año]


# add callback decorator
@app.callback( Output(component_id='bar-plot', component_property='figure'),
			   [
               Input(component_id='my_dropdown_año', component_property='value'),
               Input(component_id='my_dropdown_entidad', component_property='value')
               ])

# Add computation to callback function and return graph
def get_graph(entered_año, entered_entidad):
    # Select data based on the entered year
    #df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute average over arrival delay time.
    #line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    

    #fig = px.bar(x=np.array(["01.k","03.f","06.g","06.h","06.i","06.j","06.k","06.l"]),
    			 #y=np.array(new_df.loc[entered_entidad,"01.k":"06.l"]).astype('int32'), range_y=[0,5],title='Calidad de la entidad por dominio')
	new_df_dash =  new_df[new_df['Año']==entered_año]
	new_df_dash = new_df_dash.loc[entered_entidad,"01.k":"06.l"].reset_index()
	new_df_dash.columns=["Dominio","Calidad"]
	#new_df_dash["Calidad"]=new_df_dash["Calidad"].astype(np.int16)

	fig = px.bar(new_df_dash,
				 x="Dominio",
				 y="Calidad",
				 range_y=[0,4],
				 color = "Calidad",
				 category_orders= {"Dominio":["01.k","03.f","06.g","06.h","06.i","06.j","06.k","06.l"]},
				 #text = np.array(["A","B", "C", "D", "E","F","G","H"]),
				 title='Calidad de '+entered_entidad+' por dominio')
	fig.update_yaxes(fixedrange = True,
					 tickmode="array",
					 tickvals = ["0","1","2","3","4"],
					 ticktext = ["No se conoce","Insatisfactorio","Necesita Mejora","Adecuado","Cerca mejor práctica"])
    # tickformatstops=[{"name": ["01.k","03.f","06.g","06.h","06.i"]}]
    #fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    #fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
	return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False,port=8085,host='0.0.0.0')
	#(debug=True)
