import numpy
import math
import random


def main():
	numpy.set_printoptions(threshold='nan', linewidth='nan')

	print "How many rows on the board?"
	boardsize = int(raw_input())
	filler = '.'.replace('"', '').replace("'", '')
	userboard = numpy.zeros((boardsize, boardsize))
	showboard = numpy.full((boardsize, boardsize), filler, dtype=numpy.dtype(numpy.str))
	computerboard = numpy.zeros((boardsize, boardsize))
	probabilityboard = numpy.empty((boardsize, boardsize))
	guessboard = numpy.ones((boardsize, boardsize))
	guessboard.fill(1)
	shippositions = userplaceship(userboard)
	numships = len(shippositions)
	compshippos = compplaceship(userboard, numships)
	compshippos = numpy.resize(compshippos, (len(compshippos) / 3, 3))

	for i in range(0, len(shippositions)):

		usercoords = (shippositions[i][0], shippositions[i][1])
		userorient = shippositions[i][2]

		compcoords = (compshippos[i][0], compshippos[i][1])
		comporient = compshippos[i][2]

		computerboard[compcoords] = 1
		userboard[usercoords] = 1

		if userorient == "N":

			userboard[int(shippositions[i][0]), int(shippositions[i][1]) + 1] = 1

		if userorient == "S":

			userboard[int(shippositions[i][0]), int(shippositions[i][1]) - 1] = 1

		if userorient == "E":

			userboard[int(shippositions[i][0]) + 1, int(shippositions[i][1])] = 1

		if userorient == "W":

			userboard[int(shippositions[i][0]) - 1, int(shippositions[i][1]) - 1] = 1

		if comporient == "N":

			computerboard[int(compshippos[i][0]), int(compshippos[i][1]) + 1] = 1

		if comporient == "S":

			computerboard[int(compshippos[i][0]), int(compshippos[i][1]) - 1] = 1

		if comporient == "E":

			computerboard[int(compshippos[i][0]) + 1, int(compshippos[i][1])] = 1

		if comporient == "W":

			computerboard[int(compshippos[i][0]) - 1, int(compshippos[i][1])] = 1

	print ""
	counter = 0

	while userboard.any() and computerboard.any():

		counter = counter + 1
		showboard2 = numpy.rot90(showboard)
		print showboard2

		usershootco = usershoot(computerboard)
		"USER SHOT...."

		if computerboard[usershootco] == 1:

			print "HIT!"
			computerboard[usershootco] = 0
			showboard[usershootco] = "H"

		else:

			print "MISS!"
			showboard[usershootco] = "X"

		probabilityboard = probability(probabilityboard, guessboard)
		compshootco = compshoot(userboard, guessboard, probabilityboard)

		guessboard[compshootco] = 0
		print "COMPUTER SHOT...."
		print compshootco

		if userboard[compshootco] == 1:

			print "HIT!"
			guessboard[compshootco] = 3
			userboard[compshootco] = 0

		else:

			print "MISS!"

	if userboard.any():
		print "USER WINS IN %d MOVES!" % (counter)

	elif computerboard.any():
		print "COMPUTER WINS IN %d MOVES!" % (counter)


def usershoot(computerboard):
	print "Shoot coordinates (without separating comma)."

	shootco = raw_input().split()
	# userboard[len(userboard) - int(shootco[0]), len(userboard) - int(shootco[1])] = 0

	return shootco


def userplaceship(userboard):
	addcheck = True
	shippositions = numpy.array([])
	print "Would you like to add ship to board?"
	while addcheck is True:
		print "Please enter ship coordinates and orientation."
		shippos = raw_input().split()
		shippositions = numpy.append(shippositions, shippos)
		print "Would you like to add another ship?"
		addanswer = raw_input()
		if addanswer != "yes" and addanswer != "Yes":
			addcheck = False

	shippositions = numpy.resize(shippositions, (len(shippositions) / 3, 3))
	movecheck = "yes"
	while movecheck == "yes" or movecheck == "Yes":
		print "Would you like to move a ship?"
		movecheck = raw_input()

		if movecheck != "yes" and movecheck != "Yes":
			break

		shippositions = usermoveship(shippositions)

	return shippositions


