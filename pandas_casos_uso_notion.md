# Combinaciones de Funciones Pandas para Casos de Uso Reales

## 🎯 CASOS DE USO NIVEL PRINCIPIANTE

### 1. **Reporte Básico de Ventas** 
*"¿Cuáles productos se venden más?"*

```python
# Combinación de funciones: explorar → agrupar → agregar → ordenar
df.info()  # Entender los datos primero
ventas_mensuales = (df.groupby('producto')['ventas']
                   .sum()
                   .sort_values(ascending=False)
                   .head(10))

# Alternativa con más detalle
resumen_ventas = (df.groupby('producto')
                 .agg({'ventas': ['sum', 'count', 'mean']})
                 .round(2)
                 .sort_values(('ventas', 'sum'), ascending=False))
```

### 2. **Análisis de Clientes**
*"¿Quiénes son mis mejores clientes?"*

```python
# Combinación: agrupar → agregar → clasificar → filtrar
valor_cliente = (df.groupby('id_cliente')
                .agg({
                    'monto_pedido': ['sum', 'count', 'mean'],
                    'fecha_pedido': ['min', 'max']
                })
                .round(2))

# Agregar segmentos de clientes
valor_cliente['gasto_total'] = valor_cliente[('monto_pedido', 'sum')]
valor_cliente['segmento'] = pd.cut(valor_cliente['gasto_total'], 
                                  bins=3, 
                                  labels=['Bajo', 'Medio', 'Alto'])
```

### 3. **Verificación de Calidad de Datos**
*"¿Están mis datos lo suficientemente limpios para analizar?"*

```python
# Combinación: info → isnull → duplicated → describe
def reporte_calidad_datos(df):
    print("=== REPORTE DE CALIDAD DE DATOS ===")
    print(f"Dimensiones del dataset: {df.shape}")
    print(f"\nValores faltantes:\n{df.isnull().sum()}")
    print(f"\nFilas duplicadas: {df.duplicated().sum()}")
    print(f"\nTipos de datos:\n{df.dtypes}")
    
    # Verificar problemas obvios en los datos
    columnas_numericas = df.select_dtypes(include=['number']).columns
    for col in columnas_numericas:
        if (df[col] < 0).any():
            print(f"Advertencia: {col} tiene valores negativos")
```

## 🔍 CASOS DE USO NIVEL INTERMEDIO

### 4. **Análisis de Series Temporales**
*"¿Cómo evolucionan las ventas en el tiempo?"*

```python
# Combinación: to_datetime → set_index → resample → rolling
df['fecha'] = pd.to_datetime(df['fecha'])
df_tiempo = df.set_index('fecha').sort_index()

# Tendencias mensuales con promedios móviles
tendencias_mensuales = (df_tiempo.resample('M')['ventas']
                       .sum()
                       .to_frame()
                       .assign(
                           promedio_movil_3m=lambda x: x['ventas'].rolling(3).mean(),
                           promedio_movil_6m=lambda x: x['ventas'].rolling(6).mean(),
                           cambio_porcentual=lambda x: x['ventas'].pct_change()
                       ))

# Análisis estacional
df_tiempo['mes'] = df_tiempo.index.month
patron_estacional = (df_tiempo.groupby('mes')['ventas']
                    .agg(['mean', 'std'])
                    .round(2))
```

### 5. **Análisis de Cohortes**
*"¿Cómo se comportan las cohortes de clientes en el tiempo?"*

```python
# Combinación: to_datetime → groupby → transform → pivot → fillna
df['fecha_pedido'] = pd.to_datetime(df['fecha_pedido'])
df['mes_pedido'] = df['fecha_pedido'].dt.to_period('M')

# Crear cohortes basadas en primera compra
df['mes_cohorte'] = (df.groupby('id_cliente')['fecha_pedido']
                    .transform('min')
                    .dt.to_period('M'))

# Calcular períodos desde primera compra
df['numero_periodo'] = (df['mes_pedido'] - df['mes_cohorte']).apply(attrgetter('n'))

# Crear tabla de cohorte
datos_cohorte = (df.groupby(['mes_cohorte', 'numero_periodo'])['id_cliente']
                .nunique()
                .reset_index())

tabla_cohorte = datos_cohorte.pivot(index='mes_cohorte', 
                                   columns='numero_periodo', 
                                   values='id_cliente').fillna(0)
```

### 6. **Análisis ABC (Análisis de Pareto)**
*"¿Qué productos contribuyen más a los ingresos?"*

