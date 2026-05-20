<!-- page 1 -->
<!-- image -->

<!-- image -->

## Traducci´ on de Secuencias de la Lengua de Se˜ nas Argentina mediante Visi´ on por Computadora

por Juan Bratti

Presentado ante la FACULTAD DE MATEM ´ ATICA, ASTRONOM ´ IA, F ´ ISICA Y COMPUTACI ´ ON como parte de los requerimientos para la obtenci´ on del grado de Licenciado en Ciencias de la Computaci´ on de la

UNIVERSIDAD NACIONAL DE C ´ ORDOBA

Diciembre, 2025

Director: Dr. Diego Sebasti´ an P´ erez Profesora Representante: Dra. Laura Alonso Alemany

Este trabajo se distribuye bajo una licencia Creative Commons Atribuci´ on 4.0 Internacional cb


<!-- page 2 -->

## Resumen

Este trabajo aborda la traducci´ on autom´ atica de la Lengua de Se˜ nas Argentina (LSA) mediante t´ ecnicas de visi´ on por computadora, con el objetivo de desarrollar sistemas capaces de generar texto coherente a partir de secuencias visuales de se˜ nas. Se centra en representaciones de poses (keypoints) extra´ ıdas de los videos y utiliza el conjunto de datos LSA-T como base experimental. Se presenta una revisi´ on te´ orica sobre la traducci´ on de lenguas de se˜ nas y los modelos de aprendizaje profundo, seguida de la implementaci´ on de un modelo Transformer baseline adaptado a secuencias de keypoints. Se probaron distintas configuraciones y se desarroll´ o una versi´ on adaptada del Signformer, incorporando codificaci´ on posicional convolucional y mecanismos de atenci´ on ajustados a las din´ amicas temporales y espaciales de la lengua de se˜ nas. Los resultados muestran que el modelo baseline capta palabras frecuentes pero tiene dificultades para generar oraciones completas con sentido, mientras que la adaptaci´ on de Signformer mejora significativamente las m´ etricas BLEU, estableciendo un nuevo punto de referencia para la traducci´ on autom´ atica de LSA, sentando las bases para futuras investigaciones.

Palabras clave: Lengua de Se˜ nas Argentina, traducci´ on autom´ atica, visi´ on por computadora, Transformer, Signformer, keypoints.

## Abstract

This work addresses the machine translation of Argentine Sign Language (LSA) using computer vision techniques, aiming to develop systems capable of generating coherent text from visual sign sequences. It focuses on posebased representations (keypoints) extracted from videos and uses the LSA-T dataset as the experimental basis. A theoretical review of sign language translation and deep learning models is presented, followed by the implementation of a Transformer baseline adapted to keypoint sequences. Different configurations were tested, and an adapted version of Signformer was developed, incorporating convolutional positional encoding and attention mechanisms tailored to the temporal and spatial dynamics of sign language. Results show that the baseline model captures frequent words but struggles to generate complete, meaningful sentences, while the adapted Signformer significantly improves BLEU scores, establishing a new benchmark for LSA translation and laying the groundwork for future research.

Keywords: Argentine Sign Language, machine translation, computer vision, Transformer, Signformer, keypoints.


<!-- page 3 -->

## Agradecimientos

Quiero expresar mi eterno agradecimiento a mi Facultad y a mi Universidad, que me abrieron las puertas y me formaron tanto profesional como personalmente. Gracias por brindarme las herramientas necesarias para culminar mi carrera de grado en tiempo y forma, y a todos los profesores y profesoras que, incluso en tiempos dif´ ıciles, dedicaron su tiempo y esfuerzo a mi educaci´ on. Me enorgullece profundamente ser parte de la familia de graduados de la Universidad P´ ublica, referente de excelencia y compromiso, que debemos cuidar y defender siempre.

Tambi´ en quiero agradecer a mi director, Sebasti´ an, quien acept´ o dirigir este trabajo especial y me brind´ o la oportunidad de culminar esta etapa de mi formaci´ on profesional.

A mis amigos y amigas por acompa˜ narme y alentarme durante este camino, haci´ endolo mucho m´ as llevadero. Gracias por su paciencia y por acompa˜ narme en las largas tardes de estudio.

A mis hermanos y a toda mi familia, por su constante apoyo y por estar siempre presentes, incluso en la distancia.

Y, sobre todo, nada de esto habr´ ıa sido posible sin el esfuerzo y el apoyo incondicional de mis padres. Su ejemplo me sostuvo en cada etapa, y cada logro que celebro lleva impreso un pedacito de su sacrificio. Aunque el t´ ıtulo tenga mi nombre, siento que en gran parte les pertenece a ellos. Gracias por ense˜ narme que todo lo que me proponga es posible y que no hay meta demasiado grande.


<!-- page 4 -->

## Reconocimientos

Este trabajo utiliz´ o recursos computacionales de UNC Superc´ omputo (CCAD) de la Universidad Nacional de C´ ordoba 1 , que forman parte del Sistema Nacional de Computaci´ on de Alto Desempe˜ no (SNCAD) de la Rep´ ublica Argentina.

This work used computational resources from UNC Superc´ omputo (CCAD) - Universidad Nacional de C´ ordoba, which are part of SNCAD, Rep´ ublica Argentina.

1 https://supercomputo.unc.edu.ar/


<!-- page 5 -->

## ´ Indice

| 1. Introducci´ on       | 1. Introducci´ on                                                      | 1. Introducci´ on                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1. Introducci´ on                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 1. Introducci´ on                                                      | 10                                                    |
|-------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|-------------------------------------------------------|
| 2. La Lengua de Se˜ nas | 2. La Lengua de Se˜ nas                                                | 2. La Lengua de Se˜ nas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 2. La Lengua de Se˜ nas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 2. La Lengua de Se˜ nas                                                | 11                                                    |
|                         | 2.1. Traducci´ on y Reconocimiento de la Lengua de Se˜ nas . . . . .   | 2.1. Traducci´ on y Reconocimiento de la Lengua de Se˜ nas . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 2.1. Traducci´ on y Reconocimiento de la Lengua de Se˜ nas . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 2.1. Traducci´ on y Reconocimiento de la Lengua de Se˜ nas . . . . .   | 12                                                    |
|                         |                                                                        | 2.1.1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Reconocimiento . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | . .                                                                    | 12                                                    |
|                         |                                                                        | 2.1.2.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Traducci´ on . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | . .                                                                    | 12                                                    |
|                         | 2.2.                                                                   | Traducci´ on gloss-based y gloss-free . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Traducci´ on gloss-based y gloss-free . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Traducci´ on gloss-based y gloss-free . . . . . . . . . . . . . . .    | 13                                                    |
|                         |                                                                        | 2.2.1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Enfoque gloss-based . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | . .                                                                    | 13                                                    |
|                         |                                                                        | 2.2.2.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Enfoque gloss-free . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | . .                                                                    | 14                                                    |
|                         | 2.3.                                                                   | La Lengua de Se˜ nas Argentina . . . . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | La Lengua de Se˜ nas Argentina . . . . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | La Lengua de Se˜ nas Argentina . . . . . . . . . . . . . . . . . .     | 15                                                    |
|                         |                                                                        | 2.3.1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | LSA64 . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | . .                                                                    | 15                                                    |
|                         |                                                                        | 2.3.2.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | . .                                                                    |                                                       |
|                         |                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                        | 16                                                    |
|                         |                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | LSA-T                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                        |                                                       |
|                         | Visi´ on por Computadora                                               | Visi´ on por Computadora                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Visi´ on por Computadora                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Visi´ on por Computadora                                               |                                                       |
|                         |                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                        | 17                                                    |
|                         | 3.1. ¿Qu´ e es computer vision o visi´ on por computadora? . . . . . . | 3.1. ¿Qu´ e es computer vision o visi´ on por computadora? . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 3.1. ¿Qu´ e es computer vision o visi´ on por computadora? . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 3.1. ¿Qu´ e es computer vision o visi´ on por computadora? . . . . . . |                                                       |
|                         |                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                        | 17                                                    |
|                         | 3.2.                                                                   | Aplicaciones generales de la visi´ on por computadora . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Aplicaciones generales de la visi´ on por computadora . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Aplicaciones generales de la visi´ on por computadora . . . . . .      | 17                                                    |
|                         | 3.3.                                                                   | ¿C´ omo se representa una imagen? . . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | ¿C´ omo se representa una imagen? . . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | ¿C´ omo se representa una imagen? . . . . . . . . . . . . . . . .      | 18 53                                                 |
|                         | 3.4. 3.5. 3.6. 3.7. Visi´ ca de 4.1.                                   | Preprocesamiento previo a la extracci´ on de caracter´ ısticas . . 3.4.1. Filtrados especiales y kernels . . . . . . . . . . . . . . 3.4.2. Data Augmentation . . . . . . . . . . . . . . . . . . . Extracci´ on de caracter´ ısticas en im´ agenes . . . . . . . . . . . 3.5.1. M´ etodos cl´ asicos de extracci´ on de caracter´ ısticas . . . 3.5.2. Representaci´ on de las caracter´ ısticas . . . . . . . . . Modelos tradicionales . . . . . . . . . . . . . . . . . . . . . . Aprendizaje profundo: cambio de paradigma . . . . . . . . . 3.7.1. Redes neuronales . . . . . . . . . . . . . . . . . . . . 3.7.2. Redes Neuronales Convolucionales . . . . . . . . . . . 3.7.3. Redes Neuronales Recurrentes . . . . . . . . . . . . . 3.7.4. Arquitecturas Encoder-Decoder y Transformers . . . 3.7.5. ¿Qu´ e es un Transformer? . . . . . . . . . . . . . . . . 3.7.6. Embeddings . . . . . . . . . . . . . . . . . . . . . . . 3.7.7. Codificaci´ on posicional . . . . . . . . . . . . . . . . . 3.7.8. El Encoder . . . . . . . . . . . . . . . . . . . . . . . 3.7.9. El Decoder . . . . . . . . . . . . . . . . . . . . . . . on por Computadora aplicado a la Traducci´ on Autom´ ati- la Lengua de Se˜ nas Arquitecturas basadas en redes neuronales . . . . . . . . . . | Preprocesamiento previo a la extracci´ on de caracter´ ısticas . . 3.4.1. Filtrados especiales y kernels . . . . . . . . . . . . . . 3.4.2. Data Augmentation . . . . . . . . . . . . . . . . . . . Extracci´ on de caracter´ ısticas en im´ agenes . . . . . . . . . . . 3.5.1. M´ etodos cl´ asicos de extracci´ on de caracter´ ısticas . . . 3.5.2. Representaci´ on de las caracter´ ısticas . . . . . . . . . Modelos tradicionales . . . . . . . . . . . . . . . . . . . . . . Aprendizaje profundo: cambio de paradigma . . . . . . . . . 3.7.1. Redes neuronales . . . . . . . . . . . . . . . . . . . . 3.7.2. Redes Neuronales Convolucionales . . . . . . . . . . . 3.7.3. Redes Neuronales Recurrentes . . . . . . . . . . . . . 3.7.4. Arquitecturas Encoder-Decoder y Transformers . . . 3.7.5. ¿Qu´ e es un Transformer? . . . . . . . . . . . . . . . . 3.7.6. Embeddings . . . . . . . . . . . . . . . . . . . . . . . 3.7.7. Codificaci´ on posicional . . . . . . . . . . . . . . . . . 3.7.8. El Encoder . . . . . . . . . . . . . . . . . . . . . . . 3.7.9. El Decoder . . . . . . . . . . . . . . . . . . . . . . . on por Computadora aplicado a la Traducci´ on Autom´ ati- la Lengua de Se˜ nas Arquitecturas basadas en redes neuronales . . . . . . . . . . | . . . . . . . . . . . . . . . . . .                                    | 21 23 25 26 26 27 27 29 29 34 36 38 39 40 42 44 49 53 |


<!-- page 6 -->

| 4.1.2. Rendimiento . . . . . . . . . . . . . . . . . . . . . . . . 59 4.2. Arquitecturas basadas en transformers . . . . . . . . . . . . . 61 4.2.1. Modelo basado en transformers aplicado a SLT . . . . 62 4.2.2. Rendimiento . . . . . . . . . . . . . . . . . . . . . . . . 67                                                                                                                                                                                                                                                                                                                               |      |       |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|-------|
| 4.3. Modelo basado en keypoints . . . . . . . . . . . . . . . . . . . 68 LSA-T: Datos para la Traducci´ on Autom´ atica de LSA 69 5.1. Estructura del Dataset y Metadatos Asociados . . . . . . . . . 69 5.2. Visualizaci´ on de keypoints y bounding boxes . . . . . . . . . . 74 5.3. Preprocesamiento . . . . . . . . . . . . . . . . . . . . . . . . . 78 Modelos aplicado a LSA-T 80 6.1. Modelo basado en keypoints . . . . . . . . . . . . . . . . . . . 80 6.1.1. Configuraci´ on de entrenamiento . . . . . . . . . . . . . 99 6.1.2. Configuraci´ on de evaluaci´ on . . . . . . . . . . . . . . . 102 |      | 5. 6. |
| An´ alisis de Resultados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |      |       |
| 122                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |      | 7.    |
| 124                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |      |       |
| 125                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |      |       |
| Trabajo a Futuro . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |      |       |
| .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |      |       |
| Conclusiones                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |      |       |
| 8.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |      |       |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 8.1. |       |


<!-- page 7 -->

## 1. Introducci´ on

La comunicaci´ on constituye un pilar fundamental de la interacci´ on humana, y las barreras comunicativas entre personas oyentes y personas con dificultades auditivas contin´ uan representando un desaf´ ıo en t´ erminos de inclusi´ on y accesibilidad. La ausencia de int´ erpretes de lengua de se˜ nas en muchos entornos cotidianos limita la participaci´ on de las personas con discapacidad auditiva en la sociedad.

En los ´ ultimos a˜ nos, se han logrado avances significativos en el reconocimiento y traducci´ on de se˜ nas aisladas y de palabras individuales en diversas lenguas de se˜ nas mediante la aplicaci´ on de t´ ecnicas de visi´ on por computadora [1]. Sin embargo, el reconocimiento de una ´ unica se˜ na o palabra no es suficiente para lograr una traducci´ on completa y fluida [2] [3] [1]. Es por esto que un enfoque mas prometedor consiste en trabajar con secuencias continuas, es decir, conjuntos de gestos que forman oraciones completas en lugar de palabras individuales [4].

El desaf´ ıo de traducir secuencias continuas en la lengua de se˜ nas es considerablemente m´ as complejo, ya que implica no solo el reconocimiento de ambas manos, si no tambi´ en la combinaci´ on y relaci´ on entre gestos y la interpretaci´ on de expresiones faciales [5]. La traducci´ on en este contexto requiere modelar y comprender varios aspectos que pueden no estar directamente relacionados con las formas de las manos, lo que supone un desaf´ ıo mayor.

Gracias a la creaci´ on de conjuntos de datos espec´ ıficos para la Lengua de Se˜ nas Argentina (LSA) como LSA-T [4], se ha abierto la posibilidad de entrenar modelos de aprendizaje autom´ atico orientados a la traducci´ on de secuencias continuas en este idioma. El presente trabajo busca exponer estos avances y el potencial de distintas t´ ecnicas de visi´ on por computadora para la traducci´ on autom´ atica de LSA a texto.

Organizaci´ on del trabajo . La Secci´ on 2 presenta la Lengua de Se˜ nas, con ´ enfasis en la LSA y en las particularidades que plantean desaf´ ıos para su traducci´ on autom´ atica. La Secci´ on 3 introduce los fundamentos de la visi´ on por computadora relevantes para este campo. La Secci´ on 4 analiza c´ omo estas t´ ecnicas se aplican a la traducci´ on de lenguas de se˜ nas, revisando enfoques y modelos representativos. La Secci´ on 5 describe el conjunto de datos LSA-T, clave para el entrenamiento y evaluaci´ on de modelos en el dominio argentino. La Secci´ on 6 aborda dos arquitecturas ejemplo y sus aplicaciones a LSAT. La Secci´ on 7 presenta y analiza los resultados experimentales obtenidos, discutiendo el comportamiento de los modelos y las limitaciones observadas. Finalmente, la Secci´ on 8 expone las conclusiones generales del trabajo y plantea posibles l´ ıneas futuras de investigaci´ on.


<!-- page 8 -->

## 2. La Lengua de Se˜ nas

La lengua de se˜ nas es un sistema de comunicaci´ on visual-gestual, natural y completo, utilizado principalmente por personas sordas para comunicarse e interactuar entre s´ ı y con su entorno. Una de las confusiones m´ as comunes que hay es considerar a la lengua de se˜ nas como una mera forma de m´ ımica o gesticulaci´ on, sin embargo, se trata de una lengua con estructura propia, reglas gramaticales definidas y mucha expresividad [6]. Las lenguas de se˜ nas son lenguas naturales humanas, es decir, surgen de forma espont´ anea en comunidades ling¨ uisticas y se transmiten intergeneracionalmente. Se adquieren como una lengua materna por personas sordas expuestas a ellas desde la infancia, y cumplen con todas las funciones del lenguaje: expresar ideas, emociones, descripciones, narrativas y relaciones abstractas.

Stokoe (1980), una de las personas m´ as influyentes dentro del estudio de la lengua de se˜ nas, afirma que los signos de las lenguas de se˜ nas no son simples gestos, sino s´ ımbolos ling¨ u´ ısticos complejos, que al igual que las palabras orales, est´ an organizados en niveles de fonolog´ ıa 2 , morfolog´ ıa 3 y sintaxis [6], donde en lugar de combinar sonidos en el tiempo, las lenguas de se˜ nas organizan la informaci´ on en el espacio. En estudios, se propone una divisi´ on estructural de la lengua de se˜ nas en tres aspectos simult´ aneos de cada signo: dez o designado que refiere a la parte del cuerpo que act´ ua (por lo general las manos), sig o signado refiere al movimiento relacionado y tab o tabula hace referencia al lugar del espacio donde ocurre el signo. Esta organizaci´ on implica una sintaxis visual que combina distintas dimensiones espaciales y temporales. Las se˜ nas no son exclusivamente manuales; factores como las expresiones faciales, el movimiento de la cabeza o la mirada tienen tambi´ en una funci´ on ling¨ u´ ıstica importante, incluyendo el marcado de oraciones interrogativas, negaciones o estructuras subordinadas [6].

Por ´ ultimo, no existe una lengua de se˜ nas universal. Cada pa´ ıs (e incluso regiones dentro de un mismo pa´ ıs) puede tener su propia lengua de se˜ nas. Por ejemplo, la Lengua de Se˜ nas Argentina es distinta a la Lengua de Se˜ nas Americana (ASL), a la Lengua de Se˜ nas Brit´ anica (BSL) o la Lengua de Se˜ nas Francesa (LSF) [6].

2 Estudio de las unidades m´ ınimas distintivas que componen las se˜ nas y c´ omo se combinan para formar palabras y significados.

3 Estudio de la estructura interna de los signos y la formaci´ on de nuevos signos a partir de otros.


<!-- page 9 -->

## 2.1. Traducci´ on y Reconocimiento de la Lengua de Se˜ nas

Dentro del campo del procesamiento autom´ atico de la lengua de se˜ nas, es fundamental distinguir entre las tareas de reconocimiento y traducci´ on, ya que responden a objetivos diferentes y requieren enfoques t´ ecnicos espec´ ıficos [7].

## 2.1.1. Reconocimiento

Por un lado, el reconocimiento de la lengua de se˜ nas (Sign Language Recognition, SLR) consiste en identificar se˜ nas individuales o secuencias cortas de la lengua de se˜ nas, y clasificarlas dentro de un conjunto predefinido de categor´ ıas l´ exicas, conocidas como glosas (en ingl´ es, glosses) [8]. El objetivo del SLR no es generar texto en lenguaje oral, sino etiquetar signos espec´ ıficos, como por ejemplo reconocer que un gesto corresponde al signo 'casa' o 'trabajo', sin necesariamente producir una oraci´ on completa en espa˜ nol.

Si se trata de la identificaci´ on de se˜ nas aisladas (Isolated Sign Recognition, ISR), normalmente lo que se tiene es un video por se˜ na, y lo que se busca es reconocer la glosa que la se˜ na representa. En el caso del reconocimiento continuo (Continuous Sign Recognition, CSR), se trata de videos que contienen frases completas, no solo se˜ nas individuales, buscando obtener as´ ı la respectiva secuencia de glosas. Existen diversas aplicaciones y modelos que trabajan en el reconocimiento de se˜ nas, ya sea para el enfoque individual o continuo [9]. Es mucho m´ as frecuente ver conjuntos de datos y modelos para esta tarea que para la traducci´ on.

## 2.1.2. Traducci´ on

Por otro lado, la traducci´ on autom´ atica de la lengua de se˜ nas (Sign Language Translation, SLT) busca transformar una secuencia de se˜ nas en una oraci´ on en lenguaje oral escrito [8], no en glosas. Esta tarea, como se ha mencionado previamente, es considerablemente m´ as compleja que el reconocimiento, ya que no solo se trata de identificar signos aislados, sino de interpretar estructuras ling¨ u´ ısticas completas, resolver diferencias en el orden de las palabras y modelar informaci´ on que se transmite simult´ aneamente por elementos manuales y no manuales (como expresiones faciales, postura o el uso del espacio) [7]. Se puede observar en la figura 1 la diferencia entre SLR (en espec´ ıfico CSR) y SLT.

Una de las principales limitaciones actuales en el desarrollo de modelos de traducci´ on es que la mayor´ ıa de los conjuntos de datos disponibles est´ an orientados al reconocimiento. Es decir, contienen videos cortos etiquetados con una sola glosa, sin incluir secuencias ling¨ u´ ısticas naturales ni oraciones completas. Esto representa un obst´ aculo importante para la tarea de traducci´ on en general.


<!-- page 10 -->

Figura 1: Comparaci´ on entre reconocimiento (SLR) y traducci´ on (SLT) de la lengua de se˜ nas. Imagen proveniente de [8]

<!-- image -->

## 2.2. Traducci´ on gloss-based y gloss-free

As´ ı como podemos diferenciar en traducci´ on y reconocimiento, dentro de la traducci´ on podemos distinguir dos enfoques principales: gloss-based y gloss-free.

## 2.2.1. Enfoque gloss-based

El enfoque gloss-based plantea la traducci´ on autom´ atica como un proceso compuesto por dos etapas. Primero tenemos una etapa de reconocimiento de glosas (SLR): Se parte de un video en el que una persona realiza una secuencia de se˜ nas, y se busca extraer una secuencia de glosas. Luego, se utilizan estas glosas como entrada de un modelo de traducci´ on (por ejemplo, un transformer entrenado sobre corpus de glosas y frases en lenguaje natural). El modelo aprende a transformar secuencias de glosas como 'YO IR CASA' en una oraci´ on m´ as natural en espa˜ nol como 'Voy a casa'.

Este enfoque fue importante en el desarrollo de sistemas autom´ aticos de traducci´ on de la lengua de se˜ nas debido a varias razones. Entre ellas, permit´ ıa descomponer un problema complejo (poder obtener texto a partir de videos) en dos tareas mucho mas manejables (reconocimiento y traducci´ on). Tambi´ en, permit´ ıa aprovechar los conjuntos de datos disponibles en ese mo- mento, los cuales estaban anotados con glosas y no con frases completas. Y por ´ ultimo, permit´ ıa reutilizar los avances en la traducci´ on autom´ atica neuronal (NMT), un paradigma basado en redes neuronales profundas que aprende a traducir directamente secuencias de texto de un idioma a otro.


<!-- page 11 -->

Sin embargo, este enfoque introduce un cuello de botella informativo [7]. Las glosas son representaciones simplificadas que no capturan toda la riqueza gramatical y sem´ antica de la lengua de se˜ nas. Por lo tanto, basar el proceso de traducci´ on ´ unicamente en glosas puede limitar la calidad del resultado final, ya que parte del contenido del mensaje original se puede perder. Es por esto que l´ ıneas de investigaci´ on m´ as recientes han propuesto modelos capaces de aprender directamente desde las caracter´ ısticas visuales de los videos, evitando esta dependencia y abriendo la puerta a enfoques m´ as fieles y escalables [7] [10].

## 2.2.2. Enfoque gloss-free

El enfoque gloss-free, tambi´ en conocido como enfoque end-to-end, plantea una soluci´ on m´ as ambiciosa: eliminar por completo la etapa intermedia de reconocimiento de glosas, y entrenar un modelo que aprenda a traducir directamente de los datos visuales del video a una oraci´ on en lenguaje natural. Este tipo de modelos recibe como entrada una secuencia de video (ya sea en forma de frames RGB, secuencias de poses, keypoints o embeddings visuales), y produce como salida una secuencia de texto, sin necesidad de pasar por una transcripci´ on intermedia de glosas.

A nivel t´ ecnico, esto se logra utilizando arquitecturas encoder-decoder, en las que: el encoder visual toma la secuencia de entrada (por ejemplo, los vectores de poses o frames del video), y la transforma en una representaci´ on latente 4 de alto nivel que condensa la informaci´ on visual y temporal. Luego, el decoder textual recibe esa representaci´ on latente y genera palabra por palabra la oraci´ on en lenguaje natural correspondiente.

Los modelos gloss-free representan un cambio de paradigma, alineado con las tendencias actuales en aprendizaje profundo. En particular, el uso de transformers ha permitido avanzar significativamente en esta direcci´ on. Las ventajas de este enfoque son: aprovecha toda la informaci´ on visual disponible, ya que al no filtrar el video mediante glosas, el modelo puede aprender directamente patrones de ´ enfasis, articulaci´ on y matices sem´ anticos que las glosas no capturan. Tambi´ en, elimina acumular errores que puedan afectar a etapas posteriores ya que el modelo hace la traducci´ on directa. Por otro lado, evita realizar anotaciones de glosas, por lo que se puede trabajar con datos anotados con oraciones completas en lenguaje oral. Por ´ ultimo, mejora la generalizaci´ on, ya que en algunos estudios (por ejemplo, Camgoz et al. 2020) han demostrado que los modelos pueden lograr mejor rendimiento que sus contrapartes gloss-based en tareas de traducci´ on continua. De todas maneras, este enfoque requiere m´ as datos y potencia de c´ omputo, lo cual no es f´ acil de conseguir.

4 Es un vector num´ erico que codifica la informaci´ on esencial de una entrada (por ejemplo, una secuencia de palabras o frames) dentro de un espacio continuo de alta dimensi´ on.


<!-- page 12 -->

En el caso de la Lengua de Se˜ nas Argentina, el enfoque gloss-free ofrece una ventaja significativa, dado que no existe un conjunto de datos que contenga se˜ nas etiquetadas con glosas. [4]. Es m´ as factible desarrollar modelos que traduzcan directamente desde los datos visuales, aprovechando conjuntos como LSA-T, que ya ofrecen traducciones completas de video a texto.

## 2.3. La Lengua de Se˜ nas Argentina

La Lengua de Se˜ nas Argentina es la lengua natural utilizada por la comunidad sorda en Argentina. Al igual que otras lenguas de se˜ nas del mundo, la LSA se construye mediante la combinaci´ on simult´ anea de configuraciones de manos, movimientos, ubicaci´ on en el espacio, expresiones faciales y postura corporal. Reci´ en en 2023 fue reconocida oficialmente como lengua natural en nuestro pa´ ıs, a trav´ es de la Ley N. º 27.710.

La LSA posee una sintaxis diferente a la del espa˜ nol. Mientras que el orden t´ ıpico en espa˜ nol es sujeto-verbo-objeto, en LSA predomina el orden sujeto-objeto-verbo. Adem´ as, las oraciones interrogativas se expresan marcando el signo de pregunta al final, y no existen art´ ıculos ni sujeto t´ acito, lo que implica diferencias importantes en la estructura de las frases.

A pesar de la escasez hist´ orica de recursos anotados y del limitado desarrollo de herramientas tecnol´ ogicas espec´ ıficas para LSA, en los ´ ultimos a˜ nos se han publicado conjuntos de datos clave como LSA64 (que contiene signos aislados) y LSA-T (que incluye secuencias continuas y traducciones completas). Estos recursos abrieron la posibilidad de aplicar modelos de traducci´ on directa (gloss-free), sin necesidad de representaciones intermedias en forma de glosas.

## 2.3.1. LSA64

LSA64 es el primer conjunto de datos p´ ublico creado espec´ ıficamente para tareas de reconocimiento autom´ atico de la Lengua de Se˜ nas Argentina [11]. Fue desarrollado por investigadores del Instituto LIDI de la Universidad Nacional de La Plata (Ronchetti et al., 2023) y contiene 3200 videos correspondientes a 64 signos diferentes, realizados por 10 personas distintas. Cada persona repiti´ o cada signo cinco veces. Los signos seleccionados son parte del vocabulario m´ as com´ un de la LSA, e incluyen tanto sustantivos como verbos.


<!-- page 13 -->

Los videos en el conjunto de datos fueron grabados en dos etapas. En la primera se registraron 23 signos realizados con una sola mano, filmados en exteriores con luz natural. En la segunda etapa se agregaron 41 signos nuevos (22 bimanuales y 19 unimanuales), filmados en interiores con luz artificial. En ambas grabaciones, las personas usaron guantes de colores diferentes para cada mano y ropa oscura, sobre un fondo blanco. Esto ayud´ o a facilitar la detecci´ on y segmentaci´ on de las manos en los videos.

Si bien LSA64 est´ a pensado para tareas de reconocimiento de signos aislados y no para traducci´ on de oraciones completas, presenta una buena variedad en formas de manos, posiciones iniciales y finales, y trayectorias. Esto lo hace ´ util para entrenar que buscan reconocer se˜ nas individuales.

## 2.3.2. LSA-T

