import pandas as pd
import numpy as np
import altair as alt

def getTotalDelitos(df):
    df_TD = df.groupby('Tipo de delito').sum()
    df_TD = df_TD.drop(['AÑO','Clave_Ent'],axis=1)
    df_TD = df_TD.sum(axis=1)
    x = df_TD[0]
    return x


def getEntidadesRojas(df):
    #Entidad con mas casos del delito
    df_entity = df.groupby('Entidad').sum()
    df_entity = df_entity.drop(['AÑO','Clave_Ent'],axis=1)
    df_entity = df_entity.sum(axis=1)
    df_entity = df_entity.sort_values()
    df_entity = df_entity[::-1]
    df_entity = df_entity[:8]# Numero de identidades filtradas

    return df_entity

def getDelitosxYear(df):
    dfyear = df.groupby('AÑO').sum()
    dfyear = dfyear.drop(['Clave_Ent'],axis=1)
    dfyear = dfyear.sum(axis=1)
    return dfyear

def getmaxEnt(df):
    dfME = df.groupby(['AÑO','Entidad']).sum()
    dfME = dfME.drop(['Clave_Ent'],axis=1)
    dfME = dfME.sum(axis=1)
    dfME = dfME.unstack(level=0)
    m = dfME.max()
    idm = dfME.idxmax()
    maxEntidad=pd.concat([idm,m],axis=1)

    return maxEntidad


def graficaPastel(df,string1):
    graf = alt.Chart(df).mark_arc().encode(
    theta=alt.Theta(field="Total", type="quantitative"),
    color=alt.Color(field="Entidad", legend=None),
    tooltip = [alt.Tooltip('Entidad'),alt.Tooltip('Total:Q',format='s'),alt.Tooltip('%Total',format='%')]
    ).properties(
        title = string1,
    ).configure_title(
        fontSize = 16,
        anchor ='start',
    )

    return graf


def graficaHorizontal(df,string):
    graf = alt.Chart(df).mark_bar().encode(
        x = alt.X('Total:Q', title = 'Total de Incidencias', axis = alt.Axis(titleFontSize=15, titleAnchor='end',format = "s",labelAngle=0, labelFontSize=13)),
        y = alt.Y('AÑO:O', title = 'Años', axis = alt.Axis(titleFontSize=15, titleAnchor='start', titleAngle = 0)),
        tooltip = [alt.Tooltip('Total:Q',format='s')]
    ).properties(
        title = string,
    ).configure_title(
        fontSize = 17,
        anchor ='start',
    )
    return graf

def graficaHorizontal1(df,string):
    graf = alt.Chart(df).mark_bar().encode(
        #x='Total:Q',
        x = alt.X('Total:Q', title = 'Total de Incidencias', axis = alt.Axis(titleFontSize=15, titleAnchor='end',format = "s",labelAngle=0, labelFontSize=13)),
        #y="AÑO:O",
        y = alt.Y('AÑO:O', title = 'Años', axis = alt.Axis(titleFontSize=15, titleAnchor='start', titleAngle = 0)),
        tooltip = [alt.Tooltip('Total:Q',format='s'),alt.Tooltip('Entidad'),alt.Tooltip('%Total',format='%')]
    ).properties(
        title = string,
    ).configure_title(
        fontSize = 17,
        anchor ='start',
    )
    return graf



