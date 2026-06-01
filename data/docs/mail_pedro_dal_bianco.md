# Mail a Pedro Dal Bianco
**Para:** dalbianco.pedro@gmail.com  
**De:** matiasezequieldipaola@buenosaires.gob.ar  
**Asunto:** Proyecto LSA + GCBA — consulta técnica y posible colaboración

---

Hola Pedro,

Te escribo desde la Dirección General de Políticas de Accesibilidad e Inclusión del Gobierno de la Ciudad de Buenos Aires (GCBA), donde estamos desarrollando un proyecto de accesibilidad en Lengua de Señas Argentina. Como te mencioné por LinkedIn, tu trabajo — tanto el dataset LSA-T como el paper reciente sobre augmentación con LLMs — es directamente relevante para lo que estamos haciendo.

## El proyecto

El objetivo es construir un sistema de comunicación bidireccional entre personas sordas y el GCBA, pensado para su uso en tótems de atención al público. La idea es que una persona pueda acercarse, realizar una seña, y recibir una respuesta en LSA.

Para fin de año apuntamos a un POC con dos componentes en paralelo:

- **Traducción (Track A):** keypoints → Signformer → texto en español
- **Detección de intención (Track B):** keypoints → clasificador → agente que acciona la respuesta correcta para el trámite

El Track B lo estamos validando experimentalmente: usando el encoder Signformer ya entrenado sobre LSA-T como extractor de features, y entrenando un clasificador liviano encima. Es algo exploratorio — queremos saber si es técnicamente viable antes de comprometer más recursos.

La respuesta al firmante sería a través de un avatar simulado con videos pre-grabados en LSA, seleccionados según la intención detectada. La síntesis real de avatar es una visión para más adelante.

## El problema con los datos

Tenemos acceso al canal de YouTube del GCBA/COPIDIS, con más de 100 videos de trámites en LSA, y a material de una sesión de la Legislatura porteña con intérprete. El problema es el que tu paper describe muy bien para LSA-T: vocabulario muy disperso, cola larga, muy poco material bien anotado.

Del análisis sobre los videos curados:
- 61.8% de hapax legomena
- Coverage@5 de 9.6%

El vocabulario amplio y la esparsidad hacen inviable la traducción general en esta etapa. Seamos honestos: somos un equipo chico, sin ML pesado propio, y esa es nuestra deuda técnica más clara.

## Lo que estamos explorando

Frente a esto evaluamos dos caminos:

**1. Anotar el material existente:** Tenemos un primer contacto con un grupo de investigadores (Signai) para trabajar en la curación y anotación de los videos del GCBA.

**2. Generar nuestro propio dataset acotado:** Organizar una sesión de grabación con la comunidad sorda — clips cortos, vocabulario controlado, enfocados en 15-25 trámites específicos del GCBA. No apuntamos a traducción general sino a identificar intenciones concretas.

## Nuestra fortaleza

Lo que sí tenemos es algo difícil de conseguir para un equipo académico: acceso directo a intérpretes LSA certificados, material audiovisual existente del GCBA, y un vínculo real con la comunidad sorda porteña a través de COPIDIS. Creemos que eso puede ser valioso en una colaboración.

## Una pregunta puntual

Para el clasificador de intención con vocabulario acotado (15-25 clases), ¿qué orden de magnitud de clips por clase ves viable? ¿Cambia mucho la ecuación si hacemos fine-tuning desde el encoder LSA-T ya entrenado en lugar de entrenar desde cero?

## Colaboración

Este es un proyecto open source. Somos un equipo chico y estamos abiertos a colaboraciones o convenios que sean mutuamente beneficiosos, alineando expectativas desde el principio. Si hay interés de tu parte, cuando estés de vuelta del viaje nos encantaría agendar una llamada para contarte más y escuchar tu perspectiva.

Quedo atento. Saludos,

Matías Di Paola  
Dirección General de Políticas de Accesibilidad e Inclusión — GCBA  
matiasezequieldipaola@buenosaires.gob.ar
