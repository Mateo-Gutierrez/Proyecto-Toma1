import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Visualización de Datos Estudiantiles",
    page_icon="🎓",
    layout="wide",
)

# Cargar datos
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/Mateo-Gutierrez/Proyecto-Toma1/d3bb98b70dad9e7b2159634afb18c0e0476681e1/student-por.csv"
    return pd.read_csv(url, delimiter=";")

data = load_data()

st.title("🎓 Dashboard de análisis estudiantil")
st.markdown(
        """
        Este tablero interactivo presenta un análisis del rendimiento estudiantil basado en datos de dos colegios de Portugal. 
        Los datos incluyen información demográfica, social y académica, junto con las calificaciones finales de los estudiantes 
        en tres periodos académicos.
        
        Consideraciones:
        - En Portugal, el sistema de calificaciones es de 0 a 20, sin decimales, y el mínimo aprobatorio es 10
        - G1, G2, G3 corresponden a primer, segundo, tercer y último trimestre del año, así como el periodo calificado respectivamente
        ---
        """
    )

# Sidebar para filtros
st.sidebar.title("📊 Filtros")
selected_school = st.sidebar.multiselect(
    "Selecciona el colegio", options=data["school"].unique(), default=data["school"].unique()
)
selected_sex = st.sidebar.multiselect(
    "Selecciona el sexo", options=data["sex"].unique(), default=data["sex"].unique()
)
selected_age_range = st.sidebar.slider(
    "Selecciona rango de edad", int(data["age"].min()), int(data["age"].max()), (15, 20)
)

# Texto aclaratorio
st.sidebar.markdown(
    """
    **Aclaración:**
    El análisis de datos (gráficas, tablas, etc.) están sujetos a los filtros; por lo que se omiten muy pocos datos.
    """
)

# Aplicar filtros
filtered_data = data[
    (data["school"].isin(selected_school)) &
    (data["sex"].isin(selected_sex)) &
    (data["age"].between(*selected_age_range))
]

# Índice interactivo
secciones = [
    "📘 Información del Dataset",
    "📈 Estadísticas Generales",
    "📊 Visualizaciones Interactivas",
    "📉 Visualización de correlación",
    "✅ Resultados",
    "🧐 Conclusiones"
]
# Estilizar el texto de la radio con Markdown
st.markdown(
    """
    <style>
    .big-font {
        font-size:48px !important;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Aplicar estilo al texto de la radio
st.markdown('<p class="big-font">Navega por las secciones:</p>', unsafe_allow_html=True)

# Radio con opciones
seleccion = st.radio("", secciones)

if seleccion == "📘 Información del Dataset":
    st.title("📘 Información del Dataset")
    st.markdown(
        """
        El conjunto de datos abarca características como:
        
        - **Atributos Demográficos:** Edad, sexo, tipo de dirección.
        - **Atributos Educativos:** Tiempo de estudio, fallos previos, apoyo escolar y familiar.
        - **Notas:** Calificaciones de los periodos académicos (G1, G2 y G3).

        **Fuente de los datos:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance)
        
        ---
        """
    )

elif seleccion == "📈 Estadísticas Generales":
    st.header("📈 Estadísticas Generales")
    st.markdown(
        """
        Este conjunto de datos incluye características como edad, género, tiempo de estudio, apoyo educativo, y notas de los estudiantes.
        """
    )
    
    # Expander para registros filtrados
    with st.expander("📋 Registros Filtrados y Estadísticas Generales", expanded=False):
        st.write(f"**Total de registros filtrados:** {len(filtered_data)}")
        st.dataframe(filtered_data.describe())
    
    # Expander para descripciones de grupos
    with st.expander("📘 Descripción y Análisis Segmentado por Grupos", expanded=False):
        st.markdown(
            """
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                <p> <strong>Descripción de los Grupos:</strong></p>
            <div style="text-align: left; font-size: 18px; font-weight: bold;">
                <p><strong>G1:</strong> Nota obtenida en el primer periodo académico.</p>
                <p><strong>G2:</strong> Nota obtenida en el segundo periodo académico.</p>
                <p><strong>G3:</strong> Nota final obtenida al finalizar el año.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dividir en columnas para mostrar tablas lado a lado
        col1, col2, col3 = st.columns(3)

        # Tabla para G1
        with col1:
            st.subheader("Promedio G1 por Sexo y Edad")
            group_g1 = filtered_data.groupby(["sex", "age"])["G1"].mean().reset_index()
            st.dataframe(group_g1.style.format({"G1": "{:.2f}"}))

        # Tabla para G2
        with col2:
            st.subheader("Promedio G2 por Sexo y Edad")
            group_g2 = filtered_data.groupby(["sex", "age"])["G2"].mean().reset_index()
            st.dataframe(group_g2.style.format({"G2": "{:.2f}"}))

        # Tabla para G3
        with col3:
            st.subheader("Promedio G3 por Sexo y Edad")
            group_g3 = filtered_data.groupby(["sex", "age"])["G3"].mean().reset_index()
            st.dataframe(group_g3.style.format({"G3": "{:.2f}"}))

