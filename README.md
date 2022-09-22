# Propuesta de liga de futbolín

Ya que es probable que no podamos jugar todos los posibles partidos por cantidad, aquí propongo un sistema para poder generar iterativamente partidos teniendo en cuenta los partidos previos.

La idea es tener en una matriz ciertos pesos para la elección aleatoria de compañeros, y una análoga para rivales.

Después del sorteo de cada partido, las probabilidades de ser compañeros y rivales de los elegidos decrecerán para poder balancear estas elecciones y no repetir rivilades ni equipos de forma muy seguida.

Pasos para el sorteo:

1. Se rellenan el número de jugadores hasta tener un múltiplo de 4. Los jugadores extra se considerarán jornadas de descanso para sus rivales.

2. Se establece un número de jornadas a jugar. Los jugadores jugarán tantos partidos como jornadas (quedaría por determinar qué hacer con las jornadas de descanso)

3. Se sortea cada jornada eligiendo tantos jugadores como partidos. Para cada jugador:

   1. Se elige a su compañero de acuerdo a las probabilidades del resto de jugadores de ser su compañero.
   2. Se elige al primer rival con la intersección de probabilidades de posibles rivales del jugador y su compañero.
   3. Se elige al segundo rival con la intersección de probabilidades de posibles rivales de jugador y compañero y de posibles compañeros del primer rival.
   4. Se actualizan las relaciones de compañerismo y rivalidad entre los elegidos para la siguiente jornada.