#encoding=utf-8

import sys
import json

def main(argv):

	rtttl = argv[1]

	tone = {'a': 0, "a#": 1, 'b': 2, 'c':-9, 'c#': -8, 'd': -7, 'd#': -6, 'e': -5, 'f': -4, 'f#': -3, 'g': -2, 'g#': -1, 'h': 2}

	freqs = {-57: 16.35, -56: 17.32, -55: 18.35, -54: 19.45, -53: 20.60, -52: 21.83, -51: 23.12, -50: 24.50, -49: 25.96, -48: 27.50, -47: 29.14, -46: 30.87,
			 -45: 32.70, -44: 34.65, -43: 36.71, -42: 38.89, -41: 41.20, -40: 43.65, -39: 46.25, -38: 49.00, -37: 51.91, -36: 55.00, -35: 58.27, -34: 61.74,
			 -33: 65.41, -32: 69.30, -31: 73.42, -30: 77.78, -29: 82.41, -28: 87.31, -27: 92.50, -26: 98.00, -25: 103.83, -24: 110.00, -23: 116.54, -22: 123.47,
			 -21: 130.81, -20: 138.59, -19: 146.83, -18: 155.56, -17: 164.81, -16: 174.61, -15: 185.00, -14: 196.00, -13: 207.65, -12: 220.00, -11: 233.08, -10: 246.94,
			 -9: 261.63, -8: 277.18, -7: 293.66, -6: 311.13, -5: 329.63, -4: 349.23, -3: 369.99, -2: 392.00, -1: 415.30, 0: 440.00, 1: 466.16, 2: 493.88,
			 3: 523.25, 4: 554.37, 5: 587.33, 6: 622.25, 7: 659.25, 8: 698.46, 9: 739.99, 10: 783.99, 11: 830.61, 12: 880.00, 13: 932.33, 14: 987.77,
			 15: 1046.50, 16: 1108.73, 17: 1174.66, 18: 1244.51, 19: 1318.51, 20: 1396.91, 21: 1479.98, 22: 1567.98, 23: 1661.22, 24: 1760.00, 25: 1864.66, 26: 1975.53,
			 27: 2093.00, 28: 2217.46, 29: 2349.32, 30: 2489.02, 31: 2637.02, 32: 2793.83, 33: 2959.96, 34: 3135.96, 35: 3322.44, 36: 3520.00, 37: 3729.31, 38: 3951.07,
			 39: 4186.01, 40: 4434.92, 41: 4698.63, 42: 4978.03, 43: 5274.04, 44: 5587.65, 45: 5919.91, 46: 6271.93, 47: 6644.88, 48: 7040.00, 49: 7458.62, 50: 7902.13
			 }


	partes = rtttl.split(':')

	defeito_duracao, defeito_oitava, defeito_batidas = valores_defeito(partes[1])

	partes[0] = partes[0].strip()
	defeito_duracao = str(defeito_duracao).strip()
	defeito_oitava = str(defeito_oitava).strip()
	defeito_batidas = str(defeito_batidas).strip()

	print "\nNome da Música: " + partes[0]
	print "Duração: " + str(defeito_duracao)
	print "Oitava: " + str(defeito_oitava)
	print "Batidas por minuto: " + str(defeito_batidas) + "\n"


	a = []
	
	notas = partes[2].split(',')

	duracao_total = 0


	for nota in notas:

		nota = nota.strip()

		print "Nota: " + nota
		duracao_valor = duracao_separar(nota)


		if (duracao_valor == ''):
			duracao_valor = int(defeito_duracao)

		elif (duracao_valor != '1' and duracao_valor != '2' and duracao_valor != '4' and duracao_valor != '8' and duracao_valor != '16' and duracao_valor != '32'):
			sys.exit("Duração da nota não válida!\n")

			
		duracao = (4.0 / float(duracao_valor)) * (60.0 / float(defeito_batidas))


		nota_string, tem_ponto = nota_separar(nota)


		if (nota_string == ''):
			sys.exit("Tom da nota não válido!\n")


		if (tem_ponto == True):
			duracao = duracao * (3.0 / 2.0)

		print "Duração: %1.4f" % (float(duracao))
		

		if (nota_string == 'p'):
			oitava = None
			frequencia = 0

		else:
			tom = tone[nota_string]

			oitava = nota_oitava(nota)

		
			if (oitava == None):
				oitava = int(defeito_oitava)

			frequencia = freqs[12 * (oitava - 4) + tom]


		print "Oitava: " + str(oitava)
		print "Frequência: " + str(frequencia) + "\n"

		duracao_total = duracao_total + duracao

		a.append((duracao, frequencia))

		x = json_lista(a)


	print "Duração da música: " + str(duracao_total) + " seg\n"

	print str(a) + "\n"

	print x




def valores_defeito(data):
	j = 0
	
	for i in data:
		if (i == 'd' or i == 'o' or i == 'b'):
			j = j + 1

	if (j == 3):
		valores = data.split(',')
		defeito_duracao = int(valores[0].split('=')[1])
		defeito_oitava = int(valores[1].split('=')[1])
		defeito_batidas = int(valores[2].split('=')[1])

		if (defeito_duracao != 1 and defeito_duracao != 2 and defeito_duracao != 4 and defeito_duracao != 8 and defeito_duracao != 16 and defeito_duracao != 32):
			sys.exit("Duração não válida!\n")

		elif (defeito_oitava > 9):
			sys.exit("Oitava não válida!\n")

		else:
			return defeito_duracao, defeito_oitava, defeito_batidas

	else:
		return 4, 6, 63



def nota_oitava(nota):

	if str(nota[len(nota) - 1]) >= '0' and str(nota[len(nota) - 1]) <= '8':
		return int(nota[len(nota) - 1])
	else:
		return None



def nota_separar(data):
	nota = ''
	tem_ponto = False
	for i in data:
		if ((i >= 'a' and i <= 'h') or i == 'p' or i == '#'):
			nota += i
		if (i == '.'):
			tem_ponto = True

	return nota, tem_ponto



def duracao_separar(nota):

	if (nota == ''):
		sys.exit("Esta nota não contém elementos!\n")

	else:
		duracao_valor = ''

		for i in nota:

			if (i >= '0' and i <= '9'):
				duracao_valor = duracao_valor + i
				
			else:
				break

		return duracao_valor



def json_lista(a):
	c = []
	
	for (duracao, frequencia) in a:
		d = {}
		d['duracao'] = duracao
		d['frequencia'] = frequencia
		c.append(d)
	return json.dumps(c, separators=(',',':'))



main(sys.argv)