elif seleccion == "📊 Visualizaciones Interactivas":
    st.header("📊 Visualizaciones Interactivas")

    # Distribución por colegio
    with st.expander("Distribución de Estudiantes por Colegio", expanded=False):
        st.subheader("Distribución de Estudiantes por Colegio")
        st.markdown(
            """
            Este gráfico muestra cómo se distribuyen los estudiantes entre los dos colegios del dataset: 
            **Gabriel Pereira (GP)** y **Mousinho da Silveira (MS)**. 
            La visualización resalta la proporción de estudiantes en cada colegio, lo que puede ayudar a entender la composición del dataset.
            """
        )

        # Recuento de estudiantes por colegio
        school_counts = filtered_data["school"].value_counts()
        st.markdown(
            f"""
            **Recuento por Colegio:**
            - **Gabriel Pereira (GP):** {school_counts.get('GP', 0)} estudiantes
            - **Mousinho da Silveira (MS):** {school_counts.get('MS', 0)} estudiantes
            """
        )
        
        # Gráfico circular
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(
            school_counts,
            labels=school_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#FFD700", "#6495ED"]
        )
        ax.set_title("Distribución de Estudiantes por Colegio", fontsize=14, color="navy")
        st.pyplot(fig)

    # Relación entre sexo y notas
    with st.expander("Relación entre Sexo y Nota Final (G3) por Colegio", expanded=False):
        st.subheader("Relación entre Sexo y Nota Final (G3) por Colegio")
        st.markdown(
        """
        En esta gráfica se analiza cómo las notas finales (G3) varían según el sexo del estudiante 
        (**Femenino** o **Masculino**) y su colegio. Esta comparación permite identificar posibles diferencias 
        en el rendimiento académico por género en ambos colegios.
        """
    )

        # Gráfico de la relación entre sexo y notas finales (G3) por colegio
        fig, ax = plt.subplots(figsize=(10, 6))
        grouped_data = filtered_data.groupby(["school", "sex"])["G3"].mean().unstack()
        grouped_data.plot(kind="bar", ax=ax, color=["#FF6347", "#4682B4"])
        ax.set_title("Relación entre Sexo y Nota Final (G3) por Colegio", fontsize=14, color="navy")
        ax.set_xlabel("Colegio", fontsize=12)
        ax.set_ylabel("Nota Promedio (G3)", fontsize=12)
        st.pyplot(fig)

    # Nota final por edad y sexo
    with st.expander("Nota Final (G3) por Edad y Sexo", expanded=False):
        st.subheader("Nota Final (G3) por Edad y Sexo")
        st.markdown(
            """
            Este gráfico explora la relación entre la edad de los estudiantes y sus notas finales (G3), 
            desglosada por sexo. Permite observar patrones de rendimiento académico a través de diferentes 
            grupos de edad, separados en categorías de género.
            """
        )
        fig, ax = plt.subplots(figsize=(12, 6))
        age_sex_data = filtered_data.groupby(["age", "sex"])["G3"].mean().unstack()
        age_sex_data.plot(kind="bar", ax=ax, stacked=False, color=["#90EE90", "#FFB6C1"])
        ax.set_title("Nota Final (G3) por Edad y Sexo", fontsize=14, color="navy")
        ax.set_xlabel("Edad", fontsize=12)
        ax.set_ylabel("Nota Promedio (G3)", fontsize=12)
        st.pyplot(fig)
    with st.expander("Impacto de los recursos de apoyo escolar en las notas", expanded=False):
        # Impacto de apoyo escolar
        st.subheader("Impacto del Apoyo Escolar y Familiar")
        st.markdown("Esta sección analiza cómo el apoyo escolar y familiar afecta las notas finales de los estudiantes (G3).")

        fig, ax = plt.subplots(figsize=(8, 6))
        schoolsup_data = filtered_data.groupby("schoolsup")["G3"].mean()
        ax.bar(schoolsup_data.index, schoolsup_data.values, color=["#d73027", "#4575b4"])
        ax.set_title("Impacto del Apoyo Escolar en la Nota Final (G3)", fontsize=14, color="navy")
        ax.set_xlabel("Apoyo Escolar (Sí/No)", fontsize=12)
        ax.set_ylabel("Nota Promedio (G3)", fontsize=12)
        st.pyplot(fig)
        st.markdown("El gráfico muestra que los estudiantes sin apoyo escolar (schoolsup = no) tienen un rendimiento ligeramente superior en la nota final (G3) en comparación con quienes reciben apoyo escolar, aunque las diferencias en los promedios son pequeñas y la mediana es más alta para el grupo sin apoyo. Esto podría explicarse porque los estudiantes con apoyo escolar suelen requerir asistencia debido a dificultades académicas previas, mientras que quienes no lo reciben podrían tener una base académica más sólida y no necesitar este tipo de ayuda.")
        
        # Impacto del apoyo familiar
        fig, ax = plt.subplots(figsize=(8, 6))
        famsup_data = filtered_data.groupby("famsup")["G3"].mean()
        ax.bar(famsup_data.index, famsup_data.values, color=["#d73027", "#4575b4"])
        ax.set_title("Impacto del Apoyo Familiar en la Nota Final (G3)", fontsize=14, color="navy")
        ax.set_xlabel("Apoyo Familiar (Sí/No)", fontsize=12)
        ax.set_ylabel("Nota Promedio (G3)", fontsize=12)
        st.pyplot(fig)

        st.markdown("Los estudiantes que reciben apoyo familiar (famsup = yes) presentan un rendimiento en G3 ligeramente superior al de aquellos que no lo reciben, aunque las diferencias en las notas finales entre ambos grupos son mínimas. Esto sugiere que, si bien el apoyo familiar podría ser un factor motivador, su impacto en el rendimiento académico es limitado, y otros factores como los hábitos de estudio (studytime) o la asistencia (absences) podrían tener una influencia más significativa en las calificaciones.")

        # Comparación con acceso a internet
        st.subheader("Impacto del Acceso a Internet")
        st.markdown(
            """
            Aquí se analiza cómo el acceso a Internet afecta el rendimiento académico final. 

            """
        )
        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(8, 6))

        # Dividir los datos en función de la columna 'internet'
        categories = data['internet'].unique()  # Categorías únicas en la columna 'internet'
        data_to_plot = [data[data['internet'] == category]['G3'] for category in categories]

        # Crear boxplot
        ax.boxplot(data_to_plot, labels=categories)

        # Configurar títulos y etiquetas
        ax.set_title('Impacto del acceso a internet en la Nota final (G3)', fontsize=14)
        ax.set_xlabel('Acceso a Internet', fontsize=12)
        ax.set_ylabel('Nota final (G3)', fontsize=12)
        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    
        st.markdown(
            """
            El acceso a internet por sí solo no parece ser un factor determinante en el rendimiento académico (G3), ya que::
            
            - Tanto los estudiantes con acceso a internet ("yes") como aquellos sin acceso ("no") tienen una mediana de calificaciones finales (G3) muy parecida, alrededor de 12. Esto sugiere que, en promedio, el acceso a internet no tiene un impacto significativo en la nota final.
            - Los estudiantes con acceso a internet tienen una distribución ligeramente más compacta en las calificaciones (menos dispersión) en comparación con los estudiantes sin acceso.
            """
        )
        # Acceso a internet (internet), las horas de estudio (studytime), y el apoyo escolar (schoolsup) están relacionados.
        st.subheader("Impacto del Acceso a Internet, horas de estudio, y apoyo escolar")
        st.markdown(
            """
            El gráfico muestra cómo el acceso a internet, las horas de estudio y el apoyo escolar están relacionados. 

            """
        )
        # Crear gráfico combinado
        fig, ax = plt.subplots(figsize=(10, 6))

        # Agrupar datos y definir colores
        grouped_data = data.groupby(['internet', 'schoolsup'])['studytime']
        colors = {'yes': '#FF6347', 'no': '#4682B4'}
        positions = [1, 2, 4, 5]  # Posiciones de los boxplots
        labels = ['No Internet / No Apoyo', 'No Internet / Apoyo', 'Internet / No Apoyo', 'Internet / Apoyo']

        # Crear boxplots
        box_data = []
        for internet_value in ['no', 'yes']:
            for schoolsup_value in ['no', 'yes']:
                subset = data[
                    (data['internet'] == internet_value) & 
                    (data['schoolsup'] == schoolsup_value)
                ]['studytime']
                box_data.append(subset)

        # Dibujar el gráfico
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, widths=0.6)

        # Personalizar colores
        for patch, group in zip(bp['boxes'], [f'no_{k}' for k in colors] + [f'yes_{k}' for k in colors]):
            patch.set_facecolor(colors[group.split('_')[1]])

        # Configurar etiquetas y diseño
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Interacción entre Acceso a Internet, Horas de Estudio y Apoyo Escolar", fontsize=14)
        ax.set_xlabel("Categorías", fontsize=12)
        ax.set_ylabel("Horas de Estudio", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        st.markdown(
            """
            Los estudiantes sin internet que reciben apoyo escolar tienden a tener un rango más amplio y una mediana ligeramente superior de horas de estudio, lo que sugiere que este apoyo fomenta mejores hábitos de estudio. En cambio, quienes no tienen apoyo escolar muestran una mediana más baja, indicando menor constancia. Entre los estudiantes con acceso a internet, aquellos con apoyo escolar mantienen una mediana alta y datos más consistentes, reforzando la importancia del apoyo escolar. Sin embargo, quienes no cuentan con este apoyo presentan una mayor dispersión en las horas de estudio, lo que sugiere que el acceso a internet por sí solo no garantiza hábitos eficientes.
            """
        )
elif seleccion == "📉 Visualización de correlación":
    with st.expander("Correlación entre horas de estudio y rendimiento académico", expanded=False):
        st.header("Correlación entre horas de estudio y rendimiento académico")

        # Texto explicativo
        st.markdown(
            """
            En esta sección se explora la relación entre el tiempo dedicado al estudio semanal (**studytime**) y las calificaciones en los tres periodos académicos:
            **G1 (Primer Periodo)**, **G2 (Segundo Periodo)**, y **G3 (Nota Final)**. Además, se muestran las correlaciones calculadas entre estas variables.
            """
        )

        # Cálculo de correlaciones
        correlacion_G1 = filtered_data["studytime"].corr(filtered_data["G1"])
        correlacion_G2 = filtered_data["studytime"].corr(filtered_data["G2"])
        correlacion_G3 = filtered_data["studytime"].corr(filtered_data["G3"])

        # Mostrar las correlaciones
        st.write(f"**Correlación entre Studytime y G1:** {correlacion_G1:.2f}")
        st.write(f"**Correlación entre Studytime y G2:** {correlacion_G2:.2f}")
        st.write(f"**Correlación entre Studytime y G3:** {correlacion_G3:.2f}")

        # Gráfico: Studytime vs G1, G2, G3
        fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
        fig.suptitle("Relación entre Horas de Estudio y Notas (G1, G2, G3)", fontsize=16)

        # Gráficos individuales
        axes[0].scatter(filtered_data["studytime"], filtered_data["G1"], alpha=0.6, color="blue")
        axes[0].set_title("Studytime vs G1")
        axes[0].set_xlabel("Studytime")
        axes[0].set_ylabel("G1")

        axes[1].scatter(filtered_data["studytime"], filtered_data["G2"], alpha=0.6, color="orange")
        axes[1].set_title("Studytime vs G2")
        axes[1].set_xlabel("Studytime")

        axes[2].scatter(filtered_data["studytime"], filtered_data["G3"], alpha=0.6, color="green")
        axes[2].set_title("Studytime vs G3")
        axes[2].set_xlabel("Studytime")

        plt.tight_layout()
        st.pyplot(fig)

    with st.expander("Correlación entre ausencias y rendimiento académico", expanded=False):
        st.header("Correlación entre ausencias y rendimiento académico")

        # Texto explicativo
        st.markdown(
            """
            En esta sección se analiza la relación entre el número de ausencias (**absences**) y las calificaciones académicas (**G1, G2, G3**). 
            Se incluye una línea de regresión que indica cómo las ausencias afectan las calificaciones, sugiriendo una correlación negativa.
            """
        )

        # Cálculo de correlaciones para ausencias
        corr_absences_G1 = filtered_data["absences"].corr(filtered_data["G1"])
        corr_absences_G2 = filtered_data["absences"].corr(filtered_data["G2"])
        corr_absences_G3 = filtered_data["absences"].corr(filtered_data["G3"])

        # Mostrar las correlaciones
        st.write(f"**Correlación entre Ausencias y G1:** {corr_absences_G1:.2f}")
        st.write(f"**Correlación entre Ausencias y G2:** {corr_absences_G2:.2f}")
        st.write(f"**Correlación entre Ausencias y G3:** {corr_absences_G3:.2f}")

        # Gráfico de regresión para G3
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_data["absences"], filtered_data["G3"], alpha=0.6, color="purple", s=30, label="Datos")
        m, b = np.polyfit(filtered_data["absences"], filtered_data["G3"], 1)
        ax.plot(filtered_data["absences"], m * filtered_data["absences"] + b, color="red", label="Línea de regresión")
        ax.set_title("Relación entre Ausencias y Nota Final (G3)", fontsize=14, color="navy")
        ax.set_xlabel("Número de Ausencias", fontsize=12)
        ax.set_ylabel("Nota Final (G3)", fontsize=12)
        ax.legend()
        st.pyplot(fig)

