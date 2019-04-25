import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plotter

# Obtengo toda la data
laps = pd.read_csv('../data/formula-1-race-data-19502017/lapTimes.csv').copy()
races = pd.read_csv('../data/formula-1-race-data-19502017/races.csv').copy()
qualifying = pd.read_csv('../data/formula-1-race-data-19502017/qualifying.csv').copy()
pits = pd.read_csv('../data/formula-1-race-data-19502017/pitStops.csv').copy()

# Limpio los datos que no necesito
laps = laps.rename(columns={'time':'lapTime'})
races = races.drop(columns='url')
qualifying = qualifying.drop(columns=['qualifyId', 'position', 'q1', 'q2', 'q3'])
pits = pits.drop(columns=['time', 'duration', 'milliseconds'])


# Mergeo tablas
data = pd.merge(laps, races, on='raceId')
data = pd.merge(data, qualifying, on=['raceId', 'driverId'])

# Saco las vueltas en las que hubo pit stop
data = pd.merge(data, pits, on=['raceId', 'driverId', 'lap'], how='outer')
indexNames = data[ data['stop'] > 0].index
data.drop(indexNames, inplace=True)
data = data.drop(columns=['stop'])

# Le agrego los promedios y el driverTime que es el porcentaje para arriba o para abajo de las vueltas
meanByRace = data.groupby(['raceId']).mean().rename(columns={'milliseconds':'mean'})['mean']
data = pd.merge(data, meanByRace, on=['raceId'])
meanByRaceAndDriver = data.groupby(['raceId', 'driverId']).mean().rename(columns={'milliseconds':'driverMean'})['driverMean']
meanByRaceAndConstructor = data.groupby(['raceId', 'constructorId']).mean().rename(columns={'milliseconds':'constructorMean'})['constructorMean']
data = pd.merge(data, meanByRaceAndDriver, on=['raceId', 'driverId'])
data = pd.merge(data, meanByRaceAndConstructor, on=['raceId', 'constructorId'])
data['driverTime'] = (data['driverMean'] - data['mean'])/data['mean']
data['constructorTime'] = (data['constructorMean'] - data['mean'])/data['mean']

# Obtengo la info en pantalla
print(data['driverTime'].describe([.05, .1, .25, .5, .75, .9, .95]))
print(data['constructorTime'].describe([.05, .1, .25, .5, .75, .9, .95]))
#plotter.scatter(x=data['driverTime'], y=data['driverId'])

#data = data[((data['raceId'] >= 985) & (data['raceId'] <= 986))]








