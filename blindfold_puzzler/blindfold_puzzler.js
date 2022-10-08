#! /usr/bin/env node

import fs from 'fs'
import { Chess, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK } from 'chess.js'
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

if (process.argv.length === 3 && process.argv[2] === 'seed') {
	console.log('seeding puzzles...')

	puzzles.forEach(puzzle => {
		// TODO: seed mate in 2 puzzles
		if (puzzle['mateIn'] == 2)
			return

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

		let solution = ""
		chess.moves().forEach(move => {
			chess.move(move)
			if (chess.in_checkmate()) {
				solution = move
				puzzle.solution = move
			}
			chess.undo()
		})
	})
	fs.writeFileSync('db.json', JSON.stringify(puzzles))
	console.log('done')
	process.exit(0)
}

const rl = readline.createInterface({ input, output })
while (1) {
	const puzzle = puzzles[Math.floor(Math.random() * puzzles.length)]
	console.log('white: ', puzzle.white.join(' '))
	console.log('black: ', puzzle.black.join(' '))

	let correct = false

	while (!correct) {
		const answer = await rl.question('> ')
		if (answer === 'answer') {
			console.log(puzzle.solution)
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

			console.log(chess.ascii())

			console.log()
			break
		}

		if (answer === puzzle.solution.slice(0, -1).toLowerCase()) {
			console.log('correct!\n');
			correct = true
		} else {
			console.log('incorrect, try again')
		}
	}
}
