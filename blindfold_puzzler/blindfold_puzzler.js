#! /usr/bin/env node

import fs from 'fs'
import { Chess, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK } from 'chess.js'
import jsChessEngine from 'js-chess-engine'
import * as readline from 'node:readline/promises'
import { stdin as input, stdout as output } from 'node:process'

const file = fs.readFileSync('db.json')
const puzzles = JSON.parse(file)

const getPieceFromMove = (move) => {
	switch (move.charAt(0)) {
		case 'P': return PAWN
		case 'N': return KNIGHT
		case 'B': return BISHOP
		case 'R': return ROOK
		case 'Q': return QUEEN
		case 'K': return KING
	}
}

const createChess = (puzzle) => {
	const chess = new Chess()
	chess.clear()
	puzzle.white.forEach(move => {
		const piece = getPieceFromMove(move);
		const square = move.substring(1)
		chess.put({ type: piece, color: WHITE }, square)
	})

	puzzle.black.forEach(move => {
		const piece = getPieceFromMove(move);
		const square = move.substring(1)
		chess.put({ type: piece, color: BLACK }, square)
	})

	return chess
}

if (process.argv.length === 3 && process.argv[2] === 'seed') {
	console.log('seeding puzzles...')

	puzzles.forEach(puzzle => {
		const chess = new Chess()
		chess.clear()

		puzzle.white.forEach(move => {
			const piece = getPieceFromMove(move);
			const square = move.substring(1)
			chess.put({ type: piece, color: WHITE }, square)
		})

		puzzle.black.forEach(move => {
			const piece = getPieceFromMove(move);
			const square = move.substring(1)
			chess.put({ type: piece, color: BLACK }, square)
		})

		console.log('seeding: ', puzzle)

		let mateIn = 0
		while (1) {
			mateIn += 1

			let aiMove = jsChessEngine.aiMove(chess.fen())
			let from = Object.keys(aiMove)[0].toLowerCase()
			let to = aiMove[Object.keys(aiMove)[0]].toLowerCase()
			chess.move({ from, to })

			if (chess.in_checkmate())
				break

			aiMove = jsChessEngine.aiMove(chess.fen())
			from = Object.keys(aiMove)[0].toLowerCase()
			to = aiMove[Object.keys(aiMove)[0]].toLowerCase()
			chess.move({ from, to })
		}

		puzzle['mateIn'] = mateIn
	})
	fs.writeFileSync('db.json', JSON.stringify(puzzles))
	console.log('done')
	process.exit(0)
}

const rl = readline.createInterface({ input, output })
while (1) {
	const puzzle = puzzles[Math.floor(Math.random() * puzzles.length)]
	if (!puzzle['solution'])
		continue
	
	console.log(`white: ${puzzle.white.join(' ')}`)
	console.log(`black: ${puzzle.black.join(' ')}`)
	console.log(`mate in ${puzzle['mateIn']}`)

	while (1) {
		let chess = createChess(puzzle)
		let correct = false

		while (!correct) {
			const answer = await rl.question('> ')

			// give answer
			if (answer === 'a' || answer === 'answer') {

			}

			// show board
			else if (answer === 'h' || answer === 'hint') {
				console.log(chess.ascii())
			}

			// quit
			else if (answer === 'q' || answer === 'quit') {
				process.exit(0)
			}

			// reset puzzle
			else if (answer === 'r' || answer === 'reset') {
				chess = createChess(puzzle)
				console.log(`white: ${puzzle.white.join(' ')}`)
				console.log(`black: ${puzzle.black.join(' ')}`)
				console.log(`mate in ${puzzle['mateIn']}`)
			}

			else {
				if (!chess.move(answer)) {
					console.log('Illegal move.')
					continue
				}

				if (chess.in_checkmate()) {
					console.log('Correct!')
					correct = true
				} else {
					console.log(`fen: ${chess.fen()}`);
					const aiMove = jsChessEngine.aiMove(chess.fen())
					const from = Object.keys(aiMove)[0].toLowerCase()
					const to = aiMove[Object.keys(aiMove)[0]].toLowerCase()
					const movedPiece = chess.get(from)
					let movedPieceString = movedPiece.type.toUpperCase()
					if (movedPiece === 'P')
						movedPieceString = ''

					console.log(`black plays ${movedPieceString}${to}`)
					chess.move({ from, to })
				}
			}
		}
	}
}
