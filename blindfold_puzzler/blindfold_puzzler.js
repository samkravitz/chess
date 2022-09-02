#! /usr/bin/env node

import fs from 'fs'
import { Chess, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE, BLACK } from 'chess.js'

const file = fs.readFileSync('db.json')
const puzzles = JSON.parse(file)

if (process.argv.length === 3 && process.argv[2] === 'seed') {
	console.log('seeding puzzles...')

	puzzles.forEach(puzzle => {
		const chess = new Chess()
		chess.clear()

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
	console.log(puzzles)
	fs.writeFileSync('db2.json', JSON.stringify(puzzles))
	console.log('done')
	process.exit(0)
}