LSA-T, por su parte, es el primer conjunto de datos p´ ublico con secuencias continuas en LSA (Dal Bianco et al., 2022). Fue desarrollado por investigadores del Instituto LIDI de la Universidad Nacional de La Plata, en colaboraci´ on con otras instituciones vinculadas al procesamiento del lenguaje. El corpus se construy´ o a partir de videos extra´ ıdos del canal de YouTube CN Sordos, un medio conducido por personas sordas que transmite noticias en LSA. En total, el conjunto disponible contiene clips con subt´ ıtulos en espa˜ nol. Cada muestra tiene tambi´ en anotaciones de puntos clave (keypoints) del cuerpo y las manos obtenidas con MediaPipe (originalmente, se obtuvieron con AlphaPose, luego se actualiz´ o el conjunto de datos [12]), lo que permite entrenar modelos que usen solo la informaci´ on visual del movimiento.

Una de las principales ventajas de LSA-T es que fue generado en condiciones reales, lo que significa que los videos tienen distintos fondos, iluminaci´ on, y variedad de personas y temas. Esto lo vuelve un desaf´ ıo interesante para los modelos autom´ aticos. Algo a notar es que LSA-T no contiene glosas intermedias, por lo que es un muy buen candidato para probar modelos gloss-free. En las pr´ oximas secci´ on vamos a ver m´ as en detalle c´ omo est´ a construido y c´ omo se aplica en modelos tradicionales y en modelos m´ as avanzados.


<!-- page 14 -->

## 3. Visi´ on por Computadora

## 3.1. ¿Qu´ e es computer vision o visi´ on por computadora?

La visi´ on por computadora (computer vision) es una rama de la inteligencia artificial que busca dotar a las m´ aquinas de la capacidad de 'ver' y comprender el mundo visual que las rodea a partir de im´ agenes o secuencias de video, con el objetivo de interpretar esa informaci´ on para extraer significado, identificar patrones y, en ´ ultima instancia, facilitar la toma de decisiones autom´ aticas basadas en lo que se observa.

En los seres humanos, el sistema visual es producto de millones de a˜ nos de evoluci´ on y a˜ nos de aprendizaje individual, lo que nos permite reconocer objetos, estimar distancias, percibir formas tridimensionales y comprender interacciones complejas de manera casi instant´ anea. En cambio, para una computadora, una imagen no es m´ as que una matriz de n´ umeros. En una imagen RGB, por ejemplo, cada p´ ıxel est´ a representado por tres valores que codifican la intensidad de los colores rojo, verde y azul. A partir de esa informaci´ on cruda, un sistema de visi´ on debe deducir propiedades como la forma, el color, la iluminaci´ on, la ubicaci´ on de objetos o su movimiento.

La dificultad de esta tarea radica en que se trata de un problema inverso: a partir de proyecciones bidimensionales incompletas y afectadas por ruido, el sistema debe inferir caracter´ ısticas tridimensionales y sem´ anticas del mundo real. Este proceso requiere modelos f´ ısicos (´ optica, geometr´ ıa, radiometr´ ıa) combinados con t´ ecnicas estad´ ısticas y de aprendizaje autom´ atico que permitan desambiguar entre m´ ultiples interpretaciones posibles [13].

Gracias a los avances en aprendizaje profundo, el incremento del poder computacional (especialmente con el uso de GPUs) y la disponibilidad de grandes conjuntos de datos, la visi´ on por computadora ha experimentado un desarrollo acelerado en las ´ ultimas dos d´ ecadas. Actualmente es una tecnolog´ ıa presente en una amplia gama de aplicaciones: desde la conducci´ on aut´ onoma y la inspecci´ on industrial, hasta la medicina, la rob´ otica, la seguridad y, en el contexto de esta tesis, la traducci´ on autom´ atica de lenguas de se˜ nas.

## 3.2. Aplicaciones generales de la visi´ on por computadora

La visi´ on por computadora ha demostrado ser una tecnolog´ ıa transversal con aplicaciones en numerosos campos. En el ´ ambito del transporte, por ejemplo, es fundamental para el reconocimiento de objetos y la interpretaci´ on del entorno en sistemas de conducci´ on aut´ onoma [14]. En seguridad y vigilancia, se emplea para la detecci´ on autom´ atica de intrusiones, la identificaci´ on biom´ etrica y el an´ alisis de comportamientos en espacios p´ ublicos [15]. En medicina, se utiliza en la segmentaci´ on de im´ agenes diagn´ osticas, en la detecci´ on temprana de enfermedades y en la asistencia a procedimientos quir´ urgicos [16]. La industria manufacturera la aplica en control de calidad para identificar defectos en productos de forma autom´ atica [17]. En el ´ ambito del entretenimiento y la realidad aumentada, permite integrar objetos virtuales en escenas reales, as´ ı como capturar y reproducir movimientos humanos con alta fidelidad [18].


<!-- page 15 -->

## 3.3. ¿C´ omo se representa una imagen?

En el contexto de la visi´ on por computadora, una imagen puede definirse formalmente como una funci´ on bidimensional F ( X,Y ), donde X y Y representan coordenadas espaciales y el valor de la funci´ on en cada par ( x i , y i ) corresponde a la intensidad luminosa en ese punto. En una imagen en escala de grises, esta intensidad describe el nivel de luminosidad, mientras que en una imagen a color existen m´ ultiples funciones (o canales), cada una asociada a un componente crom´ atico seg´ un un modelo determinado, como RGB (rojo, verde, azul) HSV (tono, saturaci´ on, valor) o escala de grises.

En su forma digital, las im´ agenes se almacenan como matrices de valores num´ ericos, donde cada elemento representa un p´ ıxel. La resoluci´ on de una imagen est´ a determinada por el n´ umero total de p´ ıxeles y la profundidad de color, que especifica el rango de valores posibles para cada canal. Por ejemplo, en una imagen RGB de 8 bits por canal, cada componente de color puede tomar un valor entre 0 y 255, lo que permite representar m´ as de 16 millones de combinaciones crom´ aticas. En la figura 2 podemos observar un ejemplo de la representaci´ on en p´ ıxeles de una imagen RGB.

Si tuvi´ eramos una imagen en escala de grises, como la de la figura de aqu´ ı abajo, esta se representar´ ıa como una matriz bidimensional de enteros en el rango de 0 a 255, donde cada valor indica la intensidad luminosa en ese p´ ıxel. Un valor 0 corresponde a negro absoluto, mientras que 255 representa blanco puro, y los valores intermedios distintos tonos de gris.

Por otro lado, en el caso del espacio de color HSV, los canales corresponden a Hue (tono), Saturation (saturaci´ on) y Value (valor o brillo), donde Hue representa el matiz o tipo de color percibido (rojo, verde, azul, etc.) y suele expresarse como un ´ angulo en un c´ ırculo crom´ atico, normalmente en el rango de 0 ° a 360 ° , donde, por ejemplo, 0 ° corresponde al rojo, 120 ° al verde y 240 ° al azul. Saturation indica la 'pureza' o intensidad del color, medida como un porcentaje: un valor de 0 % corresponde a un tono completamente desaturado (gris), mientras que 100 % representa un color puro y sin mezcla con el blanco o el negro. Y por ´ ultimo Value describe el brillo del color, tambi´ en en porcentaje: 0 % es completamente negro, y 100 % es el color en su m´ axima luminosidad. Podemos ver una representaci´ on de este espacio de color en la figura 4.


<!-- page 16 -->

Figura 2: Representaci´ on de la imagen RGB de una manzana en p´ ıxeles. (A) Imagen original, (B) Imagen con zoom sobre (A), (C) Valores de los p´ ıxeles en (B)

<!-- image -->

Figura 3: Imagen proveniente de https://bioimagebook.github.io/ chapters/1-concepts/1-images\_and\_pixels/images\_and\_pixels.html . (A) Imagen original, (B) Imagen con zoom sobre (A), (C) Valores de los p´ ıxeles en (B)

<!-- image -->


<!-- page 17 -->

Figura 4: Imagen proveniente de https://www.mathworks.com/help/ images/understanding-color-spaces-and-color-space-conversion. html

<!-- image -->

A su vez, aunque el caso m´ as habitual es el de im´ agenes bidimensionales, existen representaciones m´ as complejas. Las im´ agenes volum´ etricas o tridimensionales se modelan como F ( X,Y,Z ) y est´ an compuestas por v´ oxeles (volume elements), empleados en aplicaciones como la tomograf´ ıa o la resonancia magn´ etica. Asimismo, cuando la dimensi´ on temporal es relevante, como en secuencias de video, la funci´ on se extiende a F ( X,Y,T ), incorporando la variaci´ on visual a lo largo del tiempo.

Esta representaci´ on matricial facilita el procesamiento computacional, ya que permite aplicar operaciones algebraicas, filtrados y convoluciones 5 para extraer informaci´ on relevante. En algunos casos, las im´ agenes tambi´ en se representan como grafos, en los que cada nodo corresponde a un p´ ıxel y las aristas conectan p´ ıxeles vecinos, lo que habilita el uso de algoritmos propios de la teor´ ıa de grafos para su an´ alisis. Independientemente del modelo empleado, todas estas representaciones comparten un aspecto esencial: las im´ agenes son datos estructurados con una fuerte correlaci´ on espacial, cuya correcta interpretaci´ on es la base de cualquier sistema de visi´ on por computadora.

5 Una convoluci´ on es una operaci´ on matem´ atica que combina una funci´ on (por ejemplo, una imagen o secuencia de datos) con un filtro o kernel que se desliza sobre ella, produciendo una nueva representaci´ on que resalta patrones locales como bordes, texturas o movimientos


<!-- page 18 -->

## 3.4. Preprocesamiento previo a la extracci´ on de caracter´ ısticas

El preprocesamiento de im´ agenes constituye un conjunto de operaciones dise˜ nadas para optimizar la calidad y la utilidad de los datos antes de su uso en modelos de visi´ on por computadora. Estas operaciones no solo mejoran la calidad, sino que tambi´ en transforman las im´ agenes para facilitar el an´ alisis, la extracci´ on de caracter´ ısticas y el aprendizaje autom´ atico [19]. Las operaciones que pueden aplicarse a una imagen se clasifican com´ unmente en:

- L´ ogicas : Modifican la estructura de la imagen bas´ andose en relaciones entre p´ ıxeles, especialmente en im´ agenes binarias 6 . Sirve para comparar im´ agenes y realizar c´ alculos. En la figura 5 podemos ver las distintas operaciones l´ ogicas conocidas AND, OR, XOR y NOT aplicadas sobre dos im´ agenes binarias.
- Geom´ etricas : son operaciones que modifican la posici´ on de los p´ ıxeles en una imagen. Se realizan en dos pasos, en primer lugar se realiza una transformaci´ on espacial de las coordenadas de los p´ ıxeles. Luego,

Figura 5: A y B son la representaci´ on en matrices de im´ agenes en la escala de grises. Las operaciones l´ ogicas AND, OR, XOR y NOT se aplican pixel a pixel.

<!-- image -->

6 Las im´ agenes binarias son im´ agenes que tienen ´ unicamente dos valores posibles para cada pixel: 0 (negro) o 1 (blanco).


<!-- page 19 -->

Figura 6: Ilustraci´ on de operaciones geom´ etricas sobre una imagen.

<!-- image -->

se hace una interpolaci´ on de intensidades para asignar el valor de intensidad despu´ es del cambio de posici´ on. En este proceso, un p´ ıxel con coordenadas ( x, y ) en la imagen original pasa a ( x ′ , y ′ ) en la imagen transformada, conservando su intensidad original. Esto se modela mediante una matriz de transformaci´ on T :

<!-- formula-not-decoded -->

donde [ x y ] es la posici´ on del pixel ( x, y ) modelada como matriz. Por ejemplo, en una traslaci´ on, se desplazan todos los ´ ıxeles una cantidad fija ∆ x y ∆ y , sin cambiar forma ni tama˜ no:

<!-- formula-not-decoded -->

Por otro lado, en una rotaci´ on, la imagen se gira un ´ angulo θ respecto al origen o al centro:

<!-- formula-not-decoded -->

En la figura 6 se ilustran las operaciones geom´ etricas m´ as comunes.


<!-- page 20 -->

- Matem´ aticas : abarcan operaciones elemento a elemento (por ejemplo, dividir dos im´ agenes p´ ıxel a p´ ıxel) y operaciones matriciales basadas en ´ algebra lineal. [20]

Tambi´ en tenemos otros conceptos matem´ aticos fundamentales como teor´ ıa de conjuntos la cual es especialmente ´ util en im´ agenes binarias, donde los p´ ıxeles se clasifican como primer plano (1) o fondo (0) y permite aplicar operaciones como uni´ on, intersecci´ on y diferencia sobre regiones de inter´ es, y tambi´ en tenemos los conocidos filtrados espaciales que se explican a continuaci´ on.

## 3.4.1. Filtrados especiales y kernels

En procesamiento digital de im´ agenes, un kernel es una peque˜ na matriz de n´ umeros que se utiliza para modificar los valores de los p´ ıxeles de una imagen en funci´ on de sus vecinos. Generalmente, los kernels son cuadrados de tama˜ no reducido, como 3 × 3, 5 × 5 o 7 × 7, aunque pueden tener otras dimensiones. Estos kernels se pueden utilizar sobre una imagen para realizar convoluciones o correlaciones. La idea consiste en desplazar el kernel sobre cada p´ ıxel de la imagen y calcular una suma ponderada entre los valores de la regi´ on cubierta por el kernel y los valores del propio kernel.

- En convoluci´ on cl´ asica, el kernel se rota 180 ° antes de aplicarse.
- En correlaci´ on, el kernel se aplica directamente, sin rotaci´ on.

Luego, cuando aplicamos un kernel mediante convoluci´ on/correlaci´ on sobre toda la imagen, obtenemos un filtro espacial. El resultado depende de los valores del kernel: si los valores promueven el promedio de los p´ ıxeles vecinos, el filtro act´ ua como un suavizado (reducci´ on de ruido). Si los valores resaltan diferencias locales, el filtro act´ ua como un detector de bordes o realce de detalles. Otros kernels permiten efectos como desenfoque, enfoque, eliminaci´ on de patrones, entre otros.

En s´ ıntesis, el filtrado espacial transforma la informaci´ on de la imagen a nivel local, permitiendo modificar sus caracter´ ısticas visuales o extraer informaci´ on relevante para etapas posteriores de an´ alisis. Formalmente, si f ( x, y ) es la imagen original y g es el kernel de tama˜ no m × n , la convoluci´ on se define como:

<!-- formula-not-decoded -->


<!-- page 21 -->

Figura 7: Ejemplo de operaci´ on de convoluci´ on entre un kernel de realce (sharpening) y una regi´ on de imagen. El resultado depende del contraste entre el p´ ıxel central y sus vecinos: si el centro es m´ as brillante, la salida es positiva (resaltado); si es m´ as oscuro, la salida es negativa.

<!-- image -->

que reemplaza cada p´ ıxel por el promedio de sus vecinos inmediatos. En la figura 7 se ilustra el resultado de aplicar un kernel en distintas imagenes.

Proceso de filtrado espacial . El filtrado espacial consiste en aplicar un kernel sobre la imagen siguiendo estos pasos:

1. Se coloca el kernel sobre la regi´ on de la imagen centrada en el p´ ıxel de inter´ es.
2. Se multiplica cada valor del kernel por el valor del p´ ıxel correspondiente.
3. Se suman los resultados y, en algunos casos, se normalizan (por ejemplo, dividiendo entre la suma de los coeficientes del kernel).
4. El valor resultante reemplaza al p´ ıxel original en la imagen de salida.

En la figura 8 se tiene un ejemplo de este proceso.

Algunos ejemplos pr´ acticos de los kernels utilizados en filtrados espaciales incluyen los filtros para reducir el ruido en una imagen satelital, los filtros para detectar bordes en una radiograf´ ıa y los filtros destinados a cambiar la nitidez de una fotograf´ ıa desenfocada mediante t´ ecnicas de realce (sharpening).


<!-- page 22 -->

Figura 8: Esquema de la operaci´ on de convoluci´ on 2D. El kernel se desplaza sobre la imagen de entrada, multiplicando sus valores con la regi´ on correspondiente (en azul) y sumando los resultados para generar un valor en la posici´ on correspondiente del mapa de salida (en rojo).

<!-- image -->

## 3.4.2. Data Augmentation

El aumento de datos es fundamental para mejorar la robustez y la capacidad de generalizaci´ on de modelos, en especial redes neuronales convolucionales. Consiste en ampliar artificialmente el conjunto de entrenamiento mediante:

- Transformaciones : utilizando las operaciones vistas de rotaciones, traslaciones, escalados, volteos, recortes, ajustes de brillo, contraste, saturaci´ on y cambios de espacio de color.
- Adici´ on de ruido sint´ etico : se modifica la imagen con distorsiones controlados simulando imperfecciones que pueden aparecer en escenarios reales.


<!-- page 23 -->

- Generaci´ on de datos sint´ eticos : mediante redes generativas u otros modelos generativos.

Si bien su uso m´ as com´ un es en im´ agenes, tambi´ en se aplica a otros tipos de datos como audio (inyecci´ on de ruido, cambio de tono) o texto (reordenamiento de palabras, manipulaci´ on sint´ actica). En visi´ on por computadora, adem´ as de incrementar el tama˜ no efectivo del conjunto de entrenamiento, tambi´ en introduce variabilidad, reduciendo el riesgo de sobreajuste y mejorando la adaptaci´ on del modelo a escenarios reales. Estas operaciones preparan las im´ agenes para que la etapa de extracci´ on de caracter´ ısticas pueda trabajar sobre datos limpios, normalizados y estructurados. El preprocesamiento no solo mejora la calidad visual, sino que transforma la informaci´ on de manera que patrones importantes se destaquen, reduciendo ruido, corrigiendo variaciones de iluminaci´ on o perspectiva, y facilitando la detecci´ on de elementos clave en la imagen.

## 3.5. Extracci´ on de caracter´ ısticas en im´ agenes

La extracci´ on de caracter´ ısticas es una de las etapas m´ as importantes en el procesamiento de im´ agenes dentro de la visi´ on por computadora. Su objetivo principal es transformar la informaci´ on visual en representaciones compactas, discriminativas y robustas que los algoritmos puedan analizar, comparar y clasificar de manera eficiente. Esta transformaci´ on es esencial: sin caracter´ ısticas adecuadas, incluso los modelos m´ as sofisticados no podr´ ıan interpretar correctamente la informaci´ on contenida en una imagen.

## 3.5.1. M´ etodos cl´ asicos de extracci´ on de caracter´ ısticas

Antes del auge del aprendizaje profundo, la extracci´ on de caracter´ ısticas depend´ ıa de t´ ecnicas dise˜ nadas manualmente. Estos m´ etodos buscaban (aunque hasta el d´ ıa de hoy a´ un se utilizan) identificar patrones visuales relevantes para tareas espec´ ıficas, como bordes, esquinas, texturas o puntos clave (o tambi´ en en ingl´ es keypoints). A estos m´ etodos tambi´ en se los suele llamar descriptores de caracter´ ısticas. Entre los m´ as utilizados se encuentran:

- SIFT (Scale-Invariant Feature Transform) : detecta puntos clave invariantes ante cambios de escala y rotaci´ on, localiza estos puntos con precisi´ on subp´ ıxel 7 , asigna orientaciones dominantes basadas en gradientes locales y genera descriptores, es decir, representaciones num´ ericas compactas que describen el entorno visual local alrededor de cada

7 Un subp´ ıxel se refiere a una posici´ on estimada con precisi´ on superior al tama˜ no de un p´ ıxel individual


<!-- page 24 -->

punto clave, lo que permite su emparejamiento entre im´ agenes [21]. Es ´ util cuando por ejemplo, queremos reconocer un edificio en fotos tomadas con distintas c´ amaras, ´ angulos o tama˜ nos.

- HOG (Histogram of Oriented Gradients) : describe regiones de la imagen mediante histogramas de gradientes orientados, capturando la estructura local. Es decir, en lugar de buscar puntos concretos, se fija en c´ omo est´ an distribuidos los bordes y direcciones de las l´ ıneas en una imagen [22]. Es especialmente eficaz en detecci´ on de personas y objetos con contornos definidos.
- SURF (Speeded-Up Robust Features) : Es un m´ etodo similar a SIFT pero m´ as r´ apido. Tambi´ en busca puntos importantes en una imagen y los describe, pero utiliza m´ etodos matem´ aticos que son mas eficientes [23].

Los descriptores generados por estas t´ ecnicas deben cumplir propiedades esenciales: invariancia ante transformaciones geom´ etricas (rotaci´ on, traslaci´ on, escalado), robustez frente a ruido o variaciones de iluminaci´ on, capacidad de discriminaci´ on entre objetos distintos, y eficiencia computacional para permitir su uso en sistemas de visi´ on en tiempo real.

## 3.5.2. Representaci´ on de las caracter´ ısticas

Dependiendo de su naturaleza y complejidad, las caracter´ ısticas extra´ ıdas pueden almacenarse de distintas formas [24]:

- Vectores o arreglos para almacenar valores num´ ericos simples, donde cada posici´ on corresponde a una caracter´ ıstica.
- Tensores multidimensionales cuando se trabaja con grandes vol´ umenes de datos o m´ ultiples canales, como ocurre en redes neuronales convolucionales.
- Matrices de valores de p´ ıxeles para representar directamente im´ agenes a nivel de intensidades, colores o bordes.
- Vectores binarios en representaciones categ´ oricas mediante one-hot encoding.

## 3.6. Modelos tradicionales

Una vez obtenidas las caracter´ ısticas relevantes de las im´ agenes, el siguiente paso consiste en utilizarlas junto con algoritmos de modelado. Este proceso implica dise˜ nar, entrenar y evaluar modelos capaces de aprender patrones a partir de los descriptores o caracter´ ısticas extra´ ıdas, con el fin de resolver tareas espec´ ıficas como clasificaci´ on, detecci´ on de objetos, segmentaci´ on sem´ antica o reconocimiento de escenas.


<!-- page 25 -->

Regresi´ on log´ ıstica y m´ aquinas lineales. La regresi´ on log´ ıstica representa uno de los enfoques m´ as utilizados para problemas de clasificaci´ on binaria. Su simplicidad radica en asumir que la frontera de decisi´ on puede aproximarse mediante un hiperplano en el espacio de caracter´ ısticas, lo cual permite modelar probabil´ ısticamente la pertenencia de una muestra a una clase. En este tipo de modelos, lo que se realiza es utilizar la representaci´ on de las caracter´ ısticas de una imagen para entrenar un modelo de regresi´ on log´ ıstica cl´ asico y determinar si cierta imagen contiene (por ejemplo) un gato o no [25].

M´ aquinas de soporte vectorial. Las m´ aquinas de soporte vectorial (SVM) constituyen un avance fundamental al introducir el concepto de m´ argenes m´ aximos. A diferencia de los clasificadores puramente lineales, las SVM buscan la frontera que no solo separa las clases, sino que lo hace maximizando la distancia entre los ejemplos m´ as cercanos de cada categor´ ıa. El uso de funciones kernel permite adem´ as mapear los datos a espacios de mayor dimensionalidad, capturando relaciones no lineales sin necesidad de un dise˜ no expl´ ıcito de caracter´ ısticas [26].

´ Arboles de decisi´ on y m´ etodos de ensamble. Los ´ arboles de decisi´ on ofrecen un enfoque jer´ arquico en el que los datos se dividen recursivamente de acuerdo con criterios de pureza (pertenencia a una clase por dem´ as de las otras). Aunque individuales pueden ser inestables y propensos al sobreajuste, su interpretabilidad los convierte en una herramienta importante. Este problema se mitig´ o con la aparici´ on de m´ etodos de ensamble como Random Forests y Gradient Boosting, los cuales combinan m´ ultiples ´ arboles para lograr predicciones m´ as robustas y precisas [27].

K-vecinos m´ as cercanos. El algoritmo de K-vecinos m´ as cercanos (KNN) se basa en la idea intuitiva de que instancias similares deben compartir etiquetas 8 similares. En este caso, la predicci´ on se obtiene considerando la mayor´ ıa de las etiquetas entre los vecinos m´ as pr´ oximos en el espacio de caracter´ ısticas. Su eficiencia depende fuertemente de la representaci´ on de las caracter´ ısticas y del tama˜ no del conjunto de datos [28].

8 Si se est´ an clasificando im´ agenes de animales, cada imagen tiene una etiqueta que indica su clase: 'gato', 'perro', 'conejo', etc


<!-- page 26 -->

## 3.7. Aprendizaje profundo: cambio de paradigma

El surgimiento del aprendizaje profundo (deep learning) transform´ o el campo de la visi´ on por computadora, desplazando en gran medida los enfoques basados en extracci´ on manual de caracter´ ısticas y modelos tradicionales de machine learning. A diferencia de los m´ etodos cl´ asicos, que dependen de descriptores dise˜ nados a mano y de reglas heur´ ısticas, gracias a las redes profundas es posible aprender autom´ aticamente representaciones de los datos, identificando patrones complejos y abstractos directamente a partir de im´ agenes o secuencias de video. Este cambio de paradigma permiti´ o avances significativos en tareas como clasificaci´ on, segmentaci´ on, detecci´ on de objetos y, en el contexto de esta tesis, la traducci´ on autom´ atica de la lengua de se˜ nas, al ofrecer modelos capaces de capturar tanto caracter´ ısticas espaciales locales como dependencias temporales y contextuales en los datos visuales.

## 3.7.1. Redes neuronales

Las redes neuronales artificiales constituyen uno de los pilares fundamentales del aprendizaje autom´ atico moderno y, en particular, del aprendizaje profundo. Inspiradas en la estructura y funcionamiento del cerebro humano, estas arquitecturas computacionales se dise˜ nan para aprender representaciones complejas de datos mediante el ajuste iterativo de par´ ametros internos (pesos y sesgos). Las mismas se convirtieron en una herramienta esencial en visi´ on por computadora, procesamiento del lenguaje natural, reconocimiento de voz y tambi´ en, en el contexto de este trabajo, la traducci´ on autom´ atica de la lengua de se˜ nas. Una red neuronal t´ ıpica se organiza en tres componentes principales: la capa de entrada, una serie de capas ocultas, y la capa de salida. Veamos en detalle c´ omo se conforma una red neuronal.

## Neuronas

La unidad fundamental de una red neuronal es la neurona artificial. Una neurona recibe se˜ nales de entrada (valores num´ ericos) en forma de vector ⃗ x = ( x 1 , x 2 , ..., x n ), cada una ponderada por un peso w i que determina su importancia relativa. Luego, estas entradas ponderadas se suman, se a˜ nade un sesgo b que permite desplazar la salida, y el resultado se pasa por una funci´ on de activaci´ on que introduce no linealidad al sistema. Matem´ aticamente, la operaci´ on b´ asica de una neurona puede expresarse como:

<!-- formula-not-decoded -->


<!-- page 27 -->

donde al valor z luego se le aplica una funci´ on de activaci´ on no lineal g ( z ) para producir la salida. En la figura 9 se ilustra este proceso.

Figura 9: Pasaje de un vector ⃗ x = ( x 1 , x 2 , ..., x n ) por medio de una neurona artificial.

<!-- image -->

Esta operaci´ on convierte a la neurona en un transformador de informaci´ on. Hablaremos sobre las funciones de activaci´ on m´ as adelante.

## Capas

Las neuronas se organizan en capas, que definen la arquitectura de la red. Una capa es un conjunto de neuronas que procesan informaci´ on de manera paralela. Existen tres tipos fundamentales:

- Capa de entrada: recibe los datos (por ejemplo, pixeles de una imagen o caracter´ ısticas num´ ericas) en forma de vector.
- Capas ocultas: se encuentran entre la entrada y la salida, y su funci´ on es extraer representaciones cada vez m´ as abstractas y complejas de los datos. La cantidad de capas ocultas puede variar dependiendo la arquitectura
- Capa de salida: produce el resultado final, que puede ser una clasificaci´ on, un valor num´ erico en un problema de regresi´ on, o probabilidades en un problema de decisi´ on.


<!-- page 28 -->

La profundidad y complejidad de una red dependen del n´ umero de capas ocultas y del n´ umero de neuronas por capa, lo que da lugar a arquitecturas simples o a modelos de deep learning cuando estas capas son numerosas.

## Red

Una red neuronal artificial es el conjunto completo de capas y sus interconexiones. Su estructura puede variar desde redes feed-forward, donde la informaci´ on fluye ´ unicamente desde la entrada hacia la salida (sin retroalimentaciones), hasta arquitecturas m´ as especializadas como las redes convolucionales o recurrentes. Dentro de las redes feed-forward, las m´ as comunes son las fully connected (o tambi´ en llamadas densas), en las que cada neurona de una capa est´ a conectada con todas las de la siguiente. La topolog´ ıa de la red determina c´ omo fluye la informaci´ on y es un factor decisivo en su capacidad para resolver distintos tipos de problemas. En la figura 10 podemos observar una red neuronal fully connected, que a su vez es una red feed-forward.

Figura 10: Red neuronal fully connected y feed-forward.

<!-- image -->

## Pesos (weights) y sesgos (bias)

Los pesos y sesgos son los par´ ametros que la red debe aprender durante el entrenamiento. Los pesos definen la influencia que tiene cada entrada sobre una neurona, mientras que los sesgos permiten ajustar la salida independientemente de las entradas, otorgando flexibilidad al modelo. Juntos, constituyen la base del aprendizaje, ya que al modificarse permiten que la red se adapte a los datos y capture patrones relevantes. En t´ erminos pr´ acticos, el entrenamiento consiste en encontrar el conjunto ´ optimo de pesos y sesgos que minimice el error entre la salida deseada y la salida producida por la red. Hablaremos sobre esta minimizaci´ on del error en breves.


<!-- page 29 -->

## Funciones de activaci´ on

Las funciones de activaci´ on determinan la salida de una neurona tras el c´ alculo de la suma ponderada de sus entradas. Su funci´ on es introducir no linealidad, permitiendo que la red neuronal modele relaciones complejas en los datos. Entre las m´ as utilizadas se encuentran:

