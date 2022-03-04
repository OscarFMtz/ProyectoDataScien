import streamlit as st
import numpy as np
import pandas as pd


#Importar funciones
from func import getTotalDelitos
from func import getEntidadesRojas
from func import getDelitosxYear
from func import getmaxEnt

from func import graficaHorizontal
from func import graficaHorizontal1
from func import graficaPastel

# Obtencion de Datos
df1 = pd.read_csv('./data/IDEFC_1.csv',encoding='latin-1')
df1 = df1.rename({  'INEGI':'Clave_Ent',
                    'ENTIDAD':'Entidad', 'MODALIDAD':'Tipo de delito', 'TIPO':'Modalidad', 'SUBTIPO':'Subtipo de delito',
                    'ENERO':'Enero', 'FEBRERO':'Febrero', 'MARZO':'Marzo', 'ABRIL':'Abril',
                    'MAYO':'Mayo', 'JUNIO':'Junio', 'JULIO':'Julio', 'AGOSTO':'Agosto',
                    'SEPTIEMBRE':'Septiembre', 'OCTUBRE':'Octubre','NOVIEMBRE':'Noviembre','DICIEMBRE':'Diciembre'
                }, axis=1)
df1 = df1[ df1.AÑO <= 2014]

df2 = pd.read_csv('./data/IDEFC_NM.csv',encoding='latin-1')
df2 = df2.drop(['Bien jurídico afectado'],axis=1)
df2 = df2.rename({ 'Año':'AÑO'}, axis=1)
meses = df2.columns.values
meses = meses[6:16]
for i in meses: 
    df2[i] = pd.to_numeric(df2[i], errors='coerce')
df2 = df2.fillna(0)


# Sección de  sidebar
type_delito1 = df1['Tipo de delito'].unique()
type_delito2 = df2['Tipo de delito'].unique()

st.sidebar.title("Menú de parametros para Datasets")
st.sidebar.write("Seleccionar un Tipo de Delito ")

optionbox1 = st.sidebar.selectbox(
                    '¿Cuál te gustaria explorar para el conjunto A)?',
                    type_delito1        
                    )
st.sidebar.write('You selected:', optionbox1)

optionbox2 = st.sidebar.selectbox(
                    '¿Cuál te gustaria explorar para el conjunto B)?',
                    type_delito2
                    )
st.sidebar.write('You selected:', optionbox2)

# Sección de introducción
st.title("Incidencia Delictiva en México")
st.write(
    """
    Bienvenid@ a esta breve exploración sobre las incidencias delictivas en México.

    Los datasets utilizados a continuación son datos sobre los delitos del fuero común.
    
    Y contiene las 32 entidades del país.
    
    Los datasets solo difieren en la metodología de clasificación actualizada en el año 2015.
    """
)

# Sección de datos
st.markdown(
    f"""
    ### Dataset A) 

    #### Contiene los delitos ocurridos entre los años 1997-2014

    #### Cuenta Con {len(df1.axes[0])} filas Y {len(df1.axes[1])} columnas 
    """
)
st.dataframe(df1)
st.markdown(
    f"""
    ### Dataset B)
    
    #### Contiene los delitos ocurridos entre los años 2015 hasta Julio de 2021.    
    
    #### Cuenta con {len(df2.axes[0])} filas Y {len(df2.axes[1])} columnas
    """
)
st.dataframe(df2)

#-------------------
#Tipo de delito AED
df_typeDelito1 = df1.loc[df1['Tipo de delito'].str.contains(optionbox1)]
df_typeDelito2 = df2.loc[df2['Tipo de delito'].str.contains(optionbox2)]

totalD1 = getTotalDelitos(df_typeDelito1)
totalD2 = getTotalDelitos(df_typeDelito2)


col1,col0, col2 = st.columns([2, 1, 2])
col1.subheader( f"Dataset A")
col1.markdown( f"#### Delito:  {optionbox1}") 
col1.markdown( f"### Total:{totalD1}")

col2.subheader( f"Dataset B")
col2.markdown( f"""#### Delito:  {optionbox2}""")
col2.markdown( f"### Total:{totalD2}")