elif seleccion == "✅ Resultados":
    st.header("✅ Resultados")

    # Análisis descriptivo
    with st.expander("📋 Análisis Descriptivo", expanded=False):
        st.markdown(
            """
            - Un análisis estadístico básico revela que, en promedio, los estudiantes de ambos colegios muestran una mayor influencia en su desempeño académico por parte de la madre en comparación con el padre. Este resultado sugiere que el rol materno tiene un impacto más significativo en el apoyo educativo de los estudiantes.
            - Existe una gran diferencia entre las horas libres y las horas de estudio. Quizás, dicha diferencia se refleja en 
              las notas escolares; puesto que la media de notas por periodo escolar no supera los 12 puntos (de los 20 puntos máximos otorgables).
            """
        )

    # Visualización segmentada
    with st.expander("📊 Visualización Segmentada", expanded=False):
        st.markdown(
            """
            - Al segmentar las notas por género, se observa un mayor esfuerzo reflejado en los resultados académicos de las mujeres en comparación con los hombres.
            - Con base en la interpretación anterior, se observa que el colegio Gabriel Pereira presenta calificaciones superiores en comparación con el Mousinho da Silveira. Además, en ambos casos, las mujeres obtienen notas más altas que los hombres, manteniendo una tendencia consistente.
            - Al realizar una separación por edades, se observa que los jóvenes de 19 años no demuestran interés respecto a sus notas a comparación de las demás edades. Sin embargo, segmentar de esta manera, muestra resultados distintos a los análisis anteriores, puesto que jóvenes hombres de 15 y 20 años tienen mayores calificaciones que las mujeres.
            - Los resultados muestran que los estudiantes que no reciben apoyo educativo formal tienden a obtener mejores calificaciones. Esto podría explicarse por el hecho de que, en ausencia de apoyo escolar, muchos de ellos cuentan con apoyo familiar, lo que influye positivamente en su desempeño académico. Además, se evidencia que aquellos estudiantes que recurren al conocimiento disponible en internet también logran mejorar sus calificaciones, lo que sugiere que las fuentes alternativas de aprendizaje pueden complementar eficazmente su formación.
            - Los resultados indican que los estudiantes sin acceso a internet que reciben apoyo escolar tienden a dedicar un rango más amplio de horas al estudio, con una mediana ligeramente superior, lo que sugiere que el apoyo escolar contribuye a fomentar mejores hábitos de estudio. Por el contrario, aquellos que no cuentan con dicho apoyo presentan una mediana más baja en sus horas de estudio, lo que refleja una menor constancia en sus hábitos académicos.
            """
        )
        # Expander para Resultados de las Correlaciones
    with st.expander("🔗 Resultados de las Correlaciones", expanded=False):
        st.markdown(
            """
            ### Correlación entre Faltas de asistencia y Notas
            - Los resultados muestran que, para la variable **absences**, los estudiantes con pocas ausencias (entre 0 y 10) tienden a obtener calificaciones más altas en **G3**, generalmente por encima de 7.5. 
            - Además, se observa una correlación negativa entre las ausencias y las notas finales: a medida que aumenta el número de ausencias, las calificaciones tienden a disminuir.

            ### Correlación entre Apoyo escolar y Notas
            - Los resultados muestran que los estudiantes que no reciben apoyo escolar (**schoolsup = no**) tienen un rendimiento ligeramente superior en la nota final (**G3**) en comparación con aquellos que sí reciben apoyo. 
            - Aunque las diferencias en los promedios son pequeñas, la mediana es más alta en el grupo sin apoyo escolar. Esto podría deberse a que los estudiantes que requieren apoyo suelen enfrentarse a dificultades académicas previas, mientras que quienes no lo necesitan podrían tener una base académica más sólida.
            - Por otro lado, los estudiantes que reciben apoyo familiar (**famsup = yes**) presentan un rendimiento en **G3** ligeramente superior al de aquellos que no cuentan con este respaldo. Sin embargo, las diferencias en las calificaciones finales entre ambos grupos son mínimas. Esto indica que, aunque el apoyo familiar podría ser un factor motivador, su influencia en el rendimiento académico es limitada, y variables como los hábitos de estudio (**studytime**) o la asistencia (**absences**) podrían tener un impacto más significativo en las notas.
            """
    )