- Sigmoide , que mapea valores a un rango entre 0 y 1. Podemos denotarla con la siguiente f´ ormula:

<!-- formula-not-decoded -->

- ReLU (Rectified Linear Unit) , que devuelve 0 para valores negativos y el valor original para positivos, favoreciendo el entrenamiento en redes profundas. Podemos denotarla con la siguiente f´ ormula:

<!-- formula-not-decoded -->

- Softmax , utilizada en la capa de salida para problemas de clasificaci´ on multiclase, ya que normaliza las salidas como probabilidades. Su f´ ormula matem´ atica es la siguiente:

<!-- formula-not-decoded -->

donde z = ( z 1 , z 2 , ..., z K ) es un vector de entrada.

En particular, ∑ K i =1 softmax ( z i ) = 1.

La elecci´ on de la funci´ on de activaci´ on influye en la velocidad y estabilidad del aprendizaje, as´ ı como en la capacidad de la red para aproximar funciones.

## Funci´ on de p´ erdida (loss function)

La funci´ on de p´ erdida (Loss Function) cuantifica el error entre las predicciones de la red y los valores reales. Su papel es fundamental, ya que gu´ ıa el proceso de aprendizaje al proporcionar una medida que debe minimizarse. Existen diferentes funciones de p´ erdida seg´ un el tipo de tarea: la entrop´ ıa cruzada para clasificaci´ on, el error cuadr´ atico medio (MSE) para regresi´ on, entre otras.


<!-- page 30 -->

En esta secci´ on basta con entender que la funci´ on de p´ erdida indica qu´ e tan equivocada est´ a la red y que su valor se reduce progresivamente a medida que el modelo aprende. En secciones posteriores, al describir arquitecturas espec´ ıficas como Transformers o modelos de traducci´ on autom´ atica, se retomar´ a la entrop´ ıa cruzada con mayor detalle.

## Propagaci´ on hacia adelante (Forward Propagation)

La propagaci´ on hacia adelante (forward propagation) es el proceso mediante el cual una entrada inicial se transmite a trav´ es de todas las capas de la red hasta producir una salida final. En cada capa, las neuronas calculan la combinaci´ on ponderada de las entradas, aplican la funci´ on de activaci´ on correspondiente y generan salidas que se convierten en las entradas de la capa siguiente. Este proceso culmina en la predicci´ on de la red.

## Retropropagaci´ on (Backpropagation)

La retropropagaci´ on constituye el mecanismo de aprendizaje en las redes neuronales. Una vez calculado el error mediante la funci´ on de p´ erdida elegida, este se propaga hacia atr´ as desde la capa de salida hasta las capas iniciales. Durante este proceso, se aplican las reglas del c´ alculo diferencial, especialmente la regla de la cadena, para determinar c´ omo cambia el error ante peque˜ nas variaciones de cada par´ ametro. El resultado de este an´ alisis son los gradientes, es decir, los vectores que indican la direcci´ on y magnitud del cambio necesario en cada peso y sesgo para reducir la p´ erdida [29]. Estos gradientes se combinan luego con un optimizador, como el descenso por gradiente estoc´ astico (SGD) o algoritmos m´ as avanzados como Adam/AdamW, que los utiliza para ajustar los par´ ametros del modelo de forma iterativa, disminuyendo progresivamente el error y estabilizando el aprendizaje.

## Proceso de aprendizaje

En resumen, el aprendizaje en una red neuronal consiste en ajustar los pesos y sesgos a partir de ejemplos de entrenamiento. El proceso sigue generalmente los siguientes pasos:

1. Propagaci´ on hacia adelante (forward pass): los datos de entrada se procesan capa por capa hasta producir una salida.
2. C´ alculo del error: se compara la salida de la red con la salida esperada mediante una funci´ on de p´ erdida.


<!-- page 31 -->

3. Retropropagaci´ on (backpropagation): se calcula el gradiente del error respecto a cada par´ ametro de la red usando el algoritmo de la regla de la cadena.
4. Actualizaci´ on de par´ ametros: los pesos y sesgos se ajustan en direcci´ on opuesta al gradiente para minimizar el error, mediante algoritmos de optimizaci´ on.

Este ciclo se repite durante m´ ultiples iteraciones o ´ epocas, donde una ´ epoca corresponde a una pasada completa del modelo sobre todo el conjunto de datos de entrenamiento, durante la cual se procesan todos los ejemplos usualmente en peque˜ nos grupos llamados lotes (o en ingl´ es, batches). Despu´ es de cada ´ epoca, los pesos de la red se ajustan y el modelo deber´ ıa haber reducido parcialmente su error. Repetir el proceso por varias ´ epocas permite que la red refine progresivamente sus par´ ametros, mejorando su capacidad para capturar patrones relevantes y generalizar (es decir, producir resultados correctos incluso para ejemplos nuevos o no vistos durante el entrenamiento).

Por supuesto, la cantidad de ´ epocas a realizar var´ ıa a partir del rendimiento del modelo. Un n´ umero excesivo de ´ epocas puede llevar a que nuestro modelo se sobreajuste (overfitting), es decir, la red aprenda demasiado bien los detalles del conjunto de entrenamiento y pierda la capacidad de generalizar en ejemplos no vistos. Por eso, el n´ umero de ´ epocas no siempre es fijo. Es com´ un utilizar una porci´ on del conjunto de datos para validar y monitorear el desempe˜ no durante el entrenamiento, y detenerlo cuando el modelo deje de mejorar.

## 3.7.2. Redes Neuronales Convolucionales

Las redes neuronales convolucionales (CNN, por sus siglas en ingl´ es) son un tipo especializado de red neuronal dise˜ nado para procesar datos con estructura espacial, como im´ agenes o videos. Su objetivo principal es aprender autom´ aticamente representaciones jer´ arquicas de los datos visuales, preservando la correlaci´ on espacial entre p´ ıxeles y reduciendo la complejidad computacional mediante operaciones locales [30].

A diferencia de las redes fully-connected o densas tradicionales, las CNN utilizan la estructura bidimensional (o tridimensional, en el caso de im´ agenes RGB o secuencias de video) del dato de entrada para detectar patrones espaciales en distintos niveles de abstracci´ on. En lugar de aprender pesos o sesgos independientes para cada p´ ıxel, los filtros o kernels se comparten a lo largo de toda la imagen, lo que permite detectar una misma caracter´ ıstica (por ejemplo, un borde o una textura) sin importar su posici´ on [31]. La CNN se estructuran t´ ıpicamente en tres tipos de capas fundamentales:


<!-- page 32 -->

## Capas convolucionales

Es el bloque fundamental de una CNN y donde ocurre la mayor parte del aprendizaje. Cada capa aplica varios filtros que se deslizan sobre la entrada entera realizando una operaci´ on de convoluci´ on (esto lo vimos anteriormente en la secci´ on de 'Filtrados especiales y Kernels'). El resultado de la aplicaci´ on del filtro sobre la entrada va a ser un mapa de caracter´ ısticas, por lo que mientras m´ as filtros, m´ as caracter´ ısticas se pueden detectar sobre la entrada. Adem´ as del n´ umero de filtros, tenemos los par´ ametros stride y padding . Stride determina cu´ antos p´ ıxeles se avanza al mover el filtro, en donde un valor de 1 hace que el filtro se mueva un p´ ıxel por vez, un valor de 2 el filtro salta de a dos p´ ıxeles, etc. Por otro lado, el padding define c´ omo se manejan los bordes, ya que puede suceder que un filtro no encaje perfectamente con la imagen.

Luego de obtener el mapa de caracter´ ısticas, se aplica normalmente una funci´ on de activaci´ on no lineal (como por ejemplo ReLU) para introducir no linealidad en el modelo.

## Capas de Pooling

Reducen la dimensionalidad de los mapas de caracter´ ısticas post aplicaci´ on de las funciones de activaci´ on. Esto se hace a trav´ es de operaciones como max pooling o average pooling. Por ejemplo, el max pooling selecciona el valor m´ aximo dentro de una regi´ on del mapa, y el average pooling selecci´ oona el valor promedio. Esta reducci´ on disminuye el costo computacional y aporta invariancia a peque˜ nas traslaciones o deformaciones en la entrada.

## Capas Densas (fully connected)

En la etapa final, los mapas de caracter´ ısticas se 'aplanan' (flatten) y se conectan a una o m´ as capas densas encargadas de integrar la informaci´ on global y realizar la predicci´ on final.

En la figura 11 podemos ver como se estructuran las capas y el flujo que realiza la entrada por medio de las capas hasta la capa de salida. A medida que las capas convolucionales se apilan, la red aprende representaciones jer´ arquicas: las capas iniciales detectan patrones simples como bordes o texturas, las capas intermedias combinan estos patrones en formas m´ as complejas, y las capas profundas capturan conceptos de alto nivel, como partes de objetos o gestos completos. En aplicaciones de traducci´ on de lengua de se˜ nas, las CNN suelen actuar como un extractor de caracter´ ısticas visuales, produciendo embeddings o representaciones compactas de cada frame que posteriormente pueden ser procesadas por redes recurrentes o arquitecturas de atenci´ on para capturar la din´ amica temporal de la secuencia. Vamos a explorar arquitecturas que incluyen CNNs en secciones posteriores.


<!-- page 33 -->

Figura 11: Red neuronal convolucional con capa de convoluci´ on, pooling y densa para la detecci´ on de d´ ıgitos escritos a mano en im´ agenes. Imagen proveniente de [32]

<!-- image -->

## 3.7.3. Redes Neuronales Recurrentes

Las redes neuronales recurrentes (RNN, por sus siglas en ingl´ es) son arquitecturas dise˜ nadas para procesar datos secuenciales, donde la informaci´ on previa es relevante para interpretar correctamente la entrada actual. A diferencia de las redes neuronales tradicionales, que procesan los datos en una sola direcci´ on de entrada a salida, las RNNs incorporan loops internos que permiten que la salida de un paso temporal se retroalimente como entrada en el siguiente. Esta caracter´ ıstica otorga a la red una memoria de estado, esencial para capturar dependencias temporales en secuencias de datos, como es el caso de secuencias de la lengua de se˜ nas [33]. En la figura 12 se ilustra una red neuronal recurrente con sus estados recurrentes en las capas ocultas.

El funcionamiento de una RNN puede describirse mediante la actualizaci´ on iterativa de un estado oculto h t que representa la informaci´ on relevante acumulada hasta el instante t .

Las RNNs se componen de neuronas recurrentes ilustradas en la figura 13. Estas neuronas son unidades que mantienen un estado oculto que almacena informaci´ on de entradas previas y se actualiza en cada paso temporal. Es lo que permite a la red 'recordar' el contexto anterior y ajustar sus predicciones de acuerdo con la secuencia completa. En cada paso temporal, la red recibe una entrada x t y combina la entrada con el estado oculto del paso anterior h t -1 , produciendo un nuevo estado h t = f ( W x x t + W h h t -1 + b ) donde f es una funci´ on de activaci´ on como ReLU. Este estado oculto se propaga a lo largo de la secuencia y act´ ua como una forma de memoria distribuida.


<!-- page 34 -->

Figura 12: Red neuronal recurrente

<!-- image -->

Se suele representar a las redes RNN como una serie de capas 'desenrolladas en el tiempo', donde cada paso temporal se trata como una capa independiente, lo que facilita la aplicaci´ on de retropropagaci´ on a trav´ es del tiempo (Backpropagation Through Time, BPTT). Este m´ etodo extiende la retropropagaci´ on vista anteriormente a lo largo de todos los pasos temporales de la secuencia, acumulando los gradientes de error y ajustando los pesos compartidos entre los diferentes instantes.

En la traducci´ on autom´ atica de la lengua de se˜ nas, las RNNs se combinan frecuentemente con redes convolucionales (CNNs) que act´ uan como extractores de caracter´ ısticas de cada frame de video. La CNN produce embeddings que capturan la informaci´ on espacial de manos, rostro y cuerpo, y la RNN modela la din´ amica temporal de estos gestos, generando traducciones coherentes en forma de glosses o directamente como texto [7]. Esta combinaci´ on permite a los sistemas de SLT comprender contexto y continuidad de los signos, logrando un desempe˜ no significativamente superior al uso de CNNs aisladas.


<!-- page 35 -->

Figura 13: Neurona recurrente que ilustra el proceso en el cual los estados ocultos h i con i ∈ { 0 , 1 , ..., n } se retroalimentan a los siguientes estados para producir la salida y i +1 partiendo de la entrada x i +1

<!-- image -->

## 3.7.4. Arquitecturas Encoder-Decoder y Transformers

Previo a la introducci´ on del modelo Transformer, las arquitecturas de traducci´ on autom´ atica y procesamiento secuencial se basaban en estructuras de tipo Encoder-Decoder compuestas por redes neuronales recurrentes (RNN) y tambi´ en redes convolucionales (CNN) [7] [34]. En estos enfoques, el encoder procesaba la secuencia de entrada y la comprim´ ıa en un vector de contexto fijo, que posteriormente era utilizado por el decoder para generar la secuencia de salida. Un ejemplo de este tipo de modelos fueron las redes seq2seq propuestas por Sutskever et al (2014).

Si bien estos modelos lograron resultados notables, su desempe˜ no se ve´ ıa limitado por la dificultad para capturar dependencias a largo plazo y por la naturaleza secuencial del procesamiento, que imped´ ıa el paralelismo durante el entrenamiento [35]. Este problema fue abordado con la introducci´ on del mecanismo de atenci´ on por Bahdanau et al. (2015) , que permiti´ o al decoder acceder din´ amicamente a diferentes partes de la salida del encoder en cada paso de generaci´ on [35]. Este enfoque no solo mejor´ o significativamente la calidad de las traducciones, sino que tambi´ en inspir´ o m´ ultiples variantes posteriores, como las atenciones globales y locales de Luong et al (2016) [36].

Con la popularidad del mecanismo de atenci´ on, en 2017, Vaswani et al. presentaron al modelo Transformer, el cual marc´ o un cambio de paradig- ma en el campo del aprendizaje profundo y, en particular, en las tareas de procesamiento secuencial. La clave de su ´ exito radica en el uso exclusivo de mecanismos de atenci´ on, eliminando por completo la necesidad de recurrencia o convoluci´ on. Este dise˜ no permiti´ o modelar relaciones entre todos los elementos de una secuencia de manera directa y simult´ anea, independientemente de su posici´ on relativa, mejorando tanto la capacidad de aprendizaje contextual como la eficiencia computacional [37].


<!-- page 36 -->

El objetivo de esta secci´ on no es describir con minucioso detalle el funcionamiento matem´ atico del Transformer, sino ofrecer una visi´ on intuitiva de su arquitectura y de c´ omo sus componentes principales interact´ uan entre s´ ı para procesar y generar secuencias.

## 3.7.5. ¿Qu´ e es un Transformer?

Un Transformer est´ a compuesto principalmente por dos m´ odulos: un encoder, encargado de procesar la secuencia de entrada y generar una representaci´ on intermedia de la misma, y un decoder, responsable de producir la secuencia de salida de manera progresiva a partir de esa representaci´ on. El modelo sigue un esquema de traducci´ on secuencia a secuencia, donde aprende a mapear una entrada (por ejemplo, una oraci´ on en ingl´ es) hacia una salida objetivo (su traducci´ on al espa˜ nol). En la figura 14 tenemos una ilustraci´ on de la arquitectura general de un Transformer

El flujo de datos comienza en el encoder, donde la secuencia de entrada es primero convertida a representaciones continuas a trav´ es de una capa de embedding. Cada elemento de la secuencia (sea una palabra, un subtoken o un vector de caracter´ ısticas) se proyecta a un espacio de dimensi´ on fija d model . Debido a que el Transformer no posee un mecanismo interno que capture el orden temporal de los elementos en una secuencia, a estos embeddings se les suma una codificaci´ on posicional, que introduce informaci´ on sobre la posici´ on de cada elemento en la secuencia; la suma de ambos componentes da lugar a una representaci´ on que combina significado y estructura. Esta representaci´ on se propaga a trav´ es de una pila de capas del encoder, donde cada una aplica mecanismos de atenci´ on (Multi-Head Attention) y redes feed-forward para refinar progresivamente las relaciones entre los elementos. La salida final del encoder es un conjunto de vectores que condensan la informaci´ on global de la entrada, la cual se conoce com´ unmente como 'memoria' del encoder.

El decoder por otro lado, utiliza esa memoria como fuente de contexto para generar la secuencia de salida. En cada paso de generaci´ on, el decoder recibe como entrada los tokens previamente generados, que son tambi´ en convertidos en embeddings y enriquecidos con codificaciones posicionales. A partir de esta informaci´ on, el modelo aplica sus propios mecanismos de aten- ci´ on: primero un bloque de autoatenci´ on enmascarada (Multi-Head Masked Attention) que le permite atender s´ olo a los tokens anteriores (garantizando la causalidad del proceso), y luego una atenci´ on cruzada (Multi-Head Attention) que le permite enfocarse en las partes relevantes de la memoria del encoder. De esta manera, el decoder integra tanto la historia parcial de la salida como el contexto global de la entrada.


<!-- page 37 -->

Cada nuevo estado del decoder se transforma en una distribuci´ on de probabilidad sobre el vocabulario mediante una proyecci´ on lineal seguida de una funci´ on softmax, obteniendo as´ ı las probabilidades de las posibles pr´ oximas unidades de salida. El modelo selecciona el token m´ as probable (o un conjunto de candidatos, dependiendo de la estrategia de decodificaci´ on) y lo reutiliza como entrada en el siguiente paso. Este procedimiento autoregresivo se repite hasta que se genera un s´ ımbolo especial de fin de secuencia o se alcanza una longitud m´ axima. En s´ ıntesis, el Transformer convierte una secuencia completa en otra mediante un proceso de codificaci´ on-decodificaci´ on totalmente basado en atenci´ on, donde el encoder construye una representaci´ on contextual de la entrada y el decoder la interpreta paso a paso para producir la traducci´ on final.

A continuaci´ on, se detallar´ an los componentes fundamentales que conforman esta arquitectura. Comenzaremos por los embeddings, luego introduciremos la codificaci´ on posicional, y finalmente, se explicar´ an en profundidad las estructuras del encoder y el decoder, junto con sus mecanismos internos.

## 3.7.6. Embeddings

Antes de adentrarnos en los m´ odulos principales del Transformer, es importante primero entender el preprocesamiento que se realiza sobre los datos. La secuencia de datos debe convertirse en una representaci´ on num´ erica continua que el modelo pueda procesar. Este proceso se lleva a cabo mediante representaciones especiales llamadas embeddings, las cuales proyectan cada unidad discreta de la secuencia en un vector denso de dimensi´ on fija d model .

En el contexto del procesamiento de lenguaje, cada unidad se denomina token. Un token puede representar una palabra completa, una subpalabra o hasta car´ acteres, dependiendo del m´ etodo de tokenizaci´ on utilizado. Cada uno de estos tokens es transformado en un vector de caracter´ ısticas que captura propiedades sint´ acticas y sem´ anticas aprendidas durante el entrenamiento. Esta proyecci´ on se realiza mediante una matriz de embeddings E ∈ R | V |× d model donde | V | corresponde al tama˜ no del vocabulario del modelo. Cada token act´ ua como ´ ındice dentro de esta matriz, seleccionando la fila que contiene su representaci´ on (o embedding) en el espacio vectorial.

Adem´ as de los tokens que representan palabras o s´ ımbolos del vocabu- lario, el Transformer utiliza tokens especiales que cumplen funciones estructurales dentro de la secuencia. El token &lt;SOS&gt; (Start of Sequence) marca el inicio de la secuencia de salida y sirve como primera entrada del decoder durante el proceso de generaci´ on (tambi´ en se le suele llamar &lt;BOS&gt; o Begin of Sequence). El token &lt;EOS&gt; (End of Sequence) indica el final de la secuencia y permite al modelo reconocer el momento en que debe dejar de generar nuevos tokens en la secuencia. Por ´ ultimo, el token &lt;PAD&gt; (Padding) se emplea para completar secuencias m´ as cortas dentro de un mismo lote de entrenamiento hasta alcanzar la longitud de la m´ as extensa. Este padding permite el procesar de forma paralela las secuencias que son de distintas longitudes, pero no aporta informaci´ on ´ util. Por eso, durante el c´ alculo de la atenci´ on se aplica una m´ ascara de padding, que impide que el modelo considere estas posiciones al establecer relaciones entre los tokens o al calcular la funci´ on de p´ erdida.


<!-- page 38 -->

Figura 14: Arquitectura general de un transformer. Imagen proveniente de [37]

<!-- image -->


<!-- page 39 -->

Ahora bien, como dijimos anteriormente, el Transformer no tiene una noci´ on de orden de cada token dentro de su secuencia. Dado que el mismo procesa todos los elementos en paralelo, necesita incorporar el orden de aparici´ on de cada uno. Para esto, se suman las codificaciones posicionales, que a˜ naden informaci´ on estructural al embedding original, conformando la representaci´ on que ingresa al encoder.

## 3.7.7. Codificaci´ on posicional

El codificador posicional sinusoidal b´ asicamente lo que busca es representar cada posici´ on t con un vector construido usando senos y cosenos de diferentes frecuencias. La f´ ormula para este codificador es la siguiente:

<!-- formula-not-decoded -->

donde t es el ´ ındice temporal en la secuencia, d model es la dimensi´ on del embedding de cada token e i es el ´ ındice de la dimensi´ on del embedding. Por ejemplo, si tuvieramos d model = 4 y queremos calcular el embedding posicional para t = 5 dentro de una secuencia con m´ as de 5 posiciones, vamos a tener:

- Para i = 0 tenemos:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->


<!-- page 40 -->

- Para i = 1:

<!-- formula-not-decoded -->

Entonces el vector posicional para t = 5 ser´ ıa:

<!-- formula-not-decoded -->

La elecci´ on de seno y coseno para la codificaci´ on posicional se debe a que son funciones peri´ odicas determin´ ısticas, lo que permite representar posiciones relativas sin necesidad de que la red las aprenda expl´ ıcitamente durante el entrenamiento. Estas funciones, aplicadas con diferentes frecuencias, dotan al transformer de la capacidad de interpretar tanto la cercan´ ıa como la lejan´ ıa entre elementos dentro de la secuencia.

- Con frecuencias bajas, los valores cambian lentamente: permiten diferenciar posiciones muy distantes (por ejemplo, el inicio vs el fin de una secuencia), pero no son ´ utiles para distinguir entre elementos consecutivos, ya que la variaci´ on es m´ ınima.
- Con frecuencias altas, los valores cambian r´ apidamente: son ´ utiles para discriminar entre posiciones cercanas, pero pierden capacidad para distinguir posiciones lejanas, dado que la periodicidad de la onda provoca repeticiones y ambig¨ uedades.

Para evitar estas limitaciones, la codificaci´ on posicional combina m´ ultiples frecuencias en paralelo, asignando a cada par de dimensiones del embedding una frecuencia distinta. Adem´ as, el uso simult´ aneo de seno y coseno garantiza variabilidad y unicidad en la representaci´ on, produciendo vectores ´ unicos para cada posici´ on dentro de la secuencia.

Una analog´ ıa ´ util es la del reloj:

- La manecilla de las horas representa la baja frecuencia, que cambia lentamente y captura el contexto global.
- La manecilla de los minutos refleja una frecuencia intermedia.
- La manecilla de los segundos corresponde a la alta frecuencia, que distingue cambios locales.


<!-- page 41 -->

Si observ´ aramos solo los segundos, las 12:00:05 y las 21:00:05 ser´ ıan indistinguibles. Si mir´ aramos solo las horas, las 12:00:00 y las 12:59:00 parecer´ ıan iguales. Sin embargo, al considerar conjuntamente todas las manecillas, se obtiene una representaci´ on ´ unica e inequ´ ıvoca del momento exacto. De la misma manera, la combinaci´ on de senos y cosenos en distintas frecuencias asegura que cada token posea una representaci´ on posicional ´ unica. En la figura 15 podemos visualizar mediante un mapa de calor c´ omo var´ ıan las componentes seno y coseno a lo largo de las posiciones y dimensiones del embedding.

Figura 15: Mapa de calor de la codificaci´ on posicional sinusoidal. El eje vertical representa la posici´ on dentro de la secuencia y el eje horizontal las dimensiones del embedding. Los patrones de bandas rojas y azules reflejan las oscilaciones generadas por las funciones seno y coseno en distintas frecuencias. Imagen proveniente de [38].

<!-- image -->

Una vez se producen estas codificaciones posicionales, las mismas se suman a cada embedding punto a punto.

## 3.7.8. El Encoder

Los encoders son todos id´ enticos en su estructura. La entrada al encoder es una secuencia representada como una matriz de embeddings de tama˜ no T × d model donde T corresponde a la longitud de la secuencia y d model a la dimensi´ on de cada embedding (por ejemplo 512). Cada capa de encoder est´ a compuesta por dos subcomponentes principales: un mecanismo de MultiHead Attention, que modela las dependencias entre los diferentes elementos de la secuencia, y una red Feed-Forward, que transforma y refina las representaciones obtenidas. Adem´ as, ambos subcomponentes se encuentran envueltos por conexiones residuales y normalizaciones de capas (Add &amp; Norm).


<!-- page 42 -->

## Atenci´ on Multi-Cabeza (Multi-Head Attention)

El mecanismo de Multi-Head Attention constituye el componente central de los modelos Transformer. Su funci´ on principal es permitir que cada elemento de la secuencia incorpore informaci´ on contextual proveniente de los dem´ as elementos. Por ejemplo, en una oraci´ on como 'Thinking Machines', el modelo no debe tratar a 'Machines' como un t´ ermino aislado, sino como parte de la expresi´ on completa 'Thinking Machines'. El mecanismo de atenci´ on logra esto al calcular, para cada posici´ on, qu´ e otras posiciones son m´ as relevantes y en qu´ e medida deben influir en su representaci´ on.

El funcionamiento interno puede describirse del siguiente modo: cada elemento de la secuencia genera tres representaciones conocidas como query , key y value . Para el elemento i en la secuencia:

- Query ( q i ) o vector de consulta: define qu´ e informaci´ on busca ese elemento.
- Key ( k i ) o vector de clave: define c´ omo puede ser identificado por los dem´ as elementos.
- Value ( v i ) o vector de valor: contiene la informaci´ on que el elemento comparte si resulta relevante.

No entraremos en detalle en c´ omo se genera cada vector, pero nos quedaremos con que los mismos se obtienen a trav´ es de multiplicaciones matriciales de cada embedding por tres matrices con pesos distintos (matriz W Q , W K y W V ) aprendidos durante el entrenamiento. En la figura 16 se ilustra un ejemplo de las distintas representaciones de los vectores para la frase 'Thinking Machines'.


<!-- page 43 -->

Figura 16: Ilustraci´ on de las distintas representaciones para los vectores de embedding the las palabras en la frase 'Thinking Machines'(Jay Alammar, 2018).

<!-- image -->

Con estas tres representaciones, para cada elemento i se compara q i con las keys k j de todos los elementos j de la misma secuencia, obteniendo as´ ı un puntaje definido como puntaje de similitud:

<!-- formula-not-decoded -->

Estos puntajes se escalan y se normalizan de manera que se transforman en lo que se llaman pesos de atenci´ on ˆ p i,j que determinan cu´ anta influencia ejerce cada posici´ on sobre la actual. Con esos pesos, el vector de salida de cada posici´ on se construye como una combinaci´ on ponderada de los values de toda la secuencia. De esta forma, la representaci´ on final de una palabra como 'Machines' ya no corresponde ´ unicamente a su embedding inicial, sino que incluye tambi´ en informaci´ on proveniente de 'Thinking', capturando as´ ı la dependencia sem´ antica entre ambas. El proceso se puede ver en la figura 17.


<!-- page 44 -->

Figura 17: d k es la dimensi´ on de los vectores query y key . La divisi´ on por √ d k = 8 es simplemente un dato ejemplo del paper de Vaswani. Se aplica Softmax a modo de normalizaci´ on. (Jay Alammar, 2018).

<!-- image -->

Este procedimiento se aplica en paralelo en varias 'cabezas' de atenci´ on (de all´ ı el t´ ermino multi-head attention), cada una especializada en capturar diferentes tipos de relaciones (gramaticales, sem´ anticas o posicionales). La diferencia entre cada cabeza de atenci´ on est´ a en los valores de q, k y v , generados todos de manera distinta. Finalmente, los resultados de todas las cabezas se concatenan y se proyectan nuevamente a la dimensi´ on original ( d model ) en un vector denominado como vector de atenci´ on, enriqueciendo su representaci´ on.

En s´ ıntesis, el mecanismo de atenci´ on multi-cabeza construye una nueva representaci´ on contextualizada de cada elemento, donde cada vector no solo conserva su informaci´ on original, sino que tambi´ en integra aquella proveniente de las posiciones m´ as relevantes de la secuencia T × d model .


<!-- page 45 -->

## Red Feed-Forward

La red feed-forward es el segundo componente fundamental de cada capa del encoder. Su funci´ on es refinar la representaci´ on obtenida tras el mecanismo de atenci´ on (y luego de aplicarle la operaci´ on Add &amp; Norm), incrementando la capacidad expresiva del modelo mediante transformaciones no lineales aplicadas de forma independiente a cada posici´ on de la secuencia.

Este bloque consiste en dos transformaciones lineales separadas por una funci´ on de activaci´ on no lineal (com´ unmente ReLU). En la primera transformaci´ on, cada vector de la secuencia se proyecta a un espacio intermedio de mayor dimensionalidad, denominado d ff , lo que permite al modelo representar relaciones m´ as complejas. Luego se aplica la funci´ on de activaci´ on, y finalmente, una segunda proyecci´ on devuelve el vector a su dimensi´ on original d model .

