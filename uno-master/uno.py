import random

colors = ['G','Y','B','R']
nums = [num for num in range(0,10,1)]
spec =  ['SKIP','DRAW2','REVERSE']
wild = ['WILD','DRAW4']

def cardType(type,card):
	if type == 'color':
		for color in colors:
			if color in card:
				return color
		else: return None
	elif type == 'spec':
		for item in spec:
			if item in card:
				return item
		else: return None
	elif type == 'wild':
		for item in wild:
			if item in card:
				return item
	elif type == 'num':
		if cardType('spec',card) or cardType('wild',card):
			return None
		else:
			for num in nums:
				if str(num) in card:
					return str(num)
			else: return None

def allTypes(card):
	return [cardType('color',card),cardType('num',card),cardType('spec',card),cardType('wild',card)]

def isMatch(play,card):
	playTypes = allTypes(play)
	cardTypes = allTypes(card)
	matching = False
	if cardType('wild',play):
		matching = True
	else:
		for type in playTypes:
			if type:
				if type == cardTypes[playTypes.index(type)]:
					matching = True
	return matching

def buildDeck():
	deck = []
	for color in colors:
		for num in nums:
			#4 copies of each card
			deck.append(color + str(num))
			deck.append(color + str(num))
			deck.append(color + str(num))
			deck.append(color + str(num))
		for item in spec:
			deck.append(color + item)
			deck.append(color + item)
		for item in wild:
			deck.append(item)
			deck.append(item)

	random.shuffle(deck)
	return deck

print("Get ready!")

#generating hands
deck = buildDeck()
hand1 = []
hand2 = []
hand3 = []
playHand = []
allHands = [hand1, hand2, hand3, playHand]

count = 0
while count < 7:
	for hand in allHands:
		hand.append(deck[0])
		del deck[0]
		continue
	count += 1

print("You're up first!")

validStart = False
inPlay = ''
while not validStart:
	if cardType('wild',deck[0]) != 'WILD':
		inPlay = deck[0]
		print('In play: ' + str(inPlay))
		del deck[0]
		break
	else: 
		random.shuffle(deck)
		break

turn_count = 1
win = False
reverse = False
while not win:
	handMessage = ('Your hand: ' + ' '.join(playHand))
	ipMessage = 'In play: ' + str(inPlay)
	if len(deck) == 1:
		deck = buildDeck()
		random.shuffle(deck)

	ipTypes = allTypes(inPlay)

	if turn_count < 1:
		turn_count += 4

	elif turn_count == 1:
		print(handMessage)
		yourMove = input('Your move: ').upper()
		moveTypes = allTypes(yourMove)

		if yourMove.upper() == "DRAW":
			playHand.append(deck[0])
			print('You drew: ' + str(deck[0]))
			del deck[0]
			if not reverse:
				turn_count += 1
			else: turn_count += 3
			continue
		else:
			validMove = False
			while validMove == False:
				if yourMove not in playHand:
					print("This card is not in your hand")
					break
				elif not isMatch(yourMove,inPlay):
					print('This card does not match the card in play')
					break
				else: 
					validMove = True

			if validMove == True:
				playHand.remove(yourMove.upper())
				inPlay = yourMove.upper()
				if not reverse:
					nextPlayer = 'CPU1'
					nextHand = hand1
				else:
					nextPlayer = 'CPU3'
					nextHand = hand3
				if len(playHand) == 0:
					print("You win!")
					win = True
					break
				elif cardType('spec',inPlay) == 'SKIP':
					print('{} is skipped!'.format(nextPlayer))
					turn_count += 2
					continue
				elif cardType('spec',inPlay) == 'DRAW2':
					print('{} draws two!'.format(nextPlayer))
					nextHand.append(deck[0])
					del deck[0]
					nextHand.append(deck[0])
					del deck[0]
					turn_count += 2
					continue
				elif cardType('spec',inPlay) == 'REVERSE':
					print('Play is reversed!')
					reverse = not reverse
					if not reverse:
						turn_count += 1
					else: turn_count -= 1
				elif cardType('wild',inPlay):
					drawFour = False
					if cardType('wild',inPlay) == 'DRAW4':
						drawFour = True
					wildColor = input("What color do you choose?: ").upper()
					print('The color is now {}'.format(wildColor))
					inPlay = '{}^'.format(wildColor)
					if drawFour:
						print('{} draws 4!'.format(nextPlayer))
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						ipMessage = 'In play: ' + str(inPlay)
						turn_count += 2
						continue
					else: 
						ipMessage = 'In play: ' + str(inPlay)
						print(ipMessage)
						if not reverse:
							turn_count += 1
						else: turn_count -= 1
						continue
				else:
					if not reverse:
						turn_count += 1
					else: turn_count -= 1
					continue
			print(ipMessage)


	elif turn_count in range(2,5):

		if turn_count == 2:
			activePlayer = 'CPU1'
			activeHand = hand1
			if not reverse:
				nextPlayer = 'CPU2'
				nextHand = hand2
			else:
				nextPlayer = 'Player'
				nextHand = playHand

		elif turn_count == 3:
			activePlayer = 'CPU2'
			activeHand = hand2
			if not reverse:
				nextPlayer = 'CPU3'
				nextHand = hand3
			else:
				nextPlayer = 'CPU1'
				nextHand = hand1

		elif turn_count == 4:
			activePlayer = 'CPU3'
			activeHand = hand3
			if not reverse:
				nextPlayer = 'Player'
				nextHand = playHand
			else:
				nextPlayer = 'CPU2'
				nextHand = hand2

		for card in activeHand:
			if isMatch(card,inPlay):
				activeHand.remove(card)
				inPlay = card
				print('{} plays: '.format(activePlayer) + str(card))
				if cardType('spec',inPlay) == 'SKIP':
					turn_count += 2
					print('{} is skipped!'.format(nextPlayer))
					break
				elif cardType('spec',inPlay) == 'DRAW2':
					print('{} draws two!'.format(nextPlayer))
					nextHand.append(deck[0])
					del deck[0]
					nextHand.append(deck[0])
					del deck[0]
					turn_count += 2
					print(ipMessage)
					break
				elif cardType('spec',inPlay) == 'REVERSE':
					print('Play is reversed!')
					reverse = not reverse
					if not reverse:
						turn_count += 1
					else: turn_count -= 1
				elif cardType('wild',inPlay):
					drawFourCPU = False
					if cardType('wild',inPlay) == 'DRAW4':
						drawFourCPU = True
					randColor = random.choice(colors)
					inPlay = '{}^'.format(randColor)
					print('The color is now {}'.format(cardType('color',inPlay)))
					if drawFourCPU == True:
						print('{} draws 4!'.format(nextPlayer))
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						nextHand.append(deck[0])
						del deck[0]
						turn_count += 2
						break
					else: 
						if not reverse:
							turn_count += 1
						else: turn_count -= 1
						break
				print('In play: ' + str(inPlay))
				if len(activeHand) == 0:
					print('{} wins!'.format(activePlayer))
					print('Good game! Better luck next time!')
					win = True
					break
				elif len(activeHand) == 1:
					print('{} shouts UNO!'.format(activePlayer))
					turn_count += 1
					break
				else: 
					if not reverse:
						turn_count += 1
					else: turn_count -= 1
					break
		else:
			print('{} draws a card.'.format(activePlayer))
			activeHand.append(deck[0])
			del deck[0]
			if not reverse:
				turn_count += 1
			else: turn_count -= 1
			print('In play: ' + str(inPlay))
			continue

	else: turn_count -= 4

print('Thanks for playing!')