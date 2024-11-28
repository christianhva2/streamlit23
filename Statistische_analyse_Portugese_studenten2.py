import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium
from scipy.stats import gaussian_kde

df = pd.read_csv('dataset.csv')

# Titel van de applicatie
st.title("Slagingsstatus Portugese studenten op basis van meerdere variabelen")

# Maak een sidebar met tabs
st.sidebar.title("Inhoud")
selected_tab = st.sidebar.radio("Kies een slagingsstatus-variabele", ["Universiteiten", "Geslacht", "Leeftijd", "Aanwezigheid", 
                                                       "Opleiding ouders", "Studieschulden"])

if selected_tab == "Universiteiten":
    st.markdown("Portugal kent een ruim aanbod aan universiteiten welke een uitgebreid spectrum aan leerwegen beschikbaar stellen. Na de verplichte basis- en middelbare school kiest een Portugese jongere \
                voor een opleiding, mogelijk aan één van de universiteiten die in de kaart hieronder zijn weergegeven. Veel verschillende factoren kunnen invloed hebbben op academische resultaten op deze universiteiten, \
                dus uiteindelijk op of het diploma wordt behaald, of dat er bijvoorbeeld studievertraging wordt opgelopen. Op het Polytechnic Institute Of Portalegre is hier onderzoek naar gedaan, waaruit een dataset \
                is gevolgd met variabelen gerelateerd aan de slagingsstatus van studenten, gevisualiseerd in dit dashboard. (Links in de balk kan er genavigeerd worden tussen de variabelen.)")
    st.subheader("Geospatiale inspectie universiteiten Portugal")
    st.markdown("De belangrijkste Portugese universiteiten zijn hieronder weergegeven, met het Polytechnic Institute Of Portalegrede rood gekleurd. De meeste universiteiten in Portugal zijn gelegen aan de meer dichtbevolkte \
                 kustlijn, met hoofdstad Lissabon als koploper beschikkend over vier universiteiten. Zonder specifieke data-ondersteuning begint hier de eerste variabele die invloed heeft op de slagingsstatus van studenten: de afstand tot de universiteit.\
                    Studenten die lang moeten reizen naar de universiteit halen vaak lagere cijfers omdat zij hun tijd minder goed gebruiken en minder aanwezig zijn (Nederlands Dagblad, 2015).")
# Inhoud van Tab 1
    df_coordinates = pd.DataFrame({'Universiteit': ['University of Lisbon', 'Technical University of Lisbon', 'New University of Lisbon', \
                                                        'University of Coimbra', 'Catholic University of Portugal', 'University of the Algarve', \
                                                        'University of Porto', 'Nova School of Business and Economics', 'University of Évora', \
                                                        'University of Beira Interior', 'University of Minho', 'University of Trás-os-Montes and Alto Douro', \
                                                        'University of Aveiro'],
            'LAT': [38.751496994, 38.733611, 38.735330392, 40.207444, 38.7167, 37.0283309, 41.1470368, 38.6833, 38.7, 40.2775366, 41.5608918, 41.30062, 40.6320293],
            'LNG': [-9.155332712,-9.160278 , -9.13666612, -8.459417, -9.1333, -7.924820, -8.615589, -9.3333, -7.7833, -7.5086524, -8.3937346, -7.74413, -8.6597957]})
                    
    m = folium.Map(zoom_start = 6.5, location = [39.399872,-7.8896263])
    for i in df_coordinates.index:
        folium.Marker(location = [df_coordinates['LAT'][i], df_coordinates['LNG'][i]],
        popup = df_coordinates['Universiteit'][i]).add_to(m)
    folium.Marker(location = [39.5185901,-7.649008], popup='Polytechnic Institute Of Portalegre',
    icon=folium.Icon(icon = 'check', color='red')).add_to(m)
        
    st_folium(m)
        