De este modo, un vector como z i obtenido tras la atenci´ on, se transforma primero en una versi´ on m´ as amplia y expresiva, luego se enriquece mediante la no linealidad y finalmente se comprime de nuevo a su tama˜ no inicial. Este procedimiento permite que cada representaci´ on contextualizada no solo combine informaci´ on del resto de la secuencia, sino que adem´ as sea procesada con mayor capacidad expresiva antes de aplicarle la operaci´ on Add &amp; Norm y pasar a la siguiente capa del modelo.

Cabe destacar que la salida de cada encoder mantiene la forma T × d model y constituye lo que anteriormente llamamos 'memoria' que el decoder va a usar para generar la secuencia de salida.

## Conexi´ on Residual y Capa de Normalizaci´ on (Operaci´ on Add &amp; Norm)

Tanto el bloque de atenci´ on multi-cabeza como la red feed-forward se encuentran envueltos por dos operaciones que buscan mejorar el rendimiento del modelo. Una de ellas es la conexi´ on residual y la otra la capa de normalizaci´ on.

La conexi´ on residual consiste en sumar la entrada original de una subcapa con su salida transformada. En otras palabras, en lugar de reemplazar completamente la informaci´ on de entrada, el modelo aprende una correcci´ on sobre la misma. Si denotamos la funci´ on aplicada por la subcapa como Sublayer ( x ), la salida resultante se expresa como:

<!-- formula-not-decoded -->

Esto lo que hace es evitar degradar la informaci´ on cuando la misma viaja a trav´ es de varias capas en el Transformer.


<!-- page 46 -->

Por ejemplo, en la salida del componente de atenci´ on multi-cabeza, se le suma al vector de entrada del encoder, el vector de atenci´ on z i (resultante del componente de atenci´ on multi-cabeza). De mismo modo, luego de la red feed-forward, al vector resultante de la misma se le suma su entrada (el vector de atenci´ on z luego de la conexi´ on residual y la capa de normalizaci´ on).

La capa de normalizaci´ on consta simplemente de una funci´ on que ajusta los valores que produce cada capa para que mantengan una escala estable permitiendo al modelo entrenarse de una forma mas equilibrada. Se puede denotar esta funci´ on de la siguiente forma:

<!-- formula-not-decoded -->

Ambas operaciones denotadas como Add &amp; Norm en la figura del Transformer, se repiten tras cada subcapa del encoder. La secuencia de operaciones es la siguiente:

1. Multi-Head Attention → Add &amp; Norm
2. Feed-Forward → Add &amp; Norm

## 3.7.9. El Decoder

Como ya dijimos, el decoder del Transformer es el componente encargado de generar la secuencia de salida de manera autoregresiva, es decir, produciendo un token por vez hasta alcanzar el s´ ımbolo de fin de secuencia &lt;EOS&gt; . Durante este proceso, el modelo utiliza tanto la informaci´ on de los tokens generados hasta el momento como la representaci´ on contextual o 'memoria' de la secuencia de entrada producida por el encoder.

La entrada al decoder puede representarse como una matriz de embeddings de tama˜ no T ′ × d model donde T ′ es la longitud de la secuencia de salida generada hasta el momento. Al igual que en el encoder, todas las subcapas del decoder mantienen la misma dimensionalidad de salida d model .

Cada capa del decoder se compone de tres subcomponentes principales: un bloque de Masked Multi-Head Attention, que modela las dependencias internas dentro de la secuencia generada; un bloque de Multi-Head Attention, que permite incorporar la informaci´ on proveniente del encoder; y una red Feed-Forward, que refina la representaci´ on final antes de pasar a la siguiente capa.

Como en el encoder, cada subcomponente est´ a envuelto por una conexi´ on residual y una capa de normalizaci´ on (operaci´ on Add &amp; Norm).


<!-- page 47 -->

## Masked Multi-Head Attention

El primer bloque o subcomponente del decoder es un mecanismo de atenci´ on con m´ ultiples cabezales que permite al modelo tener en cuenta los tokens previamente generados mientras predice el siguiente. Sin embargo, para mantener la coherencia temporal y evitar que el modelo acceda a informaci´ on del futuro (o sea, tokens que todav´ ıa no se generaron) esta atenci´ on se enmascara.

El enmascaramiento se aplica sobre la matriz de puntajes de atenci´ on, de modo que cada posici´ on s´ olo pueda atenderse a s´ ı misma y a las anteriores. Esto hace que al generar el token t i el modelo se base ´ unicamente en la secuencia ( t 1 , t 2 , ..., t i -1 ) respetando el flujo causal de la generaci´ on autoregresiva. El m´ etodo por el cu´ al se ignoran tokens futuros, es asignar pesos de atenci´ on nulos o menos infinito a los mismos.

El proceso interno es similar al de la atenci´ on vista en el encoder. Cada token genera tres representaciones: query (Q), key (K) y value (V), obtenidas mediante multiplicaciones por matrices entrenables. Luego se calculan los puntajes de similitud entre cada par de tokens y se normalizan mediante softmax, pero ignorando las posiciones bloqueadas por la m´ ascara.

De este modo, el modelo aprende qu´ e partes de la secuencia ya generada son m´ as relevantes para decidir cu´ al ser´ a el pr´ oximo token. La salida de este bloque ser´ an las salidas de las diferentes cabezas de atenci´ on concatenadas y proyectadas de nuevo a su tama˜ no de embedding original d model . Posteriormente, se aplica a la salida la operaci´ on Add &amp; Norm.

## Multi-Head Attention o Cross-Attention

El segundo bloque o subcomponente, establece una especie de comunicaci´ on entre el encoder y el decoder. El objetivo de este bloque, tambi´ en llamado atenci´ on cruzada (cross-attention) es proveer al decoder la 'memoria' producida por el encoder. Esto se hace de la siguiente manera: las queries (Q) se obtienen de la salida del bloque anterior del decoder, (Masked MultiHead Attention + Add &amp; Norm), mientras que las keys (K) y values (V) provienen de la salida final del encoder.

Este proceso es muy importante ya que permite al decoder determinar qu´ e partes de la entrada son relevantes para generar cada token de salida. Por ejemplo, si se quisiera traducir la oraci´ on 'Thinking Machines' al espa˜ nol, al generar el token 'm´ aquinas', el modelo aprender´ a a enfocar su atenci´ on sobre 'Machines' en la entrada; y al generar 'pensantes', desplazar´ a su atenci´ on hacia 'Thinking'. Si hablamos de funcionamiento, el mecanismo de atenci´ on aqu´ ı opera igual que la atenci´ on del encoder, pero con diferentes or´ ıgenes de informaci´ on.


<!-- page 48 -->

De nuevo, la salida de este bloque va a ser la concatenaci´ on de las salidas de los distintos cabezales previo a una proyecci´ on al tama˜ no de embedding original d model y a la operaci´ on Add &amp; Norm.

## Red Feed-Forward

Este es el tercer subcomponente del decoder, su funci´ on es transformar las representaciones obtenidas tras ambos meacnismo de atenci´ on con el objetivo de aumentar la capacidad expresiva del modelo, al igual que la red FeedForward del encoder. Luego, a la salida de la red, se le vuelve a aplicar la operaci´ on Add &amp; Norm.

## Conexi´ on Residual y Capa de Normalizaci´ on (Operaci´ on Add &amp; Norm)

La operaci´ on Add &amp; Norm es exactamente igual a la del encoder. El patr´ on completo de operaciones en este caso sigue la siguiente secuencia:

1. Masked Multi-Head Attention → Add &amp; Norm
2. Multi-Head Attention (o Cross-attention) → Add &amp; Norm
3. Feed-Forward → Add &amp; Norm

## Generaci´ on Final

Cada vector de la matriz de salida del decoder T ′ × d model representa la versi´ on final contextualizada del token correspondiente, incorporando tanto la informaci´ on del contexto previo del decoder como de la 'memoria' del encoder.

Antes de convertir estas representaciones en la predicci´ on deseada (por ejemplo, palabras) lo que se hace es aplicar una proyecci´ on lineal mediante una matriz especial de pesos W o ∈ R | V |× d model , (donde, como dijimos anteriormente, | V | es el tama˜ no del vocabulario). Esta proyecci´ on transforma cada vector en un espacio de dimensi´ on | V | , asignando un puntaje llamado logit a cada palabra posible. Luego, una funci´ on de activaci´ on softmax convierte esos puntajes en una distribuci´ on de probabilidad sobre el vocabulario, indicando cu´ al es el token m´ as probable de ser generado a continuaci´ on.

Durante la inferencia (es decir, predicci´ on sobre datos no usados en el entrenamiento), el modelo toma el token con mayor probabilidad (esto en realidad depende de la estrategia de generaci´ on, o tambi´ en llamado 'decodificaci´ on'). Luego, a˜ nade ese token a la secuencia de salida y lo reingresa al decoder para generar el siguiente. Este proceso se repite de manera autoregresiva hasta que el modelo produce el s´ ımbolo de fin de secuencia &lt;EOS&gt; o alcanza la longitud m´ axima establecida.


<!-- page 49 -->

Por ejemplo, en el caso de una tarea de traducci´ on autom´ atica entre idiomas (por ejemplo, del ingl´ es al espa˜ nol), el proceso ocurre del siguiente modo: el encoder recibe como entrada la oraci´ on en ingl´ es 'Thinking Machines' y genera una representaci´ on contextual de la misma, que resume la informaci´ on sem´ antica y sint´ actica de toda la secuencia.

El decoder, por su parte, inicia el proceso de generaci´ on con el token especial &lt;SOS&gt; (Start of Sequence), cuyo embedding se introduce como primera entrada. Utilizando esa entrada junto con la 'memoria' producida por el encoder, el modelo calcula una distribuci´ on de probabilidad sobre el vocabulario del idioma destino. La palabra con mayor probabilidad en esta primera iteraci´ on resulta ser 'M´ aquinas', por lo que el modelo la selecciona como el primer token generado.

A continuaci´ on, la secuencia parcial formada por &lt;SOS&gt; y 'M´ aquinas' se vuelve a ingresar al decoder, que repite el mismo proceso de atenci´ on y proyecci´ on. Gracias al contexto acumulado y a la informaci´ on contextual del encoder, en esta segunda iteraci´ on el modelo predice el siguiente token, 'Pensantes'. De esta manera, la secuencia de salida crece paso a paso, construyendo la traducci´ on completa 'M´ aquinas Pensantes'.

El proceso contin´ ua de forma autoregresiva, generando un token en cada paso, hasta que el modelo emite el s´ ımbolo &lt;EOS&gt; (End of Sequence), indicando el final de la generaci´ on.


<!-- page 50 -->

## 4. Visi´ on por Computadora aplicado a la Traducci´ on Autom´ atica de la Lengua de Se˜ nas

Habiendo repasado conceptos importantes, ahora revisaremos algunas arquitecturas relevantes en la tarea de traducci´ on de la lengua de se˜ nas.

## 4.1. Arquitecturas basadas en redes neuronales

Como se mencion´ o en el cap´ ıtulo anterior, las redes neuronales convolucionales (CNN) surgieron como un est´ andar en visi´ on por computadora por su capacidad para aprender representaciones jer´ arquicas de im´ agenes de manera autom´ atica y eficiente. En el contexto de SLT, las CNN fueron las primeras arquitecturas profundas en demostrar un rendimiento significativo, principalmente porque permiten extraer patrones visuales relevantes en cada frame de video, tales como la configuraci´ on de la mano, la orientaci´ on, la expresi´ on facial o la ubicaci´ on relativa de los brazos; en lugar de trabajar directamente con p´ ıxeles, las CNN aprenden a transformar secuencias de im´ agenes en representaciones de alto nivel que sirven como ingesta para modelos de traducci´ on.

## CNN como extractores de caracter´ ısticas para secuencias

En los sistemas iniciales de SLT, las CNN se utilizan como tokenizers visuales. Cada fotograma del video pasa por una red convolucional (generalmente preentrenada en tareas de clasificaci´ on de im´ agenes), que produce un vector de caracter´ ısticas o embedding. De esta forma, una secuencia de se˜ nas en video puede representarse como una serie de embeddings, donde cada embedding resume la informaci´ on espacial de un frame. Este procedimiento es an´ alogo al de los tokenizers en procesamiento de lenguaje natural: as´ ı como una oraci´ on se convierte en una secuencia de embeddings de palabras, un video de se˜ nas se convierte en una secuencia de embeddings visuales.

## Modelos h´ ıbridos CNN + RNN

El uso de CNN por s´ ı solo no es suficiente, ya que el lenguaje de se˜ nas es inherentemente temporal y depende de la evoluci´ on de los movimientos a lo largo del tiempo. Para capturar esta dimensi´ on, se desarrollaron arquitecturas h´ ıbridas que combinan CNN con redes recurrentes. En este esquema, la CNN se encarga de capturar la informaci´ on espacial en cada fotograma, mientras que la RNN modela las dependencias temporales entre los embeddings producidos, aprendiendo c´ omo una se˜ na se desarrolla y se enlaza con otras dentro de la oraci´ on.


<!-- page 51 -->

## Limitaciones de CNN en SLT

A pesar de sus logros, las CNN presentan limitaciones importantes en SLT. Primero, su capacidad de capturar dependencias temporales es indirecta, ya que dependen de un modelo adicional (RNN) para procesar secuencias. Segundo, tienden a enfocarse en ventanas locales de informaci´ on visual, lo que puede dificultar la captura de relaciones de largo alcance entre se˜ nas que se extienden en el tiempo. Adem´ as, las CNN cl´ asicas suponen una rigidez espacial en el an´ alisis: se limitan a extraer patrones en regiones fijas de la imagen, lo que puede resultar problem´ atico dado que en la lengua de se˜ nas los gestos pueden variar en posici´ on y escala seg´ un el contexto. Por ´ ultimo, al procesar secuencias largas, las CNN generan altos costos computacionales, ya que cada cuadro debe ser convolucionado y transformado en un embedding, lo cual limita su escalabilidad en corpus de gran tama˜ no.

## 4.1.1. Modelo CNN+RNN aplicado a SLT

Para ilustrar la utilidad de las arquitecturas que integran CNNs y RNNs vamos a basarnos en el trabajo realizado por Camgoz (et al) en su estudio titulado Neural Sign Language Translation [7]. Ya hemos mencionado algunos de los detalles de sus avances a lo largo de esta secci´ on, pero aqu´ ı profundizaremos a´ un m´ as en los mismos.

A diferencia del Reconocimiento de Lengua de Se˜ nas (SLR), Camgoz et al. abordan el problema completo de la traducci´ on como una tarea de Traducci´ on Autom´ atica Neuronal (NMT). Plantean el problema como una probabilidad condicional, en donde el objetivo es aprender la probabilidad condicional p ( y | x ) de generar una oraci´ on y = ( y 1 , y 2 , ..., y U ) donde U es la cantidad total de palabras, dado un video x = ( x 1 , x 2 , ..., x T ) donde T es la cantidad total de frames.

Para ello, emplean m´ etodos de deep learning basados en arquitecturas sequence-to-sequence (seq2seq), una arquitectura que como vimos est´ a dise˜ nada para mapear secuencias de entrada a secuencias de salida de longitud variable; en el contexto de SLT, la secuencia de entrada corresponde a un video que captura los signos, mientras que la secuencia de salida es la traducci´ on en lenguaje hablado o escrito.

Adem´ as de aplicar CNNs+RNNs, la arquitectura seq2seq se compone t´ ıpicamente de un mecanismo de atenci´ on y un encoder, que procesa la informaci´ on de los signos y extrae una representaci´ on interna que captura la informaci´ on espacial y temporal, y un decoder, que genera la secuencia de palabras correspondiente en la lengua objetivo. Esta estructura permite al modelo aprender tanto las relaciones entre los signos como su correspondencia con la lengua hablada, de manera an´ aloga a como los modelos de traducci´ on autom´ atica neuronal procesan texto. Podemos visualizar esta arquitectura en la figura 18.


<!-- page 52 -->

Figura 18: Enfoque tomado por Camgoz et al. para la tarea de la traducci´ on autom´ atica de video a texto de la lengua de se˜ nas. Imagen proveniente de [7].

<!-- image -->

Veamos sus componentes en m´ as detalle:

## Extracci´ on de representaciones espaciales

El primer paso consiste en procesar los videos de se˜ nas para obtener representaciones espaciales de cada frame. Ac´ a entran en juego las redes convolucionales (CNNs), que aprenden a extraer caracter´ ısticas visuales relevantes de las manos, el rostro y la postura corporal. El proceso que llevan a cabo estas redes son:

1. Cada frame x j se propaga a lo largo de una CNN.
2. La red CNN devuelve como resultado una caracter´ ıstica en forma de vector f j . Este vector representa informaci´ on visual y espacial no lineal del frame x j .

Los autores representan esta transformaci´ on de la siguiente forma:

<!-- formula-not-decoded -->


<!-- page 53 -->

## Representaci´ on de las palabras

Este estudio utiliz´ o la lengua de se˜ nas alemanas, por lo que las palabras en alem´ an se representan tambi´ en con vectores de embedding. De esta forma, el modelo puede operar tanto con representaciones visuales (signos) como con representaciones ling¨ u´ ısticas (palabras). Para realizar la representaci´ on, lo que se hace para cada palabra word j es partir de la representaci´ on inicial b´ asica (tambi´ en llamada one-hot encoding) de cada palabra y j y aplicarle una proyecci´ on lineal en donde se multiplica el vector one-hot por una matriz de pesos W sum´ andole una constante b , obtieniendo asi:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

o tambi´ en:

## Tokenizaci´ on

Para el caso de las representaciones espaciales para cada frame, la tokenizaci´ on no es trivial, ya que no existe una correspondencia directa entre los frames del video y las palabras del texto, a diferencia de la traducci´ on autom´ atica de texto. En este trabajo se exploran dos estrategias: tokenizaci´ on a nivel de frames, donde cada frame es un token, y a nivel de glosa, que agrupa varios frames seg´ un unidades de significado de la lengua de se˜ nas mediante un alineamiento definido como RNN-HMM. Por otro lado, la salida se tokeniza a nivel de palabras, siguiendo pr´ acticas comunes en traducci´ on autom´ atica. Se denota esta tokenizaci´ on de la siguiente manera:

<!-- formula-not-decoded -->

donde f 1: T representa la secuencia de embeddings espaciales del video desde el frame 1 al frame T y z 1: N representa la secuencia de tokens resultante despu´ es de aplicar la tokenizaci´ on desde el token 1 al N .

Como bien se dijo, el objetivo es traducir un video de se˜ nas (entrada) x partiendo de representaciones tokenizadas z 1: N en una oraci´ on en lengua hablada (salida) y . Para esto, Camgoz et al. proponen usar una arquitectura encoder-decoder, que se complementa con un mecanismo de atenci´ on. Veamos en detalle esta arquitectura.


<!-- page 54 -->

## Encoder

El encoder se representa con una RNN, en donde cada vector de caracter´ ıstica z 1: N pasa por la misma. Un detalle interesante es que el orden de los frames se invierte antes de pasarlos por la red. Esto puede parecer raro, pero tiene su raz´ on: al invertirlos, se acortan las dependencias entre el inicio del video y el inicio de la oraci´ on en lengua hablada, lo cual facilita el entrenamiento de la red (recordemos que no hay una correspondencia directa entre la primer se˜ na y la primer palabra en la traducci´ on en texto). Se puede pensar como cuando se lee una oraci´ on: si tuvi´ eramos una oraci´ on de 5 palabras, no se entiende la palabra 5 de manera independiente, sino en relaci´ on con las 4 anteriores.

Por lo tanto, cada vector z j de la secuencia completa z 1: N pasa a trav´ es de la RNN. A medida que va pasando cada token z j , la red guarda un estado o j que se utiliza para calcular o j -1 para el token z j -1 . La ecuaci´ on formal es la siguiente:

<!-- formula-not-decoded -->

donde el estado o N es un vector nulo (o cero en todas sus posiciones).

Bien, recordemos que cada o j producido es la memoria interna de la RNN en el paso j . Este vector no es el frame en s´ ı, eso lo representa z j , si no la combinaci´ on de lo que la red acaba de ver m´ as lo que viene recordando de pasos anteriores. Podemos verlo como una 'interpretaci´ on acumulada' de un video.

Cuando se termina de propagar toda la secuencia en la RNN, nos quedamos con el ´ ultimo estado oculto o 1 . A este estado final se le llama h sign , y es un vector latente que intenta resumir todo el video. ´ Este ser´ a el punto de partida del decoder para generar la traducci´ on a texto. A su vez, se guardan los valores o 1 , ..., o N representados como o 1: N , los mismos tambi´ en ser´ an utilizados en el decoder.

## Decoder

El decoder es otra RNN que inicia su proceso usando el vector h sign como el estado inicial h 0 de la RNN. Su tarea es ir generando la oraci´ on en la lengua destino, palabra por palabra. Primero recibe una primera palabra que ser´ a el token especial &lt;BOS&gt; (tambi´ en denotado &lt;SOS&gt; ) para indicar que empieza la traducci´ on. Luego, en cada paso:

- obtiene el word embedding g u -1 de la palabra anterior y u -1
- consulta su memoria (el estado oculto previo h u -1 )


<!-- page 55 -->

- y predice la siguiente palabra y u combinando los tres valores.

Este proceso se repite hasta que aparece el token especial &lt;EOS&gt; . As´ ı, la oraci´ on completa se construye de manera secuencial. Se puede abstraer este proceso con la siguiente ecuaci´ on:

<!-- formula-not-decoded -->

Si recordamos el inicio de esta secci´ on, sabremos que el objetivo final de esta arquitectura esta planteado como una probabilidad condicional p ( y | x ). Justamente, la etapa del decoder busca descomponer la probabilidad condicional ya mencionada p ( x | y ) en probabilidades condicionales ordenadas:

<!-- formula-not-decoded -->

donde p ( y u | y 1: u -1 , h sign ) es la probabilidad que el decoder asigna a la palabra y u dado el contexto (palabras anteriores + video). En palabras simples: la probabilidad de generar toda la oraci´ on es el producto de las probabilidades de cada palabra generada paso a paso.

Como nuestro objetivo es maximizar la probabilidad de la oraci´ on correcta, lo que buscaremos ser´ a minimizar el error producido por esta probabilidad descompuesta. Para ello, se aplica lo que se llama entrop´ ıa cruzada (crossentropy), una funci´ on de p´ erdida en donde se mide que tan 'mal' se predijo la palabra y u comparando la distribuci´ on de probabilidades generadas por el modelo con la distribuci´ on esperada (donde el token correcto tiene un valor de 1, y los dem´ as 0). Este valor de p´ erdida es un valor compuesto calculado por la suma de los errores de cada palabra. Formalmente, la p´ erdida total para una secuencia de entrenamiento se define como:

<!-- formula-not-decoded -->

donde cada t´ ermino -log p ( y u | · ) mide la penalizaci´ on asociada a la palabra y u . As´ ı, minimizar L equivale a maximizar la probabilidad de generar correctamente cada palabra de la secuencia.

Una vez obtenido el valor de p´ erdida, se propaga el mismo a trav´ es de toda la arquitectura para ajustar los pesos del decoder y encoder, los embeddings de las palabras y los pesos de las CNNs, con el objetivo de minimizar el error total.

El modelo encoder-decoder 'cl´ asico' tiene un problema que es que toda la informaci´ on del video queda comprimida en un ´ unico vector h sign . Esto es lo que se llama information bottleneck: los videos son muy largos (muchos frames) y es imposible resumirlos sin perder detalle. Es por eso que aqu´ ı entra en juego el mecanismo de atenci´ on.


<!-- page 56 -->

## Soluci´ on al cuello de botella

Para resolver este cuello de botella, se introduce la atenci´ on, mecanismo que como se dijo anteriormente, fue introducido por Bahdanau et al [35]. Esta t´ ecnica le permite al decoder 'enfocarse' en distintas partes del video seg´ un la palabra que est´ e generando en ese momento.

Lo que hace el modelo es calcular, en cada paso, un vector de contexto c u . Este vector es una combinaci´ on ponderada de todos los estados del encoder:

<!-- formula-not-decoded -->

Los coeficientes γ u,n son los pesos de atenci´ on, y se interpretan como la importancia que tiene cada parte del video n para la palabra que se est´ a traduciendo o generando y u . Existen distintas formas de calcular estos pesos. Camgoz prueba dos: la atenci´ on multiplicativa (Luong) y la atenci´ on aditiva (Bahdanau), que no ser´ an desarrollados en este trabajo.

Este vector de contexto c u se combina con el estado h u para calcular el vector de atenci´ on a u de la siguiente manera:

<!-- formula-not-decoded -->

W c es un par´ ametro aprendido durante entrenamiento.

Finalmente, se alimenta a u a una capa para modelar la probabilidad condicional ordenada de la ecuaci´ on (2). Tambi´ en se utiliza para alimentar el siguiente paso de decodificaci´ on u + 1, quedando as´ ı la ecuaci´ on (1) de la siguiente manera:

<!-- formula-not-decoded -->

Y as´ ı concluye la arquitectura basada en redes neuronales.

## 4.1.2. Rendimiento

En la tarea de traducci´ on de se˜ na a texto, este modelo utiliz´ o AlexNet como red convolucional para extraer las caracter´ ısticas espaciales de cada frame del video. Durante el entrenamiento, el sistema fue optimizado de manera completamente end-to-end, sin utilizar glosas intermedias ni supervisi´ on ling¨ u´ ıstica adicional. Es decir, el modelo aprendi´ o directamente la probabilidad condicional p ( y | x ).


<!-- page 57 -->

Para evaluar la calidad de las traducciones generadas, los autores emplearon la m´ etrica BLEU (Bilingual Evaluation Understudy), que mide la superposici´ on de n-gramas entre la traducci´ on generada por el modelo y la referencia humana del conjunto de datos. Es decir, eval´ ua la coincidencia entre palabras o secuencias cortas de palabras (tokens), sin considerar el significado sem´ antico [39].

- BLEU-1: mide coincidencia de unigramas (palabras individuales). Por ejemplo:

Referencia : 'el gato est´ a en la casa'. Lo cual en unigramas ser´ ıa ['el', 'gato', 'est´ a', 'en', 'la', 'casa'].

Predicci´ on : 'el gato est´ a en casa'. Lo cual en unigramas ser´ ıa ['el', 'gato', 'est´ a', 'en', 'casa'].

Coinciden casi todas las palabras por lo que BLEU-1 es alto.

- BLEU-2: incluye bigramas (pares de palabras consecutivas)

Referencia : en bigramas ser´ ıa ['el gato', 'gato est´ a', 'est´ a en', 'en la', 'la casa'].

Predicci´ on : en bigramas ser´ ıa ['el gato', 'gato est´ a', 'est´ a en', 'en casa']

En la predicci´ on falta 'en la' y 'la casa' por lo que BLEU-2 baja respecto a BLEU-1.

- BLEU-3 y BLEU-4: consideran hasta 3-gramas y 4-gramas, capturando mayor fluidez y coherencia.

Un valor de BLEU cercano a 1 (o 100 %) indica alta coincidencia con la traducci´ on de referencia, mientras que valores cercanos a 0 reflejan baja calidad.

Los autores reportaron los siguientes valores (tabla 1) en el conjunto de prueba del corpus de la lengua de se˜ nas alemana RWTH-PHOENIX-Weather 2014T:


<!-- page 58 -->

Tabla 1: Resultados de las m´ etricas BLEU para la tarea de SLT end-to-end del modelo basado en CNNs y RNNs [7].

| M´ etrica   | Valor   |
|-------------|---------|
| BLEU-1      | 32.24%  |
| BLEU-2      | 19.03%  |
| BLEU-3      | 12.83%  |
| BLEU-4      | 9.58%   |

## 4.2. Arquitecturas basadas en transformers

## Transformers en SLT

En el contexto de SLT, los modelos basados en Transformers introdujeron un cambio sustancial frente a los enfoques tradicionales que combinaban redes convolucionales (CNN) y redes recurrentes (RNN). A diferencia de las CNN+RNN, donde las convoluciones capturan patrones espaciales y las RNN modelan la din´ amica temporal, los Transformers utilizan un mecanismo de autoatenci´ on capaz de modelar dependencias globales tanto en el espacio como en el tiempo dentro de una misma arquitectura.

A diferencia de los modelos CNN+RNN, en los cuales las dependencias temporales se modelan de forma secuencial, el mecanismo de autoatenci´ on permite que cada frame se relacione directamente con cualquier otro, sin restricciones de distancia temporal. Esto le da al Transformer una mayor capacidad para capturar coocurrencias entre articuladores (por ejemplo, la coordinaci´ on entre una expresi´ on facial y un movimiento manual) y para manejar variaciones en la duraci´ on y velocidad de las se˜ nas.

## Ventajas frente a CNN + RNN

Adem´ as de proveer un modelado global de dependencias entre las secuencias, el uso de Transformers en SLT presenta las siguientes ventajas:

- Paralelismo y eficiencia: los Transformers procesan todos los frames en paralelo, acelerando el entrenamiento y evitando los cuellos de botella temporales t´ ıpicos de las RNN.
- Flexibilidad frente a secuencias variables: los Transformers se adaptan mejor a secuencias de distinta longitud, lo cual es crucial en SLT ya que la duraci´ on de una se˜ na o de una oraci´ on en lengua de se˜ nas puede variar significativamente entre signantes y contextos.

Veamos a continuaci´ on el estudio realizado por Camgoz et al (2020) en donde se plantea una arquitectura para la traducci´ on de la lengua de se˜ nas usando transformers.


<!-- page 59 -->

## 4.2.1. Modelo basado en transformers aplicado a SLT

Camgoz et al. (2020) propusieron una arquitectura basada en transformers con una motivaci´ on clara: en procesamiento de texto, los Transformers hab´ ıan superado ampliamente a las RNNs gracias a su capacidad de capturar dependencias de largo alcance y a su paralelizaci´ on eficiente [40]. La idea era trasladar estas ventajas a la se˜ nal visual-temporal de la lengua de se˜ nas, evitando el cuello de botella caracter´ ıstico de las RNNs.