elif seleccion == "🧐 Conclusiones":
    st.header("🧐 Conclusiones")
    st.markdown(
        """
        <div style="text-align: justify;">
            Los resultados reflejan que el apoyo escolar no siempre se traduce en mejores calificaciones, ya que los estudiantes sin este tipo de asistencia tienden a obtener notas finales ligeramente superiores. Esto podría deberse a que quienes no requieren apoyo suelen tener bases académicas más sólidas, mientras que los que lo reciben enfrentan mayores desafíos previos. Sin embargo, el apoyo escolar fomenta mejores hábitos de estudio, especialmente en estudiantes sin acceso a internet. El apoyo familiar tiene un impacto positivo moderado en el rendimiento académico, aunque las diferencias en las notas finales entre quienes lo reciben y quienes no son pequeñas. Factores como los hábitos de estudio y la asistencia parecen ser más determinantes en los resultados escolares.
        <div style="text-align: justify;">
            Finalmente, el acceso a internet no garantiza un mejor rendimiento académico, aunque sí puede contribuir a reducir la dispersión en las calificaciones. Su impacto es mayor cuando se combina con apoyo escolar, ya que permite mantener hábitos de estudio consistentes. Sin embargo, su ausencia fomenta una mayor dependencia de estrategias alternativas, como el apoyo familiar, para lograr buenos resultados.
        <div style="text-align: justify;">
            La correlación negativa entre las ausencias y las calificaciones finales indica que la asistencia regular es un factor clave en el rendimiento académico. Los estudiantes con menos de 10 ausencias logran notas superiores a 7.5, mientras que un mayor número de ausencias afecta negativamente las calificaciones, evidenciando la importancia de la constancia en el aula. En cuanto al apoyo, los estudiantes sin apoyo escolar tienden a tener un rendimiento ligeramente mejor, probablemente por contar con bases académicas más sólidas. Por otro lado, el apoyo familiar tiene un impacto positivo moderado en las notas, aunque es limitado. Factores como la asistencia y los hábitos de estudio parecen ser más determinantes para el desempeño académico que el tipo de apoyo recibido.
        """,
        unsafe_allow_html=True
    )

# Sección de Créditos
st.sidebar.markdown("### Créditos:")
st.sidebar.markdown("""
- **Brandon Martínez Moncada**  
- **Alejandra Castillo Marín**  
- **Mateo Gutierrez Roa**  
- **Eddie Santiago Ramos**  

**Materia:** Toma de decisiones 1  
**Docente:** Diego Fernando Avila Ibañez
**Universidad:** Sergio Arboleda
""")
st.sidebar.markdown("**Fuente de datos:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance)")
# Información adicional
st.sidebar.info("💡 Desarrollado con Streamlit para visualizar y analizar datos educativos.")