def usermoveship(shippositions):

	print "Please enter coordinates of ship you would like to move."
	moveship = raw_input().split()

	for i in range(0, len(shippositions)):

		shipcoords = numpy.array([shippositions[i][0], shippositions[i][1]])
		shipcoords = list(shipcoords)
		print moveship
		print shipcoords
		if moveship == shipcoords:
			print "Ship Found."
			moverow = i
			print "Please enter movement."

			moveinfo = list(raw_input())

			for i in range(0, len(moveinfo)):
				if shippositions[moverow][2] == "N":
					if moveinfo[i] == "M":
						shippositions[moverow][1] = int(shippositions[moverow][1]) + 1
					if moveinfo[i] == "R":
						shippositions[moverow][2] = "E"
					if moveinfo[i] == "L":
						shippositions[moverow][2] = "W"

				elif shippositions[moverow][2] == "S":
					if moveinfo[i] == "M":
						shippositions[moverow][1] = int(shippositions[moverow][1]) - 1
					if moveinfo[i] == "R":
						shippositions[moverow][2] = "W"
					if moveinfo[i] == "L":
						shippositions[moverow][2] = "E"

				elif shippositions[moverow][2] == "E":
					if moveinfo[i] == "M":
						shippositions[moverow][0] = int(shippositions[moverow][0]) + 1
					if moveinfo[i] == "R":
						shippositions[moverow][2] = "S"
					if moveinfo[i] == "L":
						shippositions[moverow][2] = "N"

				elif shippositions[moverow][2] == "W":
					if moveinfo[i] == "M":
						shippositions[moverow][0] = int(shippositions[moverow][0]) - 1
					if moveinfo[i] == "R":
						shippositions[moverow][2] = "N"
					if moveinfo[i] == "L":
						shippositions[moverow][2] = "S"

			print shippositions[moverow]
		else:
			print "Ship not found."

		return shippositions


def compplaceship(computerboard, numships):
	compshippos = numpy.array([])

	for i in range(0, numships):
		comporient = random.randrange(1, 4)
		if comporient == 1:
			co = "N"
		if comporient == 2:
			co = "S"
		if comporient == 3:
			co = "E"
		if comporient == 4:
			co = "W"

		ship = (random.randrange(1, len(computerboard) - 2), random.randrange(1, len(computerboard) - 2), co)
		compshippos = numpy.append(compshippos, ship)

	return compshippos


def compshoot(userboard, guessboard, probabilityboard):

	prob = 0
	for i in range(0, len(userboard)):
		for j in range(0, len(userboard)):
			if probabilityboard[i][j] > prob and guessboard[i][j] == 1:
				prob = probabilityboard[i][j]
				shootco = (i, j)

	passcheck = False
	flatprobboard = numpy.ravel(probabilityboard)
	totalsum = flatprobboard.sum()
	flatprobboard = numpy.divide(flatprobboard, totalsum)

	while passcheck is False:

		sample = numpy.random.choice(len(userboard) ** 2, p=flatprobboard)

		yco = sample % len(userboard)
		xco = math.floor(sample / len(userboard))

		shootco = (xco, yco)

		if guessboard[xco][yco] == 1:
			break

	return shootco


def probability(probabilityboard, guessboard):
	probabilityboard.fill(4)
	for i in range(0, len(guessboard)):
		for j in range(0, len(guessboard)):

			if guessboard[i][j] == 0:
				probabilityboard[i][j] = 0

			if guessboard[i][j] == 3:
				probabilityboard[i][j] = 0
				try:
					probabilityboard[i - 1][j] = probabilityboard[i - 1][j] + 4
				except:
					a = 0
				try:
					probabilityboard[i + 1][j] = probabilityboard[i + 1][j] + 4
				except:
					a = 0
				try:
					probabilityboard[i][j - 1] = probabilityboard[i][j - 1] + 4
				except:
					a = 0
				try:
					probabilityboard[i][j + 1] = probabilityboard[i][j + 1] + 4
				except:
					a = 0

			if i == 0 or guessboard[i - 1][j] == 0:
				probabilityboard[i][j] = probabilityboard[i][j] - 1

			if i == (len(guessboard) - 1) or guessboard[i + 1][j] == 0:
				probabilityboard[i][j] = probabilityboard[i][j] - 1

			if j == 0 or guessboard[i][j - 1] == 0:
				probabilityboard[i][j] = probabilityboard[i][j] - 1

			if j == (len(guessboard) - 1) or guessboard[i][j + 1] == 0:
				probabilityboard[i][j] = probabilityboard[i][j] - 1

			if probabilityboard[i][j] < 0:
				probabilityboard[i][j] = 0

	return probabilityboard


main()