Figura 19: Enfoque tomado por Camgoz et al. para la tarea de la traducci´ on autom´ atica de video a texto de la lengua de se˜ nas usando transformers. Imagen proveniente de [40].

<!-- image -->

En este caso, el problema se formula tambi´ en como el aprendizaje de una probabilidad condicional. El objetivo es estimar la probabilidad de generar una oraci´ on en lengua hablada S = ( w 1 , w 2 , . . . , w U ) de U palabras dado un video de se˜ nas V = ( I 1 , I 2 , . . . , I T ) de T cuados/frames:

<!-- formula-not-decoded -->

Adicionalmente, este modelo incluye un componente de reconocimiento de glosas G = ( g 1 , . . . , g N ) de N glosas, de manera que el aprendizaje se realiza de forma multi-tarea, con dos objetivos simult´ aneos:

<!-- formula-not-decoded -->


<!-- page 60 -->

Este detalle es importante ya que no todos los dataset disponibles incluyen glosas con las cuales poder entrenar este tipo de modelos. De todas maneras, debido a la arquitectura general, este trabajo influy´ o much´ ısimos en modelos SOTA gloss-free.

Veamos los componentes de esta arquitectura.

Figura 20: Arquitectura del modelo para el reconocimiento y traducci´ on de lengua de se˜ nas usando transformers. Imagen proveniente de [40].

<!-- image -->

## Extracci´ on de representaciones espaciales

Al igual que en el estudio anterior, el primer paso consiste en extraer informaci´ on visual de cada frame del video mediante una CNN.

1. Cada frame I t se propaga a lo largo de una CNN. 2. La red CNN devuelve como resultado una caracter´ ıstica en forma de vector f t . Este vector representa informaci´ on visual y espacial no lineal del frame I t .

Podemos abstraer esta transformaci´ on de la siguiente manera:

<!-- formula-not-decoded -->

Debido a que no se hace uso de redes recurrentes, para que el modelo pueda incorporar noci´ on de orden entre los frames, se agregan codificaciones posicionales:

<!-- formula-not-decoded -->


<!-- page 61 -->

La codificaci´ on que PositionalEncoding abstrae es la que se introdujo en la secci´ on de Transformers, y la presentada por Vaswani et al.

## Embeddings de palabras

En paralelo, las palabras del lenguaje hablado (ej. alem´ an en el dataset PHOENIX-2014T) se representan con embeddings producto de una proyecci´ on lineal, al igual que en NMT:

<!-- formula-not-decoded -->

y tambi´ en se les agrega codificaci´ on posicional:

<!-- formula-not-decoded -->

## Sign Language Recognition Transformer (SLRT)

El Sign Language Recognition Transformer (SLRT) es el componente encargado de reconocer secuencias de glosas a partir de un video continuo de se˜ nas, al mismo tiempo que aprende representaciones espaciotemporales ´ utiles para la posterior traducci´ on.

El proceso comienza con la secuencia de spatial embeddings de cada frame del video, ˆ f 1: T , a los cuales ya se les ha sumado la codificaci´ on posicional. Estos vectores son la entrada del encoder Transformer, que se encarga de modelar las dependencias temporales entre los distintos frames.

El encoder se compone de capas de self-attention y feed-forward, cada una seguida de residual connections y normalizaci´ on, siguiendo el dise˜ no est´ andar de los Transformers. Gracias a esto, el modelo es capaz de relacionar un frame con todos los dem´ as de la secuencia, capturando as´ ı contexto de largo alcance que resulta esencial en el lenguaje de se˜ nas, donde un mismo gesto puede extenderse en el tiempo y su interpretaci´ on depende de los gestos anteriores y posteriores.

Formalmente, la representaci´ on del frame I t queda definida como:

<!-- formula-not-decoded -->

donde z t es la representaci´ on contextualizada del frame t , calculada considerando toda la secuencia de entrada.

## Supervisi´ on intermedia y CTC

El SLRT no solo aprende a producir representaciones ´ utiles para la traducci´ on, sino que tambi´ en se lo entrena directamente para reconocer glosas. La dificultad est´ a en que las glosas no vienen alineadas frame a frame: una misma glosa puede abarcar varios frames, y en el dataset no suele haber anotaciones tan finas.


<!-- page 62 -->

Para resolver este problema, en lugar de entrenar ´ unicamente con entrop´ ıa cruzada a nivel de frame, se utiliza la t´ ecnica de Connectionist Temporal Classification (CTC) [41]. Este m´ etodo permite entrenar el modelo con anotaciones m´ as d´ ebiles: solo necesita la secuencia completa de glosas en el orden correcto, sin indicar d´ onde empieza y termina cada una.

El procedimiento es el siguiente:

1. Cada vector z t se proyecta con una capa lineal seguida de una softmax, obteniendo probabilidades sobre el vocabulario de glosas m´ as un s´ ımbolo especial de blank. 2. La CTC se encarga de marginalizar todas las posibles alineaciones entre frames y glosas, asignando a cada trayectoria π (secuencia de glosas + blanks) una probabilidad:

<!-- formula-not-decoded -->

donde B ( G ) es el conjunto de trayectorias que colapsan en la secuencia de glosas G .

3. El modelo se entrena maximizando la probabilidad de la secuencia de glosas real G ∗ . La p´ erdida de reconocimiento se define como:

<!-- formula-not-decoded -->

Gracias a esta supervisi´ on intermedia, el SLRT aprende representaciones que no solo capturan la din´ amica visual del video, sino que adem´ as est´ an alineadas con el vocabulario de glosas. Esto resulta fundamental porque:

- Permite que el encoder est´ e guiado por un objetivo ling¨ u´ ıstico claro (las glosas), y no solo por el de traducci´ on final.
- Aporta informaci´ on adicional durante el entrenamiento, lo que mejora el aprendizaje conjunto con el SLTT (el decoder de traducci´ on).
- Facilita la generalizaci´ on, ya que el modelo aprende a reconocer estructuras b´ asicas del lenguaje de se˜ nas antes de abordar la tarea m´ as compleja de traducir al lenguaje hablado.

## Sign Language Translation Transformer (SLTT)

El objetivo final de la arquitectura propuesta por Camgoz et al. es generar oraciones en lenguaje hablado a partir de la representaci´ on de un video en lengua de se˜ nas. Para esto, introducen el Sign Language Translation Transformer (SLTT), un decoder de tipo Transformer entrenado de manera autoregresiva, es decir, generando la oraci´ on palabra por palabra.


<!-- page 63 -->

El SLTT aprovecha las representaciones espaciotemporales previamente aprendidas por el Sign Language Recognition Transformer (SLRT), que funciona como encoder. El proceso comienza tomando la oraci´ on objetivo S en el lenguaje hablado y a˜ nadiendo al inicio el token especial de comienzo de oraci´ on &lt;BOS&gt; . Luego, como vimos al inicio cada palabra m u se convierte en un word embedding con codificaci´ on posicional, resultando en ˆ m u .

Estos embeddings se pasan por una capa de masked self-attention para asegurar que cada palabra solo pueda acceder al contexto de las palabras anteriores en la secuencia, nunca a las futuras. Una vez obtenidas estas representaciones internas, se combinan con las salidas del SLRT mediante un bloque de encoder-decoder attention, que es el encargado de aprender el alineamiento entre la secuencia de entrada (video) y la secuencia de salida (oraci´ on). Finalmente, los resultados pasan por una capa feed-forward no lineal aplicada posici´ on por posici´ on. Como en cualquier Transformer est´ andar, todas estas operaciones van seguidas de conexiones residuales y normalizaci´ on por capas, lo que facilita la estabilidad y el entrenamiento profundo del modelo.

De manera formal, el proceso de decodificaci´ on en el paso u +1 se describe como:

<!-- formula-not-decoded -->

donde z 1: T son las representaciones del video generadas por el encoder (SLRT), y ˆ m 1: u -1 son los embeddings posicionales de las palabras previamente generadas.

El SLTT genera la oraci´ on de forma iterativa, palabra a palabra, hasta producir el token especial de fin de oraci´ on &lt;EOS&gt; . Para modelar la probabilidad de toda la oraci´ on, se descompone la probabilidad condicional de secuencia en una cadena de probabilidades condicionales ordenadas:

<!-- formula-not-decoded -->

donde cada p ( w u | h u ) corresponde a la probabilidad de que el modelo genere la palabra w u dado el estado oculto en el paso u .

El entrenamiento del decoder se realiza minimizando la p´ erdida de entrop´ ıa cruzada ( L T ), que compara las distribuciones de probabilidad predichas para cada palabra con la distribuci´ on real (donde la palabra correcta tiene probabilidad 1 y el resto 0). Formalmente:


<!-- page 64 -->

<!-- formula-not-decoded -->

donde D es el tama˜ no del vocabulario y p ( ˆ w d u ) representa la probabilidad real (ground truth) de la palabra w d en el paso u .

Finalmente, todo el sistema se entrena de manera multi-tarea, combinando la p´ erdida de reconocimiento de glosas ( L R , obtenida con CTC en el SLRT) y la p´ erdida de traducci´ on L T en una sola funci´ on objetivo:

<!-- formula-not-decoded -->

donde λ R y λ T son hiperpar´ ametros que permiten ajustar la importancia relativa de cada tarea. De esta manera, el modelo aprende simult´ aneamente a reconocer glosas y a traducir a lenguaje hablado, reforzando mutuamente ambos aprendizajes.

## 4.2.2. Rendimiento

Para probar el rendimiento de este modelo, Camgoz et al. (2020) tambi´ en utilizaron las m´ etricas BLEU-1, BLEU-2, BLEU-3 y BLEU-4, calculadas sobre el corpus de la lengua de se˜ nas alemana RWTH-PHOENIX-Weather 2014T.

En comparaci´ on con su trabajo anterior basado en CNNs y RNNs (Camgoz et al., 2018), el uso de Transformers produjo una mejora sustancial en todas las m´ etricas en la tarea de traducci´ on de se˜ na a texto de forma directa. Los resultados se pueden ver en la tabla 2:

Tabla 2: Comparaci´ on de resultados BLEU entre modelos CNN+RNN (2018) y Transformer (2020).

| M´ etrica   | CNN+RNN (2018)   | Transformer (2020)   |
|-------------|------------------|----------------------|
| BLEU-1      | 32.24%           | 45.34%               |
| BLEU-2      | 19.03%           | 32.31%               |
| BLEU-3      | 12.83%           | 24.83%               |
| BLEU-4      | 9.58%            | 20.17%               |

Como podemos ver, estos resultados confirman que los transformers logran una mejor traducci´ on en comparaci´ on a los modelos basados en CNNs+RNNs. El rendimiento de los transformers duplica el desempe˜ no obtenido por los modelos recurrentes.


<!-- page 65 -->

## 4.3. Modelo basado en keypoints

En parelelo al desarrollo de modelos que se alimentan con videos crudos, han surgido modelos que utilizan puntos clave (keypoints) como representaci´ on intermedia de la se˜ na [42] [12] [43] [44]. Estos keypoints se obtienen a partir de estimadores de pose (por ejemplo, MediaPipe) que extraen autom´ aticamente coordenadas de manos, rostro y cuerpo en cada cuadro del video. De esta manera, en lugar de procesar directamente miles de p´ ıxeles por frame, el modelo trabaja con vectores que codifican ´ unicamente la estructura corporal y gestual del signo.

La principal ventaja de este enfoque es la eficiencia: los modelos basados en keypoints suelen tener una complejidad param´ etrica mucho menor que aquellos que parten del video crudo, lo cual los hace m´ as adecuados para contextos con recursos limitados y para aplicaciones en tiempo real. Adem´ as, al centrarse en la geometr´ ıa de la se˜ na, estos modelos son menos sensibles a variaciones de fondo, iluminaci´ on o apariencia del signante [42].

Dentro de esta l´ ınea, se destacan los trabajos gloss-free que combinan un encoder convolucional de secuencias de poses con un Transformer para la generaci´ on en lenguaje natural. Estos modelos demuestran que es posible obtener resultados favorables sin depender de glosas intermedias, a la vez que se reduce el tama˜ no y la complejidad de la red.

En el caso particular de la Lengua de Se˜ nas Argentina (LSA), esta aproximaci´ on cobra especial relevancia dado que el ´ unico dataset disponible ya contiene los keypoints para ponerlos a prueba. Por esta raz´ on, en el presente trabajo se adopta este enfoque y se lo eval´ ua en el corpus LSA-T, que se describe en detalle en la secci´ on 5. Posteriormente, en la secci´ on 6, se profundizar´ a en la arquitectura del modelo basado en keypoints implementado.


<!-- page 66 -->

## 5. LSA-T: Datos para la Traducci´ on Autom´ atica de LSA

En esta secci´ on vamos a explorar el conjunto de datos LSA-T.

## 5.1. Estructura del Dataset y Metadatos Asociados

Como se mencion´ o anteriormente, este conjunto de datos fue creado a partir de videos del canal de YouTube CN Sordos, y contiene un total de 8459 clips individuales. Cada clip es un fragmento de video que contiene una oraci´ on o segmento de una oraci´ on en LSA, acompa˜ nado por su traducci´ on al espa˜ nol. Los clips de video se almacenan en formato .mp4, con resoluci´ on 1920x1080 y 30 frames por segundo. Los mismos tienen una duraci´ on promedio de 9.36 segundos, con una duraci´ on m´ ınima de 0.58 segundos y m´ axima de 83.23 segundos. En la figura 21 podemos ver la distribuci´ on de la duraci´ on de los clips. Los nombres de archivo est´ an compuestos por un identificador ´ unico (id) que tambi´ en sirve como clave de acceso para los archivos auxiliares asociados a cada clip, incluyendo el archivo de puntos claves (keypoints.h5) y el archivo tabular (meta.csv) que consolida todos los metadatos relevantes del dataset.


<!-- page 67 -->

Figura 21: Distribuci´ on de la duraci´ on de los clips en el conjunto de datos LSA-T

<!-- image -->

Cada entrada en meta.csv contiene, adem´ as del id, la traducci´ on al espa˜ nol (label), el t´ ıtulo del video original (video), el nombre de la lista de reproducci´ on (playlist), los tiempos de inicio y fin dentro del video original (start, end) y la duraci´ on total del clip (duration). Tambi´ en se indica si la oraci´ on fue segmentada en varios fragmentos y a qu´ e segmento pertenece (splits). Se incluyen adem´ as, ajustes temporales (prev delta, post delta) para evitar recortes bruscos del inicio o final del gesto. Tambi´ en se tiene un indicado de la cantidad de personas presentes en el clip (signers amount). A partir de esta informaci´ on, se realiz´ o una inferencia para identificar cu´ al de las personas presentes era el/la firmante principal. Esta persona se identifica mediante un ´ ındice (infered signer) que permite acceder a sus keypoints en el archivo correspondiente, y se proporciona adem´ as una medida de confianza (infered signer confidence) entre 0 y 1 que indica la seguridad de esta inferencia.

Por otro lado, el archivo keypoints.h5 contiene los puntos clave (keypoints) de cada persona detectada en cada clip. Estos keypoints represen- tan coordenadas anat´ omicas del cuerpo humano, obtenidas autom´ aticamente (usando modelos espec´ ıficos) a partir de cada frame del video mediante t´ ecnicas de estimaci´ on de pose. Cada punto indica la posici´ on en pantalla (en coordenadas relativas) de una parte del cuerpo, como una articulaci´ on, un dedo o una regi´ on del rostro.


<!-- page 68 -->

En la publicaci´ on original del dataset [4] se menciona que para obtener los puntos clave se utiliz´ o AlphaPose con el modelo Halpe FullBody, que define 136 keypoints por persona. Sin embargo, al inspeccionar los datos, se observa que cada frame contiene 543 puntos, lo cual no corresponde al modelo Halpe, sino que coincide con la cantidad de puntos proporcionados por el modelo MediaPipe Holistic, que integra cuerpo, manos y rostro con mayor granularidad. Esta discrepancia sugiere una diferencia en la documentaci´ on original del dataset, y fue tenida en cuenta al momento de procesar los datos.

El archivo est´ a organizado jer´ arquicamente: la primera capa de grupos corresponde al id del clip, y dentro de cada uno se encuentra un grupo por cada persona detectada (signer 0, signer 1, etc.). En cada grupo se almacenan dos objetos: keypoints y boxes.

```
clip_1.mp4 (Nivel 1: Video clip) signer_0 (Nivel 2: Signante detectado) boxes: (frames, 4 columnas) (Nivel 3a) keypoints: (frames, 2172 columnas) (Nivel 3b) signer_1 (Signante adicional si existe) boxes: (frames, 4 columnas) keypoints: (frames, 2172 columnas) signer_N (Hasta 5 signantes por clip) clip_2.mp4 ... clip_8459.mp4
```

Los keypoints est´ an representados como matrices de forma (frames, 2172), donde frames es la cantidad de cuadros del video (var´ ıa seg´ un su duraci´ on), y 2172 corresponde a los datos de 543 keypoints por frame. Cada keypoint aporta 4 valores: coordenadas x , y , z y visibility . Estos cuatro valores est´ an almacenados de forma aplanada (flattened), es decir, todos seguidos en una ´ unica dimensi´ on, lo que da como resultado 543 × 4 = 2172 columnas por frame. En cuanto a los boxes, cada frame contiene una caja delimitadora que indica la regi´ on donde fue detectada la persona. Para ilustrar la organizaci´ on y el contenido del conjunto de datos, en la tabla 3 se presenta una entrada real del archivo meta.csv, junto con los primeros valores de los archivos keypoints.h5 y boxes correspondientes al firmante principal.


<!-- page 69 -->

Tabla 3: Ejemplo de metadatos asociados a un clip de video en el dataset LSA-T.

| ID del clip     | agua-como-tomar-conciencia-sobre-su-cuidado-episodio- 3-en-lengua-de-senas-argentina-lsa 32.mp4                                                                                                                                                                                                                                                                                                                                                      |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Transcripci´ on | actualmenmte existe mucha preocupaci´ on en todo lo que concierre a los recursos h´ ıdricos de todo el planeta, ya que en los ´ ultimos a˜ nos se ha venido notando una disminuci´ on significativa de los mismos por el uso indebido y el des- pilfarro debido a un crecimiento acelerado de la poblaci´ on en todo el mundo.                                                                                                                       |
| Categor´ ıa     | ecolog´ ıa                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Tiempos         | • Inicio del clip: 268.33 segundos • Fin del clip: 291.66 segundos • Duraci´ on total: 23.12 segundos • Tiempo desde el clip anterior ( prev delta ): 0.06 s • Tiempo hasta el siguiente clip ( post delta ): 0.06 s                                                                                                                                                                                                                                 |
| Segmentaci´ on  | 1. 'actualmenmte existe mucha preocupaci´ on en todo lo que concierre a los recursos' - [268.33, 271.30] 2. 'h´ ıdricos de todo el planeta, ya que en los ´ ultimos a˜ nos' - [271.36, 276.18] 3. 'se ha venido notando una disminuci´ on significativa de los mismos' - [276.24, 278.51] 4. 'por el uso indebido y el despilfarro debido a un crecimiento acelerado' - [278.57, 283.06] 5. 'de la poblaci´ on en todo el mundo.' - [283.12, 291.66] |
| Signantes       | Se identificaron dos personas en el clip ( signers amount = 2 ), siendo signer 0 el signante inferido como principal, con una confianza de 0.9857.                                                                                                                                                                                                                                                                                                   |
| Movimiento      | El nivel de movimiento observado fue de 867.44 para signer 0 y 12.58 para signer 1 , lo que refuerza la asig- naci´ on del primero como principal en la escena.                                                                                                                                                                                                                                                                                      |

El archivo keypoints con el mismo id contiene:

- Keypoints con forma (704, 2172): 704 frames, 543 puntos por frame con coordenadas x, y, z y visibility.


<!-- page 70 -->

- Boxes con forma (704,4): una caja delimitadora por frame.

## donde:

```
Keypoints shape: (704, 2172) Boxes shape: (704, 4) Primeros 5 frames de keypoints: [[ 1.294e+03 3.805e+02 nan ... 6.750e+02 -3.030e-02 nan] [ 1.294e+03 3.812e+02 nan ... 6.595e+02 -2.676e-02 nan] [ 1.294e+03 3.825e+02 nan ... 6.200e+02 -3.026e-02 nan] [ 1.294e+03 3.855e+02 nan ... 6.250e+02 -3.799e-02 nan] [ 1.294e+03 3.855e+02 nan ... 6.365e+02 -3.818e-02 nan]] Primeros 5 frames de boxes: [[1009. 204.8 1655. 1071. ] [1008.5 205.4 1652. 1072. ] [1001.5 208.2 1672. 1071. ] [ 989.5 209.2 1705. 1069. ] [ 981. 209.5 1725. 1070. ]] y si reestructuramos los keypoints en formato (543, 4) obtenemos: [ fila0: [ 1.294e+03 3.805e+02 nan 1.000e+00] fila1: [ 1.314e+03 3.422e+02 nan 1.000e+00] fila2: [ 1.329e+03 3.430e+02 nan 1.000e+00] ... fila540: [ 1.462e+03 6.655e+02 -3.778e-02 nan] fila541: [ 1.475e+03 6.625e+02 -3.354e-02 nan] fila542: [ 1.486e+03 6.750e+02 -3.030e-02 an]]
```

cada fila es la coordenada de un punto. Siguiendo el formato MediaPipe Holistic, tenemos que los keypoints est´ an ordenados de la siguiente forma:

- Filas 0-32: Cuerpo (pose) un total de 33 puntos.
- Filas 33-500: Rostro un total de 468 puntos.
- Filas 501-521: Mano izquierda un total de 21 puntos.
- Filas 522-542: Mano derecha un total de 21 puntos.


<!-- page 71 -->

En el caso de los keypoints de pose corporal (filas 0-32), cada fila contiene cuatro valores: x, y, z y visibility. Las coordenadas x e y indican la ubicaci´ on del punto en el plano 2D de la imagen, mientras que z corresponde a la profundidad relativa, aunque en este tipo de keypoints se encuentra asignada como NaN al trabajar solo en dos dimensiones. El campo visibility representa la probabilidad de que el punto sea visible en el cuadro, con valores entre 0 y 1.

Para los keypoints de rostro y manos (filas 33-542), tambi´ en se mantienen las cuatro columnas, pero en este caso la coordenada z s´ ı contiene informaci´ on de profundidad relativa respecto a la mu˜ neca (valores menores de z indican mayor cercan´ ıa a la c´ amara), mientras que el campo visibility no est´ a definido (NaN). La escala de z es aproximadamente equivalente a la de x.

## 5.2. Visualizaci´ on de keypoints y bounding boxes

Para entender la representaci´ on de los datos, mostramos los keypoints y las bounding boxes sobre el primer frame de un clip.

Figura 22: Keypoints del cuerpo detectados por MediaPipe Holistic en el frame 0. Se siguen 33 puntos clave que representan nariz, ojos, orejas, hombros, codos, mu˜ necas, manos, caderas, rodillas, tobillos y pies.

<!-- image -->

Los detalles completos de los 33 puntos se pueden consultar en https://ai.


<!-- page 72 -->

[google.dev/edge/mediapipe/solutions/vision/pose\_landmarker/index? hl=es-419 .](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/index?hl=es-419)

Figura 23: Keypoints faciales asignados por MediaPipe Holistic. Cada punto representa rasgos faciales detectables para un seguimiento preciso del rostro.

<!-- image -->


<!-- page 73 -->

Figura 24: Keypoints de la mano izquierda detectados. Cada mano est´ a representada por 21 puntos que marcan articulaciones y extremidades de los dedos.

<!-- image -->


<!-- page 74 -->

Figura 25: Keypoints de la mano derecha detectados. Cada mano est´ a representada por 21 puntos que marcan articulaciones y extremidades de los dedos.

<!-- image -->

Para m´ as informaci´ on sobre los keypoints de la mano, ver https://ai. google.dev/edge/mediapipe/solutions/vision/hand\_landmarker/index? hl=es-419 .


<!-- page 75 -->

Figura 26: Todos los keypoints combinados (cuerpo, rostro y manos) sobre el mismo frame.

<!-- image -->

## 5.3. Preprocesamiento

Durante la exploraci´ on inicial del dataset se detect´ o una cantidad significativa de valores faltantes (NaN) (aproximadamente el 97 % de los clips) lo cual es esperable en este tipo de datos ya que el extractor de poses (MediaPipe) no siempre logra detectar todos los puntos clave. Estos faltantes suelen aparecer en tres escenarios: (i) al inicio o final de un clip, cuando la persona todav´ ıa no ingres´ o al cuadro o ya sali´ o de ´ el; (ii) en frames intermedios, debido a oclusiones parciales o movimientos r´ apidos; y (iii) en secuencias completas donde no fue posible estimar un subconjunto de puntos (ej. una mano).

Para tratar estas ausencias se implement´ o un esquema de imputaci´ on basado en tres pasos, siguiendo pr´ acticas reportadas en la literatura [45]:

1. Interpolaci´ on lineal: aplicada cuando existen frames v´ alidos antes y despu´ es del valor faltante. Cada punto se imputa interpolando linealmente entre las coordenadas detectadas en los frames adyacentes.
2. Extrapolaci´ on: utilizada en los extremos de la secuencia. Si los valores faltantes ocurren al inicio, se replican los del primer frame v´ alido; si ocurren al final, se copian los del ´ ultimo frame v´ alido.


<!-- page 76 -->

3. Imputaci´ on con ceros: en casos en los que un subconjunto completo de keypoints (ej. toda una mano) no fue detectado a lo largo de la secuencia, se imputan coordenadas (0, 0) para todos sus puntos.

Adicionalmente, se restringi´ o la representaci´ on a coordenadas 2D (x, y), descartando las componentes de profundidad (z) y visibilidad que produce MediaPipe. Esto es porque las proyecciones 2D son suficientes para capturar la estructura relativa de la pose y, al mismo tiempo, reducen la dimensionalidad de la entrada de 2172 a 1086 caracter´ ısticas por frame.

Finalmente, se aplic´ o un proceso de normalizaci´ on para cada frame de keypoints. En este procedimiento, se toman por separado todas las coordenadas x y todas las coordenadas y de los puntos del cuerpo, se calcula su mediana y su desviaci´ on absoluta, y luego se normaliza cada valor restando la mediana y dividiendo por la desviaci´ on correspondiente. De este modo, se reducen las diferencias debidas a la posici´ on y escala absolutas del signante en el cuadro, permitiendo que el modelo se centre en la estructura relativa de la pose [46].


<!-- page 77 -->

## 6. Modelos aplicado a LSA-T

## 6.1. Modelo basado en keypoints

Como punto de partida para esta parte, se tom´ o como referencia la arquitectura propuesta por Dal Bianco et al. (2024) [12], el ´ unico modelo existente para la traducci´ on autom´ atica de la LSA. La decisi´ on de utilizar esta arquitectura se bas´ o en su adecuaci´ on al tipo de datos disponibles. Sin embargo con el fin de reproducir los resultados presentados por el art´ ıculo original, surgieron diversas ambig¨ uedades asociadas a la falta de precisi´ on en la descripci´ on metodol´ ogica del art´ ıculo original.

En particular, se identificaron las siguientes limitaciones:

- Algunos de los detalles en la arquitectura presentados en el paper resultaban ambiguos.
- No se brindaban detalles suficientes sobre el preprocesamiento aplicado a los datos ni sobre los criterios utilizados para la elecci´ on de los hiperpar´ ametros.

Es por esto que los resultados reportados no pudieron ser reproducidos fielmente. Se opt´ o por experimentar con una implementaci´ on inspirada en los lineamientos generales del modelo original pero con adaptaciones necesarias para garantizar su funcionamiento y reproducibilidad. Esta versi´ on conserva la esencia del enfoque propuesto, pero incorpora otras decisiones sobre el preprocesamiento y la elecci´ on de los hiperpar´ ametros.

La arquitectura propuesta por Dal Bianco et al. (2024) representada en la figura 27, utiliza exclusivamente informaci´ on de keypoints obtenida a partir de videos de se˜ nas, lo que permite reducir la dimensionalidad de los datos y eliminar factores de ruido como fondo, iluminaci´ on y vestimenta. La arquitectura general responde a un esquema encoder-decoder basado en Transformers, con un m´ odulo de convoluciones 1D para el preprocesamiento de los keypoints y un m´ odulo de embeddings para las palabras.


<!-- page 78 -->

Figura 27: Arquitectura propuesta por Dal Bianco et al. proveniente de [12].

<!-- image -->

## Embedding de los keypoints

Como vimos, cada frame de video en LSA-T se representa mediante 543 keypoints, distribuidos en 33 del cuerpo, 21 por cada mano y 468 del rostro. Dado que cada punto incluye ´ unicamente las coordenadas ( x, y ) (omitiendo visibilidad y confianza), cada frame se codifica como un vector plano de 1086 dimensiones. De este modo, una secuencia de T frames puede representarse como una matriz:

<!-- formula-not-decoded -->

donde T corresponde a la cantidad de frames de la secuencia. Como los videos poseen longitudes variables, es necesario unificar las dimensiones para procesar lotes (batches) en paralelo. Esto se resuelve en dos pasos complementarios:

1. Padding din´ amico: dentro de cada batch, todas las secuencias se rellenan con ceros hasta alcanzar la longitud del video m´ as largo del lote.
2. M´ ascara de atenci´ on: se construye una m´ ascara binaria (1 = frame v´ alido, 0 = padding) que se propaga al Transformer. De esta manera, el mecanismo de autoatenci´ on ignora las posiciones correspondientes al padding, evitando que influyan en el aprendizaje.


<!-- page 79 -->

Las secuencias de vectores resultantes se proyectan hacia un espacio de representaci´ on m´ as compacto y expresivo, preservando la estructura espacial de los keypoints. Para ello, se emplea un Pose Encoder compuesto por tres capas convolucionales 1D con kernel de tama˜ no 1. Estas convoluciones act´ uan ´ unicamente sobre la dimensi´ on de caracter´ ısticas (features), sin incorporar contexto temporal entre frames.

