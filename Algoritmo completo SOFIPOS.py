import pandas as pd
import numpy as np
import os
import pickle

# Catalogo de SOFIPOS
dir_sofipos = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_instituciones_27.csv'
df_sofipos = pd.read_csv(dir_sofipos, encoding='latin1')
df_sofipos = df_sofipos[['entidad', 'nombre_entidad']]

# Nomenclatura de los datos
dir_dicc = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_conceptos_27.csv'
df_dicc = pd.read_csv(dir_dicc, encoding='latin1')
df_dicc_s = df_dicc[['idconcepto', 'descripcion', 'nivel']]

# Base global SOFIPOs
dir_df = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\sh_datos_csv_27\sh_datos_27.csv'
df = pd.read_csv(dir_df)

# Se agregan identificadores de variables
df = pd.merge(left=df, right=df_dicc_s, on ='idconcepto', how='left')

# Se agregan nombres de las SOFIPOS
df = pd.merge(left=df, right=df_sofipos, on ='entidad', how='left')

df = df[['nivel',
         'idconcepto',
         'descripcion',
         'entidad',
         'nombre_entidad',
         'periodo',
         'valor'
         ]]

df['periodo'] = pd.to_datetime(df['periodo'].astype(str), format='%Y%m').dt.to_period('M')

# Algoritmo de series de tiempo clave
## Tablas por grupo de variables 
## Activo
### Cartera de crédito
#### Base General
df_cartera = pd.DataFrame(
    columns= ['periodo',
 'Activo',
 'Efectivo y equivalentes de efectivo',
 'Cartera de crédito',
 'Créditos comerciales',
 'Créditos consumo',
 'Créditos vivienda',
 'Activo_i_b100',
 'Activo_pct_YoY',
 'Efectivo y equivalentes de efectivo_i_b100',
 'Efectivo y equivalentes de efectivo_pct_YoY',
 'Cartera de crédito_i_b100',
 'Cartera de crédito_pct_YoY',
 'Créditos comerciales_i_b100',
 'Créditos comerciales_pct_YoY',
 'Créditos consumo_i_b100',
 'Créditos consumo_pct_YoY',
 'Créditos vivienda_i_b100',
 'Créditos vivienda_pct_YoY',
 'Créditos comerciales_w',
 'Créditos consumo_w',
 'Créditos vivienda_w',
 'sofipo',
 'fintech']
    )

#### Set de variables
var_cartera = [
        27100001,
        27100080,
        27100008, # Cartera
        27100009, # C. Comerciales
        27100010, # C. Consumo
        27100011  # C. Vivienda
    ]

### Estimación preventiva para riesgos crediticios
#### Base General
df_riesgo = pd.DataFrame(
    columns= ['periodo',
 'Créditos comerciales',
 'Créditos consumo',
 'Créditos vivienda',
 'Estimaciones preventivas para riesgos crediticios adicional',
 'Estimación preventiva para riesgos crediticios',
 'Créditos comerciales_i_b100',
 'Créditos comerciales_pct_YoY',
 'Créditos consumo_i_b100',
 'Créditos consumo_pct_YoY',
 'Créditos vivienda_i_b100',
 'Créditos vivienda_pct_YoY',
 'Estimaciones preventivas para riesgos crediticios adicional_i_b100',
 'Estimaciones preventivas para riesgos crediticios adicional_pct_YoY',
 'Estimación preventiva para riesgos crediticios_i_b100',
 'Estimación preventiva para riesgos crediticios_pct_YoY',
 'Créditos comerciales_w',
 'Créditos consumo_w',
 'Créditos vivienda_w',
 'Estimaciones preventivas para riesgos crediticios adicional_w',
 'sofipo',
 'fintech']) 

#### Set de variables
var_riesgo = [
    27100012, # Cartera
    27100013, # C. Comerciales
    27100014, # C. Consumo
    27100015,  # C. Vivienda
    27100148
    ]

### Cartera de crédito con riesgo de crédito (E1 + E2)
#### Base General
df_riesgo_E1E2 = pd.DataFrame(columns= ['periodo',
 'Cartera de crédito con riesgo de crédito (E1 + E2)',
 'Créditos comerciales (E1 + E2)',
 'Créditos consumo (E1 + E2)',
 'Créditos vivienda (E1 + E2)',
 'Cartera de crédito con riesgo de crédito (E1 + E2)_i_b100',
 'Cartera de crédito con riesgo de crédito (E1 + E2)_pct_YoY',
 'Créditos comerciales (E1 + E2)_i_b100',
 'Créditos comerciales (E1 + E2)_pct_YoY',
 'Créditos consumo (E1 + E2)_i_b100',
 'Créditos consumo (E1 + E2)_pct_YoY',
 'Créditos vivienda (E1 + E2)_i_b100',
 'Créditos vivienda (E1 + E2)_pct_YoY',
 'Créditos comerciales (E1 + E2)_w',
 'Créditos consumo (E1 + E2)_w',
 'Créditos vivienda (E1 + E2)_w',
 'sofipo',
 'fintech']
 )

#### Set de variables
var_riesgo_E1E2 = [
        27100037, # Cartera
        27100038, # C. Comerciales
        27100039, # C. Consumo
        27100040  # C. Vivienda
    ]