#Dataframe A y Entidades con mas indices de Delitos
dfEntidades1 = getEntidadesRojas(df_typeDelito1)
dfEntidades1 = dfEntidades1.reset_index()
dfEntidades1 = dfEntidades1.rename({ 0:'Total' },axis=1)
dfEntidades1['%Total'] =  dfEntidades1['Total']/totalD1


#Graficar dichas entidades
tit1 = f"Las 8 Entidades con mas {optionbox1}: "
grafPastel1 = graficaPastel(dfEntidades1,tit1)

#Dataframe B y Entidades con mas indices de Delitos
dfEntidades2 = getEntidadesRojas(df_typeDelito2)
dfEntidades2 = dfEntidades2.reset_index()
dfEntidades2 = dfEntidades2.rename({ 0:'Total' },axis=1)
dfEntidades2['%Total'] =  dfEntidades2['Total']/totalD2
#Graficar dichas entidades
tit2 = f"Las 8 Entidades con mas {optionbox2}: "
grafPastel2 = graficaPastel(dfEntidades2,tit2)

with st.container():
    st.markdown(f"#### ¿Cuales son las entidades con mayor indice ?")
    st.write("""
            Por ello se obtienen las entidades con mayor indice delictivo
            y obtenemos su porcentaje con respecto al numero total de delitos comentidos.
    """)

with st.container():
    c1,col0, c2 = st.columns([2, 1, 2])
    c1.altair_chart(grafPastel1)
    c2.altair_chart(grafPastel2,)

#st.dataframe(dfEntidades1)
#st.dataframe(dfEntidades2)


#Total Delitos por Años
dfDxYear1 = getDelitosxYear(df_typeDelito1)
dfDxYear1 = dfDxYear1.reset_index()
dfDxYear1 = dfDxYear1.rename({ 0:'Total' },axis=1)
#Grafica A
tit1 = f"Total de {optionbox1} de cada año"
graf_Year1 = graficaHorizontal(dfDxYear1,tit1)

dfDxYear2 = getDelitosxYear(df_typeDelito2)
dfDxYear2 = dfDxYear2.reset_index()
dfDxYear2 = dfDxYear2.rename({ 0:'Total' },axis=1)
#Grafica B
tit2 = f"Total de {optionbox2} de cada año"
graf_Year2 = graficaHorizontal(dfDxYear2,tit2)



with st.container():
    st.markdown(f"#### ¿Que año tuvo mayor indice delictivo?")
    st.write("""Para saber esto obtenemos el total de delitos ocurrido durante cada año""")

with st.container():
    c1,col0, c2 = st.columns([2, 1, 2])
    c1.altair_chart(graf_Year1)
    c2.altair_chart(graf_Year2)

#st.dataframe(dfDxYear1)
#st.dataframe(dfDxYear2)

#Entidad con el mayor numero de incidencias de cada año
dfmaxEntidad1 = getmaxEnt(df_typeDelito1)
dfmaxEntidad1 = dfmaxEntidad1.reset_index()
dfmaxEntidad1 = dfmaxEntidad1.rename({0: 'Entidad', 1:'Total'}, axis=1)
dfmaxEntidad1['%Total'] = dfmaxEntidad1['Total']/dfDxYear1['Total']
#Graficar MaxEntidad por año
tit1 = f"Entidad con mayor incidencias por año"
graf_MEY1 = graficaHorizontal1(dfmaxEntidad1,tit1)

dfmaxEntidad2 = getmaxEnt(df_typeDelito2)
dfmaxEntidad2 = dfmaxEntidad2.reset_index()
dfmaxEntidad2 = dfmaxEntidad2.rename({0: 'Entidad', 1:'Total'}, axis=1)
dfmaxEntidad2['%Total'] = dfmaxEntidad2['Total']/dfDxYear2['Total']
#Graficar MaxEntidad por año
tit2 = f"Entidad con mayor incidencias por año"
graf_MEY2 = graficaHorizontal1(dfmaxEntidad2,tit2)

with st.container():
    st.markdown(f"#### ¿Que Entidad tuvo mayor indice delictivo por año?")
    st.write("""Para saber esto obtenemos el valor maximo encontrado en la columna año y
    obtenemos su entidad correspondiente ademas agregamos su porcentaje con respecto al total de delitos cometidos en su año.""")
    c1,c0, c2 = st.columns([2, 1, 2])
    c1.altair_chart(graf_MEY1)
    c2.altair_chart(graf_MEY2)