```python
# Combinación: groupby → agg → sort → cumsum → cut
analisis_productos = (df.groupby('producto')
                     .agg({'ingresos': 'sum', 'cantidad': 'sum'})
                     .sort_values('ingresos', ascending=False)
                     .reset_index())

# Calcular porcentajes acumulados
ingresos_totales = analisis_productos['ingresos'].sum()
analisis_productos['pct_ingresos'] = analisis_productos['ingresos'] / ingresos_totales
analisis_productos['pct_acumulado'] = analisis_productos['pct_ingresos'].cumsum()

# Clasificar en categorías ABC
analisis_productos['categoria_abc'] = pd.cut(
    analisis_productos['pct_acumulado'],
    bins=[0, 0.8, 0.95, 1.0],
    labels=['A', 'B', 'C']
)
```

## 🚀 CASOS DE USO NIVEL AVANZADO

### 7. **Análisis RFM (Recencia, Frecuencia, Monetario)**
*"¿Cómo segmentar clientes basado en comportamiento?"*

```python
# Combinación: groupby → agg → rank → cut → assign
fecha_actual = df['fecha_pedido'].max()

rfm = (df.groupby('id_cliente')
       .agg({
           'fecha_pedido': lambda x: (fecha_actual - x.max()).days,  # Recencia
           'id_pedido': 'count',  # Frecuencia
           'monto_total': 'sum'  # Monetario
       })
       .rename(columns={
           'fecha_pedido': 'recencia',
           'id_pedido': 'frecuencia', 
           'monto_total': 'monetario'
       }))

# Crear puntajes RFM (escala 1-5)
rfm['puntaje_r'] = pd.cut(rfm['recencia'], bins=5, labels=[5,4,3,2,1])
rfm['puntaje_f'] = pd.cut(rfm['frecuencia'].rank(method='first'), bins=5, labels=[1,2,3,4,5])
rfm['puntaje_m'] = pd.cut(rfm['monetario'].rank(method='first'), bins=5, labels=[1,2,3,4,5])

# Puntaje RFM combinado
rfm['puntaje_rfm'] = (rfm['puntaje_r'].astype(str) + 
                     rfm['puntaje_f'].astype(str) + 
                     rfm['puntaje_m'].astype(str))

# Segmentar clientes
def segmento_rfm(fila):
    if fila['puntaje_rfm'] in ['555', '554', '544', '545', '454', '455', '445']:
        return 'Campeones'
    elif fila['puntaje_rfm'] in ['543', '444', '435', '355', '354', '345', '344', '335']:
        return 'Clientes Leales'
    # ... más segmentos
    else:
        return 'Otros'

rfm['segmento'] = rfm.apply(segmento_rfm, axis=1)
```

### 8. **Análisis de Cadena de Suministro (SPLY)**
*"Optimizar inventario y detectar problemas de suministro"*

```python
# Combinación: merge → rolling → shift → apply → query
datos_inventario = pd.read_csv('inventario.csv')
datos_ventas = pd.read_csv('ventas.csv')
datos_proveedores = pd.read_csv('proveedores.csv')

# Combinar datasets
analisis_suministro = (datos_ventas
                      .merge(datos_inventario, on=['id_producto', 'fecha'], how='left')
                      .merge(datos_proveedores, on='id_proveedor', how='left')
                      .sort_values(['id_producto', 'fecha']))

# Calcular métricas de cadena de suministro
metricas_suministro = (analisis_suministro
                      .groupby('id_producto')
                      .apply(lambda grupo: pd.Series({
                          'tiempo_entrega_promedio': grupo['tiempo_entrega'].mean(),
                          'tasa_desabasto': (grupo['nivel_stock'] == 0).mean(),
                          'nivel_servicio': (grupo['demanda'] <= grupo['nivel_stock']).mean(),
                          'rotacion_inventario': grupo['ventas'].sum() / grupo['nivel_stock'].mean(),
                          'stock_seguridad_necesario': grupo['demanda'].std() * np.sqrt(grupo['tiempo_entrega'].mean())
                      }))
                      .reset_index())

# Identificar riesgos en cadena de suministro
productos_riesgo = (metricas_suministro
                   .query('tasa_desabasto > 0.1 or nivel_servicio < 0.95')
                   .sort_values('tasa_desabasto', ascending=False))
```

### 9. **Análisis de Pruebas A/B**
*"¿Funcionó realmente nuestro experimento?"*