### Cartera de crédito con riesgo de crédito etapa 3
#### Base General
df_riesgo_E3 = pd.DataFrame(columns=['periodo',
 'Cartera de crédito con riesgo de crédito etapa 3',
 'Créditos comerciales',
 'Créditos consumo',
 'Créditos vivienda',
 'Cartera de crédito con riesgo de crédito etapa 3_i_b100',
 'Cartera de crédito con riesgo de crédito etapa 3_pct_YoY',
 'Créditos comerciales_i_b100',
 'Créditos comerciales_pct_YoY',
 'Créditos consumo_i_b100',
 'Créditos consumo_pct_YoY',
 'Créditos vivienda_i_b100',
 'Créditos vivienda_pct_YoY',
 'Créditos comerciales_w',
 'Créditos consumo_w',
 'Créditos vivienda_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_riesgo_E3 = [
        27100004, # Cartera
        27100005, # C. Comerciales
        27100006, # C. Consumo
        27100007  # C. Vivienda
    ]

## Pasivo
### Cartera de crédito
#### Captación tradicional
#### Base General
df_captacion = pd.DataFrame(columns= ['periodo',
 'Pasivo',
 'Captación tradicional',
 'Cuenta global de captación sin movimientos',
 'Depósitos a plazo',
 'Depósitos de exigibilidad inmediata',
 'Títulos de crédito emitidos',
 'Pasivo_i_b100',
 'Pasivo_pct_YoY',
 'Captación tradicional_i_b100',
 'Captación tradicional_pct_YoY',
 'Cuenta global de captación sin movimientos_i_b100',
 'Cuenta global de captación sin movimientos_pct_YoY',
 'Depósitos a plazo_i_b100',
 'Depósitos a plazo_pct_YoY',
 'Depósitos de exigibilidad inmediata_i_b100',
 'Depósitos de exigibilidad inmediata_pct_YoY',
 'Títulos de crédito emitidos_i_b100',
 'Títulos de crédito emitidos_pct_YoY',
 'Cuenta global de captación sin movimientos_w',
 'Depósitos a plazo_w',
 'Depósitos de exigibilidad inmediata_w',
 'Títulos de crédito emitidos_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_captacion = [
        27100053,
        27100044, # Captación tradicional NVL 1
        27100028, # Depósitos de exigibilidad inmediata
        27100029, # Depósitos a plazo
        27100158, # Títulos de crédito emitidos
        27100083  # Cuenta global de captación sin movimientos
    ]

### Cartera de crédito
#### Préstamos bancarios y de otro organismos
df_prestamosb = pd.DataFrame(columns=['periodo',
 'De corto plazo',
 'De largo plazo',
 'Préstamos bancarios y de otros organismos',
 'De corto plazo_i_b100',
 'De corto plazo_pct_YoY',
 'De largo plazo_i_b100',
 'De largo plazo_pct_YoY',
 'Préstamos bancarios y de otros organismos_i_b100',
 'Préstamos bancarios y de otros organismos_pct_YoY',
 'De corto plazo_w',
 'De largo plazo_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_prestamosb = [
        27100030, # Préstamos bancarios y de otros organismos NVL 1
        27100159, # De corto plazo
        27100160, # De largo plazo
    ]

## Cuentas de Capital
### Capital Contable
#### Base General
df_CC = pd.DataFrame(columns=['periodo',
 'Capital contable',
 'Capital contribuido',
 'Capital ganado',
 'Capital contable_i_b100',
 'Capital contable_pct_YoY',
 'Capital contribuido_i_b100',
 'Capital contribuido_pct_YoY',
 'Capital ganado_i_b100',
 'Capital ganado_pct_YoY',
 'Capital contribuido_w',
 'Capital ganado_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_CC = [
        27100002, # Capital contable NVL 1
        27100084, # Capital contribuido
        27100086, # Capital ganado
    ]

### Capital Ganado
#### Base General
df_CG = pd.DataFrame(columns=['periodo',
 'Capital ganado',
 'Incremento por actualización de reservas de capital ',
 'Otros resultados integrales',
 'Reservas de capital',
 'Resultados acumulados',
 'Capital ganado_i_b100',
 'Capital ganado_pct_YoY',
 'Incremento por actualización de reservas de capital _i_b100',
 'Incremento por actualización de reservas de capital _pct_YoY',
 'Otros resultados integrales_i_b100',
 'Otros resultados integrales_pct_YoY',
 'Reservas de capital_i_b100',
 'Reservas de capital_pct_YoY',
 'Resultados acumulados_i_b100',
 'Resultados acumulados_pct_YoY',
 'Incremento por actualización de reservas de capital _w',
 'Otros resultados integrales_w',
 'Reservas de capital_w',
 'Resultados acumulados_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_CG = [
        27100086, # Capital ganado NVL 2
        27100165, # Reservas de capital
        27100166, # Incremento por actualización de reservas de capital 
        27100211, # Resultados acumulados
        27100212  # Otros resultados integrales
    ]

### Resultados acumulados
#### Base General
df_racum = pd.DataFrame(columns=['periodo',
 'Incremento por actualización del resultado de ejercicios anteriores',
 'Resultado Neto',
 'Resultado de ejercicios anteriores',
 'Resultados acumulados',
 'Incremento por actualización del resultado de ejercicios anteriores_i_b100',
 'Incremento por actualización del resultado de ejercicios anteriores_pct_YoY',
 'Resultado Neto_i_b100',
 'Resultado Neto_pct_YoY',
 'Resultado de ejercicios anteriores_i_b100',
 'Resultado de ejercicios anteriores_pct_YoY',
 'Resultados acumulados_i_b100',
 'Resultados acumulados_pct_YoY',
 'Incremento por actualización del resultado de ejercicios anteriores_w',
 'Resultado Neto_w',
 'Resultado de ejercicios anteriores_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_racum = [
        27100211, # Resultados acumulados NVL3
        27100167, # Reservas de capital
        27100168, # Incremento por actualización de reservas de capital 
        27100198, # Resultados acumulados
    ]

## Estado de Resultados Integral
### Resultados del Ejercicio
#### Base General
df_RE = pd.DataFrame(columns=['periodo',
 'Ingresos por intereses',
 'Gastos por intereses',
 'Margen financiero',
 'Margen financiero ajustado por riesgos crediticios',
 'Resultado de la operación',
 'Resultado antes de impuestos a la utilidad',
 'Resultado por operaciones continuas',
 'Resultado neto',
 'Otros resultados integrales',
 'Participación en ORI de otras entidades',
 'RESULTADO INTEGRAL',
 'Ingresos por intereses_i_b100',
 'Ingresos por intereses_pct_YoY',
 'Gastos por intereses_i_b100',
 'Gastos por intereses_pct_YoY',
 'Margen financiero_i_b100',
 'Margen financiero_pct_YoY',
 'Margen financiero ajustado por riesgos crediticios_i_b100',
 'Margen financiero ajustado por riesgos crediticios_pct_YoY',
 'Resultado de la operación_i_b100',
 'Resultado de la operación_pct_YoY',
 'Resultado antes de impuestos a la utilidad_i_b100',
 'Resultado antes de impuestos a la utilidad_pct_YoY',
 'Resultado por operaciones continuas_i_b100',
 'Resultado por operaciones continuas_pct_YoY',
 'Resultado neto_i_b100',
 'Resultado neto_pct_YoY',
 'Otros resultados integrales_i_b100',
 'Otros resultados integrales_pct_YoY',
 'Participación en ORI de otras entidades_i_b100',
 'Participación en ORI de otras entidades_pct_YoY',
 'RESULTADO INTEGRAL_i_b100',
 'RESULTADO INTEGRAL_pct_YoY',
 'Gastos por intereses_w',
 'Margen financiero_w',
 'Margen financiero ajustado por riesgos crediticios_w',
 'Resultado de la operación_w',
 'Resultado antes de impuestos a la utilidad_w',
 'Resultado por operaciones continuas_w',
 'Resultado neto_w',
 'Otros resultados integrales_w',
 'Participación en ORI de otras entidades_w',
 'RESULTADO INTEGRAL_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_RE = [
        27100041, # Ingresos por intereses NVL 1
        27100023, # Gastos por intereses
        27100043, # Margen financiero
        27100017, # Margen financiero ajustado por riesgos crediticios
        27100042, # Resultado de la operación
        27100101, # Resultado antes de impuestos a la utilidad
        27100093, # Resultado por operaciones continuas
        27100003, # Resultado neto
        27100225, # Otros resultados integrales
        27100226, # Participación en ORI de otras entidades
        27100227, # RESULTADO INTEGRAL
    ]

### Ingresos por intereses
#### Base General
df_ingint = pd.DataFrame(columns=['periodo',
 'Ingresos por intereses',
 'Intereses de efectivo y equivalentes de efectivo',
 'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros',
 'Intereses y rendimientos a favor en operaciones de reporto',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3',
 'Ingresos por cartera de crédito valuada a valor razonable',
 'Intereses por derechos de cobro adquiridos',
 'Comisiones por el otorgamiento del crédito',
 'Efecto por renegociación de cartera de crédito',
 'Primas por colocación de deuda',
 'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital',
 'Utilidad por valorización',
 'Incremento por actualización de ingresos por intereses ',
 'Ingresos por intereses_i_b100',
 'Ingresos por intereses_pct_YoY',
 'Intereses de efectivo y equivalentes de efectivo_i_b100',
 'Intereses de efectivo y equivalentes de efectivo_pct_YoY',
 'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros_i_b100',
 'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros_pct_YoY',
 'Intereses y rendimientos a favor en operaciones de reporto_i_b100',
 'Intereses y rendimientos a favor en operaciones de reporto_pct_YoY',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)_i_b100',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)_pct_YoY',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3_i_b100',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3_pct_YoY',
 'Ingresos por cartera de crédito valuada a valor razonable_i_b100',
 'Ingresos por cartera de crédito valuada a valor razonable_pct_YoY',
 'Intereses por derechos de cobro adquiridos_i_b100',
 'Intereses por derechos de cobro adquiridos_pct_YoY',
 'Comisiones por el otorgamiento del crédito_i_b100',
 'Comisiones por el otorgamiento del crédito_pct_YoY',
 'Efecto por renegociación de cartera de crédito_i_b100',
 'Efecto por renegociación de cartera de crédito_pct_YoY',
 'Primas por colocación de deuda_i_b100',
 'Primas por colocación de deuda_pct_YoY',
 'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital_i_b100',
 'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital_pct_YoY',
 'Utilidad por valorización_i_b100',
 'Utilidad por valorización_pct_YoY',
 'Incremento por actualización de ingresos por intereses _i_b100',
 'Incremento por actualización de ingresos por intereses _pct_YoY',
 'Intereses de efectivo y equivalentes de efectivo_w',
 'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros_w',
 'Intereses y rendimientos a favor en operaciones de reporto_w',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)_w',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3_w',
 'Ingresos por cartera de crédito valuada a valor razonable_w',
 'Intereses por derechos de cobro adquiridos_w',
 'Comisiones por el otorgamiento del crédito_w',
 'Efecto por renegociación de cartera de crédito_w',
 'Primas por colocación de deuda_w',
 'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital_w',
 'Utilidad por valorización_w',
 'Incremento por actualización de ingresos por intereses _w',
 'sofipo',
 'fintech'])

#### Set de variables
var_ingint = [
        27100041, # Ingresos por intereses NVL 1
        27100031, # Intereses de efectivo y equivalentes de efectivo
        27100184, # Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros
        27100185, # Intereses y rendimientos a favor en operaciones de reporto
        27100033, # Intereses de cartera de crédito con riesgo de crédito (E1 + E2)
        27100140, # Intereses de cartera de crédito con riesgo de crédito etapa 3
        27100144, # Ingresos por cartera de crédito valuada a valor razonable
        27100213, # Intereses por derechos de cobro adquiridos
        27100186, # Comisiones por el otorgamiento del crédito
        27100214, # Efecto por renegociación de cartera de crédito
        27100215, # Primas por colocación de deuda
        27100216, # Dividendos de instrumentos financieros que califican como instrumentos financieros de capital
        27100187, # Utilidad por valorización
        27100217  # Incremento por actualización de ingresos por intereses 
    ]

### Intereses de cartera de crédito con riesgo de crédito (E1 + E2)
#### Base General
df_intE1E2 = pd.DataFrame(columns=['periodo',
 'Créditos comerciales (E1 + E2)',
 'Créditos consumo (E1 + E2)',
 'Créditos vivienda (E1 + E2)',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)',
 'Créditos comerciales (E1 + E2)_i_b100',
 'Créditos comerciales (E1 + E2)_pct_YoY',
 'Créditos consumo (E1 + E2)_i_b100',
 'Créditos consumo (E1 + E2)_pct_YoY',
 'Créditos vivienda (E1 + E2)_i_b100',
 'Créditos vivienda (E1 + E2)_pct_YoY',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)_i_b100',
 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)_pct_YoY',
 'Créditos comerciales (E1 + E2)_w',
 'Créditos consumo (E1 + E2)_w',
 'Créditos vivienda (E1 + E2)_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_intE1E2 = [
        27100033, # Intereses de cartera de crédito con riesgo de crédito (E1 + E2) NVL 2
        27100034, # Créditos comerciales (E1 + E2)
        27100035, # Créditos consumo (E1 + E2)
        27100036, # Créditos vivienda (E1 + E2)
    ]

### Intereses de cartera de crédito con riesgo de crédito etapa 3
#### Base General
df_intE3 = pd.DataFrame(columns=['periodo',
 'Créditos comerciales',
 'Créditos consumo',
 'Créditos vivienda',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3',
 'Créditos comerciales_i_b100',
 'Créditos comerciales_pct_YoY',
 'Créditos consumo_i_b100',
 'Créditos consumo_pct_YoY',
 'Créditos vivienda_i_b100',
 'Créditos vivienda_pct_YoY',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3_i_b100',
 'Intereses de cartera de crédito con riesgo de crédito etapa 3_pct_YoY',
 'Créditos comerciales_w',
 'Créditos consumo_w',
 'Créditos vivienda_w',
 'sofipo',
 'fintech'])

#### Set de variables
var_intE3 = [
        27100140, # Intereses de cartera de crédito con riesgo de crédito etapa 3 NVL 2
        27100141, # Créditos comerciales 
        27100142, # Créditos consumo
        27100143, # Créditos vivienda
    ]

## Indicadores Financieros
#### Base General
df_ind = pd.DataFrame(columns=['periodo',
 'Capital contable / Activo',
 'EPRC / Cartera de crédito',
 'GAP / Activo',
 'ICOR cartera de crédito',
 'IMOR cartera de crédito',
 'IMOR comercial',
 'IMOR consumo',
 'IMOR vivienda',
 'IMORA cartera de crédito',
 'IMORA comercial',
 'IMORA consumo',
 'IMORA vivienda',
 'Liquidez',
 'MIN',
 'ROA',
 'ROE',
 'Tasa de interés implícita (TII) cartera de crédito E1 + E2',
 'Tasa de interés implícita (TII) pasiva',
 'Capital contable / Activo_pct_YoY',
 'EPRC / Cartera de crédito_pct_YoY',
 'GAP / Activo_pct_YoY',
 'ICOR cartera de crédito_pct_YoY',
 'IMOR cartera de crédito_pct_YoY',
 'IMOR comercial_pct_YoY',
 'IMOR consumo_pct_YoY',
 'IMOR vivienda_pct_YoY',
 'IMORA cartera de crédito_pct_YoY',
 'IMORA comercial_pct_YoY',
 'IMORA consumo_pct_YoY',
 'IMORA vivienda_pct_YoY',
 'Liquidez_pct_YoY',
 'MIN_pct_YoY',
 'ROA_pct_YoY',
 'ROE_pct_YoY',
 'Tasa de interés implícita (TII) cartera de crédito E1 + E2_pct_YoY',
 'Tasa de interés implícita (TII) pasiva_pct_YoY',
 'sofipo',
 'fintech'])

#### Set de variables
var_ind = [
        27200001,	# ROA
        27200002,	# ROE
        27200113,	# Liquidez
        27200004,	# MIN
        27200114,	# GAP / Activo
        27200021,	# Capital contable / Activo
        27200005,	# IMOR cartera de crédito
        27200006,
        27200007,
        27200008,
        27200009,	# IMORA cartera de crédito
        27200010,
        27200011,
        27200012,
        27200013,	# ICOR cartera de crédito
        27200017,	# EPRC / Cartera de crédito
        27200115,	# Tasa de interés implícita (TII) cartera de crédito E1 + E2
        27200119,	#Tasa de interés implícita (TII) pasiva
    ]

## Castigos, quitas y condonaciones
#### Base General
df_castigo = pd.DataFrame(columns=['periodo',
 'Castigos, quitas y condonaciones (Suma 12 meses)',
 'Créditos comerciales',
 'Créditos consumo',
 'Créditos vivienda',
 'Castigos, quitas y condonaciones (Suma 12 meses)_i_b100',
 'Castigos, quitas y condonaciones (Suma 12 meses)_pct_YoY',
 'Créditos comerciales_i_b100',
 'Créditos comerciales_pct_YoY',
 'Créditos consumo_i_b100',
 'Créditos consumo_pct_YoY',
 'Créditos vivienda_i_b100',
 'Créditos vivienda_pct_YoY',
 'Créditos comerciales_w',
 'Créditos consumo_w',
 'Créditos vivienda_w',
 'sofipo',
 'fintech'])
 
#### Set de variables
var_castigo = [
        27200085,	# Castigos, quitas y condonaciones (Suma 12 meses)
        27200086,	# Créditos comerciales
        27200087,	# Créditos consumo
        27200088,	# Créditos vivienda
    ]

## Sofipos a analizar
df_sofipos_nam = pd.DataFrame({
    'nombre' : ['Fincomún',
               'Tamazula',
               'Libertad',
               'Sofiexpress',
               'Crediclub',
               'Total SOFIPOS',
               'Klar',  #
                'Nu México', #
                'Stori', #
                'F Broxel', #
                'Fondeadora'],
    'fintech' : ['NO',
               'NO',
               'NO',
               'NO',
               'NO',
               'NO',
               'SI',  #
                'SI', #
                'SI', #
                'SI', #
                'SI']
    })

# Algoritmo final 
dict_sofipos = {}

for sofipo in df_sofipos_nam['nombre']:
    #sofipo = 'Fincomún'
    df_sofipo = df[df['nombre_entidad'] == sofipo]
    fintech = df_sofipos_nam[df_sofipos_nam['nombre'] == sofipo]['fintech'].iat[0]

    ## ACTIVO: 
    print(f'Se agregará información de Activo de la SOFIPO: {sofipo}')
    ### Cartera de crédito
    df_sofipo_cartera = df_sofipo[df_sofipo['idconcepto'].isin(var_cartera)]
    
    df_sofipo_cartera_pivot = df_sofipo_cartera.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_cartera_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_cartera_pivot[df_sofipo_cartera_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_cartera_pivot[f'{var}_i_b100'] = round((df_sofipo_cartera_pivot[var]/base)*100, 2)
        df_sofipo_cartera_pivot[f'{var}_pct_YoY'] = round(df_sofipo_cartera_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_cartera_pivot.columns.to_list()[3:6]

    for var in vars:

        df_sofipo_cartera_pivot[f'{var}_w'] = round((df_sofipo_cartera_pivot[var]/df_sofipo_cartera_pivot['Cartera de crédito'])*100, 2)

    df_sofipo_cartera_pivot['sofipo'] = sofipo
    df_sofipo_cartera_pivot['fintech'] = fintech

    df_cartera = pd.concat([df_cartera, df_sofipo_cartera_pivot], ignore_index=True)

    print(f'Se agrego la información de Cartera de crédito de la SOFIPO: {sofipo}')

    ### Estimación preventiva para riesgos crediticios
    df_sofipo_riesgo = df_sofipo[df_sofipo['idconcepto'].isin(var_riesgo)]
    
    df_sofipo_riesgo_pivot = df_sofipo_riesgo.pivot(
    index='periodo',
    columns='descripcion',
    values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_riesgo_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_riesgo_pivot[df_sofipo_riesgo_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_riesgo_pivot[f'{var}_i_b100'] = round((df_sofipo_riesgo_pivot[var]/base)*100, 2)
        df_sofipo_riesgo_pivot[f'{var}_pct_YoY'] = round(df_sofipo_riesgo_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_riesgo_pivot.columns.to_list()[1:5]

    for var in vars:

        df_sofipo_riesgo_pivot[f'{var}_w'] = round((df_sofipo_riesgo_pivot[var]/df_sofipo_riesgo_pivot['Estimación preventiva para riesgos crediticios'])*100, 2)

    df_sofipo_riesgo_pivot['sofipo'] = sofipo
    df_sofipo_riesgo_pivot['fintech'] = fintech

    df_riesgo = pd.concat([df_riesgo, df_sofipo_riesgo_pivot], ignore_index=True)

    print(f'Se agrego la información de Estimación preventiva para riesgos crediticios de la SOFIPO: {sofipo}')

    ### Cartera de crédito con riesgo de crédito (E1 + E2)
    df_sofipo_riesgo_E1E2 = df_sofipo[df_sofipo['idconcepto'].isin(var_riesgo_E1E2)]
    
    df_sofipo_riesgo_E1E2_pivot = df_sofipo_riesgo_E1E2.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_riesgo_E1E2_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_riesgo_E1E2_pivot[df_sofipo_riesgo_E1E2_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_riesgo_E1E2_pivot[f'{var}_i_b100'] = round((df_sofipo_riesgo_E1E2_pivot[var]/base)*100, 2)
        df_sofipo_riesgo_E1E2_pivot[f'{var}_pct_YoY'] = round(df_sofipo_riesgo_E1E2_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_riesgo_E1E2_pivot.columns.to_list()[2:5]

    for var in vars:

        df_sofipo_riesgo_E1E2_pivot[f'{var}_w'] = round((df_sofipo_riesgo_E1E2_pivot[var]/df_sofipo_riesgo_E1E2_pivot['Cartera de crédito con riesgo de crédito (E1 + E2)'])*100, 2)

    df_sofipo_riesgo_E1E2_pivot['sofipo'] = sofipo
    df_sofipo_riesgo_E1E2_pivot['fintech'] = fintech

    df_riesgo_E1E2 = pd.concat([df_riesgo_E1E2, df_sofipo_riesgo_E1E2_pivot], ignore_index=True)

    print(f'Se agrego la información de Cartera de crédito con riesgo de crédito (E1 + E2) de la SOFIPO: {sofipo}')

    ### Cartera de crédito con riesgo de crédito etapa 3
    df_sofipo_riesgo_E3 = df_sofipo[df_sofipo['idconcepto'].isin(var_riesgo_E3)]
    
    df_sofipo_riesgo_E3_pivot = df_sofipo_riesgo_E3.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_riesgo_E3_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_riesgo_E3_pivot[df_sofipo_riesgo_E3_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_riesgo_E3_pivot[f'{var}_i_b100'] = round((df_sofipo_riesgo_E3_pivot[var]/base)*100, 2)
        df_sofipo_riesgo_E3_pivot[f'{var}_pct_YoY'] = round(df_sofipo_riesgo_E3_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_riesgo_E3_pivot.columns.to_list()[2:5]

    for var in vars:

        df_sofipo_riesgo_E3_pivot[f'{var}_w'] = round((df_sofipo_riesgo_E3_pivot[var]/df_sofipo_riesgo_E3_pivot['Cartera de crédito con riesgo de crédito etapa 3'])*100, 2)

    df_sofipo_riesgo_E3_pivot['sofipo'] = sofipo
    df_sofipo_riesgo_E3_pivot['fintech'] = fintech

    df_riesgo_E3 = pd.concat([df_riesgo_E3, df_sofipo_riesgo_E3_pivot], ignore_index=True)

    print(f'Se agrego la información de Cartera de crédito con riesgo de crédito etapa 3 de la SOFIPO: {sofipo}')

    ## PASIVO
    print(f'Se agregará información de las cuentas del Pasivo de la SOFIPO: {sofipo}')

    ### Captación Tradicional
    df_sofipo_captacion = df_sofipo[df_sofipo['idconcepto'].isin(var_captacion)]
    
    df_sofipo_captacion_pivot = df_sofipo_captacion.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_captacion_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_captacion_pivot[df_sofipo_captacion_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_captacion_pivot[f'{var}_i_b100'] = round((df_sofipo_captacion_pivot[var]/base)*100, 2)
        df_sofipo_captacion_pivot[f'{var}_pct_YoY'] = round(df_sofipo_captacion_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_captacion_pivot.columns.to_list()[2:7]
    vars =  set(vars) - set(['Pasivo'])

    for var in vars:

        df_sofipo_captacion_pivot[f'{var}_w'] = round((df_sofipo_captacion_pivot[var]/df_sofipo_captacion_pivot['Captación tradicional'])*100, 2)

    df_sofipo_captacion_pivot['sofipo'] = sofipo
    df_sofipo_captacion_pivot['fintech'] = fintech

    df_captacion = pd.concat([df_captacion, df_sofipo_captacion_pivot], ignore_index=True)

    print(f'Se agregó información de Captación Tradicional de la SOFIPO: {sofipo}')

    ### Préstamos bancarios y de otros organismos
    df_sofipo_prestamosb = df_sofipo[df_sofipo['idconcepto'].isin(var_prestamosb)]
    
    df_sofipo_prestamosb_pivot = df_sofipo_prestamosb.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_prestamosb_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_prestamosb_pivot[df_sofipo_prestamosb_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_prestamosb_pivot[f'{var}_i_b100'] = round((df_sofipo_prestamosb_pivot[var]/base)*100, 2)
        df_sofipo_prestamosb_pivot[f'{var}_pct_YoY'] = round(df_sofipo_prestamosb_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_prestamosb_pivot.columns.to_list()[1:3]

    for var in vars:

        df_sofipo_prestamosb_pivot[f'{var}_w'] = round((df_sofipo_prestamosb_pivot[var]/df_sofipo_prestamosb_pivot['Préstamos bancarios y de otros organismos'])*100, 2)

    df_sofipo_prestamosb_pivot['sofipo'] = sofipo
    df_sofipo_prestamosb_pivot['fintech'] = fintech

    df_prestamosb = pd.concat([df_prestamosb, df_sofipo_prestamosb_pivot], ignore_index=True)

    print(f'Se agregó información de Préstamos bancarios y de otros organismos de la SOFIPO: {sofipo}')

    ## Cuentas de Capital
    print(f'Se agregará la información de Cuentas de Capital de la SOFIPO: {sofipo}')

    ### Capital Contable
    df_sofipo_CC = df_sofipo[df_sofipo['idconcepto'].isin(var_CC)]
    
    df_sofipo_CC_pivot = df_sofipo_CC.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_CC_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_CC_pivot[df_sofipo_CC_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_CC_pivot[f'{var}_i_b100'] = round((df_sofipo_CC_pivot[var]/base)*100, 2)
        df_sofipo_CC_pivot[f'{var}_pct_YoY'] = round(df_sofipo_CC_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_CC_pivot.columns.to_list()[2:4]

    for var in vars:

        df_sofipo_CC_pivot[f'{var}_w'] = round((df_sofipo_CC_pivot[var]/df_sofipo_CC_pivot['Capital contable'])*100, 2)

    df_sofipo_CC_pivot['sofipo'] = sofipo
    df_sofipo_CC_pivot['fintech'] = fintech

    df_CC = pd.concat([df_CC, df_sofipo_CC_pivot], ignore_index=True)

    print(f'Se agregó información de Capital Contable de la SOFIPO: {sofipo}')

    ### Capital Ganado
    df_sofipo_CG = df_sofipo[df_sofipo['idconcepto'].isin(var_CG)]
    
    df_sofipo_CG_pivot = df_sofipo_CG.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_CG_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_CG_pivot[df_sofipo_CG_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_CG_pivot[f'{var}_i_b100'] = round((df_sofipo_CG_pivot[var]/base)*100, 2)
        df_sofipo_CG_pivot[f'{var}_pct_YoY'] = round(df_sofipo_CG_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_CG_pivot.columns.to_list()[2:6]

    for var in vars:

        df_sofipo_CG_pivot[f'{var}_w'] = round((df_sofipo_CG_pivot[var]/df_sofipo_CG_pivot['Capital ganado'])*100, 2)

    df_sofipo_CG_pivot['sofipo'] = sofipo
    df_sofipo_CG_pivot['fintech'] = fintech

    df_CG = pd.concat([df_CG, df_sofipo_CG_pivot], ignore_index=True)

    print(f'Se agregó información de Capital Ganado de la SOFIPO: {sofipo}')

    ### Resultados acumulados
    df_sofipo_racum = df_sofipo[df_sofipo['idconcepto'].isin(var_racum)]
    
    df_sofipo_racum_pivot = df_sofipo_racum.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_racum_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_racum_pivot[df_sofipo_racum_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_racum_pivot[f'{var}_i_b100'] = round((df_sofipo_racum_pivot[var]/base)*100, 2)
        df_sofipo_racum_pivot[f'{var}_pct_YoY'] = round(df_sofipo_racum_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_racum_pivot.columns.to_list()[1:4]

    for var in vars:

        df_sofipo_racum_pivot[f'{var}_w'] = round((df_sofipo_racum_pivot[var]/df_sofipo_racum_pivot['Resultados acumulados'])*100, 2)

    df_sofipo_racum_pivot['sofipo'] = sofipo
    df_sofipo_racum_pivot['fintech'] = fintech

    df_racum = pd.concat([df_racum, df_sofipo_racum_pivot], ignore_index=True)

    print(f'Se agregó información de Resultados acumulados de la SOFIPO: {sofipo}')

    ## Estado de Resultados Integral
    print(f'Se agregará la información del Estado de Resultados Integral de la SOFIPO: {sofipo}')

    ### Resultados del Ejercicio
    df_sofipo_RE = df_sofipo[df_sofipo['idconcepto'].isin(var_RE)]
    
    df_sofipo_RE_pivot = df_sofipo_RE.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    df_sofipo_RE_pivot = df_sofipo_RE_pivot[[
        'periodo',
        'Ingresos por intereses',
        'Gastos por intereses',
        'Margen financiero',
        'Margen financiero ajustado por riesgos crediticios',
        'Resultado de la operación',
        'Resultado antes de impuestos a la utilidad',
        'Resultado por operaciones continuas',
        'Resultado neto',
        'Otros resultados integrales',
        'Participación en ORI de otras entidades',
        'RESULTADO INTEGRAL'
        ]]
    
    #### Transformaciones internas
    vars = df_sofipo_RE_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_RE_pivot[df_sofipo_RE_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_RE_pivot[f'{var}_i_b100'] = round((df_sofipo_RE_pivot[var]/base)*100, 2)
        df_sofipo_RE_pivot[f'{var}_pct_YoY'] = round(df_sofipo_RE_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_RE_pivot.columns.to_list()[2:12]

    for var in vars:

        df_sofipo_RE_pivot[f'{var}_w'] = round((df_sofipo_RE_pivot[var]/df_sofipo_RE_pivot['Ingresos por intereses'])*100, 2)

    df_sofipo_RE_pivot['sofipo'] = sofipo
    df_sofipo_RE_pivot['fintech'] = fintech

    df_RE = pd.concat([df_RE, df_sofipo_RE_pivot], ignore_index=True)

    print(f'Se agregó la información de Resultados del Ejercicio de la SOFIPO: {sofipo}')

    ### Ingresos por intereses
    df_sofipo_ingint = df_sofipo[df_sofipo['idconcepto'].isin(var_ingint)]
    
    df_sofipo_ingint_pivot = df_sofipo_ingint.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    df_sofipo_ingint_pivot = df_sofipo_ingint_pivot[[
        'periodo',
        'Ingresos por intereses',
        'Intereses de efectivo y equivalentes de efectivo',
        'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros',
        'Intereses y rendimientos a favor en operaciones de reporto',
        'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)',
        'Intereses de cartera de crédito con riesgo de crédito etapa 3',
        'Ingresos por cartera de crédito valuada a valor razonable',
        'Intereses por derechos de cobro adquiridos',
        'Comisiones por el otorgamiento del crédito',
        'Efecto por renegociación de cartera de crédito',
        'Primas por colocación de deuda',
        'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital',
        'Utilidad por valorización',
        'Incremento por actualización de ingresos por intereses '
    ]]

    #### Transformaciones internas
    vars = df_sofipo_ingint_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_ingint_pivot[df_sofipo_ingint_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_ingint_pivot[f'{var}_i_b100'] = round((df_sofipo_ingint_pivot[var]/base)*100, 2)
        df_sofipo_ingint_pivot[f'{var}_pct_YoY'] = round(df_sofipo_ingint_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_ingint_pivot.columns.to_list()[2:15]

    for var in vars:

        df_sofipo_ingint_pivot[f'{var}_w'] = round((df_sofipo_ingint_pivot[var]/df_sofipo_ingint_pivot['Ingresos por intereses'])*100, 2)

    df_sofipo_ingint_pivot['sofipo'] = sofipo
    df_sofipo_ingint_pivot['fintech'] = fintech

    df_ingint = pd.concat([df_ingint, df_sofipo_ingint_pivot], ignore_index=True)

    print(f'Se agregó la información de Ingresos por intereses de la SOFIPO: {sofipo}')

    ### Intereses de cartera de crédito con riesgo de crédito (E1 + E2)
    df_sofipo_intE1E2 = df_sofipo[df_sofipo['idconcepto'].isin(var_intE1E2)]
    
    df_sofipo_intE1E2_pivot = df_sofipo_intE1E2.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_intE1E2_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_intE1E2_pivot[df_sofipo_intE1E2_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_intE1E2_pivot[f'{var}_i_b100'] = round((df_sofipo_intE1E2_pivot[var]/base)*100, 2)
        df_sofipo_intE1E2_pivot[f'{var}_pct_YoY'] = round(df_sofipo_intE1E2_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_intE1E2_pivot.columns.to_list()[1:4]

    for var in vars:

        df_sofipo_intE1E2_pivot[f'{var}_w'] = round((df_sofipo_intE1E2_pivot[var]/df_sofipo_intE1E2_pivot['Intereses de cartera de crédito con riesgo de crédito (E1 + E2)'])*100, 2)

    df_sofipo_intE1E2_pivot['sofipo'] = sofipo
    df_sofipo_intE1E2_pivot['fintech'] = fintech

    df_intE1E2 = pd.concat([df_intE1E2, df_sofipo_intE1E2_pivot], ignore_index=True)

    print(f'Se agregó la información de Intereses de cartera de crédito con riesgo de crédito (E1 + E2) de la SOFIPO: {sofipo}')

    ### Intereses de cartera de crédito con riesgo de crédito etapa 3
    df_sofipo_intE3 = df_sofipo[df_sofipo['idconcepto'].isin(var_intE3)]
    
    df_sofipo_intE3_pivot = df_sofipo_intE3.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    #### Transformaciones internas
    vars = df_sofipo_intE3_pivot.columns.to_list()[1:]

    #### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_intE3_pivot[df_sofipo_intE3_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_intE3_pivot[f'{var}_i_b100'] = round((df_sofipo_intE3_pivot[var]/base)*100, 2)
        df_sofipo_intE3_pivot[f'{var}_pct_YoY'] = round(df_sofipo_intE3_pivot[var].pct_change(periods=12)*100, 2)

    #### Pesos
    vars = df_sofipo_intE3_pivot.columns.to_list()[1:4]

    for var in vars:

        df_sofipo_intE3_pivot[f'{var}_w'] = round((df_sofipo_intE3_pivot[var]/df_sofipo_intE3_pivot['Intereses de cartera de crédito con riesgo de crédito etapa 3'])*100, 2)

    df_sofipo_intE3_pivot['sofipo'] = sofipo
    df_sofipo_intE3_pivot['fintech'] = fintech

    df_intE3 = pd.concat([df_intE3, df_sofipo_intE3_pivot], ignore_index=True)

    print(f'Se agregó la información de Intereses de cartera de crédito con riesgo de crédito etapa 3 de la SOFIPO: {sofipo}')

    ## Indicadores Financieros
    print(f'Se agregarán los Indicadores Financieros de la SOFIPO: {sofipo}')

    df_sofipo_ind = df_sofipo[df_sofipo['idconcepto'].isin(var_ind)]
    
    df_sofipo_ind_pivot = df_sofipo_ind.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    ### Transformaciones internas
    vars = df_sofipo_ind_pivot.columns.to_list()[1:]

    ### Indicador Base 07-2022 == 100
    for var in vars:

        df_sofipo_ind_pivot[f'{var}_pct_YoY'] = round(df_sofipo_ind_pivot[var].pct_change(periods=12)*100, 2)

    df_sofipo_ind_pivot['sofipo'] = sofipo
    df_sofipo_ind_pivot['fintech'] = fintech

    df_ind = pd.concat([df_ind, df_sofipo_ind_pivot], ignore_index=True)

    print(f'Se agregó los Indicadores Financieros de la SOFIPO: {sofipo}')

    ## Castigos, quitas y condonaciones
    print(f'Se agregará la información de Castigos, quitas y condonaciones de la SOFIPO: {sofipo}')
    df_sofipo_castigo = df_sofipo[df_sofipo['idconcepto'].isin(var_castigo)]
    
    df_sofipo_castigo_pivot = df_sofipo_castigo.pivot(
        index='periodo',
        columns='descripcion',
        values='valor'
    ).reset_index()

    ### Transformaciones internas
    vars = df_sofipo_castigo_pivot.columns.to_list()[1:]

    ### Indicador Base 07-2022 == 100
    for var in vars:

        base = df_sofipo_castigo_pivot[df_sofipo_castigo_pivot['periodo'] == '2023-01'][var].iat[0]
        df_sofipo_castigo_pivot[f'{var}_i_b100'] = round((df_sofipo_castigo_pivot[var]/base)*100, 2)
        df_sofipo_castigo_pivot[f'{var}_pct_YoY'] = round(df_sofipo_castigo_pivot[var].pct_change(periods=12)*100, 2)

    ### Pesos
    vars = df_sofipo_castigo_pivot.columns.to_list()[2:5]

    for var in vars:

        df_sofipo_castigo_pivot[f'{var}_w'] = round((df_sofipo_castigo_pivot[var]/df_sofipo_castigo_pivot['Castigos, quitas y condonaciones (Suma 12 meses)'])*100, 2)

    df_sofipo_castigo_pivot['sofipo'] = sofipo
    df_sofipo_castigo_pivot['fintech'] = fintech

    df_castigo = pd.concat([df_castigo, df_sofipo_castigo_pivot])

    print(f'Se agregó la información de Castigos, quitas y condonaciones de la SOFIPO: {sofipo}')


dict_sofipos = {
    'Inf_cartera' : df_cartera,
    'Inf_cartera_E1E2' : df_riesgo_E1E2,
    'Inf_cartera_E3' : df_riesgo_E3,
    'EPRC' : df_riesgo,
    'Capt_trad' : df_captacion,
    'Prest_bank' : df_prestamosb,
    'CC' : df_CC,
    'CG' : df_CG,
    'Res_acum' : df_racum,
    'Res_ejer' : df_RE,
    'Ing_int' : df_ingint,
    'Ing_int_E1E2' : df_intE1E2,
    'Ing_int_E3' : df_intE3,
    'Ind_financieros' : df_ind,
    'Castigos' : df_castigo
}

########################################################################################################################

df_llaves = pd.DataFrame({
    'llaves' : dict_sofipos.keys(),
    'v_clave' : ['Cartera de crédito',  # Son las variables que se utilizan para ponderar el peso del resto de variables
                 'Cartera de crédito con riesgo de crédito (E1 + E2)',
                 'Cartera de crédito con riesgo de crédito etapa 3',
                 'Estimación preventiva para riesgos crediticios',
                 'Captación tradicional',
                 'Préstamos bancarios y de otros organismos',
                 'Capital contable',
                 'Capital ganado',
                 'Resultados acumulados',
                 'Ingresos por intereses',
                 'Ingresos por intereses',
                 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)',
                 'Intereses de cartera de crédito con riesgo de crédito etapa 3',
                 '',
                 'Castigos, quitas y condonaciones (Suma 12 meses)'
                 ],

    'pesos' : ['SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'SI',
               'NO',
               'SI'
               ]
               })
# Algoritmo para agrupar fintech
llaves = dict_sofipos.keys()

dict_sofipos_fintech = {}

##############################################################################################################

for llave in llaves:
    #llave = 'Extras'
    # Variable clave
    v_clave = df_llaves[df_llaves['llaves'] == llave]['v_clave'].iat[0]
    # Pesos
    peso = df_llaves[df_llaves['llaves'] == llave]['pesos'].iat[0]
    
    df = dict_sofipos[llave]
    df_no = df[df['fintech'] == 'NO']
    df_si = df[df['fintech'] == 'SI'] # Son SOFIPOS FINTECH

    terminaciones = ['_i_b100', '_pct_YoY', '_w']

    columnas = [c for terminacion in terminaciones for c in df_si.columns if c.endswith(terminacion)]
    columnas = columnas + ['sofipo', 'fintech']
    variables = list(set(df_si.columns.to_list()) - set(columnas))

    df_si_s = df_si[variables]

    if peso == 'SI':

        df_si_g = df_si_s.groupby('periodo').agg('sum').reset_index() #No sirve para indicadores
        
        #### Indicador Base 07-2022 == 100
        variables = df_si_g.columns.to_list()
        variables = variables[1:]

        for var in variables:

            df_si_g[var] = pd.to_numeric(df_si_g[var], errors='coerce')

            base = df_si_g[df_si_g['periodo'] == '2023-01'][var].iat[0]
            
            if base == 0: 

                df_si_g[f'{var}_i_b100'] = 0

                try:
                    df_si_g[f'{var}_pct_YoY'] = round(df_si_g[var].pct_change(periods=12)*100, 2)
                    
                except Exception as e:
                    df_si_g[f'{var}_pct_YoY'] = 0

            else:
                
                df_si_g[f'{var}_i_b100'] = round((df_si_g[var]/base)*100, 2)
                df_si_g[f'{var}_pct_YoY'] = round(df_si_g[var].pct_change(periods=12)*100, 2)
        
        variables_s = list(set(variables) -set([v_clave]))
        
        for var in variables_s:

            df_si_g[f'{var}_w'] = round((df_si_g[var]/df_si_g[v_clave])*100, 2)

    elif peso == 'NO':

        df_si_g = df_si_s.groupby('periodo').agg('mean').reset_index()
        variables = df_si_g.columns.to_list()
        variables = variables[1:]

        for var in variables:

            try:
                df_si_g[f'{var}_pct_YoY'] = round(df_si_g[var].pct_change(periods=12)*100, 2)
                
            except Exception as e:
                df_si_g[f'{var}_pct_YoY'] = 0

    df_si_g['sofipo'] = 'Fintech'
    df_si_g['fintech'] = 'SI'

    var_ord = df_no.columns.to_list()
    df_si_g = df_si_g[var_ord]

    df = pd.concat([df_no, df_si_g], ignore_index=True)

    dict_sofipos_fintech[llave] = df
    

dict_sofipos_sector = {
    'original' : dict_sofipos,
    'fintech' : dict_sofipos_fintech
}

with open('dict_sofipos_sector.pkl', 'wb') as f:
    pickle.dump(dict_sofipos_sector, f)