La arquitectura tiene la siguiente forma:

<!-- formula-not-decoded -->

Donde cada capa realiza los siguientes pasos:

- Convoluci´ on 1D con kernel de tama˜ no 1: Permite combinar las coordenadas de los distintos keypoints sin considerar relaciones temporales entre frames.
- ReLU: introduce no linealidad para modelar combinaciones complejas de poses.
- Dropout: desactiva aleatoriamente un porcentaje de las neuronas durante el entrenamiento, evitando que el modelo dependa de keypoints espec´ ıficos y promoviendo representaciones m´ as robustas y generalizables.

Se ilustra el proceso de estas capas en la figura 28.

Figura 28: Ilustraci´ on del pasaje de los keypoints de un frame a trav´ es de las convoluciones y activaci´ on con ReLU.

<!-- image -->


<!-- page 80 -->

Los pesos de cada convoluci´ on se inicializan usando Xavier initialization [47], y los sesgos (bias) se inicializan en cero. Este proceso en total transforma cada frame en un vector de embedding de dimensi´ on fija d model = 256.

Se detalla la implementaci´ on del Pose Encoder aqu´ ı abajo:

```
class PoseEncoder(nn.Module): def __init__(self, input_dim: int = 1086, # 543 keypoints d_model: int = 256, # Output dropout: float = 0.2): # Dropout super(PoseEncoder, self).__init__() self.input_dim = input_dim self.d_model = d_model # Reducci´ on gradual del espacio intermediate_dim1 = max(d_model * 4, d_model) intermediate_dim2 = max(d_model * 2, d_model) # 3 convoluciones con tama~ no de kernel = 1 self.conv1 = nn.Conv1d( in_channels=input_dim, out_channels=intermediate_dim1, kernel_size=1, bias=True ) self.conv2 = nn.Conv1d( in_channels=intermediate_dim1, out_channels=intermediate_dim2, kernel_size=1, bias=True ) self.conv3 = nn.Conv1d( in_channels=intermediate_dim2, out_channels=d_model, kernel_size=1, bias=True )
```


<!-- page 81 -->

```
# Dropout para la regularizaci´ on self.dropout = nn.Dropout(dropout) # Inicializaci´ on de pesos self._init_weights() def _init_weights(self): for conv in [self.conv1, self.conv2, self.conv3]: nn.init.xavier_uniform_(conv.weight) nn.init.zeros_(conv.bias) def forward(self, x: torch.Tensor) -> torch.Tensor: # Conv1D espera algo de la forma (batch_size, channels, sequence_length) ↪ → # Se pasa de (batch, seq, features) a(batch, features, seq) ↪ → x = x.transpose(1, 2) # (batch_size, input_dim, seq_len) ↪ → # Primera convolucin, (batch_size, intermediate_dim1, seq_len) ↪ → x = self.conv1(x) # transformamos de 1086 a 1024 x = F.relu(x) x = self.dropout(x) # Segunda convolucin, (batch_size, intermediate_dim2, seq_len) ↪ → x = self.conv2(x) # transformamos de 1024 a 512 x = F.relu(x) x = self.dropout(x) # Tercera convoluci´ on, (batch_size, d_model, seq_len) x = self.conv3(x) # transformamos de 512 a 256 x = F.relu(x) x = self.dropout(x) # Se vuelve a la forma (batch, seq, features) x = x.transpose(1, 2) # (batch_size, seq_len, d_model) ↪ → return x
```


<!-- page 82 -->

## Codificaci´ on posicional

Al resultado de las convoluciones se le a˜ nade un codificador posicional (el mismo ya visto en secciones anteriores), con el fin de preservar el orden temporal de los frames. Dado que las convoluciones no retienen expl´ ıcitamente la posici´ on global de cada frame, este paso es clave para que el modelo distinga la secuencia de los gestos y no solo su contenido est´ atico. El resultado final se pasa el encoder del Transformer para procesarlos.

Se detalla la implementaci´ on del codificador posicional aqu´ ı abajo:

```
class PositionalEncoding(nn.Module): def __init__(self, d_model: int, max_length: int, dropout: float): ↪ → super(PositionalEncoding, self).__init__() self.d_model = d_model self.dropout = nn.Dropout(dropout) # Se crea la matriz de codificaci´ on posicional pe = torch.zeros(max_length, d_model) position = torch.arange(0, max_length, dtype=torch.float).unsqueeze(1) ↪ → # T´ erminos de divsisi´ on por frecuencias div_term = torch.exp(torch.arange(0, d_model, 2).float() * ↪ → (-math.log(10000.0) / d_model)) # Se aplica seno a los ´ ındices pares pe[:, 0::2] = torch.sin(position * div_term) # Se aplica coseno a los ´ ındices impares pe[:, 1::2] = torch.cos(position * div_term) # Se agrega la dimensin del batch y se guarda en el buffer ↪ → pe = pe.unsqueeze(0).transpose(0, 1) # (max_length, 1, d_model) ↪ → self.register_buffer('pe', pe) def forward(self, x: torch.Tensor) -> torch.Tensor:
```


<!-- page 83 -->

```
# forma de x: (batch_size, seq_len, d_model) seq_len = x.size(1) # Se agrega la codificaci´ on posicional # pe[:seq_len, :] tiene forma (seq_len, 1, d_model) # Se suma a todo elemento en el batch x = x + self.pe[:seq_len, :].transpose(0, 1) # (1, seq_len, d_model) ↪ → return self.dropout(x)
```

## Vocabulario y tokenizaci´ on

Mientras que el encoder procesa las secuencias de keypoints, el decoder recibe como entrada la representaci´ on del texto en espa˜ nol generado hasta el momento, y se encarga de producir la secuencia de salida palabra por palabra. Veamos a continuaci´ on como se realiza este procesamiento.

El primer paso para procesar el texto consiste en construir un vocabulario a partir de todas las transcripciones disponibles en el corpus. Cada oraci´ on es dividida en unidades l´ exicas elementales (tokens), mediante un procedimiento de tokenizaci´ on basado en reglas simples que segmenta palabras y signos de puntuaci´ on. A cada token se le asigna un identificador num´ erico ´ unico, garantizando la existencia de los s´ ımbolos especiales como &lt;SOS&gt; (start of sequence), &lt;EOS&gt; (end of sequence), &lt;PAD&gt; (relleno para padding) y &lt;UNK&gt; (palabra desconocida). La tokenizaci´ on la realizaremos a nivel palabra [12].

Por ejemplo, la oraci´ on:

```
"Hola mundo"
```

se convierte en la secuencia de tokens:

```
["Hola", "mundo"]
```

Tras a˜ nadir los delimitadores de inicio y fin de secuencia, obtenemos:

```
["<SOS>", "Hola", "mundo", "<EOS>"]
```

y finalmente, al mapear cada token a su identificador en el vocabulario, se obtiene una representaci´ on num´ erica:

```
[1, 57, 83, 2]
```

donde 1 corresponde a &lt;SOS&gt; , 57 a Hola , 83 a mundo , y 2 a &lt;EOS&gt; . De forma similar, una oraci´ on con signos de puntuaci´ on, como:


<!-- page 84 -->

"¿C´ omo est´ as?" se tokeniza de la siguiente manera: ["¿", "C´ omo", "est´ as", "?"] y su versi´ on codificada ser´ ıa, por ejemplo: [1, 91, 102, 37, 15, 2]

La existencia de estos identificadores permite que oraciones de longitud variable se representen como secuencias de n´ umeros, lo cual constituye el puente entre las cadenas de texto y la representaci´ on num´ erica necesaria para entrenar redes neuronales profundas. El vocabulario final re´ une un total de 13664 palabras, incluyendo tambi´ en algunos s´ ımbolos.

C´ odigo de implementaci´ on de las funcionalidades principales:

## class Vocabulary:

```
# Tokens especiales PAD_TOKEN = '<PAD>' SOS_TOKEN = '<SOS>' # Start of sequence EOS_TOKEN = '<EOS>' # End of sequence UNK_TOKEN = '<UNK>' # Unknown token PAD_IDX = 0 SOS_IDX = 1 EOS_IDX = 2 UNK_IDX = 3 def __init__(self, min_freq: int = 1, max_vocab_size: Optional[int] = None, lowercase: bool = True): self.min_freq = min_freq self.max_vocab_size = max_vocab_size self.lowercase = lowercase # Inicializaci´ on con tokens especiales self.word2idx = { self.PAD_TOKEN: self.PAD_IDX, self.SOS_TOKEN: self.SOS_IDX, self.EOS_TOKEN: self.EOS_IDX,
```


<!-- page 85 -->

```
self.UNK_TOKEN: self.UNK_IDX } self.idx2word = { self.PAD_IDX: self.PAD_TOKEN, self.SOS_IDX: self.SOS_TOKEN, self.EOS_IDX: self.EOS_TOKEN, self.UNK_IDX: self.UNK_TOKEN } self.word_freq = Counter() self._is_built = False def add_sentence(self, sentence: str) -> None: """ Agrega una oracin al contador de frecuencias. ↪ → """ words = self.tokenize(sentence) self.word_freq.update(words) def build_vocab(self) -> None: """ Construye el vocabulario a partir de las frecuencias recopiladas. ↪ → """ # Obtiene palabras que cumplen con la frecuencia mnima ↪ → valid_words = [word for word, freq in self.word_freq.items() ↪ → if freq >= self.min_freq] # Ordena por frecuencia (descendente) valid_words.sort(key=lambda x: self.word_freq[x], reverse=True) ↪ → # Aplica l´ ımite de tama~ no m´ aximo if self.max_vocab_size is not None: # Reserve space for special tokens
```


<!-- page 86 -->

```
max_words = self.max_vocab_size -len(self.word2idx) ↪ → valid_words = valid_words[:max_words] # Agrega las palabras al vocabulario for word in valid_words: if word not in self.word2idx: idx = len(self.word2idx) self.word2idx[word] = idx self.idx2word[idx] = word self._is_built = True print(f"Built vocabulary with {len(self.word2idx)} words") ↪ → print(f"Most frequent words: {valid_words[:10]}") def tokenize(self, text: str) -> List[str]: """ Tokeniza un texto en palabras. """ if self.lowercase: text = text.lower() # Tokenizacin simple: separa por espacios y signos de puntuacin ↪ → tokens = re.findall(r'\b\w+\b|[^\w\s]', text) return tokens def encode(self, text: str, add_special_tokens: bool = True) -> List[int]: ↪ → """ Convierte un texto en una lista de indices de tokens. """ tokens = self.tokenize(text) indices = [] if add_special_tokens: indices.append(self.SOS_IDX)
```


<!-- page 87 -->

```
for token in tokens: idx = self.word2idx.get(token, self.UNK_IDX) indices.append(idx) if add_special_tokens: indices.append(self.EOS_IDX) return indices def decode(self, indices: List[int], remove_special_tokens: bool = True) -> str: ↪ → """ Convierte una lista de ndices de tokens nuevamente en texto. ↪ → """ words = [] for idx in indices: if idx in self.idx2word: word = self.idx2word[idx] if remove_special_tokens and word in [self.PAD_TOKEN, self.SOS_TOKEN, self.EOS_TOKEN]: ↪ → ↪ → continue words.append(word) else: words.append(self.UNK_TOKEN) return ' '.join(words)
```

## Embeddings de las palabras

Los identificadores enteros del vocabulario no contienen informaci´ on sem´ antica por s´ ı mismos: el n´ umero 57 puede representar la palabra 'hola', pero el valor 57 no tiene ninguna relaci´ on intr´ ınseca con su significado ling¨ u´ ıstico. Para resolver este problema, el modelo utiliza una capa de word embeddings implementada como una tabla de b´ usqueda (lookup table), en la cual cada fila corresponde al vector asociado a un token del vocabulario.


<!-- page 88 -->

Supongamos que el vocabulario contiene 10000 palabras y que la dimensi´ on de embedding ( d model ) es 256. En ese caso, la capa de embeddings es una matriz de tama˜ no (10000 × 256), donde cada fila es el vector denso de 256 dimensiones de un token espec´ ıfico:

```
embedding_matrix = [ [e_PAD], # vector del token <PAD> [e_SOS], # vector del token <SOS> [e_EOS], # vector del token <EOS> [e_UNK], # vector del token <UNK> [e_hola], # vector de "hola" [e_mundo], # vector de "mundo" ... ]
```

Cuando una secuencia de tokens se representa como ´ ındices, por ejemplo:

```
[1, 57, 83, 2]
```

(el caso de 'hola mundo'), la capa de embeddings traduce cada ´ ındice en su vector correspondiente:

```
[ e_SOS, # vector en R^256 e_hola, # vector en R^256 e_mundo, # vector en R^256 e_EOS # vector en R^256 ]
```

El resultado es un tensor tridimensional de tama˜ no (batch size, seq len, d model), listo para ser procesado por las capas posteriores del decoder.

Estos vectores son inicializados aleatoriamente (con distribuci´ on normal escalada seg´ un la dimensi´ on del modelo) y se optimizan durante el entrenamiento mediante backpropagation. La ´ unica excepci´ on es el vector asociado al token &lt;PAD&gt; , que se mantiene fijo en cero para evitar que las posiciones de relleno influyan en las representaciones.

La implementaci´ on de los embeddings de texto es la que ofrece PyTorch.


<!-- page 89 -->

## Codificaci´ on posicional para las palabras

Al igual que en el procesamiento de los keypoints, los embeddings de palabras son enriquecidos con codificaci´ on posicional antes de ingresar al decoder. De este modo, el modelo incorpora informaci´ on sobre el orden de aparici´ on de los tokens en la oraci´ on, garantizando que se respete la estructura secuencial del espa˜ nol durante la generaci´ on del texto. El mecanismo es el mismo que en el caso de los keypoints.

## Encoder

Finalmente, tanto las representaciones visuales (keypoints + codificaci´ on posicional) como las representaciones textuales (embeddings + codificaci´ on posicional) se alimentan a un modelo Transformer encoder-decoder est´ andar. Este m´ odulo constituye el n´ ucleo de la arquitectura: es el responsable de alinear la secuencia de se˜ nas con la secuencia textual y de generar las traducciones en espa˜ nol.

En nuestro caso utilizamos un encoder compuesto por 2 capas [12], siguiendo lo reportado por Dal Bianco et al. Cada capa incluye los m´ odulos caracter´ ısticos de la arquitectura Transformer: multi-head self-attention para capturar dependencias entre los frames de la secuencia de se˜ nas, un bloque feed-forward position-wise y conexiones residuales con normalizaci´ on. El encoder transforma las representaciones visuales de los keypoints en una secuencia de vectores latentes contextualizados. Estas representaciones capturan relaciones temporales y sem´ anticas entre los distintos frames/keypoints, sirviendo como memoria que el decoder consulta para producir la traducci´ on textual.

## Decoder

El decoder se implement´ o con 6 capas [12]. Este m´ odulo recibe como entrada las secuencias parciales de texto generadas y, mediante masked self-attention y cross-attention sobre las representaciones latentes del encoder, produce palabra por palabra la traducci´ on final al espa˜ nol.

Como vimos anteriormente, el proceso de generaci´ on de las palabras se hace por pasos. En cada paso se calcula una distribuci´ on de probabilidad sobre todo el vocabulario, indicando cu´ al es la palabra m´ as probable que sigue en la traducci´ on. El proceso se repite paso a paso hasta generar el token de fin de secuencia &lt;EOS&gt; o alcanzar un m´ aximo predefinido. De todas maneras, al momento de implementarlo existen dos enfoques para realizar la generaci´ on:

- Greedy decoding: en cada paso el modelo selecciona ´ unicamente el token con mayor probabilidad, generando de forma secuencial hasta alcanzar


<!-- page 90 -->

- el token de fin &lt;EOS&gt; o hasta llegar a una secuencia de largo m´ aximo preestablecido. Este m´ etodo es r´ apido y eficiente, aunque propenso a errores acumulativos si una predicci´ on inicial es incorrecta.
- Beam search: en lugar de quedarse con una ´ unica secuencia, mantiene k candidatas en paralelo. En cada paso expande todas las secuencias y selecciona las k m´ as prometedoras seg´ un la probabilidad acumulada. Esto incrementa el costo computacional, pero suele mejorar la fluidez y la coherencia de las traducciones, especialmente en corpus peque˜ nos. El hiperpar´ ametro clave es el beam width (ej. 4, 8, 32). Un beam width demasiado grande puede incluso perjudicar la diversidad y sobreajustarse a traducciones cortas.

A continuaci´ on se muestra el c´ odigo de implementaci´ on de esta parte.

```
class Generator(nn.Module): """ Proyector final del modelo. Convierte la salida del Transformer en probabilidades sobre el vocabulario ↪ → mediante una capa lineal y log-softmax. """ def __init__(self, d_model: int, vocab_size: int): super().__init__() self.linear = nn.Linear(d_model, vocab_size) nn.init.xavier_uniform_(self.linear.weight) nn.init.zeros_(self.linear.bias) def forward(self, x: torch.Tensor) -> torch.Tensor: logits = self.linear(x) return F.log_softmax(logits, dim=-1) class SignLanguageTranslator(nn.Module): """ Modelo de traduccin de lengua de seas basado en Transformer (encoder-decoder). ↪ → """ def __init__(self, vocab_size: int, d_model: int = 256, encoder_layers: int = 2,
```


<!-- page 91 -->

```
decoder_layers: int = 6, num_heads: int = 8, d_ff: int = None, dropout: float = 0.2, max_seq_length: int = 5005, keypoint_dim: int = 1086, pad_idx: int = 0): super().__init__() if d_ff is None: d_ff = 4 * d_model self.vocab_size = vocab_size self.d_model = d_model self.pad_idx = pad_idx # 1. Codificador de poses (3 capas Conv1D) self.pose_encoder = PoseEncoder(input_dim=keypoint_dim, d_model=d_model, dropout=dropout) ↪ → # 2. Codificacin posicional (para secuencias visuales y textuales) ↪ → self.pos_encoding = PositionalEncoding(d_model=d_model, max_length=max_seq_length, dropout=dropout) ↪ → # 3. Embeddings textuales self.text_embeddings = nn.Embedding(vocab_size, d_model, padding_idx=pad_idx) ↪ → # 4. Transformer encoder-decoder est´ andar de PyTorch self.transformer = nn.Transformer( d_model=d_model, nhead=num_heads, num_encoder_layers=encoder_layers, num_decoder_layers=decoder_layers, dim_feedforward=d_ff, dropout=dropout, batch_first=True )
```

#

5.

Generador de distribuciones sobre el vocabulario


<!-- page 92 -->

```
self.generator = Generator(d_model, vocab_size) # Inicializaci´ on de embeddings nn.init.normal_(self.text_embeddings.weight, mean=0, std=d_model ** -0.5) ↪ → with torch.no_grad(): self.text_embeddings.weight[self.pad_idx].fill_(0) C´ odigo para la construcci´ on de m´ ascaras: def create_src_key_padding_mask(self, src: torch.Tensor, pad_value: float = 0.0) -> torch.Tensor: ↪ → """Mscara de padding para las secuencias de entrada (keypoints).""" ↪ → return (src.abs().sum(dim=-1) == pad_value) def create_tgt_key_padding_mask(self, tgt: torch.Tensor) -> torch.Tensor: ↪ → """Mscara de padding para las secuencias de salida (texto).""" ↪ → return (tgt == self.pad_idx) def create_tgt_mask(self, tgt_len: int, device: torch.device) -> torch.Tensor: ↪ → """Mscara triangular superior para el decoder (evita mirar al futuro).""" ↪ → return torch.triu(torch.ones(tgt_len, tgt_len, device=device), diagonal=1).bool() ↪ → Abstracciones para el encoder y decoder: def encode_poses(self, keypoints: torch.Tensor) -> torch.Tensor: ↪ → """Convierte secuencias de keypoints en representaciones latentes contextuales.""" ↪ → x = self.pose_encoder(keypoints) x = self.pos_encoding(x) return x def decode_text(self, tgt_tokens: torch.Tensor) -> torch.Tensor: ↪ →
```


<!-- page 93 -->

```
"""Convierte tokens textuales en embeddings con codificacin posicional.""" ↪ → x = self.text_embeddings(tgt_tokens) * math.sqrt(self.d_model) ↪ → x = self.pos_encoding(x) return x M´ etodo forward: def forward(self, keypoints: torch.Tensor, tgt_tokens: torch.Tensor, src_key_padding_mask: Optional[torch.Tensor] = None, ↪ → tgt_key_padding_mask: Optional[torch.Tensor] = None, ↪ → memory_key_padding_mask: Optional[torch.Tensor] = None) -> torch.Tensor: ↪ → """ Paso forward del modelo completo. Retorna las probabilidades logartmicas sobre el vocabulario. ↪ → """ device = keypoints.device tgt_len = tgt_tokens.size(1) # 1. Codificaci´ on de las se~ nas src = self.encode_poses(keypoints) # 2. Embeddings del texto tgt = self.decode_text(tgt_tokens) # 3. Creaci´ on de m´ ascaras if src_key_padding_mask is None: src_key_padding_mask = self.create_src_key_padding_mask(src) ↪ → if tgt_key_padding_mask is None: tgt_key_padding_mask = self.create_tgt_key_padding_mask(tgt_tokens) ↪ → if memory_key_padding_mask is None: memory_key_padding_mask = src_key_padding_mask
```


<!-- page 94 -->

```
def
```

```
tgt_mask = self.create_tgt_mask(tgt_len, device) # 4. Paso por el Transformer output = self.transformer( src=src, tgt=tgt, tgt_mask=tgt_mask, src_key_padding_mask=src_key_padding_mask, tgt_key_padding_mask=tgt_key_padding_mask, memory_key_padding_mask=memory_key_padding_mask ) # 5. Generacin de probabilidades sobre el vocabulario return self.generator(output) Generaci´ on Greedy: generate_greedy(self, keypoints: torch.Tensor, vocabulary: Vocabulary, max_length: int = 50) -> Tuple[torch.Tensor, torch.Tensor]: ↪ → """ Estrategia de generaci´ on greedy: en cada paso se selecciona el token ms probable hasta generar <EOS>. ↪ → """ self.eval() device = keypoints.device # 1. Codificar las se~ nas with torch.no_grad(): src = self.encode_poses(keypoints) src_mask = self.create_src_key_padding_mask(src) # 2. Inicializar secuencia con <SOS> generated = torch.full((1, 1), vocabulary.SOS_IDX, dtype=torch.long, device=device) ↪ → log_probs = torch.zeros(1, device=device) for _ in range(max_length - 1): tgt = self.decode_text(generated)
```


<!-- page 95 -->

```
tgt_mask = self.create_tgt_mask(generated.size(1), device) ↪ → out = self.transformer(src, tgt, tgt_mask=tgt_mask, src_key_padding_mask=src_ma ⌋ sk, ↪ → memory_key_padding_mask=src ⌋ _mask) ↪ → probs = self.generator(out)[:, -1, :] next_token = torch.argmax(probs, dim=-1, keepdim=True) ↪ → log_probs += torch.gather(probs, 1, next_token).squeeze(1) ↪ → generated = torch.cat([generated, next_token], dim=1) ↪ → if next_token.item() == vocabulary.EOS_IDX: break return generated, log_probs Generaci´ on Beam Search: def generate_beam_search(self, keypoints: torch.Tensor, vocabulary: Vocabulary, beam_size: int = 32, max_length: int = 50) -> Tuple[torch.Tensor, torch.Tensor]: ↪ → ↪ → """ Estrategia de generaci´ on beam search: mantiene las k secuencias m´ as probables en paralelo. """ self.eval() device = keypoints.device with torch.no_grad(): src = self.encode_poses(keypoints) src_mask = self.create_src_key_padding_mask(src) beam = [(torch.tensor([vocabulary.SOS_IDX], device=device), 0.0)] ↪ → completed = []
```


<!-- page 96 -->

```
for _ in range(max_length -1): candidates = [] for seq, score in beam: if seq[-1] == vocabulary.EOS_IDX: completed.append((seq, score)) continue seq_t = seq.unsqueeze(0) tgt = self.decode_text(seq_t) tgt_mask = self.create_tgt_mask(seq_t.size(1), device) ↪ → out = self.transformer(src, tgt, tgt_mask=tgt_mask, ↪ → src_key_padding_mask=sr ⌋ c_mask, ↪ → memory_key_padding_mask ⌋ =src_mask) ↪ → probs = self.generator(out)[0, -1, :] top_k_probs, top_k_idx = torch.topk(probs, beam_size) ↪ → for p, idx in zip(top_k_probs, top_k_idx): candidates.append((torch.cat([seq, idx.unsqueeze(0)]), score + p.item())) ↪ → candidates.sort(key=lambda x: x[1], reverse=True) beam = candidates[:beam_size] if not beam: break completed.extend(beam) best_seq, best_score = max(completed, key=lambda x: x[1]) ↪ → return best_seq.unsqueeze(0), torch.tensor([best_score]) ↪ →
```

Se puede ver el c´ odigo completo de este modelo en el repositorio de Github 9 .

## 6.1.1. Configuraci´ on de entrenamiento

Los entrenamientos, experimentos y evaluaciones se pudieron realizar gracias al uso de la computadora Nabucodonosor que forma parte del Centro de Computaci´ on de Alto Desempe˜ no (CCAD) de la Universidad Nacional de C´ ordoba, la cual cuenta con una CPU Intel Xeon CPU E5-2680 v2, RAM de 64GB, una GPU NVIDIA A30 y 24 GB de memoria HBM2.

9 https://github.com/juanbratti/KeypointsModel-LSA


<!-- page 97 -->

## Datos de Entrenamiento, Evaluaci´ on y Validaci´ on

Los datos se dividieron en tres subconjuntos mutuamente excluyentes con el fin de entrenar, validar y evaluar el modelo de traducci´ on. Primero, se filtraron los clips que no conten´ ıan keypoints v´ alidos, descartando aquellos en los que el extractor de poses (MediaPipe) no logr´ o detectar ning´ un signante. Tras esta eliminaci´ on, se obtuvo un total de 8457 clips v´ alidos.

- Entrenamiento (80 %): 6765 clips. Utilizados para ajustar los par´ ametros del modelo.
- Validaci´ on (10 %): 845 clips. Permiten ajustar hiperpar´ ametros y aplicar estrategias de early stopping.
- Evaluaci´ on/Test (10 %): 847 clips. Reservados exclusivamente para medir la capacidad de generalizaci´ on del modelo.

Este esquema asegura que ning´ un clip aparezca en m´ as de un subconjunto. Todos los experimentos se realizaron sobre estos mismos splits, lo cual garantiza la comparabilidad de resultados entre diferentes configuraciones de modelo y m´ etodos de decodificaci´ on.

## Hiperpar´ ametros

Los par´ ametros documentados aqu´ ı son par´ ametros que se tomaron como experimento inicial.

- Epochs (100): un epoch corresponde a una pasada completa sobre el conjunto de entrenamiento. En la pr´ actica, el modelo procesa los datos en lotes (batches) m´ as peque˜ nos y al finalizar un epoch habr´ a visto todos los ejemplos disponibles. Se fij´ o un m´ aximo de 100 epochs como tope.
- batch size (2): el batch size indica cu´ antos ejemplos se procesan simult´ aneamente antes de realizar una actualizaci´ on de los par´ ametros del modelo. En este trabajo se utiliz´ o un tama˜ no inicial de lote muy reducido (2 muestras por batch).
- Optimizador (AdamW): elegido por su buen desempe˜ no en Transformers [48], con β = (0 , 9 , 0 , 98) y ϵ = 10 -9 [37]. Este optimizador es un algoritmo que decide c´ omo actualizar los pesos del modelo en cada paso de entrenamiento al realizar backpropagation.


<!-- page 98 -->

- Learning rate (3e-5): controla el tama˜ no de los ajustes realizados a los par´ ametros internos (pesos) de un modelo durante cada paso del entrenamiento.
- Weight decay (0.01): penaliza pesos grandes para mejorar generalizaci´ on. B´ asicamente evita que los pesos obtenidos al realizar backpropagation no se descontrolen y que el modelo no se desestabilice.
- Scheduler (cosine annealing): ajusta din´ amicamente el learning rate siguiendo una curva coseno decreciente, lo que ayuda a una convergencia m´ as suave en entrenamientos largos.
- Grad clip (0.5): limita la magnitud de los gradientes para evitar explosiones de gradiente en secuencias largas. Si un gradiente tiene un valor muy grande, se recorta a 0.5. El gradiente es el vector de direcciones de descenso de la funci´ on de p´ erdida.
- Label smoothing (0.1): suaviza las etiquetas para evitar que el modelo se vuelva demasiado confiado en predicciones incorrectas, mejorando la generalizaci´ on. Un valor de 0.1 favorece el accuracy y el score de BLEU al menos en texto [37].

Se hizo uso del mecanismo de early stopping, el cual monitoriza la p´ erdida en el conjunto de validaci´ on y detiene autom´ aticamente el entrenamiento cuando no se observan mejoras durante un n´ umero determinado de ´ epocas consecutivas (en nuestro caso, 15). De esta manera, se evita el sobreajuste y se ahorra tiempo de c´ omputo, manteniendo el mejor modelo validado hasta ese punto. En el momento de entrenamiento, bast´ o con aproximadamente 55 ´ epocas para que el modelo se estabilice sin mejoras.

