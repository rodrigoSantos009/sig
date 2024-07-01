import geobr 
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def show_top_riskiest_municipalities(state, num_municipalities):
    risk_areas = geobr.read_disaster_risk_area()
    
    risk_areas_state = risk_areas[risk_areas['abbrev_state'] == state]
    
    risk_areas_by_municipality = risk_areas_state.groupby('name_muni').size().reset_index(name='count')

    risk_areas_sorted = risk_areas_by_municipality.sort_values(by='count', ascending=False)

    top_municipalities = risk_areas_sorted.head(num_municipalities)

    plt.figure(figsize=(10, 6))
    plt.barh(top_municipalities['name_muni'], top_municipalities['count'], color='skyblue')
    plt.xlabel('Número de Áreas de Risco')
    plt.title(f'Top {num_municipalities} Municípios em {state} com Mais Áreas de Risco de Desastres Naturais')
    plt.gca().invert_yaxis()
    plt.show()

estados = geobr.read_state()

dropdown_estado = widgets.Dropdown(
    options=estados['abbrev_state'].tolist(),
    description='Selecione o Estado:',
    disabled=False,
)

slider_num_municipalities = widgets.IntSlider(
    value=10,
    min=1,
    max=20,
    step=1,
    description='Municípios:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
)

def on_dropdown_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        state_selected = change['new']
        num_municipalities_selected = slider_num_municipalities.value
        show_top_riskiest_municipalities(state_selected, num_municipalities_selected)

def on_slider_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        state_selected = dropdown_estado.value
        num_municipalities_selected = change['new']
        show_top_riskiest_municipalities(state_selected, num_municipalities_selected)

dropdown_estado.observe(on_dropdown_change)
slider_num_municipalities.observe(on_slider_change)

box_layout = widgets.Layout(display='flex',
                    flex_flow='row',
                    justify_content='space-between',
                    width='50%')

widgets.VBox([dropdown_estado, slider_num_municipalities], layout=box_layout)