if selected_tab == "Geslacht":
    st.subheader("Diploma behaald of niet? Afhankelijk van je geslacht!")
    st.markdown("De tweede variabele die invloed heeft op de slagingsstatus is het geslacht. Al jarenlang is er een duidelijke trend te zien tussen de studieresultaten van mannen en vrouwen, vrouwen studeren namelijk \
                    sneller af aan de universiteiten dan mannen en vallen minder vaak uit (TU Delft, 2019). Hoe dit van toepassing is op de universiteit in Portugal is hieronder in een staafdiagram weergegeven.") 
    st.write("")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        ##### Staafdiagram
        Er is duidelijk te zien dat ook op de Portugese universiteit het geslacht van de student veel invloed heeft op de slagingsstatus. Bij het aanvinken van de procenten komt naar voren dat \
        bijna  twee keer zoveel vrouwelijke studenten het diploma halen als de mannelijke.""")
        st.markdown("Absoluut gezien vallen bijna evenveel vrouwen als mannen uit, maar ook hier volgen de percentages de trend. Bijna evenveel vrouwen als mannen zijn op dit moment nog ingeschreven aan de universiteit.")
    
    with col2:
        df = pd.read_csv('dataset.csv')
        target_translation = {'Graduate': 'Afgestudeerd', 'Dropout': 'Uitgevallen', 'Enrolled': 'Ingeschreven'}
        df['Target'] = df['Target'].replace(target_translation)
    
        # Target volgorde
        target_order = ['Afgestudeerd', 'Uitgevallen', 'Ingeschreven']
        df['Target'] = pd.Categorical(df['Target'], categories=target_order, ordered=True)
    
        # Checkbox unique for tab1
        Toon_Vrouw_1 = st.checkbox("Toon Vrouwelijke studenten", value=True)
        Toon_Man_1 = st.checkbox("Toon Mannelijke studenten", value=True)
    
        # filtert data op basis van de check boxes
        if Toon_Vrouw_1 and not Toon_Man_1:
            filtered_df = df[df['Gender'] == 0]
        elif Toon_Man_1 and not Toon_Vrouw_1:
            filtered_df = df[df['Gender'] == 1]
        else:
            filtered_df = df  
    
        # Checkbox y-as als percentage
        percentage = st.checkbox("Toon y-as als percentage", value=False)
    
        # Calculate counts or percentages
        count_df = filtered_df.groupby(['Gender', 'Target']).size().reset_index(name='Aantal')
        percentage_df = count_df.copy()
        percentage_df['Percentage'] = percentage_df.groupby('Gender')['Aantal'].transform(lambda x: 100 * x / x.sum())
    
        # Select appropriate y-axis based on checkbox
        if percentage:
            y_column = 'Percentage'
            y_axis_label = 'Percentage'
            df_plot = percentage_df
        else:
            y_column = 'Aantal'
            y_axis_label = 'Aantal'
            df_plot = count_df
    
        # Plotly bar plot
        color_map = {"Afgestudeerd": "blue", "Uitgevallen": "orange", "Ingeschreven": "green"}
        fig = px.bar(
            df_plot,
            x="Gender",
            y=y_column,
            color="Target",
            category_orders={"Target": target_order},
            barmode='group',
            labels={"Gender": "Geslacht", "Target": "Slagingsstatus", y_column: y_axis_label},
            color_discrete_map=color_map
        )
    
        # Update layout
        fig.update_layout(
            title='Slagingsstatus van studenten op basis van geslacht',
            xaxis_title='Geslacht',
            yaxis_title=y_axis_label,
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Vrouw', 'Man']
            )
        )
    
        st.plotly_chart(fig)
  st.markdown("Refresh de pagina als de markers niet goed worden weergegeven")
# Inhoud van Tab 2
elif selected_tab == "Leeftijd":
    st.subheader("Je bent nooit te oud om te leren! Of toch wel?")
 
    st.markdown("""In dit tabblad wordt de invloed van leeftijd op de slagingsstatus van studenten onderzocht. De meeste
    studenten beginnen hun studie voor hun 25e levensjaar, een leeftijd waarop het brein zich aan het ontwikkelen is dus. Naarmate
    we als mens ouder worden, neemt deze ontwikkeling af en nemen onze verantwoordelijkheden toe, wat de studieprestaties beïnvloedt.""")
    st.markdown("Hieronder zijn een lijnplot en een dichtheidsplot weergegeven die het verband tussen leeftijd en academisch succes weergeven.\
                De regressie gerelateerd aan de menselijke leetijd kan gevisualiseerd worden via de checkbox en het dropdown menu.")
    
    # Load the dataset
    df = pd.read_csv('dataset.csv')

    target_translation = {
        'Graduate': 'Afgestudeerd',
        'Dropout': 'Uitgevallen',
        'Enrolled': 'Ingeschreven' }

    df['Target'] = df['Target'].replace(target_translation)
    
    # Colormap
    color_map = {
        'Uitgevallen': 'orange',  
        'Ingeschreven': 'green',  
        'Afgestudeerd': 'blue'  
    }
    # Twee kolommen
    col1, col2 = st.columns([1, 2])
    
    with col1:
        Toon_Vrouw_2 = st.checkbox("Toon Vrouwelijke studenten", value=True)
        Toon_Man_2 = st.checkbox("Toon Mannelijke studenten", value=True)
        regressie = st.checkbox("Toon Regressielijn(en)", value=False)
    
    with col2:
        lijnen = st.multiselect("Selecteer regressielijn(en):",
                                options=['Uitgevallen', 'Ingeschreven', 'Afgestudeerd'],
                                default=['Uitgevallen', 'Ingeschreven', 'Afgestudeerd'])
    
    # Filter data based on checkboxes in tab2
    if Toon_Vrouw_2 and not Toon_Man_2:
        filtered_df = df[df['Gender'] == 0]
    elif Toon_Man_2 and not Toon_Vrouw_2:
        filtered_df = df[df['Gender'] == 1]
    else:
        filtered_df = df
    
    # Leeftijd range slider
    age_range = st.slider("Leeftijd range", 17, 50, (17, 50))
    
    # Filtert data op leeftijd
    filtered_df = filtered_df[(filtered_df['Age at enrollment'] >= age_range[0]) & (filtered_df['Age at enrollment'] <= age_range[1])]
    
    # Berekent % per studie status
    df_age = pd.crosstab(filtered_df['Age at enrollment'], filtered_df['Target'])
    df_age['Totaal'] = df_age['Uitgevallen'] + df_age['Ingeschreven'] + df_age['Afgestudeerd']
    df_age['Uitgevallen'] = df_age['Uitgevallen'] / df_age['Totaal']
    df_age['Ingeschreven'] = df_age['Ingeschreven'] / df_age['Totaal']
    df_age['Afgestudeerd'] = df_age['Afgestudeerd'] / df_age['Totaal']
    
    # df naar long
    df_age = df_age.reset_index()
    df_long = pd.melt(df_age, id_vars=['Age at enrollment'], value_vars=['Uitgevallen', 'Ingeschreven', 'Afgestudeerd'],
                    var_name='Column', value_name='Value')
    
    filtered_df = df_long[df_long['Column'].isin(lijnen)]
    
    
    if regressie:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_df, x='Age at enrollment', y='Value', hue='Column',
            palette=[color_map[status] for status in filtered_df['Column'].unique()])
    
        for status in ['Uitgevallen', 'Ingeschreven', 'Afgestudeerd']:
            subset = filtered_df[filtered_df['Column'] == status]
            sns.regplot(x='Age at enrollment', y='Value', data=subset,
                        scatter=False,
                        line_kws={'linestyle': '--', 'color': color_map[status]},
                        label=f'Regressie {status.replace("%", "")}')
        plt.title('Slagingsstatus van studenten op basis van leeftijd (%)')
        plt.xlabel('Leeftijd')
        plt.ylabel('Percentage')
        plt.xlim(age_range[0], age_range[1])
        plt.legend(title='Slagingsstatus%', loc='upper right')
    
        st.pyplot(plt)
    
    else:
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_df, x='Age at enrollment', y='Value', hue='Column', palette=['orange', 'green', 'blue'])
    
    
        plt.title('Slagingsstatus van studenten op basis van leeftijd (%)')
        plt.xlabel('Leeftijd')
        plt.ylabel('Percentage')
        plt.xlim(age_range[0], age_range[1])
        plt.legend(title='Slagingsstatus%', loc='upper right')
    
        st.pyplot(plt)

    st.markdown("""De lijnen in de lijngrafiek zijn erg onstabiel. Dit wordt veroorzaakt doordat er vanzelfsprekend niet altijd evenveel
    studenten met dezelfde leeftijd op de universiteit zijn (geweest). Om deze reden is er een kde-plot, ookwel dichtheidsplot, toegevoegd. Deze plot is stabieler en laat daarom het verband tussen leeftijd en slaginsstatus beter zien. Zie hieronder:""")
    
    # KDE plot for each category
    fig = px.line()
    
    for categorie in df_long['Column'].unique():
        categorie_data = df_long[df_long['Column'] == categorie]
        kde = gaussian_kde(categorie_data['Age at enrollment'], weights=categorie_data['Value'])
        x_vals = np.linspace(age_range[0], age_range[1], 100)
        y_vals = kde(x_vals)
        fig.add_scatter(x=x_vals, y=y_vals, mode='lines', name=categorie, line=dict(color=color_map[categorie]))
    
    # Update layout
    fig.update_layout(
        title='Slagingsstatus van studenten op basis van leeftijd (kansdichtheid)',
        xaxis_title='Leeftijd',
        yaxis_title='Kansdichtheid',
        legend_title_text='Slagingsstatus%'
    )
    
    
    
    # Display Plotly figure in Streamlit
    st.plotly_chart(fig)
    st.markdown("""In de kde-plot is te zien dat omstreeks de leeftijden 30 tot 35 jaar de kans het grootst is om de studie te beëndigen. Naarmate
    de studenten ouder worden daalt deze kans geleidelijk, maar er zijn natuurlijk weinig studenten in deze leeftijdsklasse. De slagingskans is het groostst
    rond de leeftijd dat de meeste jongeren studeren, en in deze lijn is een duidelijk verval te zien hoe ouder de studenten zijn. Volgens variabele leeftijd \
    geeft een leeftijd tussen 20 en 25 de grootste kans op slagen, en hebben studenten die ouder zijn het erg lastig om hun diploma te halen.""")
    
# Inhoud van Tab 3
elif selected_tab == "Aanwezigheid":
    st.subheader('Een avond- of ochtendmens?')
    st.markdown("""
    De meeste studenten zullen hun universitaire activiteiten overdag uitvoeren, omdat op deze tijden simpelweg de meeste lessen worden gegeven.
    Echter bestaan er ook altijd studenten die dit 's avonds doen, bijvoorbeeld volwassenen die al een baan hebben en overdag geen tijd hebben voor een studie.
    In dit tabblad wordt er naar data gekeken gerelateerd aan of studeren in de avond of overdag invloed heeft op de slagingsstatus van studenten.
    """)
    
    # Twee kolommen
    col1, col2 = st.columns([1, 2])
    
    with col1:
        
        st.markdown("""
        ##### Cirkeldiagram
        De studenten die gebruik maken van de avondschool hebben en gelijke kans om te stoppen met de studie als om af te studeren, namelijk ongeveer 40 procent.
        Voor studenten die overdag studeren is er daarentegen een duidelijk verschil te zien. Iets meer dan de helft van de studenten lukt het om
        af te studeren en 'maar' ongeveer 30 procent stopt met de studie. Hieruit is te concluderen dat studenten die in de avond studeren meer kans
        hebben om het diploma van de bijbehorende studie niet te halen.
        """)
    
    df = pd.read_csv('dataset.csv')
    
    with col2:
        # Dropdown
        aanwezigheid_opties = ['Selecteer een optie', 'Avond', 'Overdag', 'Beiden']
        geselecteerde_aanwezigheid = st.selectbox("Kies het aanwezigheidstype:", aanwezigheid_opties)
    
        # Vertaling Engels naar Nederlands
        doelvertaling = {
            'Graduate': 'Afgestudeerd',
            'Dropout': 'Uitgevallen',
            'Enrolled': 'Ingeschreven'
        }
        df['Target'] = df['Target'].replace(doelvertaling)
    
        # Definieer de volgorde en kleurmapping van de 'Target' categorieën
        doel_volgorde = ['Afgestudeerd', 'Uitgevallen', 'Ingeschreven']
        kleur_map = {
            "Afgestudeerd": "blue",
            "Uitgevallen": "orange",
            "Ingeschreven": "green"
        }
    
        # Zorg ervoor dat de 'Target' kolom als categorisch wordt behandeld met een vaste volgorde
        df['Target'] = pd.Categorical(df['Target'], categories=doel_volgorde, ordered=True)
    
        # Filter de data op basis van het geselecteerde aanwezigheidstype
        if geselecteerde_aanwezigheid == 'Avond':
            gefilterde_df = df[df['Daytime/evening attendance'] == 0]  
        elif geselecteerde_aanwezigheid == 'Overdag':
            gefilterde_df = df[df['Daytime/evening attendance'] == 1]  
        elif geselecteerde_aanwezigheid == 'Beiden':
            gefilterde_df = df
        else:
            gefilterde_df = df  
    
        doel_tellingen = gefilterde_df['Target'].value_counts().reindex(doel_volgorde).fillna(0).reset_index()
        doel_tellingen.columns = ['Target', 'Aantal']  
    
        # Cirkel diagram
        fig = px.pie(
            doel_tellingen,
            names='Target',    
            values='Aantal',  
            title='Slagingsstatus van studenten op basis van aanwezigheid (%)',
            color='Target',    
            color_discrete_map=kleur_map,
            category_orders={'Target': doel_volgorde}  
        )
    
        fig.update_traces(
            rotation=90,        
            direction="clockwise",
            textinfo='percent+label'  
        )
    
        st.plotly_chart(fig)

        target_translation = {
        'Graduate': 'Afgestudeerd',
        'Dropout': 'Uitgevallen',
        'Enrolled': 'Ingeschreven'
    }
    st.markdown("""Voor het creëren van een volledig beeld is hieronder een staafdiagram met aantallen studenten op de Portugese universiteit toegevoegd:
        """)
    df['Target'] = df['Target'].replace(target_translation)

    # Definieer de volgorde van de Target-categorieën
    target_order = ['Afgestudeerd', 'Uitgevallen', 'Ingeschreven']

    # Zorg ervoor dat de Target-kolom als categorisch wordt beschouwd en de volgorde vasthoudt
    df['Target'] = pd.Categorical(df['Target'], categories=target_order, ordered=True)

    # Voeg checkboxes toe voor gender
    show_avond = st.checkbox("Toon Avond", value=True)
    show_middag = st.checkbox("Toon Overdag", value=True)

    # Filter de data op basis van de geselecteerde checkboxes
    if show_avond and not show_middag:
        filtered_df = df[df['Daytime/evening attendance'] == 0]
    elif show_middag and not show_avond:
        filtered_df = df[df['Daytime/evening attendance'] == 1]
    else:
        filtered_df = df  # Toon alles als beide opties geselecteerd zijn of geen selectie is gemaakt

    # Maak de plotly histogram
    # Controleer of de gefilterde dataset niet leeg is
    if not filtered_df.empty:

        # Maak de Plotly countplot
        color_map = {
            "Afgestudeerd": "blue", 
            "Uitgevallen": "orange",
            "Ingeschreven": "green"
        }
        fig = px.histogram(filtered_df, 
                        x="Daytime/evening attendance", 
                        color="Target", 
                        category_orders={"Target": target_order},
                        barmode='group',  # Zet de barmode op 'group' om ze naast elkaar te tonen
                        labels={"Daytime/evening attendance": "Avond/middag aanwezigheid", "Target": "Slagingsstatus", "count": "Aantal"},
                        color_discrete_map=color_map)
            
        # Pas de as-labels aan
        fig.update_layout(
                        title = 'Slagingsstatus van studenten op basis van aanwezigheid (aantallen)',
                        xaxis_title='Avond/overdag aanwezigheid', 
                        yaxis_title='Aantal',
                        xaxis=dict(tickmode='array', 
                                    tickvals=[0, 1], 
                                    ticktext=['Avond', 'Overdag']))

        # Toon de Plotly-figuur in Streamlit
        st.plotly_chart(fig)

    st.markdown("""
        Het verschil in aantallen studenten die overdag of 's avonds hun lessen volgen heeft meestal te maken met het werk dat de studenten doen. Fulltime werken en nog een studie in de avond volgen
        vraagt veel discipline en goede planning, wat kan verklaren dat het percentage dat een diploma haalt lager is dan voor mensen die overdag naar school gaan.
        """)
        
# Inhoud van Tab 4
elif selected_tab == "Opleiding ouders":
    st.subheader("Zo ouder, zo kind") 
    st.markdown("Een andere variabele die de slagingsstatus kan beïnvloeden is het opleidingsniveau van de ouders van de studenten. Volgens het CBS (2017) krijgen kinderen van (hoog)opgeleide ouders vaker een hoger schooladvies en scoren zij beter in het onderwijs. Om dit te onderzoeken \
                op de Portugese universiteit zijn de opleidingen van alle ouders van de studenten gecategoriseerd, met hieronder een toelichting: ")
    st.markdown('**Ongeschoold:** Kan niet/slecht lezen en schrijven  \n**Basis onderwijs**: Heeft de basisschool afgerond  \n**Voortgezet onderwijs**: Heeft de middelbare school afgerond  \n**Studie**: Heeft een opleiding afgerond  \n**Onbekend**: Opleidingsniveau niet bekend')
    st.markdown("Via het dropdown menu boven de grafiek kan het opleidingsniveau van de ouder(s) aangepast worden. Naar wens kan ook slechts één ouder worden weergegeven en er is een mogelijkheid opleidingsniveau's met elkaar te vergelijken door dit vinkje aan te klikken.")
    # Inladen dataset
    df = pd.read_csv('dataset.csv')
    
    # Vertaal de Target-categorieën naar Nederlands
    target_translation = {
        'Graduate': 'Afgestudeerd',
        'Dropout': 'Uitgevallen',
        'Enrolled': 'Ingeschreven' }

    df['Target'] = df['Target'].replace(target_translation)

    # Definieer de volgorde van de Target-categorieën
    target_order = ['Afgestudeerd', 'Uitgevallen', 'Ingeschreven']
    df['Target'] = pd.Categorical(df['Target'], categories=target_order, ordered=True)
        
    # Functie om de opleiding te bepalen
    def opleiding_ouders(x):
        if x in [25, 26]:
            return "Ongeschoold"
        elif x in [9, 18, 20, 21, 27, 28, 11, 13, 15, 16, 17, 22, 29, 31, 32]:
            return "Basis Onderwijs"
        elif x in [1, 7, 8, 10, 12, 14, 19]:
            return 'Voortgezet Onderwijs'
        elif x in [2, 3, 4, 5, 6, 23, 30, 33, 34]:
            return 'Studie'
        else:
            return 'Onbekend'

    # Toepassen van de functie op beide kolommen
    df['Opleiding moeder'] = df["Mother's qualification"].map(opleiding_ouders)
    df['Opleiding vader'] = df["Father's qualification"].map(opleiding_ouders)

    # Maak een lange DataFrame met beide ouders
    df_combined = pd.DataFrame({
        'Ouder': ['Moeder'] * len(df) + ['Vader'] * len(df),
        'Opleiding': list(df['Opleiding moeder']) + list(df['Opleiding vader']),
        'Target': list(df['Target']) * 2  # Neem de 'Target' kolom voor beide ouders
    })

    show_vergelijking = st.checkbox("Vergelijk ouders", value = False)
    if show_vergelijking:
        col1, col2 = st.columns(2)
    else:
        col1 = st.container()

    with col1:
        show_moeder_1 = st.checkbox("Toon Moeder", key="show_moeder_1", value=True)
        show_vader_1 = st.checkbox("Toon Vader", key="show_vader_1", value=True)

        selected_parents_1 = []
        if show_moeder_1:
            selected_parents_1.append("Moeder")
        if show_vader_1:
            selected_parents_1.append("Vader")

        df_filtered_1 = df_combined[df_combined['Ouder'].isin(selected_parents_1)]
        option_selected_1 = st.selectbox("Kies opleidingsniveau:", df_filtered_1['Opleiding'].unique(), key="selectbox1")
        df_filtered_1 = df_filtered_1[df_filtered_1['Opleiding'] == option_selected_1]

        color_map = {
                "Afgestudeerd": "blue", 
                "Uitgevallen": "orange",
                "Ingeschreven": "green"}
            
        fig1 = px.histogram(df_filtered_1, x='Ouder', color='Target', 
                    title='Slagingsstatus naar opleidingsniveau ouders',
                    labels={"Ouder": "Ouder", "Target": "Slagingsstatus"},
                    color_discrete_map=color_map,
                    barmode='stack')
        fig1.update_layout(yaxis_title='Aantal')
        st.plotly_chart(fig1)

    if show_vergelijking:
        with col2:
            show_moeder_2 = st.checkbox("Toon Moeder (vergelijking)", key="show_moeder_2", value=True)
            show_vader_2 = st.checkbox("Toon Vader (vergelijking)", key="show_vader_2", value=True)

            selected_parents_2 = []
            if show_moeder_2:
                selected_parents_2.append("Moeder")
            if show_vader_2:
                selected_parents_2.append("Vader")

            df_filtered_2 = df_combined[df_combined['Ouder'].isin(selected_parents_2)]
            option_selected_2 = st.selectbox("Kies opleidingsniveau (vergelijking):", df_filtered_2['Opleiding'].unique(), key="selectbox2")
            df_filtered_2 = df_filtered_2[df_filtered_2['Opleiding'] == option_selected_2]

            fig2 = px.histogram(df_filtered_2, x='Ouder', color='Target', 
                title='Vergelijking opleidingsniveau ouders',
                labels={"Ouder": "Ouder", "Target": "Slagingsstatus", "count": "Aantal"},
                color_discrete_map=color_map,
                barmode='stack')
            st.plotly_chart(fig2)

    st.markdown("Te zien is dat van de studenten met ouders die alleen de basisschool hebben afgerond er bijna precies evenveel uitvallen, slagen en ingeschreven staan. Op de universiteit zijn relatief veel studenten met een vader die de middelbare school heeft afgerond \
                van wie meer dan 50 procent afstudeert. De moeders van de studenten hebben veelal een studie afgerond. Meer dan 50 procenten van deze studenten haalt hun diploma ook. Opleidingsniveau van de ouders lijkt op de Portugese universiteit niet direct in verband \
                te staan met of je de studie haalt of niet, maar de betere cognitieve ontwikkeling kan zeker meehelpen.")
        
# Inhoud van Tab 5
elif selected_tab == "Studieschulden":
    st.subheader("'Krap bij kas zitten'")
    st.markdown("De wereld draait om geld en in de studentenwereld is dat niet anders. De laatste variabele die invloed heeft op de slaginsstatus van studenten is daarom of de studenten een studieschuld hebben of niet. \
                Hiervoor is gekeken naar de relatie tussen de studieschuldstatus en de cijfers die de studenten halen. Het cijfersysteem in Portugal loopt van 0 tot 20 punten, dit kan weergegeven worden door het boxje onder de plot aan te vinken.\
                Echter, bij minder 10 punten heeft de student het vak niet gehaald en wordt deze score niet meegenoomen in de data (gradecalculator, 2021). Hieruit volgen de boxplots hieronder.")
        
    # Inladen dataset
    df = pd.read_csv('dataset.csv')

    import plotly.graph_objects as go
    # Maakt een checkbox
    gender_option = st.checkbox("Toon Vrouw", value=True)
    gender_option2 = st.checkbox("Toon Man",value=True)
#Als iemand lager dan 10 punten heeft tescoord, heeft deze persoon het vak niet gehaald, er wordt dan meteen een 0 genoteerd, daarom alleen cijfers > 10.
    # Verwijderd alle cijfers onder de tien
    df2 = df[['Curricular units 1st sem (grade)','Curricular units 2nd sem (grade)',  'Debtor', 'Gender']]
    df2 = df2[(df2['Curricular units 1st sem (grade)'] >= 10) & (df2['Curricular units 2nd sem (grade)'] >= 10)]
    df2 = df2.replace({'Debtor':{0: 'Geen studieschulden', 1: 'Wel studieschulden'}})
    
    if gender_option and gender_option2:
        df3 = df2
    elif gender_option:
        df3 = df2[df2['Gender'] == 0]
    elif gender_option2:
        df3 = df2[df2['Gender'] == 1]
    else:
        df3 = df2[df2['Gender'] == 3]
    
    # Maakt boxplot eerste semester
    fig = go.Figure()
    fig.add_trace(go.Box(x=df3['Curricular units 1st sem (grade)'],
                    y=df3['Debtor'],
                    name = 'Cijfer semester één',
                    marker_color='orange'))
    
    #    Maakt boxplot tweede semester
    fig.add_trace(go.Box(x=df3['Curricular units 2nd sem (grade)'],
                    y=df3['Debtor'],
                    name = 'Cijfer semester twee',
                    marker_color='green'))
    # Voegt titel toe
    fig.update_layout(
            title = 'Cijfers van studenten op basis van studieschulden',
            xaxis=dict(title='Cijfers', zeroline=False),
            boxmode='group')
        
    #Laat boxpplot horizontaal zien
    fig.update_traces(orientation='h')

    # Plot de grafiek in Streamlit
    st.plotly_chart(fig)

    image_option = st.checkbox("Toon Portugese cijfersysteem", value=False)
    if image_option:
        st.error("Afbeelding niet gevonden. Controleer het bestandspad!")
        
    st.markdown("De grafiek laat zien dat de studenten met studieschulden met gemiddeld een iets lager cijfer hun vakken halen dan hun medestudenten zonder schulden. Daarnaast zijn er bij de studenten zonder schulden vaker \
                uitschieters te zien richting de perfecte score tijdens een beoordelingsmoment. De variabele studieschuld lijkt dus de slagingsstatus van studenten tamelijk te beïnvloeden.")