```python
# Combinación: groupby → agg → apply → merge → assign
def analisis_prueba_ab(df, columna_metrica='tasa_conversion'):
    # Estadísticas básicas por grupo
    stats_grupo = (df.groupby('grupo_prueba')[columna_metrica]
                  .agg(['count', 'mean', 'std', 'var'])
                  .round(4))
    
    # Prueba de significancia estadística
    from scipy import stats
    
    control = df[df['grupo_prueba'] == 'control'][columna_metrica]
    tratamiento = df[df['grupo_prueba'] == 'tratamiento'][columna_metrica]
    
    t_stat, p_value = stats.ttest_ind(control, tratamiento)
    
    # Tamaño del efecto (d de Cohen)
    std_combinada = np.sqrt(((len(control)-1)*control.var() + 
                           (len(tratamiento)-1)*tratamiento.var()) / 
                          (len(control)+len(tratamiento)-2))
    cohens_d = (tratamiento.mean() - control.mean()) / std_combinada
    
    resultados = {
        'media_control': control.mean(),
        'media_tratamiento': tratamiento.mean(),
        'mejora': ((tratamiento.mean() / control.mean()) - 1) * 100,
        'valor_p': p_value,
        'estadisticamente_significativo': p_value < 0.05,
        'cohens_d': cohens_d,
        'tamano_efecto': 'pequeño' if abs(cohens_d) < 0.5 else 'medio' if abs(cohens_d) < 0.8 else 'grande'
    }
    
    return pd.Series(resultados)

# Análisis por segmentos
resultados_segmento = (df.groupby(['segmento', 'grupo_prueba'])['tasa_conversion']
                      .agg(['mean', 'count'])
                      .unstack('grupo_prueba')
                      .round(4))
```

### 10. **Análisis Financiero (Desglose P&L)**
*"Entender rentabilidad a través de dimensiones"*

```python
# Combinación: pivot_table → stack → unstack → pct_change → cumsum
analisis_financiero = (df.pivot_table(
    values=['ingresos', 'costos', 'ganancias'], 
    index=['año', 'trimestre'],
    columns=['categoria_producto', 'region'],
    aggfunc='sum',
    fill_value=0
).round(2))

# Calcular márgenes de ganancia
margenes_ganancia = (analisis_financiero['ganancias'] / 
                    analisis_financiero['ingresos'] * 100).round(2)

# Crecimiento año tras año
crecimiento_interanual = (analisis_financiero
                         .groupby(level=1)  # Agrupar por trimestre
                         .pct_change(periods=4)  # Comparar con mismo trimestre año anterior
                         .multiply(100)
                         .round(2))

# Rendimiento acumulativo
rendimiento_acumulativo = (analisis_financiero
                          .groupby(level=0)  # Agrupar por año
                          .cumsum())

# Resumen de rendimiento
def crear_dashboard_financiero(df):
    dashboard = pd.DataFrame()
    
    # Métricas clave
    dashboard['ingresos_totales'] = df.groupby('categoria_producto')['ingresos'].sum()
    dashboard['ganancias_totales'] = df.groupby('categoria_producto')['ganancias'].sum()
    dashboard['margen_ganancia'] = (dashboard['ganancias_totales'] / 
                                   dashboard['ingresos_totales'] * 100)
    dashboard['participacion_ingresos'] = (dashboard['ingresos_totales'] / 
                                          dashboard['ingresos_totales'].sum() * 100)
    
    return dashboard.round(2)
```

## 🎯 PATRONES DE COMBINACIÓN DE FUNCIONES

### **Patrón 1: Explorar → Limpiar → Analizar**
```python
# Siempre empezar aquí
df.info() → df.isnull().sum() → df.describe()
↓
df.fillna() → df.drop_duplicates() → df.dropna()
↓
df.groupby().agg() → df.sort_values() → df.head()
```

### **Patrón 2: Series Temporales**
```python
pd.to_datetime() → df.set_index() → df.sort_index()
↓
df.resample() → df.rolling() → df.shift()
↓
df.pct_change() → df.cumsum() → df.expanding()
```

### **Patrón 3: Múltiples Datasets**
```python
pd.read_csv() × múltiples → pd.merge() → df.drop_duplicates()
↓
df.groupby() → df.agg() → df.reset_index()
↓
df.pivot_table() → df.fillna() → df.round()
```

### **Patrón 4: Análisis Estadístico**
```python
df.groupby() → df.agg() → df.describe()
↓
df.corr() → df.apply() → funciones scipy.stats
↓
df.assign() → pd.cut() → df.value_counts()
```

## 🏆 CONSEJOS PRO PARA COMBINAR FUNCIONES

1. **Encadenar operaciones** con `.pipe()` para legibilidad
2. **Usar `.assign()`** en lugar de crear columnas por separado  
3. **Combinar `.query()`** con `.groupby()` para agregaciones filtradas
4. **Usar `.agg()`** con diccionarios para diferentes operaciones por columna
5. **Aplicar `.round()`** al final de cálculos para salida limpia

La clave está en entender que el análisis de datos se trata de **combinar operaciones simples** para responder preguntas complejas de negocio.