La funci´ on de p´ erdida usada fue la entrop´ ıa cruzada, la cual ya se introdujo en secciones anteriores [7] [40]. Adem´ as, al entrenar se emplea teacher forcing [49], una t´ ecnica com´ un en modelos secuencia a secuencia con decodificaci´ on autoregresiva. Este m´ etodo consiste en alimentar al decoder durante el entrenamiento con la secuencia de referencia correcta en lugar de con sus propias predicciones previas. De esta forma, el modelo recibe en cada paso el contexto adecuado, evitando la propagaci´ on de errores acumulativos durante la generaci´ on y acelerando la convergencia. En otras palabras, en lugar de que el modelo 'se alimente a s´ ı mismo' con lo que predijo (lo cual podr´ ıa ser incorrecto y desviar la secuencia completa), se le proporciona la respuesta real durante el entrenamiento. Esto favorece un aprendizaje m´ as estable y eficaz, aunque durante la inferencia, cuando las etiquetas verdaderas no est´ an disponibles, el modelo debe generar de manera autoregresiva bas´ andose ´ unicamente en sus propias salidas anteriores. La decisi´ on de usar teacher forcing es totalmente a modo de experimentaci´ on.


<!-- page 99 -->

El tiempo de entrenamiento para esta configuraci´ on fue de aproximadamente tres horas y media.

## 6.1.2. Configuraci´ on de evaluaci´ on

## M´ etricas de evaluaci´ on

Para medir el desempe˜ no del modelo se utilizaron las m´ etricas de BLEU-1, BLEU-2, BLEU-3, BLEU-4 ya introducidas en secciones anteriores, m´ as las siguientes:

- Word accuracy: esta m´ etrica mide cu´ antas palabras individuales coinciden con la referencia en la posici´ on correcta.

<!-- formula-not-decoded -->

- Sentence accuracy: Similar al Word Accuracy, esta m´ etrica calcula la proporci´ on de que la oraci´ on predicha sea exactamente igual a la referencia:

<!-- formula-not-decoded -->

Es mucho m´ as estricta que la Word Accuracy ya que con un error m´ ınimo en la predicci´ on, la oraci´ on completa se considera incorrecta.

Para el c´ alculo de BLEU-1/. . . /-4 se us´ o la funci´ on bleu score de la librer´ ıa NLTK.

## Resultados obtenidos

Siguiendo los hiperpar´ ametros detallados m´ as arriba, se muestran aqu´ ı abajo los resultados luego de entrenar y evaluar el modelo. La evaluaci´ on fue sobre 847 ejemplos del split de testeo.

Tabla 4: Resultados de evaluaci´ on del modelo sobre el conjunto de evaluaci´ on (847 ejemplos).

| Modelo                    | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|---------------------------|----------|----------|----------|----------|------------|------------|
| Greedy                    | 9.0%     | 3.0%     | 1.4%     | 0.8%     | 1.0%       | 0.0%       |
| Beam search beam width=32 | 6.8%     | 2.5%     | 1.2%     | 0.6%     | 0.7%       | 0.0%       |


<!-- page 100 -->

Resultados reportados por Dal Bianco et al. (2024) La siguiente tabla muestra los resultados reportados por Dal Bianco et al. cuyo modelo se basa en una arquitectura an´ aloga a la utilizada en este trabajo. Es importante tener en cuenta que estos valores no son directamente comparables, ya que el art´ ıculo original no detalla aspectos clave como el preprocesamiento, las definiciones exactas de las m´ etricas o el tama˜ no del conjunto de evaluaci´ on.

Tabla 5: Resultados reportados por Dal Bianco et al. para la tarea de traducci´ on autom´ atica de lengua de se˜ nas.

| Modelo                                 | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   |
|----------------------------------------|----------|----------|----------|----------|------------|
| Dal Bianco et al. (greedy)             | 6.4%     | 5.0%     | 0.3%     | 0.2%     | 16.7%      |
| Dal Bianco et al. (beam search, bw=32) | 6.7%     | 5.0%     | 0.1%     | 0.05%    | 16.7%      |

Los resultados del modelo muestran BLEU-1 ligeramente superiores a los de Dal Bianco et al. (2024), pero muestran un deterioro m´ as pronunciado en BLEU-2 y BLEU-3. La mayor diferencia se observa en Word Accuracy, donde nuestro modelo alcanza apenas 1 % frente al 16.7 % reportado por Dal Bianco et al.

De todas maneras, los resultados obtenidos en este experimento reafirman algunas de las conclusiones presentadas en el trabajo hecho por Dal Bianco et al. En primer lugar, el vocabulario de LSA-T es muy grande (en nuestro caso, luego del preprocesamiento el vocabulario suma un total de 13664 palabras incluyendo s´ ımbolos de puntuaci´ on y dem´ as). Adem´ as, en LSA-T, m´ as del 50 % de las palabras son palabras que aparecen una sola vez y el 96 % de las frases son ´ unicas. Esto lo que produce es que el modelo se entrena con frases y palabras que apenas aparecen, por eso es que el BLEU-1 nos da un valor alto: el modelo sabe reconocer solamente algunas palabras muy frecuentes, pero BLEU-2, BLEU-3 y BLEU-4 se derrumba abruptamente (las coincidencias de n-gramas largos son casi imposibles sin m´ as datos).

Estos resultados tambi´ en est´ an alineados con las caracter´ ısticas de los modelos basados en transformers, los mismos necesitan muchos datos para poder ser realmente eficientes. Veamos ejemplos en la evaluaci´ on (tabla 6 y tabla 7):


<!-- page 101 -->

## Ejemplos Cualitativos Greedy

Referencia: 'el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.'

Predicci´ on: 'la ley es un trabajo que se puede ser una persona sorda'

Referencia: 'gracias. gracias a vos'

Predicci´ on: 'hola , ¿ c´ omo est´ an ? ¿ c´ omo est´ an ?...'

Referencia: 'si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.'

Predicci´ on: 'la primera vez es la primera vez que se puede ser una persona sorda , que se puede. . . .'

Referencia:

's´ ı, muy interesante'

Predicci´ on: '¿ qu´

e es el agua ?'

Tabla 6: Ejemplos cualitativos de predicciones generadas con decodificaci´ on greedy .

## Ejemplos Cualitativos Beam Search (beam width = 32)

Referencia: 'el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.'

Predicci´ on: 'nos vemos el pr´ oximo domingo a las 19 : 00'

Referencia:

Predicci´ on:

'gracias. gracias a vos'

'hola , mi nombre es lautaro'

Referencia: 'si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.'

Predicci´ on: 'desde 'cn sordos' vamos a ver qu´ e es el agua para que las personas sordas

Referencia:

's´ ı, muy interesante'

Predicci´ on: 'nos vemos el pr´

oximo domingo a 'cn sordos''

Tabla 7: Ejemplos cualitativos de predicciones generadas con decodificaci´ on beam search (beam width = 32).

Esta claro que las predicciones del modelo no son buenas. Nuestro objetivo de ahora en adelante es intentar mejorar las m´ etricas BLEU-2, BLEU-3, BLEU-4 y Word Accuracy. Este objetivo podemos lograrlo mediante dos caminos:

1. Re-entrenar el modelo cambiando los hiperpar´ ametros y/o arquitectura.


<!-- page 102 -->

2. Re-evaluar el modelo cambiando las estrategias de generaci´ on, sin reentrenar.

## 6.1.3. Experimento 1: Variaci´ on de beam width sobre baseline

Utilizando el mejor modelo obtenido durante el entrenamiento realizado con la configuraci´ on inicial presentada en la secci´ on anterior (lo denominaremos como baseline), vamos a experimentar distintas formas de generar las secuencias resultado en la traducci´ on. En espec´ ıfico, jugaremos con la variaci´ on del par´ ametro beam width de Beam Search. Se presentan aqu´ ı abajo los resultados para distintos valores.

Tabla 8: Resultados obtenidos por el modelo baseline bajo diferentes configuraciones de decodificaci´ on.

| Modelo              | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|---------------------|----------|----------|----------|----------|------------|------------|
| Greedy              | 9.0%     | 3.0%     | 1.4%     | 0.8%     | 1.0%       | 0.0%       |
| Beam search (bw=32) | 6.8%     | 2.5%     | 1.2%     | 0.6%     | 0.7%       | 0.0%       |
| Beam search (bw=24) | 8.2%     | 3.1%     | 1.5%     | 0.8%     | 0.8%       | 0.0%       |
| Beam search (bw=16) | 9.5%     | 3.4%     | 1.7%     | 0.9%     | 0.9%       | 0.0%       |
| Beam search (bw=8)  | 11.1%    | 3.9%     | 1.8%     | 1.0%     | 1.2%       | 0.0%       |
| Beam search (bw=5)  | 11.4%    | 4.4%     | 2.2%     | 1.2%     | 1.3%       | 0.0%       |

Podemos observar que mientras m´ as peque˜ no el beam width, mejores resultados en nuestras m´ etricas (figura 29). Esto puede deberse a que a mayor beam width, m´ as se favorecen las oraciones con probabilidad muy alta (aquellas cortas y repetitivas, producidas por ruido en el entrenamiento). Tambi´ en podmeos notar un mejor word accuracy, llegando hasta un m´ aximo de 1.3 % (figura 30).


<!-- page 103 -->

Figura 29: Visualizaci´ on de los valores BLEU para los distintos tama˜ nos de beam width en el experimento 1. Beam width=1 equivale a greedy.

<!-- image -->

Figura 30: Visualizaci´ on de la relaci´ on entre el tama˜ no de beam width y word accuracy en el experimento 1.

<!-- image -->

Los ejemplos cualitativos a continuaci´ on son los generados por la estrate- gia de decodificaci´ on con mejores resultados. En este caso, fue beam search con beam width equivalente a 5:


<!-- page 104 -->

Tabla 9: Ejemplos cualitativos de traducciones generadas por el modelo con Beam Width = 5 en el experimento 1.

| Referencia: el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires. Predicci´ on: en 'cn sordos' es muy interesante ....         |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Referencia: gracias. gracias a vos Predicci´ on: ¡ gracias !...                                                                                                                   |
| Referencia: si no hace tope con los pies no, ya que podr´ ıa caerse y romperse. Predicci´ on: por ejemplo , en el caso de las personas sordas , en el caso de las personas sor... |
| Referencia: s´ ı, muy interesante Predicci´ on: es muy interesante                                                                                                                |

## 6.1.4. Experimento 2: 4 capas de encoders

Podr´ ıamos experimentar re-entrenar el modelo con los mismos hiperpar´ ametros pero aumentando la cantidad de capas del encoder de 2 a 4. Esto permitir´ ıa enriquecer las representaciones de los datos de entrada con el objetivo de mejorar el contexto global de una se˜ na y sus variaciones locales. Diferenciaremos a esta variaci´ on del baseline denot´ andolo como '4x6'.

El entrenamiento dur´ o aproximadamente cuatro horas y media, realizandose en 54 epochs.

Tabla 10: Resultados obtenidos por el modelo 4x6 bajo diferentes configuraciones de decodificaci´ on.

| Modelo                   | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|--------------------------|----------|----------|----------|----------|------------|------------|
| 4x6 (greedy)             | 11.1%    | 3.6%     | 1.6%     | 0.9%     | 1.0%       | 0.0%       |
| 4x6 (beam search, bw=32) | 7.2%     | 2.6%     | 1.4%     | 0.8%     | 0.7%       | 0.0%       |
| 4x6 (beam search, bw=24) | 7.9%     | 2.8%     | 1.4%     | 0.9%     | 0.7%       | 0.0%       |
| 4x6 (beam search, bw=16) | 9.0%     | 3.2%     | 1.7%     | 1.0%     | 0.8%       | 0.0%       |
| 4x6 (beam search, bw=8)  | 10.6%    | 3.6%     | 1.7%     | 0.9%     | 1.1%       | 0.0%       |
| 4x6 (beam search, bw=5)  | 11.9%    | 4.3%     | 2.2%     | 1.3%     | 1.2%       | 0.0%       |

En este experimento podemos observar que en general se obtuvieron mejores resultados que en el caso de baseline (figura 31 y 32, con excepci´ on a decodificaci´ on con beam width = 5 en el baseline, donde se obtuvo un re- sultado muy parecido a excepci´ on de BLEU-1, donde en este experimento result´ o mayor.


<!-- page 105 -->

Figura 31: Visualizaci´ on de los valores BLEU para los distintos tama˜ nos de beam width en el experimento 2. Beam width=1 equivale a greedy.

<!-- image -->

Los ejemplos cualitativos a continuaci´ on son los generados por la estrategia de decodificaci´ on con mejores resultados. En este caso, fue beam search con beam width equivalente a 5:

Referencia: 'el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.

Predicci´ on: 'en 'cn sordos' vamos a ver qu´

e es la comunidad sorda'

Referencia:

'gracias. gracias a vos'

Predicci´ on:

'chau...'

Referencia:

'si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.'

Predicci´ on: 'por ejemplo , en el caso de las personas sordas , en el caso de las personas sor...'

Referencia: 's´ ı, muy interesante'

Predicci´ on: 'en 'cn sordos' vamos a hablar de la comunidad sorda'

Tabla 11: Ejemplos cualitativos de predicciones generadas con decodificaci´ on beam search (beam width = 5) en el experimento 2.


<!-- page 106 -->

Figura 32: Visualizaci´ on de la relaci´ on entre el tama˜ no de beam width y word accuracy en el experimento 2.

<!-- image -->

## 6.1.5. Experimento 3: 6 capas de encoder

Para analizar el l´ ımite de mejora que se puede obtener modificando la cantidad de capas del encoder, detallamos aqu´ ı abajo los resultados luego de reentrenar el modelo con 6 capas de encoder. Vamos a denotarlo como '6x6'.

El entrenamient´ o dur´ o aproximadamente tres horas y media, y se complet´ o en 39 epochs.

Tabla 12: Resultados obtenidos por el modelo 6x6 bajo diferentes configuraciones de decodificaci´ on en el experimento 3.

| Modelo                   | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|--------------------------|----------|----------|----------|----------|------------|------------|
| 6x6 (greedy)             | 9.8%     | 3.1%     | 0.9%     | 0.3%     | 1.0%       | 0.0%       |
| 6x6 (beam search, bw=32) | 6.9%     | 2.4%     | 1.1%     | 0.5%     | 0.9%       | 0.0%       |
| 6x6 (beam search, bw=24) | 6.3%     | 2.4%     | 1.1%     | 0.6%     | 0.8%       | 0.0%       |
| 6x6 (beam search, bw=16) | 5.1%     | 1.8%     | 0.7%     | 0.2%     | 0.6%       | 0.0%       |
| 6x6 (beam search, bw=8)  | 9.0%     | 3.3%     | 1.4%     | 0.6%     | 1.0%       | 0.0%       |
| 6x6 (beam search, bw=5)  | 10.1%    | 3.9%     | 1.7%     | 0.8%     | 1.1%       | 0.0%       |

Notemos que con 6 capas de encoder, llegamos a un punto en donde no se ven mejoras en el rendimiento en comparaci´ on al experimento anterior (figura 33 y figura 34); los resultados obtenidos son hasta peores que los obtenidos con 4 encoders. El empeoramiento puede deberse a una desalineaci´ on encoder-decoder, ya que un encoder demasiado profundo genera representaciones excesivamente transformadas que el decoder no logra interpretar bien. Adem´ as, debido a que el modelo crece en complejidad, es necesario una cantidad de datos mayor para aprovechar el nivel de profundidad que 6 encoders aportan.


<!-- page 107 -->

Figura 33: Visualizaci´ on de los valores BLEU para los distintos tama˜ nos de beam width en el experimento 3. Beam width=1 equivale a greedy.

<!-- image -->


<!-- page 108 -->

Figura 34: Visualizaci´ on de la relaci´ on entre el tama˜ no de beam width y word accuracy en el experimento 3.

<!-- image -->

Los ejemplos cualitativos a continuaci´ on son los generados por la estrategia de decodificaci´ on con mejores resultados. En este caso, fue beam search con beam width equivalente a 5 (tabla 13).

Referencia: el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.

Predicci´ on: ¿ qu´ e es el pr´ oximo domingo ?

Referencia:

gracias. gracias a vos

Predicci´ on: hola , ¿ c´ omo est´ an ? mi nombre es lautaro

Referencia: si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.

Predicci´ on: por ejemplo , en el pa´ ıs , el mundo , en el mundo , en el agua , el mundo es el...

Referencia:

s´ ı, muy interesante

Predicci´ on: es muy importante que las personas sordas son las personas sordas

Tabla 13: Los ejemplos cualitativos a continuaci´ on son los generados por la estrategia de decodificaci´ on con mejores resultados en el experimento 3. En este caso, fue beam search con beam width = 5.


<!-- page 109 -->

## 6.1.6. Experimento 4: 4 capas de Encoders y 8 capas de Decoders

Debido a que nuestro experimento con 4 encoders mostr´ o resultados positivos en comparaci´ on con el baseline, podemos experimentar aumentar la cantidad de capas de decoders a 8. Denotaremos el modelo resultante de este experimento como '4x8'.

El entrenamiento dur´ o aproximadamente cuatro horas y cuarenta minutos, complet´ andose as´ ı en 47 epochs.

Tabla 14: Resultados obtenidos por el modelo 4x8 bajo diferentes configuraciones de decodificaci´ on.

| Modelo                   | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|--------------------------|----------|----------|----------|----------|------------|------------|
| 4x8 (greedy)             | 10.0%    | 3.4%     | 1.3%     | 0.6%     | 1.3%       | 0.0%       |
| 4x8 (beam search, bw=32) | 3.9%     | 1.5%     | 0.7%     | 0.3%     | 0.6%       | 0.0%       |
| 4x8 (beam search, bw=24) | 3.9%     | 1.5%     | 0.7%     | 0.4%     | 0.6%       | 0.0%       |
| 4x8 (beam search, bw=16) | 4.2%     | 1.6%     | 0.6%     | 0.3%     | 0.6%       | 0.0%       |
| 4x8 (beam search, bw=8)  | 10.6%    | 3.9%     | 1.6%     | 0.8%     | 1.1%       | 0.0%       |
| 4x8 (beam search, bw=5)  | 11.2%    | 4.1%     | 1.9%     | 1.0%     | 1.2%       | 0.0%       |

Notemos que tampoco vemos una mejora sustancial, es m´ as, para BLEU3 y BLEU-4 obtenemos peores resultados con beam width=5 en comparaci´ on al modelo 4x6.

Figura 35: Visualizaci´ on de los valores BLEU para los distintos tama˜ nos de beam width en el experimento 4. Beam width=1 equivale a greedy.

<!-- image -->


<!-- page 110 -->

Figura 36: Visualizaci´ on de la relaci´ on entre el tama˜ no de beam width y word accuracy en el experimento 4.

<!-- image -->

Los ejemplos cualitativos a continuaci´ on son los generados por la estrategia de decodificaci´ on con mejores resultados. En este caso, fue beam search con beam width equivalente a 5:

Referencia: el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.

Predicci´ on: por ejemplo , en el objetivo de la comunidad sorda de la comunidad sorda ....

Referencia:

gracias. gracias a vos

Predicci´ on:

hola , ¿ c´ omo est´ as ? ¿ c´ omo est´ as ?...

Referencia:

si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.

Predicci´ on: en el caso de las personas sordas , la comunidad sorda de la lengua de se˜ nas de ...

Referencia:

s´ ı, muy interesante

Predicci´ on: en 'cn sordos' es la comunidad sorda ....

Tabla 15: Ejemplos cualitativos de traducciones generadas por el modelo con beam search y beam width = 5 en el experimento 4.


<!-- page 111 -->

## 6.1.7. Experimento 5: Modelo 4x6 con kernel size=3

En los experimentos anteriores, el Pose Encoder utilizado emplea tres capas convolucionales 1D con kernel size igual a 1. Esto implica que cada frame de keypoints se procesa de manera independiente, sin capturar informaci´ on temporal entre frames adyacentes. Para explorar si una mayor capacidad de modelado local puede ayudar al modelo a capturar mejor los patrones de movimiento en las secuencias de poses, se realiz´ o un nuevo experimento aumentando el kernel size a 3 en las tres capas convolucionales.

Al incrementar el tama˜ no del kernel, cada convoluci´ on pasa a considerar no solo el frame actual, sino tambi´ en sus vecinos inmediatos (anterior y siguiente). Esto introduce una forma de contexto temporal local, permitiendo que el encoder extraiga caracter´ ısticas que representen mejor la din´ amica de las se˜ nas.

Debido a que el kernel size pas´ o de 1 a 3, fue necesario agregar padding = 1. Esto se debe a que una convoluci´ on con kernel de tama˜ no 3 y stride = 1 reduce la longitud de la secuencia en los bordes (ya que el filtro no puede aplicarse completamente en los extremos). El padding de 1 elemento a cada lado de la secuencia corrige este problema, asegurando que la salida conserve la misma longitud que la entrada (same padding), lo cual es necesario para mantener la compatibilidad con el resto de las capas del modelo.

El entrenamiento tard´ o aproximadamente tres horas y media complet´ andose as´ ı en 40 epochs.

Se detallan a continuaci´ on los resultados de este experimento:

Tabla 16: Resultados obtenidos por el modelo 4x6 con kernel=3 bajo diferentes configuraciones de decodificaci´ on.

| Modelo                              | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | Word Acc   | Sent Acc   |
|-------------------------------------|----------|----------|----------|----------|------------|------------|
| 4x6 y kernel=3 (greedy)             | 11.3%    | 3.6%     | 1.2%     | 0.5%     | 0.9%       | 0.0%       |
| 4x6 y kernel=3 (beam search, bw=32) | 7.4%     | 2.5%     | 1.2%     | 0.6%     | 0.7%       | 0.0%       |
| 4x6 y kernel=3 (beam search, bw=24) | 8.3%     | 2.8%     | 1.4%     | 0.8%     | 0.9%       | 0.0%       |
| 4x6 y kernel=3 (beam search, bw=16) | 9.7%     | 3.3%     | 1.6%     | 0.9%     | 1.1%       | 0.0%       |
| 4x6 y kernel=3 (beam search, bw=8)  | 10.5%    | 3.6%     | 1.7%     | 1.0%     | 1.0%       | 0.0%       |
| 4x6 y kernel=3 (beam search, bw=5)  | 9.4%     | 3.0%     | 1.4%     | 0.8%     | 1.1%       | 0.0%       |

En general, los resultados muestran un comportamiento similar al de los experimentos previos, a excepci´ on del Word Accuracy que tiene mejoras leves en los casos en BLEU-2 y BLEU-3.


<!-- page 112 -->

Figura 37: Visualizaci´ on de los valores BLEU para los distintos tama˜ nos de beam width en el experimento 5. Beam width=1 equivale a greedy.

<!-- image -->

Figura 38: Visualizaci´ on de la relaci´ on entre el tama˜ no de beam width y word accuracy en el experimento 5.

<!-- image -->

Referencia: el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.

Predicci´ on:

¿ qu´ e es ?

Referencia:

gracias. gracias a vos

Predicci´ on:

¡ chau...

Referencia:

si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.

Predicci´ on: es muy importante que la comunidad sorda es muy importante que la comunidad sord...

Referencia:

s´ ı, muy interesante

Predicci´ on:

hola , ¿ c´ omo est´ an ?...


<!-- page 113 -->

Tabla 17: Ejemplos cualitativos generados por el modelo con beam search y beam width = 8 en el experimento 5.

## 6.2. Adaptaci´ on de Signformer

Con el objetivo de proporcionar un nuevo baseline m´ as actual y optimizado, se propone la utilizaci´ on de Signformer (Yang, 2024), un modelo que mantiene el paradigma gloss-free pero introduce innovaciones para mejorar la eficiencia y reducir la cantidad de par´ ametros [10]. En esta secci´ on, se adapta Signformer para procesar secuencias de keypoints del conjunto de datos LSA-T, explorando su desempe˜ no como modelo de traducci´ on autom´ atica de se˜ nas a texto a partir de representaciones de pose.

## 6.2.1. ¿Qu´ e es Signformer?

Signformer es un modelo de traducci´ on de lengua de se˜ nas propuesto como una alternativa ligera, eficiente y completamente entrenada desde cero (sin modelos preentrenados). Su objetivo es resolver el problema del alto costo computacional, embeddings preentrenados y la dependencia actualmente muy popular de usar grandes modelos de lenguaje. El modelo fue dise˜ nado espec´ ıficamente para el paradigma gloss-free, es decir, traduce directamente secuencias de video a texto sin utilizar anotaciones intermedias de glosas. A pesar de su tama˜ no compacto (entre 0.57 y 3.88 millones de par´ ametros), logra resultados competitivos, alcanzando el segundo lugar en el leaderboard de 2024 para SLT sin glosas. Bas´ andose en la arquitectura en transformers presentado por Camgoz et al. (2020), Yang introduce varias innovaciones para capturar la informaci´ on visual y temporal de los videos de se˜ nas.


<!-- page 114 -->

Figura 39: Arquitectura de Signformer propuesta por Yang (2024). Imagen proveniente de [10].

<!-- image -->

## Embedding de los frames

Signformer recibe como entrada secuencias de caracter´ ısticas visuales extra´ ıdas directamente de los videos de lengua de se˜ nas. En el trabajo original, cada frame se proyecta a un vector de 1024 dimensiones mediante una red convolucional entrenada desde cero, sin preentrenamiento. A estos embeddings se les agrega una codificaci´ on posicional absoluta, siguiendo el esquema original de Attention is All You Need , para preservar la informaci´ on del orden temporal de los frames antes de ser procesados por el encoder del transformer.

## Embedding de las palabras

En el decodificador, las palabras o tokens del texto destino se representan mediante un embedding tambi´ en aprendido desde cero, sin recurrir a modelos de lenguaje preentrenados ni a vectores externos. Cada token se mapea a un vector de dimensi´ on d , que se combina nuevamente con una codificaci´ on posicional absoluta.

## Encoder

El encoder procesa la secuencia de frames a trav´ es de tres subcomponentes principales: CoPE + Gloss Attention, Conv Module y Pointwise FeedForward. El m´ odulo CoPE (Convolutional Positional Encoding) ajusta los embeddings para capturar la posici´ on y din´ amica temporal de los gestos, aprendiendo codificaciones dependientes del contexto local de los frames, mientras que la Gloss Attention [50] permite al encoder enfocarse en regiones relevantes de la secuencia para identificar glosas, en lugar de aplicar atenci´ on global. Ambos mecanismos operan dentro de un Residual Module, aplicando Add &amp; Norm (operaciones ya repasadas anteriormente) para preservar la informaci´ on de entrada. A continuaci´ on, el Conv Module aplica convoluciones punto a punto y otras transformaciones para refinar la representaci´ on de cada frame, sumando la entrada original a la salida transformada dentro de un Residual Module. Finalmente, la capa Pointwise FeedForward procesa cada frame individualmente dentro de un Residual Module, proyectando los embeddings a un espacio m´ as abstracto y agregando no linealidad para capturar relaciones complejas.


<!-- page 115 -->

## Decoder

El decoder genera la secuencia de tokens conectando la informaci´ on textual con la visual procesada por el encoder. Primero, la Multihead Attention captura dependencias internas entre los tokens generados hasta el momento. Luego, la Cross Attention conecta cada token del decoder con los embeddings del encoder, integrando la informaci´ on visual de los frames con la representaci´ on textual. El m´ odulo CoPE ajusta los embeddings de salida para capturar la posici´ on relativa de los tokens dentro de la secuencia generada, mientras que la capa Pointwise FeedForward residual refina los embeddings y los proyecta a la dimensi´ on final del espacio de vocabulario, preparando cada token para su predicci´ on. Todos los subcomponentes del encoder y decoder operan dentro de Residual Modules, asegurando estabilidad en el entrenamiento y preservaci´ on de la informaci´ on original a lo largo de la red.

## Adaptaci´ on a LSA-T

Para utilizar Signformer, se readapt´ o su arquitectura para aceptar los keypoints que forman parte de LSA-T en lugar de la informaci´ on RGB. Los cambios que se hicieron fueron:

- Se tuvo que modificar la dimensi´ on de entrada del encoder para aceptar keypoints en lugar de embeddings de CNN. Se pas´ o de una dimensi´ on de 1024 a 1086.
- Tambi´ en se aument´ o la longitud m´ axima de cada feature. Se paso de aproximadamente 200 a 1242, que es el video m´ as largo en frames.


<!-- page 116 -->

- Se implement´ o un VocabularyAdapter para generar los archivos que toma Signformer para funcionar (.dev, .train y .test).

## 6.2.2. Configuraci´ on de entrenamiento

Se utiliz´ o una configuraci´ on similar a la del modelo basado en keypoints de la secci´ on anterior, esto se debe a la naturaleza del dataset LSA-T. Se emplearon los mismos splits de train, dev y test que fueron generados en el preprocesamiento del dataset. Algunos de los hiperpar´ ametros utilizados fueron:

- Epochs: 100, donde un epoch corresponde a una pasada completa sobre el conjunto de entrenamiento.
- Batch size: 2, reducido debido a la longitud de las secuencias.
- Optimizador: AdamW, con par´ ametros β = (0 , 9 , 0 , 998).
- Learning rate: 3e-5.
- Weight decay: 0.01, para mejorar la generalizaci´ on del modelo.
- Label smoothing: 0.1, para suavizar etiquetas y mejorar generalizaci´ on.
- Embeddings: dimensi´ on de 256.
- Feedforward: dimensi´ on de 1024.
- CoPE desactivado: debido a problemas de memoria, no se pudo utilizar el modelo con el componente CoPE, por lo que se dej´ o desactivado aprovechando los dem´ as componentes de Signformer.

Por otro lado, se utilizaron 2 capas de encoder, 6 capas de decoder e inicializaci´ on Xavier. Los dem´ as hiperpar´ ametros se dejaron tal como se encuentran en el archivo de configuraci´ on por defecto de Signformer.

El tiempo de entrenamiento fue de aproximadamente 24 horas, complet´ andose as´ ı en 49 epochs.

## 6.2.3. Configuraci´ on de evaluaci´ on

## M´ etricas de evaluaci´ on

Adem´ as de las m´ etricas BLEU-1, BLEU-2, BLEU-3 y BLEU-4, Signformer implementa la m´ etrica ROUGE [51]. En espec´ ıfico, implementa la variaci´ on ROUGE-L que compara el texto generado por el modelo con un texto de referencia buscando la subsecuencia m´ as larga (LCS) de palabras que aparece en ambos y en el mismo orden. A diferencia de otras m´ etricas que solo comparan grupos de palabras contiguas, ROUGE-L permite que las palabras coincidan aunque no est´ en una al lado de la otra, siempre que mantengan el orden relativo. Ejemplos en la tabla 18.


<!-- page 117 -->

Tabla 18: Ejemplos de subsecuencia m´ as larga (LCS) usados en ROUGE-L

| Referencia                                 | Hip´ otesis                              | (LCS)                         |
|--------------------------------------------|------------------------------------------|-------------------------------|
| El gato negro duerme en la silla           | El gato duerme en la silla               | El gato duerme en la silla    |
| Hoy hace mucho calor en la ciudad          | Hace calor en la ciudad hoy              | hace calor en la ciudad       |
| La traducci´ on autom´ atica es complicada | La traducci´ on es complicada y r´ apida | La traducci´ on es complicada |

Se deja el c´ odigo de las adaptaci´ on, implementaci´ on de ROUGE y dem´ as detalles en el link del repositorio de Github 10 .

## Resultados obtenidos

A continuaci´ on se detallan los resultados obtenidos mediante Signformer, adaptando el mismo al dataset LSA-T.

Tabla 19: Resultados obtenidos por el modelo Signformer adaptado a LSA-T (keypoints)

| Modelo                      | BLEU-1   | BLEU-2   | BLEU-3   | BLEU-4   | ROUGE   |
|-----------------------------|----------|----------|----------|----------|---------|
| Signformer LSA-T (sin CoPE) | 15.00%   | 4.95%    | 2.08%    | 1.17%    | 10.68%  |

Notemos que los resultados obtenidos son los mejores en comparaci´ on a todos los experimentos que hemos realizado hasta ahora. En el caso de los resultados obtenidos sin CoPE la cantidad de epochs necesarios para converger fue de 49 y el beam width ´ optimo fue de tama˜ no 3 (calculado autom´ aticamente por Signformer).

Si bien las m´ etricas BLEU fueron mejores, veamos ejemplos cualitativos usando el modelo entrenado (tabla 20)

10 https://github.com/juanbratti/SignformerAdaptation-LSA


<!-- page 118 -->

Tabla 20: Ejemplos cualitativos de predicciones generadas con decodificaci´ on beam search con bw=3 en Signformer aplicado a LSA-T.

| Ejemplos Cualitativos Signformer en LSA-T                                                                                                                                                               |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Referencia: 'el regreso a la escuela comenzar´ a el pr´ oximo mi´ ercoles 17 de febrero en la ciudad de buenos aires.' Predicci´ on: 'el gobierno nacional de la provincia de buenos aires y el mundo.' |
| Referencia: 'gracias. gracias a vos' Predicci´ on: 'en relaci´ on a lo que es muy importante.'                                                                                                          |
| Referencia: 'si no hace tope con los pies no, ya que podr´ ıa caerse y romperse.' Predicci´ on: 'en 'cn sordos' vamos a hablar de la comunidad sorda.'                                                  |
| Referencia: 's´ ı, muy interesante' Predicci´ on: 'en el pr´ oximo domingo a las 19:00 de la ley.'                                                                                                      |


<!-- page 119 -->

## 7. An´ alisis de Resultados

En el modelo baseline, se pudo ver que con 2 encoders y 6 decoders se alcanz´ o un BLEU-1 de 9.0 % y un BLEU-4 de 0.8 % usando greedy decoding. Aunque los valores son bajos, era algo esperable considerando la dificultad del dataset LSA-T. Este corpus tiene un vocabulario enorme y la mayor´ ıa de las frases aparecen una sola vez, por lo que el modelo termina reconociendo solo palabras muy frecuentes. Eso explica por qu´ e el BLEU-1 se mantiene relativamente alto, pero los BLEU de orden superior (2, 3 y 4) caen r´ apidamente: al modelo le cuesta mantener el orden y la coherencia de las oraciones completas.

Luego, probando distintas configuraciones de beam search, notamos algo interesante: los beam widths m´ as chicos (entre 5 y 8) dieron mejores resultados que los m´ as grandes. Con beam widths grandes (por ejemplo 32), el modelo tiende a generar frases muy cortas o repetitivas, priorizando opciones con alta probabilidad pero poco contenido. En cambio, con beam widths reducidos la generaci´ on es m´ as variada y las m´ etricas mejoran, especialmente en los n-gramas m´ as largos.

Despu´ es de eso, se decidi´ o experimentar con la cantidad de capas del encoder. Aumentando la cantidad de capas de 2 a 4, las m´ etricas subieron: el modelo alcanz´ o un BLEU-1 de 11.1 % y un BLEU-4 de 1.3 %, lo que muestra que un encoder un poco m´ as profundo logra representaciones m´ as ricas y mejora el contexto global de cada se˜ na. Sin embargo, al usar 6 capas, el rendimiento baj´ o levemente. Esto puede deberse a que el modelo se vuelve demasiado complejo para la cantidad de datos que tiene, o a que el decoder no logra interpretar bien las representaciones tan transformadas que genera un encoder profundo.

Siguiendo esa l´ ınea, se prob´ o una modificaci´ on en la arquitectura del Pose Encoder. Lo que se hizo fue pasar de usar tres capas convolucionales 1D con kernel size = 1 a kernel size = 3, permitiendo aprovechar la informaci´ on temporal entre frames consecutivos. Si bien este experimento mostr´ o algunas mejoras en las m´ etricas BLEU-2 y BLEU-3 en comparaci´ on a los dem´ as, el impacto general fue moderado, lo que indica que este tipo de ajuste por s´ ı solo tampoco alcanza para resolver las limitaciones de los datos de entrada.

Luego, siguiendo el resultado positivo de 4 encoders, se aumentaron las capas del decoder a 8, pero no hubo mejoras. De hecho, algunas m´ etricas bajaron, lo cual refuerza la idea de que el cuello de botella no est´ a en el decoder, sino en la representaci´ on visual de entrada. Los keypoints, por s´ ı solos, no parecen suficientes para capturar toda la informaci´ on sem´ antica del video.

Por otro lado, los resultados obtenidos con Signformer representan un avance significativo respecto al modelo baseline. Mientras que el baseline alcanzaba un BLEU-1 de 9.0 % y un BLEU-4 de 0.8 %, la adaptaci´ on de Signformer a los keypoints de LSA-T elev´ o estas m´ etricas a 15.0 % y 1.17 %, respectivamente. Esta mejora evidencia que el modelo puede capturar mejor la informaci´ on temporal y sem´ antica de los videos gracias a la Gloss Attention [50] y el m´ odulo convolucional, superando las limitaciones que presentaban los encoders m´ as profundos, los kernels m´ as grandes o el aumento de capas en el decoder del baseline. Los resultados muestran que el modelo logra reconocer parte del vocabulario de las oraciones de referencia, pero, al igual que el modelo anterior, todav´ ıa tiene problemas para mantener una estructura coherente tanto a nivel sint´ actico como sem´ antico. Esto se nota claramente en los ejemplos cualitativos: las frases generadas tienen una gram´ atica correcta, pero su significado suele diferir bastante del de la referencia original. Una de las principales razones de este comportamiento es la desactivaci´ on del m´ odulo CoPE, que es el encargado de capturar la din´ amica temporal de los gestos. Al no usarlo, el modelo pierde informaci´ on clave sobre el orden y la progresi´ on de los movimientos, lo que afecta su capacidad de interpretar correctamente las se˜ nas. Aun as´ ı, las m´ etricas BLEU muestran una mejora considerable frente al modelo anterior. Por eso, esta adaptaci´ on puede considerarse un nuevo baseline sobre el cual continuar haciendo pruebas y ajustes en el futuro.


<!-- page 120 -->

En conclusi´ on, el modelo baseline logra reconocer algunas palabras frecuentes, pero todav´ ıa tiene dificultades para generar oraciones completas y coherentes debido a la alta variabilidad y escasa repetici´ on de ejemplos en el dataset LSA-T. Aun as´ ı, los experimentos permitieron identificar configuraciones m´ as efectivas (por ejemplo, usar 4 encoders) y comprender mejor las limitaciones del sistema. La adaptaci´ on de Signformer, al procesar de manera m´ as eficiente las secuencias de keypoints y preservar el contexto temporal, establece un nuevo baseline s´ olido, superando las m´ etricas del modelo previo y ofreciendo una base m´ as robusta para futuros experimentos y mejoras.


<!-- page 121 -->

## 8. Conclusiones

El objetivo principal de este trabajo fue explorar la traducci´ on autom´ atica de la Lengua de Se˜ nas Argentina utilizando representaciones de pose basadas en keypoints, extra´ ıdas del conjunto de datos LSA-T. La idea fue adaptar y evaluar arquitecturas del tipo Transformer bajo el enfoque gloss-free, con el fin de generar texto directamente a partir de secuencias visuales, sin depender de una etapa intermedia de glosas. Para esto, se comenz´ o reproduciendo un modelo baseline inspirado en el trabajo de Dal Bianco et al. (2024), probando diferentes configuraciones arquitect´ onicas y estrategias de decodificaci´ on, y luego se desarroll´ o una versi´ on adaptada del modelo Signformer ajustada al formato de keypoints de LSA-T.

Los resultados mostraron que el modelo baseline fue capaz de reconocer palabras frecuentes, pero tuvo dificultades para mantener coherencia sint´ actica y sem´ antica en oraciones completas. Este comportamiento era esperable, considerando la alta variabilidad de LSA-T y la limitada cantidad de ejemplos disponibles por clase. Sin embargo, algunos ajustes como el uso de cuatro capas de encoder y valores de beam width reducidos, demostraron un impacto positivo en las m´ etricas BLEU, logrando una mejora relativa en la calidad de las traducciones generadas. En comparaci´ on, la adaptaci´ on de Signformer logr´ o un avance m´ as notorio: las m´ etricas BLEU-1 y BLEU-4 aumentaron de 9.0 % y 0.8 % en el baseline a 15.0 % y 1.17 %, respectivamente, lo que evidencia una mejor capacidad para capturar las relaciones temporales y sem´ anticas entre los gestos.

Aun con estas mejoras, persisten limitaciones importantes. El modelo depende exclusivamente de informaci´ on de pose, lo que restringe la riqueza sem´ antica que puede aprovecharse durante la traducci´ on. Adem´ as, el tama˜ no y la diversidad del dataset LSA-T no alcanzan para explotar completamente el potencial de las arquitecturas Transformer. Tambi´ en fue necesario descartar la incorporaci´ on del m´ odulo CoPE de Signformer por limitaciones de memoria, por lo que no se pudo evaluar su aporte real al desempe˜ no del modelo. En conjunto, estas limitaciones marcan un punto de partida para futuras mejoras.

En s´ ıntesis, este trabajo representa un avance concreto dentro del campo de la traducci´ on autom´ atica de la Lengua de Se˜ nas Argentina. La adaptaci´ on de Signformer presentada aqu´ ı constituye la primera aplicaci´ on de este modelo al dominio de la LSA utilizando ´ unicamente representaciones de pose, y los resultados obtenidos demuestran que los enfoques gloss-free pueden ser una alternativa viable para lenguas con pocos recursos anotados. Adem´ as, se incluy´ o un repaso te´ orico detallado sobre los modelos m´ as relevantes utilizados hist´ oricamente para esta tarea, con el prop´ osito de contextualizar los avances recientes y dejar documentadas las bases conceptuales que guiaron la implementaci´ on. Finalmente, se deja disponible y documentado el c´ odigo desarrollado, junto con la descripci´ on del proceso experimental, de modo que este trabajo pueda servir como punto de partida para futuras continuaciones.


<!-- page 122 -->

## 8.1. Trabajo a Futuro

A partir de lo observado, hay varias formas de seguir mejorando este trabajo:

1. Probar con distintas formas de preprocesar los keypoints: en este trabajo se lleva a cabo solamente una t´ ecnica de preprocesamiento, en donde las normalizaciones no tienen en cuenta la coordenada z de los keypoints. Un enfoque interesante podr´ ıa ser replantear esta etapa y aplicar normalizaciones m´ as espec´ ıficas, que utilicen el centrado del cuerpo o profundidad del signante.
2. Incluir un encoder pre-entrenado: as´ ı como Camgoz et al. utilizaron un encoder pre-entrenado para obtener los embeddings de los frames, se podr´ ıa pre-entrenar al encoder con datasets grandes de poses humanas antes de pasarle los keypoints de LSA-T. Esto podr´ ıa ayudar al modelo a entender mejor los movimientos y generalizar m´ as r´ apido.
3. Incluir informaci´ on RGB: Si bien la informaci´ on RGB puede introducir ruido debido a los colores y al fondo de los signantes, ser´ ıa interesante experimentar con el modelo Signformer utilizando los frames en formato RGB, o un h´ ıbidro entre RGB y keypoints.
4. Experimentar Signformer con CoPE para ver la mejora real de de la codificaci´ on posicional implementada por el modelo.


<!-- page 123 -->

## Referencias

- [1] Franco Ronchetti et al. 'Handshape recognition for Argentinian Sign Language using ProbSom'. En: CoRR abs/2310.17427 (2023). doi : 10.48550/ARXIV.2310.17427 . arXiv: 2310.17427 . url : https: //doi.org/10.48550/arXiv.2310.17427 .
- [2] Dongxu Li et al. 'Word-level Deep Sign Language Recognition from Video: A New Large-scale Dataset and Methods Comparison'. En: IEEE Winter Conference on Applications of Computer Vision, WACV 2020, Snowmass Village, CO, USA, March 1-5, 2020 . IEEE, 2020, p´ ags. 1448-1458. doi : 10 . 1109 / WACV45572 . 2020 . 9093512 . url : https://doi.org/10.1109/WACV45572.2020.9093512 .
- [3] Shankara Narayanan V, Sneha Varsha M y Padmavathi S. 'Continuous Sign Language Recognition using Convolutional Neural Network'. En: 2024 Second International Conference on Emerging Trends in Information Technology and Engineering (ICETITE) . 2024, p´ ags. 1-6. doi : 10.1109/ic-ETITE58242.2024.10493715 .
- [4] Pedro Dal Bianco et al. 'LSA-T: The First Continuous Argentinian Sign Language Dataset for Sign Language Translation'. En: Advances in Artificial Intelligence - IBERAMIA 2022 - 17th Ibero-American Conference on AI, Cartagena de Indias, Colombia, November 23-25, 2022, Proceedings . Ed. por Ana Cristina Bicharra Garcia, Mariza Ferro y Julio C´ esar Rodr´ ıguez Rib´ on. Vol. 13788. Lecture Notes in Computer Science. Springer, 2022, p´ ags. 293-304. doi : 10.1007/978-3-03122419-5\_25 . url : https://doi.org/10.1007/978-3-031-22419-5\_25 .
- [5] Danielle Bragg et al. 'Sign Language Recognition, Generation, and Translation: An Interdisciplinary Perspective'. En: The 21st International ACM SIGACCESS Conference on Computers and Accessibility, ASSETS 2019, Pittsburgh, PA, USA, October 28-30, 2019 . Ed. por Jeffrey P. Bigham, Shiri Azenkot y Shaun K. Kane. ACM, 2019, p´ ags. 16-31. doi : 10.1145/3308561.3353774 . url : https://doi. org/10.1145/3308561.3353774 .
- [6] Jr. Stokoe William C. 'Sign Language Structure: An Outline of the Visual Communication Systems of the American Deaf'. En: The Journal of Deaf Studies and Deaf Education 10.1 (ene. de 2005), p´ ags. 3-37. issn : 1081-4159. doi : 10.1093/deafed/eni001 . eprint: https:// academic.oup.com/jdsde/article-pdf/10/1/3/1034248/eni001. pdf . url : https://doi.org/10.1093/deafed/eni001 .


<!-- page 124 -->

- [7] Necati Cihan Camg¨ oz et al. 'Neural Sign Language Translation'. En: 2018 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, USA, June 18-22, 2018 . Computer Vision Foundation / IEEE Computer Society, 2018, p´ ags. 7784-7793. doi : 10.1109/CVPR.2018.00812 . url : http://openaccess.thecvf. com/content%5C\_cvpr%5C\_2018/html/Camgoz%5C\_Neural%5C\_Sign% 5C\_Language%5C\_CVPR%5C\_2018%5C\_paper.html .
- [8] Zeyu Liang, Huailing Li y Jianping Chai. 'Sign Language Translation: ASurvey of Approaches and Techniques'. En: Electronics 12.12 (2023). issn : 2079-9292. doi : 10.3390/electronics12122678 . url : https: //www.mdpi.com/2079-9292/12/12/2678 .
- [9] M. Madhiarasan y Partha Pratim Roy. 'A Comprehensive Review of Sign Language Recognition: Different Types, Modalities, and Datasets'. En: CoRR abs/2204.03328 (2022). doi : 10.48550/ARXIV.2204. 03328 . arXiv: 2204.03328 . url : https://doi.org/10.48550/arXiv. 2204.03328 .
- [10] Eta Yang. Signformer is all you need: Towards Edge AI for Sign Language . 2024. arXiv: 2411.12901 [cs.CL] . url : https://arxiv.org/ abs/2411.12901 .
- [11] Franco Ronchetti et al. 'LSA64: An Argentinian Sign Language Dataset'. En: CoRR abs/2310.17429 (2023). doi : 10.48550/ARXIV.2310. 17429 . arXiv: 2310.17429 . url : https://doi.org/10.48550/arXiv. 2310.17429 .
- [12] Pedro Dal Bianco et al. 'Study on pose-based deep learning models for gloss-free Sign Language Translation'. En: J. Comput. Sci. Technol. 24.2 (2024), p´ ag. 09. doi : 10.24215/16666038.24.E09 . url : https: //doi.org/10.24215/16666038.24.e09 .
- [13] Richard Szeliski. Computer Vision: Algorithms and Applications . 2nd. New York, NY: Springer, 2022. url : https://szeliski.org/Book/ .
- [14] Esma Dilek y Murat Dener. 'Computer Vision Applications in Intelligent Transportation Systems: A Survey'. En: Sensors 23.6 (2023). issn : 1424-8220. doi : 10.3390/s23062938 . url : https://www.mdpi. com/1424-8220/23/6/2938 .
- [15] Ansam A. Abdulhussein, Hasanien Kariem Kuba y Alaa Neamah Azeez Alanssari. 'Computer Vision to Improve Security Surveillance through the Identification of Digital Patterns'. En: 2020 International Conference on Industrial Engineering, Applications and Manufacturing (ICIEAM) . 2020, p´ ags. 1-5. doi : 10.1109/ICIEAM48468.2020.9112022 .


<!-- page 125 -->

- [16] Md Mohsin Kabir et al. 'Computer vision algorithms in healthcare: Recent advancements and future challenges'. En: Computers in Biology and Medicine 185 (2025), p´ ag. 109531. issn : 0010-4825. doi : https:// doi.org/10.1016/j.compbiomed.2024.109531 . url : https://www. sciencedirect.com/science/article/pii/S0010482524016160 .
- [17] Longfei Zhou, Lin Zhang y Nicholas Konz. 'Computer Vision Techniques in Manufacturing'. En: IEEE Trans. Syst. Man Cybern. Syst. 53.1 (2023), p´ ags. 105-117. doi : 10.1109/TSMC.2022.3166397 . url : https://doi.org/10.1109/TSMC.2022.3166397 .
- [18] J´ ulio Castro Lopes y Rui Pedro Lopes. 'Computer Vision in Augmented, Virtual, Mixed and Extended Reality environments-A bibliometric review'. En: Visual Informatics 8.4 (2024), p´ ags. 13-22. issn : 2468502X. doi : https://doi.org/10.1016/j.visinf.2024.11.002 . url : https://www.sciencedirect.com/science/article/pii/ S2468502X24000676 .
- [19] Hugging Face. Pre-processing for Computer Vision Tasks . Accessed: 2025-10-04. 2025. url : https://huggingface.co/learn/computervision-course/unit1/image\_and\_imaging/examples-preprocess .
- [20] Mohammed Hasan. Lecture Notes . Al-Mustaqbal University. 2024. url : https://www.uomus.edu.iq/img/lectures21/MUCLecture\_2022\_ 8185959.pdf (visitado 04-10-2025).
- [21] David G. Lowe. 'Distinctive Image Features from Scale-Invariant Keypoints'. En: Int. J. Comput. Vis. 60.2 (2004), p´ ags. 91-110. doi : 10. 1023/B:VISI.0000029664.99615.94 . url : https://doi.org/10. 1023/B:VISI.0000029664.99615.94 .
- [22] N. Dalal y B. Triggs. 'Histograms of oriented gradients for human detection'. En: 2005 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'05) . Vol. 1. 2005, 886-893 vol. 1. doi : 10.1109/CVPR.2005.177 .
- [23] Herbert Bay, Tinne Tuytelaars y Luc Van Gool. 'SURF: Speeded Up Robust Features'. En: Computer Vision - ECCV 2006, 9th European Conference on Computer Vision, Graz, Austria, May 7-13, 2006, Proceedings, Part I . Ed. por Ales Leonardis, Horst Bischof y Axel Pinz. Vol. 3951. Lecture Notes in Computer Science. Springer, 2006, p´ ags. 404-417. doi : 10.1007/11744023\_32 . url : https://doi.org/ 10.1007/11744023%5C\_32 .


<!-- page 126 -->

- [24] Hugging Face. Feature Description . Accessed: 2025-10-04. 2025. url : https://huggingface.co/learn/computer-vision-course/unit1/ feature-extraction/feature\_description .
- [25] Logistic Regression . Wikipedia, Accessed: 2025-10-04. 2025. url : https: //en.wikipedia.org/wiki/Logistic\_regression .
- [26] Support vector machine . Wikipedia, The Free Encyclopedia. Accessed: 2025-10-04. 2025. url : https://en.wikipedia.org/wiki/Support\_ vector\_machine .
- [27] Jamie Shotton et al. 'Real-Time Human Pose Recognition in Parts from Single Depth Images'. En: Machine Learning for Computer Vision . Ed. por Roberto Cipolla, Sebastiano Battiato y Giovanni Maria Farinella. Vol. 411. Studies in Computational Intelligence. Springer, 2013, p´ ags. 119-135. doi : 10.1007/978-3-642-28661-2\_5 . url : https://doi.org/10.1007/978-3-642-28661-2%5C\_5 .
- [28] Sivic y Zisserman. 'Video Google: a text retrieval approach to object matching in videos'. En: Proceedings Ninth IEEE International Conference on Computer Vision . 2003, 1470-1477 vol.2. doi : 10.1109/ICCV. 2003.1238663 .
- [29] David E Rumelhart, Geoffrey E Hinton y Ronald J Williams. 'Learning representations by back-propagating errors'. en. En: Nature 323.6088 (oct. de 1986), p´ ags. 533-536.
- [30] Moez Krichen. 'Convolutional Neural Networks: A Survey'. En: Computers 12.8 (2023). issn : 2073-431X. doi : 10.3390/computers12080151 . url : https://www.mdpi.com/2073-431X/12/8/151 .
- [31] IBM. ¿Qu´ e son las redes neuronales convolucionales? Recuperado de IBM Think. n.d. url : https://www.ibm.com/es-es/think/topics/ convolutional-neural-networks (visitado 05-10-2025).
- [32] Clinton J. Wang et al. 'Deep learning for liver tumor diagnosis part II: convolutional neural network interpretation using radiologic imaging features'. en. En: European Radiology 29.7 (mayo de 2019 0 5), p´ ags. 3348-3357. doi : 10.1007/s00330-019-06214-8 . url : http: //dx.doi.org/10.1007/s00330-019-06214-8 .
- [33] Robin M. Schmidt. Recurrent Neural Networks (RNNs): A gentle Introduction and Overview . 2019. arXiv: 1912.05911 [cs.LG] . url : https: //arxiv.org/abs/1912.05911 .
- [34] Ilya Sutskever, Oriol Vinyals y Quoc V. Le. Sequence to Sequence Learning with Neural Networks . 2014. arXiv: 1409.3215 [cs.CL] . url : https://arxiv.org/abs/1409.3215 .


<!-- page 127 -->

- [35] Dzmitry Bahdanau, Kyunghyun Cho y Yoshua Bengio. Neural Machine Translation by Jointly Learning to Align and Translate . 2016. arXiv: 1409.0473 [cs.CL] . url : https://arxiv.org/abs/1409.0473 .
- [36] Minh-Thang Luong, Hieu Pham y Christopher D. Manning. Effective Approaches to Attention-based Neural Machine Translation . 2015. arXiv: 1508.04025 [cs.CL] . url : https://arxiv.org/abs/1508. 04025 .
- [37] Ashish Vaswani et al. Attention Is All You Need . 2023. arXiv: 1706. 03762 [cs.CL] . url : https://arxiv.org/abs/1706.03762 .
- [38] Huiyan Han et al. A human activity recognition method based on Vision Transformer - Scientific Figure . https://www.researchgate. net/figure/Visualization-thermal-map-of-position-encoder\_ fig5\_381960929 . Accessed: 21 Oct 2025. 2024.
- [39] Kishore Papineni et al. 'Bleu: a Method for Automatic Evaluation of Machine Translation'. En: Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics, July 6-12, 2002, Philadelphia, PA, USA . ACL, 2002, p´ ags. 311-318. doi : 10.3115/1073083. 1073135 . url : https://aclanthology.org/P02-1040/ .
- [40] Necati Cihan Camg¨ oz et al. 'Sign Language Transformers: Joint Endto-End Sign Language Recognition and Translation'. En: 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2020, Seattle, WA, USA, June 13-19, 2020 . Computer Vision Foundation / IEEE, 2020, p´ ags. 10020-10030. doi : 10.1109/CVPR42600.2020. 01004 . url : https://openaccess.thecvf.com/content%5C\_CVPR% 5C\_2020/html/Camgoz%5C\_Sign%5C\_Language%5C\_Transformers% 5C\_Joint%5C\_End-to-End%5C\_Sign%5C\_Language%5C\_Recognition% 5C\_and%5C\_Translation%5C\_CVPR%5C\_2020%5C\_paper.html .
- [41] Alex Graves et al. 'Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks'. En: Machine Learning, Proceedings of the Twenty-Third International Conference (ICML 2006), Pittsburgh, Pennsylvania, USA, June 25-29, 2006 . Ed. por William W. Cohen y Andrew W. Moore. Vol. 148. ACM International Conference Proceeding Series. ACM, 2006, p´ ags. 369-376. doi : 10.1145/1143844.1143891 . url : https://doi.org/10.1145/ 1143844.1143891 .
- [42] Youngmin Kim et al. 'Keypoint based Sign Language Translation without Glosses'. En: CoRR abs/2204.10511 (2022). doi : 10.48550/ARXIV. 2204.10511 . arXiv: 2204.10511 . url : https://doi.org/10.48550/ arXiv.2204.10511 .


<!-- page 128 -->

- [43] Mo Guan et al. 'Multi-Stream Keypoint Attention Network for Sign Language Recognition and Translation'. En: CoRR abs/2405.05672 (2024). doi : 10.48550/ARXIV.2405.05672 . arXiv: 2405.05672 . url : https://doi.org/10.48550/arXiv.2405.05672 .
- [44] HossamEldin Mahmoud, Mustafa A. Elattar y M. Saeed Darweesh. 'Joint Sign Language Recognition and Translation Using Keypoint Estimation'. En: 2023 11th International Japan-Africa Conference on Electronics, Communications, and Computations (JAC-ECC) . 2023, p´ ags. 184-189. doi : 10.1109/JAC-ECC61002.2023.10479621 .
- [45] Mathieu De Coster et al. 'Towards the extraction of robust sign embeddings for low resource sign language recognition'. En: CoRR abs/2306.17558 (2023). doi : 10.48550/ARXIV.2306.17558 . arXiv: 2306.17558 . url : https://doi.org/10.48550/arXiv.2306.17558 .
- [46] Sang-Ki Ko et al. 'Neural Sign Language Translation based on Human Keypoint Estimation'. En: CoRR abs/1811.11436 (2018). arXiv: 1811. 11436 . url : http://arxiv.org/abs/1811.11436 .
- [47] Xavier Glorot y Yoshua Bengio. 'Understanding the difficulty of training deep feedforward neural networks'. En: Proceedings of the Thirteenth International Conference on Artificial Intelligence and Statistics, AISTATS 2010, Chia Laguna Resort, Sardinia, Italy, May 13-15, 2010 . Ed. por Yee Whye Teh y D. Mike Titterington. Vol. 9. JMLR Proceedings. JMLR.org, 2010, p´ ags. 249-256. url : http://proceedings. mlr.press/v9/glorot10a.html .
- [48] Ilya Loshchilov y Frank Hutter. 'Fixing Weight Decay Regularization in Adam'. En: CoRR abs/1711.05101 (2017). arXiv: 1711.05101 . url : http://arxiv.org/abs/1711.05101 .
- [49] Ronald J. Williams y David Zipser. 'A Learning Algorithm for Continually Running Fully Recurrent Neural Networks'. En: Neural Comput. 1.2 (1989), p´ ags. 270-280. doi : 10.1162/NECO.1989.1.2.270 . url : https://doi.org/10.1162/neco.1989.1.2.270 .
- [50] Aoxiong Yin et al. 'Gloss Attention for Gloss-free Sign Language Translation'. En: IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2023, Vancouver, BC, Canada, June 17-24, 2023 . IEEE, 2023, p´ ags. 2551-2562. doi : 10.1109/CVPR52729.2023.00251 . url : https://doi.org/10.1109/CVPR52729.2023.00251 .


<!-- page 129 -->

- [51] Chin-Yew Lin. 'ROUGE: A Package for Automatic Evaluation of Summaries'. En: Text Summarization Branches Out . Barcelona, Spain: Association for Computational Linguistics, jul. de 2004, p´ ags. 74-81. url : https://aclanthology.org/W04-1013/ .